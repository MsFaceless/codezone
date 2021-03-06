# -*- coding: utf-8 -*-
"""GroupController controller module"""

import os
import json
import requests
from datetime import datetime
from pkg_resources import resource_filename

from tg import predicates
from tg import expose, require, redirect, validate, flash, url, request, response

from rocket.model import *

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController
from rocket.lib.tgfileuploader import FileUploader
from rocket.lib.tg_generic_reportlab import PDFCreator, Paragraph

from sqlalchemy import func, desc, asc

FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
IMAGES_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'images')
CATALOG_DIRNAME = os.path.join(IMAGES_DIRNAME, 'catalog_pictures')

SEARCHKEY_GROUP = 'Organisation_SearchKeyword'
SEARCHKEY_MEMBER = 'Members_SearchKeyword'
SEARCHKEY_MEMBER_GROUP_ID = 'Members_Group_ID_SearchKeyword'

LIMIT = 20

__all__ = ['CommonController']

class CommonController(BaseController):
    """Docstring for CommonController."""

    def get_groups_list(self, *args, **kwargs):
        return []

    def get_selectbox_groups(self, *args, **kwargs):
        group_type_id = kwargs.get('group_type_id', None)
        usernow = request.identity.get('user', {})
        outputlist = []
        dbase_query = self.get_groups_list()
        for rocketgroup, group in dbase_query:
            if group_type_id and rocketgroup.group_type_id == group_type_id:
                outputlist.append({'id' : rocketgroup.id, 'name' : group.get('name')})
            elif not group_type_id:
                outputlist.append({'id' : rocketgroup.id, 'name' : group.get('name')})
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_gender(self, *args, **kwargs):
        kwargs['outputlist'] = [{'name' : m.name, 'id' : m.value} for m in Gender]
        return create_selectbox_html(**kwargs)

    def get_postal_address_html(self, *args, **kwargs):
        postal = kwargs.get('postal', {})
        form_id = kwargs.get('postal_form_id', None)
        address1 = postal.get('address1') if postal else ''
        if not address1: address1 = ''
        address2 = postal.get('address2') if postal else ''
        if not address2: address2 = ''
        address3 = postal.get('address3') if postal else ''
        if not address3: address3 = ''
        postal_code = postal.get('postal_code') if postal else ''
        if not postal_code: postal_code = ''
        hidden_input = self.get_hidden_input(**{'id': 'postal_id', 'value': postal.get('id')}) if postal else ''
        html = f"""
        <form id='{form_id}'>
            {hidden_input}
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Postal Address</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="address1" value='{address1}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label"></label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="address2" value='{address2}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label"></label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="address3" value='{address3}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Postal Code</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='10' name="postal_code" value='{postal_code}'>
                        </div>
                    </div>
                </div>
            </div>
        </form>
        """
        return html

    def get_street_address_html(self, *args, **kwargs):
        street = kwargs.get('street', {})
        form_id = kwargs.get('street_form_id', None)

        country_selected = street.get('country_id') if street else ''
        country_kwargs = {'id' : 'country_id', 'selected' : country_selected}
        selectbox_country = self.get_selectbox_countries(**country_kwargs)

        region_selected = street.get('region_id') if street else ''
        region_kwargs = {'id' : 'region_id', 'selected' : region_selected, 'country_id' : country_selected}
        selectbox_region = self.get_selectbox_regions(**region_kwargs)

        address1 = street.get('address1') if street else ''
        if not address1: address1 = ''
        address2 = street.get('address2') if street else ''
        if not address2: address2 = ''
        address3 = street.get('address3') if street else ''
        if not address3: address3 = ''
        postal_code = street.get('postal_code') if street else ''
        if not postal_code: postal_code = ''
        hidden_input = self.get_hidden_input(**{'id': 'street_id', 'value': street.get('id')}) if street else ''
        html = f"""
        <form id='{form_id}'>
            {hidden_input}
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Country</label>
                        <div class="col-md-9">
                            {selectbox_country}
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Region</label>
                        <div id='div_region' class="col-md-9">
                            {selectbox_region}
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Street Address</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name='address1' value='{address1}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label"></label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="address2" value='{address2}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label"></label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="address3" value='{address3}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Postal Code</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='10' name='postal_code' value='{postal_code}'>
                        </div>
                    </div>
                </div>
            </div>
        </form>
        """
        javascript = """
        <script>
            $('#country_id').change(function(){
                var region_selected = $('#region_id option: selected').val();
                if(!region_selected){
                    var kwargs = 'id=region_id&required=true&country_id='+$('#country_id option: selected').val();
                    $('#div_region').load('/common/get_selectbox_regions', kwargs, function(data){
                        return false;
                    });
                };
            });
            $('#country_id').trigger('change');
        </script>
        """
        return html + javascript

    def get_selectbox_countries(self, *args, **kwargs):
        kwargs['outputlist'] = [] 
        return create_selectbox_html(**kwargs)

    @expose()
    def get_selectbox_regions(self, *args, **kwargs):
        kwargs['outputlist'] = [] 
        return create_selectbox_html(**kwargs)

    def get_selectbox_banks(self, *args, **kwargs):
        kwargs['outputlist'] = [] 
        return create_selectbox_html(**kwargs)

    def get_selectbox_bank_account_types(self, *args, **kwargs):
        kwargs['outputlist'] = [{'name' : m.name, 'id' : m.value} for m in BankAccountType]
        return create_selectbox_html(**kwargs)

    def get_bank_account_html(self, *args, **kwargs):
        bank = kwargs.get('bank', {})
        form_id = kwargs.get('bank_form_id', None)
        bank_selected = bank.get('bank_id') if bank else ''
        bank_kwargs = {'id' : 'bank_id', 'selected' : bank_selected}
        selectbox_banks = self.get_selectbox_banks(**bank_kwargs)
        type_selected = bank.get('bank_account_type_id') if bank else ''
        type_kwargs = {'id' : 'bank_account_type_id', 'selected' : type_selected}
        selectbox_bankaccounttypes = self.get_selectbox_bank_account_types(**type_kwargs)
        account_number = bank.get('account_number') if bank else ''
        if not account_number: account_number = ''
        account_holder = bank.get('account_holder') if bank else ''
        if not account_holder: account_holder = ''
        branch_code = bank.get('branch_code') if bank else ''
        if not branch_code: branch_code = ''
        hidden_input = self.get_hidden_input(**{'id': 'this_bank_id', 'value': bank.get('id')}) if bank else ''
        html = f"""
        <form id='{form_id}'>
            {hidden_input}
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Bank</label>
                        <div class="col-md-9">
                            {selectbox_banks}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Account number</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="account_number" value='{account_number}'>
                        </div>
                    </div>
                </div>
            </div>
            <div class="row">
                <div class="col-md-6">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Account Type</label>
                        <div class="col-md-9">
                            {selectbox_bankaccounttypes}
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Account Holder</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='255' name="account_holder" value='{account_holder}'>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">Branch Code</label>
                        <div class="col-md-9">
                            <input type="text" class="form-control" maxlength='50' name="branch_code" value='{branch_code}'>
                        </div>
                    </div>
                </div>
            </div>
        </form>
        """
        return html

    def get_hidden_input(self, *args, **kwargs):
        input_id = kwargs.get('id', 'id')
        input_value = kwargs.get('value', None)
        return f"""<input style='display: none;' type="text" id="{input_id}" name="{input_id}" class="form-control" value="{input_value}"/>"""

    def get_session_key(self, searchkey):
        key = DBSession.query(SessionKey). \
                filter(SessionKey.name==searchkey). \
                first()
        if key: return key
        return self.set_session_key(searchkey)

    def set_session_key(self, searchkey):
        new = SessionKey()
        new.name = searchkey
        DBSession.add(new)
        DBSession.flush()
        return new

    def get_session_value(self, searchkey):
        usernow = request.identity.get('user', {})
        key = self.get_session_key(searchkey)
        return DBSession.query(SessionValue). \
                filter(SessionValue.key_id==key.id). \
                filter(SessionValue.user_id==usernow.id). \
                first()

    def set_session_value(self, searchkey, searchphrase):
        value = self.get_session_value(searchkey)
        if not value: return self.create_session_value(searchkey, searchphrase)
        value.value = searchphrase
        DBSession.flush()
        return searchphrase

    def create_session_value(self, searchkey, searchphrase):
        usernow = request.identity.get('user', {})
        key = self.get_session_key(searchkey)
        new = SessionValue()
        new.key_id = key.id
        new.user_id = usernow.id
        new.value = searchphrase
        DBSession.add(new)
        DBSession.flush()
        return searchphrase

    def delete_session_value(self, searchkey):
        usernow = request.identity.get('user', {})
        value = self.get_session_value(searchkey)
        if value: DBSession.delete(value)
        return ''

    def get_searchphrase(self, *args, **kwargs):
        searchkey = kwargs.get('searchkey', None)
        if not searchkey: return ''
        reset = kwargs.get('reset', False)
        if reset: return self.delete_session_value(searchkey)
        searchphrase = kwargs.get('searchphrase', None)
        if not searchphrase:
            value = self.get_session_value(searchkey)
            return value.value if value else ''
        return self.set_session_value(searchkey, searchphrase)

    def check_usernow_has_role(self, role=None):
        if not role: return False
        usernow = request.identity.get('user')
        exists = DBSession.query(Role). \
                filter(Role.name==role). \
                first()
        return True if (exists and exists in usernow.roles) else False
