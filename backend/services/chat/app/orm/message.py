from tortoise import Model
from tortoise.contrib.pydantic import pydantic_queryset_creator, pydantic_model_creator
from tortoise.fields.data import BigIntField, TextField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation


class MessageModel(Model):
    id = BigIntField(pk=True)

    text = TextField(null=False)

    message_from: ForeignKeyRelation = ForeignKeyField(model_name='models.UserModel',
                                                       related_name='messages')

    chat: ForeignKeyRelation = ForeignKeyField(model_name='models.ChatModel',
                                               related_name='messages')


message_schema_out = pydantic_model_creator(MessageModel,
                                            name='MessageSchemaOut')
messages_schema_out = pydantic_queryset_creator(MessageModel,
                                                name='MessagesSchemaOut')
