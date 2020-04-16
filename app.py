import schedule
import time
import telegram
from telegram import *
from telegram.ext import *
from threading import *
import logging as py_log
from nsepy import get_history
import numpy as np
import pandas as pd
from datetime import date, timedelta
import os
import csv
py_log.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=py_log.INFO)
logger = py_log.getLogger()
logger.setLevel(py_log.INFO)


token = "1089284422:AAFLulS1w1NVzFdh-2hsSVlFRtiIGh2ph7s"
bot = Bot(token=token)
chat = [-469052538,537825532]

for chat in chat:
    bot.send_message(chat_id = chat, text = "Bot Starting")

def function1():
    os.system("python stockSD.py")
    chat = [-469052538,537825532]
    for chat in chat:
        bot.send_message(chat_id = chat, text = "stocksd executed")
        bot.send_document(chat_id = chat, document = open("historicalSD1.csv","rb"))

schedule.every().day.at("15:30").do(function1)

while True:
    schedule.run_pending()
    time.sleep(1)