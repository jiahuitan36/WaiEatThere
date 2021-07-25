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

    cursor.execute('SELECT EXISTS(SELECT * FROM payment WHERE group_id =(%s))', (chat_id,))
    payment_exists = cursor.fetchone()

    print("Bot started is")
    print(bot_started)
    if (bot_started[0] == 1):
        bot.send_message(message.chat.id, "Bot already started")
    elif payment_exists[0] == 1:
        payment_message = "Please clear all outstanding payments first!" + '\n' + '\n'

        cursor.execute('SELECT user_id, payment_amount FROM payment WHERE group_id = (%s)', (message.chat.id,))
        payments = cursor.fetchall()
        for payment in payments:
            cursor.execute('SELECT username FROM user WHERE user_id=(%s)', (payment[0],))
            username = cursor.fetchone()[0]
            payment_message += username + " needs to pay $" + str(payment[1])
        
        keyboard = [[types.InlineKeyboardButton("Pay Money", callback_data='pay money')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.send_message(message.chat.id, payment_message, reply_markup = markup)
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

    result = "Welcome to CAPT Supper Bot! You can now proceed to add your orders. Please proceed back to your group chat and press the Al Amaan's button." + '\n' + '\n' + "Anytime you need help, send /help in the chat!"

    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, 'Time of upload: 1216')


@bot.message_handler(commands=['help'])
def help(message):
    text = "How may I help you?"
    keyboard = [
        [types.InlineKeyboardButton("General", callback_data="help/general")],
        [types.InlineKeyboardButton("Orders", callback_data="help/queries")],
        [types.InlineKeyboardButton("Payment", callback_data="help/payment")],
        [types.InlineKeyboardButton("Others", callback_data="help/others")]
        ]
    markup = types.InlineKeyboardMarkup(keyboard)


    bot.send_message(message.chat.id, text, reply_markup = markup)

@bot.message_handler(commands=['sqltest'])
def sqltest(message):
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM menu')
    orders = cursor.fetchall()
    result = ""
    for item in orders:
        result += '\n' + item[2]

    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['finishreview'])
def finishreview(message):

    connection = mysql.connector.connect(host='us-cdbr-east-04.cleardb.com',
                                     database='heroku_ad23a96e20d8188',
                                     user='b76c66fd1150f8',
                                     password='4b16094b')


    cursor = connection.cursor()

    user_id = message.from_user.id

    cursor.execute('UPDATE reviews SET review = (%s) WHERE user_id = (%s) AND review = (%s)', (-1, user_id, 0,))
    connection.commit()

    bot.send_message(message.from_user.id, user_id)

