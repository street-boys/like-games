from tortoise import Model
from tortoise.fields.data import BigIntField, TextField
from tortoise.fields.relational import (ForeignKeyField, ForeignKeyRelation,
                                        OneToOneRelation, ReverseRelation)

from structures.enums import CardTypeEnum


class CardModel(Model):
    id = BigIntField(pk=True)

    rank = TextField()
    suit = TextField()
    type = BigIntField(default=CardTypeEnum.DECK.value)

    player = BigIntField(default=0)

    deck: ForeignKeyRelation = ForeignKeyField(model_name='models.DeckModel', related_name='cards')


class DeckModel(Model):
    id = BigIntField(pk=True)

    cards: ReverseRelation
    game: OneToOneRelation
