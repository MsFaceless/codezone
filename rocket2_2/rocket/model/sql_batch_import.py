# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_phat_table, get_type_table

# ********************* Batch Import ***********************************#

BatchImportType = get_type_table(model_name='BatchImport', table_name='batch_import')

columns_tbl_batch_import = {
    '__tablename__': 'tbl_batch_import',
    'import_type_id': common_columns.get('integer_not_nullable')(),
    'filename': common_columns.get('description_not_nullable')(),
    'processed': common_columns.get('datetime')(),
    'total_count': common_columns.get('integer')(),
    'accepted_count': common_columns.get('integer')(),
    #pre_purchase_count: common_columns.get('integer_default')(0), # Ask Directors if this functionality is required ???? 14 Jan 2020 Trevor
    'rejected_count': common_columns.get('integer')(),
    'notes': common_columns.get('description_not_nullable')(),
    #'is_complete_load': common_columns.get('boolean_default_false')(),
    #'is_complete_update': common_columns.get('boolean_default_false')(),
    #'is_successful': common_columns.get('boolean_default_false')(),
    }
BatchImport = get_phat_table(model_name='BatchImport', columndict=columns_tbl_batch_import)

columns_tbl_batch_import_audit = {
    '__tablename__': 'tbl_batch_import_audit',
    'batch_import_id': common_columns.get('integer_not_nullable')(),
    'audit_date_time': common_columns.get('datetime')(), #: common_columns.get('datetime_default_now')(),
    'audit': common_columns.get('description_not_nullable')(),
    }
BatchImportAudit = get_phat_table(model_name='BatchImportAudit', columndict=columns_tbl_batch_import_audit)

columns_tbl_batch_import_error = {
    '__tablename__': 'tbl_batch_import_error',
    'batch_import_id': common_columns.get('integer_not_nullable')(),
    'message': common_columns.get('longtext_not_nullable')(),
    }
BatchImportError = get_phat_table(model_name='BatchImportError', columndict=columns_tbl_batch_import_error)

# ********************* Member Request ***********************************#

columns_tbl_member_request = {
    '__tablename__': 'tbl_member_request',
    'batch_import_id': common_columns.get('integer_not_nullable')(),
    'identity_number': common_columns.get('description_not_nullable')(),
    'first_name': common_columns.get('description_not_nullable')(),
    'surname': common_columns.get('description_not_nullable')(),
    'mobile': common_columns.get('description_not_nullable')(),
    'intermediary_code': common_columns.get('code')(),
    'gender': common_columns.get('description')(),
    'gender_type_id': common_columns.get('integer')(),
    'date_of_birth': common_columns.get('date')(),
    'language_type_id': common_columns.get('integer')(),
    'startdate': common_columns.get('date')(),
    'beneficiary_identity_number': common_columns.get('description')(),
    'beneficiary_first_name': common_columns.get('description')(),
    'beneficiary_surname': common_columns.get('description')(),
    'beneficiary_mobile': common_columns.get('description')(),
    'beneficiary_date_of_birth': common_columns.get('date')(),
    'group_reference': common_columns.get('description')(),
    'client_code': common_columns.get('code')(),
    'client_id': common_columns.get('integer')(),
    }
MemberRequest = get_phat_table(model_name='MemberRequest', columndict=columns_tbl_member_request)

columns_tbl_batch_import_entity_person_link = {
    '__tablename__': 'tbl_batch_import_entity_person_link',
    'batch_import_id': common_columns.get('integer_not_nullable')(),
    'entity_person_id': common_columns.get('integer_not_nullable')(),
}
BatchImportEntityPersonLink = get_phat_table(model_name='BatchImportEntityPersonLink', columndict=columns_tbl_batch_import_entity_person_link)

# ********************* Policy Request ***********************************#

columns_tbl_policy_request = {
    '__tablename__': 'tbl_policy_request',
    'batch_import_id': common_columns.get('integer_not_nullable')(),
    'identity_number': common_columns.get('description_not_nullable')(),
    'product_code': common_columns.get('code_not_nullable')(),
    'purchase_date': common_columns.get('date')(), #: common_columns.get('date_not_nullable')(),
    }
PolicyRequest = get_phat_table(model_name='PolicyRequest', columndict=columns_tbl_policy_request)

columns_tbl_batch_import_policy = {
    '__tablename__': 'tbl_batch_import_policy',
    'batch_import_id': common_columns.get('integer_not_nullable')(),
    'policy_id': common_columns.get('integer_not_nullable')(),
}
BatchImportPolicy = get_phat_table(model_name='BatchImportPolicy', columndict=columns_tbl_batch_import_policy)
