# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import heroku3
import asyncio
import sys
from os import environ, execle, path, remove
from config import HEROKU_API, HEROKU_APP_NAME, PREFIX

from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError, NoSuchPathError

from pyrogram import filters
from _pyrogram import app, CMD_HELP
from _pyrogram.helpers.pyrohelper import get_arg

CMD_HELP.update(
    {
        "Heroku": """
**Heroku**
  `update`-> Updates the userbot to latest build.
  `restart` -> To Restart the Userbot
  `logs` -> To Get Heroku Logs"""
    }
)

UPSTREAM_REPO_URL = "https://github.com/TheCodents/DevelopersUserbot"
requirements_path = path.join(
    path.dirname(path.dirname(path.dirname(__file__))), "requirements.txt"
)


async def gen_chlog(repo, diff):
    ch_log = ""
    d_form = "On %d/%m/%y at %H:%M:%S"
    for c in repo.iter_commits(diff):
        ch_log += f"**#{c.count()}** : {c.committed_datetime.strftime(d_form)} : [{c.summary}]({UPSTREAM_REPO_URL.rstrip('/')}/commit/{c}) by `{c.author}`\n"
    return ch_log


async def updateme_requirements():
    reqs = str(requirements_path)
    try:
        process = await asyncio.create_subprocess_shell(
            " ".join([sys.executable, "-m", "pip", "install", "-r", reqs]),
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        await process.communicate()
        return process.returncode
    except Exception as e:
        return repr(e)


@app.on_message(filters.command("update", PREFIX) & filters.me)
async def upstream(client, message):
    status = await message.edit("`Checking for updates, please wait....`")
    conf = get_arg(message)
    off_repo = UPSTREAM_REPO_URL
    try:
        txt = "`Oops.. Updater cannot continue due to "
        txt += "some problems occured`\n\n**LOGTRACE:**\n"
        repo = Repo()
    except NoSuchPathError as error:
        await status.edit(f"{txt}\n`directory {error} is not found`")
        repo.__del__()
        return
    except GitCommandError as error:
        await status.edit(f"{txt}\n`Early failure! {error}`")
        repo.__del__()
        return
    except InvalidGitRepositoryError as error:
        if conf != "now":
            pass
        repo = Repo.init()
        origin = repo.create_remote("upstream", off_repo)
        origin.fetch()
        repo.create_head("master", origin.refs.master)
        repo.heads.master.set_tracking_branch(origin.refs.master)
        repo.heads.master.checkout(True)
    ac_br = repo.active_branch.name
    if ac_br != "master":
        await status.edit(
            f"**[UPDATER]:**` You are on ({ac_br})\n Please change to master branch.`"
        )
        repo.__del__()
        return
    try:
        repo.create_remote("upstream", off_repo)
    except BaseException:
        pass
    ups_rem = repo.remote("upstream")
    ups_rem.fetch(ac_br)
    changelog = await gen_chlog(repo, f"HEAD..upstream/{ac_br}")
    if "now" not in conf:
        if changelog:
            changelog_str = f"**New UPDATE available for [[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br}):\n\nCHANGELOG**\n\n{changelog}"
            if len(changelog_str) > 4096:
                await status.edit("`Changelog is too big, view the file to see it.`")
                file = open("output.txt", "w+")
                file.write(changelog_str)
                file.close()
                await app.send_document(
                    message.chat.id,
                    "output.txt",
                    caption=f"Do {PREFIX}`update now` to update.",
                    reply_to_message_id=status.message_id,
                )
                remove("output.txt")
            else:
                return await status.edit(
                    f"{changelog_str}\n\nDo `.update now` to update.",
                    disable_web_page_preview=True,
                )
        else:
            await status.edit(
                f"\n`Your BOT is`  **up-to-date**  `with`  **[[{ac_br}]]({UPSTREAM_REPO_URL}/tree/{ac_br})**\n",
                disable_web_page_preview=True,
            )
            repo.__del__()
            return
    if HEROKU_API is not None:
        import heroku3

        heroku = heroku3.from_key(HEROKU_API)
        heroku_app = None
        heroku_applications = heroku.apps()
        if not HEROKU_APP_NAME:
            await status.edit(
                "`Please set up the HEROKU_APP_NAME variable to be able to update userbot.`"
            )
            repo.__del__()
            return
        for app in heroku_applications:
            if app.name == HEROKU_APP_NAME:
                heroku_app = app
                break
        if heroku_app is None:
            await status.edit(
                f"{txt}\n`Invalid Heroku credentials for updating userbot dyno.`"
            )
            repo.__del__()
            return
        await status.edit(
            "`Userbot dyno build in progress, please wait for it to complete.`"
        )
        ups_rem.fetch(ac_br)
        repo.git.reset("--hard", "FETCH_HEAD")
        heroku_git_url = heroku_app.git_url.replace(
            "https://", "https://api:" + HEROKU_API + "@"
        )
        if "heroku" in repo.remotes:
            remote = repo.remote("heroku")
            remote.set_url(heroku_git_url)
        else:
            remote = repo.create_remote("heroku", heroku_git_url)
        try:
            remote.push(refspec=f"HEAD:refs/heads/{ac_br}", force=True)
        except GitCommandError as error:
            pass
        await status.edit("`Successfully Updated!\nRestarting, please wait...`")
    else:
        # Classic Updater, pretty straightforward.
        try:
            ups_rem.pull(ac_br)
        except GitCommandError:
            repo.git.reset("--hard", "FETCH_HEAD")
        await updateme_requirements()
        await status.edit(
            "`Successfully Updated!\nBot is restarting... Wait for a second!`",
        )
        # Spin a new instance of bot
        args = [sys.executable, "./resources/startup/deploy.sh"]
        execle(sys.executable, *args, environ)
        return

@app.on_message(filters.command("restart", PREFIX) & filters.me)
async def restart(client, message):
    try:
        await message.edit("Restarting your Userbot, It will take few minutes, Please Wait")
        heroku_conn = heroku3.from_key(HEROKU_API)
        server = heroku_conn.app(HEROKU_APP_NAME)
        server.restart()
    except Exception as e:
        await message.edit(f"Your `HEROKU_APP_NAME` or `HEROKU_API` is Wrong or Not Filled, Please Make it correct or fill it \n\nError: ```{e}```")


@app.on_message(filters.command("logs", PREFIX) & filters.me)
async def log(client, message):
    try:
        await message.edit("Getting Logs")
        heroku_conn = heroku3.from_key(HEROKU_API)
        server = heroku_conn.get_app_log(HEROKU_APP_NAME, dyno='pyrogram.1', lines=100, source='app', timeout=100)
        log = heroku_conn.get_app_log(HEROKU_APP_NAME, dyno='telethon.1', lines=100, source='app', timeout=100)
        f_logs = server + "\n\n===================================================================================================================================================\n\n" + log

        if len(f_logs) > 4096:
            file = open("logs.txt", "w+")
            file.write(f_logs)
            file.close()
            await app.send_document(
                message.chat.id,
                "logs.txt",
                caption=f"Logs for {HEROKU_APP_NAME}",
                
            )
            remove("logs.txt")

    except Exception as e:
        await message.edit(f"{e}")
