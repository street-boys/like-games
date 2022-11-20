from random import shuffle

from schemas.game import CardSchema, DeckSchema
from structures.constants import CARD_RANK, CARD_SUIT


class DeckAccessor:
    def __generate_deck(self) -> list[CardSchema]:
        to_return: list[CardSchema] = []
        for suit in CARD_SUIT:
            for rank in CARD_RANK:
                to_return.append(CardSchema(rank=rank, suit=suit))

        return to_return

    def make_deck(self, with_shuffle: bool = False) -> DeckSchema:
        to_return = DeckSchema(deck=self.__generate_deck())

        if with_shuffle:
            shuffle(to_return.deck)

        return to_return

    def __take_one_card(self, deck: DeckSchema) -> CardSchema:
        card_to_give = deck.deck.pop(0)
        deck.deck.append(card_to_give)

        return card_to_give

    def take_cards(self, deck: DeckSchema, number: int) -> list[CardSchema]:
        if number >= len(deck.deck):
            raise RuntimeError

        return [self.__take_one_card(deck=deck) for _ in range(number)]
