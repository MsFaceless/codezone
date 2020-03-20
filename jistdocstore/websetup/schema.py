# -*- coding: utf-8 -*-
"""Setup the jistdocstore application"""
from __future__ import print_function

import logging
from tg import config
import transaction

def setup_schema(command, conf, vars):
    """Place any commands to setup jistdocstore here"""
    # Load the models

    # <websetup.websetup.schema.before.model.import>
    from jistdocstore import model
    # <websetup.websetup.schema.after.model.import>

    
    # <websetup.websetup.schema.before.metadata.create_all>
    print("Creating tables")
    #model.metadata.create_all(bind=config['tg.app_globals'].sa_engine)
    model.metadata.create_all(bind=config['tg.app_globals'].sa_engine)
    model.metadata.create_all(bind=config['tg.app_globals'].sa_engine_first)
    model.metadata2.create_all(bind=config['tg.app_globals'].sa_engine_second)
    model.metadata3.create_all(bind=config['tg.app_globals'].sa_engine_third)
    model.metadata4.create_all(bind=config['tg.app_globals'].sa_engine_fourth)
    model.metadata5.create_all(bind=config['tg.app_globals'].sa_engine_fifth)
    model.metadata7.create_all(bind=config['tg.app_globals'].sa_engine_seven)
    model.metadata8.create_all(bind=config['tg.app_globals'].sa_engine_eight)
    model.metadata9.create_all(bind=config['tg.app_globals'].sa_engine_nine)
    model.metadata6.create_all(bind=config['tg.app_globals'].sa_engine_six)
    model.metadata10.create_all(bind=config['tg.app_globals'].sa_engine_ten)
    model.metadata11.create_all(bind=config['tg.app_globals'].sa_engine_eleven)
    model.metadata12.create_all(bind=config['tg.app_globals'].sa_engine_twelve)
    model.metadata13.create_all(bind=config['tg.app_globals'].sa_engine_thirteen)
    # <websetup.websetup.schema.after.metadata.create_all>

    # <websetup.websetup.schema.after.metadata.create_all>
    transaction.commit()
    #print('Initializing Migrations')
    #import alembic.config, alembic.command
    #alembic_cfg = alembic.config.Config()
    #alembic_cfg.set_main_option("script_location", "migration")
    #alembic_cfg.set_main_option("sqlalchemy.url", config['sqlalchemy.url'])
    #alembic.command.stamp(alembic_cfg, "head")
