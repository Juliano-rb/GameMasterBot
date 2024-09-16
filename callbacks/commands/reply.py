import logging
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update,
)
from telegram.ext import ContextTypes
from telegram.constants import ChatAction
from database import Database
from gemini import GeminiClient
from chatgpt_md_converter import telegram_format
from google.api_core.exceptions import ResourceExhausted
from prompt.prompt import get_template_configs


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
    except ResourceExhausted:
        logging.error(f"Gemini quota has been exhausted. Chat: {chatid}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Gemini quota has been exhausted. Try again later.",
        )
    except Exception as e:
        logging.error(e)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Um erro ocorreu.",
        )
