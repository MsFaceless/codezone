# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_phat_table, get_type_table

# ********************* Claim ***********************************#

columns_tbl_claim = {
    '__tablename__': 'tbl_claim',
    'capture_date': common_columns.get('date')(),
    'cover_and_exclusion_type_id': common_columns.get('integer_not_nullable')(),
    }
Claim = get_phat_table(model_name='Claim', columndict=columns_tbl_claim)

columns_tbl_claim_claimant = {
    '__tablename__': 'tbl_claim_claimant',
    'claim_id': common_columns.get('integer_not_nullable')(),
    'person_id': common_columns.get('integer_not_nullable')(),
    }
ClaimClaimant = get_phat_table(model_name='ClaimClaimant', columndict=columns_tbl_claim_claimant)

# ********************* Claim Status ***********************************#

ClaimStatusType = get_type_table(model_name='ClaimStatus', table_name='claim_status')

columns_tbl_claim_status = {
    '__tablename__': 'tbl_claim_status',
    'claim_id': common_columns.get('integer_not_nullable')(),
    'claim_status_reason_id': common_columns.get('integer_not_nullable')(),
    'comment': common_columns.get('description')(),
    'current_status': common_columns.get('boolean')(),
    }
ClaimStatus = get_phat_table(model_name='ClaimStatus', columndict=columns_tbl_claim_status)

columns_tbl_claim_status_reason = {
    '__tablename__': 'tbl_claim_status_reason',
    'claim_status_type_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('title')(),
    }
ClaimStatusReason = get_phat_table(model_name='ClaimStatusReason', columndict=columns_tbl_claim_status_reason)


# ********************* Claim Document ***********************************#

columns_tbl_claim_document = {
    '__tablename__': 'tbl_claim_document',
    'claim_id': common_columns.get('integer_not_nullable')(),
    'document_repository_id': common_columns.get('integer_not_nullable')(),
    }
ClaimDocument = get_phat_table(model_name='ClaimDocument', columndict=columns_tbl_claim_document)

# ********************* Claim Policy ***********************************#

columns_tbl_claim_policy_beneficiary = {
    '__tablename__': 'tbl_claim_policy_beneficiary',
    'claim_policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'policy_beneficiary_id': common_columns.get('integer_not_nullable')(),
    }
ClaimPolicyBeneficiary = get_phat_table(model_name='ClaimPolicyBeneficiary', columndict=columns_tbl_claim_policy_beneficiary)

columns_tbl_claim_policy_benefit = {
    '__tablename__': 'tbl_claim_policy_benefit',
    'claim_id': common_columns.get('integer_not_nullable')(),
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    }
ClaimPolicyBenefit = get_phat_table(model_name='ClaimPolicyBenefit', columndict=columns_tbl_claim_policy_benefit)

# ********************* Claim Payout ***********************************#

ClaimPayoutAllocationType = get_type_table(model_name='ClaimPayoutAllocation', table_name='claim_payout_allocation')

columns_tbl_claim_payout_schedule = {
    '__tablename__': 'tbl_claim_payout_schedule',
    'claim_payout_allocation_type_id': common_columns.get('integer_not_nullable')(),
    'claim_policy_beneficiary_id': common_columns.get('integer_not_nullable')(),
    'due_date': common_columns.get('date')(),
    'amount': common_columns.get('currency')(),
    }
ClaimPayoutSchedule = get_phat_table(model_name='ClaimPayoutSchedule', columndict=columns_tbl_claim_payout_schedule)
