from callbacks.commands import reply
from telegram import Update
from telegram.ext import ContextTypes


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
        # pylint: disable=not-callable
        return await reply(update, context)

    if bot_name in message or is_reply_to_me:
        # pylint: disable=not-callable
        return await reply(update, context)
