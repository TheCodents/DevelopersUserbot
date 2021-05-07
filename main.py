import multiprocessing

from _telethon import app as tapp
from _pyrogram import app as papp
    
def prun(pclient, useless):# kinda weird
    what = useless
    pclient.run()
    
if __name__ == "__main__":
    multiprocessing.Process(target=prun, args=(papp, True)).start()
    # await tapp.connect()
    tapp.run_until_disconnected()
