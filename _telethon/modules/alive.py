import sys
import time
from datetime import datetime
from io import BytesIO
import requests
from PIL import Image
from telethon import __version__ as __tele_version__
from telethon import events, TelegramClient
from _telethon import app, StartTime
from config import PREFIX

def get_readable_time(seconds: int) -> str:
    count = 0
    ping_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]

    while count < 4:
        count += 1
        if count < 3:
            remainder, result = divmod(seconds, 60)
        else:
            remainder, result = divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)

    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        ping_time += time_list.pop() + ", "

    time_list.reverse()
    ping_time += ":".join(time_list)

    return ping_time

__python_version__ = f"{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]}"


@app.on(events.NewMessage(outgoing=True, pattern=f"^{PREFIX}alive (.*)"))
async def alive_t(event):
    if "-t" in event.text:
        pass
    else:
        return
    start = datetime.now()
    end = datetime.now()
    (end - start).microseconds / 1000
    uptime = get_readable_time((time.time() - StartTime))
    reply_msg = f"**[Developer](https://github.com/TheCodents/DevelopersUserbot)**\n"
    reply_msg += f"Python Version: `{__python_version__}`\n"
    reply_msg += f"Telethon Version: `{__tele_version__}`\n"
    end_time = time.time()
    reply_msg += f"\nUptime: {uptime}"
    await event.edit(reply_msg)

@app.on(events.NewMessage(outgoing=True, pattern=f"^{PREFIX}ping (.*)"))
async def _(event):
    if "-t" in event.text:
        pass
    else:
        return
    start = datetime.now()
    end = datetime.now()
    ms = (end - start).microseconds / 1000
    await event.edit(f"Pong!\n`{ms} ms`")
