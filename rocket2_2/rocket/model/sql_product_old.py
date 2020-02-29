# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_type_table, get_phat_table

# ---------------------------- Product -----------------------------------

# Product, ProductType, ProductState, ProductHistoryLink

ProductType = get_type_table(model_name='Product', table_name='product')  # Voucher, Traditional, Term Life, Credit Life
ProductStateType = get_type_table(model_name='ProductState', table_name='product_state') # Sandbox, Active, Expired

columns_tbl_product = {
    '__tablename__': 'tbl_product',
    'product_type_id': common_columns.get('integer')(),
    'code': common_columns.get('code')(),
    'name': common_columns.get('title_not_nullable')(),
    'product_owner_id': common_columns.get('integer')(),
    'product_state_id': common_columns.get('integer')(),
    'policy_number_prefix': common_columns.get('title')(),
}
Product = get_phat_table(model_name='Product', columndict=columns_tbl_product)

columns_tbl_product_history_link = {
    '__tablename__': 'tbl_product_history_link',
    'product_id': common_columns.get('integer_not_nullable')(),
    'previous_product_id': common_columns.get('integer')()
}
ProductHistoryLink = get_phat_table(model_name='ProductHistoryLink', columndict=columns_tbl_product_history_link)

# ---------------------------- Product Premium Increases-----------------------------------

# ProductAnnualPremiumIncreaseOption, ProductPremiumFrequencyOption

columns_tbl_product_annual_premium_increase_option = {
    '__tablename__': 'tbl_product_annual_premium_increase_option',
    'product_id': common_columns.get('integer_not_nullable')(),
    'premium_increase_percentage': common_columns.get('percentage')(),
    'sum_assured_increase_percentage': common_columns.get('percentage')()
}
ProductAnnualPremiumIncreaseOption = get_phat_table(model_name='ProductAnnualPremiumIncreaseOption',
                                                    columndict=columns_tbl_product_annual_premium_increase_option)

columns_tbl_product_premium_frequency_option = {
    '__tablename__': 'tbl_product_premium_frequency_option',
    'product_id': common_columns.get('integer_not_nullable')(),
    'product_frequency_type_id': common_columns.get('integer_not_nullable')(),
    'adjustment_factor': common_columns.get('factor')()
}
ProductPremiumFrequencyOption = get_phat_table(model_name='ProductPremiumFrequencyOption',
                                               columndict=columns_tbl_product_premium_frequency_option)

# ---------------------------------- System Document ------------------------------------

# SystemDocumentType, SystemDocument, ProductSystemDocumentLink

SystemDocumentType = get_type_table(model_name='SystemDocument', table_name='system_document')

columns_tbl_system_document = {
    '__tablename__': 'tbl_system_document',
    'name': common_columns.get('title')(),
    'description': common_columns.get('description')(),
    'system_document_type_id': common_columns.get('integer')()
}
SystemDocument = get_phat_table(model_name='SystemDocument', columndict=columns_tbl_system_document)

columns_tbl_product_system_document_link = {
    '__tablename__': 'tbl_product_system_document_link',
    'product_id': common_columns.get('integer_not_nullable')(),
    'system_document_id': common_columns.get('integer')(),
    'file_path': common_columns.get('description')(),
}
ProductSystemDocumentLink = get_phat_table(model_name='ProductSystemDocumentLink',
                                           columndict=columns_tbl_product_system_document_link)

# ---------------------------------- Life Assured ------------------------------------

# ProductBenefitLifeAssured, ProductBenefitLifeAssuredType, ProductBenefitLifeAssuredRelationshipType
# ProductBenefitLifeAssuredSumAssuredType, ProductBenefitLifeAssuredSumAssuredPercentage, ProductBenefitLifeAssuredSumAssuredAmount
# ProductBenefitLifeAssuredMaximumAge

ProductBenefitLifeAssuredRelationshipType = get_type_table(model_name='ProductBenefitLifeAssuredRelationship', table_name='product_benefit_life_assured_relationship')

