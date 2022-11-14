from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship

from db.base import Base


class BonusModel(Base):
    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("usermodel.id"))
    user = relationship("UserModel", back_populates="bonus")

    delay_hours = Column(Integer, default=4)  # 14400 seconds
    last_taken_bonus = Column(DateTime, default=None, nullable=True)

    bonus = Column(Integer, default=15000)
