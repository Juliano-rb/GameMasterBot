from telegram import Update
from telegram.ext import ContextTypes
from database import Database
from prompt.prompt import get_template_configs


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database()

    chatid = update.effective_chat.id

    database.set(chatid, [])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Cleaned chat history.",
    )

    options_text = "".join(
        [
            f"- /{item['id']} - <b>{item['Description']}</b>\n"
            for item in get_template_configs()
        ]
    )
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Welcome to Game Master Bot. I can run RPG campaigns for you. \n\n"
            "/start clean chat history to start a new campaing. \n\n"
            "Choose one of the themes below to start your campaign:\n" + options_text
        ),
        parse_mode="HTML",
    )
