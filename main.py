import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    ContextTypes,
    CommandHandler,
    MessageHandler,
    filters,
    Application,
)
from dotenv import load_dotenv
import os
from database import Database
from gemini import GeminiClient

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

gemini = GeminiClient()
database = Database()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chatid = update.effective_chat.id
    chat_history = database.get(chatid)
    if not chat_history:
        database.set(chatid, [])
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Cleaned chat history.",
        )

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Welcome to Game Master Bot. I can run RPG campaigns for you. \n\nJust reply this message with your commands.",
    )


async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    chatid = update.effective_chat.id
    chat_history = database.get(chatid)

    try:
        response, updated_history = gemini.chat(message, history_data=chat_history)
        database.set(chatid, updated_history)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Um erro ocorreu.",
        )


async def all_messages_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message.text
    reply_to_message = update.message.reply_to_message
    is_reply_to_me = (
        reply_to_message.from_user.id == context.bot.id if reply_to_message else None
    )
    bot_name = context.bot.username
    in_group = (
        update.message.chat.type == "group" or update.message.chat.type == "supergroup"
    )

    if not in_group:
        return await reply(update, context)

    if bot_name in message or is_reply_to_me:
        return await reply(update, context)


async def post_init(application: Application) -> None:
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


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    start_handler = CommandHandler(["start", "iniciar"], start)
    narrator_command = CommandHandler(["narrador", "narrator"], reply)
    messageHanlder = MessageHandler(
        filters.TEXT & (~filters.COMMAND), all_messages_handler
    )

    application.add_handler(start_handler)
    application.add_handler(narrator_command)
    application.add_handler(messageHanlder)

    application.run_polling()
