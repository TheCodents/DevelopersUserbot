# This file is taken from @pyrogram on GitHub
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
"""
    }
)


SCHEMA = "https"
BASE = "nekobin.com"
ENDPOINT = f"{SCHEMA}://{BASE}/api/documents"
ANSWER = "Pasted to Nekobin \n{}"
TIMEOUT = 3
MESSAGE_ID_DIFF = 100


@app.on_message(
    filters.command(["neko", "nekobin", "bin", "paste"], PREFIX) & filters.me
)
async def neko(_, message: Message):
    reply = message.reply_to_message
    if not reply:
        return
    async with aiohttp.ClientSession() as session:
        async with session.post(
            ENDPOINT,
            json={"content": reply.text},
            timeout=TIMEOUT
        ) as response:
            key = (await response.json())["result"]["key"]
    await message.edit(ANSWER.format(f"{BASE}/{key}.py"))
