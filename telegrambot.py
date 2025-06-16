import os
import django
import sys
from dotenv import load_dotenv
from asgiref.sync import sync_to_async


# Dynamically set path to your Django project root
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(BASE_DIR)
sys.path.append(PROJECT_ROOT)  #  path to your project root
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AdvanceBlog.settings')  #  your_project.settings
django.setup()

# Now safe to import Django models
from telegram_bot.models import TelegramUser
from telegram_bot.views import ask_openai

# Load environment variables
load_dotenv()
API_KEY = os.getenv('TELEGRAM_API_KEY')  # use os.getenv instead of os.environ()

from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, CommandHandler, filters

print('BOT STARTED')

# Wrap your existing sync function
ask_openai_async = sync_to_async(ask_openai)


@sync_to_async
def get_or_create_user(chat_id, username, first_name, last_name):
    return TelegramUser.objects.get_or_create(
        telegram_id=chat_id,
        defaults={
            'username': username,
            'first_name': first_name,
            'last_name': last_name,
        }
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    chat_id = user.id
    first_name = user.first_name
    last_name = user.last_name
    username = user.username

    obj, created = await get_or_create_user(chat_id, username, first_name, last_name)

    if created:
        print(f"New user added: {first_name}")
        await update.message.reply_text(f"Hi {first_name}, you are registered!")
    else:
        await update.message.reply_text(f"Welcome back {first_name}!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = str(update.message.text).lower()
    response = await ask_openai_async(text)  # Await the async wrapper
    await update.message.reply_text(response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(API_KEY).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling()
