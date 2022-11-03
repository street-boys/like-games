from tortoise import Model
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise.fields.data import BigIntField, BooleanField
from tortoise.fields.relational import (ForeignKeyField, ForeignKeyRelation,
                                        OneToOneField, OneToOneRelation)


class UserModel(Model):
    id = BigIntField(pk=True)

    user_id = BigIntField(null=False, unique=True)

    player: OneToOneRelation


user_schema_out = pydantic_model_creator(UserModel,
                                         name='UserSchemaOut',
                                         exclude=('player',))


class PlayerModel(Model):
    id = BigIntField(pk=True)

    game_chips = BigIntField(default=0)

    in_game_order = BigIntField(default=0)

    last_bet = BigIntField(default=0)
    round_bet = BigIntField(default=0)

    is_allin = BooleanField(default=False)
    is_folded = BooleanField(default=False)

    user: OneToOneRelation = OneToOneField(model_name='models.UserModel', related_name='player')

    game: ForeignKeyRelation = ForeignKeyField(model_name='models.GameModel', related_name='players')


player_schema_out = pydantic_model_creator(PlayerModel,
                                           name='PlayerSchemaOut',
                                           exclude=('user', 'game',))
