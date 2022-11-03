from pydantic import BaseModel


class PotSchema(BaseModel):
    id: int
    user_id: int
    pot: int