@bot.message_handler(func=lambda message: True)
def echo_message(message):
    if message.chat.type == 'private':
        user_id = message.from_user.id

        connection = mysql.connector.connect(host='us-cdbr-east-04.cleardb.com',
                                        database='heroku_ad23a96e20d8188',
                                        user='b76c66fd1150f8',
                                        password='4b16094b')


        cursor = connection.cursor()

        cursor.execute('UPDATE orders SET remarks = (%s) WHERE user_id = (%s) AND latest_order = (%s)', (message.text, user_id, 1,))
        connection.commit()
        #bot.reply_to(message, message.text)
        bot.reply_to(message, "Remark added")

        cursor.execute('SELECT group_id, message_id, remarks FROM orders WHERE user_id=(%s) AND latest_order=(%s)', (user_id, 1))
        data = cursor.fetchall()
        group_id = data[0][0]
        message_id = data[0][1]
        #remarks = data[0][2]

        button_data = 'cuisine/nil/' + group_id + "/" + str(message_id)
        remove_data = 'remove order/' + group_id + "/" + str(message_id)
        close_data = 'close order/' + group_id

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
        cursor.execute('SELECT username, item, price, remarks FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id WHERE orders.group_id = (%s)', (group_id,))
        orders = cursor.fetchall()

        for order in orders:
            result += '\n' + order[0] + " - " + order[1] + " ($" + str(order[2]) + ")"
            if order[3] != None:
                result += ' (' + order[3] + ')'

        bot.edit_message_text(chat_id = group_id, message_id = message_id, text = result, reply_markup=markup)


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
        button_data = 'cuisine/nil/' + chat_id + "/" + str(call.message.message_id)
        remove_data = 'remove order/' + chat_id + "/" + str(call.message.message_id)
        close_data = 'close order/' + chat_id

        keyboard = [
        [types.InlineKeyboardButton("Insert Order", callback_data=button_data)],
        [types.InlineKeyboardButton("Remove Order", callback_data=remove_data)],
        [types.InlineKeyboardButton("Close All Orders", callback_data=close_data)]
    ]
        markup = types.InlineKeyboardMarkup(keyboard)

        result = "*Instructions:*" + '\n' + "Click on *Insert Order* to add your orders, and the bot will message you privately for the menu." + '\n' + "Click on *Remove Order* if you would like to remove a previous order" + '\n' + "Click on *Close All Orders* when everyone in the group has finished adding their orders"
        result += '\n' + '\n' + "*Order Summary*"

        # command = 'SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id'
        # cursor.execute(command)
        cursor.execute('SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id WHERE orders.group_id = (%s)', (chat_id,))
        orders = cursor.fetchall()

        for order in orders:
            result += '\n' + order[0] + " - " + order[1]

        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup, parse_mode="Markdown")


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

            bestbutton_data = "item" + "/" + "best" + "/" + groupchat_id + "/" + groupmessage_id
            keyboard.append([types.InlineKeyboardButton("Best Sellers", callback_data=bestbutton_data)])

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
        
        # if "best" in data:
        #     cursor.execute("select menu.item, reviews.item_id, avg(review) as rev from reviews inner join menu on reviews.item_id = menu.item_id where review > 1 group by item_id order by rev DESC, menu.item asc limit 5")
        # else:    
        cursor.execute('SELECT DISTINCT category FROM menu WHERE cuisine=(%s)', (cuisine,))
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
            #if len(item[0]) < 20:
            keyboard.append([types.InlineKeyboardButton(item[0], callback_data=button_data)])

        back_data = back_level + "/" + "Back" + "/" + groupchat_id + "/" + groupmessage_id + "/" + "back"
        keyboard.append([types.InlineKeyboardButton("Back", callback_data=back_data)])

        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)

    
    # Items / Milkshakes / Group chat id / message id / Previous menu
    if 'item' in data:
        category = data[1]
        orders = []

        if "best" in data:
            cursor.execute("select menu.item, menu.price, reviews.item_id, avg(review) as rev from reviews inner join menu on reviews.item_id = menu.item_id where review > 1 group by item_id order by rev DESC, menu.item asc limit 5")
            items = cursor.fetchall()
            for item in items:
                orders.append([item[0], item[1]])
        else:
            sqlcommand = 'SELECT item, price FROM menu WHERE category = "' + category + '"'
            cursor.execute(sqlcommand)
            orders = cursor.fetchall()
        keyboard = []

        level = 'order'
        groupchat_id = data[2]
        groupmessage_id = data[3]

        

        if "best" not in data:
            back_level = "category"
            back_menu = data[4]
        else:
            back_level = "cuisine"
            back_menu = "back"
        
        for item in orders:
            item_name = item[0]
            item_price = str(item[1])
            item_text = item[0] + " - $" + item_price

            cursor.execute('SELECT item_id FROM menu WHERE item=(%s)', (item_name,))
            item_id = cursor.fetchall()[0][0]
            cursor.execute('SELECT AVG(review) FROM reviews WHERE item_id=(%s) AND review > 0', (item_id,))
            #item_rating = str(cursor.fetchall()[0][0])
            item_rating = cursor.fetchall()[0][0]

            if item_rating == None:
                item_rating = "No Rating"
            else:
                if (item_rating % 1) != 0:
                    item_rating = round(item_rating, 2)
                else:
                    item_rating = round(item_rating, 0)
                item_rating = str(item_rating) + "/5"


            button_data = button_data = level + "/" + item[0] + "/" + groupchat_id + "/" + groupmessage_id
            keyboard.append([types.InlineKeyboardButton(item_text + " (" + item_rating + ")", callback_data=button_data)])
        
        back_data = back_level + "/" + back_menu + "/" + groupchat_id + "/" + groupmessage_id


        keyboard.append([types.InlineKeyboardButton("Back", callback_data=back_data)])
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What would you like to order?", reply_markup=markup)
    
    # Selecting Actual Order item to be added
    if 'order' in data:
        group_id = data[2]
        groupmessage_id = data[3]
        item_name = data[1]
        cursor.execute('SELECT item_id FROM menu WHERE item=%s', (item_name,))
        item_code = cursor.fetchall()[0][0]

        #cursor.execute('INSERT INTO orders_test VALUES (%s, %s, %s, %s)', (group_id, call.from_user.id, call.from_user.username, item_name))
        cursor.execute('UPDATE orders SET latest_order=(%s) WHERE user_id=(%s) AND group_id=(%s)', (0, call.from_user.id, group_id,))
        cursor.execute('INSERT INTO orders(group_id, user_id, item_id, latest_order, message_id) VALUES (%s, %s, %s, %s, %s)', (group_id, call.from_user.id, item_code, 1, groupmessage_id,))
        connection.commit()

        order_id += 1
        order_message = "*Order Summary*" + '\n'        

        cursor.execute('SELECT item_id FROM orders WHERE user_id=(%s)', (call.from_user.id,))
        indiv_orders = cursor.fetchall()
        for order in indiv_orders:
            item_id = order[0]
            cursor.execute('SELECT item, price FROM menu WHERE item_id=(%s)', (item_id,))
            item_ordered = cursor.fetchone()
            print(item_ordered)
            item_name = item_ordered[0]
            item_price = item_ordered[1]
            order_message += '\n' + item_name + " ($" + str(item_price) + ")"

        order_message += '\n' + '\n' + "*You have just ordered* " + "*" + data[1] + "*" + '\n' + '\n'
        order_message += " (If you have any remarks (eg. no chili) please type them below before adding your next order)"

        bot.send_message(call.from_user.id, order_message, parse_mode="Markdown")

        # To edit main group message
        
        
        button_data = 'cuisine/nil/' + group_id + "/" + groupmessage_id
        remove_data = 'remove order/' + group_id + "/" + groupmessage_id
        close_data = 'close order/' + group_id

        keyboard = [
            [types.InlineKeyboardButton("Insert Order", callback_data=button_data)],
            [types.InlineKeyboardButton("Remove Order", callback_data=remove_data)],
            [types.InlineKeyboardButton("Close All Orders", callback_data=close_data)]
        ]
        markup = types.InlineKeyboardMarkup(keyboard)
        
        result = "*Instructions:*" + '\n' + "Click on *Insert Order* to add your orders, and the bot will message you privately for the menu." + '\n' + "Click on *Remove Order* if you would like to remove a previous order" + '\n' + "Click on *Close All Orders* when everyone in the group has finished adding their orders"
        result += '\n' + '\n' + "*Order Summary*"

        #command = 'SELECT username, item, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id'
        #cursor.execute(command)
        cursor.execute('SELECT username, item, remarks, price FROM orders INNER JOIN user ON user.user_id = orders.user_id INNER JOIN menu ON menu.item_id = orders.item_id WHERE orders.group_id = (%s)', (group_id,))
        orders = cursor.fetchall()

        for order in orders:
            print(order)
            result += '\n' + order[0] + " - " + order[1] + " ($" + str(order[3]) + ")"
            if order[2] != None:
                result += " (" + order[2] + ")"


        bot.edit_message_text(chat_id = group_id, message_id = groupmessage_id, text = result, reply_markup=markup, parse_mode="Markdown")
    
    if call.data == 'back':
        keyboard = [
            [types.InlineKeyboardButton("Insert Order", callback_data='ameens')],
            [types.InlineKeyboardButton("Macs Orders", callback_data='macs')]
        ]
    
    if "remove order" in call.data:
        id = str(call.from_user.id)
        group_id = data[1]
        result = "Select Order to Remove"

        if 'delete' in call.data:
            item = data[3]   
            cursor.execute('DELETE FROM orders WHERE user_id=(%s) AND item_id=(%s) LIMIT 1', (id, item))
            connection.commit()


        command = 'SELECT item_id FROM orders WHERE user_id = ' + id
        cursor.execute(command)
        orders = cursor.fetchall()
        keyboard = []
        
        for order in orders:
            datastring = 'remove order/' + group_id + '/' + data[2] + "/" + order[0] + '/' + 'delete'
            cursor.execute('SELECT item FROM menu WHERE item_id = (%s)', (order[0],))
            item_name = cursor.fetchall()

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
                result += '\n' + order[0] + " - " + order[1] + " ($" + str(order[2]) + ")"
                print(result) 

            bot.edit_message_text(chat_id = group_id, message_id = data[2], text = result, reply_markup = markup)

            order_message = "*Order Summary*" + '\n'        

            cursor.execute('SELECT item_id FROM orders WHERE user_id=(%s)', (call.from_user.id,))
            indiv_orders = cursor.fetchall()
            for order in indiv_orders:
                item_id = order[0]
                cursor.execute('SELECT item, price FROM menu WHERE item_id=(%s)', (item_id,))
                item_ordered = cursor.fetchone()
                print(item_ordered)
                item_name = item_ordered[0]
                item_price = item_ordered[1]
                order_message += '\n' + item_name + " ($" + str(item_price) + ")"
            
            cursor.execute('SELECT item FROM menu WHERE item_id=(%s)', (data[3],))
            item_name = cursor.fetchone()[0]

            order_message += '\n' + '\n' + "*You have just removed* " + "*" + item_name + "*"
            
            bot.send_message(call.from_user.id, order_message, parse_mode="Markdown")


        else:
            bot.send_message(call.from_user.id, result, reply_markup = markup)
    
    if data[0] == "close order":
        cursor.execute('SELECT DISTINCT user_id FROM orders WHERE group_id = (%s)', (call.message.chat.id,))
        users = cursor.fetchall()
        
        cursor.execute('SELECT SUM(price) FROM orders JOIN menu WHERE orders.item_id = menu.item_id')
        total_amount = cursor.fetchone()[0]
        print(total_amount)

        if total_amount < 50:
            print(total_amount)
            delivery_fee = round((3 / len(users)), 2)
            print(delivery_fee)
            result = "Here is your bill!" + '\n' + "(Delivery charge of $" + str(delivery_fee) + " is already included in your total bill)" + '\n'
            print(result)
        else:
            result = "Here is your bill!" + '\n'
        


        for person in users:
            cursor.execute('SELECT SUM(price), username FROM menu INNER JOIN orders ON orders.item_id = menu.item_id INNER JOIN `user` ON user.user_id = orders.user_id WHERE orders.user_id = (%s) AND orders.group_id=(%s)', (person[0], call.message.chat.id,))
            amount = cursor.fetchone()

            indiv_amount = round(amount[0], 2)

            if total_amount < 50:
                indiv_amount += 3 / len(users)

            result += "\n" + amount[1] + " needs to pay $ " + str(indiv_amount)
            cursor.execute('INSERT INTO payment(group_id, user_id, payment_amount) values (%s, %s, %s)', (call.message.chat.id, person[0], str(indiv_amount),))
            connection.commit()

            cursor.execute('SELECT item_id FROM orders WHERE user_id = (%s)', (person[0],))
            items = cursor.fetchall()
            for item in items:
                cursor.execute('INSERT INTO reviews(user_id, item_id, review) values (%s, %s, %s)', (person[0], item[0], 0,))
                connection.commit()
        
        cursor.execute('DELETE FROM orders WHERE group_id = (%s)', (call.message.chat.id,))
        connection.commit()

        keyboard = [[types.InlineKeyboardButton("Pay Money", callback_data='pay money')]]
        markup = types.InlineKeyboardMarkup(keyboard)
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup=markup)
    
    if call.data == "pay money":
        cursor.execute('delete from payment where user_id = (%s)', (call.from_user.id,))
        connection.commit()

        text = "Payment Cleared by " + call.from_user.username

        bot.send_message(call.message.chat.id, text)

        #cursor.execute('SELECT DISTINCT item_id FROM orders WHERE user_id=(%s) AND group_id=(%s)', (call.from_user.id, call.message.chat.id,))
        cursor.execute('SELECT DISTINCT item_id FROM reviews WHERE user_id=(%s) AND review=(%s)', (call.from_user.id, 0,))
        orders = cursor.fetchall()
        keyboard = []
        for item in orders:
            cursor.execute('SELECT item FROM menu WHERE item_id=(%s)', (item[0],))
            item_name = cursor.fetchone()[0]
            review_data = "reviews/" + item[0]
            keyboard.append([types.InlineKeyboardButton(item_name, callback_data=review_data)])
        keyboard.append([types.InlineKeyboardButton("Done Reviewing", callback_data="reviews/done")])
        markup = types.InlineKeyboardMarkup(keyboard)
        result = "Would you like to review these items?" + '\n' + "If you do not wish to review any items, please click the Done button."
        bot.send_message(call.from_user.id, result, reply_markup=markup)

        # cursor.execute('DELETE FROM orders WHERE group_id = (%s) AND user_id = (%s)', (call.message.chat.id, call.from_user.id))
        # connection.commit()
    
    if "reviews" in call.data:
        if len(data) == 3:
            item_id = data[1]
            review_value = int(data[2])
            cursor.execute('UPDATE reviews SET review = (%s) WHERE user_id = (%s) AND item_id = (%s) AND review = (%s)', (review_value, call.from_user.id, item_id, 0,))
            connection.commit()
            bot.send_message(call.message.chat.id, "Thanks for reviewing!")
            
        else:
            if "back" in call.data:
                cursor.execute('SELECT DISTINCT item_id FROM reviews WHERE user_id=(%s) AND review=(%s)', (call.from_user.id, 0,))
                orders = cursor.fetchall()
                keyboard = []
                for item in orders:
                    cursor.execute('SELECT item FROM menu WHERE item_id=(%s)', (item[0],))
                    item_name = cursor.fetchone()[0]
                    review_data = "reviews/" + item[0]
                    keyboard.append([types.InlineKeyboardButton(item_name, callback_data=review_data)])
                keyboard.append([types.InlineKeyboardButton("Done Reviewing", callback_data="reviews/done")])
                markup = types.InlineKeyboardMarkup(keyboard)
                result = "Would you like to review these items?"
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup = markup)
            elif "done" in call.data:
                cursor.execute('UPDATE reviews SET review = (%s) WHERE user_id = (%s) AND review = (%s)', (-1, call.from_user.id, 0,))
                connection.commit()

                bot.send_message(call.from_user.id, "You have finished reviewing.")
            else:
                keyboard = []
                i = 5
                while i > 0:
                    review_data = "reviews/" + data[1] + "/" + str(i)
                    keyboard.append([types.InlineKeyboardButton(str(i), callback_data=review_data)])
                    i -= 1
                keyboard.append([types.InlineKeyboardButton("Back", callback_data="reviews/back")])
                keyboard.append([types.InlineKeyboardButton("Done Reviewing", callback_data="reviews/done")])
                markup = types.InlineKeyboardMarkup(keyboard)
                result = "Please select a rating from 1-5, with 5 being the best." + '\n' + "If you would like to review another item, please click on the *Back* button." + '\n' + "If you are done reviewing, please click on the *Done Reviewing* button"
                bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = result, reply_markup = markup, parse_mode="Markdown")
    if "help" in data:
        if "general" in data:
            general = "*Q: How to start the bot?*" + "\n" + "A: Execute */startorder*." + "\n \n" + "*Q: I can't start the bot in a group*" + "\n" + \
                "A: There are two possible scenerios. Firstly, a bot is already started in the group. Hence, to stop the bot, simply click on *Close All Orders* for the existing bot. Secondly, someone in the group probably has an outstanding payment, either from the same group or from another group. To solve this, the person in question simply has to clear his/her payment and click on 'Pay Money'."
            bot.send_message(call.message.chat.id, parse_mode="Markdown", text = general)
        elif "queries" in data:
            print("hello")
            order = "*Q: How to insert orders?*" + '\n' + "A: Click on *Insert Order* to add your orders, and the bot will message you privately for the menu."
            order += '\n' + '\n' + "*Q: How to remove orders?*" + '\n' + "A: Click on *Remove Order* if you would like to remove a previous order."
            order += '\n' + '\n' + "*Q: How to close orders?*" + "\n" + "A: Click on *Close All Orders* when everyone in the group has finished adding their orders"
            order += '\n' + '\n' + "*Q: How do I add remarks for the items I ordered?*" + "\n" + "A: After you have inserted an order, the bot will send you a message asking you to add remarks for that order. However, in the case where you ordered item A but didn't add a remark and proceeded to order item B, it would not be possible for you to add a remark to item A anymore. In this situation, you can remove item A from your order list and order it again."
            order += '\n' + '\n' + "*Q: How can I view all the items that I ordered?*" + "\n" + "A: In your private chat with the bot, you will see an *Order Summary* message that will be populated as you insert your orders. There is also an *Order Summary* message in the group, where you can see your own orders and what other people ordered."    
            order += '\n' + '\n' + "*Q: How do I review a food item?*" + '\n' + "A: After you click on *Pay Money*, the bot will privately message you and ask for your reviews. You can choose to review as many items as you want. After you are done reviewing, simply click on *Done Reviewing*."
            bot.send_message(call.message.chat.id, parse_mode="Markdown", text = order)
        elif "payment" in data:
            payment = "*Q: How much is delivery?*" + "\n" + "A: Delivery fee is *$3* if total orders do not exceed $50. The delivery fee that each person has to pay will be calculated and included in the final bill." + "\n \n" + \
        "*Q: How do we settle the payment?*" + "\n" + \
        "A: If the bot is used in a group, the person who helped to pay first can send his number in the group and people can click on *Pay Money* after they have paid."
            bot.send_message(call.message.chat.id, parse_mode="Markdown", text = payment)
        else:
            others = "If you have any other questions, please feel free to pm the admins! (@jia_huiii or @jofoooooo)"
            bot.send_message(call.message.chat.id, parse_mode="Markdown", text = others)
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