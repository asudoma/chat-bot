from motor.motor_asyncio import AsyncIOMotorCollection, AsyncIOMotorDatabase

from database.models import Chat, Message, User


class UserRepository:
    __slots__ = ("_database", "_collection")

    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database
        self._collection: AsyncIOMotorCollection = self._database.users

    async def get_one(self, user_id: int) -> User | None:
        user_data = await self._collection.find_one({"user_id": user_id})
        return User.model_validate(user_data) if user_data else None

    async def create(self, user: User):
        await self._collection.insert_one(user.model_dump())

    async def save(self, user: User):
        await self._collection.update_one(
            filter={"user_id": user.user_id}, update={"$set": user.model_dump()}, upsert=True
        )


class ChatRepository:
    __slots__ = ("_database", "_collection")

    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database
        self._collection: AsyncIOMotorCollection = self._database.chats

    async def get_one(self, chat_id: int) -> Chat | None:
        chat = await self._collection.find_one({"chat_id": chat_id})
        return Chat.model_validate(chat) if chat else None

    async def create(self, chat: Chat):
        await self._collection.insert_one(chat.model_dump())


class MessageRepository:
    __slots__ = ("_database", "_collection")

    def __init__(self, database: AsyncIOMotorDatabase):
        self._database = database
        self._collection: AsyncIOMotorCollection = self._database.messages

    async def create(self, message: Message):
        await self._collection.insert_one(message.model_dump(exclude_none=True))
