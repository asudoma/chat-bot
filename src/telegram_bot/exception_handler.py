import logging

from telegram import Update
from telegram.ext import ContextTypes

from clients.file_server.exceptions import YoutubeError

logger = logging.getLogger(__name__)


def exception_handler(func):
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
        try:
            return await func(update, context, **kwargs)
        except Exception as exc:
            if isinstance(exc, YoutubeError):
                match exc.code:
                    case 1001:
                        text = "There are no captions in the video."
                    case 1002:
                        text = "Wrong video ID. Try another link."
                    case _:
                        text = "We got an error while getting data from youtube.\nTry again."
            else:
                text = "Кажется произошла ошибка. Но мы уже начали её чинить!\nПопробуйте еще раз."
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=text,
            )
            logger.exception("Error occurred")
            raise

    return wrapper
