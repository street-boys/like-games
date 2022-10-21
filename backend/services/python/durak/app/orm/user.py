from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField
from tortoise.fields.relational import (ForeignKeyField, ForeignKeyRelation,
                                        OneToOneField, OneToOneRelation,
                                        ReverseRelation)


class UserModel(Model):
    id = BigIntField(pk=True)

    user_id = BigIntField(null=False, unique=True)

    player: OneToOneRelation


user_schema_out = pydantic_model_creator(UserModel,
                                         name='UserSchemaOut')


class PlayerModel(Model):
    id = BigIntField(pk=True)

    in_game_order = BigIntField(default=0)

    user: OneToOneRelation = OneToOneField(model_name='models.UserModel', related_name='player')

    game: ForeignKeyRelation = ForeignKeyField(model_name='models.GameModel', related_name='players')
