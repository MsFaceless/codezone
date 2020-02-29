# -*- coding: utf-8 -*-

import os
from datetime import datetime
from hashlib import sha256

from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Unicode, Integer, DateTime, Boolean
from sqlalchemy.orm import relation, synonym

from rocket.model import DeclarativeBase, metadata, DBSession
from rocket.lib.model_utils import PhatBase, common_columns, get_phat_table, get_type_table

# ********************* Entity Types ***********************************#

EntityType = get_type_table(model_name='Entity', table_name='entity')
EntityOrganisationType = get_type_table(model_name='EntityOrganisation', table_name='entity_organisation')
EntityOrganisationContactType = get_type_table(model_name='EntityOrganisationContact', table_name='entity_organisation_contact')
EntityOrganisationAddressType = get_type_table(model_name='EntityOrganisationAddress', table_name='entity_organisation_address')

# ********************* Entity ***********************************#

columns_tbl_entity = {
    '__tablename__': 'tbl_entity',
    'entity_type_id': common_columns.get('integer_not_nullable')(),
}
Entity = get_phat_table(model_name='Entity', columndict=columns_tbl_entity)

columns_tbl_entity_person = {
    '__tablename__': 'tbl_entity_person',
    'entity_id': common_columns.get('integer_not_nullable')(),
    'person_id': common_columns.get('integer_not_nullable')(),
    'identity_number': common_columns.get('description')(),
}
EntityPerson = get_phat_table(model_name='EntityPerson', columndict=columns_tbl_entity_person)

columns_tbl_entity_person_relationship_link = {
    '__tablename__': 'tbl_entity_person_relationship_link',
    'entity_person_id': common_columns.get('integer_not_nullable')(),
    'relation_entity_person_id': common_columns.get('integer_not_nullable')(),
    'relationship_type_id': common_columns.get('integer_not_nullable')(),
    'is_beneficiary': common_columns.get('boolean_default_false')(),
}
EntityPersonRelationshipLink = get_phat_table(model_name='EntityPersonRelationshipLink', columndict=columns_tbl_entity_person_relationship_link)

columns_tbl_entity_organisation = {
    '__tablename__': 'tbl_entity_organisation',
    'entity_id': common_columns.get('integer_not_nullable')(),
    'entity_organisation_type_id': common_columns.get('integer_not_nullable')(),
    'code': common_columns.get('description_not_nullable')(),
    'name': common_columns.get('description_not_nullable')(),
    'tax_number': common_columns.get('description_not_nullable')(),
    'registration_number': common_columns.get('description_not_nullable')(),
    'financial_regulatory_number': common_columns.get('description_not_nullable')()
}
EntityOrganisation = get_phat_table(model_name='EntityOrganisation', columndict=columns_tbl_entity_organisation)

# ********************* Entity Organisation ***********************************#

columns_tbl_entity_organisation_contact = {
    '__tablename__': 'tbl_entity_organisation_contact',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
    'entity_organisation_contact_type_id': common_columns.get('integer_not_nullable')(),
    'name': common_columns.get('description')(),
    'value': common_columns.get('description')(),
    'preferred': common_columns.get('boolean_default_false')(),
}
EntityOrganisationContact = get_phat_table(model_name='EntityOrganisationContact', columndict=columns_tbl_entity_organisation_contact)

columns_tbl_organisation_bank_account_link = {
    '__tablename__': 'tbl_organisation_bank_account_link',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
    'bank_account_id': common_columns.get('integer_not_nullable')(),
}
EntityOrganisationBankAccountLink = get_phat_table(model_name='EntityOrganisationBankAccountLink',
                                             columndict=columns_tbl_organisation_bank_account_link)

columns_tbl_organisation_address = {
    '__tablename__': 'tbl_organisation_address',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
    'entity_organisation_address_type_id': common_columns.get('integer_not_nullable')(),
    'address_id': common_columns.get('integer_not_nullable')(),
}
EntityOrganisationAddress = get_phat_table(model_name='EntityOrganisationAddress',
                                         columndict=columns_tbl_organisation_address)

# ********************* Entity Organisation Client ***********************************#

columns_tbl_entity_organisation_client = {
    '__tablename__': 'tbl_entity_organisation_client',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
    'billing_frequency_id': common_columns.get('integer_not_nullable')(),
}
EntityOrganisationClient = get_phat_table(model_name='EntityOrganisationClient', columndict=columns_tbl_entity_organisation_client)

columns_tbl_entity_organisation_client_person_link = {
    '__tablename__': 'tbl_entity_organisation_client_person_link',
    'entity_organisation_client_id': common_columns.get('integer_not_nullable')(),
    'entity_person_id': common_columns.get('integer_not_nullable')(),
}
EntityOrganisationClientPersonLink = get_phat_table(model_name='EntityOrganisationClientPersonLink', columndict=columns_tbl_entity_organisation_client_person_link)

# ********************* Entity Organisation Product Owner ***********************************#

columns_tbl_entity_organisation_product_owner = {
    '__tablename__': 'tbl_entity_organisation_product_owner',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
    'policy_number_prefix': common_columns.get('description')(),
}
EntityOrganisationProductOwner = get_phat_table(model_name='EntityOrganisationProductOwner', columndict=columns_tbl_entity_organisation_product_owner)

# ********************* Entity Organisation Insurer ***********************************#

columns_tbl_entity_organisation_insurer = {
    '__tablename__': 'tbl_entity_organisation_insurer',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
}
EntityOrganisationInsurer = get_phat_table(model_name='EntityOrganisationInsurer', columndict=columns_tbl_entity_organisation_insurer)

# ********************* Entity Organisation Intermediary ***********************************#

columns_tbl_entity_intermediary = {
    '__tablename__': 'tbl_entity_intermediary',
    'entity_organisation_id': common_columns.get('integer_not_nullable')(),
    'entity_intermediary_disclosure_id': common_columns.get('integer')(),
}
EntityOrganisationIntermediary = get_phat_table(model_name='EntityOrganisationIntermediary', columndict=columns_tbl_entity_intermediary)

columns_tbl_entity_intermediary_agent = {
    '__tablename__': 'tbl_entity_intermediary_agent',
    'entity_organisation_intermediary_id': common_columns.get('integer_not_nullable')(),
    'entity_person_id': common_columns.get('integer_not_nullable')(),
    'code': common_columns.get('description_not_nullable')(),
    'termination_date': common_columns.get('date')(),
    'financial_regulatory_number': common_columns.get('description_not_nullable')()
}
EntityOrganisationIntermediaryAgent = get_phat_table(model_name='EntityOrganisationIntermediaryAgent', columndict=columns_tbl_entity_intermediary_agent)

columns_tbl_entity_organisation_intermediary_disclosure = {
    '__tablename__': 'tbl_entity_organisation_intermediary_disclosure',
    'text': common_columns.get('longtext_not_nullable')(),
}
EntityOrganisationIntermediaryDisclosure = get_phat_table(model_name='EntityOrganisationIntermediaryDisclosure',
                                              columndict=columns_tbl_entity_organisation_intermediary_disclosure)
