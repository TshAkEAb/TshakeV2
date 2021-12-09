from pyrogram import Client, filters

from utlis.rank import setrank ,isrank ,remrank ,setsudos ,remsudos ,setsudo
from handlers.callback import updateCallback
from handlers.msg import updateHandlers
from handlers.inline import updateInline
from handlers.delete import delete
from utlis.tg import Bot,Del24
from handlers.edit import edit
from utlis.locks import GPck
from handlers.nf import nf
from config import *

import threading, requests, time, random
import redis
import sched, time ,os

R = redis.Redis(charset="utf-8", decode_responses=True)
if not os.path.isdir('./files'):
    os.mkdir("./files")
    
app = Client("NB"+BOT_ID,bot_token=TOKEN,api_id = API_ID, api_hash = API_HASH)
setsudo(R,SUDO)
R.set("{}Nbot:BOTrank".format(BOT_ID), BOT_ID)

if R.get("{}:Nbot:restart".format(BOT_ID)):
  Bot("sendMessage",{"chat_id":R.get("{}:Nbot:restart".format(BOT_ID)),"text":"تم اعادة تشغيل البوت - Done restart the bot","parse_mode":"html"})
  R.delete("{}:Nbot:restart".format(BOT_ID))
  
  
t = threading.Thread(target=Del24,args=("clonsft", "message",R))
t.daemon = True
t.start()

t = threading.Thread(target=GPck,args=("client", "message",R))
t.daemon = True
t.start()
@app.on_inline_query()
def answer(client, inline_query):
    t = threading.Thread(target=updateInline,args=(client, inline_query,R))
    t.daemon = True
    t.start()

@app.on_message(~filters.edited & ~filters.new_chat_title & ~filters.pinned_message & ~filters.left_chat_member & ~filters.new_chat_photo & ~filters.new_chat_members & ~filters.delete_chat_photo & ~filters.channel)
def update(client, message):
    t = threading.Thread(target=updateHandlers,args=(client, message,R))
    t.daemon = True
    t.start()
@app.on_callback_query()
def callback(client, callback_query ):
    t = threading.Thread(target=updateCallback,args=(client, callback_query,R))
    t.daemon = True
    t.start()
@app.on_message(filters.edited & ~filters.channel)
def updateEdit(client, message):
    t = threading.Thread(target=edit,args=(client, message,R))
    t.daemon = True
    t.start()
@app.on_message(filters.new_chat_title | filters.pinned_message | filters.left_chat_member | filters.new_chat_photo | filters.new_chat_members | filters.delete_chat_photo & ~filters.channel)
def updateEdit(client, message):
    t = threading.Thread(target=nf,args=(client, message,R))
    t.daemon = True
    t.start()

app.run()
