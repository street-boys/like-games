from sqlalchemy import BigInteger, Column, Integer

from db.base import Base


class PotModel(Base):
    id = Column(Integer, primary_key=True)

    user_id = Column(Integer, unique=True, nullable=False)

    pot = Column(BigInteger, default=15000)
