# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import asyncio

import aiohttp
from pyrogram import filters
from pyrogram.types import Message
from _pyrogram import app, CMD_HELP
from config import PREFIX

CMD_HELP.update(
    {
        "Misc": """
**Misc**
  `paste` -> Paste replied content to nekobin.com.
  `tr` [lang code] -> Transalte a text to a given language.
  `info` [user handle] -> Provides information about the user.
  `id` [user handle] -> Give user or chat id
  `restart` -> Restart the Clients
  `load -p` -> To Install/Load Pyrogram Plugins
  `load -t` -> To Install/Load Telethon Plugins
"""
    }
)


@app.on_message(
    filters.command(["neko", "nekobin", "bin", "paste"], PREFIX) & filters.me
)
async def paste(_, message: Message):
    text = message.reply_to_message.text
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://nekobin.com/api/documents", json={"content": text}, timeout=3
            ) as response:
                key = (await response.json())["result"]["key"]
    except Exception:
        await message.edit_text("`Pasting failed`")
        await asyncio.sleep(2)
        await message.delete()
        return
    else:
        url = f"https://nekobin.com/{key}"
        reply_text = f"Pasted to Nekobin : {url}"
        delete = (
            True
            if len(message.command) > 1
            and message.command[1] in ["d", "del"]
            and message.reply_to_message.from_user.is_self
            else False
        )
        if delete:
            await asyncio.gather(
                app.send_message(
                    message.chat.id, reply_text, disable_web_page_preview=True
                ),
                message.reply_to_message.delete(),
                message.delete(),
            )
        else:
            await message.edit_text(
                reply_text,
                disable_web_page_preview=True,
            )