columns_tbl_product_benefit_life_assured = {
    '__tablename__': 'tbl_product_benefit_life_assured',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'relationship_type_id': common_columns.get('integer_not_nullable')(),
    'maximum_lives': common_columns.get('integer_default')(default=1),
    'minimum_age': common_columns.get('integer_default')(default=1),
    'has_maximum_age': common_columns.get('boolean_default_false')(),
}
ProductBenefitLifeAssured = get_phat_table(model_name='ProductBenefitLifeAssured', columndict=columns_tbl_product_benefit_life_assured)

columns_tbl_product_benefit_life_assured_maximum_age = {
    '__tablename__': 'tbl_product_benefit_life_assured_maximum_age',
    'product_benefit_life_assured_id': common_columns.get('integer_not_nullable')(),
    'maximum_age': common_columns.get('integer_not_nullable')()
}
ProductBenefitLifeAssuredMaximumAge = get_phat_table(model_name='ProductBenefitLifeAssuredMaximumAge', columndict=columns_tbl_product_benefit_life_assured_maximum_age)

# ---------------------------- Asset Assured -----------------------------------

ProductBenefitAssetTempType = get_type_table(model_name='ProductBenefitAssetTemp', table_name='product_benefit_asset_temp')

columns_tbl_product_benefit_asset_temp = {
    '__tablename__': 'tbl_product_benefit_asset_temp',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_asset_temp_type_id': common_columns.get('integer_not_nullable')(),
    'description': common_columns.get('longtext_not_nullable')(),
}
ProductBenefitAssetTemp = get_phat_table(model_name='ProductBenefitAssetTemp', columndict=columns_tbl_product_benefit_asset_temp)

columns_tbl_product_benefit_asset_premium_rate_link_temp = {
    '__tablename__': 'tbl_product_benefit_asset_premium_rate_link_temp',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_asset_temp_type_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_asset_premium_rate_temp_id': common_columns.get('integer_not_nullable')(),
}
ProductBenefitAssetPremiumRateLinkTemp = get_phat_table(model_name='ProductBenefitAssetPremiumRateLinkTemp', columndict=columns_tbl_product_benefit_asset_premium_rate_link_temp)

columns_tbl_product_benefit_asset_premium_rate_temp = {
    '__tablename__': 'tbl_product_benefit_asset_premium_rate_temp',
    'product_benefit_asset_temp_type_id': common_columns.get('integer_not_nullable')(),
    'code': common_columns.get('code')(),
    'name': common_columns.get('title')(),
}
ProductBenefitAssetPremiumRateTemp = get_phat_table(model_name='ProductBenefitAssetPremiumRateTemp', columndict=columns_tbl_product_benefit_asset_premium_rate_temp)

columns_tbl_product_benefit_asset_premium_rate_vehicle_line_item_temp = {
    '__tablename__': 'tbl_product_benefit_asset_premium_rate_vehicle_line_item_temp',
    'product_benefit_asset_premium_rate_temp_id': common_columns.get('integer_not_nullable')(),
    'description': common_columns.get('description_not_nullable')(),
    'insured_amount': common_columns.get('currency_not_nullable')(),
    'uninsured_amount': common_columns.get('currency_not_nullable')(),
    'third_party_amount': common_columns.get('currency_not_nullable')(),
}
ProductBenefitAssetPremiumRateVehicleLineItemTemp = get_phat_table(model_name='ProductBenefitAssetPremiumRateVehicleLineItemTemp',
                                                 columndict=columns_tbl_product_benefit_asset_premium_rate_vehicle_line_item_temp)

columns_tbl_product_benefit_asset_premium_rate_employee_line_item_temp = {
    '__tablename__': 'tbl_product_benefit_asset_premium_rate_employee_line_item_temp',
    'product_benefit_asset_premium_rate_temp_id': common_columns.get('integer_not_nullable')(),
    'minimum_employees_coverable': common_columns.get('integer')(),
    'maximum_employees_coverable': common_columns.get('integer')(),
    'amount': common_columns.get('currency_not_nullable')(),
}
ProductBenefitAssetPremiumRateEmployeeLineItemTemp = get_phat_table(model_name='ProductBenefitAssetPremiumRateEmployeeLineItemTemp',
                                                 columndict=columns_tbl_product_benefit_asset_premium_rate_employee_line_item_temp)

