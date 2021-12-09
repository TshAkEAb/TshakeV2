from utlis.rank import setrank,isrank,remrank,remsudos,setsudo,GPranks,IDrank
from utlis.send import send_msg, BYusers, Sendto, fwdto,Name,Glang,getAge
from utlis.locks import st,getOR,Clang,st_res
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,datetime,os
import importlib


from os import listdir
from os.path import isfile, join

def updateCallback(client, callback_query,redis):
  try:
    json.loads(callback_query.data)
  except Exception as e:
    if redis.smembers("{}Nbot:botfiles".format(BOT_ID)):
      onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
      filesR = redis.smembers("{}Nbot:botfiles".format(BOT_ID))
      for f in onlyfiles:
        if f in filesR:
          fi = f.replace(".py","")
          UpMs= "files."+fi
          try:
            U = importlib.import_module(UpMs)
            t = threading.Thread(target=U.updateCb,args=(client, callback_query,redis))
            t.setDaemon(True)
            t.start()
            importlib.reload(U)
          except Exception as e:
            pass
      return False
    
    
  if callback_query.inline_message_id:
    if redis.smembers("{}Nbot:botfiles".format(BOT_ID)):
      onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
      filesR = redis.smembers("{}Nbot:botfiles".format(BOT_ID))
      for f in onlyfiles:
        if f in filesR:
          fi = f.replace(".py","")
          UpMs= "files."+fi
          try:
            U = importlib.import_module(UpMs)
            t = threading.Thread(target=U.updateCb,args=(client, callback_query,redis))
            t.setDaemon(True)
            t.start()
            importlib.reload(U)
          except Exception as e:
            pass
    return False
    
  userID = callback_query.from_user.id
  
  chatID = callback_query.message.chat.id
  userFN = callback_query.from_user.first_name
  title = callback_query.message.chat.title
  message_id = callback_query.message.message_id
  date = json.loads(callback_query.data)
  
  group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  

  if date[0] == "Cordertow":
    rank = isrank(redis,userID,chatID)
    if (rank is "sudo" or rank is "asudo" or rank is "sudos" or rank is "malk" or rank is "acreator" or rank is "creator" or rank is "owner"):
      if redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),date[1]):
        GetGprank = GPranks(date[1],chatID)
        if GetGprank == "kicked":
          Bot("unbanChatMember",{"chat_id":chatID,"user_id":date[1]})
        redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),date[1])
        Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
      else:
        Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
    return False
  if date[0] == "delBL":
    Hash = date[1]
    chat = date[3]
    if redis.sismember("{}Nbot:groups".format(BOT_ID),chat):
      redis.delete("{}Nbot:{}:{}".format(BOT_ID,chat,Hash))
      Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})
  if re.search("del(.*)replys$",date[0]):
    if int(date[2]) != userID:
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":r.notforyou,"show_alert":True})
      return 0
    t = date[0].replace("del","")
    if date[1] != "kb":
      redis.delete("{}Nbot:{}:{}".format(BOT_ID,date[1],t))
      Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})
    else:
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
      redis.delete("{}Nbot:{}:{}".format(BOT_ID,chatID,t))
      Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
  
  if re.search("del(.*)replysBOT",date[0]):
    rank = isrank(redis,userID,chatID)
    if rank == "sudo":
      t = date[0].replace("del","")
      t = t.replace("BOT","")
      if date[1] != "kb":
        redis.delete("{}Nbot:{}".format(BOT_ID,t))
        Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
        redis.delete("{}Nbot:{}".format(BOT_ID,t))
        Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
    else:
      Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":r.SudoOnle,"show_alert":True})
  if date[0] == "delfromb":
    Hash = date[1]
    chat = date[3]
    if redis.sismember("{}Nbot:groups".format(BOT_ID),chat):
      if Hash == "blockanimations":
        ID = callback_query.message.animation.file_id
        redis.srem("{}Nbot:{}:{}".format(BOT_ID,chat,Hash),ID)
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message_id})
      if Hash == "blockSTICKERs":
        ID = callback_query.message.sticker.file_id
        redis.srem("{}Nbot:{}:{}".format(BOT_ID,chat,Hash),ID)
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message_id})
      if Hash == "blockphotos":
        ID = callback_query.message.photo.file_id
        redis.srem("{}Nbot:{}:{}".format(BOT_ID,chat,Hash),ID)
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message_id})

  User_click = int((redis.get("{}Nbot:{}:floodClick".format(BOT_ID,userID)) or 1))
  if User_click > 10:
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
    Bot("sendMessage",{"chat_id":chatID,"text":r.banclick.format(BY),"disable_web_page_preview":True,"parse_mode":"html"})
    redis.setex("{}Nbot:floodUsers:{}".format(BOT_ID,userID),60*2,"Ban")
    redis.delete("{}Nbot:{}:floodClick".format(BOT_ID,userID))
  if chatID == userID:
    group = True
  if group is True and int(date[2]) == userID and not redis.get("{}Nbot:floodUsers:{}".format(BOT_ID,userID)):
    if date[0] == "delcheck":
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.notcertain, callback_data=json.dumps(["kickcheck","",userID])),InlineKeyboardButton(r.certain, callback_data=json.dumps(["certain","",userID]))]])
        random.shuffle(reply_markup.inline_keyboard[0])
        Bot("editMessageText",{"chat_id":chatID,"text":r.ucertain,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    if date[0] == "certain":
      Bot("restrictChatMember",{"chat_id": chatID,"user_id":userID,"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,"can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,})
      T ="<a href=\"tg://user?id={}\">{}</a>".format(userID,Name(userFN))
      Bot("editMessageText",{"chat_id":chatID,"text":r.unrestricted.format(T),"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      

    if date[0] == "kickcheck":
      Bot("kickChatMember",{"chat_id":chatID,"user_id":userID})
      T ="<a href=\"tg://user?id={}\">{}</a>".format(userID,Name(userFN))
      crid = redis.get("{}Nbot:{}:creator".format(BOT_ID,chatID))
      redis.sadd("{}Nbot:{}:bans".format(BOT_ID,chatID),userID)
      reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(r.Corder, callback_data=json.dumps(["Cordertow",userID]))]])
      Bot("editMessageText",{"chat_id":chatID,"text":r.bancheck.format(T),"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html","reply_markup":reply_markup})
      

    if date[0] == "delF":
      File = date[1]
      os.system("rm ./files/"+File)
      Bot("editMessageText",{"chat_id":chatID,"text":r.Delfile.format(File),"message_id":message_id,"parse_mode":"html","disable_web_page_preview":True})

    if date[0] == "delFa":
      os.system("rm -rf ./files/*")
      Bot("editMessageText",{"chat_id":chatID,"text":r.Delfiles,"message_id":message_id,"parse_mode":"html","disable_web_page_preview":True})


    if date[0] == "dlf":
      File = date[1]
      os.system("rm ./files/"+File)
      url = "https://raw.githubusercontent.com/TshAkEAb/TshakeV2-files/master/"+File
      out = requests.get(url).text
      f = open("./files/"+File,"w+")
      f.write(out)
      f.close()
      Bot("editMessageText",{"chat_id":chatID,"text":r.Dua.format(File),"message_id":message_id,"parse_mode":"html","disable_web_page_preview":True})

    if date[0] == "au":
      File = date[1]
      if redis.sismember("{}Nbot:botfiles".format(BOT_ID),File):
        redis.srem("{}Nbot:botfiles".format(BOT_ID),File)
      else:
        redis.sadd("{}Nbot:botfiles".format(BOT_ID),File)
      onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
      filesR = redis.smembers("{}Nbot:botfiles".format(BOT_ID))
      array = []
      for f in onlyfiles:
        if f in filesR:
          s = r.true
        else:
          s = r.false
        array.append([InlineKeyboardButton(f+" "+s,callback_data=json.dumps(["au",f,userID]))])
      kb = InlineKeyboardMarkup(array)
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":kb})

    if date[0] == "twostepset":
      get = date[1] 
      if get == "eq":
        redis.hset("{}Nbot:bancheck:t".format(BOT_ID),chatID,"two")
        tx = r.Ttwo
        g= "two"
      if get == "two":
        redis.hdel("{}Nbot:bancheck:t".format(BOT_ID),chatID)
        
        g= "eq"
        tx =  r.Teq
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.tset.format(tx),callback_data=json.dumps(["twostepset",g,userID]))]])
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":kb})
      


    if date[0] == "floodset":
      get = date[1] 
      if get == "ban":
        redis.hset("{}Nbot:floodset".format(BOT_ID),chatID,"res")
        tx = r.Tres
        g= "res"
      if get == "res":
        redis.hset("{}Nbot:floodset".format(BOT_ID),chatID,"ban")
        g= "ban"
        tx =  r.Tban
      kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.fset.format(tx),callback_data=json.dumps(["floodset",g,userID]))]])
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":kb})
      
    if date[0] == "delmsgclick":
      Bot("deleteMessage",{"chat_id":chatID,"message_id":message_id})
      Bot("deleteMessage",{"chat_id":chatID,"message_id":callback_query.message.reply_to_message.message_id})

    if date[0] == "ckGPs":
      rank = isrank(redis,userID,chatID)
      if rank == "sudo":
        Bot("editMessageText",{"chat_id":chatID,"text":r.ckpr,"message_id":message_id,"parse_mode":"html","disable_web_page_preview":True})
        IDS = redis.smembers("{}Nbot:groups".format(BOT_ID))
        i = 0
        for ID in IDS:
          get = Bot("getChat",{"chat_id":ID})
          if get["ok"] == False:
            redis.srem("{}Nbot:groups".format(BOT_ID),ID)
            redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),ID)
            NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
            redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),ID,str(NextDay_Date))
            i+=1
          time.sleep(0.3)
        pr = redis.scard("{}Nbot:privates".format(BOT_ID))
        gp = redis.scard("{}Nbot:groups".format(BOT_ID))
        Bot("editMessageText",{"chat_id":chatID,"text":r.showstats.format(gp,pr)+r.Dckg.format(i),"message_id":message_id,"parse_mode":"html","disable_web_page_preview":True})

      else:
        Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":r.SudoOnle,"show_alert":True})

    if date[0] == "Chlang":
      name = date[1]
      redis.srem("{}Nbot:lang:ar".format(BOT_ID),chatID)
      redis.srem("{}Nbot:lang:arem".format(BOT_ID),chatID)
      redis.srem("{}Nbot:lang:en".format(BOT_ID),chatID)
      redis.sadd("{}Nbot:lang:{}".format(BOT_ID,name),chatID)
      
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":Clang(client, callback_query,redis,r)})

    if date[0] == "ShowDateUser":
      t = IDrank(redis,userID,chatID,r)
      msgs = (redis.hget("{}Nbot:{}:msgs".format(BOT_ID,chatID),userID) or 0)
      edits = (redis.hget("{}Nbot:{}:edits".format(BOT_ID,chatID),userID) or 0)
      rate = int(msgs)*100/20000
      age = getAge(userID,r)
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(Name(userFN),url="t.me/zx_xx")],[InlineKeyboardButton(r.Rrank.format(t),url="t.me/zx_xx")],[InlineKeyboardButton(r.Rmsgs.format(msgs),url="t.me/zx_xx")],[InlineKeyboardButton(r.Rrate.format(str(rate)+"%"),url="t.me/zx_xx")],[InlineKeyboardButton(r.Redits.format(edits),url="t.me/zx_xx")],[InlineKeyboardButton(r.Rage.format(age),url="t.me/zx_xx")]])
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
    if re.search("ShowO",date[0]):
      T = date[0].replace("ShowO","")
      rank = isrank(redis,userID,chatID)
      if T == "lock":
        reply_markup = getOR(rank,r,userID)
        tx = r.LockO
      if T == "admin":
        reply_markup = getOR(rank,r,userID)
        tx = r.AdminO

      if T == "owner":
        reply_markup = getOR(rank,r,userID)
        tx = r.OwnerO

      if T == "creator":
        reply_markup = getOR(rank,r,userID)
        tx = r.CreatorO

      if T == "sudos":
        reply_markup = getOR(rank,r,userID)
        tx = r.SudosO
      if T == "sudo":
        reply_markup = getOR(rank,r,userID)
        tx = r.SudoO

      Bot("editMessageText",{"chat_id":chatID,"text":tx,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      
    if date[0] == "sendtogroups":
      Bot("editMessageText",{"chat_id":chatID,"text":r.PRsendtoGP,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      done,dont = Sendto(redis,callback_query,"groups")
      Bot("editMessageText",{"chat_id":chatID,"text":r.DsendtoGP.format(done,dont),"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      redis.delete("{}Nbot:donesend".format(BOT_ID))
      redis.delete("{}Nbot:dontsend".format(BOT_ID))
      
    if date[0] == "sendtoprivates":
      Bot("editMessageText",{"chat_id":chatID,"text":r.PRsendtoPR,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      done,dont = Sendto(redis,callback_query,"privates")
      Bot("editMessageText",{"chat_id":chatID,"text":r.DsendtoPR.format(done,dont),"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      redis.delete("{}Nbot:donesend".format(BOT_ID))
      redis.delete("{}Nbot:dontsend".format(BOT_ID))

    if date[0] == "fwdtogroups":
      Bot("editMessageText",{"chat_id":chatID,"text":r.PRsendtoGP,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      done,dont = fwdto(redis,callback_query,"groups")
      Bot("editMessageText",{"chat_id":chatID,"text":r.DsendtoGP.format(done,dont),"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      redis.delete("{}Nbot:donesend".format(BOT_ID))
      redis.delete("{}Nbot:dontsend".format(BOT_ID))
      
    if date[0] == "fwdtoprivates":
      Bot("editMessageText",{"chat_id":chatID,"text":r.PRsendtoPR,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      done,dont = fwdto(redis,callback_query,"privates")
      Bot("editMessageText",{"chat_id":chatID,"text":r.DsendtoPR.format(done,dont),"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
      redis.delete("{}Nbot:donesend".format(BOT_ID))
      redis.delete("{}Nbot:dontsend".format(BOT_ID))


    if date[0] == "kickme-yes":
      Bot("kickChatMember",{"chat_id":chatID,"user_id":userID})
      Bot("unbanChatMember",{"chat_id":chatID,"user_id":userID})
      Bot("editMessageText",{"chat_id":chatID,"text":r.Dkickme,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})
    
    if date[0] == "kickme-no":
      Bot("editMessageText",{"chat_id":chatID,"text":r.Nkickme,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html"})

    if date[0] == "delfromb":
      Hash = date[1]
      if Hash == "blockanimations":
        ID = callback_query.message.animation.file_id
        redis.srem("{}Nbot:{}:{}".format(BOT_ID,chatId,TY),ID)
        Bot("editMessageText",{"chat_id":chatID,"text":r.DoneUNblock,"message_id":message_id,"disable_web_page_preview":True})

    if date[0] == "Blocklist":
      Botuser = client.get_me().username
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STword,callback_data=json.dumps(["showBlocklist","",userID])),InlineKeyboardButton(c.STgifs,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockanimations")),],[InlineKeyboardButton(c.STphoto,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockphotos")),InlineKeyboardButton(c.STsticker,url="https://telegram.me/{}?start=showBlocklist={}={}={}".format(Botuser,chatID,userID,"blockSTICKERs")),]])
      Bot("editMessageText",{"chat_id":chatID,"text":r.blocklist.format(r.blocklist2,title),"message_id":message_id,"parse_mode":"html","reply_markup":reply_markup})
    if date[0] == "replylist":
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STword,callback_data=json.dumps(["showreplylist","",userID])),InlineKeyboardButton(c.STgifs,callback_data=json.dumps(["showGFreplylist","",userID])),],[InlineKeyboardButton(c.STvoice,callback_data=json.dumps(["showVOreplylist","",userID])),InlineKeyboardButton(c.STsticker,callback_data=json.dumps(["showSTreplylist","",userID])),],[InlineKeyboardButton("Mp3",callback_data=json.dumps(["showAUreplylist","",userID]))]])
      Bot("editMessageText",{"chat_id":chatID,"text":r.blocklist.format(r.replylist,title),"message_id":message_id,"parse_mode":"html","reply_markup":reply_markup})
    if date[0] == "replylistBOT":
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(c.STword,callback_data=json.dumps(["showreplylistBOT","",userID])),InlineKeyboardButton(c.STgifs,callback_data=json.dumps(["showGFreplylistBOT","",userID])),],[InlineKeyboardButton(c.STvoice,callback_data=json.dumps(["showVOreplylistBOT","",userID])),InlineKeyboardButton(c.STsticker,callback_data=json.dumps(["showSTreplylistBOT","",userID])),]])
      Bot("editMessageText",{"chat_id":chatID,"text":r.blocklist.format(r.replylistBot,title),"message_id":message_id,"parse_mode":"html","reply_markup":reply_markup})
    
    if date[0] == "alllist":
      reply_markup=InlineKeyboardMarkup(
          [[InlineKeyboardButton(c.STbanall,callback_data=json.dumps(["showbanall","",userID]))
          ,InlineKeyboardButton(c.STtkall,callback_data=json.dumps(["showtkall","",userID])),]
          ])
      Bot("editMessageText",{"chat_id":chatID,"text":r.banlist,"message_id":message_id,"parse_mode":"html","reply_markup":reply_markup})
    
    if date[0] == "delallban":
      redis.delete("{}Nbot:bans".format(BOT_ID))
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["alllist","",userID])),]])
      Bot("editMessageText",{"chat_id":chatID,"text":r.Ddelbanall,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html","reply_markup":reply_markup})

    if date[0] == "delalltk":
      redis.delete("{}Nbot:restricteds".format(BOT_ID))
      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["alllist","",userID])),]])
      Bot("editMessageText",{"chat_id":chatID,"text":r.Ddeltkall,"message_id":message_id,"disable_web_page_preview":True,"parse_mode":"html","reply_markup":reply_markup})
      
    if date[0] == "showBlocklist":
      li = redis.smembers("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - "+word
          i += 1
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.BlocklistRm,callback_data=json.dumps(["delListblockTEXTs","",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["Blocklist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["Blocklist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.BlocklistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
    
    if date[0] == "showbanall":
      arrays = redis.smembers("{}Nbot:bans".format(BOT_ID))
      if arrays:
        b = BYusers(arrays,chatID,redis,client)
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.allbandel,callback_data=json.dumps(["delallban","",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["alllist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":b,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup,"parse_mode":"markdown"})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["alllist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.allbanE,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    if date[0] == "showtkall":
      arrays = redis.smembers("{}Nbot:restricteds".format(BOT_ID))
      if arrays:
        b = BYusers(arrays,chatID,redis,client)
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.alltkdel,callback_data=json.dumps(["delalltk","",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["alllist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":b,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup,"parse_mode":"markdown"})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["alllist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.alltkE,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
    
    if date[0] == "showreplylist":
      li = redis.hkeys("{}Nbot:{}:TXreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylist={}={}={}".format(Botuser,chatID,userID,"TXreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.replylistRm,callback_data=json.dumps(["delTXreplys","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.replylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    if date[0] == "showAUreplylist":
      li = redis.hkeys("{}Nbot:{}:AUreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylist={}={}={}".format(Botuser,chatID,userID,"STreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📂꒐ قائمة الصوتيات فارغة",callback_data=json.dumps(["delSTreplys","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":"📂꒐ قائمة الصوتيات فارغة","message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})


    if date[0] == "showSTreplylist":
      li = redis.hkeys("{}Nbot:{}:STreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylist={}={}={}".format(Botuser,chatID,userID,"STreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.STreplylistRm,callback_data=json.dumps(["delSTreplys","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.STreplylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})


    if date[0] == "showGFreplylist":
      li = redis.hkeys("{}Nbot:{}:GFreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylist={}={}={}".format(Botuser,chatID,userID,"GFreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.GFreplylistRm,callback_data=json.dumps(["delGFreplys","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.GFreplylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    if date[0] == "showVOreplylist":
      li = redis.hkeys("{}Nbot:{}:VOreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylist={}={}={}".format(Botuser,chatID,userID,"VOreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.VOreplylistRm,callback_data=json.dumps(["delVOreplys","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylist","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.VOreplylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    if date[0] == "showreplylistBOT":
      li = redis.hkeys("{}Nbot:TXreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylistBOT={}={}={}".format(Botuser,chatID,userID,"TXreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.replylistRm,callback_data=json.dumps(["delTXreplysBOT","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.replylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})


    if date[0] == "showSTreplylistBOT":
      li = redis.hkeys("{}Nbot:STreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylistBOT={}={}={}".format(Botuser,chatID,userID,"STreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.STreplylistRm,callback_data=json.dumps(["delSTreplysBOT","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.STreplylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})


    if date[0] == "showGFreplylistBOT":
      li = redis.hkeys("{}Nbot:GFreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylistBOT={}={}={}".format(Botuser,chatID,userID,"GFreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.GFreplylistRm,callback_data=json.dumps(["delGFreplysBOT","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.GFreplylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    if date[0] == "showVOreplylistBOT":
      li = redis.hkeys("{}Nbot:VOreplys".format(BOT_ID,chatID))
      if li:
        words = ""
        i = 1
        for word in li:
          words = words+"\n"+str(i)+" - {"+word+"}"
          i += 1
        if len(words) > 3000:
          Botuser = client.get_me().username
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.clickTOpv,url="https://telegram.me/{}?start=showreplylistBOT={}={}={}".format(Botuser,chatID,userID,"VOreplys")),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":r.Toolong,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
        else:
          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.VOreplylistRm,callback_data=json.dumps(["delVOreplysBOT","kb",userID])),],[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
          Bot("editMessageText",{"chat_id":chatID,"text":words,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
      else:
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("<<",callback_data=json.dumps(["replylistBOT","",userID])),]])
        Bot("editMessageText",{"chat_id":chatID,"text":r.VOreplylistEm,"message_id":message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

    
    if date[0] == "listCH":
      if int(date[1]) != 4:
        Bot("editMessageText",{"chat_id":chatID,"text":r.settings.format(title),"message_id":message_id,"disable_web_page_preview":True,"reply_markup":st(client, callback_query,redis,int(date[1])),"parse_mode":"html"})
        #Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"reply_markup":st(client, callback_query,redis,int(date[3]))})
      else:
        T = (redis.hget("{}Nbot:time_ck".format(BOT_ID),chatID) or 3)
        m = (redis.hget("{}Nbot:max_msg".format(BOT_ID),chatID) or 10)
        Bot("editMessageText",{"chat_id":chatID,"text":r.st2.format(T,m),"message_id":message_id,"disable_web_page_preview":True,"reply_markup":st(client, callback_query,redis,int(date[1])),"parse_mode":"html"})
    if date[0] == "listCH-res":
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"reply_markup":st_res(client, callback_query,redis,int(date[1]))})


      #Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"reply_markup":st(client, callback_query,redis,int(date[1]))})
    if date[0] == 'LU-res':
      d = date[1].split("-")
      lock = d[0]
      lockres = d[0]+":"+d[1]
      if redis.sismember("{}Nbot:{}".format(BOT_ID,lockres),chatID):
        redis.srem("{}Nbot:{}".format(BOT_ID,lockres),chatID)
      else:
        redis.sadd("{}Nbot:{}".format(BOT_ID,lockres),chatID)
        redis.sadd("{}Nbot:{}".format(BOT_ID,lock),chatID)
      Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"reply_markup":st_res(client, callback_query,redis,int(date[3]))})


    
    
    if date[0] == 'LU':
      if redis.sismember("{}Nbot:{}".format(BOT_ID,date[1]),chatID):
        save = redis.srem("{}Nbot:{}".format(BOT_ID,date[1]),chatID)
      else:
        save = redis.sadd("{}Nbot:{}".format(BOT_ID,date[1]),chatID)
      if int(date[3]) != 4:
        Bot("editMessageText",{"chat_id":chatID,"text":r.settings.format(title),"message_id":message_id,"disable_web_page_preview":True,"reply_markup":st(client, callback_query,redis,int(date[3])),"parse_mode":"html"})
        #Bot("editMessageReplyMarkup",{"chat_id":chatID,"message_id":message_id,"reply_markup":st(client, callback_query,redis,int(date[3]))})
      else:
        T = (redis.hget("{}Nbot:time_ck".format(BOT_ID),chatID) or 3)
        m = (redis.hget("{}Nbot:max_msg".format(BOT_ID),chatID) or 10)
        Bot("editMessageText",{"chat_id":chatID,"text":r.st2.format(T,m),"message_id":message_id,"disable_web_page_preview":True,"reply_markup":st(client, callback_query,redis,int(date[3])),"parse_mode":"html"})

    if date[0] == "delListblockTEXTs":
      redis.delete("{}Nbot:{}:blockTEXTs".format(BOT_ID,chatID))
      Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})

    if date[0] == "delListbans":
      arrays = redis.smembers("{}Nbot:{}:bans".format(BOT_ID,chatID))
      for user in arrays:
        GetGprank = GPranks(user,chatID)
        if GetGprank == "kicked":
          Bot("unbanChatMember",{"chat_id":chatID,"user_id":user})
        redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),user)
      Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})

    if date[0] == "delListrestricteds":
      arrays = redis.smembers("{}Nbot:{}:restricteds".format(BOT_ID,chatID))
      for user in arrays:
        GetGprank = GPranks(user,chatID)
        if GetGprank == "restricted":
          Bot("restrictChatMember",{"chat_id": chatID,"user_id": user,"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,"can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,})
        redis.srem("{}Nbot:{}:restricteds".format(BOT_ID,chatID),user)
      Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})

    if date[0] == "LandU":
      if date[3] == "LtoU":
        if redis.sismember("{}Nbot:{}".format(BOT_ID,date[1]),chatID):
          redis.srem("{}Nbot:{}".format(BOT_ID,date[1]),chatID)
          Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
        else:
          Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
      if date[3] == "UtoL":
        if redis.sismember("{}Nbot:{}".format(BOT_ID,date[1]),chatID):
          Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
        else:
          redis.sadd("{}Nbot:{}".format(BOT_ID,date[1]),chatID)
          Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
    
    if date[0] == "Corder":
      if date[1] == "bans":
        if date[4] == "UtoB":
          if redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),date[3]):
            Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
          else:
            GetGprank = GPranks(date[3],chatID)
            if GetGprank == "kicked":
              Bot("kickChatMember",{"chat_id":chatID,"user_id":date[3]})
            redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),date[3])
            Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
        if date[4] == "BtoU":
          if redis.sismember("{}Nbot:{}:bans".format(BOT_ID,chatID),date[3]):
            GetGprank = GPranks(date[3],chatID)
            if GetGprank == "kicked":
              Bot("unbanChatMember",{"chat_id":chatID,"user_id":date[3]})
            redis.srem("{}Nbot:{}:bans".format(BOT_ID,chatID),date[3])
            Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
          else:
            Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
      
      if date[1] == "restricteds":
        if date[4] == "UtoB":
          if redis.sismember("{}Nbot:{}:restricteds".format(BOT_ID,chatID),date[3]):
            Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
          else:
            GetGprank = GPranks(date[3],chatID)
            if GetGprank == "restricted":
              Bot("restrictChatMember",{"chat_id": chatID,"user_id": date[3],"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,"can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,})
            redis.sadd("{}Nbot:{}:restricteds".format(BOT_ID,chatID),date[3])
            Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
        if date[4] == "BtoU":
          if redis.sismember("{}Nbot:{}:restricteds".format(BOT_ID,chatID),date[3]):
            GetGprank = GPranks(date[3],chatID)
            if GetGprank == "restricted":
              Bot("restrictChatMember",{"chat_id": chatID,"user_id": date[3],"can_send_messages": 1,"can_send_media_messages": 1,"can_send_other_messages": 1,"can_send_polls": 1,"can_change_info": 1,"can_add_web_page_previews": 1,"can_pin_messages": 1,})
            redis.srem("{}Nbot:{}:restricteds".format(BOT_ID,chatID),date[3])
            Bot("editMessageText",{"chat_id":chatID,"text":r.doneCO,"message_id":message_id,"disable_web_page_preview":True})
          else:
            Bot("editMessageText",{"chat_id":chatID,"text":r.ARdoneCO,"message_id":message_id,"disable_web_page_preview":True})
    
    if date[0] == "delList":
      H = date[1]


      if H != "sudos" and H != "creator" and H != "asudos":
        redis.delete("{}Nbot:{}:{}".format(BOT_ID,chatID,H))
        Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})
      if H == "sudos" or H == "asudo":
        redis.delete("{}Nbot:{}".format(BOT_ID,H))
        Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})
      if H == "creator":
        redis.delete("{}Nbot:{}:{}".format(BOT_ID,chatID,H))
        Bot("editMessageText",{"chat_id":chatID,"text":r.DoneDelList,"message_id":message_id,"disable_web_page_preview":True})
    redis.setex("{}Nbot:{}:floodClick".format(BOT_ID,userID), 3, User_click+1)
    Bot("answerCallbackQuery",{"callback_query_id":callback_query.id})
  elif int(date[2]) != userID:
    Bot("answerCallbackQuery",{"callback_query_id":callback_query.id,"text":r.notforyou,"show_alert":True})
    redis.setex("{}Nbot:{}:floodClick".format(BOT_ID,userID), 3, User_click+1)

  if redis.smembers("{}Nbot:botfiles".format(BOT_ID)):
    onlyfiles = [f for f in listdir("files") if isfile(join("files", f))]
    filesR = redis.smembers("{}Nbot:botfiles".format(BOT_ID))
    for f in onlyfiles:
      if f in filesR:
        fi = f.replace(".py","")
        UpMs= "files."+fi
        try:
          U = importlib.import_module(UpMs)
          t = threading.Thread(target=U.updateCb,args=(client, callback_query,redis))
          t.setDaemon(True)
          t.start()
          importlib.reload(U)
        except Exception as e:
          pass

