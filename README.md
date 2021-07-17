# WaiEatThere - A Supper Telebot 
A telebot that makes the process of ordering supper smoother and easier for hostel residents.

Created with Python, MySQL and Telegram’s BotFather and pyTelegramBotAPI.

## Table of contents 
* [Demo](#demo)
* [Motivations](#motivations)
* [Features](#features)
* [Usage](#usage)
* [Notes](#notes)


## Demo
Link to live demo: https://www.youtube.com/watch?v=x8MGODSSd5g&ab_channel=JosiahFoo

## Motivations 
As students staying on campus, supper orders are a regular part of hostel life. Students will likely order delivery for supper at least once a week, and often ask each other to help takeaway food when they order lunch as well.

Many students have also experienced the difficulties in collating orders. We usually open an order in group chats, and people will individually add their orders to these messages. However, we often run into a few issues. Firstly, students do not always know what the menu items are, since we usually order from a restaurant that is not on common platforms like GrabFood. Secondly, some orders sometimes get missed out since everyone is rushing to add their orders to the message, and the chat is full of multiple messages with the same order. Lastly, there are sometimes issues with our current payment system and some people who help to order do not always get their full money back. 

	
## Features
* Order Compilation 
  * Allow users to compile a full list of orders
  * Allow separate chats to collect orders separately, without affecting other chats
  * Allow users to select location to order from
  * Allow users to select specific order items
  
* Bill Splitting 
  * Allow for the display of the total order cost
  * Allow for the display of individual order costs for each person
  * Allow users to remove their name from the payment list with a button press
  * Automatically sends reminders to users who have not paid after 24 hours

* Reviews
  * Allow for users to give reviews for items that they ordered 
  * Allow users to view the reviews for each item on the menu 
  * Creation of a ‘Best Sellers’ list in the menu, which consists of the top few best rated food
  
## Usage
To start the telebot, add @captsuppertest3bot to a group. 

Then, execute `\startorder` and toggle between the buttons


## Notes 
* Only one bot can be ran in each group at any one time
* Each person can only order if he/she does not have any outstanding payment incurred from previous orders

## Link to more detailed README
Link to README: https://docs.google.com/document/d/1SmJzhFRgrpuUAE4reUO4XfJHEJCBx2wB9E5jJSqifiY/edit
