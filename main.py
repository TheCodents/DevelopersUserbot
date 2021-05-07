import multiprocessing

from _telethon import app as tapp
from _pyrogram import app as papp

def trun(tclient):
    tclient.run_until_disconnected()
    
def prun(pclient):
    pclient.run()
    
multiprocessing.Process(target=trun, args=(tapp)).start()
prun(papp)
