from structures.constants import CARD_RANK_52, CARD_SUIT


class Rank:
    def __init__(self, value: str) -> None:
        if value not in CARD_RANK_52:
            raise ValueError
        self.value = value

    def __str__(self) -> str:
        return self.value.upper()


class Suit:
    def __init__(self, value: str) -> None:
        if value not in CARD_SUIT:
            raise ValueError
        self.value = value

    def __str__(self) -> str:
        return self.value.lower()


class Card:
    def __init__(self, rank: Rank, suit: Suit) -> None:
        self.rank = rank
        self.suit = suit

    def __str__(self) -> str:
        return f'{self.rank}{self.suit}'
