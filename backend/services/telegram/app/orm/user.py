from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class UserModel(Base):
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, unique=True)

    bonus = relationship("BonusModel", back_populates="user")
