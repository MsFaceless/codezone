# -*- coding: utf-8 -*-
"""Policy controller module"""

from tg import predicates, require
from tg import expose, redirect, validate, flash, url, request
from datetime import datetime, date

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from sqlalchemy import func, desc, asc

from rocket.model import *

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController
from rocket.lib.type_utils import TypeDictionary
from rocket.controllers.members import MemberController
import rocket.lib.vault_utils as vault

TYPEUTIL = TypeDictionary()

DBQUERY_LIMIT = 15
POLICY_NUMBER_MAX_LENGTH = 20

class PolicyController(BaseController):

    def __init__(self, *args, **kwargs):
        #self.address_type_list = vault.get_address_type_list()
        #self.contact_type_list = vault.get_contact_type_list()
        #self.identity_type_list = vault.get_identity_type_list()
        #self.bankaccount_type_list = vault.get_bankaccount_type_list()
        #self.person_title_type_list = vault.get_person_title_type_list()
        #self.person_gender_type_list = vault.get_person_gender_type_list()
        pass

##################################################################################################################
# Policy - New
##################################################################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def new(self, *args, **kwargs):
        html = ''
        javascript = ''
        title = _("New Policy")
        return dict(title=title, html=html, javascript=javascript)

##################################################################################################################
# Policy - List
##################################################################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_policies_html(*args, **kwargs)
        javascript = self.get_javascript_policy_onload()
        title = _("Policies")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_policies_html(self, *args, **kwargs):
        outputlist = []
        dbase_query = Policy.get_limit(DBQUERY_LIMIT, 'policy_number')
        for item in dbase_query:
            # Policy Holder
            entity_policy_holder = EntityPerson.by_attr_first('entity_id', item.entity_policy_holder_id)
            personobj_policy_holder = vault.get_personobj_by_id(entity_policy_holder.person_id)
            policy_holder = personobj_policy_holder.get('person', {})
            policy_holder_full_name = f"{policy_holder.get('firstname', '')} {policy_holder.get('surname', '')}"
            # Policy Owner
            policy_owner_full_name = None
            entity_policy_owner = EntityPerson.by_attr_first('entity_id', item.entity_policy_owner_id)
            if entity_policy_owner:
                personobj_policy_owner = vault.get_personobj_by_id(entity_policy_owner.person_id)
                if personobj_policy_owner:
                    policy_owner = personobj_policy_owner.get('person', {})
                    policy_owner_full_name = f"{policy_owner.get('firstname', '')} {policy_owner.get('surname', '')}"

            policy_state_name = None
            state = PolicyState.by_attr_first('policy_id', item.id)
            if state:
                policy_state_name = TYPEUTIL.get_pretty_name('policy_state_type', state.policy_state_type_id)

            #product = Product.by_id(item.product_id)
            product = DBSession.query(Product).filter(Product.id==item.product_id).one()
            outputlist.append({
                'policy_number': f"<div class='edit policy_edit action_link' policy_id='{item.id}'>{item.policy_number}</div>",
                'policy_holder':  policy_holder_full_name,
                'policy_owner': policy_owner_full_name,
                'product' : product.name,
                'state': policy_state_name,
            })
        dbcolumnlist = [
            'policy_number',
            'policy_holder',
            'policy_owner',
            'product',
            'state',
        ]
        theadlist = [
            'Policy Number',
            'Policy Holder',
            'Policy Owner',
            'Product',
            'State'
        ]
        tdclasslist = [
            'action_link',
            'text-left',
            'text-left',
            'text-left',
            'text-left',
        ]
        htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "policy_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                 <h4 class="card-title">{_('Policies')}</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_policy" class="btn btn-primary ml-auto">Create New Policy</button>
                            </div>
                        </div>
                        <div class="row d-flex align-items-center">
                            <div class="col-md-4 d-flex">
                                <input id='search' type="text" class="form-control mr-2 search" name="searchphrase" placeholder="Search by Code or Description">
                            </div>
                            <div class="col-md-4 pl-0">
                                <button id='btn_search' class="btn btn-primary action_search">Search</button>
                                <button id='btn_reset' class="btn btn-primary">Reset</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div id='div_policy_table' class="table-responsive">
                            {htmltbl}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_javascript_policy_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_policy").click(function(){
            $('#dialogdiv').load('/policy/get_modal_new_policy?', function(data){
                return false;
            });
        });
        $(".policy_edit").click(function(){
            var policy_id = $(this).attr('policy_id');
            var kwargs = {'policy_id' : policy_id};
            $.redirect('/policy/short_term_edit', kwargs);
        });
        """
        return javascript

    @expose()
    def get_modal_new_policy(self, *args, **kwargs):
        dbase_query = self.get_dbase_query_entity_person(*args, **kwargs)
        outputlist = []
        for entity_person in dbase_query:
            # Person from Vault
            personobj = vault.get_personobj_by_id(entity_person.person_id)
            if not personobj: continue
            #personobj = {}
            person = personobj.get('person', {})
            # Person Identity
            identity_number = None
            identitylist = personobj.get('identities', [])
            if len(identitylist) >= 1: identity_number = identitylist[0].get('number', None)
            # Person Mobile
            mobile = None
            contactlist = personobj.get('contacts', [])
            if len(contactlist) >= 1: mobile = contactlist[0].get('value', None)
            # Radio for selection
            radio = create_radio_html(**{'class' : 'policy_create',
                                         'name_key' : 'entity_id',
                                         'name_value' : entity_person.entity_id,
                                         'id_key' : 'entity_id',
                                         'id_value' : entity_person.entity_id })
            outputlist.append({
                'radio' : radio,
                'idnumber' : identity_number,
                'name': person.get('firstname', ''),
                'surname': person.get('surname', ''),
                'mobile': mobile,
                             })
        dbcolumnlist=[
                'radio',
                'idnumber',
                'name',
                'surname',
                'mobile',
                    ]
        theadlist=[
                '',
                _('ID Number'),
                _('First Name'),
                _('Surname'),
                _('Mobile Number'),
                ]
        tdclasslist = [
                'action_link',
                '',
                '',
                '',
                'text-right',
        ]
        htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "member_table", tdclasslist)
        selectbox_products = self.get_selectbox_products()
        html = f"""
        <div class="modal fade" id="dialog_new_policy" tabindex="-1" role="dialog" aria-labelledby="myproductLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-xl">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-8">
                            <h4 class="card-title">Create New Policy: Select a Product and Member</h4>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-4">
                                {selectbox_products}
                            </div>
                            <div class="col-md-4">
                                <input type="text" class="form-control search" name="searchphrase" placeholder="{_('Search by ID Number, Name or Surname')}">
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-primary action_search">{_('Search')}</button>
                                <button class="btn btn-primary">{_('Reset')}</button>
                            </div>
                        </div>
                        <div class="table-responsive">
                            {htmltbl}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $(".action_search").click(function(){
                var kwargs = 'searchphrase='+$('#searchphrase').val();
                console.log(kwargs);
            });
            $(".policy_create").click(function(){
                var product_id = $('#product_id option:selected').val();
                if(product_id){
                    var kwargs = 'product_id='+product_id;
                    kwargs += '&entity_id='+$(this).attr('entity_id');
                    $.post('/policy/create_new_policy?', kwargs, function(data){
                        if(data){
                            var kwargs = {'policy_id' : data};
                            $.redirect('/policy/short_term_edit', kwargs);
                            return false;
                        };
                    });
                }else{
                    $('#product_id').focus();
                };
            });
            $('.policy_back').click(function(){
                $('#dialog_new_policy').modal('hide');
            });
            $('#dialog_new_policy').modal();
        </script>
        """
        return html + javascript

    def get_selectbox_products(self, *args, **kwargs):
        kwargs['id'] = 'product_id'
        active = TYPEUTIL.get_id_of_name('product_state_type', 'active')
        dbase_query = DBSession.query(Product). \
                filter(Product.active==True). \
                order_by(asc(Product.code)). \
                all()
                #filter(Product.product_state_id==active). \
        kwargs['outputlist'] = [{'name': f"{x.code}: {x.name}", 'id': x.id} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    @expose()
    def get_dbase_query_entity_person(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)
        if searchphrase:
            print('DO THE SEARCH NOW')
            return []
        return DBSession.query(EntityPerson). \
            filter(EntityPerson.active==True). \
            order_by(desc(EntityPerson.person_id)). \
            limit(DBQUERY_LIMIT)
            #order_by(desc(EntityPerson.person_id)). \

    @expose()
    def create_new_policy(self, *args, **kwargs):
        usernow = request.identity['user']
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        individual = TYPEUTIL.get_id_of_name('policy_type', 'individual')
        policy_number = self.get_unique_policy_number(product_id)
        if not policy_number: return ''
        this = Policy()
        this.product_id = product_id
        this.policy_number = policy_number
        this.entity_policy_holder_id = kwargs.get('entity_id', None)
        this.policy_type_id = individual
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()

        proposal = TYPEUTIL.get_id_of_name('policy_state_type', 'proposal')
        state = PolicyState()
        state.policy_id = this.id
        state.policy_state_type_id = proposal
        state.added_by = usernow.id
        DBSession.add(state)
        DBSession.flush()
        return str(this.id)

    def get_unique_policy_number(self, product_id=None, *args, **kwargs):
        if not product_id: return False
        product = Product.by_id(product_id)
        if not product: return False

        product_prefix = ''
        if product.policy_number_prefix:
            product_prefix = product.policy_number_prefix.strip().upper()

        product_owner_prefix = ''
        product_owner = EntityOrganisationProductOwner.by_id(product.product_owner_id)
        if product_owner and product_owner.policy_number_prefix:
            product_owner_prefix = product_owner.policy_number_prefix.strip().upper()

        number = datetime.now().strftime("%y%m%d%H%M%S%f")
        policy_number = product_prefix + product_owner_prefix + number
        policy_number = policy_number[: POLICY_NUMBER_MAX_LENGTH]

        exists = Policy.by_attr_first('policy_number', policy_number)
        if exists: return self.get_unique_policy_number(product_id)
        return policy_number

##################################################################################################################
# Short Term - Edit
##################################################################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def short_term_edit(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        if not policy_id: redirect('/policy/index')
        policy = Policy.by_id(policy_id)
        if not policy: redirect('/policy/index')
        html = self.get_short_term_edit_html(policy)
        javascript = self.get_javascript_short_term_onload()
        title = f"Policy: {policy.policy_number}"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_javascript_short_term_onload(self, *args, **kwargs):
        javascript = """
        $("#btn_policy_back").click(function(){
            $.redirect('/policy/index');
        });
        $(".open_short_term").click(function(){
            var kwargs = 'product_benefit_id='+$(this).attr('product_benefit_id');
            kwargs += '&policy_id='+$(this).attr('policy_id');
            $('.nav-link:eq(1)').trigger('click');
            $('#tab2').load('/policy/get_short_term_edit_benefit_assets?', kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_short_term_edit_html(self, policy=None, *args, **kwargs):
        if not policy: redirect('/policy/index')

        # HEADER
        card_header = self.get_short_edit_header_html(policy)

        # TAB 1
        tab1_content = self.get_short_term_benefits_html(policy)

        # TAB 2
        tab2_content = self.get_short_term_edit_benefit_assets(policy)

        # TAB 3
        tab3_content = self.get_short_term_edit_summary(policy)

        # TAB 4
        tab4_content = self.get_short_term_edit_documents(policy)

        # TAB 5
        tab5_content = self.get_short_term_edit_transaction(policy)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    <ul class="nav nav-pills nav-pills-primary justify-content-center" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#tab1" role="tablist">
                                Benefits
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab2" role="tablist">
                                Benefit Assets
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab3" role="tablist">
                                Summary
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab4" role="tablist">
                                Documents
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab5" role="tablist">
                                Transaction
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="tab-content tab-space tab-subcategories">
                    <div class="tab-pane active" id="tab1">
                        {tab1_content}
                    </div>
                    <div class="tab-pane" id="tab2">
                        {tab2_content}
                    </div>
                    <div class="tab-pane" id="tab3">
                        {tab3_content}
                    </div>
                    <div class="tab-pane" id="tab4">
                        {tab4_content}
                    </div>
                    <div class="tab-pane" id="tab5">
                        {tab5_content}
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_short_term_edit_benefit_assets_error(self, *args, **kwargs):
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Assets for: ')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    Please select a Policy Benefit to continue.
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_policy_benefit_employee_asset_temp_html(self, policy_id=None, *args, **kwargs):
        if not policy_id: return ''
        dbase_query = PolicyBenefitEmployeeAssetTemp.by_attr_all('policy_id', policy_id)
        outputlist = []
        for item in dbase_query:
            asset = ProductBenefitAssetPremiumRateEmployeeLineItemTemp.by_id(item.asset_premium_rate_employee_line_item_id)
            outputlist.append({
                #'name' : "<div class='edit policy_benefit_employee_asset_temp_edit' policy_benefit_employee_asset_temp_id='{1}'>{0}</div>".format(item.name, item.id),
                'count' : f"{asset.minimum_employees_coverable} - {asset.maximum_employees_coverable}",
                'surname' : item.name,
                'amount' : getcurrency(asset.amount),
                             })
        dbcolumnlist=[
                #'name',
                'count',
                'surname',
                'amount',
                    ]
        theadlist=[
                #'Name',
                'Count',
                'Description',
                'Amount',
                ]
        tdclasslist = [
                '',
                '',
                'text-right',
                ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_employee_asset_temp_table", tdclasslist)

    @expose()
    def get_policy_benefit_property_asset_temp_html(self, policy_id=None, *args, **kwargs):
        if not policy_id: return ''
        dbase_query = PolicyBenefitPropertyAssetTemp.by_attr_all('policy_id', policy_id)
        outputlist = []
        for item in dbase_query:
            asset = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_id(item.asset_premium_rate_turnover_line_item_id)
            outputlist.append({
                #'number_of_premises' : "<div class='edit policy_benefit_property_asset_temp_edit' policy_benefit_property_asset_temp_id='{1}'>{0}</div>".format(item.number_of_premises, item.id),
                #'is_owned' : item.is_owned,
                #'is_shared' : item.is_shared,
                #'number_of_shared' : item.number_of_shared,
                'turnover' : f"{asset.minimum_turnover} - {asset.maximum_turnover}",
                'description' : item.description,
                'amount' : getcurrency(asset.amount),
                             })
        dbcolumnlist=[
                #'number_of_premises',
                #'is_owned',
                #'is_shared',
                #'number_of_shared',
                'turnover',
                'description',
                'amount',
                    ]
        theadlist=[
                #'Number Of Premises',
                #'Is_Owned',
                #'Is_Shared',
                #'Number Of Shared',
                'Turnover',
                'Description',
                'Amount',
                ]
        tdclasslist = [
                '',
                '',
                'text-right',
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_property_asset_temp_table", tdclasslist)

    @expose()
    def get_policy_benefit_vehicle_asset_temp_html(self, policy_id=None, *args, **kwargs):
        if not policy_id: return ''
        dbase_query = PolicyBenefitVehicleAssetTemp.by_attr_all('policy_id', policy_id)
        outputlist = []
        for item in dbase_query:
            asset = ProductBenefitAssetPremiumRateVehicleLineItemTemp.by_id(item.asset_premium_rate_vehicle_line_item_id)
            outputlist.append({
                #'insured_type_id' : "<div class='edit policy_benefit_vehicle_asset_temp_edit' policy_benefit_vehicle_asset_temp_id='{1}'>{0}</div>".format(item.insured_type_id, item.id),
                #'owned_type_id' : item.owned_type_id,
                #'is_fleet' : item.is_fleet,
                #'number_of_vehicles' : item.number_of_vehicles,
                'description' : asset.description,
                'type_of_vehicle' : item.type_of_vehicle,
                'insured' : getcurrency(asset.insured_amount),
                'uninsured' : getcurrency(asset.uninsured_amount),
                'third_party' : getcurrency(asset.third_party_amount),
                #'vin_number' : item.vin_number,
                #'registration_number' : item.registration_number,
                             })
        dbcolumnlist=[
                #'insured_type_id',
                #'owned_type_id',
                #'is_fleet',
                #'number_of_vehicles',
                'description',
                'type_of_vehicle',
                'insured',
                'uninsured',
                'third_party',
                #'vin_number',
                #'registration_number',
                    ]
        theadlist=[
                #'Insured_Type_Id',
                #'Owned_Type_Id',
                #'Is_Fleet',
                #'Number Of Vehicles',
                'Premium Rate',
                'Description',
                'Insured',
                'Uninsured',
                'Third Party',
                #'Vin Number',
                #'Registration Number',
                ]
        tdclasslist = [
                '',
                '',
                'text-right',
                'text-right',
                'text-right',
                ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_vehicle_asset_temp_table", tdclasslist)

    @expose()
    def get_policy_benefit_business_asset_temp_html(self, policy_id=None, *args, **kwargs):
        if not policy_id: return ''
        dbase_query = PolicyBenefitBusinessAssetTemp.by_attr_all('policy_id', policy_id)
        outputlist = []
        for item in dbase_query:
            asset = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_id(item.asset_premium_rate_turnover_line_item_id)
            outputlist.append({
                #'company_registration_number' : "<div class='edit policy_benefit_business_asset_temp_edit' policy_benefit_business_asset_temp_id='{1}'>{0}</div>".format(item.company_registration_number, item.id),
                #'turnover' : item.turnover,
                #'email' : item.email,
                #'contact_name' : item.contact_name,
                #'contact_number' : item.contact_number,
                'line_item' : f"{asset.minimum_turnover} - {asset.maximum_turnover}",
                'activity' : item.activity,
                'amount' : getcurrency(asset.amount),
                             })
        dbcolumnlist=[
                #'company_registration_number',
                #'turnover',
                #'email',
                #'contact_name',
                #'contact_number',
                'line_item',
                'activity',
                'amount',
                    ]
        theadlist=[
                #'Company_Registration Number',
                #'Turnover',
                #'Email',
                #'Contact Name',
                #'Contact Number',
                'Turnover',
                'Description',
                'Amount',
                ]
        tdclasslist = [
                '',
                '',
                'text-right',
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "policy_benefit_business_asset_temp_table", tdclasslist)

    @expose()
    def get_short_term_edit_benefit_assets(self, *args, **kwargs):
        print('Placeholder: do the benefit assets', kwargs)
        policy_id = kwargs.get('policy_id', None)
        if not policy_id: return self.get_short_term_edit_benefit_assets_error()
        product_benefit_id = kwargs.get('product_benefit_id', None)
        if not product_benefit_id: return self.get_short_term_edit_benefit_assets_error()
        benefit = ProductBenefit.by_id(product_benefit_id)
        product_asset = ProductBenefitAssetTemp.by_attr_first('product_benefit_id', product_benefit_id)

        asset_business = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'business')
        asset_vehicle = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'vehicle')
        asset_employee = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'employee')
        asset_property = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'property')

        if product_asset.product_benefit_asset_temp_type_id == asset_business:
            htmltbl = self.get_policy_benefit_business_asset_temp_html(policy_id)
            asset_type_id = asset_business
            button_text = 'Business'

        if product_asset.product_benefit_asset_temp_type_id == asset_vehicle:
            htmltbl = self.get_policy_benefit_vehicle_asset_temp_html(policy_id)
            asset_type_id = asset_vehicle
            button_text = 'Vehicle'

        if product_asset.product_benefit_asset_temp_type_id == asset_employee:
            htmltbl = self.get_policy_benefit_employee_asset_temp_html(policy_id)
            asset_type_id = asset_employee
            button_text = 'Employee'

        if product_asset.product_benefit_asset_temp_type_id == asset_property:
            htmltbl = self.get_policy_benefit_property_asset_temp_html(policy_id)
            asset_type_id = asset_property
            button_text = 'Property'

        title = _(f"Assets for: {benefit.name}")
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{title}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_policy_benefit_asset" product_benefit_id='{product_benefit_id}' asset_type_id='{asset_type_id}' class="btn btn-primary ml-auto">Add {button_text} Asset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    {htmltbl}
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#create_policy_benefit_asset').click(function(){
                var kwargs = 'product_benefit_id='+$(this).attr('product_benefit_id');
                kwargs += '&asset_type_id='+$(this).attr('asset_type_id');
                kwargs += '&policy_id='+$('#btn_policy_back').attr('policy_id');
                $('#dialogdiv').load('/policy/get_modal_new_policy_benefit_asset?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_new_policy_benefit_asset(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        asset_type_id = int(kwargs.get('asset_type_id', 0))
        product_benefit_id = kwargs.get('product_benefit_id', None)
        hidden_input_policy_id = get_hidden_input(**{'id': 'policy_id', 'value': policy_id})
        hidden_input = get_hidden_input(**{'id': 'product_benefit_id', 'value': product_benefit_id})

        asset_business = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'business')
        asset_vehicle = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'vehicle')
        asset_employee = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'employee')
        asset_property = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'property')

        link = ProductBenefitAssetPremiumRateLinkTemp.by_attr_first('product_benefit_id', product_benefit_id)

        if asset_type_id == asset_business:
            lineitems = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', link.product_benefit_asset_premium_rate_temp_id)
            id = 'asset_premium_rate_business_line_item_id'
            outputlist = [{'id': x.id, 'name': f"Turnover: {x.minimum_turnover} - {x.maximum_turnover}, Amount: {getcurrency(x.amount)}"} for x in lineitems]

        if asset_type_id == asset_vehicle:
            lineitems = ProductBenefitAssetPremiumRateVehicleLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', link.product_benefit_asset_premium_rate_temp_id)
            id = 'asset_premium_rate_vehicle_line_item_id'
            outputlist = []
            for x in lineitems:
                name = f"""
                {x.description}
                Insured: {getcurrency(x.insured_amount)}
                Uninsured: {getcurrency(x.uninsured_amount)}
                Third Party: {getcurrency(x.third_party_amount)}
                """
                outputlist.append({
                    'id' : x.id,
                    'name' : name,
                })

        if asset_type_id == asset_employee:
            lineitems = ProductBenefitAssetPremiumRateEmployeeLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', link.product_benefit_asset_premium_rate_temp_id)
            id = 'asset_premium_rate_employee_line_item_id'
            outputlist = [{'id': x.id, 'name': f"Employees: {x.minimum_employees_coverable} - {x.maximum_employees_coverable}, Amount: {getcurrency(x.amount)}"} for x in lineitems]

        if asset_type_id == asset_property:
            lineitems = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', link.product_benefit_asset_premium_rate_temp_id)
            id = 'asset_premium_rate_property_line_item_id'
            outputlist = [{'id': x.id, 'name': f"Turnover: {x.minimum_turnover} - {x.maximum_turnover}, Amount: {getcurrency(x.amount)}"} for x in lineitems]

        kwargs['id'] = id
        kwargs['outputlist'] = outputlist
        selectbox = create_selectbox_html(**kwargs)

        html = f"""
        <div class="modal fade" id="dialog_policy_benefit_asset_temp" tabindex="-1" role="dialog" aria-labelledby="mypolicy_benefit_asset_tempLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Policy Benefit Asset</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_policy_benefit_asset_temp'>
                            {hidden_input}
                            {hidden_input_policy_id}
                            <div class="form-group row">
                                <label class="col-md-4 col-form-label" required for="{id}">Rate Table</label>
                                <div class="col-md-8">
                                    {selectbox}
                                </div>
                            </div>
                            <div class="form-group row">
                                <label class="col-md-4 col-form-label" required for="description">Description</label>
                                <div class="col-md-8">
                                    <textarea name='description' type="text" class="form-control" rows="4" maxlength='200'></textarea>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_policy_benefit_asset_temp' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary policy_benefit_asset_temp_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_policy_benefit_asset_temp'
        setFormValidation(form_id);
        $('#save_policy_benefit_asset_temp').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/policy/save_policy_benefit_business_asset?', formserial, function(data){
                    $('#tab2').load('/policy/get_short_term_edit_benefit_assets?', formserial, function(data){
                        $('#dialog_policy_benefit_asset_temp').modal('hide');
                        return false;
                    });
                    return false;
                });
             }
        });
        $('.policy_benefit_asset_temp_back').click(function(){
            $('#dialog_policy_benefit_asset_temp').modal('hide');
        });
        $('#dialog_policy_benefit_asset_temp').modal();
        </script>
     	"""
        return html + javascript

    def get_short_term_edit_summary(self, policy=None, *args, **kwargs):
        print('Placeholder: do the summary')
        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Summary')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_summary" class="btn btn-primary ml-auto">Add</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    body
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_short_term_edit_documents(self, policy=None, *args, **kwargs):
        if not policy: return ''
        product = DBSession.query(Product).filter(Product.id == policy.product_id).first()
        if not product: return ''
        contract_html = self.get_policy_contract_html(product)
        system_document_html = self.get_system_document_html(product)
        html = f"""
        <div class="row">
            <div class="col-md-6" id='div_system_document_link_html'>
                {contract_html}
            </div>
            <div class="col-md-6" id='div_system_document_html'>
                {system_document_html}
            </div>
        </div>
        """
        return html
    def get_policy_contract_html(self, product=None, *args, **kwargs):
        if product : product_id = product.id
        if not product_id: return ''
        dbase_query = ProductSystemDocumentLink.by_attr_all('product_id', product_id)
        outputlist = []
        for item in dbase_query:
            doc = SystemDocument.by_id(item.system_document_id)
            outputlist.append({
                'name' : f"<div class='edit welcome_package_link_edit action_link' link_id='{item.id}'>{doc.name}</div>",
                'file_path' : remove_hash_from_filename(item.file_path),
                'download' : f"<div class='welcome_package_link_download action_link' link_id='{item.id}'>download</div>",
                             })
        dbcolumnlist=[
                'name',
                'file_path',
                'download',
        ]
        theadlist=[
                'Name',
                'File Name',
                '',
        ]
        tdclasslist = [
                '',
                '',
                'text-right',
        ]
        welcome_package_linktable = build_html_table(outputlist, dbcolumnlist, theadlist, "welcome_package_link_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Welcome Package')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {welcome_package_linktable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('.welcome_package_link_download').click(function(){
                var formserial = 'link_id='+$(this).attr('link_id');
                var href_with_formserial = '/product/download_welcome?'+formserial;
                window.location = href_with_formserial
            });

        </script>
        """
        return html + javascript

    @expose()
    def get_system_document_html(self, product=None, *args, **kwargs):
        if product: product_id = product.id
        if not product_id: return ''
        dbase_query = ProductSystemDocumentLink.by_attr_all('product_id', product_id)
        outputlist = []
        for item in dbase_query:
            if item.file_path: continue
            doc = SystemDocument.by_id(item.system_document_id)
            outputlist.append({
                'name' : doc.name,
                'delete' : f"<div class='delete_system_document_link action_link text-right' product_id='{product_id}' link_id='{item.id}'>delete</div>",
                             })
        dbcolumnlist=[
                'name',
                'delete',
                    ]
        theadlist=[
                'Name',
                '',
                ]
        linktable = build_html_table(outputlist, dbcolumnlist, theadlist, "product_link_table")
        html = f"""
        <div class="card">
            <div class="card-header">
                <div class="row d-flex">
                    <div class="col-md-6">
                        <h4 class="card-title">{_('Claims Documents')}</h4>
                    </div>

                </div>
            </div>
            <div class="card-body">
                {linktable}
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_product_system_document_link").click(function(){
                var kwargs = 'product_id='+$(this).attr('product_id');
                $('#dialogdiv').load('/product/get_modal_new_product_system_document_link?', kwargs, function(data){
                    return false;
                });
            });
            $(".delete_system_document_link").click(function(){
                var kwargs = 'product_id='+$(this).attr('product_id');
                kwargs += '&link_id='+$(this).attr('link_id');
                $.post('/product/save_delete_product_system_document_link?', kwargs, function(data){
                    $('#div_system_document_html').load('/product/get_system_document_html?', kwargs, function(data){
                        return false;
                    });
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    def get_short_term_edit_transaction(self, policy=None, *args, **kwargs):
        print('Placeholder: do the transaction')
        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Transaction')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                          <button id="create_new_transaction" class="btn btn-primary ml-auto">{_('New Transaction')}</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">

                </div>
            </div>
        </div>
        """
        return html

    def get_short_edit_header_html(self, policy=None, *args, **kwargs):
        if not policy: return ''
        product = DBSession.query(Product).filter(Product.id==policy.product_id).first()
        if not product: return ''
        product_life_assured_type_name = None
        if product.product_assured_type_id:
            product_life_assured_type_name = TYPEUTIL.get_pretty_name('product_life_assured_type', product.product_assured_type_id)
        entity_policy_holder = Entity.by_id(policy.entity_policy_holder_id)
        if not entity_policy_holder: return ''
        ep_holder = EntityPerson.by_attr_first('entity_id', entity_policy_holder.id)
        personobj_policy_holder = vault.get_personobj_by_id(ep_holder.person_id)
        if not personobj_policy_holder: return ''
        policy_holder = personobj_policy_holder.get('person', {})
        policy_holder_full_name = f"{policy_holder.get('firstname', '')} {policy_holder.get('surname', '')}"
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-9">
                                <h4 class="card-title">Policy for: {policy_holder_full_name} ({policy.policy_number})</h4>
                            </div>
                            <div class="col-md-3 text-right">
                                <button id="btn_policy_back" policy_id='{policy.id}' class="btn btn-primary ml-auto">Back to Policies</button>
                            </div>
                        </div>
                        <hr>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">Product: </label>
                                        <label class="col-md-3 col-form-label">{product.code} - {product.name}</label>
                                    </div>
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Assured: ')}</label>
                                        <label class="col-md-3 col-form-label">{product_life_assured_type_name}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_short_term_benefits_html(self, policy= None, *args, **kwargs):
        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"
        dbase_query = ProductBenefit.by_attr_all('product_id', policy.product_id)
        outputlist = []
        for item in dbase_query:
            product_benefit_asset = ProductBenefitAssetTemp.by_attr_first('product_benefit_id', item.id)
            benefit_cover =ProductBenefitCoverLink.by_id(item.product_benefit_cover_link_id)
            ben_cover= TYPEUTIL.get_pretty_name("cover_and_exclusion_type", benefit_cover.cover_and_exclusion_type_id)
            benefit_asset_type = TYPEUTIL.get_pretty_name("product_benefit_asset_temp_type", product_benefit_asset.product_benefit_asset_temp_type_id)
            outputlist.append({
                'name': f"<div class='edit edit_contact'  contact_id='{item.id}'>{item.name}</div>",
                'benefit_cover': ben_cover,
                'benefit_asset_type':  benefit_asset_type,
                'compulsory':  img_active if item.is_compulsory else img_inactive,
                'action': f"<div class='edit open_short_term'  product_benefit_id='{item.id}' policy_id='{policy.id}'>open</div>",
            })
        dbcolumnlist = [
            'name',
            'benefit_cover',
            'benefit_asset_type',
            'compulsory',
            'action',
        ]
        theadlist = [
            'Name',
            'Benefit Cover',
            'Asset Type',
            'Compulsory'
            ''
        ]
        tdclasslist = [
            '',
            '',
            '',
            'text-center',
            'text-right action_link',
        ]
        benefitstable = build_html_table(outputlist, dbcolumnlist, theadlist, "short_term_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Benefits</h4>
                            </div>

                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {benefitstable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def save_policy_benefit_business_asset(self, *args, **kwargs):
        usernow = request.identity.get('user', None)

        policy_id = kwargs.get('policy_id', None)
        description = kwargs.get('description', None)
        product_benefit_id = kwargs.get('product_benefit_id', None)
        asset_premium_rate_vehicle_line_item_id = kwargs.get('asset_premium_rate_vehicle_line_item_id', None)
        asset_premium_rate_business_line_item_id = kwargs.get('asset_premium_rate_business_line_item_id', None)
        asset_premium_rate_employee_line_item_id = kwargs.get('asset_premium_rate_employee_line_item_id', None)
        asset_premium_rate_property_line_item_id = kwargs.get('asset_premium_rate_property_line_item_id', None)

        polben = DBSession.query(PolicyBenefit). \
                filter(PolicyBenefit.product_benefit_id==product_benefit_id). \
                filter(PolicyBenefit.policy_id==policy_id). \
                filter(PolicyBenefit.active==True). \
                first()
        if not polben:
            polben = PolicyBenefit()
            polben.product_benefit_id = product_benefit_id
            polben.policy_id = policy_id
            polben.claims_left = 1
            polben.added_by = usernow.id
            DBSession.add(polben)
            DBSession.flush()

        if asset_premium_rate_vehicle_line_item_id:
            link = PolicyBenefitVehicleAssetTemp()
            link.policy_id = policy_id
            link.policy_benefit_id = polben.id
            link.product_benefit_id = product_benefit_id
            link.asset_premium_rate_vehicle_line_item_id = asset_premium_rate_vehicle_line_item_id
            link.type_of_vehicle = description
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()

        if asset_premium_rate_business_line_item_id:
            link = PolicyBenefitBusinessAssetTemp()
            link.policy_id = policy_id
            link.policy_benefit_id = polben.id
            link.product_benefit_id = product_benefit_id
            link.asset_premium_rate_turnover_line_item_id = asset_premium_rate_business_line_item_id
            link.activity = description
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()

        if asset_premium_rate_employee_line_item_id:
            link = PolicyBenefitEmployeeAssetTemp()
            link.policy_id = policy_id
            link.policy_benefit_id = polben.id
            link.product_benefit_id = product_benefit_id
            link.asset_premium_rate_employee_line_item_id = asset_premium_rate_employee_line_item_id
            link.name = description
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()

        if asset_premium_rate_property_line_item_id:
            link = PolicyBenefitPropertyAssetTemp()
            link.policy_id = policy_id
            link.policy_benefit_id = polben.id
            link.product_benefit_id = product_benefit_id
            link.asset_premium_rate_turnover_line_item_id = asset_premium_rate_property_line_item_id
            link.description = description
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()

        return 'true'

##################################################################################################################
# Policy - Edit
##################################################################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        if not policy_id: redirect('/policy/index')
        policy = Policy.by_id(policy_id)
        if not policy: redirect('/policy/index')
        html = self.get_policy_edit_html(policy)
        javascript = self.get_javascript_edit_policy_onload()
        title = f"Edit: {policy.policy_number}"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_policy_edit_html(self, policy=None, *args, **kwargs):
        if not policy: redirect('/policy/index')

        # HEADER
        card_header = self.get_policy_edit_header_html(policy)

        # TAB 1
        tab1_content = self.get_policy_edit_premium_and_dates_html(policy)

        # TAB 2
        tab2_content = self.get_policy_edit_beneficiaries_html(policy)

        # TAB 3
        tab3_content = self.get_policy_edit_loaders_html(policy)

        # TAB 4
        tab4_content = self.get_policy_edit_summary_html(policy)

        # TAB 5
        tab5_content = self.get_policy_edit_acceptance_html(policy)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    <ul class="nav nav-pills nav-pills-primary justify-content-center" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#tab1" role="tablist">
                                Premium & Dates
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab2" role="tablist">
                                Beneficiaries
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab3" role="tablist">
                                Loaders
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab4" role="tablist">
                                Summary
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab5" role="tablist">
                                Acceptance
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="tab-content tab-space tab-subcategories">
                    <div class="tab-pane active" id="tab1">
                        {tab1_content}
                    </div>
                    <div class="tab-pane" id="tab2">
                        {tab2_content}
                    </div>
                    <div class="tab-pane" id="tab3">
                        {tab3_content}
                    </div>
                    <div class="tab-pane" id="tab4">
                        {tab4_content}
                    </div>
                    <div class="tab-pane" id="tab5">
                        {tab5_content}
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_javascript_edit_policy_onload(self, *args, **kwargs):
        javascript = """
        $("#btn_policy_back").click(function(){
            $.redirect('/policy/index');
        });
        """
        return javascript

##################################################################################################################
# Policy - Edit - Header
##################################################################################################################

    def get_policy_edit_header_html(self, policy=None, *args, **kwargs):
        if not policy: return ''
        product = Product.by_id(policy.product_id)
        if not product: return ''
        product_life_assured_type_name = None
        if product.product_assured_type_id:
            product_life_assured_type_name = TYPEUTIL.get_pretty_name('product_life_assured_type', product.product_assured_type_id)

        entity_policy_holder = EntityPerson.by_id(policy.entity_policy_holder_id)
        if not entity_policy_holder: return ''
        personobj_policy_holder = vault.get_personobj_by_id(entity_policy_holder.person_id)
        if not personobj_policy_holder: return ''
        policy_holder = personobj_policy_holder.get('person', {})
        policy_holder_full_name = f"{policy_holder.get('firstname', '')} {policy_holder.get('surname', '')}"

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-9">
                                <h4 class="card-title">Create New Policy for: {policy_holder_full_name} ({policy.policy_number})</h4>
                            </div>
                            <div class="col-md-3 text-right">
                                <button id="btn_policy_back" class="btn btn-primary ml-auto">Back to Policies</button>
                            </div>
                        </div>
                        <hr>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">Product: </label>
                                        <label class="col-md-3 col-form-label">{product.code} - {product.name}</label>
                                    </div>
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Life(s) Assured: ')}</label>
                                        <label class="col-md-3 col-form-label">{product_life_assured_type_name}</label>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

##################################################################################################################
# Policy - Edit - Premium and Dates
##################################################################################################################

    def get_policy_edit_premium_and_dates_html(self, policy=None, *args, **kwargs):

        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Premium & Dates')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            button
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    body
                </div>
            </div>
        </div>
        """
        return html

##################################################################################################################
# Policy - Edit - Beneficiaries
##################################################################################################################

    def get_policy_edit_beneficiaries_html(self, policy=None, *args, **kwargs):
        print('Placeholder: Add beneficiaries, must add up to 100%')
        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Beneficiaries')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            button
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    body
                </div>
            </div>
        </div>
        """
        return html

##################################################################################################################
# Policy - Edit - Loaders
##################################################################################################################

    def get_policy_edit_loaders_html(self, policy=None, *args, **kwargs):
        print('Placeholder: answer loader questions')
        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Loaders')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            button
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    body
                </div>
            </div>
        </div>
        """
        return html

##################################################################################################################
# Policy - Edit - Summary
##################################################################################################################

    def get_policy_edit_summary_html(self, policy=None, *args, **kwargs):
        print('Placeholder: show the summary of the policy with benefits')
        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Summary')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            button
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    body
                </div>
            </div>
        </div>
        """
        return html

##################################################################################################################
# Policy - Edit - Acceptance
##################################################################################################################

    def get_policy_edit_acceptance_html(self, policy=None, *args, **kwargs):
        print('Placeholder: click to accept here, we should add initial premium capture here.')
        if not policy: return ''
        html = f"""
        <div class="row">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                             <h4 class="card-title">{_('Acceptance')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            button
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    body
                </div>
            </div>
        </div>
        """
        return html
