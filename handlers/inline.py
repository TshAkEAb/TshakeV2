from utlis.rank import setrank,isrank,remrank,remsudos,setsudo,GPranks,IDrank
from utlis.send import send_msg, BYusers, Sendto, fwdto,Name,Glang
from utlis.locks import st,getOR,Clang,st_res
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,datetime
import importlib


from os import listdir
from os.path import isfile, join

def updateInline(client, inline_query,redis):
  if redis.smembers("{}Nbot:botfiles".format(BOT_ID)):
    onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
    filesR = redis.smembers("{}Nbot:botfiles".format(BOT_ID))
    for f in onlyfiles:
      if f in filesR:
        fi = f.replace(".py","")
        UpMs= "files."+fi
        try:
          U = importlib.import_module(UpMs)
          t = threading.Thread(target=U.updateIn,args=(client, inline_query,redis))
          t.daemon = True
          t.start()
          importlib.reload(U)
        except Exception as e:
          pass

