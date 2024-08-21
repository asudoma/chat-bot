from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class User(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    user_id: int = Field(alias="id")
    first_name: str | None = None
    last_name: str | None = None
    username: str | None = None
    is_bot: bool = False
    is_premium: bool = False
    language_code: str | None = None
    active: bool = True
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Chat(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    chat_id: int = Field(alias="id")
    type: str = Field(alias="type")
    created: datetime = Field(default_factory=lambda: datetime.now(UTC))


class Message(BaseModel):
    model_config = ConfigDict(extra="ignore", populate_by_name=True)

    message_id: int | None = Field(alias="id", default=None)
    role: Literal["user", "server"]
    type: Literal["command", "command_answer", "user_text", "answer", "consultant"]
    text: str = Field()
    chat_id: int | None = None
    model_name: str | None = None
    usage: dict | None = Field(default_factory=dict)
    created: datetime = Field(default_factory=lambda: datetime.now(UTC), populate_by_name=True, alias="date")
