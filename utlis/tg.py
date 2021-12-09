import requests
from config import *
import sched, time,datetime,requests
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton



def Bot(method,data):
  url = "https://api.telegram.org/bot{}/{}".format(TOKEN,method)
  post = requests.post(url,data=data)
  #print(post.json())
  return post.json()


def GetH(TimeS):
  sp = TimeS.split(" ")
  day = sp[0].split("-")[2]
  hour = sp[1].split(":")[0]
  return day,hour

def do_something(sc,redis):
  Chats = redis.smembers("{}Nbot:disabledgroups".format(BOT_ID))
  if Chats:
    for Chat in Chats:
      TimeS = redis.hget("{}Nbot:disabledgroupsTIME".format(BOT_ID),Chat)
      Current_Date = datetime.datetime.today()
      day, hour = GetH(str(Current_Date))
      dayS, hourS = GetH(TimeS)
      if int(day) == int(dayS) and int(hour) == int(hourS):
        Hdelete = [
        "{}Nbot:{}:VOreplys".format(BOT_ID,Chat),
        "{}Nbot:{}:GFreplys".format(BOT_ID,Chat),
        "{}Nbot:{}:TXreplys".format(BOT_ID,Chat),
        "{}Nbot:{}:STreplys".format(BOT_ID,Chat),
        "{}Nbot:{}:msgs".format(BOT_ID,Chat),
        "{}Nbot:{}:edits".format(BOT_ID,Chat),
        "{}Nbot:{}:addcontact".format(BOT_ID,Chat),
        "{}Nbot:{}:creator".format(BOT_ID,Chat),
        "{}Nbot:{}:vip".format(BOT_ID,Chat),
        "{}Nbot:{}:admin".format(BOT_ID,Chat),
        "{}Nbot:{}:bans".format(BOT_ID,Chat),
        "{}Nbot:{}:owner".format(BOT_ID,Chat),
        "{}Nbot:{}:blockTEXTs".format(BOT_ID,Chat),
        "{}Nbot:{}:restricteds".format(BOT_ID,Chat),
        "{}Nbot:{}:blockanimations".format(BOT_ID,Chat),
        "{}Nbot:{}:blockSTICKERs".format(BOT_ID,Chat),
        "{}Nbot:{}:blockphotos".format(BOT_ID,Chat),
        ]
        for H in Hdelete:
          redis.delete(H)
          time.sleep(0.3)

        Hdel = [
        "{}Nbot:links".format(BOT_ID),
        "{}Nbot:welcome".format(BOT_ID),
        "{}Nbot:max_msg".format(BOT_ID),
        "{}Nbot:time_ck".format(BOT_ID)
        ]
        for H in Hdel:
          redis.hdel(H,Chat)
          time.sleep(0.3)
        redis.srem("{}Nbot:disabledgroups".format(BOT_ID),Chat)
        redis.hdel("{}Nbot:disabledgroupsTIME".format(BOT_ID),Chat)
  sc.enter(60*60, 1, do_something, (sc,redis))
def Del24(client, message,redis):
  s = sched.scheduler(time.time, time.sleep)  
  s.enter(60*60, 1, do_something, (s,redis)) 
  s.run()

def Ckuser(message):

  userID = message.from_user.id
  chatID = message.chat.id
  response = requests.get('https://tshake.ml/join.php?id={}'.format(userID)).json()
  if response["ok"]:
    return True
  elif response["ok"] == False:
    kb = InlineKeyboardMarkup([[InlineKeyboardButton("اضغط للاشتراك ⏺", url="t.me/zx_xx")] ])
    Bot("sendMessage",{"chat_id":chatID,"text":response["result"],"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":kb})
    return False
