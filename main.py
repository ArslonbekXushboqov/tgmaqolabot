import telebot
from telegraph import Telegraph
import sqlite3 as sql
import datetime as dt
from buttons import *
from config import *

x = dt.datetime.now()


sana=x.strftime("%x")

with sql.connect(dbfile) as con:
    cur=con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users(
        id INTEGER,
        name TEXT
    )""")

    con.commit()

def insert(userid, name):
    con= sql.connect(dbfile)
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id = ?",(userid,))

    if cur.fetchone() is None:

        cur.execute("INSERT INTO users(id,name)VALUES(?,?)",(userid,name))
        con.commit()


bot=telebot.TeleBot(token)

telegraph = Telegraph()

@bot.message_handler(commands=['start'])
def start(msg):
    u_name = msg.from_user.first_name
    user_id = msg.chat.id
    insert(user_id, u_name)
    bot.send_message(user_id, f"Assalomu alaykum <a href='tg://user?id={user_id}'>{u_name}</a>\n\nMen sizga telegra.ph da osongina maqola yaratishga yordam beraman!", parse_mode="html", reply_markup=CREATE_BUTTONS)

@bot.callback_query_handler(func= lambda call: True)
def callbacks(call):
    if call.data == "del":
        try:
            for i in range(2):
                bot.delete_message(call.message.chat.id, call.message.message_id-i)
        except:
            pass

    if call.data == "create":
    		user_id=call.message.chat.id
    		msg_id=call.message.message_id
    		
    		bot.edit_message_text("🚀 Boshlandi!", user_id, msg_id)

    		xabar=bot.send_message(user_id,"Sarlavha uchun nom kiriting:", reply_markup=markup)
    		bot.register_next_step_handler(xabar, sarlavha)

def sarlavha(msg):
    ftext=msg.text
    msg = bot.send_message(msg.chat.id, "Endi maqola uchun matn yuboring.\n*HTML* textlar qoʻllab quvvatlanadi.", reply_markup=markup, parse_mode="markdown")
    bot.register_next_step_handler(msg, maqola, ftext)

def maqola(msg, ftext):
	try:
		text=msg.text
		user_id=msg.chat.id
		telegraph.create_account(short_name='2021')
		response = telegraph.create_page(
		f'{ftext}',
		html_content=f'{text}'
		)
		bot.send_message(user_id, f"✅ Muvaffaqiyatli yaratildi!\n\n📌 Sarlavha: <b>{ftext}</b>\n\n📑 Maqola matni: <b>{text}</b>\n\n🔗 Maqola linki: https://telegra.ph/{(response['path'])}\n\n📅 Sana: <b>{sana}</b>", parse_mode="html", reply_markup=DEL_BUTTONS)
		bot.send_message(logs_channel, f"#maqola\n\n👨‍🔧 Yaratuvchi: <code>{user_id}</code>\n\n🔗 Maqola: https://telegra.ph/{response['path']}\n\n📅 Sana: <b>{sana}</b>", parse_mode="html")
	except Exception as ex:
		print(ex)
	
bot.polling(none_stop=True)