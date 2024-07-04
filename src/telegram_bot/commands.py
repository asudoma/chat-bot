from telegram import Update
from telegram.ext import ContextTypes

from database.models import Message, User
from telegram_bot.decorators import bot_is_typing, provide_user
from telegram_bot.exception_handler import exception_handler
from telegram_bot.helpers import create_chat_service


@provide_user
@exception_handler
@bot_is_typing
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
    chat_service = await create_chat_service(user, update.effective_chat)
    message = update.message
    answer = await chat_service.create_message(
        Message(message_id=message.id, role="user", text=message.text, created=message.date, type="command")
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)


@provide_user
@exception_handler
@bot_is_typing
async def process_message(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
    chat_service = await create_chat_service(user, update.effective_chat)
    message = update.message
    answer = await chat_service.create_message(
        Message(message_id=message.id, role="user", text=message.text, created=message.date, type="user_text")
    )
    await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