columns_tbl_product_benefit_asset_premium_rate_turnover_line_item_temp = {
    '__tablename__': 'tbl_product_benefit_asset_premium_rate_turnover_line_item_temp',
    'product_benefit_asset_premium_rate_temp_id': common_columns.get('integer_not_nullable')(),
    'minimum_turnover': common_columns.get('integer_not_nullable')(),
    'maximum_turnover': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')(),
}
ProductBenefitAssetPremiumRateTurnoverLineItemTemp = get_phat_table(model_name='ProductBenefitAssetPremiumRateTurnoverLineItemTemp',
                                                 columndict=columns_tbl_product_benefit_asset_premium_rate_turnover_line_item_temp)

# ---------------------------------- Loaders ------------------------------------

# ProductLoaderLink, LoaderQuestion, LoaderQuestionPremiumEffectType, LoaderQuestionAnswer,
# LoaderQuestionAnswerType, LoaderQuestionAnswerPercentage, LoaderQuestionAnswerAmount

columns_tbl_product_loader_link = {
    '__tablename__': 'tbl_product_loader_link',
    'product_id': common_columns.get('integer_not_nullable')(),
    'loader_question_id': common_columns.get('integer_not_nullable')()
}
ProductLoaderLink = get_phat_table(model_name='ProductLoaderLink', columndict=columns_tbl_product_loader_link)

columns_tbl_loader_question = {
    '__tablename__': 'tbl_loader_question',
    'text': common_columns.get('longtext')(),
    'loader_question_premium_effect_type_id': common_columns.get('integer_not_nullable')()
}
LoaderQuestion = get_phat_table(model_name='LoaderQuestion', columndict=columns_tbl_loader_question)

LoaderQuestionPremiumEffectType = get_type_table(model_name='LoaderQuestionPremiumEffect',
                                                 table_name='loader_question_premium_effect')

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
LoaderQuestionAnswerPercentage = get_phat_table(model_name='LoaderQuestionAnswerPercentage',
                                                columndict=columns_tbl_loader_question_answer_percentage)

columns_tbl_loader_question_answer_amount = {
    '__tablename__': 'tbl_loader_question_answer_amount',
    'loader_question_answer_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')()
}
LoaderQuestionAnswerAmount = get_phat_table(model_name='LoaderQuestionAnswerAmount',
                                            columndict=columns_tbl_loader_question_answer_amount)

# -------------------------------------------- Allocations --------------------------------------------

# GeneralLedgerAccount, ProductBenefitAllocation, ProductBenefitAllocationType,
# ProductBenefitAllocationCalculationType, ProductBenefitAllocationType, ProductBenefitAllocationLink,
# ProductBenefitAllocationLinkCalculationPercentage, ProductBenefitAllocationLinkCalculationAmount,
# ProductBenefitAllocationLinkCalculationFactor

columns_tbl_general_ledger_account = {
    '__tablename__': 'tbl_general_ledger_account',
    'name': common_columns.get('title_not_nullable')(),
    'debit_account': common_columns.get('title_not_nullable')(),
    'credit_account': common_columns.get('title_not_nullable')(),
    'gl_key': common_columns.get('title_not_nullable')()
}
GeneralLedgerAccount = get_phat_table(model_name='GeneralLedgerAccount', columndict=columns_tbl_general_ledger_account)

columns_tbl_product_benefit_allocation = {
    '__tablename__': 'tbl_product_benefit_allocation',
    'name': common_columns.get('title_not_nullable')()  # commission, profit, contingency etc.
}
ProductBenefitAllocation = get_phat_table(model_name='ProductBenefitAllocation', columndict=columns_tbl_product_benefit_allocation)

ProductBenefitAllocationCalculationType = get_type_table(model_name='ProductBenefitAllocationCalculation', table_name='product_benefit_allocation_calculation')
ProductBenefitAllocationType = get_type_table(model_name='ProductBenefitAllocation', table_name='product_benefit_allocation')

