# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import math
from datetime import datetime
import asyncio
from pyrogram import filters
from pyrogram.types import Message
from inspect import getfullargspec
from _pyrogram import app
from config import PREFIX

async def edrep(msg: Message, **kwargs):
    func = msg.edit_text if msg.from_user.is_self else msg.reply
    spec = getfullargspec(func.__wrapped__).args
    await func(**{k: v for k, v in kwargs.items() if k in spec})


async def admin_check(message: Message) -> bool:
    client = message._client
    chat_id = message.chat.id
    user_id = message.from_user.id

    check_status = await client.get_chat_member(chat_id=chat_id, user_id=user_id)
    admin_strings = ["creator", "administrator"]
    return check_status.status in admin_strings


@app.on_message(filters.command("purge", PREFIX) & filters.me)
async def purge_message(client, message):
    if message.chat.type in (("supergroup", "channel")):
        is_admin = await admin_check(message)
        if not is_admin:
            await message.delete()
            return
    else:
        pass
    start_t = datetime.now()
    await message.delete()
    message_ids = []
    count_del_etion_s = 0
    if message.reply_to_message:
        for a_s_message_id in range(
            message.reply_to_message.message_id, message.message_id
        ):
            message_ids.append(a_s_message_id)
            if len(message_ids) == 100:
                await client.delete_messages(
                    chat_id=message.chat.id, message_ids=message_ids, revoke=True
                )
                count_del_etion_s += len(message_ids)
                message_ids = []
        if message_ids:
            await client.delete_messages(
                chat_id=message.chat.id, message_ids=message_ids, revoke=True
            )
            count_del_etion_s += len(message_ids)
    end_t = datetime.now()
    time_taken_ms = (end_t - start_t).seconds
    ms_g = await client.send_message(
        message.chat.id,
        f"Purged {count_del_etion_s} messages in {time_taken_ms} seconds",
    )
    await asyncio.sleep(5)
    await ms_g.delete()


@app.on_message(filters.command("del", PREFIX) & filters.me)
async def delete_replied(client, message):
    msg_ids = [message.message_id]
    if message.reply_to_message:
        msg_ids.append(message.reply_to_message.message_id)
    await client.delete_messages(message.chat.id, msg_ids)
