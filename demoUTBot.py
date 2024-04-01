import telebot
import time
import pandas as pd
from telebot import types

# - login
def loadCSV():
    df = pd.read_csv('login.csv', dtype=str)
    keys = list(df['NAME'].dropna())
    values = list(df['ID'].dropna())
    map_values = dict(zip(keys, values))
    return map_values

bot = telebot.TeleBot('7068784385:AAG1QR74-WqHVvg8JuN_MLBzkRfvnXlervo')
users_map = loadCSV()

def extract_name(text):
    return text.split()[1] if len(text.split()) > 1 else None

def save_id(name, id):
    users_map[name] = id
    with open('login.csv','w') as fd:
        fd.write("NAME,ID")
        for k in users_map.keys():
            fd.write("\n"+k+","+str(users_map[k]))

def check_and_save_user(name, id):
    if users_map[name] == "0":
        save_id(name, id)
    else:
        if str(id) != users_map[name]:
            return False
    return True

@bot.message_handler(commands=['start'])
def send_welcome(message):
    name = extract_name(message.text)
    if name: 
        if name in users_map.keys():
            valid = check_and_save_user(name, message.chat.id)
            if valid:
                reply = "Hello {0}".format(name)
            else:
                reply = "You can't use the bot or you need to reset login (contact Administration)"
        else:
            reply = "You can't use the bot"
    else:
        reply = "Please insert your name after /start (/start <name>)"
    bot.reply_to(message, reply)
# --

# - commands
@bot.message_handler(commands=['hi'])
def send_welcome(message):
    if str(message.chat.id) in users_map.values():
        reply = "Hi"
    else:
        reply = "You can't use the bot or you need to login (/start <name>)"
    bot.reply_to(message, reply)
# --
    
# - doc
@bot.message_handler(commands=['doc'])
def send_welcome(message):
    if str(message.chat.id) in users_map.values():
        markup = types.ReplyKeyboardMarkup(row_width=1)
        itembtn1 = types.KeyboardButton('/ADEL')
        itembtn2 = types.KeyboardButton('/X56')
        markup.add(itembtn1, itembtn2)
        bot.send_message(message.chat.id, "What doc you need:", reply_markup=markup)
    else:
        reply = "You can't use the bot or you need to login (/start <name>)"
        bot.reply_to(message, reply)

@bot.message_handler(commands=['ADEL'])
def send_welcome(message):
    if str(message.chat.id) in users_map.values():
        doc = open('documentation/ADEL.pdf', 'rb')
        bot.send_document(message.chat.id, doc)
    else:
        reply = "You can't use the bot or you need to login (/start <name>)"
        bot.reply_to(message, reply)

@bot.message_handler(commands=['X56'])
def send_welcome(message):
    if str(message.chat.id) in users_map.values():
        doc = open('documentation/X56.pdf', 'rb')
        bot.send_document(message.chat.id, doc)
    else:
        reply = "You can't use the bot or you need to login (/start <name>)"
        bot.reply_to(message, reply)
# --

bot.polling()

while True:
    time.sleep(0)