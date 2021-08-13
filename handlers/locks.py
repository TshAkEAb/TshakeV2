from utlis.rank import setrank,isrank,remrank,remsudos,setsudo
from utlis.send import send_msg, Name,Glang
from utlis.tg import Bot
import importlib

import threading, requests, time, random, re,json
from config import *


def locks(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  userFN = Name(message.from_user.first_name)
  chatID = message.chat.id
  rank = isrank(redis,userID,chatID)
  text = message.text
  title = message.chat.title
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  T = text.split(" ")[1]
  if text == c.Lurl :
    get = redis.sismember("{}Nbot:Llink".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Llink",T,redis)
    else:
      save = redis.sadd("{}Nbot:Llink".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Llink",T,redis)

  if text == c.Uurl :
    get = redis.sismember("{}Nbot:Llink".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Llink".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Llink",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Llink",T,redis)

  if text == c.Lphoto :
    get = redis.sismember("{}Nbot:Lphoto".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lphoto",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lphoto".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lphoto",T,redis)

  if text == c.Uphoto :
    get = redis.sismember("{}Nbot:Lphoto".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lphoto".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lphoto",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lphoto",T,redis)

  if text == c.Lusername :
    get = redis.sismember("{}Nbot:Lusername".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lusername",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lusername".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lusername",T,redis)

  if text == c.Uusername :
    get = redis.sismember("{}Nbot:Lusername".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lusername".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lusername",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lusername",T,redis)

  if text == c.Ltag :
    get = redis.sismember("{}Nbot:Ltag".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Ltag",T,redis)
    else:
      save = redis.sadd("{}Nbot:Ltag".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Ltag",T,redis)

  if text == c.Utag :
    get = redis.sismember("{}Nbot:Ltag".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Ltag".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Ltag",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Ltag",T,redis)

  if text == c.Lvideo :
    get = redis.sismember("{}Nbot:Lvideo".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lvideo",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lvideo".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lvideo",T,redis)

  if text == c.Uvideo :
    get = redis.sismember("{}Nbot:Lvideo".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lvideo".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lvideo",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lvideo",T,redis)

  if text == c.Lgifs :
    get = redis.sismember("{}Nbot:Lgifs".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lgifs",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lgifs".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lgifs",T,redis)

  if text == c.Ugifs :
    get = redis.sismember("{}Nbot:Lgifs".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lgifs".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lgifs",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lgifs",T,redis)

  if text == c.Lsticker :
    get = redis.sismember("{}Nbot:Lsticker".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lsticker",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lsticker".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lsticker",T,redis)

  if text == c.Usticker :
    get = redis.sismember("{}Nbot:Lsticker".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lsticker".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lsticker",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lsticker",T,redis)

  if text == c.Lfiles :
    get = redis.sismember("{}Nbot:Lfiles".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lfiles",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lfiles".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lfiles",T,redis)

  if text == c.Ufiles :
    get = redis.sismember("{}Nbot:Lfiles".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lfiles".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lfiles",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lfiles",T,redis)

  if text == c.Lmusic :
    get = redis.sismember("{}Nbot:Lmusic".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lmusic",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lmusic".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lmusic",T,redis)

  if text == c.Umusic :
    get = redis.sismember("{}Nbot:Lmusic".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lmusic".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lmusic",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lmusic",T,redis)

  if text == c.Lfwd :
    get = redis.sismember("{}Nbot:Lfwd".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lfwd",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lfwd".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lfwd",T,redis)

  if text == c.Ufwd :
    get = redis.sismember("{}Nbot:Lfwd".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lfwd".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lfwd",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lfwd",T,redis)

  if text == c.Lvoice :
    get = redis.sismember("{}Nbot:Lvoice".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lvoice",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lvoice".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lvoice",T,redis)

  if text == c.Uvoice :
    get = redis.sismember("{}Nbot:Lvoice".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lvoice".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lvoice",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lvoice",T,redis)

  if text == c.Lcontact :
    get = redis.sismember("{}Nbot:Lcontact".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lcontact",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lcontact".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lcontact",T,redis)

  if text == c.Ucontact :
    get = redis.sismember("{}Nbot:Lcontact".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lcontact".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lcontact",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lcontact",T,redis)

  if text == c.Lmarkdown :
    get = redis.sismember("{}Nbot:Lmarkdown".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lmarkdown",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lmarkdown".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lmarkdown",T,redis)

  if text == c.Umarkdown :
    get = redis.sismember("{}Nbot:Lmarkdown".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lmarkdown".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lmarkdown",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lmarkdown",T,redis)

  if text == c.Lbots :
    get = redis.sismember("{}Nbot:Lbots".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lbots",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lbots".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lbots",T,redis)

  if text == c.Ubots :
    get = redis.sismember("{}Nbot:Lbots".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lbots".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lbots",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lbots",T,redis)

  if text == c.Ledits :
    get = redis.sismember("{}Nbot:Ledits".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Ledits",T,redis)
    else:
      save = redis.sadd("{}Nbot:Ledits".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Ledits",T,redis)

  if text == c.Uedits :
    get = redis.sismember("{}Nbot:Ledits".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Ledits".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Ledits",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Ledits",T,redis)

  if text == c.Larabic :
    get = redis.sismember("{}Nbot:Larabic".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Larabic",T,redis)
    else:
      save = redis.sadd("{}Nbot:Larabic".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Larabic",T,redis)

  if text == c.Uarabic :
    get = redis.sismember("{}Nbot:Larabic".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Larabic".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Larabic",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Larabic",T,redis)

  if text == c.Lenglish :
    get = redis.sismember("{}Nbot:Lenglish".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lenglish",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lenglish".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lenglish",T,redis)

  if text == c.Uenglish :
    get = redis.sismember("{}Nbot:Lenglish".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lenglish".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lenglish",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lenglish",T,redis)



  if text == c.Linline :
    get = redis.sismember("{}Nbot:Linline".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Linline",T,redis)
    else:
      save = redis.sadd("{}Nbot:Linline".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Linline",T,redis)

  if text == c.Uinline :
    get = redis.sismember("{}Nbot:Linline".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Linline".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Linline",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Linline",T,redis)

  if text == c.Lchat :
    Bot("setChatPermissions",{"chat_id":chatID})
    send_msg("LUN",client, message,r.lock,"Lchat",T,redis)


  if text == c.Uchat :
    Bot("setchatpermissions",{"chat_id":chatID,"permissions":json.dumps({"can_send_messages":True,"can_send_media_messages":True,"can_send_polls":True,"can_send_other_messages":True,"can_invite_users":True,"can_add_web_page_previews":True})})
    send_msg("LUN",client, message,r.unlock,"Lchat",T,redis)


  if text == c.Ljoin :
    get = redis.sismember("{}Nbot:Ljoin".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Ljoin",T,redis)
    else:
      save = redis.sadd("{}Nbot:Ljoin".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Ljoin",T,redis)

  if text == c.Ujoin :
    get = redis.sismember("{}Nbot:Ljoin".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Ljoin".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Ljoin",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Ljoin",T,redis)



  if text == c.Llongtext :
    get = redis.sismember("{}Nbot:Llongtext".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Llongtext",T,redis)
    else:
      save = redis.sadd("{}Nbot:Llongtext".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Llongtext",T,redis)

  if text == c.Ulongtext :
    get = redis.sismember("{}Nbot:Llongtext".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Llongtext".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Llongtext",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Llongtext",T,redis)

  if text == c.Lall :
    get = redis.sismember("{}Nbot:Lall".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lall",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lall".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lall",T,redis)

  if text == c.Uall :
    get = redis.sismember("{}Nbot:Lall".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lall".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lall",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lall",T,redis)

  if text == c.Lnote :
    get = redis.sismember("{}Nbot:Lnote".format(BOT_ID),chatID)
    if get :
      send_msg("LUN",client, message,r.locked,"Lnote",T,redis)
    else:
      save = redis.sadd("{}Nbot:Lnote".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.lock,"Lnote",T,redis)

  if text == c.Unote :
    get = redis.sismember("{}Nbot:Lnote".format(BOT_ID),chatID)
    if get :
      save = redis.srem("{}Nbot:Lnote".format(BOT_ID),chatID)
      send_msg("LU",client, message,r.unlock,"Lnote",T,redis)
    else:
      send_msg("LUN",client, message,r.unlocked,"Lnote",T,redis)
  if rank != "admin" and rank != "owner":
      if text == c.Lpin :
        R = text.split(" ")[1]
        BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
        get = redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID)
        if get :
          save = redis.srem("{}Nbot:Lpin".format(BOT_ID),chatID)
          Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

      if text == c.Upin :
        R = text.split(" ")[1]
        BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
        get = redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID)
        if get :
          Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
        else:
          save = redis.sadd("{}Nbot:Lpin".format(BOT_ID),chatID)
          Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
        
  if rank != "admin":
    if text == c.LwelcomeSend :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:welcomeSend".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:welcomeSend".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.UwelcomeSend :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:welcomeSend".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:welcomeSend".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

  if rank != "admin":

    if text == "قفل الدخول" :
      get = redis.sismember("{}Nbot:Lgpjoin".format(BOT_ID),chatID)
      if get :
        send_msg("LUN",client, message,r.locked,"Lgpjoin",T,redis)
      else:
        save = redis.sadd("{}Nbot:Lgpjoin".format(BOT_ID),chatID)
        send_msg("LU",client, message,r.lock,"Lgpjoin",T,redis)

    if text == "فتح الدخول" :
      get = redis.sismember("{}Nbot:Lgpjoin".format(BOT_ID),chatID)
      if get :
        save = redis.srem("{}Nbot:Lgpjoin".format(BOT_ID),chatID)
        send_msg("LU",client, message,r.unlock,"Lgpjoin",T,redis)
      else:
        send_msg("LUN",client, message,r.unlocked,"Lgpjoin",T,redis)

      
    if text == c.Lbancheck :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:bancheck".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:bancheck".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Ubancheck :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:bancheck".format(BOT_ID),chatID)
      if get :
        save = redis.srem("{}Nbot:bancheck".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Lreply :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:ReplySend".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:ReplySend".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Ureply :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:ReplySend".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:ReplySend".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.LreplyBOT :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:ReplySendBOT".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:ReplySendBOT".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.UreplyBOT :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:ReplySendBOT".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:ReplySendBOT".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Lkickme :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:kickme".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:kickme".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Ukickme :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:kickme".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:kickme".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Lshowlink :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:showlink".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:showlink".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Ushowlink :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:showlink".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:showlink".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})


    if re.search(c.Lkickban, text) and  (rank is "sudo" or rank is "asudo" or rank is "sudos" or rank is "malk" or rank is "acreator") :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:kickban".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:kickban".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if re.search(c.Ukickban, text) and  (rank is "sudo" or rank is "asudo" or rank is "sudos" or rank is "malk" or rank is "acreator"):
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:kickban".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:kickban".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})




    if text == c.LID :
      R = text.split(" ")[1]
      get = redis.sismember("{}Nbot:IDSend".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:IDSend".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.UID : 
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:IDSend".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:IDSend".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if re.search(c.LIDPH,text):
      R = text.replace(c.stAd,"")
      get = redis.sismember("{}Nbot:IDSendPH".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:IDSendPH".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if re.search(c.UIDPH,text): 
      R = text.replace(c.stUd,"")
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:IDSendPH".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:IDSendPH".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Lflood :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:Lflood".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:Lflood".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.Uflood :
      R = text.split(" ")[1]
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:Lflood".format(BOT_ID),chatID)
      if get :
        save = redis.srem("{}Nbot:Lflood".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})



    if re.search(c.LIDpt,text):
      R = text.replace(c.stAd,"")
      get = redis.sismember("{}Nbot:IDpt".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:IDpt".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if re.search(c.UIDpt,text): 
      R = text.replace(c.stUd,"")
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:IDpt".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:IDpt".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if re.search("^تعطيل الاوامر العامه$",text):
      R = text.replace(c.stUd,"")
      get = redis.sismember("{}Nbot:publicOrders".format(BOT_ID),chatID)
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      if get :
        save = redis.srem("{}Nbot:publicOrders".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.unADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
         Bot("sendMessage",{"chat_id":chatID,"text":r.unADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if re.search("^تفعيل الاوامر العامه$",text):
      R = text.replace(c.stAd,"")
      BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
      get = redis.sismember("{}Nbot:publicOrders".format(BOT_ID),chatID)
      if get :
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADD.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      else:
        save = redis.sadd("{}Nbot:publicOrders".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.ADDed.format(BY,R),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

