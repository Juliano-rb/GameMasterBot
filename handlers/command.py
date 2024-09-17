import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from chatgpt_md_converter import telegram_format
from services.database import Database
from services.gemini_api import GeminiClient
from prompt.prompt import get_template_configs
from google.api_core.exceptions import ResourceExhausted


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    chatid = update.effective_chat.id
    from_name = (
        update.message.from_user.first_name + " " + update.message.from_user.name
    )

    await context.bot.send_chat_action(chat_id=chatid, action=ChatAction.TYPING)

    database = Database()
    gemini = GeminiClient()

    chat_history = database.get(chatid)
    if not chat_history:

        keyboard = [
            [InlineKeyboardButton(text=item["Description"], callback_data=item["id"])]
            for item in get_template_configs()
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=("Choose one of the themes below to start your campaign:\n\n"),
            parse_mode="HTML",
            reply_markup=reply_markup,
        )
        return

    message_header = f"new message from: {from_name}\n------\n"

    try:
        response, updated_history = gemini.chat(
            message_header + message, history_data=chat_history
        )
        formatted_response = telegram_format(response)
        database.set(chatid, updated_history)
        await context.bot.send_message(
            chat_id=update.effective_chat.id, text=formatted_response, parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Error sending data to Gemini. Chat: {chatid}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"An error occurred: {str(e)}",
        )


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    database = Database()

    chatid = update.effective_chat.id

    database.set(chatid, [])

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Cleaned chat history.",
    )

    keyboard = [
        [InlineKeyboardButton(text=item["Description"], callback_data=item["id"])]
        for item in get_template_configs()
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=(
            "Welcome to Game Master Bot. I can run RPG campaigns for you. \n\n"
            "Choose one of the themes below to start your campaign"
        ),
        parse_mode="HTML",
        reply_markup=reply_markup,
    )
