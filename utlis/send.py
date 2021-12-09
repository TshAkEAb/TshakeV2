from utlis.rank import setrank,isrank,remrank,remsudos,setsudo
from utlis.tg import Bot
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json ,os ,datetime
import importlib

def send_msg(type,client, message,textM,Lhash,T,redis):
  userID = message.from_user.id
  userFN = message.from_user.first_name
  chatID = message.chat.id
  text = message.text

  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  if type == "LU":
    if re.search(c.stL, text):
      Tp = "LtoU"
    if re.search(c.stU, text):
      Tp = "UtoL"
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
    tx = textM.format(BY,T)
    b = json.dumps(["LandU",Lhash,userID,Tp])
    v = InlineKeyboardMarkup([[InlineKeyboardButton(r.Corder, callback_data=b)]])
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":v})
  if type == "LUN":
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
    tx = textM.format(BY,T)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

  if type == "UD":
    R = text.split(" ")[1]
    userId = T.id
    userFn = Name(T.first_name)
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
    tx = textM.format(BY,R)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

  if type == "BN":
    userId = T.id
    userFn = Name(T.first_name)
    BY = "[{}](tg://user?id={})".format(userFn,userId)
    tx = textM.format(BY)
    if re.search(c.stC, text):
      Tp = "UtoB"
    else:
      Tp = "BtoU"
    b = json.dumps(["Corder",Lhash,userID,userId,Tp])
    v = InlineKeyboardMarkup([[InlineKeyboardButton(r.Corder, callback_data=b)]])
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"markdown","disable_web_page_preview":True,"reply_markup":v})
  
  if type == "BNN":
    userId = T.id
    userFn = Name(T.first_name)
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
    tx = textM.format(BY)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
  


def BYusers(arrays,chatID,redis,client):
  users = ""
  i = 0
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  for user in arrays:
    i +=1
    try:
      getUser = client.get_users(user)
      userId = getUser.id
      userFn = getUser.first_name
      users = users+"\n"+str(i)+" - "+"[{}](tg://user?id={})".format(userFn,userId)
    except Exception as e:
      users = users+"\n"+str(i)+" - "+"[{}](tg://user?id={})".format(user,user)
      print(e)
  return users

def CKsend(redis,callback_query,type,ck,sID):
  if ck["ok"] == False and not redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),sID):
    redis.sadd("{}Nbot:dontsend".format(BOT_ID),sID)
    if type == "privates":
      redis.srem("{}Nbot:privates".format(BOT_ID),sID)
    else:
      redis.srem("{}Nbot:groups".format(BOT_ID),sID)
  elif ck["ok"]:
    redis.sadd("{}Nbot:donesend".format(BOT_ID),sID)

