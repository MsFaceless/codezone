# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_type_table, get_phat_table

###############################################################################
# All Product Related Types
###############################################################################

# Shared between Product and Benefit
CommunicationType = get_type_table(model_name='Communication', table_name='communication') # Sms, Email, Print
PeriodType = get_type_table(model_name='Period', table_name='period') # Days, Months, Calendar Months, etc.

# Product
ProductType = get_type_table(model_name='Product', table_name='product')  # Contractual, Voucher
ProductStateType = get_type_table(model_name='ProductState', table_name='product_state') # Sandbox, Active, Expired
ProductMessageType = get_type_table(model_name='ProductMessage', table_name='product_message') # Reminder, Confirmation

# Benefit
BenefitPurchaseType = get_type_table(model_name='BenefitPurchase', table_name='benefit_purchase') # Group, Coupon, Loyalty
BenefitPriceType = get_type_table(model_name='BenefitPrice', table_name='benefit_price') # Rate table, Fixed premium & sum assured
BenefitInsuredType = get_type_table(model_name='BenefitInsured', table_name='benefit_insured') # Business, Natural Person, Member only, Family only, Member & Family
BenefitCoverAndExclusionType = get_type_table(model_name='BenefitCoverAndExclusion', table_name='benefit_cover_and_exclusion') # All Death, Suicide, etc.
BenefitExclusionExpiryType = get_type_table(model_name='BenefitExclusionExpiry', table_name='benefit_exclusion_expiry') # Days, Premiums, Infinte
BenefitPeriodEffectType = get_type_table(model_name='BenefitPeriodEffect', table_name='benefit_period_effect') # Active, Claim Grace, Refund Grace, etc.
BenefitMessageType = get_type_table(model_name='BenefitMessage', table_name='benefit_message') # Refund, Claim
BenefitAllocationType = get_type_table(model_name='BenefitAllocation', table_name='benefit_allocation') # Acquisition, Purchase, Claim, Redemption
BenefitAllocationCalculationType = get_type_table(model_name='BenefitAllocationCalculation', table_name='benefit_allocation_calculation') # Percentage, Amount, Factor
BenefitFrequencyType = get_type_table(model_name='BenefitFrequency', table_name='benefit_frequency') # Daily, Weekly, etc.
BenefitAssuredLifeRelationshipType = get_type_table(model_name='BenefitAssuredLifeRelationship', table_name='benefit_assured_life_relationship') # Principal, Spouse, etc.
BenefitAssetType = get_type_table(model_name='BenefitAsset', table_name='benefit_asset') # Business, Employee, Vehicle, Property

# Utilities
SystemDocumentType = get_type_table(model_name='SystemDocument', table_name='system_document') # Welcome, Claim, Member, Product
LoaderQuestionPremiumEffectType = get_type_table(model_name='LoaderQuestionPremiumEffect', table_name='loader_question_premium_effect') # None, Percentage, Amount

###############################################################################
# Product
###############################################################################

columns_tbl_product = {
    '__tablename__': 'tbl_product',
    'product_type_id': common_columns.get('integer')(),
    'code': common_columns.get('code_not_nullable')(),
    'name': common_columns.get('title_not_nullable')(),
    'entity_org_product_owner_id': common_columns.get('integer')(),
    'product_state_type_id': common_columns.get('integer')(), # default: Sandbox
    'policy_number_prefix': common_columns.get('title')(),
}
Product = get_phat_table(model_name='Product', columndict=columns_tbl_product)

columns_tbl_product_history_link = {
    '__tablename__': 'tbl_product_history_link',
    'product_id': common_columns.get('integer_not_nullable')(),
    'previous_product_id': common_columns.get('integer_not_nullable')()
}
ProductHistoryLink = get_phat_table(model_name='ProductHistoryLink', columndict=columns_tbl_product_history_link)

###############################################################################
# Benefit
###############################################################################

