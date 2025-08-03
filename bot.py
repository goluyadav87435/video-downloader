import telebot
import subprocess

# ✅ Aapka Bot Token
TOKEN = "8374166424:AAFhp0PrJFKveBYT5ycIcFAP3RHgBgYcRHg"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👋 Welcome! Send me any video link and I'll try to download it.")

@bot.message_handler(func=lambda message: True)
def handle_link(message):
    url = message.text.strip()
    chat_id = message.chat.id

    bot.send_message(chat_id, "⏳ Downloading... Please wait...")

    try:
        # Video download command using yt-dlp
        output_file = "video.mp4"
        cmd = ["yt-dlp", "-o", output_file, url]
        subprocess.run(cmd, check=True)

        # Send video back to user
        with open(output_file, "rb") as video:
            bot.send_video(chat_id, video)

    except Exception as e:
        bot.send_message(chat_id, f"❌ Failed to download: {e}")

bot.polling()
