import sys
import glob
import logging
import importlib
from pathlib import Path
from telethon import TelegramClient, events
from _telethon import app, LOGGER
from _telethon.modules import *

def load_plugins(plugin_name):
    path = Path(f"_telethon/modules/{plugin_name}.py")
    name = "_telethon.modules.{}".format(plugin_name)
    spec = importlib.util.spec_from_file_location(name, path)
    load = importlib.util.module_from_spec(spec)
    load.logger = logging.getLogger(plugin_name)
    spec.loader.exec_module(load)
    sys.modules["_telethon.modules." + plugin_name] = load

path = "_telethon/modules/*.py"
files = glob.glob(path)
for name in files:
    with open(name) as a:
        patt = Path(a.name)
        plugin_name = patt.stem
        load_plugins(plugin_name.replace(".py", ""))

app.start()
print("Telethon User Client Started \nPowered By @TheCodents\n(C) 2021 Jayant Kageri")
app.run_until_disconnected()
