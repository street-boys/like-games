from typing import Any

from logic.cards.card import Card
from orm.card import CardModel
from orm.deck import DeckModel
from orm.game import GameModel
from structures.enums import CardTypeEnum
from structures.named_tuples import attribute


async def create_card(card: Card,
                      deck: DeckModel,
                      player_id: int) -> CardModel:
    card = await CardModel.get_or_create(rank=card.rank.value, suit=card.suit.value,
                                         deck=deck, player_id=player_id)

    return card[0]


async def create_deck(game: GameModel) -> DeckModel:
    deck = await DeckModel.get_or_create(game=game)

    return deck[0]


async def update_card(card: CardModel,
                      data: dict) -> None:
    await card.update_from_dict(data=data)
    await card.save()


async def get_card_by(attr: attribute, value: Any) -> CardModel:
    __filter = {
        attr.filter.name: value
    }

    pot = await CardModel.get_or_none(**__filter)

    return pot


def is_on_table(card: CardModel) -> bool:
    return card.card_type == CardTypeEnum.table


async def get_player_cards(player_id: int) -> list[CardModel]:
    cards = await CardModel.filter(player_id=player_id,
                                   card_type=CardTypeEnum.hand.value)

    return cards


async def get_player_cards_count(player_id: int) -> int:
    count = await CardModel.filter(player_id=player_id,
                                   card_type=CardTypeEnum.hand.value).count()

    return count


async def get_deck_cards_count(deck: DeckModel) -> int:
    count = await deck.cards.all().filter(card_type=CardTypeEnum.deck.value).count()

    return count


def is_player_card(player_id: int,
                   card: CardModel):
    return card.card_type == CardTypeEnum.hand.value and card.player_id == player_id


async def get_table_cards(game: GameModel) -> list[CardModel]:
    cards = await CardModel.filter(deck=game.deck,
                                   card_type=CardTypeEnum.table.value)

    return cards
