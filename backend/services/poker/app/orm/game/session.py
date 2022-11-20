from sqlalchemy import Column, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class SessionModel(Base):
    id = Column(Integer, primary_key=True)

    game_id = Column(Integer, ForeignKey("gamemodel.id"))
    game = relationship("GameModel", back_populates="sessions")