columns_tbl_product_benefit_allocation_link = {
    '__tablename__': 'tbl_product_benefit_allocation_link',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_allocation_id': common_columns.get('integer_not_nullable')(),
    'gl_account_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_allocation_type_id': common_columns.get('integer_not_nullable')(),
    'product_allocation_calculation_type_id': common_columns.get('integer_not_nullable')(),
    'is_claimable': common_columns.get('boolean')()
}
ProductBenefitAllocationLink = get_phat_table(model_name='ProductBenefitAllocationLink', columndict=columns_tbl_product_benefit_allocation_link)

columns_tbl_product_benefit_allocation_link_calculation_percentage = {
    '__tablename__': 'tbl_product_benefit_allocation_link_calculation_percentage',
    'product_benefit_allocation_link_id': common_columns.get('integer_not_nullable')(),
    'percentage': common_columns.get('percentage_not_nullable')()
}
ProductBenefitAllocationLinkCalculationPercentage \
    = get_phat_table(model_name='ProductBenefitAllocationLinkCalculationPercentage',
                     columndict=columns_tbl_product_benefit_allocation_link_calculation_percentage)

columns_tbl_product_benefit_allocation_link_calculation_amount = {
    '__tablename__': 'tbl_product_benefit_allocation_link_calculation_amount',
    'product_benefit_allocation_link_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')()
}
ProductBenefitAllocationLinkCalculationAmount = \
    get_phat_table(model_name='ProductBenefitAllocationLinkCalculationAmount',
                   columndict=columns_tbl_product_benefit_allocation_link_calculation_amount)

columns_tbl_product_benefit_allocation_link_calculation_factor = {
    '__tablename__': 'tbl_product_benefit_allocation_link_calculation_factor',
    'product_benefit_allocation_link_id': common_columns.get('integer_not_nullable')(),
    'factor': common_columns.get('integer_not_nullable')()
}
ProductBenefitAllocationLinkCalculationFactor = \
    get_phat_table(model_name='ProductBenefitAllocationLinkCalculationFactor',
                   columndict=columns_tbl_product_benefit_allocation_link_calculation_factor)

# ---------------------------------- Communication ------------------------------------

# ProductMessageType, ProductCommunicationType, ProductMessage, ProductMessageMedia, ProductReminder

ProductMessageType = get_type_table(model_name='ProductMessage', table_name='product_message')

ProductCommunicationType = get_type_table(model_name='ProductCommunication', table_name='product_communication')

columns_tbl_product_message = {
    '__tablename__': 'tbl_product_message',
    'product_id': common_columns.get('integer_not_nullable')(),
    'product_message_type_id': common_columns.get('integer_not_nullable')(),
    'product_communication_type_id': common_columns.get('integer')(),
    'content': common_columns.get('longtext_not_nullable')()
}
ProductMessage = get_phat_table(model_name='ProductMessage', columndict=columns_tbl_product_message)

columns_tbl_product_message_media = {
    '__tablename__': 'tbl_product_message_media',
    'product_message_id': common_columns.get('integer_not_nullable')(),
    'line_start': common_columns.get('integer')(),
    'file_path': common_columns.get('description')()
}
ProductMessageMedia = get_phat_table(model_name='ProductMessageMedia', columndict=columns_tbl_product_message_media)

columns_tbl_product_reminder = {
    '__tablename__': 'tbl_product_reminder',
    'product_message_id': common_columns.get('integer_not_nullable')(),
    'period': common_columns.get('integer_not_nullable')(),
    'product_period_type_id': common_columns.get('integer_not_nullable')()
}
ProductReminder = get_phat_table(model_name='ProductReminder', columndict=columns_tbl_product_reminder)

# ---------------------------------- Product Benefit Claim Questions ----------------------------------

