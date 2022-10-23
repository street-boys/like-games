from tortoise import Model
from tortoise.fields.data import BigIntField
from tortoise.fields.relational import (OneToOneRelation, ReverseRelation, OneToOneField)


class DeckModel(Model):
    id = BigIntField(pk=True)

    game: OneToOneRelation = OneToOneField(model_name='models.GameModel', related_name='deck')

    cards: ReverseRelation
