from __future__ import print_function
import os
from telegram.ext import *
from telegram import *
import logging
from nsepy import get_history
import numpy as np
import pandas as pd
import csv
import pandas.io.json as pd_json
from datetime import date, timedelta
from gspread_pandas import Spread, Client
from nsetools import Nse

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

print("Phase 1 complete")
token = "1089284422:AAFLulS1w1NVzFdh-2hsSVlFRtiIGh2ph7s"
bot = Bot(token=token)
updater = Updater(token=token, use_context=True, workers = 20)

@run_async
def start(update, context):
    chat_id = update.message.chat_id
    user = update.message.from_user
    print(user)
    myself = bot.get_me()
    print(myself)
    context.bot.send_message(chat_id=chat_id, text="Hello {} \nAnd welcome to @{} \n I am live and making sure your tasks are exceuted at proper intervals".format(user['first_name'],myself['username']))

@run_async
def stocksd(update,context):
    chat_id = update.message.chat_id
    a = context.bot.send_message(chat_id = chat_id, text="Okay starting to execute StockSD manually!!")
    msgid = a.message_id
    os.system("python stockSD.py")
    bot.send_document(chat_id = chat_id, document = open("historicalSD1.csv","rb"))
    context.bot.edit_message_text(chat_id = chat_id, message_id = msgid, text ="Successfully Executed")

@run_async
def hhh(update,context):
    chat_id = update.message.chat_id
    a = context.bot.send_message(chat_id = chat_id, text="Okay starting to execute hhh manually!!")
    msgid = a.message_id
    os.system("python hhh.py")
    context.bot.edit_message_text(chat_id = chat_id, message_id = msgid, text ="Successfully Executed")
@run_async
def uploadit(update,context):
    chat_id = update.message.chat_id
    context.bot.send_document(chat_id = chat_id, document = open("historicalSD1.csv","rb"))

@run_async
def ls(update,context):
    chat_id = update.message.chat_id
    os.system("ls -a")
    context.bot.send_message(chat_id,text="Done check shell!")

print("Phase 2 compleye")
dispatcher= updater.dispatcher
start_handler = CommandHandler('start', start)
caps_handler = CommandHandler('stocksd', stocksd)
help_handler = CommandHandler('hhh', hhh)
upload_handler = CommandHandler('upload', uploadit)
ls_handler = CommandHandler('ls',ls)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(caps_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(upload_handler)
dispatcher.add_handler(ls_handler)
updater.start_polling()