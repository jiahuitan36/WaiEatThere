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

@bot.message_handler(commands=['startorder'])
def startorder(message):
    connection = mysql.connector.connect(host='us-cdbr-east-04.cleardb.com',
                                     database='heroku_ad23a96e20d8188',
                                     user='b76c66fd1150f8',
                                     password='4b16094b')


    cursor = connection.cursor()
    chat_id = str(message.chat.id)
    ameens = "ameens/" + chat_id

    keyboard = [[types.InlineKeyboardButton("Al Amaan", callback_data=ameens)],
                [types.InlineKeyboardButton("New User", url="https://telegram.me/captsuppertest3bot")]
    ]

    markup = types.InlineKeyboardMarkup(keyboard)

    cursor.execute('select exists(select * from orders where group_id = (%s))', (chat_id,))
    bot_started = cursor.fetchone()
    print("Bot started is")
    print(bot_started)
    if bot_started[0] == 1:
        bot.send_message(message.chat.id, "Bot already started")
    else:

        #text = "Where would you like to order from?" + '\n' + "If you are a new user, please click on the New User button"
        line1 = "Welcome! This is a supper bot specially designed to make the order compilation and payment processes easier!"
        line2 = "If you are a new user, please click on the New User button and click on the Start button in the chat with the bot."
        line3 = "Else, click on Al Amaan's to start ordering."
        line4 = "Just a few things to note when using this bot:"
        line5 = "1. Do not start more than 1 bot in the group!"
        line6 = "2. If you have an outstanding payment, you will not be able to order anything"

        text = line1 + '\n' + '\n' + line2 + '\n' + line3 + '\n' + '\n' + line4 + '\n' + line5 + '\n' + line6

        bot.send_message(message.chat.id, text, reply_markup=markup)

@bot.message_handler(commands=['start'])
def start(message):
    connection = mysql.connector.connect(host='us-cdbr-east-04.cleardb.com',
                                     database='heroku_ad23a96e20d8188',
                                     user='b76c66fd1150f8',
                                     password='4b16094b')


    cursor = connection.cursor()
    cursor.execute('INSERT IGNORE INTO `user` VALUES(%s, %s)', (message.from_user.id, message.from_user.username))
    connection.commit()
    bot.send_message(message.chat.id, "Welcome to CAPT Supper Bot! You can now proceed to add your orders. Please proceed back to your group chat and press the Al Amaan's button.")

