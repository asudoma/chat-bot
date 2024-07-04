from motor.motor_asyncio import AsyncIOMotorClient

from settings import settings


def get_client() -> AsyncIOMotorClient:
    return AsyncIOMotorClient(settings.mongo_uri)


mongo_client = get_client()
