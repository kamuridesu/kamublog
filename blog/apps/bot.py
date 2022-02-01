from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

updater = Updater(token='M', use_context=True)
dispatcher = updater.dispatcher

def send_message(chat_id, messag):
    updater.bot.send_message(chat_id=chat_id, text=messag)

if __name__ == "__main__":
    updater.start_polling()