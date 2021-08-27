"""DataBase models."""
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PlusItem(Base):
    """Items plus."""

    __tablename__ = 'plus_items'

    id = Column(Integer, primary_key=True)

    url = Column(Text)
    discription = Column(Text)
    image_url = Column(Text)
