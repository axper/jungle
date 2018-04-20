#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
We are using joined table inheritance here because Antelopes and Lions have additional attributes.
Even though hippos and hyenas don't add new attributes, they might in the future.

Joined table inheritance docs: http://docs.sqlalchemy.org/en/latest/orm/inheritance.html#joined-table-inheritance

Friends == Acquaintances. The word Acquaintances is hard to type and say so I use the word Friends throughout the code.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Table, CheckConstraint, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy_repr import RepresentableBase

Base = declarative_base(cls=RepresentableBase)

friend_table = Table(
    'friend', Base.metadata,
    Column('left_id', Integer, ForeignKey('animal.id')),
    Column('right_id', Integer, ForeignKey('animal.id')),
    CheckConstraint('left_id != right_id', name='cannot_befriend_self_constraint'),
    UniqueConstraint('left_id', 'right_id', name='can_be_friends_only_once_constraint')
)


# noinspection PyClassHasNoInit
class Animal(Base):
    __tablename__ = 'animal'
    id = Column(Integer, primary_key=True)
    type = Column(String, nullable=False)
    name = Column(String, nullable=False)
    age = Column(Integer, nullable=False)
    friends = relationship('Animal',
                           secondary=friend_table,
                           primaryjoin=friend_table.c.left_id == id,
                           secondaryjoin=friend_table.c.right_id == id)

    __table_args__ = (
        # TODO: Add constraint here for max friend count, see: https://stackoverflow.com/q/49935712/2529583
        # CheckConstraint(func.count(friends) < 10, name='max_friends_constraint'),
    )
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
