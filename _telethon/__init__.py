import time
from datetime import datetime
import logging
from telethon import TelegramClient, events
from telethon.sessions import StringSession
from config import *

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

LOGGER = logging.getLogger(__name__)
StartTime = time.time()
app = TelegramClient(StringSession(TE_SESSION), api_id=API_ID, api_hash=API_HASH)