columns_tbl_benefit = {
    '__tablename__': 'tbl_benefit',
    'product_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('title_not_nullable')(),
    'entity_org_insurer_id': common_columns.get('integer_not_nullable')(),
    'benefit_price_type_id': common_columns.get('integer_not_nullable')(),
    'is_life': common_columns.get('boolean')(),
    'benefit_insured_type_id': common_columns.get('integer_not_nullable')(),
    'benefit_purchase_type_id': common_columns.get('integer')(),
    'benefit_cover_link_id': common_columns.get('integer_not_nullable')(),
    'is_main_benefit': common_columns.get('boolean')(),
    'is_compulsory': common_columns.get('boolean')(),
    'allow_multiple_payouts': common_columns.get('boolean_default_false')(),
    'limit_claims': common_columns.get('boolean_default_true')(),
    'claim_terminates_policy': common_columns.get('boolean')(),
}
Benefit = get_phat_table(model_name='Benefit', columndict=columns_tbl_benefit)

columns_tbl_benefit_claim_count = {
    '__tablename__': 'tbl_benefit_claim_count',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'number_of_claims': common_columns.get('integer_default')(default=1),
    'frequency_type_id': common_columns.get('integer_not_nullable')()
}
BenefitClaimCount = get_phat_table(model_name='BenefitClaimCount', columndict=columns_tbl_benefit_claim_count)

columns_tbl_benefit_payout_frequency_option = {
    '__tablename__': 'tbl_benefit_payout_frequency_option',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'number_of_payouts': common_columns.get('integer_default')(default=1),
    'frequency_type_id': common_columns.get('integer_not_nullable')()
}
BenefitPayoutFrequencyOption = get_phat_table(model_name='BenefitPayoutFrequencyOption', columndict=columns_tbl_benefit_payout_frequency_option)

columns_tbl_benefit_premium_frequency_option = {
    '__tablename__': 'tbl_benefit_premium_frequency_option',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'adjustment_factor': common_columns.get('factor')(),
    'frequency_type_id': common_columns.get('integer_not_nullable')(),
}
BenefitPremiumFrequencyOption = get_phat_table(model_name='BenefitPremiumFrequencyOption', columndict=columns_tbl_benefit_premium_frequency_option)

columns_tbl_benefit_annual_increase_option = {
    '__tablename__': 'tbl_benefit_annual_increase_option',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'premium_increase_percentage': common_columns.get('percentage')(),
    'sum_assured_increase_percentage': common_columns.get('percentage')()
}
BenefitAnnualIncreaseOption = get_phat_table(model_name='BenefitAnnualIncreaseOption', columndict=columns_tbl_benefit_annual_increase_option)

###############################################################################
# Benefit - Premium and Sum Assured
###############################################################################

columns_tbl_benefit_rate_table = {
    '__tablename__': 'tbl_benefit_rate_table',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'minimum_premium': common_columns.get('currency')(),
    'maximum_premium': common_columns.get('currency')(),
    'minimum_sum_assured': common_columns.get('currency')(),
    'maximum_sum_assured': common_columns.get('currency')(),
}
BenefitRateTable = get_phat_table(model_name='BenefitRateTable', columndict=columns_tbl_benefit_rate_table)

columns_tbl_benefit_price = {
    '__tablename__': 'tbl_benefit_price',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'premium': common_columns.get('currency_not_nullable')(),
    'sum_assured': common_columns.get('currency_not_nullable')(),
}
BenefitPrice = get_phat_table(model_name='BenefitPrice', columndict=columns_tbl_benefit_price)

columns_tbl_benefit_premium_rounding = {
    '__tablename__': 'tbl_benefit_premium_rounding',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'minimum_premium': common_columns.get('currency')(),
    'maximum_premium': common_columns.get('currency')(),
    'set_premium': common_columns.get('currency')(),
}
BenefitPremiumRounding = get_phat_table(model_name='BenefitPremiumRounding', columndict=columns_tbl_benefit_premium_rounding)

###############################################################################
# Benefit - Assured - Life
###############################################################################

