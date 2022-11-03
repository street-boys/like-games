from enum import Enum


class FilterEnum(str, Enum):
    id = 'id'
    user_id = 'user_id'


class CardTypeEnum(Enum):
    DECK = 1
    PLAYER = 2
    TABLE = 3


class DeckTypeEnum(Enum):
    deck_52 = 1


class GameStateEnum(Enum):
    WAIT_FOR_PLAYERS = 1
    WAIT_FOR_BET = 2
    WAIT_FOR_FIND_WINNER = 3


class RoundTypeEnum(Enum):
    PREFLOP = 1
    FLOP = 2
    RIVER = 3
    TURN = 4
    SHOWDOWN = 5
