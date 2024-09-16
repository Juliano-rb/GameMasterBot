import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
)
from dotenv import load_dotenv
import os
from callbacks import all_messages_handler, post_init
from callbacks.commands import play, start, reply
from prompt.prompt import get_template_configs_ids

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    application = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()

    commands = get_template_configs_ids()

    start_handler = CommandHandler(["start", "iniciar"], start)
    narrator_command = CommandHandler(["narrador", "narrator"], reply)
    message_hanlder = MessageHandler(
        filters.TEXT & (~filters.COMMAND), all_messages_handler
    )
    play_game_handler = CommandHandler(commands, play)

    application.add_handler(start_handler)
    application.add_handler(narrator_command)
    application.add_handler(message_hanlder)
    application.add_handler(play_game_handler)

    application.run_polling()
