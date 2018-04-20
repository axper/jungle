#!/usr/bin/env python
# -*- coding: utf-8 -*-
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import config

engine = create_engine(config.DATABASE_URL, echo=False)
Session = sessionmaker(bind=engine)
