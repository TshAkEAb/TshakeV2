from utlis.rank import setrank,isrank,remrank,remsudos,setsudo
from config import *
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,importlib
from os import listdir
from os.path import isfile, join

def getOR(rank,r,userID):
  if rank == "admin":
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.lockC,callback_data=json.dumps(["ShowOlock","",userID])),InlineKeyboardButton(r.AdminC,callback_data=json.dumps(["ShowOadmin","",userID])),],])
  if rank == "owner":
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.lockC,callback_data=json.dumps(["ShowOlock","",userID])),InlineKeyboardButton(r.AdminC,callback_data=json.dumps(["ShowOadmin","",userID])),],[InlineKeyboardButton(r.OwnerC,callback_data=json.dumps(["ShowOowner","",userID])),],])
  if rank == "creator" or rank == "acreator" or rank == "malk":
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.lockC,callback_data=json.dumps(["ShowOlock","",userID])),InlineKeyboardButton(r.AdminC,callback_data=json.dumps(["ShowOadmin","",userID])),],[InlineKeyboardButton(r.OwnerC,callback_data=json.dumps(["ShowOowner","",userID])),InlineKeyboardButton(r.CreatorC,callback_data=json.dumps(["ShowOcreator","",userID])),],])
  if rank == "sudos":
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.lockC,callback_data=json.dumps(["ShowOlock","",userID])),InlineKeyboardButton(r.AdminC,callback_data=json.dumps(["ShowOadmin","",userID])),],[InlineKeyboardButton(r.OwnerC,callback_data=json.dumps(["ShowOowner","",userID])),InlineKeyboardButton(r.CreatorC,callback_data=json.dumps(["ShowOcreator","",userID])),],[InlineKeyboardButton(r.SudosC,callback_data=json.dumps(["ShowOsudos","",userID])),],])
  if rank == "sudo" or rank == "asudo":
    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.lockC,callback_data=json.dumps(["ShowOlock","",userID])),InlineKeyboardButton(r.AdminC,callback_data=json.dumps(["ShowOadmin","",userID])),],[InlineKeyboardButton(r.OwnerC,callback_data=json.dumps(["ShowOowner","",userID])),InlineKeyboardButton(r.CreatorC,callback_data=json.dumps(["ShowOcreator","",userID])),],[InlineKeyboardButton(r.SudosC,callback_data=json.dumps(["ShowOsudos","",userID])),InlineKeyboardButton(r.SudoC,callback_data=json.dumps(["ShowOsudo","",userID])),],])
  return (reply_markup or "")


