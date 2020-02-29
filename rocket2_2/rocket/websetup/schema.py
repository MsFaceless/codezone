# -*- coding: utf-8 -*-
"""Setup the rocket application"""
from __future__ import print_function

from tg import config
import transaction


def setup_schema(command, conf, vars):
    """Place any commands to setup rocket here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from rocket import model
    # <websetup.websetup.schema.after.model.import>

    # <websetup.websetup.schema.before.metadata.create_all>
    print("Creating tables")
    model.metadata.create_all(bind=config['tg.app_globals'].sa_engine)
    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()
