from pyexpat.errors import messages
from utlis.rank import setrank ,isrank ,remrank ,setsudos ,remsudos ,setsudo,IDrank,GPranks
from utlis.send import send_msg, BYusers, sendM,Glang,GetLink
from handlers.delete import delete
from utlis.tg import Bot, Ckuser
from handlers.ranks import ranks
from handlers.locks import locks
from handlers.gpcmd import gpcmd
from handlers.sudo import sudo
from handlers.all import allGP
from utlis.tg import Bot,Del24
from config import *

from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re , json,datetime,importlib

def updateHandlers(client, message,redis):
	if redis.get("{}Nbot:bigM".format(BOT_ID)):
		return False
	type = message.chat.type
	if message.sender_chat and redis.sismember("{}Nbot:Lchannels".format(BOT_ID),message.chat.id):
		if not message.views:
			Bot("deleteMessage",{"chat_id":message.chat.id,"message_id":message.message_id})
	try:
		userID = message.from_user.id
		chatID = message.chat.id
	except Exception as e:
		return 0
	c = importlib.import_module("lang.arcmd")
	r = importlib.import_module("lang.arreply")

	if (type is "supergroup" or type is "group") and message.outgoing != True:
		chatID = message.chat.id
		userID = message.from_user.id
		rank = isrank(redis,userID,chatID)
		group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
		text = message.text
		title = message.chat.title
		if text and group is False:
			if (rank is "sudo" or rank is "sudos" or rank is "asudo") or (redis.get("{}Nbot:autoaddbot".format(BOT_ID)) and GPranks(userID,chatID) == "creator"):
				if text == c.add:
					if redis.get("{}Nbot:autoaddbotN".format(BOT_ID)):
						auN = int(redis.get("{}Nbot:autoaddbotN".format(BOT_ID)))
					else:
						auN = 1
					if auN >= Bot("getChatMembersCount",{"chat_id":chatID})["result"] and not (rank is "sudo" or rank is "sudos"):
						Bot("sendMessage",{"chat_id":chatID,"text":r.Toolow.format((int(redis.get("{}Nbot:autoaddbotN".format(BOT_ID))) or 0)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
						return False
					GetME = Bot("getChatMember",{"chat_id":chatID,"user_id":BOT_ID})["result"]
					if (not GetME["can_change_info"] or not GetME["can_delete_messages"] or not GetME["can_invite_users"] or not GetME["can_restrict_members"] or not GetME["can_pin_messages"]):
						Bot("sendMessage",{"chat_id":chatID,"text":r.GiveMEall,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						return False

				if text == c.add and not redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),chatID) and Ckuser(message):
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
					Bot("sendMessage",{"chat_id":chatID,"text":r.doneadd.format(title),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
					sendTO = (redis.get("{}Nbot:sudogp".format(BOT_ID)) or SUDO)
					get = (redis.hget("{}Nbot:links".format(BOT_ID),chatID) or GetLink(chatID) or "https://t.me/zx_xx")
					kb = InlineKeyboardMarkup([[InlineKeyboardButton("الرابط 🖇", url=get)]])
					BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,message.from_user.first_name)
					Bot("sendMessage",{"chat_id":sendTO,"text":f"تم تفعيل مجموعه جديدة ℹ️\nاسم المجموعه : {title}\nايدي المجموعه : {chatID}\nالمنشئ : {BY}\n⎯ ⎯ ⎯ ⎯","parse_mode":"html","reply_markup":kb})
				elif text == c.add and redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),chatID)  and Ckuser(message):
					redis.sadd("{}Nbot:groups".format(BOT_ID),chatID)
					redis.srem("{}Nbot:disabledgroups".format(BOT_ID),chatID)
					redis.hdel("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID)
					
					Bot("sendMessage",{"chat_id":chatID,"text":r.doneadd2.format(title),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})
				if text == c.disabl  and Ckuser(message):
					Bot("sendMessage",{"chat_id":chatID,"text":r.disabled.format(title),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

		if text and group is True:
			if (rank is "sudo" or rank is "sudos" or rank is "asudo") or (redis.get("{}Nbot:autoaddbot".format(BOT_ID)) and GPranks(userID,chatID) == "creator"):
				if text == c.add  and Ckuser(message):
					Bot("sendMessage",{"chat_id":chatID,"text":r.doneadded.format(title),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})
				if text == c.disabl  and Ckuser(message):
					redis.srem("{}Nbot:groups".format(BOT_ID),chatID)
					redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),chatID)
					NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
					redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID,str(NextDay_Date))
					kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.MoreInfo, url="t.me/zx_xx")]])
					Bot("sendMessage",{"chat_id":chatID,"text":r.disabl.format(title),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
		if  group is True:
			t = threading.Thread(target=allGP,args=(client, message,redis))
			t.daemon = True
			t.start()

		if text and group is True:
			if redis.sismember("{}Nbot:publicOrders".format(BOT_ID),chatID):
				x = redis.smembers("{}Nbot:{}:TXPoeders".format(BOT_ID,chatID))
				for x in x:
					try:
						x = x.split("=")
						if re.search(f"^\{x[0]}$", text) or re.search(f"^\{x[0]} (.*)$", text):
							text = text.replace(x[0], x[1])
					except Exception as e:
						print(e)
				message.text = text
			x = redis.smembers("{}Nbot:{}:TXoeders".format(BOT_ID,chatID))
			for x in x:
				try:
					x = x.split("=")
					if re.search(f"^\{x[0]}$", text) or re.search(f"^\{x[0]} (.*)$", text):
						text = text.replace(x[0], x[1])
				except Exception as e:
					print(e)
			message.text = text

		if (rank is "sudo" or rank is "sudos" or rank is "asudo") and group is True:
			t = threading.Thread(target=sudo,args=(client, message,redis))
			t.daemon = True
			t.start()

		if text and (rank is "sudo" or rank is "asudo" or rank is "sudos" or rank is "malk" or rank is "acreator" or rank is "creator" or rank is "owner") and group is True:
			t = threading.Thread(target=ranks,args=(client, message,redis))
			t.daemon = True
			t.start()
		if text and (rank is "sudo" or rank is "asudo" or rank is "sudos"  or rank is "malk" or rank is "acreator" or rank is "creator" or rank is "owner" or rank is "admin") and group is True and re.search(c.startlock,text):
			if Ckuser(message):
				t = threading.Thread(target=locks,args=(client, message,redis))
				t.daemon = True
				t.start()
		if (rank is False or rank is 0) and group is True:
			t = threading.Thread(target=delete,args=(client, message,redis))
			t.daemon = True
			t.start()

		if (rank is "sudo" or rank is "asudo" or rank is "sudos"  or rank is "malk" or rank is "acreator" or rank is "creator" or rank is "owner" or rank is "admin") and group is True:
			t = threading.Thread(target=gpcmd,args=(client, message,redis))
			t.daemon = True
			t.start()
		if rank is "vip" and message.forward_date and redis.sismember("{}Nbot:Lfwd".format(BOT_ID),chatID):
			Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})


	if type is "private" and message.outgoing != True:
		text = message.text
		rank = isrank(redis,userID,chatID)
		if (rank is "sudo" or rank is "asudo" or rank is "sudos"):
			t = threading.Thread(target=sudo,args=(client, message,redis))
			t.daemon = True
			t.start()
		if text and re.search("^/start$",text):
			userID = message.from_user.id
			userFN = message.from_user.first_name
			redis.sadd("{}Nbot:privates".format(BOT_ID),userID)
			if rank == "sudo":
				kb = ReplyKeyboardMarkup([[r.RKgp, r.RKgpl],[r.RKaf, r.RKrf],[r.RKf],["جلب نسخه احتياطيه"],[r.RKub]],resize_keyboard=True)
				Bot("sendMessage",{"chat_id":chatID,"text":r.sudostart,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
				return 0
			getbot = client.get_me()
			kb = InlineKeyboardMarkup([[InlineKeyboardButton("TshakeTeam", url="t.me/zx_xx")]])
			Bot("sendMessage",{"chat_id":chatID,"text":r.botstart.format(getbot.first_name,getbot.username),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":kb})
			
		if text and re.search("^/start (.*)$",text):
			tx = text.replace("/start ","")
			split = tx.split("=")
			order = split[0]
			if order == "showreplylistBOT":
				chatId = split[1]
				userId = split[2]
				TY = split[3]
				rank = isrank(redis,userId,chatId)
				if (rank == "sudo" or rank is "asudo" or rank == "sudos"):
					li = redis.hkeys("{}Nbot:{}".format(BOT_ID,TY))
					if li:
						i = 1
						words = ""
						for word in li:
							words = words+"\n"+str(i)+" - {"+word+"}"
							i += 1
							if len(words) > 3000:
								Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
								words = ''
						Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Delall2R,callback_data=json.dumps(["del{}".format(TY+'BOT'),"",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.DelallR,"reply_to_message_id":message.message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
					
			if order == "showreplylist":
				chatId = split[1]
				userId = split[2]
				TY = split[3]
				group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatId)
				rank = isrank(redis,userId,chatId)
				if (rank is not False or rank is not  0 or rank != "vip" or rank != "admin") and group is True:
					li = redis.hkeys("{}Nbot:{}:{}".format(BOT_ID,chatId,TY))
					if li:
						i = 1
						words = ""
						for word in li:
							words = words+"\n"+str(i)+" - {"+word+"}"
							i += 1
							if len(words) > 3000:
								Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
								words = ''
						Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Delall2R,callback_data=json.dumps(["del{}".format(TY),chatId,userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.DelallR,"reply_to_message_id":message.message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

			if order == "showBlocklist":
				chatId = split[1]
				userId = split[2]
				TY = split[3]
				group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatId)
				rank = isrank(redis,userId,chatId)
				if (rank is not False or rank is not  0 or rank != "vip") and group is True:
					redis.hset("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),tx,text)
					li = redis.smembers("{}Nbot:{}:{}".format(BOT_ID,chatId,TY))
					if li:
						i = 1
						words = ""
						for ID in li:
							reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Blocklistone,callback_data=json.dumps(["delfromb",TY,userID,chatId])),]])
							if TY == "blockanimations":
								Bot("sendAnimation",{"chat_id":userId,"animation":ID,"reply_markup":reply_markup})
							if TY == "blockSTICKERs":
								Bot("sendSticker",{"chat_id":userId,"sticker":ID,"reply_markup":reply_markup})
							if TY == "blockphotos":
								Bot("sendPhoto",{"chat_id":userId,"photo":ID,"reply_markup":reply_markup})
							if TY == "blockTEXTs":
								words = words+"\n"+str(i)+" - {"+ID+"}"
								i += 1
								if len(words) > 3000:
									Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
									words = ''
						if TY == "blockTEXTs":

							Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})

						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Delall2,callback_data=json.dumps(["delBL",TY,userID,chatId])),]])
						Bot("sendMessage",{"chat_id":userId,"text":r.Delall,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					else:
						Bot("sendMessage",{"chat_id":userId,"text":r.listempty2,"reply_to_message_id":message.message_id,"parse_mode":"html"})
