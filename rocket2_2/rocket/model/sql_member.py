# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_phat_table, get_type_table

# ********************* Member ***********************************#

columns_tbl_member = {
    '__tablename__': 'tbl_member',
    'person_id': common_columns.get('integer_unique_not_nullable')(),
    'register_date': common_columns.get('date_not_nullable')(),
    'external_id': common_columns.get('integer')()
}
Member = get_phat_table(model_name='Member', columndict=columns_tbl_member)

# ********************* Member Comment ***********************************#

columns_tbl_member_comment = {
    '__tablename__': 'tbl_member_comment',
    'member_id': common_columns.get('integer_not_nullable')(),
    'comment': common_columns.get('longtext_not_nullable')()
}
MemberComment = get_phat_table(model_name='MemberComment', columndict=columns_tbl_member_comment)

# ********************* Member Enrolment ***********************************#

columns_tbl_member_enrolment = {
    '__tablename__': 'tbl_member_enrolment',
    'member_id': common_columns.get('integer')(),
    'product_id': common_columns.get('integer')(),
    'reference': common_columns.get('description')(),
    'is_enroled': common_columns.get('boolean')()
}
MemberEnrolment = get_phat_table(model_name='MemberEnrolment', columndict=columns_tbl_member_enrolment)

columns_tbl_member_enrolment_lead = {
    '__tablename__': 'tbl_member_enrolment_lead',
    'member_enrolment_id': common_columns.get('integer')(),
    'lead_date': common_columns.get('datetime')(),
    'lead_by_id': common_columns.get('integer')()
}
MemberEnrolmentLead = get_phat_table(model_name='MemberEnrolmentLead', columndict=columns_tbl_member_enrolment_lead)

columns_tbl_member_enrolment_participant = {
    '__tablename__': 'tbl_member_enrolment_participant',
    'member_enrolment_id': common_columns.get('integer')(),
    'enrol_date': common_columns.get('datetime')(),
    'enrol_by_id': common_columns.get('integer')()
}
MemberEnrolmentPartipant = get_phat_table(model_name='MemberEnrolmentPartipant', columndict=columns_tbl_member_enrolment_participant)

# ********************* Member Family ***********************************#

columns_tbl_member_family = {
    '__tablename__': 'tbl_member_family',
    'member_id': common_columns.get('integer')(),
    'family_member_id': common_columns.get('integer')(),
    'relationship_type_id': common_columns.get('integer')()
}
MemberFamily = get_phat_table(model_name='MemberFamily', columndict=columns_tbl_member_family)

# ********************* Member Client ***********************************#

columns_tbl_member_client = {
    '__tablename__': 'tbl_member_client',
    'member_id': common_columns.get('integer')(),
    'client_id': common_columns.get('integer')()
}
MemberClient = get_phat_table(model_name='MemberClient', columndict=columns_tbl_member_client)

# ********************* Member Quote ***********************************#

columns_tbl_member_quote = {
    '__tablename__': 'tbl_member_quote',
    'member_id': common_columns.get('integer')(),
    'quote_by_id': common_columns.get('integer')(),
    'product_id': common_columns.get('integer')(),
    'total_premium': common_columns.get('currency')()
}
MemberQuote = get_phat_table(model_name='MemberQuote', columndict=columns_tbl_member_quote)

columns_tbl_member_quote_life_assured = {
    '__tablename__': 'tbl_member_quote_life_assured',
    'quote_id': common_columns.get('integer')(),
    'product_life_assured_id': common_columns.get('integer')(),
    'birthdate': common_columns.get('datetime')(),
    'gender_id': common_columns.get('integer')(),
    'percentage': common_columns.get('currency')(),
    'premium': common_columns.get('currency')(),
    'sum_assured': common_columns.get('currency')()
}
MemberQuoteLifeAssured = get_phat_table(model_name='MemberQuoteLifeAssured', columndict=columns_tbl_member_quote_life_assured)

columns_tbl_member_quote_life_assured_loader = {
    '__tablename__': 'tbl_member_quote_life_assured_loader',
    'quote_life_assured_id': common_columns.get('integer')(),
    'product_loader_link_id': common_columns.get('integer')(),
    'loader_question_answer_id': common_columns.get('integer')()
}
MemberQuoteLifeAssuredLoader = get_phat_table(model_name='MemberQuoteLifeAssuredLoader', columndict=columns_tbl_member_quote_life_assured_loader)
