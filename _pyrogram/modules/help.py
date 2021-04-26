# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

from pyrogram import filters
from _pyrogram import app, HELP, CMD_HELP
from config import PREFIX
from _pyrogram.helpers.pyrohelper import get_arg

HELP.update(
    {
        "**Admin Tools**": "__ban, unban, promote, demote, kick, mute, unmute, pin, purge, del, invite__",
        "**Alive**": "__alive, ping__",
        "**Developer**": "__peval, teval, term__",
        "**Misc**": "__paste, tr, info, id__",
        "**Heroku**": "__update, restart, logs__",
    }
)


@app.on_message(filters.command("help", PREFIX) & filters.me)
async def help(client, message):
    args = get_arg(message)
    if not args:
        text = "**Available Commands**\n\n"
        for key, value in HELP.items():
            text += f"{key}: {value}\n\n"
        await message.edit(text)
        return
    else:
        module_help = CMD_HELP.get(args, False)
        if not module_help:
            await message.edit("__Invalid module name specified.__")
            return
        else:
            await message.edit(module_help)
