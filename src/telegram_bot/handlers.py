from telegram.ext import BaseHandler, CommandHandler, MessageHandler, filters

from telegram_bot.commands import process_message, start


def create_handlers() -> list[BaseHandler]:
    return [
        CommandHandler("start", start),
        MessageHandler(filters.TEXT & (~filters.COMMAND), process_message),
        MessageHandler(filters.COMMAND, start),
    ]
