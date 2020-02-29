# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_type_table, get_phat_table

# ---------------------------- Currency -----------------------------------

columns_tbl_currency = {
    '__tablename__': 'tbl_currency',
    'code': common_columns.get('title_not_nullable')(),
    'name': common_columns.get('title_not_nullable')(),
    'is_home_currency': common_columns.get('boolean_default_false')()
}
Currency = get_phat_table(model_name='Currency', columndict=columns_tbl_currency)

columns_tbl_language = {
    '__tablename__': 'tbl_language',
    'code': common_columns.get('title_not_nullable')(),
    'name': common_columns.get('title_not_nullable')()
}
Language = get_phat_table(model_name='Language', columndict=columns_tbl_language)

columns_tbl_mail_merge = {
    '__tablename__': 'tbl_mail_merge',
    'code': common_columns.get('title_not_nullable')(),
    'name': common_columns.get('title_not_nullable')()
}
MailMerge = get_phat_table(model_name='MailMerge', columndict=columns_tbl_mail_merge)

MailOptionType = get_type_table(model_name='MailOption', table_name='mail_option')
BillingFrequencyType =get_type_table(model_name='BillingFrequency', table_name='billing_frequency')

AddressType = get_type_table(model_name='Address', table_name='address')
ContactType = get_type_table(model_name='Contact', table_name='contact')
PersonIdentityType = get_type_table(model_name='PersonIdentity', table_name='person_identity')
PersonGenderType =get_type_table(model_name='PersonGender', table_name='person_gender')
PersonTitleType =get_type_table(model_name='PersonTitle', table_name='person_title')

# ********************* Bank ***********************************#

BankAccountType =get_type_table(model_name='BankAccount', table_name='bank_account')

columns_tbl_bank = {
    '__tablename__': 'tbl_bank',
    'name': common_columns.get('title_not_nullable')()
}
Bank = get_phat_table(model_name='Bank', columndict=columns_tbl_bank)

# ********************* Location ***********************************#

columns_tbl_country = {
    '__tablename__': 'tbl_country',
    'code': common_columns.get('title_not_nullable')(),
    'name': common_columns.get('title_not_nullable')()
}
Country = get_phat_table(model_name='Country', columndict=columns_tbl_country)

columns_tbl_region = {
    '__tablename__': 'tbl_region',
    'country_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('title_not_nullable')()
}
Region = get_phat_table(model_name='Region', columndict=columns_tbl_region)

columns_tbl_district = {
    '__tablename__': 'tbl_district',
    'region_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('title_not_nullable')()
}
District = get_phat_table(model_name='District', columndict=columns_tbl_district)

columns_tbl_centre = {
    '__tablename__': 'tbl_centre',
    'district_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('title_not_nullable')()
}
Centre = get_phat_table(model_name='Centre', columndict=columns_tbl_centre)
