#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config
from models import Base

logging.basicConfig(level=logging.DEBUG)

engine = create_engine(config.DATABASE_URL, echo=False)
logging.info('Created engine: {}'.format(engine))
Session = sessionmaker(bind=engine)
session = Session()
logging.info('Created session: {}'.format(session))
Base.metadata.create_all(engine)
logging.info('Created database schema.')
