from sqlalchemy import Integer, Column, String, Enum

from db.base import Base
from structures.enums import CardTypeEnum


class CardModel(Base):
    id = Column(Integer, primary_key=True)

    rank = Column(String)
    suit = Column(String)
    type = Column(Enum(CardTypeEnum), default=CardTypeEnum.deck)
