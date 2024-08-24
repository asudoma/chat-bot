from pydantic import BaseModel, HttpUrl, field_serializer


class RecognizeVoiceRequestModel(BaseModel):
    file_id: str
    file_path: HttpUrl | str
    file_size: int
    file_unique_id: str
    entity_id: str

    @field_serializer("file_path")
    def file_path_serializer(self, value: str | HttpUrl) -> str:
        return str(value)


class RecognizeVoiceResponseModel(BaseModel):
    text: str
