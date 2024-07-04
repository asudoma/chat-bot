from openai import AsyncOpenAI

from settings import settings

openai_client = AsyncOpenAI(api_key=settings.openai_secret_key)
