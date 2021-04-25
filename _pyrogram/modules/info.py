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
    text_unping = '<b>Chat ID:</b>'
    if message.chat.username:
        text_unping = f'<a href="https://t.me/{message.chat.username}">{text_unping}</a>'
    text_unping += f' <code>{message.chat.id}</code>\n'
    text = '<b>Message ID:</b>'
    if message.link:
        text = f'<a href="{message.link}">{text}</a>'
    text += f' <code>{message.message_id}</code>\n'
    text_unping += text
    if message.from_user:
        text_unping += f'<b><a href="tg://user?id={message.from_user.id}">User ID:</a></b> <code>{message.from_user.id}</code>\n'
    text_ping = text_unping
    reply = message.reply_to_message
    if not getattr(reply, 'empty', True):
        text_unping += '\n'
        text = '<b>Replied Message ID:</b>'
        if reply.link:
            text = f'<a href="{reply.link}">{text}</a>'
        text += f' <code>{reply.message_id}</code>\n'
        text_unping += text
        text_ping = text_unping
        if reply.from_user:
            text = '<b>Replied User ID:</b>'
            if reply.from_user.username:
                text = f'<a href="https://t.me/{reply.from_user.username}">{text}</a>'
            text += f' <code>{reply.from_user.id}</code>\n'
            text_unping += text
            text_ping += f'<b><a href="tg://user?id={reply.from_user.id}">Replied User ID:</a></b> <code>{reply.from_user.id}</code>\n'
        if reply.forward_from:
            text_unping += '\n'
            text = '<b>Forwarded User ID:</b>'
            if reply.forward_from.username:
                text = f'<a href="https://t.me/{reply.forward_from.username}">{text}</a>'
            text += f' <code>{reply.forward_from.id}</code>\n'
            text_unping += text
            text_ping += f'\n<b><a href="tg://user?id={reply.forward_from.id}">Forwarded User ID:</a></b> <code>{reply.forward_from.id}</code>\n'
    reply = await message.edit(text_unping, disable_web_page_preview=True)
    if text_unping != text_ping:
        await message.edit(text_ping, disable_web_page_preview=True)
