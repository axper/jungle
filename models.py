"""
We are using joined table inheritance here because Antelopes and Lions have additional attributes.
Even though hippos and hyenas don't add new attributes, they might in the future.

Joined table inheritance docs: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#joined-table-inheritance
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# noinspection PyClassHasNoInit
class Animal(Base):
    __tablename__ = 'animal'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'animal',
        'polymorphic_on': type
    }


# noinspection PyClassHasNoInit
class Lion(Animal):
    __tablename__ = 'lion'
    hunger = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'lion',
    }


# noinspection PyClassHasNoInit
class Hippopotamus(Animal):
    __tablename__ = 'hippopotamus'

    __mapper_args__ = {
        'polymorphic_identity': 'hippopotamus',
    }


# noinspection PyClassHasNoInit
class Antelope(Animal):
    __tablename__ = 'antelope'
    speed = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'antelope',
    }


# noinspection PyClassHasNoInit
class Hyena(Animal):
    __tablename__ = 'hyena'

    __mapper_args__ = {
        'polymorphic_identity': 'hyena',
    }
