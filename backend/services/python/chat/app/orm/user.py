from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField
from tortoise.fields.relational import (ManyToManyField, ManyToManyRelation,
                                        ReverseRelation)


class UserModel(Model):
    id = BigIntField(pk=True)

    user_id = BigIntField(null=False, unique=True)

    messages: ReverseRelation
    chats: ManyToManyRelation = ManyToManyField(model_name='models.ChatModel',
                                                related_name='users')


user_schema_out = pydantic_model_creator(UserModel,
                                         name='UserSchemaOut')
