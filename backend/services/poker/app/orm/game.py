from tortoise import Model
from tortoise.fields.data import BigIntField, BooleanField, IntField
from tortoise.fields.relational import OneToOneRelation, ReverseRelation

from structures.enums import GameStateEnum, RoundTypeEnum


class GameModel(Model):
    id = BigIntField(pk=True)

    max_players = IntField(default=9)

    state = IntField(default=GameStateEnum.WAIT_FOR_PLAYERS.value)

    current_player = BigIntField(default=0)

    dealer_player = BigIntField(default=0)
    small_blind_player = BigIntField(default=0)
    big_blind_player = BigIntField(default=0)

    chips_to_join = BigIntField(default=10000)

    small_blind = BigIntField(default=50)

    round = IntField(default=RoundTypeEnum.PREFLOP.value)

    last_bet = BigIntField(default=0)

    pot = BigIntField(default=0)

    all_player = BooleanField(default=False)

    players: ReverseRelation

    deck: OneToOneRelation
