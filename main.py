
import multiprocessing

from _telethon import app as ttapp
from _pyrogram import app as pgapp
    
def prun(pclient, **args):# kinda weird
    pclient.run()
    
if __name__ == "__main__":
    multiprocessing.Process(target=prun, args=(pgapp, True)).start()
    ttapp.run_until_disconnected()
