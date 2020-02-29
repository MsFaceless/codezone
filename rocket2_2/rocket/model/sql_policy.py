# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_phat_table, get_type_table

# ********************* Policy ***********************************#

PolicyType = get_type_table(model_name='Policy', table_name='policy')
PolicyDateType = get_type_table(model_name='PolicyDate', table_name='policy_date')

columns_tbl_policy = {
    '__tablename__': 'tbl_policy',
    'policy_number': common_columns.get('title_not_nullable')(),
    'policy_type_id' : common_columns.get('integer_not_nullable')(),
    'product_id' : common_columns.get('integer_not_nullable')(),
    'entity_insured_id' : common_columns.get('integer_not_nullable')(),
    'entity_policy_owner_id' : common_columns.get('integer')(),
    'application_form_serial_no' : common_columns.get('title')(),
    }
Policy = get_phat_table(model_name='Policy', columndict=columns_tbl_policy)

columns_tbl_policy_intermediary_link = {
    '__tablename__': 'tbl_policy_intermediary_link',
    'policy_id' : common_columns.get('integer_not_nullable')(),
    'entity_organisation_intermediary_id' : common_columns.get('integer_not_nullable')(),
    'entity_organisation_intermediary_agent_id' : common_columns.get('integer')(),
    }
PolicyIntermediaryLink = get_phat_table(model_name='PolicyIntermediaryLink', columndict=columns_tbl_policy_intermediary_link)

columns_tbl_policy_date = {
    '__tablename__': 'tbl_policy_date',
    'policy_id': common_columns.get('percentage')(),
    'policy_date_type_id': common_columns.get('integer_not_nullable')(),
    'date': common_columns.get('date')(),
    }
PolicyDate = get_phat_table(model_name='PolicyDate', columndict=columns_tbl_policy_date)

# ********************* Policy State ***********************************#

PolicyStateType = get_type_table(model_name='PolicyState', table_name='policy_state')

columns_tbl_policy_state = {
    '__tablename__': 'tbl_policy_state',
    'policy_id' : common_columns.get('integer_not_nullable')(),
    'policy_state_type_id' : common_columns.get('integer_not_nullable')(),
    'datetime' : common_columns.get('datetime_default_now')(),
    }
PolicyState = get_phat_table(model_name='PolicyState', columndict=columns_tbl_policy_state)

# ********************* Policy History ***********************************#

columns_tbl_policy_history = {
    '__tablename__': 'tbl_policy_history',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'previous_policy_id': common_columns.get('integer_not_nullable')(),
    }
PolicyHistory = get_phat_table(model_name='PolicyHistory', columndict=columns_tbl_policy_history)

# ********************* Policy Beneficiary ***********************************#

columns_tbl_policy_beneficiary = {
    '__tablename__': 'tbl_policy_beneficiary',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'entity_person_id': common_columns.get('integer_not_nullable')(), # Populated via EntityPersonRelationshipLink.is_beneficiary = True
    'notify': common_columns.get('boolean_default_false')(),
    'relationship_type_id': common_columns.get('integer_not_nullable')(), # Auto populate from EntityPersonRelationshipLink.relationship_type_id
    'share_of_sum_assured': common_columns.get('currency')(),
    }
PolicyBeneficiary = get_phat_table(model_name='PolicyBeneficiary', columndict=columns_tbl_policy_beneficiary)

# ********************* Policy Life Assured ***********************************#

columns_tbl_policy_life_assured = {
    '__tablename__': 'tbl_policy_life_assured',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'relationship_type_id': common_columns.get('integer_not_nullable')(),
    'inception_age': common_columns.get('integer_not_nullable')(),
    'entity_person_id': common_columns.get('integer_not_nullable')(),
    }
PolicyLifeAssured = get_phat_table(model_name='PolicyLifeAssured', columndict=columns_tbl_policy_life_assured)

columns_tbl_policy_life_assured_sum_assured = {
    '__tablename__': 'tbl_policy_life_assured_sum_assured',
    'policy_life_assured_id': common_columns.get('integer_not_nullable')(),
    'initial_sum_assured_amount': common_columns.get('currency')(),
    'current_sum_assured_amount': common_columns.get('currency')(),
    'share_of_policy_premium_amount': common_columns.get('currency')(),
    'sum_assured_increase_percentage': common_columns.get('percentage')(),
    }
PolicyLifeAssuredSumAssured = get_phat_table(model_name='PolicyLifeAssuredSumAssured', columndict=columns_tbl_policy_life_assured_sum_assured)

# ********************* Policy Benefit ***********************************#

columns_tbl_policy_benefit = {
    '__tablename__': 'tbl_policy_benefit',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'claims_left': common_columns.get('integer_not_nullable')(),
    }
PolicyBenefit = get_phat_table(model_name='PolicyBenefit', columndict=columns_tbl_policy_benefit)

# Below table exists to reduce the calls between 'services' 14 Jan 2020 Camilla
# This is duplicated with model/claim.py - tbl_claim_policy_benefit
columns_tbl_policy_benefit_claim = {
    '__tablename__': 'tbl_policy_benefit_claim',
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'claim_id': common_columns.get('integer_not_nullable')(),
    }
PolicyBenefitClaim = get_phat_table(model_name='PolicyBenefitClaim', columndict=columns_tbl_policy_benefit_claim)

