from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends
from starlette import status

from accessors.card import create_deck, create_card, get_player_cards
from accessors.game import get_game_by
from accessors.user import get_user_by, get_player_by
from accessors.integration.users import get_user_request
from logic.cards.card import Card
from logic.cards.deck import Deck
from responses.okay import okay_response
from schemas.integration.user import UserSchema
from structures.enums import FilterEnum, DeckTypeEnum, CardTypeEnum
from structures.named_tuples import attribute

card_router = APIRouter()


@card_router.get(path='.cards.me')
async def me_cards(user: UserSchema = Depends(get_user_request)) -> dict:
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    player = await get_player_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not player:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='not in game')
    cards = await get_player_cards(player_id=player.id)
    return okay_response(detail={
        'cards': cards
    })


@card_router.get(path='.add.cards')
async def add(user: UserSchema = Depends(get_user_request)):
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    player = await get_player_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not player:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='not in game')
    game = await get_game_by(attr=attribute(FilterEnum.id), value=1)
    deck = await create_deck(game=game)

    async for card in deck.cards:
        await card.update_from_dict({
            'player_id': 0,
            'card_type': CardTypeEnum.deck.value
        })
        await card.save()
    return await deck.cards


@card_router.get(path='.some')
async def some(user: UserSchema = Depends(get_user_request)):
    user = await get_user_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='user not found')
    player = await get_player_by(attr=attribute(FilterEnum.user_id), value=user.id)
    if not player:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail='not in game')
    game = await get_game_by(attr=attribute(FilterEnum.id), value=1)

    deck = await create_deck(game=game)
    d = Deck(deck_type=DeckTypeEnum.deck_36)

    for card in d.cards:
        await create_card(card=card,
                          deck=deck,
                          player_id=0)

    return await deck.cards
