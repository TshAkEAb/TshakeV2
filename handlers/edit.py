
from utlis.rank import setrank ,isrank ,remrank ,setsudos ,remsudos ,setsudo
from handlers.delete import delete
from utlis.tg import Bot
from config import *

import threading, requests, time, random

def edit(client, message,redis):
    userID = message.from_user.id
    chatID = message.chat.id
    rank = isrank(redis,userID,chatID)
    group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
    redis.hincrby("{}Nbot:{}:edits".format(BOT_ID,chatID),userID)
    if not message.outgoing:
        if (rank is False or rank is 0) and group is True and redis.sismember("{}Nbot:Ledits".format(BOT_ID),chatID):
            Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
        if not (rank is "sudo" or rank is "asudo" or rank is "sudos"  or rank is "malk") and group is True and redis.sismember("{}Nbot:Ledits".format(BOT_ID),chatID) and not message.text:
            Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
        if not (rank is "sudo" or rank is "asudo" or rank is "sudos"  or rank is "malk") and group is True and not redis.sismember("{}Nbot:Ledits".format(BOT_ID),chatID):
            t = threading.Thread(target=delete,args=(client, message,redis))
            t.daemon = True
            t.start()