columns_tbl_product_benefit_claim_question_link = {
    '__tablename__': 'tbl_product_benefit_claim_question_link',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'claim_question_id': common_columns.get('integer_not_nullable')(),
    'claim_question_correct_answer_id': common_columns.get('integer_not_nullable')(),
}
ProductBenefitClaimQuestionLink = get_phat_table(model_name='ProductBenefitClaimQuestionLink', columndict=columns_tbl_product_benefit_claim_question_link)

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

# ---------------------------- Cover and Exclusions -----------------------------------

# ProductCoverAndExclusionType, ProductBenefitCoverLink, ProductBenefitExclusionLink, ProductBenefitExclusionExpiryType
# ProductBenefitExclusion, ProductBenefitExclusionExpiryDays, ProductBenefitExclusionExpiryCount

ProductCoverAndExclusionType = get_type_table(model_name='ProductCoverAndExclusion',
                                              table_name='benefit_cover_and_exclusion')

columns_tbl_product_benefit_cover_link = {
    '__tablename__': 'tbl_product_benefit_cover_link',
    'benefit_cover_and_exclusion_type_id': common_columns.get('integer_not_nullable')()
}
ProductBenefitCoverLink = get_phat_table(model_name='ProductBenefitCoverLink',
                                         columndict=columns_tbl_product_benefit_cover_link)

columns_tbl_product_benefit_exclusion_link = {
    '__tablename__': 'tbl_product_benefit_exclusion_link',
    'benefit_cover_and_exclusion_type_id': common_columns.get('integer_not_nullable')()
}
ProductBenefitExclusionLink = get_phat_table(model_name='ProductBenefitExclusionLink',
                                             columndict=columns_tbl_product_benefit_exclusion_link)

ProductBenefitExclusionExpiryType = get_type_table(model_name='ProductBenefitExclusionExpiry',
                                                   table_name='product_benefit_exclusion_expiry')

columns_tbl_product_benefit_exclusion = {
    '__tablename__': 'tbl_product_benefit_exclusion',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_exclusion_link_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_exclusion_expiry_type_id': common_columns.get('integer_not_nullable')()
}
ProductBenefitExclusion = get_phat_table(model_name='ProductBenefitExclusion',
                                         columndict=columns_tbl_product_benefit_exclusion)

columns_tbl_product_benefit_exclusion_expiry_days = {
    '__tablename__': 'tbl_product_benefit_exclusion_expiry_days',
    'product_benefit_exclusion_id': common_columns.get('integer_not_nullable')(),
    'number_of_days': common_columns.get('integer_not_nullable')()
}
ProductBenefitExclusionExpiryDays = get_phat_table(model_name='ProductBenefitExclusionExpiryDays',
                                                   columndict=columns_tbl_product_benefit_exclusion_expiry_days)

columns_tbl_product_benefit_exclusion_expiry_count = {
    '__tablename__': 'tbl_product_benefit_exclusion_expiry_count',
    'product_benefit_exclusion_id': common_columns.get('integer_not_nullable')(),
    'count': common_columns.get('integer')()
}
ProductBenefitExclusionExpiryCount = get_phat_table(model_name='ProductBenefitExclusionExpiryCount',
                                                    columndict=columns_tbl_product_benefit_exclusion_expiry_count)

# ---------------------------- Benefits -----------------------------------

# ProductBenefit, ProductBenefitType

ProductBenefitPurchaseType = get_type_table(model_name='ProductBenefitPurchase', table_name='product_benefit_purchase')
ProductBenefitPriceInitialSetupType = get_type_table(model_name='ProductBenefitPriceInitialSetup', table_name='product_benefit_price_initial_setup')
ProductBenefitAssuredType = get_type_table(model_name='ProductBenefitAssured', table_name='product_benefit_assured') # Life or Non Life

