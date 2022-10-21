from tortoise import Model
from tortoise.fields.data import BigIntField, IntField
from tortoise.fields.relational import OneToOneRelation, ReverseRelation

from structures.enums import GameStateEnum


class GameModel(Model):
    id = BigIntField(pk=True)

    chat_id = BigIntField(default=0)

    state = IntField(default=GameStateEnum.WAIT_FOR_PLAYERS.value)

    player = BigIntField(default=0)

    players: ReverseRelation

    deck: OneToOneRelation
