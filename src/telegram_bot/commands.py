from sentry_sdk.integrations import httpx
from telegram import Update
from telegram.ext import ContextTypes

from clients.file_server.client import Client as FileClient
from clients.file_server.exceptions import ServerNotWorkingError, WrongResponseError
from clients.file_server.models import RecognizeVoiceRequestModel
from database.models import Message, User
from telegram_bot.decorators import bot_is_typing, provide_user
from telegram_bot.exception_handler import exception_handler
from telegram_bot.helpers import create_chat_service


@provide_user
@exception_handler
@bot_is_typing
async def process_command(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
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


@provide_user
@exception_handler
@bot_is_typing
async def process_voice(update: Update, context: ContextTypes.DEFAULT_TYPE, user: User):
    chat_service = await create_chat_service(user, update.effective_chat)
    message = update.message
    file_id = message.voice.file_id
    file = await message.get_bot().get_file(file_id)
    async with httpx.AsyncClient() as client:
        file_client = FileClient(client)
        request_data = {
            **file.to_dict(),
            "entity_id": str(update.effective_chat.id),
        }
        try:
            result = await file_client.recognize_speech(RecognizeVoiceRequestModel(**request_data))
        except (ServerNotWorkingError, WrongResponseError):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="В данный момент распознавание голоса не работает. Попробуйте позже или напишите вопрос текстом",
            )
        else:
            data = Message(
                message_id=message.id,
                role="user",
                text=result.text,
                created=message.date,
                type="user_voice",
                voice_params=request_data,
            )
            answer = await chat_service.create_message(data)
            await context.bot.send_message(chat_id=update.effective_chat.id, text=answer)