columns_tbl_benefit_assured_life = {
    '__tablename__': 'tbl_benefit_assured_life',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'benefit_assured_life_relationship_type_id': common_columns.get('integer_not_nullable')(),
    'maximum_entry_age': common_columns.get('integer')(), # Oldest age at purchase
    'expiry_age': common_columns.get('integer')(), # Oldest age for policy to be valid
    'maximum_lives': common_columns.get('integer_default')(default=1),
    'minimum_age': common_columns.get('integer_default')(default=1),
    'has_maximum_age': common_columns.get('boolean_default_false')(),
}
BenefitAssuredLife = get_phat_table(model_name='BenefitAssuredLife', columndict=columns_tbl_benefit_assured_life)

columns_tbl_benefit_assured_life_maximum_age = {
    '__tablename__': 'tbl_benefit_assured_life_maximum_age',
    'benefit_assured_life_id': common_columns.get('integer_not_nullable')(),
    'maximum_age': common_columns.get('integer_not_nullable')()
}
BenefitAssuredLifeMaximumAge = get_phat_table(model_name='BenefitAssuredLifeMaximumAge', columndict=columns_tbl_benefit_assured_life_maximum_age)

###############################################################################
# Benefit - Assured - Non Life
###############################################################################

columns_tbl_benefit_assured_non_life = {
    '__tablename__': 'tbl_benefit_assured_non_life',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'benefit_asset_type_id': common_columns.get('integer_not_nullable')(),
    'description': common_columns.get('description')(),
}
BenefitAssuredNonLife = get_phat_table(model_name='BenefitAssuredNonLife', columndict=columns_tbl_benefit_assured_non_life)

###############################################################################
# Product - System Document
###############################################################################

columns_tbl_system_document = {
    '__tablename__': 'tbl_system_document',
    'name': common_columns.get('title_not_nullable')(),
    'description': common_columns.get('description_not_nullable')(),
    'system_document_type_id': common_columns.get('integer_not_nullable')()
}
SystemDocument = get_phat_table(model_name='SystemDocument', columndict=columns_tbl_system_document)

columns_tbl_product_system_document_link = {
    '__tablename__': 'tbl_product_system_document_link',
    'product_id': common_columns.get('integer_not_nullable')(),
    'system_document_id': common_columns.get('integer')(),
    'file_path': common_columns.get('description')(),
}
ProductSystemDocumentLink = get_phat_table(model_name='ProductSystemDocumentLink', columndict=columns_tbl_product_system_document_link)

###############################################################################
# Product - Messaging and Communication
###############################################################################

columns_tbl_product_message = {
    '__tablename__': 'tbl_product_message',
    'product_id': common_columns.get('integer_not_nullable')(),
    'product_message_type_id': common_columns.get('integer_not_nullable')(), # E.g. Reminder or Confirmation
    'communication_type_id': common_columns.get('integer')(),
    'content': common_columns.get('longtext_not_nullable')()
}
ProductMessage = get_phat_table(model_name='ProductMessage', columndict=columns_tbl_product_message)

columns_tbl_product_message_media = {
    '__tablename__': 'tbl_product_message_media',
    'product_message_id': common_columns.get('integer_not_nullable')(),
    'file_path': common_columns.get('description')()
}
ProductMessageMedia = get_phat_table(model_name='ProductMessageMedia', columndict=columns_tbl_product_message_media)

columns_tbl_product_message_reminder = {
    '__tablename__': 'tbl_product_message_reminder',
    'product_message_id': common_columns.get('integer_not_nullable')(),
    'period': common_columns.get('integer_not_nullable')(),
    'period_type_id': common_columns.get('integer_not_nullable')()
}
ProductMessageReminder = get_phat_table(model_name='ProductMessageReminder', columndict=columns_tbl_product_message_reminder)

###############################################################################
# Benefit - Messaging and Communication
###############################################################################

columns_tbl_benefit_message = {
    '__tablename__': 'tbl_benefit_message',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'benefit_message_type_id': common_columns.get('integer_not_nullable')(), # E.g. Refund or Claim
    'communication_type_id': common_columns.get('integer')(),
    'content': common_columns.get('longtext_not_nullable')()
}
BenefitMessage = get_phat_table(model_name='BenefitMessage', columndict=columns_tbl_benefit_message)

