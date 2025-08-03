import os
import yt_dlp
from flask import Flask, request
from telegram import Update, Bot
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

TOKEN = "8374166424:AAFhp0PrJFKveBYT5ycIcFAP3RHgBgYcRHg"
bot = Bot(token=TOKEN)
app = Flask(__name__)

application = ApplicationBuilder().token(TOKEN).build()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Send me a video link to download.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("⏬ Downloading... Please wait.")
    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'best[filesize<50M]/best',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as video:
            await update.message.reply_video(video)
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"⚠️ Error: {str(e)}")

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

@app.route("/", methods=["GET"])
def index():
    return "✅ Bot is running."

@app.route("/", methods=["POST"])
async def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    await application.process_update(update)
    return "ok"

if __name__ == "__main__":
    app.run(port=8080)