columns_tbl_product_benefit = {
    '__tablename__': 'tbl_product_benefit',
    'product_id': common_columns.get('integer_not_nullable')(),
    'insurer_id': common_columns.get('integer')(),
    'product_benefit_assured_type_id': common_columns.get('integer')(),
    'product_benefit_purchase_type_id': common_columns.get('integer')(),
    'product_benefit_price_initial_setup_type_id': common_columns.get('integer')(),

    'product_benefit_type_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('title')(),
    'is_compulsory': common_columns.get('boolean')(),
    'product_benefit_effect_on_sum_assured_type_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_effect_on_price_type_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_share_of_price_type_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_share_of_sum_assured_type_id': common_columns.get('integer_not_nullable')(),
    'maturity_age': common_columns.get('integer')(),
    'product_benefit_cover_link_id': common_columns.get('integer_not_nullable')(),
    'allow_multiple_payouts': common_columns.get('boolean_default_false')(),
    'limit_claims': common_columns.get('boolean_default_true')(),
    'number_of_claims': common_columns.get('integer_default')(default=1),
    'claim_terminates_policy': common_columns.get('boolean')(),
}
ProductBenefit = get_phat_table(model_name='ProductBenefit', columndict=columns_tbl_product_benefit)

columns_tbl_product_benefit_premium_rate_link = {
    '__tablename__': 'tbl_product_benefit_premium_rate_link',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_premium_rate_id': common_columns.get('integer')(),
}
ProductBenefitPremiumRateLink = get_phat_table(model_name='ProductBenefitPremiumRateLink',
                                         columndict=columns_tbl_product_benefit_premium_rate_link)

columns_tbl_product_benefit_premium_rate = {
    '__tablename__': 'tbl_product_benefit_premium_rate',
    'code': common_columns.get('code')(),
    'name': common_columns.get('title')(),
    'base_value': common_columns.get('currency_default_not_nullable')(default=1000.00)
}
ProductBenefitPremiumRate = get_phat_table(model_name='ProductBenefitPremiumRate', columndict=columns_tbl_product_benefit_premium_rate)

columns_tbl_product_benefit_premium_rate_line_item = {
    '__tablename__': 'tbl_product_benefit_premium_rate_line_item',
    'product_benefit_premium_rate_id': common_columns.get('integer_not_nullable')(),
    'gender_id': common_columns.get('integer_not_nullable')(),  # optional from utilities
    'maximum_age': common_columns.get('integer')(),
    'minimum_age': common_columns.get('integer')(),
    'rate_factor': common_columns.get('factor')()
}
ProductBenefitPremiumRateLineItem = get_phat_table(model_name='ProductBenefitPremiumRateLineItem',
                                                 columndict=columns_tbl_product_benefit_premium_rate_line_item)

ProductBenefitType = get_type_table(model_name='ProductBenefit', table_name='product_benefit')

# ---------------------------- Benefit Premium and Sum Assured -----------------------------------

# ProductBenefitEffectOnSumAssuredType, ProductBenefitEffectOnPriceType, ProductBenefitShareOfPriceType,
# ProductBenefitShareOfSumAssuredType, ProductBenefitPaymentFrequency, ProductBenefitShareOfSumAssuredPercentage,
# ProductBenefitShareOfSumAssuredAmount, ProductBenefitShareOfSumAssuredStatedBenefit, StatedBenefit,
# StatedBenefitLineItem, ProductBenefitShareOfPriceAmount, ProductBenefitShareOfPricePercentage

ProductBenefitEffectOnSumAssuredType = get_type_table(model_name='ProductBenefitEffectOnSumAssured',
                                                      table_name='product_benefit_effect_on_sum_assured')

ProductBenefitEffectOnPriceType = get_type_table(model_name='ProductBenefitEffectOnPrice',
                                                 table_name='product_benefit_effect_on_price')

ProductBenefitShareOfPriceType = get_type_table(model_name='ProductBenefitShareOfPrice',
                                                table_name='product_benefit_share_of_price')

ProductBenefitShareOfSumAssuredType = get_type_table(model_name='ProductBenefitShareOfSumAssured',
                                                     table_name='product_benefit_share_of_sum_assured')

columns_tbl_product_benefit_payment_frequency = {
    '__tablename__': 'tbl_product_benefit_payment_frequency',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'number_of_payments': common_columns.get('integer_default')(default=1),
    'product_frequency_type_id': common_columns.get('integer_not_nullable')()
}
ProductBenefitPaymentFrequency = get_phat_table(model_name='ProductBenefitPaymentFrequency',
                                                columndict=columns_tbl_product_benefit_payment_frequency)

