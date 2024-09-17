import logging
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    CallbackQueryHandler,
)

from handlers.message import any_message_handler
from handlers.callbacks import play_callback, post_init_callback
from handlers.command import start, reply
from prompt.prompt import get_template_configs_ids
from config import BOT_TOKEN


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


if __name__ == "__main__":
    application = (
        ApplicationBuilder().token(BOT_TOKEN).post_init(post_init_callback).build()
    )

    bot_commands = get_template_configs_ids()

    start_handler = CommandHandler(["start", "iniciar"], start)
    narrator_command = CommandHandler(["narrador", "narrator"], reply)
    message_hanlder = MessageHandler(
        filters.TEXT & (~filters.COMMAND), any_message_handler
    )
    play_game_handler = CallbackQueryHandler(play_callback)

    application.add_handler(start_handler)
    application.add_handler(narrator_command)
    application.add_handler(message_hanlder)
    application.add_handler(play_game_handler)

    application.run_polling()
