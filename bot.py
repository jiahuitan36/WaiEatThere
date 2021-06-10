import logging
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import telebot
from flask import Flask, request
import os
import mysql.connector
from flask_mysqldb import MySQL
import MySQLdb.cursors

TOKEN = '1574285111:AAEKWu2V4a2nVgbpqyh9v9IfIpKcvBSIsqk'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

connection = mysql.connector.connect(host='us-cdbr-east-04.cleardb.com',
                                     database='heroku_ad23a96e20d8188',
                                     user='b76c66fd1150f8',
                                     password='4b16094b')


cursor = connection.cursor()

order_id = 1


logging.basicConfig(
    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    chat_id = str(message.chat.id) + "!@#"
    keyboard = [
        [types.InlineKeyboardButton("Al Amaan", callback_data=('ameens'))],
        [types.InlineKeyboardButton("McDonald's", callback_data='macs')]
    ]

    # keyboard = [
    #     [types.InlineKeyboardButton("Al Amaan", callback_data=(chat_id + 'ameens'))],
    #     [types.InlineKeyboardButton("McDonald's", callback_data='macs')]
    # ]

    markup = types.InlineKeyboardMarkup(keyboard)
    bot.send_message(message.chat.id, "Where would you like to order from?", reply_markup=markup)

@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, 'Time of upload: 2212')

@bot.message_handler(commands=['sqltest'])
def sqltest(message):
    cursor = connection.cursor()
    

    cursor.execute('SELECT * FROM menu')
    orders = cursor.fetchall()
    result = ""
    for item in orders:
        result += '\n' + item[2]

    bot.send_message(message.chat.id, result)

bot.message_handler(commands=['messagetest'])
def messagetest(message):
    bot.send_message(message.from_user.id, "hello")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    result = "FIRST LINE"
    cursor = connection.cursor()
    print(result)
    print(call.data)
    data = call.data.split("!@#")
    print(data[0])
    print(data[0] in ("Indian Kitchen", "Thai Kitchen"))

    global order_id
    
    #if 'ameens' in data[1]:
    if 'ameens' in call.data:
        cursor.execute('SELECT DISTINCT cuisine FROM menu')
        orders = cursor.fetchall()
        keyboard = []

        for item in orders:
             result += '\n' + item[0]
             keyboard.append([types.InlineKeyboardButton(item[0], callback_data=item[0])])

        markup = types.InlineKeyboardMarkup(keyboard)
        if call.data == 'ameens back':
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
        else:
            bot.send_message(call.from_user.id, "What would you like to order?", reply_markup = markup)
    
    #if data[0] == "Indian Kitchen":
    #if data[0] in ("Indian Kitchen", "Thai Kitchen", "Western Kitchen", "Drinks", "cuisine back"):
    if call.data in ("Indian Kitchen", "Thai Kitchen", "Western Kitchen", "Drinks", "cuisine back"):
        cuisine = call.data
        print("Cleared")
        #cuisine = data[0]
        sqlcommand = 'SELECT DISTINCT category FROM menu WHERE cuisine = "' + cuisine + '"'

        cursor.execute(sqlcommand)
        orders = cursor.fetchall()
        keyboard = []
        
        for item in orders:
             result += '\n' + item[0]
             keyboard.append([types.InlineKeyboardButton(item[0], callback_data=item[0])])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data="ameens back")])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    if call.data in ("Breads", "Rice", "Fried Rice", "Omelette", "Finger Food", "Pasta", "Spin", "Favourites"):
        category = call.data
        sqlcommand = 'SELECT DISTINCT item FROM menu WHERE category = "' + category + '"'

        cursor.execute(sqlcommand)
        orders = cursor.fetchall()
        keyboard = []
        
        for item in orders:
            #result += '\n' + item[0]
            keyboard.append([types.InlineKeyboardButton(item[0], callback_data=item[0])])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data="ameens back")])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    if call.data in ("Plain Naan", "Butter Naan", "Salted Fish", "Tomato & Chicken", "Crab Stick", "Prawns", "French Fries"): #or call.data == "Butter Naan":
        cursor.execute('INSERT INTO orders_testing VALUES (%s, %s, %s, %s)', (order_id, call.from_user.id, call.from_user.username, call.data))
        connection.commit()
        order_id += 1
        bot.send_message(call.from_user.id, "Order saved")


    if call.data == 'back':
        #cursor = connection.cursor()
        keyboard = [
            [types.InlineKeyboardButton("Insert Order", callback_data='ameens')],
            [types.InlineKeyboardButton("Macs Orders", callback_data='macs')]
        ]
    
    if call.data == 'macs':
        #cursor = connection.cursor()
        cursor.execute('SELECT * FROM menu')
        orders = cursor.fetchall()
        for item in orders:
            result += '\n' + item[2]
        keyboard = [
            [types.InlineKeyboardButton("Insert Order", callback_data='ameens')],
            [types.InlineKeyboardButton("Back", callback_data='back')]
        ]

    
    #markup = types.InlineKeyboardMarkup(keyboard)
    #bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
    #cursor.close()
    #connection.close()

def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('test', test))

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url='https://orbitaldatabasetest.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    main()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))