columns_tbl_product_benefit_share_of_sum_assured_percentage = {
    '__tablename__': 'tbl_product_benefit_share_of_sum_assured_percentage',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'percentage': common_columns.get('percentage_not_nullable')()
}
ProductBenefitShareOfSumAssuredPercentage = \
    get_phat_table(model_name='ProductBenefitShareOfSumAssuredPercentage',
                   columndict=columns_tbl_product_benefit_share_of_sum_assured_percentage)

columns_tbl_product_benefit_share_of_sum_assured_amount = {
    '__tablename__': 'tbl_product_benefit_share_of_sum_assured_amount',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')()
}
ProductBenefitShareOfSumAssuredAmount = \
    get_phat_table(model_name='ProductBenefitShareOfSumAssuredAmount',
                   columndict=columns_tbl_product_benefit_share_of_sum_assured_amount)

columns_tbl_product_benefit_share_of_sum_assured_stated_benefit = {
    '__tablename__': 'tbl_product_benefit_share_of_sum_assured_stated_benefit',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'stated_benefit_id': common_columns.get('integer_not_nullable')()
}
ProductBenefitShareOfSumAssuredStatedBenefit = \
    get_phat_table(model_name='ProductBenefitShareOfSumAssuredStatedBenefit',
                   columndict=columns_tbl_product_benefit_share_of_sum_assured_stated_benefit)

columns_tbl_stated_benefit_table = {
    '__tablename__': 'tbl_stated_benefit',
    'name': common_columns.get('title')()
}
StatedBenefit = get_phat_table(model_name='StatedBenefit', columndict=columns_tbl_stated_benefit_table)

columns_tbl_stated_benefit_line_item = {
    '__tablename__': 'tbl_stated_benefit_line_item',
    'stated_benefit_id': common_columns.get('integer_not_nullable')()
}
StatedBenefitLineItem = get_phat_table(model_name='StatedBenefitLineItem',
                                            columndict=columns_tbl_stated_benefit_line_item)

columns_tbl_product_benefit_share_of_price_amount = {
    '__tablename__': 'tbl_product_benefit_share_of_price_amount',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency_not_nullable')()
}
ProductBenefitShareOfPriceAmount = get_phat_table(model_name='ProductBenefitShareOfPriceAmount',
                                                  columndict=columns_tbl_product_benefit_share_of_price_amount)

columns_tbl_product_benefit_share_of_price_percentage = {
    '__tablename__': 'tbl_product_benefit_share_of_price_percentage',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'percentage': common_columns.get('percentage_not_nullable')()
}
ProductBenefitShareOfPricePercentage = get_phat_table(model_name='ProductBenefitShareOfPricePercentage',
                                                      columndict=columns_tbl_product_benefit_share_of_price_percentage)

# ---------------------------- ProductBenefit Frequencies and Periods -----------------------------------

# ProductBenefitFrequencyType, ProductBenefitPeriodType, ProductBenefitPeriodEffectType, ProductBenefitPeriod

ProductBenefitFrequencyType = get_type_table(model_name='ProductBenefitFrequency', table_name='product_benefit_frequency')

ProductBenefitPeriodType = get_type_table(model_name='ProductBenefitPeriod', table_name='product_benefit_period')

ProductBenefitPeriodEffectType = get_type_table(model_name='ProductBenefitPeriodEffect', table_name='product_benefit_period_effect')

columns_tbl_product_benefit_period = {
    '__tablename__': 'tbl_product_benefit_period',
    'product_benefit_id': common_columns.get('integer_not_nullable')(),
    'product_benefit_period_effect_type_id': common_columns.get('integer')(),
    'product_benefit_period_type_id': common_columns.get('integer_not_nullable')(),
    'time_period': common_columns.get('integer')()
}
ProductBenefitPeriod = get_phat_table(model_name='ProductBenefitPeriod', columndict=columns_tbl_product_benefit_period)
