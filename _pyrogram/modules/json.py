from pyrogram.types import *
from _pyrogram import *
from pyrogram import *

@app.on_message(filters.command("json", PREFIX) & filters.me)
async def start(client, message):
	if message.reply_to_message:
		await message.reply(message.reply_to_message)
	else:
		await message.reply(message)