def st(client, message,redis,type = 1):
  userID = message.from_user.id
  if (hasattr(message,"chat")):
    chatID = message.chat.id
  else:
    chatID = message.message.chat.id
  rank = isrank(redis,userID,chatID)
  
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  if redis.sismember("{}Nbot:Llink".format(BOT_ID),chatID):
    link = c.STlink+" "+r.false
  else:
    link = c.STlink+" "+r.true

  if redis.sismember("{}Nbot:Lusername".format(BOT_ID),chatID):#2
    username = c.STusername+" "+r.false
  else:
    username = c.STusername+" "+r.true

  if redis.sismember("{}Nbot:Ltag".format(BOT_ID),chatID):#3
    tag = c.STtag+" "+r.false
  else:
    tag = c.STtag+" "+r.true

  if redis.sismember("{}Nbot:Lenglish".format(BOT_ID),chatID):#4
    english = c.STenglish+" "+r.false
  else:
    english = c.STenglish+" "+r.true

  if redis.sismember("{}Nbot:Larabic".format(BOT_ID),chatID):#5
    arabic = c.STarabic+" "+r.false
  else:
    arabic = c.STarabic+" "+r.true

  if redis.sismember("{}Nbot:Lmarkdown".format(BOT_ID),chatID):#6
    markdown = c.STmarkdown+" "+r.false
  else:
    markdown = c.STmarkdown+" "+r.true

  if redis.sismember("{}Nbot:Linline".format(BOT_ID),chatID):#7
    inline = c.STinline+" "+r.false
  else:
    inline = c.STinline+" "+r.true

  if redis.sismember("{}Nbot:Lsticker".format(BOT_ID),chatID):#8
    sticker = c.STsticker+" "+r.false
  else:
    sticker = c.STsticker+" "+r.true

  if redis.sismember("{}Nbot:Lgifs".format(BOT_ID),chatID):#9
    gifs = c.STgifs+" "+r.false
  else:
    gifs = c.STgifs+" "+r.true

  if redis.sismember("{}Nbot:Lvideo".format(BOT_ID),chatID):#10
    video = c.STvideo+" "+r.false
  else:
    video = c.STvideo+" "+r.true

  if redis.sismember("{}Nbot:Lvoice".format(BOT_ID),chatID):#11
    voice = c.STvoice+" "+r.false
  else:
    voice = c.STvoice+" "+r.true

  if redis.sismember("{}Nbot:Lmusic".format(BOT_ID),chatID):#12
    music = c.STmusic+" "+r.false
  else:
    music = c.STmusic+" "+r.true

  if redis.sismember("{}Nbot:Lfiles".format(BOT_ID),chatID):#13
    files = c.STfiles+" "+r.false
  else:
    files = c.STfiles+" "+r.true

  if redis.sismember("{}Nbot:Lphoto".format(BOT_ID),chatID):#14
    photo = c.STphoto+" "+r.false
  else:
    photo = c.STphoto+" "+r.true

  if redis.sismember("{}Nbot:Lcontact".format(BOT_ID),chatID):#15
    contact = c.STcontact+" "+r.false
  else:
    contact = c.STcontact+" "+r.true

  if redis.sismember("{}Nbot:Lbots".format(BOT_ID),chatID):#16
    bots = c.STbots+" "+r.false
  else:
    bots = c.STbots+" "+r.true

  if redis.sismember("{}Nbot:Ljoin".format(BOT_ID),chatID):#17
    join = c.STjoin+" "+r.false
  else:
    join = c.STjoin+" "+r.true

  if redis.sismember("{}Nbot:Lfwd".format(BOT_ID),chatID):#18
    fwd = c.STfwd+" "+r.false
  else:
    fwd = c.STfwd+" "+r.true

  if redis.sismember("{}Nbot:Lnote".format(BOT_ID),chatID):#19
    note = c.STnote+" "+r.false
  else:
    note = c.STnote+" "+r.true
  if redis.sismember("{}Nbot:Ledits".format(BOT_ID),chatID):#19
    edits = c.STedits+" "+r.false
  else:
    edits = c.STedits+" "+r.true
  if redis.sismember("{}Nbot:Llongtext".format(BOT_ID),chatID):#19
    longtext = c.STlongtext+" "+r.false
  else:
    longtext = c.STlongtext+" "+r.true

  if redis.sismember("{}Nbot:Lflood".format(BOT_ID),chatID):#19
    flood = c.STflood+" "+r.false
  else:
    flood = c.STflood+" "+r.true
  if not redis.sismember("{}Nbot:welcomeSend".format(BOT_ID),chatID):
    welcomeSend = c.STwelcomeSend+" "+r.true
  else:
    welcomeSend = c.STwelcomeSend+" "+r.false

  if not redis.sismember("{}Nbot:ReplySend".format(BOT_ID),chatID):
    ReplySend = c.STReplySend+" "+r.true
  else:
    ReplySend = c.STReplySend+" "+r.false

  if not redis.sismember("{}Nbot:ReplySendBOT".format(BOT_ID),chatID):
    ReplySendBOT = c.STReplySendBOT+" "+r.true
  else:
    ReplySendBOT = c.STReplySendBOT+" "+r.false

  if not redis.sismember("{}Nbot:kickme".format(BOT_ID),chatID):
    kickme = c.STkickme+" "+r.true
  else:
    kickme = c.STkickme+" "+r.false

  if redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID):
    pin = c.STpin+" "+r.false
  else:
    pin = c.STpin+" "+r.true

  if not redis.sismember("{}Nbot:IDSend".format(BOT_ID),chatID):
    IDSend = c.STIDSend+" "+r.true
  else:
    IDSend = c.STIDSend+" "+r.false

  if redis.sismember("{}Nbot:bancheck".format(BOT_ID),chatID):
    bancheck = c.STbancheck+" "+r.true
  else:
    bancheck = c.STbancheck+" "+r.false

  if type == 1:
    reply_markup=InlineKeyboardMarkup([
        [
          InlineKeyboardButton(link,callback_data=json.dumps(["LU","Llink",userID,1])),
          InlineKeyboardButton(bots,callback_data=json.dumps(["LU","Lbots",userID,1])),
          ],[
            InlineKeyboardButton(video,callback_data=json.dumps(["LU","Lvideo",userID,1])),
            InlineKeyboardButton(note,callback_data=json.dumps(["LU","Lnote",userID,1])),
            ],[
              InlineKeyboardButton(music,callback_data=json.dumps(["LU","Lmusic",userID,1])),
              InlineKeyboardButton(voice,callback_data=json.dumps(["LU","Lvoice",userID,1]))
              ],[
                InlineKeyboardButton(gifs,callback_data=json.dumps(["LU","Lgifs",userID,1])),
                InlineKeyboardButton(photo,callback_data=json.dumps(["LU","Lphoto",userID,1])),
                ],[
                  InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),
                  InlineKeyboardButton(r.fr,callback_data=json.dumps(["listCH",2,userID])),
                  ]
                  ])

  if type == 2:
    reply_markup=InlineKeyboardMarkup([
        [
          InlineKeyboardButton(inline,callback_data=json.dumps(["LU","Linline",userID,2])),
          InlineKeyboardButton(markdown,callback_data=json.dumps(["LU","Lmarkdown",userID,2])),
          ],[
            InlineKeyboardButton(files,callback_data=json.dumps(["LU","Lfiles",userID,2])),
            InlineKeyboardButton(contact,callback_data=json.dumps(["LU","Lcontact",userID,2])),
            ],[
              InlineKeyboardButton(sticker,callback_data=json.dumps(["LU","Lsticker",userID,2])),
              InlineKeyboardButton(fwd,callback_data=json.dumps(["LU","Lfwd",userID,2])),
              ],[
                InlineKeyboardButton(username,callback_data=json.dumps(["LU","Lusername",userID,2])),
                InlineKeyboardButton(english,callback_data=json.dumps(["LU","Lenglish",userID,2])),
                ],[
                  InlineKeyboardButton(r.pk,callback_data=json.dumps(["listCH",1,userID])),
                  InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),
                  InlineKeyboardButton(r.fr,callback_data=json.dumps(["listCH",3,userID])),
                  ]
                  ])

  if type == 3:
    if rank != "admin":
      t = [InlineKeyboardButton(r.pk,callback_data=json.dumps(["listCH",2,userID])),
      InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),
      InlineKeyboardButton(r.fr,callback_data=json.dumps(["listCH",4,userID]))]
    else:
      t = [InlineKeyboardButton(r.pk,callback_data=json.dumps(["listCH",2,userID])),]
    reply_markup=InlineKeyboardMarkup([
        [
                       InlineKeyboardButton(arabic,callback_data=json.dumps(["LU","Larabic",userID,3])),
                    InlineKeyboardButton(tag,callback_data=json.dumps(["LU","Ltag",userID,3])),
          ],[
                    InlineKeyboardButton(join,callback_data=json.dumps(["LU","Ljoin",userID,3])),
                    InlineKeyboardButton(edits,callback_data=json.dumps(["LU","Ledits",userID,3])),
            ],[
                    InlineKeyboardButton(longtext,callback_data=json.dumps(["LU","Llongtext",userID,3])),
              ],t
                  ])
  if type == 4:
    reply_markup=InlineKeyboardMarkup([
        [
                    InlineKeyboardButton(flood,callback_data=json.dumps(["LU","Lflood",userID,4])),
                    InlineKeyboardButton(welcomeSend,callback_data=json.dumps(["LU","welcomeSend",userID,4])),
          ],[
                    InlineKeyboardButton(ReplySend,callback_data=json.dumps(["LU","ReplySend",userID,4])),
                    InlineKeyboardButton(ReplySendBOT,callback_data=json.dumps(["LU","ReplySendBOT",userID,4])),
            ],[
                    InlineKeyboardButton(kickme,callback_data=json.dumps(["LU","kickme",userID,4])),
                    InlineKeyboardButton(pin,callback_data=json.dumps(["LU","Lpin",userID,4])),
              ],[
                    InlineKeyboardButton(IDSend,callback_data=json.dumps(["LU","IDSend",userID,4])),
                    InlineKeyboardButton(bancheck,callback_data=json.dumps(["LU","bancheck",userID,4])),
              ],[
                  InlineKeyboardButton(r.pk,callback_data=json.dumps(["listCH",3,userID])),InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),
                  ]
                  ])
  return reply_markup

