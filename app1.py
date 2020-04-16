from __future__ import print_function
import schedule
import time
import os
import telegram
from telegram import *
from telegram.ext import *
from threading import *
import logging as py_log
from nsetools import Nse
import csv
import pandas as pd
import pandas.io.json as pd_json
from datetime import date, timedelta
from gspread_pandas import Spread, Client

py_log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=py_log.INFO)
logger = py_log.getLogger()
logger.setLevel(py_log.INFO)


token = "1089284422:AAFLulS1w1NVzFdh-2hsSVlFRtiIGh2ph7s"
bot = Bot(token=token)
chat = [-469052538,537825532]
for chat in chat:
    bot.send_message(chat_id = chat,text = "Bot started Successfully will exceute actions at specific periods and notify Thanks!!!!!")


def function1():
    os.system("python hhh.py")
    chat = [-469052538,537825532]
    for chat in chat:
        bot.send_message(chat_id = chat, text = "hhh executed")

schedule.every().day.at("03:50").do(function1)

while True:
    schedule.run_pending()
    time.sleep(1)