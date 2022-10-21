from pydantic import BaseModel


class ChatSchema(BaseModel):
    id: int
    chat_type: str
