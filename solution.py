#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from random import randint

import names
from dijkstar import Graph, find_path, NoPathError
from sqlalchemy import func

import config
import models
from database import Session, engine

logging.basicConfig(level=config.LOGGING_LEVEL)


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


def can_become_friends(animal1, animal2):
    """
    Checks whether given 2 animals can be friends or not.

    Animals can be friends only if:
    1. They are not the same instance
    2. They are not already friends
    3. Each one of them has less than EACH_ANIMAL_MAX_FRIENDS other friends

    :param animal1: An animal instance
    :param animal2: An animal instance
    :return: True if they can be friends, False otherwise.
    """
    if animal1 == animal2:
        logging.info('Animal: {} cannot be friend of itself.'.format(animal1))
        return False
    if animal1 in animal2.friends or animal2 in animal1.friends:
        logging.info('Animals are already friends: {}, {}'.format(animal1, animal2))
        return False
    if len(animal1.friends) >= config.EACH_ANIMAL_MAX_FRIENDS:
        logging.info('Max friend count reached for: {}'.format(animal1))
        return False
    if len(animal2.friends) >= config.EACH_ANIMAL_MAX_FRIENDS:
        logging.info('Max friend count reached for: {}'.format(animal2))
        return False
    logging.debug('Animals can be friends: {}, {}'.format(animal1, animal2))
    return True


def get_hungriest_lion(session):
    """
    Finds the hungriest lion in the jungle.

    If there are multiple lions with same maximum hunger attribute, we pick the first random one.

    :param session: The SQLAlchemy session
    :return: The lion which has the biggest hunger attribute value.
    """
    return session.query(models.Lion, func.max(models.Lion.hunger)).all()[0][0]


def get_slowest_antelope(session):
    """
    Finds the slowest antelope in the jungle.

    If there are multiple antelopes with same minimum speed attribute, we pick the first random one.

    :param session: The SQLAlchemy session
    :return: The Antelope which has the smallest speed attribute value.
    """
    return session.query(models.Antelope, func.min(models.Antelope.speed)).all()[0][0]


# noinspection PyUnusedLocal
def get_cost(u, v, e, prev_e):
    """
    Gets the cost of graph traversal from point u to point v.

    We take into account only v's cost, which is determined by what type of animal v is.

    # TODO: Optimize this function if needed, currently we hit the db every time.

    :param u: from point, an animal instance
    :param v: to point, an animal instance
    :param e:
    :param prev_e:
    :return: a number indicating the cost of traversal
    """
    session = Session()
    animal = session.query(models.Animal).get(v)
    if animal.type == 'lion':
        return config.LION_COST
    elif animal.type == 'hippopotamus':
        return config.HIPPOPOTAMUS_COST
    elif animal.type == 'antelope':
        return config.ANTELOPE_COST
    elif animal.type == 'hyena':
        return config.HYENA_COST
    else:
        raise ValueError('Unhandled animal type: {}'.format(animal.type))


def main():
    session = Session()
    logging.info('Created session: {}'.format(session))
    models.Base.metadata.create_all(engine)
    logging.info('Created database schema.')

    add_random_animals_of_type_to_session(session, create_lion, config.LION_COUNT)
    add_random_animals_of_type_to_session(session, create_hippopotamus, config.HIPPOPOTAMUS_COUNT)
    add_random_animals_of_type_to_session(session, create_antelope, config.ANTELOPE_COUNT)
    add_random_animals_of_type_to_session(session, create_hyena, config.HYENA_COUNT)

    all_animals = session.query(models.Animal).all()

    friendship_count = 0
    while friendship_count < config.MAX_FRIENDSHIP_COUNT:
        random_animal_1 = all_animals[randint(0, len(all_animals) - 1)]
        random_animal_2 = all_animals[randint(0, len(all_animals) - 1)]
        if can_become_friends(random_animal_1, random_animal_2):
            logging.info('Creating friendship between: {}, {}'.format(random_animal_1, random_animal_2))
            random_animal_1.friends.append(random_animal_2)
            random_animal_2.friends.append(random_animal_1)
            session.add(random_animal_1)
            session.add(random_animal_2)
            friendship_count += 1

    session.commit()

    hungriest_lion = get_hungriest_lion(session)
    logging.info('Hungriest lion is: {}'.format(hungriest_lion))

    slowest_antelope = get_slowest_antelope(session)
    logging.info('Slowest antelope is: {}'.format(slowest_antelope))

    graph = Graph()
    for animal in all_animals:
        for friend in animal.friends:
            graph.add_edge(animal.id, friend.id)
    try:
        shortest_path = find_path(graph, hungriest_lion.id, slowest_antelope.id, cost_func=get_cost)
    except NoPathError:
        logging.warn('The lion stays hungry today')
    else:
        logging.info('Shortest path to slowest antelope is through animal ids: {}'.format(shortest_path[0]))


if __name__ == '__main__':
    main()
