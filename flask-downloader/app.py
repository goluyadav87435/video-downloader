import os
from flask import Flask, request
from yt_dlp import YoutubeDL
import telebot

# Telegram Bot Token
BOT_TOKEN = '8374166424:AAFhp0PrJFKveBYT5ycIcFAP3RHgBgYcRHg'
bot = telebot.TeleBot(BOT_TOKEN)

# Flask app setup
app = Flask(__name__)

# Download folder
DOWNLOAD_DIR = 'downloads'
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# YDL options
ydl_opts = {
    'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
    'format': 'best[filesize<2000M]/best',
    'noplaylist': True,
    'quiet': True,
    'no_warnings': True,
}

# Webhook endpoint to receive Telegram messages
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return '', 200

# /start command handler
@bot.message_handler(commands=["start"])
def start_message(message):
    bot.reply_to(message, "👋 Send me a video link to download it.")

# Video link handler
@bot.message_handler(func=lambda message: message.text and message.text.startswith(("http://", "https://")))
def handle_video_link(message):
    url = message.text.strip()
    chat_id = message.chat.id
    bot.send_message(chat_id, "📥 Downloading... Please wait.")
    
    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        # Send video if file exists and is less than 2GB
        if os.path.exists(filename) and os.path.getsize(filename) < 2 * 1024 * 1024 * 1024:
            with open(filename, 'rb') as video:
                bot.send_video(chat_id, video)
        else:
            bot.send_message(chat_id, "⚠️ File too large to send on Telegram.")

    except Exception as e:
        bot.send_message(chat_id, f"❌ Error: {str(e)}")

# Root route just for checking if Flask app is running
@app.route('/')
def index():
    return "✅ Flask + Telegram Bot is Running."

if __name__ == '__main__':
    # Start Flask app
    app.run(host='0.0.0.0', port=5000)