def Sendto(redis,callback_query,type):
  IDS = redis.smembers("{}Nbot:{}".format(BOT_ID,type))
  if callback_query.message.reply_to_message.text:
    for sID in IDS:
     ck = Bot("sendMessage",{"chat_id":sID,"text":callback_query.message.reply_to_message.text,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.photo:
    ID = callback_query.message.reply_to_message.photo.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendphoto",{"chat_id":sID,"photo":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.video:
    ID = callback_query.message.reply_to_message.video.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendvideo",{"chat_id":sID,"video":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.video_note:
    ID = callback_query.message.reply_to_message.video_note.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendVideoNote",{"chat_id":sID,"video_note":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.voice:
    ID = callback_query.message.reply_to_message.voice.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendvoice",{"chat_id":sID,"voice":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.audio:
    ID = callback_query.message.reply_to_message.audio.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendaudio",{"chat_id":sID,"audio":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.sticker:
    ID = callback_query.message.reply_to_message.sticker.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendsticker",{"chat_id":sID,"sticker":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)
     
  if callback_query.message.reply_to_message.document:
    ID = callback_query.message.reply_to_message.document.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("senddocument",{"chat_id":sID,"document":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.animation:
    ID = callback_query.message.reply_to_message.animation.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendanimation",{"chat_id":sID,"animation":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)
  

  return redis.scard("{}Nbot:donesend".format(BOT_ID)),redis.scard("{}Nbot:dontsend".format(BOT_ID))



def fwdto(redis,callback_query,type):
  IDS = redis.smembers("{}Nbot:{}".format(BOT_ID,type))
  if callback_query.message.reply_to_message.message_id:
    for sID in IDS:
      ck = Bot("forwardMessage",{"chat_id":sID,"from_chat_id":callback_query.message.chat.id,"message_id":callback_query.message.reply_to_message.message_id})
      CKsend(redis,callback_query,type,ck,sID)
      time.sleep(0.3)
  return redis.scard("{}Nbot:donesend".format(BOT_ID)),redis.scard("{}Nbot:dontsend".format(BOT_ID))

def sendM(T,msg,message):
  if T == "NO":
    chatID = message.chat.id
    Len = 3000
    msgs = [msg[y-Len:y] for y in range(Len, len(msg)+Len,Len)]
    for tx in msgs:
      Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"markdown","disable_web_page_preview":True})
      time.sleep(0.3)

def GetLink(chatID):
  li = Bot("getchat",{"chat_id":chatID})["result"]
  if "invite_link" in li:
    return li["invite_link"]
  else:
    Bot("exportChatInviteLink",{"chat_id":chatID})
    li = Bot("getchat",{"chat_id":chatID})["result"]
    if "invite_link" in li:
      return li["invite_link"]
    else:
      return False
  

def Name(name):
  Len = 10
  names = [name[y-Len:y] for y in range(Len, len(name)+Len,Len)]
  return names[0]


def run(redis,chatID):
  redis.set("{}:Nbot:restart".format(BOT_ID),chatID)
  os.system("pm2 restart {}".format(BOT_ID))

def Glang(redis,chatID):
  if redis.sismember("{}Nbot:lang:ar".format(BOT_ID),chatID):
    lang = "ar"
  elif redis.sismember("{}Nbot:lang:en".format(BOT_ID),chatID):
    lang = "en"
  elif redis.sismember("{}Nbot:lang:arem".format(BOT_ID),chatID):
    lang = "arem"
  else :
    lang = "arem"
  return lang

#from https://github.com/wjclub/telegram-bot-getids/blob/master/idage.js
def getDate(userID):
    ages = {
        "2768409"   : 1383264000,
        "7679610"   : 1388448000,
        "11538514"  : 1391212000,
        "15835244"  : 1392940000,
        "23646077"  : 1393459000,
        "38015510"  : 1393632000,
        "44634663"  : 1399334000,
        "46145305"  : 1400198000,
        "54845238"  : 1411257000,
        "63263518"  : 1414454000,
        "101260938" : 1425600000,
        "101323197" : 1426204000,
        "111220210" : 1433376000,
        "103258382" : 1432771000,
        "103151531" : 1439078000,
        "116812045" : 1429574000,
        "122600695" : 1439683000,
        "109393468" : 1437696000,
        "112594714" : 1437782000,
        "124872445" : 1439856000,
        "130029930" : 1444003000,
        "125828524" : 1441324000,
        "133909606" : 1444176000,
        "157242073" : 1448928000,
        "143445125" : 1452211000,
        "148670295" : 1453420000,
        "152079341" : 1446768000,
        "171295414" : 1457481000,
        "181783990" : 1460246000,
        "222021233" : 1465344000,
        "225034354" : 1466208000,
        "278941742" : 1473465000,
        "285253072" : 1476835000,
        "294851037" : 1479600000,
        "297621225" : 1481846000,
        "328594461" : 1482969000,
        "337808429" : 1487707000,
        "341546272" : 1487782000,
        "352940995" : 1487894000,
        "369669043" : 1490918000,
        "400169472" : 1501459000,
        "805158066" : 1563208000
    }
    
    ids = list(ages.keys())
    nids = [int(x) for x in ids]
    minId = nids[0]
    maxId = nids[len(nids) - 1]
    
    if userID < minId:
        return [-1, ages[ids[0]]]
    elif userID > maxId:
        return [1, ages[ids[len(ids) - 1]]]
    else:
        lid = nids[0]
        i = 0
        while i < len(ids):
            if userID <= nids[i] :
                uid = nids[i]
                lage = ages[str(lid)]
                uage = ages[str(uid)]
                idratio = ((userID - lid) / (uid - lid))
                midDate = (idratio * (uage - lage)) + lage
                return [0, midDate]
            else:
                lid = nids[i]
            i += 1
def getAge(userID,r):
    ar = getDate(userID)
    dt = datetime.datetime.fromtimestamp(ar[1]).strftime('%Y/%m')
    if ar[0] < 0:
        v = 'older_than'
    elif ar[0] > 0:
        v = 'newer_than'
    else:
        v = 'aprox'
    t = "{} {}".format(r.age[v],dt)
    return t
