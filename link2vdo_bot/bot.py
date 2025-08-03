from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import yt_dlp
import os

BOT_TOKEN = "8374166424:AAFhp0PrJFKveBYT5ycIcFAP3RHgBgYcRHg"

async def start(update, context):
    await update.message.reply_text("👋 Hello! Send any video link to download.")

async def download_video(update, context):
    url = update.message.text
    await update.message.reply_text("📥 Downloading... please wait.")

    try:
        ydl_opts = {
            'outtmpl': '%(title)s.%(ext)s',
            'format': 'best',
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        with open(file_name, 'rb') as f:
            await update.message.reply_video(f)

        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"❌ Failed to download:\n{e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == "__main__":
    main()


