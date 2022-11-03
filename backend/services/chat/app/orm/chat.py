from tortoise import Model
from tortoise.fields.data import BigIntField, CharEnumField
from tortoise.fields.relational import ReverseRelation

from structures.enums import ChatTypeEnum


class ChatModel(Model):
    id = BigIntField(pk=True)

    chat_type = CharEnumField(enum_type=ChatTypeEnum, default=ChatTypeEnum.public)

    messages: ReverseRelation
    users: ReverseRelation

    class Meta:
        ordering = ["id"]
