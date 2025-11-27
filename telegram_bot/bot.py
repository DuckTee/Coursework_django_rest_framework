from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from django.conf import settings


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Я бот для привычек.")


def run_bot():
    app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.run_polling()
