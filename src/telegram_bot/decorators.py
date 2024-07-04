import functools

from telegram import Update
from telegram.constants import ChatAction
from telegram.ext import ContextTypes

from database.models import User
from database.mongo import mongo_client
from settings import settings
from telegram_bot.services import UserService


def provide_user(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
        database = mongo_client[settings.mongo_db_name]
        user_service = UserService(database=database)
        user = await user_service.get_or_create_user(User.model_validate(update.effective_user.to_dict()))

        if not user.active:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"К сожалению, ваш аккаунт неактивен или заблокирован.\n"
                f"Пожалуйста, свяжитесь с нами для разблокировки {settings.support_email}",
            )
            return
        return await func(update=update, context=context, user=user, **kwargs)

    return wrapper


def bot_is_typing(func):
    @functools.wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, **kwargs):
        await context.bot.send_chat_action(chat_id=update.effective_message.chat_id, action=ChatAction.TYPING)
        return await func(update=update, context=context, **kwargs)

    return wrapper
