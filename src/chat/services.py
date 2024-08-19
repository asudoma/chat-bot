from motor.motor_asyncio import AsyncIOMotorDatabase
from openai import AsyncOpenAI

from database.models import Chat, Message, User
from database.repositories import ChatRepository, MessageRepository, UserRepository
from settings import settings


class ChatService:
    __slots__ = (
        "user",
        "database",
        "user_repository",
        "chat_repository",
        "openai_client",
        "chat",
        "message_repository",
    )

    def __init__(self, user: User, openai_client: AsyncOpenAI, database: AsyncIOMotorDatabase):
        self.user = user
        self.openai_client = openai_client
        self.database = database
        self.user_repository = UserRepository(database=self.database)
        self.chat_repository = ChatRepository(database=self.database)
        self.message_repository = MessageRepository(database=self.database)
        self.chat: Chat | None = None

    async def set_chat(self, chat: Chat):
        self.chat = await self.chat_repository.get_one(chat.chat_id)
        if not self.chat:
            await self.chat_repository.create(chat)
            self.chat = chat

    async def create_message(self, message: Message):
        message.chat_id = self.chat.chat_id
        await self.message_repository.create(message)
        if message.type == "command":
            answer = await self.process_command(message.text)
            await self.message_repository.create(
                Message(chat_id=message.chat_id, role="server", type="command_answer", text=answer)
            )
            return answer
        if message.type == "user_text":
            answer = await self.create_reply(message.text)
            await self.message_repository.create(
                Message(
                    chat_id=message.chat_id, role="server", type="answer", text=answer, model_name=settings.model_name
                )
            )
            return answer

    async def process_command(self, text: str) -> str:
        if text == "/start":
            return (
                "Привет! 😃 Я ваш дружелюбный текстовый бот, всегда готов помочь с любыми задачами. "
                "Вопросы, идеи или просто поболтать — я всегда здесь для вас!\n"
                "Пока что могу общаться только текстом, но скоро у меня появится еще больше возможностей, "
                "и тогда наше общение станет еще круче. Если что-то нужно или есть вопросы, не стесняйся, пиши! 😊\n"
                "Кстати, как тебя зовут?"
            )
        else:
            return "Пока, к сожалению, такой команды не знаю 😊"

    async def create_reply(self, message: str) -> str:
        messages = [
            {
                "role": "system",
                "content": "You are helpful unobtrusive assistant. Your name is Чарли.",
            }
        ]
        context = await self.create_context(self.chat.chat_id)
        if context:
            messages.extend(context)
        messages.append({"role": "user", "content": message})
        chat_completion = await self.openai_client.chat.completions.create(messages=messages, model=settings.model_name)
        assistant_message = chat_completion.choices[0].message.content
        return assistant_message

    async def create_context(self, chat_id: int) -> list[dict]:
        last_messages = await self.message_repository.get_last_messages(chat_id, settings.context_length)
        if not last_messages:
            return []
        result = []
        for message in reversed(last_messages):
            role = message.role if message.role == "user" else "assistant"
            result.append({"role": role, "content": message.text})
        return result
