from motor.motor_asyncio import AsyncIOMotorDatabase
from telegram import Update
from telegram.ext import ContextTypes

from database.models import User
from database.repositories import UserRepository


class UserService:
    __slots__ = ("database", "user_repository", "user")

    def __init__(self, database: AsyncIOMotorDatabase):
        self.database = database
        self.user_repository = UserRepository(database=self.database)
        self.user: User | None = None

    async def get_or_create_user(self, user: User) -> User:
        if not await self.user_repository.get_one(user.user_id):
            await self.user_repository.create(user)
        self.user = user
        return self.user


class MessageHandler:
    def __init__(self, user: User):
        self.user: User = user

    async def handle_user_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        pass
