from tortoise import Model
from tortoise.fields.data import BigIntField, BooleanField, TextField
from tortoise.fields.relational import ForeignKeyField, ForeignKeyRelation

from structures.enums import CardTypeEnum


class CardModel(Model):
    id = BigIntField(pk=True)

    rank = TextField()
    suit = TextField()

    trump = BooleanField(default=False)

    killed = BooleanField(default=False)
    killed_by_card = BigIntField(default=0)

    deck: ForeignKeyRelation = ForeignKeyField(model_name='models.DeckModel', related_name='cards')

    card_type = BigIntField(default=CardTypeEnum.deck.value)

    player_id = BigIntField(default=0)
