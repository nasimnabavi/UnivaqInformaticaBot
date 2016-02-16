#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
This Bot uses the Updater class to handle the bot.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import json
import string
import logging
import telegram
import feedparser
import configparser

from telegram import Updater

def get_configuration():
    """Get global configuration from service.cfg"""

    config = configparser.ConfigParser()
    config.read("service.cfg")

    return config

def get_logger(debug):
    """Get logger object"""

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
        )
    logger = logging.getLogger(__name__)

    if debug is False:
        logging.disable(logging.CRITICAL)

    return logger

def pull_news():
    """ This function is built to pull all the news from rss endpoint """
    document = feedparser.parse(
        "http://www.disim.univaq.it/didattica/content.php?fid=rss&pid=114&did=8&lid=it"
        )
    news = [
        {"title": item.title, "description": string.replace(item.description, "&amp;#39;", "'")}
        for item in document["entries"][:10]
        ]
    return news

def write_news():
    """Pulling and writing news to the json file"""
    news = pull_news()
    with open("json/news.json", "w") as news_file:
        json.dump(news, news_file)

def check_news():
    """This function check if there is some unread news from the website"""
    pulled_news = pull_news()
    stored_news = read_news()
    unread_news = []

    for i in range(0, 10):
        if pulled_news[i]["title"] != stored_news[i]["title"]:
            unread_news.append(pulled_news[i]["title"])

    return unread_news

def read_news():
    """This function read news locally stored into the json file"""
    with open("json/news.json", "r") as news_file:
        return json.load(news_file)

def start_command(bot, update):
    """Defining the `start` command"""

    welcome = "Ciao, sono il bot dell'Univaq (Università dell'Aquila).\n" \
              "Premendo uno dei bottoni che vedi qui sotto, " \
              "posso fornirti tutte le informazioni di cui hai bisogno sulla nostra università. "

    bot.sendMessage(update.message.chat_id, text=welcome)

def help_command(bot, update):
    """Defining the `help` command"""

    help_message = "Sono il bot dell'Univaq (Università dell'Aquila).\n" \
                   "Premendo uno dei bottoni qui sotto, posso fornirti " \
                   "tutte le informazioni di cui hai bisogno sulla nostra università.\n\n" \
                   "Ecco la lista di comandi:\n\n" \
                   "/help - Stampa questo messaggio\n" \
                   "/news - Stampa le ultime 10 news\n" \
                   "/prof - Mostra info sui professori\n" \
                   "/mensa - Stampa gli orari della mensa\n" \
                   "/cancel - Cancella l'ultima operazione\n" \
                   "/commands_keyboard - Mostra la tastiera"

    bot.sendMessage(update.message.chat_id, text=help_message)

def news_command(bot, update):
    """Defining the `news` command"""

    bot.sendMessage(update.message.chat_id, text=update.message.text)

def prof_command(bot, update):
    """Defining the `prof` command"""

    bot.sendMessage(update.message.chat_id, text="Lista professori da Professors.json")

def commands_keyboard(bot, update):
    """Enable a custom keyboard"""

    keyboard = [["/help", "/news", "/prof", "/mensa", "/cancel"]]
    reply_markup = telegram.ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    bot.sendMessage(update.message.chat_id, text="Enabled keyboard", reply_markup=reply_markup)

def canteen_command(bot, update):
    """Defining the `canteen` command"""

    bot.sendMessage(update.message.chat_id, text="Orari della mensa")

def cancel_command(bot, update):
    """Defining the cancel command to delete last operation"""

    bot.sendMessage(update.message.chat_id, text="Ultima operazione annullata")

def newson_command(bot, update):
    """Defining the command to enable notifications for news"""

    def notify_news(bat):
        """Defining method that will be repeated over and over"""
        unread_news = check_news()

        if len(unread_news) > 0:
            write_news()
            bat.sendMessage(update.message.chat_id, text='Ci sono nuove news')

    bot.sendMessage(update.message.chat_id, text='Notifiche abilitate')
    JOB_QUEUE.put(notify_news, 10, repeat=True)

def newsoff_command(bot, update):
    """Defining the command to disable notifications for news"""

    JOB_QUEUE.stop()
    bot.sendMessage(update.message.chat_id, text='Notifiche disabilitate')

def main():
    """Defining the main function"""

    global JOB_QUEUE

    config = get_configuration()
    token = config.get('API-KEYS', 'TelegramBot')
    debug = config.getboolean('UTILS', 'Debug')
    logger = get_logger(debug)

    updater = Updater(token)
    JOB_QUEUE = updater.job_queue
    dispatcher = updater.dispatcher

    dispatcher.addTelegramCommandHandler("start", start_command)
    dispatcher.addTelegramCommandHandler("help", help_command)
    dispatcher.addTelegramCommandHandler("news", news_command)
    dispatcher.addTelegramCommandHandler("newson", newson_command)
    dispatcher.addTelegramCommandHandler("newsoff", newsoff_command)
    dispatcher.addTelegramCommandHandler("prof", prof_command)
    dispatcher.addTelegramCommandHandler("mensa", canteen_command)
    dispatcher.addTelegramCommandHandler("commands_keyboard", commands_keyboard)
    dispatcher.addTelegramCommandHandler("cancel", cancel_command)


    logger.info('Bot started')

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
