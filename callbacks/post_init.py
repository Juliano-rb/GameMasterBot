from telegram.ext import (
    Application,
)


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
