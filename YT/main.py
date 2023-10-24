import telegram.ext
from telegram.ext import CommandHandler, MessageHandler, Filters, Updater
from dotenv import load_dotenv
import os
from pytube import YouTube

load_dotenv()
TOKEN = os.getenv("TOKEN")

def start(update, context):
    update.message.reply_text("Benvenuto in questo BOT.")
    update.message.reply_text("Scrivi l'URL di un video di YouTube:")

def handle_input(update, context):
    url = update.message.text

    try:
        yt = YouTube(url)
        video_url = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first().url
        update.message.reply_text("Ecco il video:")
        update.message.reply_text(video_url)
    except Exception as e:
        update.message.reply_text(f"Si è verificato un errore: {str(e)}")

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_input))

    updater.start_polling()
    updater.idle()
