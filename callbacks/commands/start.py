from telegram import Update
from telegram.ext import ContextTypes
from database import Database


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database()

    chatid = update.effective_chat.id

    database.set(chatid, [])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Cleaned chat history.",
    )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to Game Master Bot. I can run RPG campaigns for you. \n\nJust reply this message with your commands.",
    )
