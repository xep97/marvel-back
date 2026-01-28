from sqlalchemy import Column, String
from db import Base

class HeroDB(Base):
    __tablename__ = "heroes"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    alter_ego = Column(String, nullable=False)
    power = Column(String, nullable=False)
    team = Column(String, nullable=False)

    