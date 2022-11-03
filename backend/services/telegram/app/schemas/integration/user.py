from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    id: int
    telegram: int
    email: EmailStr = None
    username: str
    join: datetime = None
