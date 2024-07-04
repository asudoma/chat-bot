import logging

from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


def exception_handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
        try:
            return await func(update, context, **kwargs)
        except Exception:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Кажется произошла ошибка. Но мы уже начали её чинить!\nПопробуйте еще раз.",
            )
            logger.exception("Error occurred")
            raise

    return wrapper
