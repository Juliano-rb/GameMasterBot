import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os
from gemini import GeminiClient

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

gemini = GeminiClient()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to Game Master Bot. I can run RPG campaigns for you.",
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    response = gemini.chat(message)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler("start", start)
    message_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), reply)
    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
