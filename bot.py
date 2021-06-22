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
    chat_id = str(message.chat.id)
    ameens = "ameens/" + chat_id
    #keyboard = [
    #    [types.InlineKeyboardButton("Al Amaan", callback_data=ameens)],
    #    [types.InlineKeyboardButton("McDonald's", callback_data='macs')],
    #    [types.InlineKeyboardButton("Remove Order", callback_data='remove order')]
    #]

    keyboard = [[types.InlineKeyboardButton("Al Amaan", callback_data=ameens)]]

    # keyboard = [
    #     [types.InlineKeyboardButton("Al Amaan", callback_data=(chat_id + 'ameens'))],
    #     [types.InlineKeyboardButton("McDonald's", callback_data='macs')]
    # ]

    markup = types.InlineKeyboardMarkup(keyboard)

    # cursor.execute('select exists(select * from orders where group_id = (%s))', (chat_id,))
    # bot_started = cursor.fetchone()
    # if bot_started[0] == 1:
    #     bot.send_message(message.chat.id, "Bot already started")
    # else:
    bot.send_message(message.chat.id, "Where would you like to order from?", reply_markup=markup)

@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, 'Time of upload: 2039')

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

    connection = mysql.connector.connect(host='us-cdbr-east-04.cleardb.com',
                                     database='heroku_ad23a96e20d8188',
                                     user='b76c66fd1150f8',
                                     password='4b16094b')


    cursor = connection.cursor()

    result = "FIRST LINE"
    cursor = connection.cursor()
    
    data = call.data.split("/")
    print(data)

    global order_id

    if 'ameens' in data:
        chat_id = data[1]
        button_data = 'cuisine/nil/' + chat_id
        remove_data = 'remove order/' + chat_id
        close_data = 'close order/' + chat_id

        keyboard = [
        [types.InlineKeyboardButton("Insert Order", callback_data=button_data)],
        [types.InlineKeyboardButton("Remove Order", callback_data=remove_data)],
        [types.InlineKeyboardButton("Close All Orders", callback_data=close_data)]
    ]
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "Order Options", reply_markup=markup)

    if 'cuisine' in data:
        cursor.execute('select exists(select * from payment where user_id = (%s))', (call.from_user.id,))
        check = cursor.fetchone()
        print(data)
       
        if check[0] == 1:
            bot.send_message(call.from_user.id, "You have an outstanding payment")
        else:
            cursor.execute('SELECT DISTINCT cuisine FROM menu')
            orders = cursor.fetchall()
            keyboard = []

            level = "category"
            chat_id = data[2]

            for item in orders:
                result += '\n' + item[0]
                button_data = level + "/" + item[0] + "/" + chat_id
                keyboard.append([types.InlineKeyboardButton(item[0], callback_data=button_data)])

            markup = types.InlineKeyboardMarkup(keyboard)
            if "back" in call.data:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
            else:
                bot.send_message(call.from_user.id, "What would you like to order?", reply_markup = markup)
    
    if 'category' in data:
        cuisine = data[1]
        sqlcommand = 'SELECT DISTINCT category FROM menu WHERE cuisine = "' + cuisine + '"'

        cursor.execute(sqlcommand)
        orders = cursor.fetchall()
        keyboard = []

        level = 'item'
        back_level = 'cuisine'
        chat_id = data[2]
        
        for item in orders:
            result += '\n' + item[0]
            button_data = level + "/" + item[0] + "/" + chat_id + "/" + data[1]
            keyboard.append([types.InlineKeyboardButton(item[0], callback_data=button_data)])

        back_data = back_level + "/" + "Back" + "/" + chat_id + "/" + "back"

        keyboard.append([types.InlineKeyboardButton("Back", callback_data=back_data)])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    if 'item' in data:
        category = data[1]
        sqlcommand = 'SELECT DISTINCT item FROM menu WHERE category = "' + category + '"'
        print(data)

        cursor.execute(sqlcommand)
        orders = cursor.fetchall()
        keyboard = []

        level = 'order'
        chat_id = data[2]

        back_level = "category"
        back_menu = data[3]
        
        for item in orders:
            button_data = button_data = level + "/" + item[0] + "/" + chat_id
            keyboard.append([types.InlineKeyboardButton(item[0], callback_data=button_data)])
        
        back_data = back_level + "/" + back_menu + "/" + chat_id

        keyboard.append([types.InlineKeyboardButton("Back", callback_data=back_data)])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    # Selecting Actual Order item to be added
    if 'order' in data:
        group_id = data[2]
        item_name = data[1]
        cursor.execute('SELECT item_id FROM menu WHERE item=%s', (item_name,))
        item_code = cursor.fetchall()[0][0]

        cursor.execute('INSERT INTO orders_test VALUES (%s, %s, %s, %s)', (group_id, call.from_user.id, call.from_user.username, item_name))
        cursor.execute('INSERT IGNORE INTO `user` VALUES(%s, %s)', (call.from_user.id, call.from_user.username))
        cursor.execute('INSERT INTO orders(group_id, user_id, item_id) VALUES (%s, %s, %s)', (group_id, call.from_user.id, item_code,))
        connection.commit()

        order_id += 1
        bot.send_message(call.from_user.id, "Order saved")
    
    if call.data == 'back':
        keyboard = [
            [types.InlineKeyboardButton("Insert Order", callback_data='ameens')],
            [types.InlineKeyboardButton("Macs Orders", callback_data='macs')]
        ]
    
    if "remove order" in call.data:
        print(data)
        id = str(call.from_user.id)
        group_id = data[1]
        result = "Select Order to Remove"

        if 'delete' in call.data:
            item = data[2]   
            cursor.execute('DELETE FROM orders WHERE user_id=%s AND item_id=%s', (id, item))
            connection.commit()


        command = 'SELECT item_id FROM orders WHERE user_id = ' + id
        cursor.execute(command)
        orders = cursor.fetchall()
        keyboard = []
        
        for order in orders:
            datastring = 'remove order/' + group_id + '/' + order[0] + '/' + 'delete'
            keyboard.append([types.InlineKeyboardButton(order[0], callback_data=datastring)])
            result += ('\n' + order[0])
        markup = types.InlineKeyboardMarkup(keyboard)

        if "delete" in call.data:
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
        else:
            bot.send_message(call.from_user.id, result, reply_markup = markup)
    
    if data[0] == "close order":
        cursor.execute('SELECT DISTINCT user_id FROM orders')
        users = cursor.fetchall()
        for person in users:
            cursor.execute('select SUM(price), username from menu inner join orders on orders.item_id = menu.item_id inner join `user` on user.user_id = orders.user_id where orders.user_id = (%s)', (person[0],))
            amount = cursor.fetchone()
            result += "\n" + amount[1] + " needs to pay $ " + str(amount[0])
            cursor.execute('INSERT INTO payment(user_id, payment_amount) values (%s, %s)', (person[0], str(amount[0]),))
            connection.commit()
        
        cursor.execute('delete from orders where group_id = (%s)', (data[1],))
        connection.commit()

        keyboard = [[types.InlineKeyboardButton("Pay Money", callback_data='pay money')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
    
    if call.data == "pay money":
        cursor.execute('delete from payment where user_id = (%s)', (call.from_user.id,))
        connection.commit()
        bot.send_message(call.message.chat.id, "Payment Cleared")

    
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