columns_tbl_benefit_message_media = {
    '__tablename__': 'tbl_benefit_message_media',
    'benefit_message_id': common_columns.get('integer_not_nullable')(),
    'file_path': common_columns.get('description')()
}
BenefitMessageMedia = get_phat_table(model_name='BenefitMessageMedia', columndict=columns_tbl_benefit_message_media)

columns_tbl_benefit_message_reminder = {
    '__tablename__': 'tbl_benefit_message_reminder',
    'benefit_message_id': common_columns.get('integer_not_nullable')(),
    'period': common_columns.get('integer_not_nullable')(),
    'period_type_id': common_columns.get('integer_not_nullable')()
}
BenefitMessageReminder = get_phat_table(model_name='BenefitMessageReminder', columndict=columns_tbl_benefit_message_reminder)

###############################################################################
# Benefit - Claim Questions
###############################################################################

columns_tbl_benefit_claim_question_link = {
    '__tablename__': 'tbl_benefit_claim_question_link',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'claim_question_id': common_columns.get('integer_not_nullable')(),
    'claim_question_correct_answer_id': common_columns.get('integer_not_nullable')(),
}
BenefitClaimQuestionLink = get_phat_table(model_name='BenefitClaimQuestionLink', columndict=columns_tbl_benefit_claim_question_link)

columns_tbl_claim_question = {
    '__tablename__': 'tbl_claim_question',
    'text': common_columns.get('longtext_not_nullable')()
}
ClaimQuestion = get_phat_table(model_name='ClaimQuestion', columndict=columns_tbl_claim_question)

columns_tbl_claim_question_answer = {
    '__tablename__': 'tbl_claim_question_answer',
    'claim_question_id': common_columns.get('integer_not_nullable')(),
    'answer_text': common_columns.get('longtext_not_nullable')(),
}
ClaimQuestionAnswer = get_phat_table(model_name='ClaimQuestionAnswer', columndict=columns_tbl_claim_question_answer)

###############################################################################
# Benefit - Cover and Exclusions
###############################################################################

columns_tbl_benefit_cover_link = {
    '__tablename__': 'tbl_benefit_cover_link',
    'cover_and_exclusion_type_id': common_columns.get('integer_not_nullable')()
}
BenefitCoverLink = get_phat_table(model_name='BenefitCoverLink', columndict=columns_tbl_benefit_cover_link)

columns_tbl_benefit_exclusion_link = {
    '__tablename__': 'tbl_benefit_exclusion_link',
    'cover_and_exclusion_type_id': common_columns.get('integer_not_nullable')()
}
BenefitExclusionLink = get_phat_table(model_name='BenefitExclusionLink', columndict=columns_tbl_benefit_exclusion_link)

columns_tbl_benefit_exclusion = {
    '__tablename__': 'tbl_benefit_exclusion',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'benefit_exclusion_link_id': common_columns.get('integer_not_nullable')(),
    'benefit_exclusion_expiry_type_id': common_columns.get('integer_not_nullable')()
}
BenefitExclusion = get_phat_table(model_name='BenefitExclusion', columndict=columns_tbl_benefit_exclusion)

columns_tbl_benefit_exclusion_expiry_days = {
    '__tablename__': 'tbl_benefit_exclusion_expiry_days',
    'benefit_exclusion_id': common_columns.get('integer_not_nullable')(),
    'number_of_days': common_columns.get('integer_not_nullable')()
}
BenefitExclusionExpiryDays = get_phat_table(model_name='BenefitExclusionExpiryDays', columndict=columns_tbl_benefit_exclusion_expiry_days)

columns_tbl_benefit_exclusion_expiry_count = {
    '__tablename__': 'tbl_benefit_exclusion_expiry_count',
    'benefit_exclusion_id': common_columns.get('integer_not_nullable')(),
    'count': common_columns.get('integer')()
}
BenefitExclusionExpiryCount = get_phat_table(model_name='BenefitExclusionExpiryCount', columndict=columns_tbl_benefit_exclusion_expiry_count)

###############################################################################
# Benefit - Period or Durations
###############################################################################