@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, 'Time of upload: 1516')

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
    #print(call.message.message_id)
    #print(call.from_user.id)
    #print(call.from_user)

    global order_id

    if 'ameens' in data:
        chat_id = data[1]
        button_data = 'cuisine/nil/' + chat_id + "/" + str(call.message.message_id)
        remove_data = 'remove order/' + chat_id + "/" + str(call.message.message_id)
        close_data = 'close order/' + chat_id

        keyboard = [
        [types.InlineKeyboardButton("Insert Order", callback_data=button_data)],
        [types.InlineKeyboardButton("Remove Order", callback_data=remove_data)],
        [types.InlineKeyboardButton("Close All Orders", callback_data=close_data)]
    ]
        markup = types.InlineKeyboardMarkup(keyboard)

        result = "Instructions:" + '\n' + "Click on Insert Order to add your orders, and the bot will message you privately for the menu." + '\n' + "Click on Remove Order if you would like to remove a previous order" + '\n' + "Click on Close All Orders when everyone in the group has finished adding their orders"
        result += '\n' + '\n' + "Order Summary"

        # command = 'SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id'
        # cursor.execute(command)
        cursor.execute('SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id WHERE orders.group_id = (%s)', (chat_id,))
        orders = cursor.fetchall()

        for order in orders:
            result += '\n' + order[0] + " - " + order[1]

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)


    # CUISINE DATA FORMAT
    # current menu level / previous menu / group chat id / group message id
    if 'cuisine' in data:
        # cursor.execute('INSERT IGNORE INTO `user` VALUES(%s, %s)', (call.from_user.id, call.from_user.username))
        # connection.commit()
        cursor.execute('select exists(select * from payment where user_id = (%s))', (call.from_user.id,))
        check = cursor.fetchone()
        
        if check[0] == 1:
            bot.send_message(call.from_user.id, "You have an outstanding payment")
        else:
            cursor.execute('SELECT DISTINCT cuisine FROM menu')
            orders = cursor.fetchall()
            keyboard = []

            level = "category"
            groupchat_id = data[2]
            groupmessage_id = data[3]

            for item in orders:
                result += '\n' + item[0]
                button_data = level + "/" + item[0] + "/" + groupchat_id + "/" + groupmessage_id
                keyboard.append([types.InlineKeyboardButton(item[0], callback_data=button_data)])

            markup = types.InlineKeyboardMarkup(keyboard)
            if "back" in call.data:
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
            else:
                bot.send_message(call.from_user.id, "What would you like to order?", reply_markup = markup)
    
    # CATEGORY DATA FORMAT
    # Category / Drinks and Desserts / Group chat id / group message id
    if 'category' in data:
        cuisine = data[1]
        sqlcommand = 'SELECT DISTINCT category FROM menu WHERE cuisine = "' + cuisine + '"'

        cursor.execute(sqlcommand)
        orders = cursor.fetchall()
        keyboard = []

        level = 'item'
        back_level = 'cuisine'
        groupchat_id = data[2]
        groupmessage_id = data[3]
        
        for item in orders:
            result += '\n' + item[0]
            #button_data = level + "/" + item[0] + "/" + groupchat_id + "/" + data[1]
            button_data = level + "/" + item[0] + "/" + groupchat_id + "/" + groupmessage_id + "/" + data[1]
            keyboard.append([types.InlineKeyboardButton(item[0], callback_data=button_data)])

        back_data = back_level + "/" + "Back" + "/" + groupchat_id + "/" + "back"

        keyboard.append([types.InlineKeyboardButton("Back", callback_data=back_data)])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    # Items / Milkshakes / Group chat id / message id / Previous menu
    if 'item' in data:
        category = data[1]
        sqlcommand = 'SELECT item, price FROM menu WHERE category = "' + category + '"'
        #print(data)

        cursor.execute(sqlcommand)
        orders = cursor.fetchall()
        keyboard = []

        level = 'order'
        groupchat_id = data[2]
        groupmessage_id = data[3]

        back_level = "category"
        back_menu = data[4]
        
        for item in orders:
            item_name = item[0]
            item_price = str(item[1])
            item_text = item[0] + " - $" + item_price

            button_data = button_data = level + "/" + item[0] + "/" + groupchat_id + "/" + groupmessage_id
            keyboard.append([types.InlineKeyboardButton(item_text, callback_data=button_data)])
        
        back_data = back_level + "/" + back_menu + "/" + groupchat_id + "/" + groupmessage_id
        print(back_data)

        keyboard.append([types.InlineKeyboardButton("Back", callback_data=back_data)])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    # Selecting Actual Order item to be added
    if 'order' in data:
        group_id = data[2]
        item_name = data[1]
        cursor.execute('SELECT item_id FROM menu WHERE item=%s', (item_name,))
        item_code = cursor.fetchall()[0][0]

        #cursor.execute('INSERT INTO orders_test VALUES (%s, %s, %s, %s)', (group_id, call.from_user.id, call.from_user.username, item_name))
        cursor.execute('INSERT INTO orders(group_id, user_id, item_id) VALUES (%s, %s, %s)', (group_id, call.from_user.id, item_code,))
        connection.commit()

        order_id += 1
        bot.send_message(call.from_user.id, "Order saved")

        # To edit main group message
        groupmessage_id = data[3]
        
        button_data = 'cuisine/nil/' + group_id + "/" + groupmessage_id
        remove_data = 'remove order/' + group_id + "/" + groupmessage_id
        close_data = 'close order/' + group_id

        keyboard = [
            [types.InlineKeyboardButton("Insert Order", callback_data=button_data)],
            [types.InlineKeyboardButton("Remove Order", callback_data=remove_data)],
            [types.InlineKeyboardButton("Close All Orders", callback_data=close_data)]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        
        result = "Instructions:" + '\n' + "Click on Insert Order to add your orders, and the bot will message you privately for the menu." + '\n' + "Click on Remove Order if you would like to remove a previous order" + '\n' + "Click on Close All Orders when everyone in the group has finished adding their orders"
        result += '\n' + '\n' + "Order Summary"

        #command = 'SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id'
        #cursor.execute(command)
        cursor.execute('SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id WHERE orders.group_id = (%s)', (group_id,))
        orders = cursor.fetchall()

        print(orders)

        for order in orders:
            result += '\n' + order[0] + " - " + order[1]

        bot.edit_message_text(chat_id = group_id, message_id = groupmessage_id, text = result, reply_markup=markup)
    
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
            item = data[3]   
            cursor.execute('DELETE FROM orders WHERE user_id=%s AND item_id=%s', (id, item))
            connection.commit()


        command = 'SELECT item_id FROM orders WHERE user_id = ' + id
        cursor.execute(command)
        orders = cursor.fetchall()
        keyboard = []
        
        for order in orders:
            datastring = 'remove order/' + group_id + '/' + data[2] + "/" + order[0] + '/' + 'delete'
            cursor.execute('SELECT item FROM menu WHERE item_id = (%s)', (order[0],))
            item_name = cursor.fetchall()

            #print(item_name)

            #keyboard.append([types.InlineKeyboardButton(order[0], callback_data=datastring)])
            keyboard.append([types.InlineKeyboardButton(item_name[0][0], callback_data=datastring)])

            result += ('\n' + item_name[0][0])
            #result += ('\n' + item_name)
        markup = types.InlineKeyboardMarkup(keyboard)

        if "delete" in call.data:
            bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
            
            button_data = 'cuisine/nil/' + group_id + "/" + str(data[2])
            remove_data = 'remove order/' + group_id + "/" + str(data[2])
            close_data = 'close order/' + group_id

            keyboard = [
                [types.InlineKeyboardButton("Insert Order", callback_data=button_data)],
                [types.InlineKeyboardButton("Remove Order", callback_data=remove_data)],
                [types.InlineKeyboardButton("Close All Orders", callback_data=close_data)]
            ]   
            markup = types.InlineKeyboardMarkup(keyboard)

            result = "Instructions:" + '\n' + "Click on Insert Order to add your orders, and the bot will message you privately for the menu." + '\n' + "Click on Remove Order if you would like to remove a previous order" + '\n' + "Click on Close All Orders when everyone in the group has finished adding their orders"
            result += '\n' + '\n' + "Order Summary"

            cursor.execute('SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id WHERE orders.group_id = (%s)', (group_id,))
            orders = cursor.fetchall()


            for order in orders:
                result += '\n' + order[0] + " - " + order[1]

            bot.edit_message_text(chat_id = group_id, message_id = data[2], text = result, reply_markup = markup)
        else:
            bot.send_message(call.from_user.id, result, reply_markup = markup)
    
    if data[0] == "close order":
        cursor.execute('SELECT DISTINCT user_id FROM orders WHERE group_id = (%s)', (call.message.chat.id,))
        users = cursor.fetchall()
        result = "Here is your bill!" + '\n'
        for person in users:
            cursor.execute('SELECT SUM(price), username FROM menu INNER JOIN orders ON orders.item_id = menu.item_id INNER JOIN `user` ON user.user_id = orders.user_id WHERE orders.user_id = (%s) AND orders.group_id=(%s)', (person[0], call.message.chat.id,))
            amount = cursor.fetchone()
            result += "\n" + amount[1] + " needs to pay $ " + str(amount[0])
            cursor.execute('INSERT INTO payment(group_id, user_id, payment_amount) values (%s, %s, %s)', (call.message.chat.id, person[0], str(amount[0]),))
            connection.commit()

        # cursor.execute('delete from orders where group_id = (%s)', (data[1],))
        # connection.commit()

        keyboard = [[types.InlineKeyboardButton("Pay Money", callback_data='pay money')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
    
    if call.data == "pay money":
        cursor.execute('delete from payment where user_id = (%s)', (call.from_user.id,))
        #cursor.execute('DELETE FROM payment where group_id = (%s)', (call.message.chat.id,))
        connection.commit()

        text = "Payment Cleared by " + call.from_user.username

        bot.send_message(call.message.chat.id, text)

        cursor.execute('SELECT DISTINCT item_id FROM orders WHERE user_id=(%s) AND group_id=(%s)', (call.from_user.id, call.message.chat.id))
        orders = cursor.fetchall()
        keyboard = []
        for item in orders:
            cursor.execute('SELECT item FROM menu WHERE item_id=(%s)', (item[0],))
            item_name = cursor.fetchone()[0]
            review_data = "reviews/" + item[0]
            keyboard.append([types.InlineKeyboardButton(item_name, callback_data=review_data)])
        markup = types.InlineKeyboardMarkup(keyboard)
        result = "Would you like to review these items?" + '\n' + "(Due to current limitations, you can only choose 1 item to review if you ordered multiple items)"
        bot.send_message(call.from_user.id, result, reply_markup=markup)

        cursor.execute('delete from orders where group_id = (%s)', (call.message.chat.id,))
        connection.commit()
    
    if "reviews" in call.data:
        if len(data) == 3:
            item_id = data[1]
            review_value = int(data[2])
            cursor.execute('INSERT INTO reviews(user_id, item_id, review) VALUES (%s, %s, %s)', (call.from_user.id, item_id, review_value,))
            

        keyboard = []
        i = 5
        while i > 0:
            review_data = "reviews/" + data[1] + "/" + str(i)
            keyboard.append([types.InlineKeyboardButton(str(i), callback_data=review_data)])
            i -= 1
        markup = types.InlineKeyboardMarkup(keyboard)
        result = "Please select a rating from 1-5, with 5 being the best" + '\n' + "(Please do not click on any numbers for now as it will not respond)"
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup = markup)

    
    #markup = types.InlineKeyboardMarkup(keyboard)
    #bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
    #cursor.close()
    #connection.close()

def main() -> None:
    updater = Updater(TOKEN)

    updater.dispatcher.add_handler(CommandHandler('start', startorder))
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