# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import os
from datetime import datetime

from pyrogram import filters
from pyrogram.types import User, InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.raw import functions
from pyrogram.errors import PeerIdInvalid
from _pyrogram import app
from config import PREFIX


def ReplyCheck(message: Message):
    reply_id = None

    if message.reply_to_message:
        reply_id = message.reply_to_message.message_id

    elif not message.from_user.is_self:
        reply_id = message.message_id

    return reply_id


infotext = (
    "**[{full_name}](tg://user?id={user_id})**\n"
    "    > User ID: `{user_id}`\n"
    "    > First Name: `{first_name}`\n"
    "    > Last Name: `{last_name}`\n"
    "    > Username: @{username}\n"
)


def FullName(user: User):
    return user.first_name + " " + user.last_name if user.last_name else user.first_name


@app.on_message(filters.command("info", PREFIX) & filters.me)
async def whois(client, message):
    cmd = message.command
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except Exception as e:
        await message.edit(f"{e}")
        return
    await message.edit_text(
    infotext.format(
        full_name=FullName(user),
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name or "",
        username=user.username or "",
    ),
            disable_web_page_preview=True,
        )


@app.on_message(filters.command("id", PREFIX) & filters.me)
async def id(client, message):
    cmd = message.command
    chat_id = message.chat.id
    if not message.reply_to_message and len(cmd) == 1:
        get_user = message.from_user.id
    elif len(cmd) == 1:
        get_user = message.reply_to_message.from_user.id
    elif len(cmd) > 1:
        get_user = cmd[1]
        try:
            get_user = int(cmd[1])
        except ValueError:
            pass
    try:
        user = await client.get_users(get_user)
    except Exception as e:
        await message.edit(f"{e}")
        return
    if message.chat.username:
        chat_78 = f"[**Chat ID**](https://t.me/{message.chat.username}): `{message.chat.id}`"
    else:
        chat_78 = f"**Chat ID**: `{message.chat.id}`"
    text = f"""{chat_78} \n[**Message ID**](https://t.me/{message.chat.id}/{message.message_id}): `{message.message_id}`\n[**User ID**](tg://user?id={user.id}):`{user.id}`\n"""
    await message.edit(text)
