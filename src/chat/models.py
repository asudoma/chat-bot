from pydantic import BaseModel


class ReplyData(BaseModel):
    content: str
    prompt_tokens: int
    total_tokens: int
    model_name: str
