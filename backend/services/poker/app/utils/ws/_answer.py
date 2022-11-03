from pydantic import BaseModel


class AnswerWSSchema(BaseModel):
    ok: bool
    type: str
    detail: dict
