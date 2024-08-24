from motor.motor_asyncio import AsyncIOMotorDatabase
from openai import AsyncOpenAI

from chat.handlers.commands import CommandManager
from chat.models import ReplyData
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
        "command_manager",
    )

    def __init__(
        self, user: User, openai_client: AsyncOpenAI, database: AsyncIOMotorDatabase, command_manager: CommandManager
    ):
        self.user = user
        self.openai_client = openai_client
        self.database = database
        self.user_repository = UserRepository(database=self.database)
        self.chat_repository = ChatRepository(database=self.database)
        self.message_repository = MessageRepository(database=self.database)
        self.command_manager: CommandManager = command_manager
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
            answer_data = await self.create_reply(message.text)
            await self.message_repository.create(
                Message(
                    chat_id=message.chat_id,
                    role="server",
                    type="consultant",
                    text=answer_data.content,
                    model_name=settings.model_name,
                    usage={
                        "prompt_tokens": answer_data.prompt_tokens,
                        "total_tokens": answer_data.total_tokens,
                        "model_name": answer_data.model_name,
                    },
                )
            )
            return answer_data.content
        if message.type == "user_voice":
            answer_data = await self.create_reply(message.text)
            await self.message_repository.create(
                Message(
                    chat_id=message.chat_id,
                    role="server",
                    type="consultant",
                    text=answer_data.content,
                    model_name=settings.model_name,
                    usage={
                        "prompt_tokens": answer_data.prompt_tokens,
                        "total_tokens": answer_data.total_tokens,
                        "model_name": answer_data.model_name,
                    },
                )
            )
            return answer_data.content

    async def process_command(self, text: str) -> str:
        command = self.command_manager.get_handler(text)
        return await command.process()

    async def create_reply(self, message: str) -> ReplyData:
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
        return ReplyData(
            content=chat_completion.choices[0].message.content,
            prompt_tokens=chat_completion.usage.prompt_tokens,
            total_tokens=chat_completion.usage.total_tokens,
            model_name=chat_completion.model,
        )

    async def create_context(self, chat_id: int) -> list[dict]:
        last_messages = await self.message_repository.get_last_messages(chat_id, settings.context_length)
        if not last_messages:
            return []
        result = []
        for message in reversed(last_messages):
            role = message.role if message.role == "user" else "assistant"
            result.append({"role": role, "content": message.text})
        return result
