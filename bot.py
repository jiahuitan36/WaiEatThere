import logging
from telebot import types
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
import telebot
from flask import Flask, request
import os

TOKEN = '1861297084:AAH5tvvF2julhMLQMB5Oo1rJu4RMrHF9cYI'
bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)
chat_dict = {}
results_list = []
ameens_categories = ["Thai Kitchen", "Indian Kitchen", "Western Kitchen", "Drinks"]
thai_categories = ["Noodles", "Steam Rice", "Fried Rice"]
indian_categories = ["Tandoori", "Breads", "Rice (Indian)", "Meats (Indian)", "Vegetables"]
western_categories = ["Finger Food", "Pasta", "Salad", "Roti John", "Burgers", "Meats (Western)"]
drinks_categories = ["Standard", "Spin", "Milk Shakes"]

#Thai Food
noodles_orders = ["Maggi Pattaya (Chicken)", "Maggi Pattaya (Beef)"]
steamrice_orders = ["Sweet and Sour", "Black Pepper"]
friedrice_orders = ["Chinese Style (Chicken)", "Thai Style (Chicken)"]
#Indian Food
tandoori_orders = ["Tandoori Chicken"]
bread_orders = ["Plain Naan", "Garlic Naan", "Butter Naan"]
indmeat_orders = ["Butter Chicken"]
indrice_orders = ["Chicken Briyani"]
veg_orders = ["Paneer Butter Masala"]
#Western Food
fingerfood_orders = ["Chicken Wing Set (2pcs)", "Cheese Fries"]
pasta_orders = ["Sausage Carbonara", "Mushroom and Chicken Pasta"]
salad_orders = ["Garden Salad"]
rotijohn_orders = ["Roti John", "Roti John Cheese"]
burger_orders = ["Fried Fish Burger"]
wesmeat_orders = ["Fish and Chips", "Mushroom Steak"]
#Drinks
standarddrinks_orders = ["Teh Bing", "Ice Milo", "Ice Teh Cino"]
spindrinks_orders = ["Green Apple"]
milkshakes_orders = ["Banana Milkshake", "Sweet Corn Milkshake"]


