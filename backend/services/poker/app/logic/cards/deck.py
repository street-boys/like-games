from random import shuffle

from logic.cards.card import Card, Rank, Suit
from structures.constants import CARD_RANK_52, CARD_SUIT
from structures.enums import DeckTypeEnum


class Deck:
    cards: list[Card] = None

    def __init__(self, deck_type: DeckTypeEnum) -> None:
        self._build(deck_type)

    def shuffle(self) -> None:
        shuffle(self.cards)

    def _give_one_card(self) -> None:
        card_to_give = self.cards.pop(0)
        self.cards.append(card_to_give)

        return card_to_give

    def give_cards(self, count: int) -> list[Card]:
        if count >= len(self.cards):
            raise RuntimeError
        return [self._give_one_card() for _ in range(count)]

    def _build(self, deck_type: DeckTypeEnum) -> None:
        match deck_type:
            case DeckTypeEnum.deck_52:
                self.cards = self.__generate_cards_from(ranks=CARD_RANK_52)

    @staticmethod
    def __generate_cards_from(ranks: set[str]) -> list[Card]:
        return [Card(rank=Rank(rank), suit=Suit(suit)) for suit in CARD_SUIT for rank in ranks]
