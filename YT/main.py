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

    # Puoi fare ciò che vuoi con il valore immesso, ad esempio assegnarlo a una variabile
    yt = YouTube(url)
    
    # Scegli il formato MP4 in streaming
    vid = yt.streams.filter(progressive=True, file_extension='mp4').order_by('resolution').desc().first()
    
    # Imposta il percorso di download
    download_path = 'percorso/del/tuo/download'  # Sostituisci con il percorso desiderato

    # Scarica il video in blocchi
    video_path = os.path.join(download_path, f"{yt.title}.mp4")
    with open(video_path, 'wb') as file:
        for chunk in vid.stream_to_buffer():
            file.write(chunk)

    update.message.reply_text("Video in anteprima:")

    # Invia il video scaricato come messaggio video
    context.bot.send_video(chat_id=update.effective_chat.id, video=open(video_path, 'rb'))

    # Elimina il file locale
    os.remove(video_path)

if __name__ == "__main__":
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_input))

    updater.start_polling()
    updater.idle()
