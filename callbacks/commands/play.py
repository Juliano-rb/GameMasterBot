import logging
from typing import Callable
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ChatAction
from database import Database
from gemini import GeminiClient
from chatgpt_md_converter import telegram_format
from google.api_core.exceptions import ResourceExhausted
from prompt.prompt import load_prompt


async def play(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    chatid = update.effective_chat.id
    from_name = (
        update.callback_query.from_user.first_name
        + " "
        + update.callback_query.from_user.name
    )
    user_language = update.callback_query.from_user.language_code

    await context.bot.send_chat_action(chat_id=chatid, action=ChatAction.TYPING)

    database = Database()
    gemini = GeminiClient()

    chat_history = database.get(chatid)
    if chat_history:
        chat_history = []
        database.set(chatid, chat_history)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Cleaned chat history.",
        )

    prompt = load_prompt(query.data, user_language)
    print(prompt)

    message_header = f"new message from: {from_name}\n------\n"

    try:
        response, updated_history = gemini.chat(
            message_header + prompt, history_data=chat_history
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
