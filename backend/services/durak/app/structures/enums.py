from enum import Enum


class FilterEnum(str, Enum):
    id = 'id'
    user_id = 'user_id'


class DeckTypeEnum(Enum):
    deck_52 = 1
    deck_36 = 2


class CardTypeEnum(Enum):
    deck = 1
    hand = 2
    table = 3
    trash = 4


class GameStateEnum(Enum):
    WAIT_FOR_PLAYERS = 1
    WAIT_FOR_READY = 2
    WAIT_FOR_PLAYER_ACTION = 3
    WAIT_FOR_ANY_ACTION = 4
