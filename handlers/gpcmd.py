from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,Grank,IDrank,isrankDef,remasudo
from utlis.tg import Bot , Ckuser
from utlis.send import send_msg, BYusers, Name,Glang,sendM,getAge
from utlis.locks import st,Clang,st_res
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from os import listdir
from os.path import isfile, join


def gpcmd(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  chatID = message.chat.id
  title = message.chat.title
  rank = isrank(redis,userID,chatID)
  text = message.text
  username = message.from_user.username
  if username is None:
    username = "None"
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  #steps
  if redis.hexists("{}Nbot:step:or".format(BOT_ID),userID):
    tx = redis.hget("{}Nbot:step:or".format(BOT_ID),userID)
    if text :
      redis.sadd("{}Nbot:{}:TXoeders".format(BOT_ID,chatID),f"{tx}={text}")
      redis.hdel("{}Nbot:step:or".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":f"✅꒐ تم اضافه الامر {tx} الى {text}","reply_to_message_id":message.message_id,"parse_mode":"html"})
    

  if redis.hexists("{}Nbot:step".format(BOT_ID),userID):
    tx = redis.hget("{}Nbot:step".format(BOT_ID),userID)
    if text :
      redis.hset("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),tx,text)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRtext.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
    
    if message.sticker:
      ID = message.sticker.file_id
      redis.hset("{}Nbot:{}:STreplys".format(BOT_ID,chatID),tx,ID)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRst.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

    if message.animation:
      ID = message.animation.file_id
      redis.hset("{}Nbot:{}:GFreplys".format(BOT_ID,chatID),tx,ID)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRgf.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

    if message.voice:
      ID = message.voice.file_id
      redis.hset("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),tx,ID)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRvo.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

    if message.audio:
      ID = message.audio.file_id
      redis.hset("{}Nbot:{}:AUreplys".format(BOT_ID,chatID),tx,ID)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRvo.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
    
      
    if message.photo:
      ID = message.photo.file_id
      redis.hset("{}Nbot:{}:PHreplys".format(BOT_ID,chatID),tx,ID)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRph.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
    if message.document:
      ID = message.document.file_id
      redis.hset("{}Nbot:{}:DOreplys".format(BOT_ID,chatID),tx,ID)
      redis.hdel("{}Nbot:step".format(BOT_ID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.SRfi.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})



###############
  if text:
    if text == c.delrpmsg and message.reply_to_message:
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message.reply_to_message.message_id})

    if text == c.settingsCmd and Ckuser(message):
      kb = st(client, message,redis)
      Bot("sendMessage",{"chat_id":chatID,"text":r.settings.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})


    if re.search(c.settingsCmdRes, text) and Ckuser(message):
      kb = st_res(client, message,redis)
      Bot("sendMessage",{"chat_id":chatID,"text":r.settingsRes.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
    if re.search(c.del_bans,text):
      arrays = redis.smembers("{}Nbot:{}:bans".format(BOT_ID,chatID))
      for user in arrays:
        GetGprank = GPranks(user,chatID)
        if GetGprank == "kicked":
          Bot("unbanChatMember",{"chat_id":chatID,"user_id":user})
        redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),user)
      Bot("sendMessage",{"chat_id":chatID,"text":r.DoneDelList,"disable_web_page_preview":True})

    if re.search(c.del_mutes,text):
      redis.delete(f"{BOT_ID}Nbot:{chatID}:muteusers")
      Bot("sendMessage",{"chat_id":chatID,"text":r.DoneDelList,"disable_web_page_preview":True})
    if re.search(c.mutes, text):
      arrays = redis.smembers("{}Nbot:{}:muteusers".format(BOT_ID,chatID))
      b = BYusers(arrays,chatID,redis,client)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","muteusers",userID]))]])
      if  b is not "":
        Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
      else:
        Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

      
      
    if re.search(c.del_restricteds,text):
      arrays = redis.smembers("{}Nbot:{}:restricteds".format(BOT_ID,chatID))
      for user in arrays:
        GetGprank = GPranks(user,chatID)
        if GetGprank == "restricted":
          Bot("restrictChatMember",{"chat_id": chatID,"user_id": user,"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,"can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,})
        redis.srem("{}Nbot:{}:restricteds".format(BOT_ID,chatID),user)
      Bot("sendMessage",{"chat_id":chatID,"text":r.DoneDelList,"disable_web_page_preview":True})
      
    if re.search(c.bans, text) :
      arrays = redis.smembers("{}Nbot:{}:bans".format(BOT_ID,chatID))
      b = BYusers(arrays,chatID,redis,client)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delListbans","",userID]))]])
      if  b is not "":
        Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
      else:
        Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

    if re.search(c.restricteds, text):
      arrays = redis.smembers("{}Nbot:{}:restricteds".format(BOT_ID,chatID))
      b = BYusers(arrays,chatID,redis,client)
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delListrestricteds","",userID]))]])
      if  b is not "":
        Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
      else:
        Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

    orban = redis.hget("{}Nbot:banor:cb".format(BOT_ID),chatID) or c.ban
    orban2 = redis.hget("{}Nbot:banor:cb2".format(BOT_ID),chatID) or c.ban2
    if re.search(c.ban+"|"+orban, text) :
      if (rank == "creater" or rank == "owner" or rank == "admin" ) and redis.sismember("{}Nbot:kickban".format(BOT_ID),chatID):
        Bot("sendMessage",{"chat_id":chatID,"text":"عذراً الحظر معطل ⚠️","reply_to_message_id":message.message_id,"parse_mode":"html"})
        return 0
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search(c.ban2+"|"+orban2,text):
        user = int(re.search(r'\d+', text).group())
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        GetGprank = GPranks(userId,chatID)
        if Getrank == "bot":return False
        if GetGprank == "NoMember":
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoMember,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        if (GetGprank == "left" or GetGprank == "kicked"):
          Bot("sendMessage",{"chat_id":chatID,"text":r.haveKick,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif (GetGprank == "member" or GetGprank == "restricted") and (Getrank is False or Getrank is 0):
          if redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),userId):
            send_msg("BNN",client, message,r.Dban,"bans",getUser,redis)
          else:
            Bot("kickChatMember",{"chat_id":chatID,"user_id":userId})
            redis.sadd("{}Nbot:{}:bans".format(BOT_ID,chatID),userId)
            send_msg("BN",client, message,r.ban,"bans",getUser,redis)
        elif (GetGprank == "creator" or GetGprank == "administrator") or (Getrank != False or Getrank != 0):
          Bot("sendMessage",{"chat_id":chatID,"text":r.haveRank.format(Grank((Getrank or GetGprank),r)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

    if re.search(c.unban, text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search(c.unban2,text):
        user = text.split(" ")[1]
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        GetGprank = GPranks(userId,chatID)
        if Getrank == "bot":return False
        if GetGprank == "NoMember":
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoMember,"reply_to_message_id":message.message_id,"parse_mode":"html"})
          return False
        if GetGprank == "kicked":
          Bot("unbanChatMember",{"chat_id":chatID,"user_id":userId})
          redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),userId)
          send_msg("BN",client, message,r.unban,"bans",getUser,redis)
        else:
          send_msg("BNN",client, message,r.Dunban,"bans",getUser,redis)
      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
   
    ortk = redis.hget("{}Nbot:tkor:cb".format(BOT_ID),chatID) or c.TK
    ortk2 = redis.hget("{}Nbot:tkor:cb2".format(BOT_ID),chatID) or c.TK2
    if re.search(c.TK+"|"+ortk, text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search(c.TK2+"|"+ortk2,text):
        user = int(re.search(r'\d+', text).group())
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        GetGprank = GPranks(userId,chatID)
        if Getrank == "bot":return False
        if GetGprank == "NoMember":
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoMember,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        if (GetGprank == "left" or GetGprank == "kicked"):
          Bot("sendMessage",{"chat_id":chatID,"text":r.haveKick,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif (GetGprank == "restricted"):
          send_msg("BNN",client, message,r.haveRc,"restricteds",getUser,redis)
          #Bot("sendMessage",{"chat_id":chatID,"text":r.haveRc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif GetGprank == "member" and (Getrank is False or Getrank is 0):
          if redis.sismember("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId):
            send_msg("BNN",client, message,r.Drestricted,"restricteds",getUser,redis)
          else:
            Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,
            "can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,"can_invite_users": 0,})
            redis.sadd("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId)
            send_msg("BN",client, message,r.restricted,"restricteds",getUser,redis)
        elif (GetGprank == "creator" or GetGprank == "administrator") or (Getrank != False or Getrank != 0):
          Bot("sendMessage",{"chat_id":chatID,"text":r.haveRank.format(Grank((Getrank or GetGprank),r)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
    


    if re.search("^كشف القيود$|^كشف القيود @(.*)$|^كشف القيود [0-9]+$", text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search("^كشف القيود [0-9]+$",text):
        user = int(re.search(r'\d+', text).group())
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
        if Getrank == "bot":return False
        tx = f"🚹꒐ العضو : {BY}\n"
        if redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),userId):
          tx += "الحظر 🚫: محظور\n"
        else:
          tx += "الحظر 🚫: غير محظور\n"
        if redis.sismember("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId):
          tx += "الكتم 📮: مكتوم\n"
        else:
          tx += "الكتم 📮: غير مكتوم\n"
        Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html"})

      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

    if re.search("^الغاء القيود$|^الغاء القيود @(.*)$|^الغاء القيود [0-9]+$", text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search("^الغاء القيود [0-9]+$",text):
        user = int(re.search(r'\d+', text).group())
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        GetGprank = GPranks(userId,chatID)
        BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
        if Getrank == "bot":return False
        print(GetGprank)
        if GetGprank == "member" and not redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),userId) and not redis.sismember("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId):
          Bot("sendMessage",{"chat_id":chatID,"text":f"🚹꒐ العضو : {BY}\n⚪️꒐ لا توجد عليه قيود","reply_to_message_id":message.message_id,"parse_mode":"html"})
        
        if GetGprank == "NoMember":
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoMember,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        if redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),userId) or redis.sismember("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId) or GetGprank == "restricted" or GetGprank == "kicked":
          if GetGprank == "kicked":
            Bot("unbanChatMember",{"chat_id":chatID,"user_id":userId})
          redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),userId)
          Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,
          "can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,"can_invite_users": 1,})
          redis.srem("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId)
          Bot("sendMessage",{"chat_id":chatID,"text":f"🚹꒐ العضو : {BY}\n⚪️꒐ تم الغاء القيود","reply_to_message_id":message.message_id,"parse_mode":"html"})

      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        
        
        


    if re.search(c.unmute, text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search(c.unmute2,text):
        user = text.split(" ")[1]
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        if Getrank == "bot":return False
        if (Getrank is False or Getrank is 0):
          BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
          if not redis.sismember(f"{BOT_ID}Nbot:{chatID}:muteusers",userId):
            Bot("sendMessage",{"chat_id":chatID,"text":f"🚹꒐ العضو : {BY}\n🚷꒐ غير مكتوم من المجموعة","reply_to_message_id":message.message_id,"parse_mode":"html"})
          else:
            redis.srem(f"{BOT_ID}Nbot:{chatID}:muteusers",userId)
            Bot("sendMessage",{"chat_id":chatID,"text":f"🚹꒐ العضو : {BY}\n🚷꒐ تم الغاء كتمه من المجموعة","reply_to_message_id":message.message_id,"parse_mode":"html"})
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.haveRank.format(Grank((Getrank or GetGprank),r)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})


    if re.search(c.mute, text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search(c.mute2,text):
        user = int(re.search(r'\d+', text).group())
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        Getrank = isrank(redis,userId,chatID)
        if Getrank == "bot":return False
        if (Getrank is False or Getrank is 0):
          BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
          if redis.sismember(f"{BOT_ID}Nbot:{chatID}:muteusers",userId):
            Bot("sendMessage",{"chat_id":chatID,"text":f"🚹꒐ العضو : {BY}\n🚷꒐ بالفعل مكتوم من المجموعة","reply_to_message_id":message.message_id,"parse_mode":"html"})
          else:
            redis.sadd(f"{BOT_ID}Nbot:{chatID}:muteusers",userId)
            Bot("sendMessage",{"chat_id":chatID,"text":f"🚹꒐ العضو : {BY}\n🚷꒐ تم كتمه من المجموعة","reply_to_message_id":message.message_id,"parse_mode":"html"})
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.haveRank.format(Grank((Getrank or GetGprank),r)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})


        
        
        
    if re.search(c.unTK, text):
      if re.search("@",text):
        user = text.split("@")[1]
      if re.search(c.unTK2,text):
        user = text.split(" ")[1]
      if message.reply_to_message:
        user = message.reply_to_message.from_user.id
      if 'user' not in locals():return False
      try:
        getUser = client.get_users(user)
        userId = getUser.id
        userFn = getUser.first_name
        Getrank = isrank(redis,userId,chatID)
        GetGprank = GPranks(userId,chatID)
        if Getrank == "bot":return False
        if GetGprank == "NoMember":
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoMember,"reply_to_message_id":message.message_id,"parse_mode":"html"})
          return False
        if GetGprank == "restricted":
          Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,
          "can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,"can_invite_users": 1,})
          redis.srem("{}Nbot:{}:restricteds".format(BOT_ID,chatID),userId)
          send_msg("BN",client, message,r.unrestricted,"restricteds",getUser,redis)
        else:
          send_msg("BNN",client, message,r.Dunrestricted,"restricteds",getUser,redis)
      except Exception as e:
        Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
    
    if rank != "admin":

      if re.search(c.setname, text):
        name = text.replace(c.Dsetname,"")
        Bot("setChatTitle",{"chat_id":chatID,"title":name})
        Bot("sendMessage",{"chat_id":chatID,"text":r.Dsetname.format(name),"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search(c.setabout, text):
        about = text.replace(c.Dsetabout,"")
        Bot("setChatDescription",{"chat_id":chatID,"description":about})
        Bot("sendMessage",{"chat_id":chatID,"text":r.Dsetabout.format(about),"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search(c.setphoto, text) and message.reply_to_message and message.reply_to_message.photo:
        ID = message.reply_to_message.photo.file_id
        client.set_chat_photo(chat_id=chatID,photo=ID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.Dsetphoto,"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search("^حذف الصورة$|^حذف الصوره$", text):
        client.delete_chat_photo(chat_id=chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":"☑️꒐ تم حذف صورة المجموعة","reply_to_message_id":message.message_id,"parse_mode":"html"})
      
      if re.search("^الاوامر المضافه$",text):
        tx = "الاوامر المضافه ℹ️:\n"
        x = redis.smembers("{}Nbot:{}:TXoeders".format(BOT_ID,chatID))
        if not x :
          message.reply_text(r.listempty2)
          return 0
        i = 1
        for x in x:
          x = x.split("=")
          tx = tx+f"{i} - {x[0]} > {x[1]}\n"
          i +=1
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","TXoeders",userID]))]])
        message.reply_text(tx,reply_markup=kb)
        
      if re.search("^حذف امر (.*)$",text):
        cc = re.findall("^حذف امر (.*)$",text)[0]
        x = redis.smembers("{}Nbot:{}:TXoeders".format(BOT_ID,chatID))
        for x1 in x:
          x = x1.split("=")
          if x[0] == cc:
            redis.srem("{}Nbot:{}:TXoeders".format(BOT_ID,chatID),x1)
            message.reply_text(f"✅꒐ تم حذف الامر {cc}")
            return 0
        message.reply_text(f"⚠️꒐ لا يوجد {cc} امر")
      if re.search("^اضف امر (?!عام)\w*$",text):
        cc = re.findall(c.addor,text)
        redis.hset("{}Nbot:step:or".format(BOT_ID),userID,cc[0])
        message.reply_text(f"⏺꒐ الان ارسل الامر ليتم تغيره الى {cc[0]}")

      if re.search(c.remallR, text):
        if re.search("@",text):
          user = text.split("@")[1]
        if re.search(c.remallR2,text):
          user = text.split(" ")[1]
        if message.reply_to_message:
          user = message.reply_to_message.from_user.id
        if 'user' not in locals():return False
        try:
          getUser = client.get_users(user)
          userId = getUser.id
          userFn = getUser.first_name
          Rank = isrank(redis,userId,chatID)
          tx = ""
          if (Rank is False or Rank is 0):
            BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
            Bot("sendMessage",{"chat_id":chatID,"text":r.remallN.format(BY),"reply_to_message_id":message.message_id,"parse_mode":"html"})
            return 0
          to_del_ranks = {
            "sudo":{"asudo","sudos","malk","acreator","creator","owner","admin","vip"},
            "asudo":{"asudo","sudos","malk","acreator","creator","owner","admin","vip"},
            "sudos":{"malk","acreator","creator","owner","admin","vip"},
            "malk":{"acreator","creator","owner","admin","vip"},
            "acreator":{"creator","owner","admin","vip"},
            "creator":{"owner","admin","vip"},
            "owner":{"admin","vip"},
            "admin":{"vip"},
          }
          i = 0
          for x in to_del_ranks[rank]:
            if isrankDef(redis,userId,chatID,x) is str(x):
              t = Grank(x,r)
              tx = tx+t+","
              if x is "asudo":
                 remasudo(redis,userId)
              if x is "sudos":
                 remsudos(redis,userId)
              elif x is "malk":
                remrank(redis,x,userId,chatID,"one")
              else:
                remrank(redis,x,userId,chatID,"array")
          BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
          Bot("sendMessage",{"chat_id":chatID,"text":r.remall.format(BY,tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        except Exception as e:
          Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      if re.search(c.floodset, text):
        if redis.hexists("{}Nbot:floodset".format(BOT_ID),chatID):
          get = redis.hget("{}Nbot:floodset".format(BOT_ID),chatID)
        else:
          get = "res"
        if get == "ban":
          tx = r.Tban
        if get == "res":
          tx =  r.Tres
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.fset.format(tx),callback_data=json.dumps(["floodset",get,userID]))]])
        Bot("sendMessage",{"chat_id":chatID,"text":r.Tfset,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})

      if re.search(c.twostepset, text):
        if redis.hexists("{}Nbot:bancheck:t".format(BOT_ID),chatID):
          get = redis.hget("{}Nbot:bancheck:t".format(BOT_ID),chatID)
        else:
          get = "eq"
        if get == "eq":
          tx = r.Teq
        if get == "two":
          tx =  r.Ttwo
        kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.tset.format(tx),callback_data=json.dumps(["twostepset",get,userID]))]])
        Bot("sendMessage",{"chat_id":chatID,"text":r.Ttset,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})

      if re.search(c.delIDC, text):
        redis.hdel("{}Nbot:SHOWid".format(BOT_ID),chatID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.Ddelid,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      if re.search("^تعين ايدي$|^وضع ايدي$",text):
        message.reply_text("""⚠️꒐ يمكنك تغير الايدي بأرسال
⏺꒐ `تعين الايدي النص`

🔽꒐ ويمكنك ايضاً اضافه
{id} - لعرض الايدي
{username} - لعرض المعرف
{stast} - لعرض الرتبه
{msgs} - لعرض عدد الرسائل
{edits} - لعرض عدد السحكات
{rate} - لعرض نسبه التفاعل
⎯ ⎯ ⎯ ⎯""")
      if re.search("^اضف رد$",text):
        message.reply_text(  
"""⚠️꒐ يمكنك اضف رد  بأرسال
⏺꒐ `اضف رد النص`

🔽꒐ ويمكنك ايضاً اضافه html

<b>bold</b>
*bold*

<i>italic</i>
__italic__

<a href=\"https://t.me/mdddd/\">Mohammed</a>
[Mohammed](https://t.me/mdddd/)

<code>inline fixed-width code</code>
`inline fixed-width code`
⎯ ⎯ ⎯ ⎯""",parse_mode="markdown",disable_web_page_preview=True)
      if re.search(c.setIDC, text):
          # print("ssssssssss")
          # tx = text.replace(c.RsetIDC,"")
          tx = re.findall(c.setIDC,text)[0][1]
          rep = {"#age":"{age}","#name":"{name}","#id":"{id}","#username":"{username}","#msgs":"{msgs}","#stast":"{stast}","#edits":"{edits}","#rate":"{rate}","{us}":"{username}","#us":"{username}"}
          for v in rep.keys():
            tx = tx.replace(v,rep[v])
            
          t = IDrank(redis,userID,chatID,r)
          msgs = (redis.hget("{}Nbot:{}:msgs".format(BOT_ID,chatID),userID) or 0)
          edits = (redis.hget("{}Nbot:{}:edits".format(BOT_ID,chatID),userID) or 0)
          rate = int(msgs)*100/20000
          age = getAge(userID,r)
          v = Bot("sendMessage",{"chat_id":chatID,"text":tx.format(username=("@"+username or "None"),id=userID,stast=t,msgs=msgs,edits=edits,age=age,rate=str(rate)+"%"),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          if v["ok"]:
            redis.hset("{}Nbot:SHOWid".format(BOT_ID),chatID,tx)
            Bot("sendMessage",{"chat_id":chatID,"text":r.DsetIDShow,"reply_to_message_id":message.message_id,"parse_mode":"html"})
          elif v["ok"] == False:
            Bot("sendMessage",{"chat_id":chatID,"text":r.DsetSudosShowE,"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search(c.block, text):
        if re.search(c.block2, text):
          tx = text.replace(c.RPbk,"")
          if redis.sismember("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID),tx):
            Bot("sendMessage",{"chat_id":chatID,"text":r.Adoneblock.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          else:
            redis.sadd("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID),tx)
            Bot("sendMessage",{"chat_id":chatID,"text":r.Doneblock.format(tx,title),"reply_to_message_id":message.message_id,"parse_mode":"html"})

        if message.reply_to_message:
          if message.reply_to_message.sticker:
            ID = message.reply_to_message.sticker.file_id
            if redis.sismember("{}Nbot:{}:blockSTICKERs".format(BOT_ID,chatID),ID):
              Bot("sendMessage",{"chat_id":chatID,"text":r.StA.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
            else:
              redis.sadd("{}Nbot:{}:blockSTICKERs".format(BOT_ID,chatID),ID)
              Bot("sendMessage",{"chat_id":chatID,"text":r.StB.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
          
          if message.reply_to_message.photo:
            ID = message.reply_to_message.photo.file_id
            if redis.sismember("{}Nbot:{}:blockphotos".format(BOT_ID,chatID),ID):
              Bot("sendMessage",{"chat_id":chatID,"text":r.PhA.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
            else:
              redis.sadd("{}Nbot:{}:blockphotos".format(BOT_ID,chatID),ID)
              Bot("sendMessage",{"chat_id":chatID,"text":r.PhB.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
          
          if message.reply_to_message.animation:
            ID = message.reply_to_message.animation.file_id
            if redis.sismember("{}Nbot:{}:blockanimations".format(BOT_ID,chatID),ID):
              Bot("sendMessage",{"chat_id":chatID,"text":r.GfA.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
            else:
              redis.sadd("{}Nbot:{}:blockanimations".format(BOT_ID,chatID),ID)
              Bot("sendMessage",{"chat_id":chatID,"text":r.GfB.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

      if re.search(c.unblock, text):
        if re.search(c.unblock2, text):
          tx = text.replace(c.RPubk,"")
          if redis.sismember("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID),tx):
            redis.srem("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID),tx)
            Bot("sendMessage",{"chat_id":chatID,"text":r.unDoneblock.format(tx,title),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          else:
            Bot("sendMessage",{"chat_id":chatID,"text":r.unAdoneblock.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})

        if message.reply_to_message:
          if message.reply_to_message.sticker:
            ID = message.reply_to_message.sticker.file_id
            if redis.sismember("{}Nbot:{}:blockSTICKERs".format(BOT_ID,chatID),ID):
              redis.srem("{}Nbot:{}:blockSTICKERs".format(BOT_ID,chatID),ID)
              Bot("sendMessage",{"chat_id":chatID,"text":r.unStB.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
            else:
              Bot("sendMessage",{"chat_id":chatID,"text":r.unStA.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

          if message.reply_to_message.photo:
            ID = message.reply_to_message.photo.file_id
            if redis.sismember("{}Nbot:{}:blockphotos".format(BOT_ID,chatID),ID):
              redis.srem("{}Nbot:{}:blockphotos".format(BOT_ID,chatID),ID)
              Bot("sendMessage",{"chat_id":chatID,"text":r.unPhB.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})       
            else:
              Bot("sendMessage",{"chat_id":chatID,"text":r.unPhA.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
          
          if message.reply_to_message.animation:
            ID = message.reply_to_message.animation.file_id
            if redis.sismember("{}Nbot:{}:blockanimations".format(BOT_ID,chatID),ID):
              redis.srem("{}Nbot:{}:blockanimations".format(BOT_ID,chatID),ID)
              Bot("sendMessage",{"chat_id":chatID,"text":r.unGfB.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})
            else:
              Bot("sendMessage",{"chat_id":chatID,"text":r.unGfA.format(title),"reply_to_message_id":message.reply_to_message.message_id,"parse_mode":"html"})

      if re.search(c.Blocklist, text):
        Botuser = client.get_me().username
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STword,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockTEXTs")),InlineKeyboardButton(c.STgifs,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockanimations")),],[InlineKeyboardButton(c.STphoto,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockphotos")),InlineKeyboardButton(c.STsticker,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockSTICKERs")),]])
        Bot("sendMessage",{"chat_id":chatID,"text":r.blocklist.format(r.blocklist2,title),"reply_to_message_id":message.message_id,"reply_markup":reply_markup})

      if re.search(c.Replylist, text):
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STword,callback_data=json.dumps(["showreplylist","",userID])),InlineKeyboardButton(c.STgifs,callback_data=json.dumps(["showGFreplylist","",userID])),],[InlineKeyboardButton(c.STvoice,callback_data=json.dumps(["showVOreplylist","",userID])),InlineKeyboardButton(c.STsticker,callback_data=json.dumps(["showSTreplylist","",userID])),],[InlineKeyboardButton("Mp3",callback_data=json.dumps(["showAUreplylist","",userID]))]])
        Bot("sendMessage",{"chat_id":chatID,"text":r.blocklist.format(text,title),"reply_to_message_id":message.message_id,"reply_markup":reply_markup})

      if re.search(c.FloodT, text):
        Nu = text.split(" ")[2]
        redis.hset("{}Nbot:time_ck".format(BOT_ID),chatID,Nu)
        Bot("sendMessage",{"chat_id":chatID,"text":r.DoneSet.format(text.split(" ")[0]+" "+text.split(" ")[1],Nu),"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search(c.FloodM, text):
        Nu = text.split(" ")[2]
        redis.hset("{}Nbot:max_msg".format(BOT_ID),chatID,Nu)
        Bot("sendMessage",{"chat_id":chatID,"text":r.DoneSet.format(text.split(" ")[0]+" "+text.split(" ")[1],Nu),"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search(c.STWEL, text):
        Wc = text.replace(c.RPwel,"")
        redis.hset("{}Nbot:welcome".format(BOT_ID),chatID,Wc)
        Bot("sendMessage",{"chat_id":chatID,"text":r.Donewel.format(Wc),"reply_to_message_id":message.message_id,"parse_mode":"html"})


      if re.search(c.STreply, text):
        tx = text.replace(c.RPreply,"")
        if redis.hexists("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),tx):
          Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:STreplys".format(BOT_ID,chatID),tx):
          Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:GFreplys".format(BOT_ID,chatID),tx):
          Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),tx):
          Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:AUreplys".format(BOT_ID,chatID),tx):
          Bot("sendMessage",{"chat_id":chatID,"text":r.Yrp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        else:
          redis.hset("{}Nbot:step".format(BOT_ID),userID,tx)
          kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.MoreInfo, url="t.me/zx_xx")]])
          Bot("sendMessage",{"chat_id":chatID,"text":r.Sendreply % tx,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})

      if re.search(c.DLreply, text):
        tx = text.replace(c.RPdreply,"")
        if redis.hexists("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),tx):
          redis.hdel("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),tx)
          Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:STreplys".format(BOT_ID,chatID),tx):
          redis.hdel("{}Nbot:{}:STreplys".format(BOT_ID,chatID),tx)
          Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:GFreplys".format(BOT_ID,chatID),tx):
          redis.hdel("{}Nbot:{}:GFreplys".format(BOT_ID,chatID),tx)
          Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),tx):
          redis.hdel("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),tx)
          Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:AUreplys".format(BOT_ID,chatID),tx):
          redis.hdel("{}Nbot:{}:AUreplys".format(BOT_ID,chatID),tx)
          Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        elif redis.hexists("{}Nbot:{}:PHreplys".format(BOT_ID,chatID),tx):
          redis.hdel("{}Nbot:{}:PHreplys".format(BOT_ID,chatID),tx)
          Bot("sendMessage",{"chat_id":chatID,"text":r.Drp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.Norp.format(tx),"reply_to_message_id":message.message_id,"parse_mode":"html"})



    if re.search(c.pinmsg, text) and message.reply_to_message:
      if not redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID):
        ID = message.reply_to_message.message_id
        Bot("pinChatMessage",{"chat_id":chatID,"message_id":ID})
        redis.hset("{}Nbot:pinmsgs".format(BOT_ID),chatID,ID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.Dpinmsg,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      elif redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID) and GPranks(userID,chatID) == "creator":
        ID = message.reply_to_message.message_id
        Bot("pinChatMessage",{"chat_id":chatID,"message_id":ID})
        redis.hset("{}Nbot:pinmsgs".format(BOT_ID),chatID,ID)
        Bot("sendMessage",{"chat_id":chatID,"text":r.Dpinmsg,"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if re.search(c.unpinmsg, text):
        if not redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID):
          Bot("unpinChatMessage",{"chat_id":chatID})
          Bot("sendMessage",{"chat_id":chatID,"text":r.Dunpinmsg,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        if redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID) and GPranks(userID,chatID) == "creator":
          Bot("unpinChatMessage",{"chat_id":chatID})
          Bot("sendMessage",{"chat_id":chatID,"text":r.Dunpinmsg,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      
    if re.search(c.SETlink, text):
      lk = text.replace(c.RPlink,"")
      redis.hset("{}Nbot:links".format(BOT_ID),chatID,lk)
      Bot("sendMessage",{"chat_id":chatID,"text":r.Dsetlk.format(lk),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

#cre
    if rank != "admin" and rank != "owner":
      if re.search(c.deletebots, text):
        bots = [x for x in client.iter_chat_members(chatID,filter="bots") if x.user.is_bot and x.user.id !=int(BOT_ID) and x.status != "administrator"]
        if bots:
          Bot("sendMessage",{"chat_id":chatID,"text":r.LenBots.format(len(bots)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          for u in bots:
            Bot("kickChatMember",{"chat_id":chatID,"user_id":u.user.id,"until_date":int(time.time() + 60)})
            time.sleep(0.3)
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoBots,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      
      if re.search(c.deletebans, text):
        kicked = [x for x in client.iter_chat_members(chatID,filter="kicked")]
        if kicked:
          Bot("sendMessage",{"chat_id":chatID,"text":r.Lenbans.format(len(kicked)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          for u in kicked:
            Bot("unbanChatMember",{"chat_id":chatID,"user_id":u.user.id})
            redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),u.user.id)
            time.sleep(0.3)
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.NobansC,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      

      if re.search(c.deleterks, text):
        restricted = [x for x in client.iter_chat_members(chatID,filter="restricted")]
        if restricted:
          Bot("sendMessage",{"chat_id":chatID,"text":r.Lenrks.format(len(restricted)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          for u in restricted:
            Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,
          "can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,"can_invite_users": 1,})
            redis.srem("{}Nbot:{}:restricteds".format(BOT_ID,chatID),u.user.id)
            time.sleep(0.3)
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.NorksC,"reply_to_message_id":message.message_id,"parse_mode":"html"})
        
      if re.search(c.deleteDeleted, text):
        deleted = [x for x in client.iter_chat_members(chatID) if x.user.is_deleted]
        if deleted:
          Bot("sendMessage",{"chat_id":chatID,"text":r.LenDeleted.format(len(deleted)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
          for u in deleted:
            Bot("kickChatMember",{"chat_id":chatID,"user_id":u.user.id,"until_date":int(time.time() + 60)})
            time.sleep(0.3)
        else:
          Bot("sendMessage",{"chat_id":chatID,"text":r.NoDeleted,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      
      if re.search(c.delmsgs, text):
              lim = text.split(" ")[1]
              ids = []
              if message.reply_to_message:
                nu = message.reply_to_message.message_id
                ids.append(message.message_id)
              elif message.message_id:
                nu = message.message_id
              for i in range(int(lim)):
                ids.append(nu-i)
              client.delete_messages(chatID, ids)
      if re.search(c.tagall, text):
        tagall = [x for x in client.iter_chat_members(chatID)]
        if tagall:
          listTag = ""
          i = 1
          for u in tagall:
            if u.user.username:
              listTag = listTag+"\n"+str(i)+" - [@{}]".format(u.user.username)
            else:
              listTag = listTag+"\n"+str(i)+" - [{}](tg://user?id={})".format(u.user.first_name,u.user.id)
            i += 1 
          sendM("NO",listTag,message)
          
      # if re.search(c.Chlang, text):
      #   Bot("sendMessage",{"chat_id":chatID,"text":r.Chlang,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":Clang(client, message,redis,r)})
      if re.search(c.PROadmins, text):
        ads = Bot("getChatAdministrators",{"chat_id":chatID})
        for ad in ads['result']:
          userId = ad["user"]["id"]
          userFn = ad["user"]["first_name"]
          if ad['status'] == "administrator" and int(userId) != int(BOT_ID):
            setrank(redis,"admin",userId,chatID,"array")
        Bot("sendMessage",{"chat_id":chatID,"text":r.DPROadmins,"reply_to_message_id":message.message_id,"parse_mode":"html"})