def Cklang(name,r,redis,chatID):
  if redis.sismember("{}Nbot:lang:{}".format(BOT_ID,name),chatID):
    return r.true
  else:
    return ""
def Clang(client, message,redis,r):
  if (hasattr(message,"chat")):
    chatID = message.chat.id
  else:
    chatID = message.message.chat.id
  userID = message.from_user.id
  onlyfiles = [f for f in listdir("lang") if isfile(join("lang", f))]
  array = []
  names = []
  i = 0
  for f in onlyfiles:
    name = f.split("-")[0]
    if name not in names:
      array.append([InlineKeyboardButton(r.lang[name]+" "+Cklang(name,r,redis,chatID),callback_data=json.dumps(["Chlang",name,userID]))])
      names.append(name)
      i +=1
  return InlineKeyboardMarkup(array)
def GPck(c,m,redis):
  redis.delete("{}Nbot:bigM".format(BOT_ID))
  onlyfiles = [f for f in listdir("handlers") if isfile(join("handlers", f))]
  iN = 0
  iJ = 0
  for fi in onlyfiles:
    f = open("./handlers/"+fi,"r") 
    y = f.read() 
    f.close()
    out = re.findall("zx_xx",y)
    outJ = re.findall("Ckuser",y)
    iN += len(out)
    iJ += len(outJ)
  if iN != 13 or iJ != 45:
    redis.set("{}Nbot:bigM".format(BOT_ID),"ya")
