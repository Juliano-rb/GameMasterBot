import logging
from telegram import Update
from telegram.ext import CallbackContext
from telegram.constants import ChatAction
from telegram.ext import (
    Application,
)
from chatgpt_md_converter import telegram_format
from services.database import Database
from services.gemini_api import GeminiClient
from services.i18n import get_locale
from prompt.prompt import load_prompt


async def post_init_callback(application: Application) -> None:
    await application.bot.set_my_commands(
        [
            ("start", "Restart the conversation. Welcome message."),
            ("narrator", "Chat with the narrator in groups."),
        ],
        language_code="en",
    )
    await application.bot.set_my_commands(
        [
            ("iniciar", "Reinicia a conversa. Mensagem de boas vindas."),
            ("narrador", "Conversa com o narrador em grupos."),
        ],
        language_code="pt",
    )


async def play_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    chatid = update.effective_chat.id
    from_name = (
        update.callback_query.from_user.first_name
        + " "
        + update.callback_query.from_user.name
    )
    user_language = update.callback_query.from_user.language_code
    _ = get_locale(user_language)

    await context.bot.send_chat_action(chat_id=chatid, action=ChatAction.TYPING)

    database = Database()
    gemini = GeminiClient()

    chat_history = database.get(chatid)
    if chat_history:
        chat_history = []
        database.set(chatid, chat_history)

        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=_("Cleaned chat history."),
        )

    prompt = load_prompt(query.data, user_language)

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
    except Exception as e:
        logging.error(f"Error sending data to Gemini. Chat: {chatid}")
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=_("An error occurred:") + str(e),
        )
