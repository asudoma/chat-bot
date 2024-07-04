from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    log_level: str = "INFO"
    openai_secret_key: str
    mongo_uri: str = "mongodb://localhost:27017/"
    mongo_db_name: str = "chatbot"
    support_email: str = "artem.sudoma@gmail.com"
    sentry_dsn: str | None = None


settings = Settings()