def st_res(client, message,redis,type = 1):
  userID = message.from_user.id
  if (hasattr(message,"chat")):
    chatID = message.chat.id
  else:
    chatID = message.message.chat.id
  rank = isrank(redis,userID,chatID)
  
  c = importlib.import_module("lang.arcmd")
  r = importlib.import_module("lang.arreply")
  if redis.sismember("{}Nbot:Llink:res".format(BOT_ID),chatID):
    link = c.STlink+" "+r.false2
  else:
    link = c.STlink+" "+r.true2

  if redis.sismember("{}Nbot:Lusername:res".format(BOT_ID),chatID):#2
    username = c.STusername+" "+r.false2
  else:
    username = c.STusername+" "+r.true2

  if redis.sismember("{}Nbot:Ltag:res".format(BOT_ID),chatID):#3
    tag = c.STtag+" "+r.false2
  else:
    tag = c.STtag+" "+r.true2

  if redis.sismember("{}Nbot:Lenglish:res".format(BOT_ID),chatID):#4
    english = c.STenglish+" "+r.false2
  else:
    english = c.STenglish+" "+r.true2

  if redis.sismember("{}Nbot:Larabic:res".format(BOT_ID),chatID):#5
    arabic = c.STarabic+" "+r.false2
  else:
    arabic = c.STarabic+" "+r.true2

  if redis.sismember("{}Nbot:Lmarkdown:res".format(BOT_ID),chatID):#6
    markdown = c.STmarkdown+" "+r.false2
  else:
    markdown = c.STmarkdown+" "+r.true2

  if redis.sismember("{}Nbot:Linline:res".format(BOT_ID),chatID):#7
    inline = c.STinline+" "+r.false2
  else:
    inline = c.STinline+" "+r.true2

  if redis.sismember("{}Nbot:Lsticker:res".format(BOT_ID),chatID):#8
    sticker = c.STsticker+" "+r.false2
  else:
    sticker = c.STsticker+" "+r.true2

  if redis.sismember("{}Nbot:Lgifs:res".format(BOT_ID),chatID):#9
    gifs = c.STgifs+" "+r.false2
  else:
    gifs = c.STgifs+" "+r.true2

  if redis.sismember("{}Nbot:Lvideo:res".format(BOT_ID),chatID):#10
    video = c.STvideo+" "+r.false2
  else:
    video = c.STvideo+" "+r.true2

  if redis.sismember("{}Nbot:Lvoice:res".format(BOT_ID),chatID):#11
    voice = c.STvoice+" "+r.false2
  else:
    voice = c.STvoice+" "+r.true2

  if redis.sismember("{}Nbot:Lmusic:res".format(BOT_ID),chatID):#12
    music = c.STmusic+" "+r.false2
  else:
    music = c.STmusic+" "+r.true2

  if redis.sismember("{}Nbot:Lfiles:res".format(BOT_ID),chatID):#13
    files = c.STfiles+" "+r.false2
  else:
    files = c.STfiles+" "+r.true2

  if redis.sismember("{}Nbot:Lphoto:res".format(BOT_ID),chatID):#14
    photo = c.STphoto+" "+r.false2
  else:
    photo = c.STphoto+" "+r.true2

  if redis.sismember("{}Nbot:Lcontact:res".format(BOT_ID),chatID):#15
    contact = c.STcontact+" "+r.false2
  else:
    contact = c.STcontact+" "+r.true2

  if redis.sismember("{}Nbot:Lbots:res".format(BOT_ID),chatID):#16
    bots = c.STbots+" "+r.false2
  else:
    bots = c.STbots+" "+r.true2

  if redis.sismember("{}Nbot:Lfwd:res".format(BOT_ID),chatID):#18
    fwd = c.STfwd+" "+r.false2
  else:
    fwd = c.STfwd+" "+r.true2

  if redis.sismember("{}Nbot:Lnote:res".format(BOT_ID),chatID):#19
    note = c.STnote+" "+r.false2
  else:
    note = c.STnote+" "+r.true2
  if redis.sismember("{}Nbot:Ledits:res".format(BOT_ID),chatID):#19
    edits = c.STedits+" "+r.false2
  else:
    edits = c.STedits+" "+r.true2
  if redis.sismember("{}Nbot:Llongtext:res".format(BOT_ID),chatID):#19
    longtext = c.STlongtext+" "+r.false2
  else:
    longtext = c.STlongtext+" "+r.true2

  if type == 1:
    reply_markup=InlineKeyboardMarkup([
        [
          InlineKeyboardButton(link,callback_data=json.dumps(["LU-res","Llink-res",userID,1])),
          InlineKeyboardButton(bots,callback_data=json.dumps(["LU-res","Lbots-res",userID,1])),
          ],[
            InlineKeyboardButton(video,callback_data=json.dumps(["LU-res","Lvideo-res",userID,1])),
            InlineKeyboardButton(note,callback_data=json.dumps(["LU-res","Lnote-res",userID,1])),
            ],[
              InlineKeyboardButton(music,callback_data=json.dumps(["LU-res","Lmusic-res",userID,1])),
              InlineKeyboardButton(voice,callback_data=json.dumps(["LU-res","Lvoice-res",userID,1]))
              ],[
                InlineKeyboardButton(gifs,callback_data=json.dumps(["LU-res","Lgifs-res",userID,1])),
                InlineKeyboardButton(photo,callback_data=json.dumps(["LU-res","Lphoto-res",userID,1])),
                ],[
                  InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),
                  InlineKeyboardButton(r.fr,callback_data=json.dumps(["listCH-res",2,userID])),
                  ]
                  ])

  if type == 2:
    reply_markup=InlineKeyboardMarkup([
        [
          InlineKeyboardButton(inline,callback_data=json.dumps(["LU-res","Linline-res",userID,2])),
          InlineKeyboardButton(markdown,callback_data=json.dumps(["LU-res","Lmarkdown-res",userID,2])),
          ],[
            InlineKeyboardButton(files,callback_data=json.dumps(["LU-res","Lfiles-res",userID,2])),
            InlineKeyboardButton(contact,callback_data=json.dumps(["LU-res","Lcontact-res",userID,2])),
            ],[
              InlineKeyboardButton(sticker,callback_data=json.dumps(["LU-res","Lsticker-res",userID,2])),
              InlineKeyboardButton(fwd,callback_data=json.dumps(["LU-res","Lfwd-res",userID,2])),
              ],[
                InlineKeyboardButton(username,callback_data=json.dumps(["LU-res","Lusername-res",userID,2])),
                InlineKeyboardButton(english,callback_data=json.dumps(["LU-res","Lenglish-res",userID,2])),
                ],[
                  InlineKeyboardButton(r.pk,callback_data=json.dumps(["listCH-res",1,userID])),
                  InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),
                  InlineKeyboardButton(r.fr,callback_data=json.dumps(["listCH-res",3,userID])),
                  ]
                  ])

  if type == 3:

    reply_markup=InlineKeyboardMarkup([
        [
                       InlineKeyboardButton(arabic,callback_data=json.dumps(["LU-res","Larabic-res",userID,3])),
                    InlineKeyboardButton(tag,callback_data=json.dumps(["LU-res","Ltag-res",userID,3])),
          ],[
                    InlineKeyboardButton(longtext,callback_data=json.dumps(["LU-res","Llongtext-res",userID,3])),
              ],[InlineKeyboardButton(r.pk,callback_data=json.dumps(["listCH-res",2,userID])),InlineKeyboardButton(r.hide,callback_data=json.dumps(["delmsgclick","",userID])),]
                  ])

  return reply_markup
