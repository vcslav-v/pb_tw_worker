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


class PremiumItem(Base):
    """Items premium."""

    __tablename__ = 'premium_items'

    id = Column(Integer, primary_key=True)

    url = Column(Text)
    discription = Column(Text)
    image_url = Column(Text)


class Cookie(Base):
    """Cookie."""

    __tablename__ = 'cookies'

    id = Column(Integer, primary_key=True)

    domain = Column(Text)
    data = Column(Text)


class PostedTDarticle(Base):
    """Posted TD articles."""

    __tablename__ = 'posted_td_articles'

    id = Column(Integer, primary_key=True)

    url = Column(Text, unique=True)