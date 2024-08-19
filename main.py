import os
import telebot
import yt_dlp
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Initialize the bot with the token
bot = telebot.TeleBot(BOT_TOKEN)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(
        message, "Send me a YouTube video link, and I'll download it for you!")


@bot.message_handler(func=lambda message: True)
def download_video(message):
    video_url = message.text

    # Send a "processing" message
    processing_message = bot.reply_to(
        message, "Processing your request, please wait...")

    # Download the video using yt-dlp
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_url])

        # Send the video back to the user
        with open('downloaded_video.mp4', 'rb') as video_file:
            bot.send_video(message.chat.id, video_file)

        # Delete the file after sending
        os.remove('downloaded_video.mp4')
        print("downloaded_video.mp4 deleted successfully.")

        # Delete the "processing" message
        bot.delete_message(message.chat.id, processing_message.message_id)

    except Exception as e:
        bot.reply_to(message, f"An error occurred: {str(e)}")
        bot.delete_message(message.chat.id, processing_message.message_id)


# Start the bot
bot.infinity_polling()