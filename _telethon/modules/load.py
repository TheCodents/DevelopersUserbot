# This file is taken from UniBorg
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import asyncio
import traceback
import os
from datetime import datetime
from _telethon import app
from _telethon import load_plugins as load_module

DELETE_TIMEOUT = 5

@app.on(events.NewMessage(outgoing=True, pattern=f"^{PREFIX}load (.*)"))
async def install_plug_in(event):
async def install(event):
    if event.fwd_from:
        return
    if event.reply_to_msg_id:
        try:
            downloaded_file_name = await event.client.download_media(  # pylint:disable=E0602
                await event.get_reply_message(),
                "_telethon/modules/"  # pylint:disable=E0602
            )
            if "(" not in downloaded_file_name:
                path1 = Path(downloaded_file_name)
                shortname = path1.stem
                load_module(shortname.replace(".py", ""))
                await event.edit("Installed Plugin `{}`".format(os.path.basename(downloaded_file_name)))
            else:
                os.remove(downloaded_file_name)
                await event.edit("Errors! This plugin is already installed/pre-installed Hmm As Usual My Owner Is Some Mental.")
        except Exception as e:  # pylint:disable=C0103,W0703
            await event.edit(str(e))
            os.remove(downloaded_file_name)
    await asyncio.sleep(DELETE_TIMEOUT)


def load_module(shortname):
    if shortname.startswith("__"):
        pass
    elif shortname.endswith("_"):
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"_telethon/modules/{shortname}.py")
        name = "_telethon.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    else:
        import sys
        import importlib
        from pathlib import Path
        path = Path(f"_telethon/modules/{shortname}.py")
        name = "_telethon.modules.{}".format(shortname)
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["_telethon.modules."+shortname] = mod
