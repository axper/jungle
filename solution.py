#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from random import randint

import names
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
import models

logging.basicConfig(level=logging.DEBUG)


def create_lion():
    """
    :return: A Lion model with random attributes, not saved to database
    """
    name = names.get_first_name()
    age = randint(config.AGE_MIN, config.AGE_MAX)
    hunger = randint(config.HUNGER_MIN, config.HUNGER_MAX)
    return models.Lion(name=name, age=age, hunger=hunger)


def create_hippopotamus():
    """
    :return: A Hippopotamus model with random attributes, not saved to database
    """
    name = names.get_first_name()
    age = randint(config.AGE_MIN, config.AGE_MAX)
    return models.Hippopotamus(name=name, age=age)


def create_antelope():
    """
    :return: An Antelope model with random attributes, not saved to database
    """
    name = names.get_first_name()
    age = randint(config.AGE_MIN, config.AGE_MAX)
    speed = randint(config.SPEED_MIN, config.SPEED_MAX)
    return models.Antelope(name=name, age=age, speed=speed)


def create_hyena():
    """
    :return: A Hyena model with random attributes, not saved to database
    """
    name = names.get_first_name()
    age = randint(config.AGE_MIN, config.AGE_MAX)
    return models.Hyena(name=name, age=age)


def add_random_animals_of_type_to_session(session, animal_creator_function, count):
    """
    Adds count instances of an animal created by animal_creator_function to SQLAlchemy session.

    :param session: SQLAlchemy session instance
    :param animal_creator_function: A function that accepts no arguments and returns an animal model
    :param count: How many instances of the animal to add to the session
    :return: None
    """
    for _ in xrange(count):
        animal = animal_creator_function()
        logging.info('Adding animal: {}'.format(animal))
        session.add(animal)


def main():
    engine = create_engine(config.DATABASE_URL, echo=False)
    logging.info('Created engine: {}'.format(engine))
    Session = sessionmaker(bind=engine)
    session = Session()
    logging.info('Created session: {}'.format(session))
    models.Base.metadata.create_all(engine)
    logging.info('Created database schema.')

    add_random_animals_of_type_to_session(session, create_lion, config.LION_COUNT)
    add_random_animals_of_type_to_session(session, create_hippopotamus, config.HIPPOPOTAMUS_COUNT)
    add_random_animals_of_type_to_session(session, create_antelope, config.ANTELOPE_COUNT)
    add_random_animals_of_type_to_session(session, create_hyena, config.HYENA_COUNT)

    session.commit()


if __name__ == '__main__':
    main()
