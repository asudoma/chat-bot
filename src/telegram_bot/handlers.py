from telegram.ext import BaseHandler, CommandHandler, MessageHandler, filters

from telegram_bot.commands import process_command, process_message, process_voice


def create_handlers() -> list[BaseHandler]:
    return [
        CommandHandler("start", process_command),
        MessageHandler(filters.TEXT & (~filters.COMMAND), process_message),
        MessageHandler(filters.VOICE & (~filters.COMMAND), process_voice),
        MessageHandler(filters.COMMAND, process_command),
    ]
