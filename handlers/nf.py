from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks
from utlis.send import send_msg, BYusers,Name,Glang
from utlis.locks import st
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,datetime
import importlib
import random
def rand(r1_list,aw):
  q = aw
  while q == aw:
    q = random.choice(r1_list)
  return q
def eq():
  nm_list = [1,2,3,4,5,6,7,8,9]
  r1_list = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
  sm_list = ["-","+"]
  q = "{} {} {}".format(random.choice(nm_list) ,random.choice(sm_list) ,random.choice(nm_list))
  aw = eval(q)
  r1 = rand(r1_list,aw)
  r2 = rand(r1_list,aw)
  return q,aw,r1,r2

def nf(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  chatID = message.chat.id
  title = message.chat.title
  rank = isrank(redis,userID,chatID)
  text = message.text
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
  rank = isrank(redis,userID,chatID)
  if group is True and message.outgoing != True:

    if message.left_chat_member:
      if message.left_chat_member.id == int(BOT_ID):
        redis.srem("{}Nbot:groups".format(BOT_ID),chatID)
        redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),chatID)
        NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
        redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID,str(NextDay_Date))
    if message.pinned_message and userID != int(BOT_ID):
      if redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID) and GPranks(userID,chatID) != "creator":
        ID = redis.hget("{}Nbot:pinmsgs".format(BOT_ID),chatID)
        Bot("unpinChatMessage",{"chat_id":chatID,"message_id":message.pinned_message.message_id})

    
    if message.new_chat_members:

      if (rank is False or rank is 0) and GPranks(userID,chatID) == "member" and re.search("is_bot=True",str(message.new_chat_members)):
        if redis.sismember("{}Nbot:Lbots".format(BOT_ID),chatID):
          for mb in message.new_chat_members:
            first_name = mb.first_name
            username = mb.username
            isbot = mb.is_bot
            mbID = mb.id
            if isbot:
              Bot("kickChatMember",{"chat_id":chatID,"user_id":mb.id})

      if message.new_chat_members and redis.sismember("{}Nbot:bancheck".format(BOT_ID),chatID):
        if redis.hget("{}Nbot:bancheck:t".format(BOT_ID),chatID):
          for mb in message.new_chat_members:
            userFn = mb.first_name
            username = mb.username
            isbot = mb.is_bot
            userId = mb.id
            if isbot:return False
            Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,
            "can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,"can_invite_users": 0,})
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.no, callback_data=json.dumps(["kickcheck","",userId])),InlineKeyboardButton(r.yes, callback_data=json.dumps(["delcheck","",userId]))]])
            T ="<a href=\"tg://user?id={}\">{}</a>".format(userId,Name(userFn))
            random.shuffle(kb.inline_keyboard[0])
            Bot("sendMessage",{"chat_id":chatID,"text":r.checkmem.format(T),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
        else:
          for mb in message.new_chat_members:
            userFn = mb.first_name
            username = mb.username
            isbot = mb.is_bot
            userId = mb.id
            if isbot:return False
            q,aw,r1,r2 = eq()
            Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,
            "can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,"can_invite_users": 0,})
            kb = InlineKeyboardMarkup([[InlineKeyboardButton(aw, callback_data=json.dumps(["certain","",userId])),InlineKeyboardButton(r1, callback_data=json.dumps(["kickcheck","",userId])),InlineKeyboardButton(r2, callback_data=json.dumps(["kickcheck","",userId]))]])
            random.shuffle(kb.inline_keyboard[0])
            T ="<a href=\"tg://user?id={}\">{}</a>".format(userId,Name(userFn))
            Bot("sendMessage",{"chat_id":chatID,"text":r.checkmem2.format(T,q),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
  

      if redis.sismember("{}Nbot:Ljoin".format(BOT_ID),chatID):#17
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
        
      if message.new_chat_members and not redis.sismember("{}Nbot:welcomeSend".format(BOT_ID),chatID):
        wl = (redis.hget("{}Nbot:welcome".format(BOT_ID),chatID) or "")
        userId = message.new_chat_members[0].id
        userFn = message.new_chat_members[0].first_name
        T ="<a href=\"tg://user?id={}\">{}</a>".format(userId,Name(userFn))
        Bot("sendMessage",{"chat_id":chatID,"text":wl.format(us=T),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        
      if message.new_chat_members:
        userId = message.new_chat_members[0].id
        if userID != userId:
          redis.hincrby("{}Nbot:{}:addcontact".format(BOT_ID,chatID),userID)

      if message.new_chat_members:
        chatID = message.chat.id
        userId = message.new_chat_members[0].id
        if redis.sismember("{}Nbot:restricteds".format(BOT_ID),userId):
          Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,
            "can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,"can_invite_users": 0,})
        if redis.sismember("{}Nbot:bans".format(BOT_ID),userId):
          Bot("kickChatMember",{"chat_id":chatID,"user_id":userId})
