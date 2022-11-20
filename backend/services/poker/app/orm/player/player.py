from sqlalchemy import Boolean, Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class PlayerModel(Base):
    id = Column(Integer, primary_key=True)

    game_chips = Column(Integer, default=0)

    in_game_order = Column(Integer, default=0)

    last_bet = Column(Integer, default=0)
    round_bet = Column(Integer, default=0)

    is_allin = Column(Boolean, default=False)
    is_folded = Column(Boolean, default=False)

    user_id = Column(Integer, ForeignKey("usermodel.id"))
    user = relationship("UserModel", back_populates="player")
