"""
We are using joined table inheritance here because Antelopes and Lions have additional attributes.
Even though hippos and hyenas don't add new attributes, they might in the future.

Joined table inheritance docs: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#joined-table-inheritance
"""
from sqlalchemy import Column, Integer, String, ForeignKey
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
    id = Column(Integer, ForeignKey('animal.id'), primary_key=True)
    hunger = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'lion',
    }


# noinspection PyClassHasNoInit
class Hippopotamus(Animal):
    __tablename__ = 'hippopotamus'
    id = Column(Integer, ForeignKey('animal.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'hippopotamus',
    }


# noinspection PyClassHasNoInit
class Antelope(Animal):
    __tablename__ = 'antelope'
    id = Column(Integer, ForeignKey('animal.id'), primary_key=True)
    speed = Column(Integer, nullable=False)

    __mapper_args__ = {
        'polymorphic_identity': 'antelope',
    }


# noinspection PyClassHasNoInit
class Hyena(Animal):
    __tablename__ = 'hyena'
    id = Column(Integer, ForeignKey('animal.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'hyena',
    }