columns_tbl_benefit_period = {
    '__tablename__': 'tbl_benefit_period',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'benefit_period_effect_type_id': common_columns.get('integer')(),
    'period_type_id': common_columns.get('integer_not_nullable')(),
    'time_period': common_columns.get('integer')()
}
BenefitPeriod = get_phat_table(model_name='BenefitPeriod', columndict=columns_tbl_benefit_period)

###############################################################################
# Benefit - Allocations
###############################################################################

columns_tbl_general_ledger_account = {
    '__tablename__': 'tbl_general_ledger_account',
    'name': common_columns.get('title_not_nullable')(),
    'debit_account': common_columns.get('title_not_nullable')(),
    'credit_account': common_columns.get('title_not_nullable')(),
    'gl_key': common_columns.get('title_not_nullable')()
}
GeneralLedgerAccount = get_phat_table(model_name='GeneralLedgerAccount', columndict=columns_tbl_general_ledger_account)

columns_tbl_benefit_allocation = {
    '__tablename__': 'tbl_benefit_allocation',
    'name': common_columns.get('title_not_nullable')()
}
BenefitAllocation = get_phat_table(model_name='BenefitAllocation', columndict=columns_tbl_benefit_allocation)

columns_tbl_benefit_allocation_link = {
    '__tablename__': 'tbl_benefit_allocation_link',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'benefit_allocation_id': common_columns.get('integer_not_nullable')(),
    'gl_account_id': common_columns.get('integer_not_nullable')(),
    'benefit_allocation_type_id': common_columns.get('integer_not_nullable')(),
    'allocation_calculation_type_id': common_columns.get('integer_not_nullable')(),
    'is_claimable': common_columns.get('boolean')()
}
BenefitAllocationLink = get_phat_table(model_name='BenefitAllocationLink', columndict=columns_tbl_benefit_allocation_link)

columns_tbl_benefit_allocation_link_calculation_percentage = {
    '__tablename__': 'tbl_benefit_allocation_link_calculation_percentage',
    'benefit_allocation_link_id': common_columns.get('integer_not_nullable')(),
    'percentage': common_columns.get('percentage_not_nullable')()
}
BenefitAllocationLinkCalculationPercentage = get_phat_table(model_name='BenefitAllocationLinkCalculationPercentage', columndict=columns_tbl_benefit_allocation_link_calculation_percentage)

columns_tbl_benefit_allocation_link_calculation_amount = {
    '__tablename__': 'tbl_benefit_allocation_link_calculation_amount',
    'benefit_allocation_link_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')()
}
BenefitAllocationLinkCalculationAmount = get_phat_table(model_name='BenefitAllocationLinkCalculationAmount', columndict=columns_tbl_benefit_allocation_link_calculation_amount)

columns_tbl_benefit_allocation_link_calculation_factor = {
    '__tablename__': 'tbl_benefit_allocation_link_calculation_factor',
    'benefit_allocation_link_id': common_columns.get('integer_not_nullable')(),
    'factor': common_columns.get('integer_not_nullable')()
}
BenefitAllocationLinkCalculationFactor = get_phat_table(model_name='BenefitAllocationLinkCalculationFactor', columndict=columns_tbl_benefit_allocation_link_calculation_factor)

###############################################################################
# Benefit - Loaders
###############################################################################

columns_tbl_benefit_loader_link = {
    '__tablename__': 'tbl_benefit_loader_link',
    'benefit_id': common_columns.get('integer_not_nullable')(),
    'loader_question_id': common_columns.get('integer_not_nullable')()
}
BenefitLoaderLink = get_phat_table(model_name='BenefitLoaderLink', columndict=columns_tbl_benefit_loader_link)

columns_tbl_loader_question = {
    '__tablename__': 'tbl_loader_question',
    'text': common_columns.get('longtext')(),
    'loader_question_premium_effect_type_id': common_columns.get('integer_not_nullable')()
}
LoaderQuestion = get_phat_table(model_name='LoaderQuestion', columndict=columns_tbl_loader_question)