logging.basicConfig(
    format ='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)
logger = logging.getLogger(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.id not in chat_dict:
        chat_dict[message.chat.id] = []
    
    keyboard = [
        [types.InlineKeyboardButton("Ameen's", callback_data='ameens')],
       [types.InlineKeyboardButton("Macs", callback_data='macs')]
    ]

    markup = types.InlineKeyboardMarkup(keyboard)

    bot.send_message(message.chat.id, 'Where would you like to order from?:', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    curr_chat_id = call.message.chat.id
    curr_message_id = call.message.message_id
    
    print("CALL PRINTED BELOW")
    #print(call.data)
    #print(call.data == "Indian Kitchen")
    print(call.data == "Breads")
    print(chat_dict[curr_chat_id])

    result = ""
    keyboard = []


    if call.data == 'ameens' or call.data == 'back_ameens_main':
        for category in ameens_categories:
            keyboard.append([types.InlineKeyboardButton(category, callback_data=category)])
    
    elif call.data == 'macs':
        
        keyboard = [
            [types.InlineKeyboardButton("Filet O Fish", callback_data='Filet O Fish')],
            [types.InlineKeyboardButton("Big Mac", callback_data='Big Mac')]
        ]

    if call.data == "Indian Kitchen" or call.data == 'back_indian':
        for category in indian_categories:
            keyboard.append([types.InlineKeyboardButton(category, callback_data=category)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data="back_ameens_main")])

    #Indian - Tandoori
    if call.data == "Tandoori":
        for order in tandoori_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    if call.data in tandoori_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in tandoori_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    #Indian - Breads
    if call.data == "Breads":
        for order in bread_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    if call.data in bread_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in bread_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])
    
    #Indian - Rice
    if call.data == "Rice (Indian)":
        for order in indrice_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    if call.data in indrice_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in indrice_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])
    
    #Indian - Meats
    if call.data == "Meats (Indian)":
        for order in indmeat_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    if call.data in indmeat_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in indmeat_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    #Indian - Veggies
    if call.data == "Vegetables":
        for order in veg_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    if call.data in veg_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in veg_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_indian')])

    #THAI KITCHEN#
    if call.data == "Thai Kitchen" or call.data == 'back_thai':
        for category in thai_categories:
            keyboard.append([types.InlineKeyboardButton(category, callback_data=category)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data="back_ameens_main")])

    #Thai - Noodles
    if call.data == "Noodles":
        for order in noodles_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_thai')])

    if call.data in noodles_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in noodles_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_thai')])
    
    #Thai - SteamRice
    if call.data == "Steam Rice":
        for order in steamrice_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_thai')])

    if call.data in steamrice_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in steamrice_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_thai')])

    #Thai - Fried Rice
    if call.data == "Fried Rice":
        for order in friedrice_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_thai')])

    if call.data in friedrice_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in friedrice_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_thai')])

    #WESTERN KITCHEN#
    if call.data == "Western Kitchen" or call.data == 'back_western':
        for category in western_categories:
            keyboard.append([types.InlineKeyboardButton(category, callback_data=category)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data="back_ameens_main")])
    
    #Western - Finger Food
    if call.data == "Finger Food":
        for order in fingerfood_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])

    if call.data in fingerfood_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in fingerfood_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])
    
    #Western - Pasta
    if call.data == "Pasta":
        for order in pasta_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])

    if call.data in pasta_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in pasta_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])
    
    #Western - Salad
    if call.data == "Salad":
        for order in salad_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])

    if call.data in salad_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in salad_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])
    
    #Western - Roti John
    if call.data == "Roti John":
        for order in rotijohn_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])

    if call.data in rotijohn_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in rotijohn_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])
    
    #Western - Meats
    if call.data == "Meats (Western)":
        for order in wesmeat_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])

    if call.data in wesmeat_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in wesmeat_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])
    
    #Western - Burger
    if call.data == "Burgers":
        for order in burger_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])

    if call.data in burger_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in burger_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_western')])
    
    #WDrinks Menu#
    if call.data == "Drinks" or call.data == 'back_drinks':
        for category in drinks_categories:
            keyboard.append([types.InlineKeyboardButton(category, callback_data=category)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data="back_ameens_main")])
    
    #Drinks - Standard
    if call.data == "Standard":
        for order in standarddrinks_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_drinks')])

    if call.data in standarddrinks_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in standarddrinks_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_drinks')])
    
    #Drinks - Standard
    if call.data == "Spin":
        for order in spindrinks_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_drinks')])

    if call.data in spindrinks_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in spindrinks_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_drinks')])
    
    #Drinks - Standard
    if call.data == "Milk Shakes":
        for order in milkshakes_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_drinks')])

    if call.data in milkshakes_orders:
        chat_dict[curr_chat_id].append(call.from_user.username + " - " + call.data)
        for order in milkshakes_orders:
            keyboard.append([types.InlineKeyboardButton(order, callback_data=order)])
        keyboard.append([types.InlineKeyboardButton("Back", callback_data='back_drinks')])
    


        
    #if call.data in ('Filet O Fish', 'Big Mac'):
    #    chat_dict[curr_chat_id].append(call.data)
    #    keyboard = [
    #        [types.InlineKeyboardButton("Filet O Fish", callback_data='Filet O Fish')],
    #        [types.InlineKeyboardButton("Big Mac", callback_data='Big Mac')]
    #    ]

    for order in chat_dict[curr_chat_id]:
               #result += '\n' + call.from_user.username + " - " + order
               result += '\n' + order
    
    markup = types.InlineKeyboardMarkup(keyboard)

    if result == "":
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = "What do you want to order?", reply_markup = markup)
    else:
        bot.edit_message_text(chat_id = call.message.chat.id, message_id = call.message.message_id, text = f"Orders: {result}", reply_markup = markup)
        


@bot.message_handler(commands=['test'])
def test(message):
    bot.send_message(message.chat.id, "Rev 6.24, hello")



#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_message(message):
#    bot.reply_to(message, message.text)

def main() -> None:
    updater = Updater('1861297084:AAH5tvvF2julhMLQMB5Oo1rJu4RMrHF9cYI')

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
    bot.set_webhook(url='https://captsupperbot.herokuapp.com/' + TOKEN)
    return "!", 200


if __name__ == "__main__":
    main()
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))