columns_tbl_policy_benefit_cover = {
    '__tablename__': 'tbl_policy_benefit_cover',
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'cover_and_exclusion_type_id': common_columns.get('integer_not_nullable')(),
    }
PolicyBenefitCover = get_phat_table(model_name='PolicyBenefitCover', columndict=columns_tbl_policy_benefit_cover)

columns_tbl_policy_benefit_exclusion = {
    '__tablename__': 'tbl_policy_benefit_exclusion',
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_exclusion_id': common_columns.get('integer_not_nullable')(),
    }
PolicyBenefitExclusion = get_phat_table(model_name='PolicyBenefitExclusion', columndict=columns_tbl_policy_benefit_exclusion)

columns_tbl_policy_benefit_exclusion_expiry = {
    '__tablename__': 'tbl_policy_benefit_exclusion_expiry',
    'policy_benefit_exclusion_id': common_columns.get('integer_not_nullable')(),
    'expiry_date': common_columns.get('date')(),
    }
PolicyBenefitExclusionExpiry = get_phat_table(model_name='PolicyBenefitExclusionExpiry', columndict=columns_tbl_policy_benefit_exclusion_expiry)

# ********************* Policy Loader ***********************************#

columns_tbl_policy_loader = {
    '__tablename__': 'tbl_policy_loader',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'loader_question_answer_id': common_columns.get('integer_not_nullable')(),
    }
PolicyLoader = get_phat_table(model_name='PolicyLoader', columndict=columns_tbl_policy_loader)

# ********************* Policy Premium ***********************************#

PolicyPremiumPaymentMethodType = get_type_table(model_name='PolicyPremiumPaymentMethod', table_name='policy_premium_payment_method')

columns_tbl_policy_premium = {
    '__tablename__': 'tbl_policy_premium',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'initial_annual_premium_amount': common_columns.get('currency')(),
    'current_annual_premium_amount': common_columns.get('currency')(),
    'premium_increase_percentage': common_columns.get('percentage_not_nullable')(),
    'policy_premium_payment_method_type_id': common_columns.get('integer_not_nullable')(),
    }
PolicyPremium = get_phat_table(model_name='PolicyPremium', columndict=columns_tbl_policy_premium)

columns_tbl_policy_premium_payment_schedule = {
    '__tablename__': 'tbl_policy_premium_payment_schedule',
    'policy_premium_id': common_columns.get('integer_not_nullable')(),
    'premium_frequency_id': common_columns.get('integer_not_nullable')(),
    'adjustment_factor': common_columns.get('integer_not_nullable')(),
    }
PolicyPremiumPaymentSchedule = get_phat_table(model_name='PolicyPremiumPaymentSchedule', columndict=columns_tbl_policy_premium_payment_schedule)

# ********************* Policy Temp ***********************************#

columns_tbl_policy_benefit_business_asset_temp = {
    '__tablename__': 'tbl_policy_benefit_business_asset_temp',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'asset_premium_rate_turnover_line_item_id' : common_columns.get('integer_not_nullable')(),
    'company_registration_number': common_columns.get('description')(),
    'turnover': common_columns.get('currency')(),
    'email': common_columns.get('description')(),
    'contact_name': common_columns.get('description')(),
    'contact_number': common_columns.get('description')(),
    'activity': common_columns.get('description')(),
    }
PolicyBenefitBusinessAssetTemp = get_phat_table(model_name='PolicyBenefitBusinessAssetTemp', columndict=columns_tbl_policy_benefit_business_asset_temp)

columns_tbl_policy_benefit_employee_asset_temp = {
    '__tablename__': 'tbl_policy_benefit_employee_asset_temp',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'asset_premium_rate_employee_line_item_id' : common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('description')(),
    'surname': common_columns.get('description')(),
    }
PolicyBenefitEmployeeAssetTemp = get_phat_table(model_name='PolicyBenefitEmployeeAssetTemp', columndict=columns_tbl_policy_benefit_employee_asset_temp)

columns_tbl_policy_benefit_property_asset_temp = {
    '__tablename__': 'tbl_policy_benefit_property_asset_temp',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'asset_premium_rate_turnover_line_item_id' : common_columns.get('integer_not_nullable')(),
    'description': common_columns.get('description')(),
    'number_of_premises': common_columns.get('integer')(),
    'is_owner': common_columns.get('boolean')(),
    'is_shared': common_columns.get('boolean')(),
    'number_of_shared': common_columns.get('integer')(),
    }
PolicyBenefitPropertyAssetTemp = get_phat_table(model_name='PolicyBenefitPropertyAssetTemp', columndict=columns_tbl_policy_benefit_property_asset_temp)

columns_tbl_policy_benefit_vehicle_asset_temp = {
    '__tablename__': 'tbl_policy_benefit_vehicle_asset_temp',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'policy_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'asset_premium_rate_vehicle_line_item_id' : common_columns.get('integer_not_nullable')(),
    'insured_type_id': common_columns.get('integer')(),
    'owned_type_id': common_columns.get('integer')(),
    'is_fleet': common_columns.get('boolean')(),
    'number_of_vehicles': common_columns.get('integer')(),
    'type_of_vehicle': common_columns.get('description')(),
    'vin_number': common_columns.get('description')(),
    'registration_number': common_columns.get('description')(),
    }
PolicyBenefitVehicleAssetTemp = get_phat_table(model_name='PolicyBenefitVehicleAssetTemp', columndict=columns_tbl_policy_benefit_vehicle_asset_temp)
