
import multiprocessing

from _telethon import app as ttapp
from _pyrogram import app as pgapp

def trun(tclient):
    tclient.run_until_disconnected()
    
def prun(pclient):
    pclient.run()
    
multiprocessing.Process(target=trun, args=(ttapp)).start()
prun(pgapp)