columns_tbl_loader_question_answer = {
    '__tablename__': 'tbl_loader_question_answer',
    'loader_question_id': common_columns.get('integer_not_nullable')(),
    'answer_text': common_columns.get('longtext')(),
}
LoaderQuestionAnswer = get_phat_table(model_name='LoaderQuestionAnswer', columndict=columns_tbl_loader_question_answer)

columns_tbl_loader_question_answer_percentage = {
    '__tablename__': 'tbl_loader_question_answer_percentage',
    'loader_question_answer_id': common_columns.get('integer_not_nullable')(),
    'percentage': common_columns.get('percentage_not_nullable')()
}
LoaderQuestionAnswerPercentage = get_phat_table(model_name='LoaderQuestionAnswerPercentage', columndict=columns_tbl_loader_question_answer_percentage)

columns_tbl_loader_question_answer_amount = {
    '__tablename__': 'tbl_loader_question_answer_amount',
    'loader_question_answer_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')()
}
LoaderQuestionAnswerAmount = get_phat_table(model_name='LoaderQuestionAnswerAmount', columndict=columns_tbl_loader_question_answer_amount)

###############################################################################
# Benefit - Rate Tables
###############################################################################

columns_tbl_rate_table = {
    '__tablename__': 'tbl_rate_table',
    'is_life': common_columns.get('boolean')(),
    'code': common_columns.get('code')(),
    'name': common_columns.get('title')(),
}
RateTable = get_phat_table(model_name='RateTable', columndict=columns_tbl_rate_table)

columns_tbl_rate_table_asset_type = {
    '__tablename__': 'tbl_rate_table_asset_type',
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'benefit_asset_type': common_columns.get('integer_not_nullable')(),
}
RateTableAssetType = get_phat_table(model_name='RateTableAssetType', columndict=columns_tbl_rate_table_asset_type)

columns_tbl_rate_table_base_value = {
    '__tablename__': 'tbl_rate_table_base_value',
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'base_value': common_columns.get('integer_not_nullable')(default=1000),
}
RateTableAssetType = get_phat_table(model_name='RateTableAssetType', columndict=columns_tbl_rate_table_base_value)

columns_tbl_rate_table_line_item_life = {
    '__tablename__': 'tbl_rate_table_line_item_life',
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'gender_type_id': common_columns.get('integer_not_nullable')(),  # optional from utilities
    'maximum_age': common_columns.get('integer')(),
    'minimum_age': common_columns.get('integer')(),
    'rate_factor': common_columns.get('factor')(),
}
RateTableLineItemLife = get_phat_table(model_name='RateTableLineItemLife', columndict=columns_tbl_rate_table_line_item_life)

columns_tbl_rate_table_line_item_vehicle = {
    '__tablename__': 'columns_tbl_rate_table_line_item_vehicle',
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'description': common_columns.get('description_not_nullable')(),
    'insured_amount': common_columns.get('currency_not_nullable')(),
    'uninsured_amount': common_columns.get('currency_not_nullable')(),
    'third_party_amount': common_columns.get('currency_not_nullable')(),
}
RateTableLineItemVehicle = get_phat_table(model_name='RateTableLineItemVehicle', columndict=columns_tbl_rate_table_line_item_vehicle)

columns_tbl_rate_table_line_item_employee = {
    '__tablename__': 'tbl_rate_table_line_item_employee',
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'minimum_employees_coverable': common_columns.get('integer')(),
    'maximum_employees_coverable': common_columns.get('integer')(),
    'amount': common_columns.get('currency_not_nullable')(),
}
RateTableLineItemEmployee = get_phat_table(model_name='RateTableLineItemEmployee', columndict=columns_tbl_rate_table_line_item_employee)

columns_tbl_rate_table_line_item_turnover = {
    '__tablename__': 'tbl_rate_table_line_item_turnover',
    'rate_table_id': common_columns.get('integer_not_nullable')(),
    'minimum_turnover': common_columns.get('integer_not_nullable')(),
    'maximum_turnover': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')(),
}
RateTableLineItemTurnover = get_phat_table(model_name='RateTableLineItemTurnover', columndict=columns_tbl_rate_table_line_item_turnover)
