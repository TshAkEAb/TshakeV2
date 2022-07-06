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

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, importlib
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

@app.on_message(~filters.new_chat_title & ~filters.pinned_message & ~filters.left_chat_member & ~filters.new_chat_photo & ~filters.new_chat_members & ~filters.delete_chat_photo & ~filters.channel)
def update(client, message):
    t = threading.Thread(target=updateHandlers,args=(client, message,R))
    t.daemon = True
    t.start()
@app.on_callback_query()
def callback(client, callback_query ):
    t = threading.Thread(target=updateCallback,args=(client, callback_query,R))
    t.daemon = True
    t.start()
@app.on_edited_message(~filters.channel)
def updateEdit(client, message):
    t = threading.Thread(target=edit,args=(client, message,R))
    t.daemon = True
    t.start()
@app.on_message(filters.new_chat_title | filters.pinned_message | filters.left_chat_member | filters.new_chat_photo | filters.new_chat_members | filters.delete_chat_photo & ~filters.channel)
def updateEdit(client, message):
    t = threading.Thread(target=nf,args=(client, message,R))
    t.daemon = True
    t.start()

def updateAuto(client, message,redis):
    chatID = message.chat.id
    userID = message.from_user.id
    c = importlib.import_module("lang.arcmd")
    r = importlib.import_module("lang.arreply")
    group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
    if group is False and redis.get("{}Nbot:autoaddbot".format(BOT_ID)):
        if redis.get("{}Nbot:autoaddbotN".format(BOT_ID)):
            auN = int(redis.get("{}Nbot:autoaddbotN".format(BOT_ID)))
        else:
            auN = 1
        m = message.new_chat_member
        if not m.privileges.can_change_info or not m.privileges.can_delete_messages or not m.privileges.can_invite_users or not m.privileges.can_restrict_members or not m.privileges.can_pin_messages:
            Bot("sendMessage",{"chat_id":chatID,"text":r.GiveMEall,"parse_mode":"html"})
            return False
        title = message.chat.title
        if not redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),chatID):
            locksarray = {'Llink','Llongtext','Lmarkdown','Linline','Lfiles','Lcontact','Lbots','Lfwd','Lnote'}
            for lock in locksarray:
                redis.sadd("{}Nbot:{}".format(BOT_ID,lock),chatID)
            ads = Bot("getChatAdministrators",{"chat_id":chatID})
            for ad in ads['result']:
                userId = ad["user"]["id"]
                userFn = ad["user"]["first_name"]
                if ad['status'] == "administrator" and int(userId) != int(BOT_ID):
                    setrank(redis,"admin",userId,chatID,"array")
                if ad['status'] == "creator":
                    setrank(redis,"malk",userId,chatID,"one")
            add = redis.sadd("{}Nbot:groups".format(BOT_ID),chatID)
            Bot("exportChatInviteLink",{"chat_id":chatID})
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.MoreInfo, url="t.me/zx_xx")]])
            Bot("sendMessage",{"chat_id":chatID,"text":r.doneadd.format(title),"parse_mode":"markdown","reply_markup":kb})
            sendTO = (redis.get("{}Nbot:sudogp".format(BOT_ID)) or SUDO)
            get = (redis.hget("{}Nbot:links".format(BOT_ID),chatID) or GetLink(chatID) or "https://t.me/zx_xx")
            kb = InlineKeyboardMarkup([[InlineKeyboardButton("الرابط 🖇", url=get)]])
            BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,message.from_user.first_name)
            Bot("sendMessage",{"chat_id":sendTO,"text":f"تم تفعيل مجموعه جديدة ℹ️\nاسم المجموعه : {title}\nايدي المجموعه : {chatID}\nالمنشئ : {BY}\n⎯ ⎯ ⎯ ⎯","parse_mode":"html","reply_markup":kb})
        elif redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),chatID):
            redis.sadd("{}Nbot:groups".format(BOT_ID),chatID)
            redis.srem("{}Nbot:disabledgroups".format(BOT_ID),chatID)
            redis.hdel("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID)
            v = Bot("sendMessage",{"chat_id":chatID,"text":r.doneadd2.format(title),"parse_mode":"markdown"})

@app.on_chat_member_updated(filters.group)
def updatemember(client, message):
    if message.new_chat_member and message.new_chat_member.user.id == int(BOT_ID) and message.new_chat_member.status == enums.ChatMemberStatus.ADMINISTRATOR:
        t = threading.Thread(target=updateAuto,args=(client, message,R))
        t.daemon = True
        t.start()
app.run()
