# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_type_table, get_phat_table

# ---------------------------- Message -----------------------------------

MessageBatchType = get_type_table(model_name='MessageBatch', table_name='message_batch')  # Email, Excel
