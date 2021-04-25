# This file is Originally Written By @SpEcHiDe on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import os
from importlib import import_module, reload
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.handlers.handler import Handler
from _pyrogram import LOGGER, app
from config import PREFIX

@app.on_message(filters.command("load -p", PREFIX) & filters.me)
async def load_plugin(client: Client, message: Message):
    status_message = await message.reply("...")
    try:
        if message.reply_to_message is not None:
            down_loaded_plugin_name = await message.reply_to_message.download(
                file_name="./modules/"
            )
            if down_loaded_plugin_name is not None:
                # LOGGER.info(down_loaded_plugin_name)
                relative_path_for_dlpn = os.path.relpath(
                    down_loaded_plugin_name,
                    os.getcwd()
                )
                # LOGGER.info(relative_path_for_dlpn)
                lded_count = 0
                path = Path(relative_path_for_dlpn)
                module_path = ".".join(
                    path.parent.parts + (path.stem,)
                )
                # LOGGER.info(module_path)
                module = reload(import_module(module_path))
                # https://git.io/JvlNL
                for name in vars(module).keys():
                    # noinspection PyBroadException
                    try:
                        handler, group = getattr(module, name).handler

                        if isinstance(handler, Handler) and isinstance(group, int):
                            client.add_handler(handler, group)
                            LOGGER.info(
                                '[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                    client.session_name,
                                    type(handler).__name__,
                                    name,
                                    group,
                                    module_path
                                )
                            )
                            lded_count += 1
                    except Exception:
                        pass
                await status_message.edit(
                    f"Loded {lded_count} in Pyrogram User Client"
                )
    except Exception as error:
        await status_message.edit(
            f"ERROR: <code>{error}</code>"
        )
