# This file is Originally Written By @okay-retard on GitHub
# The Author (Jayant Kageri) just Ported this for Devloper Userbot
# (C) 2021 Jayant Kageri

import logging
import sys
import time
import pyromod.listen
from pyrogram import Client, errors
from config import API_HASH, API_ID, PY_SESSION
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

LOGGER = logging.getLogger("pyrogram").setLevel(logging.WARNING)


HELP = {}
CMD_HELP = {}

StartTime = time.time()

API_ID = API_ID
API_HASH = API_HASH
PY_SESSION = PY_SESSION

app = Client(PY_SESSION, api_id=API_ID, api_hash=API_HASH)
