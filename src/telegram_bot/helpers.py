from telegram import Chat as TGChat

from chat.services import ChatService
from core.openai import openai_client
from database.models import Chat, User
from database.mongo import mongo_client
from settings import settings


async def create_chat_service(user: User, chat: TGChat) -> ChatService:
    chat = Chat.model_validate(chat.to_dict())
    chat_service = ChatService(user=user, openai_client=openai_client, database=mongo_client[settings.mongo_db_name])
    await chat_service.set_chat(chat)
    return chat_service
