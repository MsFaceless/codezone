# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_phat_table, get_type_table

# ********************* Payment ***********************************#

PaymentType = get_type_table(model_name='Payment', table_name='payment')
PaymentTransactionType = get_type_table(model_name='PaymentTransaction', table_name='payment_transaction')
PaymentTransactionDebitCreditType = get_type_table(model_name='PaymentTransactionDebitCredit', table_name='payment_transaction_debit_credit')

columns_tbl_payment = {
    '__tablename__': 'tbl_payment',
    'policy_id': common_columns.get('integer')(),
    'payment_date': common_columns.get('datetime')(),
    'registration_date': common_columns.get('datetime')(),
    'registration_by_id': common_columns.get('integer')(),
    'payment_type_id': common_columns.get('integer')(),
    'payment_transaction_type_id': common_columns.get('integer')(),
    'currency_id': common_columns.get('integer')(),
    'receipt_number': common_columns.get('description')(),
    'message': common_columns.get('description')(),
    'payment_post_method_id': common_columns.get('integer')(),
    'bank_reference': common_columns.get('description')()
}
Payment = get_phat_table(model_name='Payment', columndict=columns_tbl_payment)

columns_tbl_payment_link = {
    '__tablename__': 'tbl_payment_link',
    'payment_id': common_columns.get('integer')(),
    'contra_payment_id': common_columns.get('integer')(),
}
PaymentLink = get_phat_table(model_name='PaymentLink', columndict=columns_tbl_payment_link)

columns_tbl_payment_credit = {
    '__tablename__': 'tbl_payment_credit',
    'payment_id': common_columns.get('integer')(),
    'amount': common_columns.get('currency')(),
}
PaymentCredit = get_phat_table(model_name='PaymentCredit', columndict=columns_tbl_payment_credit)

columns_tbl_payment_debit = {
    '__tablename__': 'tbl_payment_debit',
    'payment_id': common_columns.get('integer')(),
    'amount': common_columns.get('currency')(),
}
PaymentDebit = get_phat_table(model_name='PaymentDebit', columndict=columns_tbl_payment_debit)

columns_tbl_payment_post_method = {
    '__tablename__': 'tbl_payment_post_method',
    'name': common_columns.get('description')(),
}
PaymentPostMethod = get_phat_table(model_name='PaymentPostMethod', columndict=columns_tbl_payment_post_method)

# ********************* Transaction ***********************************#

TransactionExtractStatusType = get_type_table(model_name='TransactionExtractStatus', table_name='transaction_extract_status')

columns_tbl_transaction = {
    '__tablename__': 'tbl_transaction',
    'policy_id': common_columns.get('integer_not_nullable')(),
    'transaction_extract_status_type_id': common_columns.get('integer_not_nullable')(),
    'amount': common_columns.get('currency')(),
    'general_ledger_account_id': common_columns.get('integer')(),
}
Transaction = get_phat_table(model_name='Transaction', columndict=columns_tbl_transaction)

columns_tbl_transaction_product_allocation_link = {
    '__tablename__': 'tbl_transaction_product_allocation_link',
    'transaction_id': common_columns.get('integer')(),
    'product_allocation_link_id': common_columns.get('integer')()
}
TransactionProductAllocationLink = get_phat_table(model_name='TransactionProductAllocationLink', columndict=columns_tbl_transaction_product_allocation_link)

columns_tbl_transaction_product_benefit_allocation_link = {
    '__tablename__': 'tbl_transaction_product_benefit_allocation_link',
    'transaction_id': common_columns.get('integer')(),
    'product_benefit_allocation_link_id': common_columns.get('integer')()
}
TransactionProductBenefitAllocationLink = get_phat_table(model_name='TransactionProductBenefitAllocationLink', columndict=columns_tbl_transaction_product_benefit_allocation_link)

columns_tbl_transaction_claim_schedule = {
    '__tablename__': 'tbl_transaction_claim_schedule',
    'transaction_id': common_columns.get('integer')(),
    'claim_payout_schedule_id': common_columns.get('integer')()
}
TransactionClaimSchedule = get_phat_table(model_name='TransactionClaimSchedule', columndict=columns_tbl_transaction_claim_schedule)

columns_tbl_transaction_payment = {
    '__tablename__': 'tbl_transaction_payment',
    'transaction_id': common_columns.get('integer')(),
    'payment_id': common_columns.get('integer')()
}
TransactionPayment = get_phat_table(model_name='TransactionPayment', columndict=columns_tbl_transaction_payment)
