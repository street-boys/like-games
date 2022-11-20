from enum import Enum


class RegistrationTypeEnum(str, Enum):
    provided = "provided"
    telegram = "telegram"


class CardPositionEnum(str, Enum):
    deck = "deck"
    player = "player"
    table = "table"


class GameTypeEnum(str, Enum):
    texas = "texas"


class RoundTypeEnum(Enum):
    PREFLOP = 1
    FLOP = 2
    RIVER = 3
    TURN = 4
    SHOWDOWN = 5
