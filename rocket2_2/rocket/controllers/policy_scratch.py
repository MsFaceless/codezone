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
from rocket.lib.type_utils import TypeDictionary as TypeDict
from rocket.controllers.members import MemberController

MEMBER_CONT = MemberController()

LIMIT = 20

class PolicyController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_policy_list_html(*args, **kwargs)
        javascript = self.get_javascript_policy_onload()
        title = _("Policies")
        return dict(title=title, html=html, javascript=javascript)

##################################################################################################################
# Start Policy List
##################################################################################################################
    @expose()
    def get_policy_list_html(self, *args, **kwargs):
        policytable = self.get_policy_list_html_tbl(**kwargs)
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
                            <button id="btn_create_new_policy_popup" class="btn btn-primary ml-auto">Create a new Policy</button>
                            <!--
                            -->
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-8 d-flex">
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
                        {policytable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_javascript_policy_onload(self, *args, **kwargs):
        javascript = """
        $("#btn_create_new_policy_popup").click(function(){
            $('#dialogdiv').load('/policy/get_modal_select_member?', function(data){
                return false;
            });
        });
        """
        return javascript

    def get_policy_list_html_tbl(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_policy_list(*args, **kwargs)
        outputlist = []
        td = TypeDict()
        for item in dbase_query:
            print('Placeholder: get person name here.')
            print('Placeholder: for fake data stuff removal.')
            member_holder = Member.by_id(item.policy_holder_id)
            policy_holder = 'Soap, Josephine'
            member_owner = Member.by_id(item.policy_owner_id)
            policy_owner = 'Sizpack, Frederick'
            #product = Product.by_id(item.product_id)
            #product_name = product.name
            product_name = 'ACME Product Name'
            #policy_state = td.get_pretty_name('policy_state_type', policy.policy_state_type_id)
            policy_state = td.get_pretty_name('policy_state_type', td.get_id_of_name('policy_state_type', 'proposal'))
            outputlist.append({
                'policy_number': "<div class='edit entity_edit' policy_id='{1}'>{0}</div>".format(
                    item.policy_number, item.id),
                'policy_holder': policy_holder,
                'policy_owner': policy_owner,
                'product' : product_name,
                'state': policy_state,
            })
        theadlist = [
            'Policy Number',
            'Policy Holder',
            'Policy Owner',
            'Product',
            'State'
        ]
        dbcolumnlist = [
            'policy_number',
            'policy_holder',
            'policy_owner',
            'product',
            'state',
        ]
        tdclasslist = [
            'action_link',
            'text-left',
            'text-left',
            'text-left',
            'text-left',
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "policy_table", tdclasslist)

    @expose()
    def get_active_policy_list(self, *args, **kwargs):
        print('Getting the ')
        dbase_query = DBSession.query(Policy). \
            filter(Policy.active == 1). \
            order_by(asc(Policy.id)). \
            limit(LIMIT)
        return dbase_query

##################################################################################################################
# Start NEW Policy
##################################################################################################################
    @expose()
    def get_modal_select_member(self, *args, **kwargs):
        usernow = request.identity['user']
        selectbox_products = self.get_selectbox_products(**{
            'id' : 'product_id',
            #'selected' : searchstate,
            'class_names': 'col-md-4',
            })
        kwargs['selectbox_products'] = 'selectbox_products'
        #Get the HTML table from Member Conrtoller. Add some nioce logic there to remove the unnecessary fields.
        print('Placeholder: Fake policy id')
        policy_id = 1
        kwargs['policy_id'] = policy_id
        #END FAKE DATA
        member_list = MEMBER_CONT.get_member_html_table(*args, **kwargs)

        html = f"""
        <div class="modal fade" id="dialog_new_policy" tabindex="-1" role="dialog" aria-labelledby="myproductLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Member and Product Selection </h4>
                        </div>
                        <hr>
                    </div>
                    <div class="row d-flex align-items-center">
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
                    <div class="card-body">
                        <div class="table-responsive">
                            {member_list}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button id='btn_create_new_policy' class="btn btn-primary">Create Policy</button>
                        <button class="btn btn-outline-primary policy_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        $("#btn_create_new_policy").click(function(){
            console.log('Placeholder: Fake data removal')
            /*
            var data = {policy_id : $(this).attr('policy_id')};
            */
            var data = {policy_id : 1};
            $.redirect('/policy/create_new_policy_form', data);
        });
        $('.policy_back').click(function(){
            $('#dialog_new_policy').modal('hide');
        });

        $('#dialog_new_policy').modal();
        </script>
        """
        return html + javascript

    def get_selectbox_products(self, *args, **kwargs):
        #dbase_query = Product.get_all('code')
        kwargs['id'] = 'product_id'
        print("Build list of available Products")
        kwargs['outputdict'] = []
        return create_selectbox_html(**kwargs)

##################################################################################################################
# Create NEW Policy fORM
##################################################################################################################
    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def create_new_policy_form(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        if not policy_id: redirect('/policy/index')
        policy = Policy.by_id(policy_id)
        member = Member.by_id(policy.policy_holder_id) if policy else None
        product = Product.by_id(policy.product_id) if policy else None
        print('placeholder: No products. Un comment follwing line when there are.')
        #if not product or not member: redirect('/policy/index')
        print('placeholder: We need initial validation here')
        #We need to do some initial validation here. Is the person too old to purhcase product or age >= maturity age.
        html = self.get_new_policy_html(*args, **kwargs)
        javascript = self.get_javascript_new_policy_onload()
        title = _("New Policy")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_new_policy_html(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        product = Product.by_id(product_id)
        td = TypeDict()
        print('Placehodler: Fake date hereunder for removal')
        if product: # Initial protective code. Testing only.
            product_type_id = product.product_type_id
        else:
            product_type_id = td.get_id_of_name('product_type', 'voucher')

        if product_type_id == td.get_id_of_name('product_type', 'voucher'):
            #Then do Voucher stuff
            return self.get_new_voucher_policy_html(*args, **kwargs)
        if product_type_id == td.get_id_of_name('product_type', 'traditional'):
            #Then do Traditional stuff
            return self.get_new_traditional_policy_html(*args, **kwargs)
        if product_type_id == td.get_id_of_name('product_type', 'term_life'):
            #Then do Term Life stuff
            return  self.get_new_term_life_policy_html(*args, **kwargs)
        if product_type_id == td.get_id_of_name('product_type', 'credit_life'):
            #Then do Credit Life stuff
            return self.get_new_credit_life_policy_html(*args, **kwargs)
        return ''

    @expose()
    def get_javascript_new_policy_onload(self, *args, **kwargs):
        javascript = """
        $("#return_to_policy_list").click(function(){
            $.redirect('/policy/index');
        });
        """
        return javascript

    @expose()
    def get_new_voucher_policy_html(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        if not policy_id: return 'false'
        policy = Policy.by_id(policy_id)
        member = Member.by_id(policy.policy_holder_id) if policy else None
        product = Product.by_id(policy.product_id) if policy else None
        td = TypeDict()
        #product_type_id = product.product_type_id
        product_type_id = td.get_id_of_name('product_type', 'voucher')
        product_type = td.get_pretty_name('product_type', product_type_id)

        # HEADER
        card_header = self.get_policy_card_header_html(policy_id)
        # TAB 1
        card_premium_and_dates = self.get_show_policy_premium_dates_html(policy_id)
        # TAB 2
        card_beneficiary = self.get_show_policy_beneficiary_html(policy_id)
        # TAB 3
        card_loaders = self.get_show_policy_loaders_html(policy_id)
        # TAB 4
        card_policy_summary = self.get_show_policy_summary_html(policy_id)
        # TAB 5
        card_policy_accept = self.get_show_policy_accept_html(policy_id)

        form_show_tab1 = f"""
        <form id='form_edit_voucher_product'>
            {card_premium_and_dates}
        </form>
        """

        form_show_tab2 = f"""
        <form id='form_edit_voucher_product'>
            {card_beneficiary}
        </form>
        """

        form_show_tab3 = f"""
        <form id='form_edit_voucher_product'>
            {card_loaders}
        </form>
        """

        form_show_tab4 = f"""
        <form id='form_edit_voucher_product'>
            {card_policy_summary}
        </form>
        """

        form_show_tab5 = f"""
        <form id='form_edit_voucher_product'>
            {card_policy_accept}
        </form>
        """

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    <ul class="nav nav-pills nav-pills-primary justify-content-center" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#tab1" role="tablist">
                                Premium and Dates
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
                        {form_show_tab1}
                    </div>
                    <div class="tab-pane" id="tab2">
                        {form_show_tab2}
                    </div>
                    <div class="tab-pane" id="tab3">
                        {form_show_tab3}
                    </div>
                    <div class="tab-pane" id="tab4">
                        {form_show_tab4}
                    </div>
                    <div class="tab-pane" id="tab5">
                        {form_show_tab5}
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_policy_card_header_html(self, policy_id=None, *args, **kwargs):
        print('Placeholder: remove comment next line')
        #if not policy_id: return ''
        policy = Policy.by_id(policy_id)
        print('Placeholder: remove comment next line')
        #if not policy: return ''
        member = Member.by_id(policy.policy_owner_id) if policy else None
        print('Placeholder: remove comment next line')
        #if not member: return ''
        product = Product.by_id(policy.product_id) if policy else None
        print('Placeholder: remove comment next line')
        #if not product: return ''

        #Get the person from Vault
        print('Placeholder: for vault.')

        print('Placeholder: left typedict here for sequenc.')
        td = TypeDict()

        print('Placeholder: for fake data removal.')
        person = 'Placeholder for vault'
        identity_number = '1234567890123'
        name = 'Joe'
        surname = 'Soap'

        this_person = surname+', '+name+' ('+identity_number+')'
        print('Placeholder: for fake data removel.')
        if product: # Initial protective code. Testing only.
            product_type_id = product.product_type_id
            product_code = product.code
            product_name = product.name
            product_owner_id = product.product_owner_id
            product_insurer_id = product.insurer_id
            product_life_assured_type_id = product.product_life_assured_type_id
            currency_id = product.currency_id
        else:
            product_type_id = td.get_id_of_name('product_type', 'voucher')
            product_code = 'TEST001'
            product_name = 'Test Product Number 001'
            product_owner_id = 1
            product_insurer_id = 2
            product_life_assured_type_id = td.get_id_of_name('product_life_assured_type', 'member_and_family')
            product_currency_id = 1

        traditional = td.get_id_of_name('product_type', 'traditional')
        fixed_price = td.get_id_of_name('product_price_initial_setup_type', 'fixed_price')
        product_type = td.get_pretty_name('product_type', product_type_id)
        life_assured_type = td.get_pretty_name('product_life_assured_type', product_life_assured_type_id)

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-9">
                                <h4 class="card-title">Create new Policy for: </h4>
                                <h3 class="card-title">{this_person}</h3>
                            </div>
                            <div class="col-md-3 text-right">
                                <button id="return_to_policy_list" class="btn btn-primary ml-auto">Return to Policy List</button>
                            </div>
                        </div>
                        <hr>
                        <div class="card-body">
                            <div class="row">
                                <div class="col-md-7">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{product_code} - </label>
                                        <label class="col-md-3 col-form-label">{product_name}</label>
                                    </div>
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Life(s) Assured: ')}</label>
                                        <label class="col-md-3 col-form-label">{life_assured_type}</label>
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

    def get_show_policy_premium_dates_html(self, policy_id=None, *args, **kwargs):
        print('Placeholder: detail comment removal')
        #Select the premium frequency and set/view dates
        return ''

    def get_show_policy_beneficiary_html(self, policy_id=None, *args, **kwargs):
        print('Placeholder: detail comment removal')
        #Add beneficiary(s) here. Must add up to 100%
        return ''

    def get_show_policy_loaders_html(self, policy_id=None, *args, **kwargs):
        print('Placeholder: detail comment removal')
        #Answer loader questions
        return ''

    def get_show_policy_summary_html(self, policy_id=None, *args, **kwargs):
        print('Placeholder: detail comment removal')
        #Show a summary of the polisy with benefits
        return ''

    def get_show_policy_accept_html(self, policy_id=None, *args, **kwargs):
        print('Placeholder: detail comment removal')
        #Click to accept as setup. We could add initial premium capture here also.
        return ''




#----- Save the Policy Here now.
# Notes:
# Save enough detail away from the popuip to create the policy record.
# Thereafter we have the Policy_id that can be used everytwhere.
#----- Save new Policy.
    @expose()
    def save_new_policy(self, *args, **kwargs):
        product_id = kwargs.get('product_id')

        td = TypeDict()
        individual = td.get_id_of_name('policy_type', 'individual')
        proposal_date = td.get_id_of_name('policy_date_type', 'proposal')
        proposal_state = td.get_id_of_name('policy_state_type', 'proposal')

        product = Product.by_id(product_id)
        policy_number = self.generate_new_policy_number(product_id)
        product_frequency_type_id = kwargs.get('product_frequency_type_id')
        #Save Policy
        policy_id = self.write_new_policy({
            'policy_number': policy_number,
            'policy_type_id':  individual,
            'product_id':  policy_id,
            'policy_owner_id':  kwargs.get('member_id'),
            'policy_holder_id':  kwargs.get('member_id'),
            'application_form_serial_no':  kwargs.get('application_form_serial_no'),
            'intermediary_id':  kwargs.get('intermediary_id'),
        })
        policy_state_id = self.write_new_policy_state(**{
                'policy_id': policy_id,
                'policy_state_type_id': proposal_state
                })
        self.write_new_policy_date({
            'policy_id': policy_id,
            'policy_date_type_id': proposal_date,
            'date': now.today(),
        })
        return str(policy_id)



    def write_new_policy(self, *args, **kwargs):
        usernow = request.identity['user']
        this = Policy()
        this.policy_number = kwargs.get('policy_number', '')
        this.policy_type_id = kwargs.get('policy_type_id', None)
        this.product_id = kwargs.get('product_id', None)
        this.policy_owner_id = kwargs.get('policy_owner_id', None)
        this.policy_holder_id = kwargs.get('policy_holder_id', None)
        this.application_form_serial_no = kwargs.get('application_form_serial_no', None)
        this.intermediary_id = kwargs.get('intermediary_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    def write_new_policy_state(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyState()
        this.policy_id = kwargs.get('policy_id', None)
        this.policy_state_type_id = kwargs.get('policy_state_type_id', None)
        this.datetime_set = datetime.now()
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

#----- Save new Policy Dates.
    @expose()
    def save_new_policy_dates(self, *args, **kwargs):
        product_id = kwargs.get('product_id')
        td = TypeDict()
        print('Placeholder: for fake data removal.')
        #product_frequency_type_id = kwargs.get('product_frequency_type_id')
        product_frequency_type_id = td.get_id_of_name('product_frequency_type', 'monthly')

        #Save Policy Dates
        wait_period = 0
        wait_period_type_id = None
        cover_period = 0
        cover_period_type_id = None
        cover_from_date = date.today()
        cover_to_date = None

        outputlist = ProductPeriod.by_attr_all('product_id', product_id)
        for item in outputlist:
            #Period Effect
            if item.product_period_effect_type_id == td.get_id_of_name('product_period_effect_type', 'active'):
                #Cover period can get set here..
                cover_period = item.time_period
                cover_period_type_id = item.product_period_type_id

            elif item.product_period_effect_type_id == td.get_id_of_name('product_period_effect_type', 'waiting'):
                #Set Wait period here
                wait_period = item.time_period
                wait_period_type_id = item.product_period_type_id

        #Evaluate the periods
        cover_from_date =  self.set_cover_from_date(cover_from_date, wait_period, wait_period_type_id)
        cover_to_date = self.set_cover_to_date(cover_from_date, cover_period)
        #Default vaules
        accepted_date = date.today()
        policy_date = date.today()
        valid_from_date = cover_from_date
        valid_to_date = cover_to_date
        maturatity_date = None
        member_age = kwargs.get("memberage", None)
        # Maturity
        if product.maturity_age and member_age:
            #Then we can set the maturity date by obtaining the difference between the mmebers current age and the maturity age
            maturatity_date = add_months_to_date(date.today(), ((product.maturity_age - member_age)+1))

        #Save away the various dates as needed.
        if accepted_date:
            policy_date_id = self.write_new_policy_date({
                        'policy_id': policy_id,
                        'policy_date_type_id': td.get_id_of_name('policy_date_type', 'accepted'),
                        'date': accepted_date,
                    })

        if policy_date:
            policy_date_id = self.write_new_policy_date({
                        'policy_id': policy_id,
                        'policy_date_type_id': td.get_id_of_name('policy_date_type', 'policy'),
                        'date': policy_date,
                    })

        if valid_from_date:
            policy_date_id = self.write_new_policy_date({
                        'policy_id': policy_id,
                        'policy_date_type_id': td.get_id_of_name('policy_date_type', 'valid_from'),
                        'date': valid_from_date,
                    })

        if valid_to_date:
            policy_date_id = self.write_new_policy_date({
                        'policy_id': policy_id,
                        'policy_date_type_id': td.get_id_of_name('policy_date_type', 'valid_to'),
                        'date': valid_to_date,
                    })

        if maturatity_date:
            policy_date_id = self.write_new_policy_date({
                        'policy_id': policy_id,
                        'policy_date_type_id': td.get_id_of_name('policy_date_type', 'maturatity'),
                        'date': maturatity_date,
                    })
        return 'true'

#----- Save new Policy Benefits from Product.
    @expose()
    def save_new_policy_benefits(self, *args, **kwargs):
        product_id = kwargs.get('product_id')
        td = TypeDict()

        #Product Benefit
        product_benefits = ProductBenefit.by_attr_all('product_id', product_id, )
        for benefit in product_benefits:
            policy_benefit_id = self.write_new_policy_benefit({
                'policy_id': policy_id,
                'product_benefit_id': benefit.id,
                'claims_left': benefit.number_of_claims
            })
            #Product Benefit Cover
            self.save_new_policy_benefit_cover(policy_benefit_id, benefit.product_benefit_cover_link_id)
            #Product Benefit exclusions
            self.save_new_policy_benefit_exclusions(policy_benefit_id, benefit.id)
        return 'true'

    def write_new_policy_benefit(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyBenefit()
        this.policy_id = kwargs.get('policy_id', None)
        this.product_benefit_id = kwargs.get('product_benefit_id', None)
        this.claims_left = kwargs.get('claims_left', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    def write_new_policy_benefit_cover(self, policy_benefit_id=None, product_benefit_cover_link_id=None, *args, **kwargs):
        if not policy_benefit_id or not product_benefit_cover_link_id:
            return 'false'
        usernow = request.identity['user']
        this = PolicyBenefitCover()
        this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
        this.cover_and_exclusion_type_id = kwargs.get('cover_and_exclusion_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    def save_new_policy_benefit_exclusions(self, policy_benefit_id=None, benefit_id=None, *args, **kwargs):
        #Product Benefit exclusions
        product_benefit_exclusions = ProductBenefitExclusion.by_attr_all('product_benefit_id', benefit.id)
        for exclusion in product_benefit_exclusions:
            policy_benefit_exclusion_id = self.write_new_policy_benefit_exclusion({
                'policy_benefit_id': policy_benefit_id,
                'product_benefit_exclusion_id': exclusion.id,
            })
            #Product Benefit exclusion expiry
            self.write_new_policy_benefit_exclusion_expiry(policy_benefit_exclusion_id, exclusion.id, exclusion.product_benefit_exclusion_expiry_type_id)
        return

    def write_new_policy_benefit_exclusion(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyBenefitExclusion()
        this.policy_benefit_id = kwargs.get('policy_benefit_id', None)
        this.product_benefit_exclusion_id = kwargs.get('product_benefit_exclusion_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    def save_new_policy_benefit_exclusion_expiry(self, policy_benefit_exclusion_id=None, exclusion_id=None, product_benefit_exclusion_expiry_type_id=None, *args, **kwargs):
        expiry_date = None
        #Product Benefit exclusion expiry
        if exclusion.product_benefit_exclusion_expiry_type_id == td.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_days'):
            #Calculate the days from today
            product_benefit_exclusion_days = ProductBenefitExclusionExpiryDays.by_attr_all('product_benefit_exclusion_id', exclusion.id)
            for exclusion_day in product_benefit_exclusion_days:
                exclusion_days = exclusion_day.number_of_days
            expiry_date = add_days_to_date(date.today(), exclusion_days)

        elif exclusion.product_benefit_exclusion_expiry_type_id == td.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_premiums'):
            print('Placeholder: Give this more thought.')
            #Calculate the propoised number of premiums from today. Read the selected premium frequency to determine this.
            if product_frequency_type_id == td.get_id_of_name('product_frequency_type', 'single'):
                #Then what do we do? TODO: Default to Infinite for now till we have clarity
                expiry_date = None
            elif product_frequency_type_id == td.get_id_of_name('product_frequency_type', 'daily'):
                #Then what do we do???
                expiry_date = add_days_to_date(date.today(), 1) #TODO: Makes no sense....
            elif product_frequency_type_id == td.get_id_of_name('product_frequency_type', 'monthly'):
                #Then what do we do???
                expiry_date = None
                expiry_date = add_months_to_date(date.today(), 1)
            elif product_frequency_type_id == td.get_id_of_name('product_frequency_type', 'semi_annually'):
                #Then what do we do???
                expiry_date = add_months_to_date(date.today(), 6)
            elif product_frequency_type_id == td.get_id_of_name('product_frequency_type', 'annually'):
                #Then what do we do???
                expiry_date = add_months_to_date(date.today(), 12)

        expiry_id = self.write_new_policy_benefit_exclusion_expiry({
            'policy_benefit_exclusion_id': policy_benefit_exclusion_id,
            'expiry_date': expiry_date,
        })
        return str(expiry_id)

    def write_new_policy_benefit_exclusion_expiry(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyBenefitExclusionExpiry()
        this.product_benefit_exclusion_id = kwargs.get('product_benefit_exclusion_id', None)
        this.expiry_date = kwargs.get('expiry_date', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

# ######################################################################################################################
# #Child Files
# #Save Beneficiary(s)
    @expose()
    def save_new_policy_beneficiary(self, *args, **kwargs):
        print('Placeholder: Member and person records need to be saved/checked here')
        policy_id = kwargs.get('policy_id', None)
        beneficiary_id = kwargs.get('member_id', None)
        notify = kwargs.get('notify', False)
        relationship_type_id = kwargs.get('relationship_type_id', None)
        share_of_sum_assured = kwargs.get('share_of_sum_assured', None)
        if not policy_id or not beneficiary_id or not relationship_type_id or not share_of_sum_assured:
           return 'false'

        #Save beneficiary
        policy_beneficiary_id = self.write_new_policy_beneficiary({
            'policy_id':  policy_id,
            'beneficiary_id': beneficiary_id ,
            'notify': notify ,
            'relationship_type_id': relationship_type_id ,
            'share_of_sum_assured': share_of_sum_assured ,
        })
        return str(policy_beneficiary_id)

    def write_new_policy_beneficiary(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyBeneficiary()
        this.policy_id = kwargs.get('policy_id', None)
        this.beneficiary_id = kwargs.get('beneficiary_id', None)
        this.notify = kwargs.get('notify', None)
        this.relationship_type_id = kwargs.get('relationship_type_id', None)
        this.share_of_sum_assured = kwargs.get('share_of_sum_assured', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

# #Save Life Assured(s) and Details
    @expose()
    def save_new_policy_life_assured(self, *args, **kwargs):
        #member and person records shouold be saved before we get here.
        policy_id = kwargs.get('policy_id', None)
        member_id = kwargs.get('member_id', None)
        relationship_type_id = kwargs.get('relationship_type_id', None)
        inception_age = kwargs.get('relationship_type_id', None)
        if not policy_id or not member_id or not relationship_type_id or not inception_age:
            return 'false'

        #Save life assured
        life_assured_id = self.write_new_policy_life_assured({
            'policy_id':  policy_id,
            'member_id': member_id,
            'relationship_type_id': relationship_type_id,
            'inception_age': inception_age,
        })
        return str(ife_assured_id)

    def write_new_policy_life_assured(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyLifeAssured()
        this.policy_id = kwargs.get('policy_id', None)
        this.relationship_type_id = kwargs.get('relationship_type_id', None)
        this.inception_age = kwargs.get('inception_age', None)
        this.member_id = kwargs.get('member_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_policy_life_assured_sum_assured(self, *args, **kwargs):
        policy_life_assured_id = kwargs.get('policy_life_assured_id', None)
        initial_sum_assured_amount = kwargs.get('initial_sum_assured_amount', None)
        current_sum_assured_amount = kwargs.get('current_sum_assured_amount', None)
        share_of_policy_premium_amount = kwargs.get('share_of_policy_premium_amount', None)
        sum_assured_increase_percentage = kwargs.get('sum_assured_increase_percentage', None)
        if not policy_life_assured_id or not initial_sum_assured_amount or not share_of_policy_premium_amount:
            return 'false'

        #Save life assured summ assured
        life_assured_sum_assured_id = self.write_new_policy_life_assured_sum_assured({
            'policy_life_assured_id': policy_life_assured_id,
            'initial_sum_assured_amount': initial_sum_assured_amount,
            'current_sum_assured_amount': current_sum_assured_amount,
            'share_of_policy_premium_amount': share_of_policy_premium_amount,
            'sum_assured_increase_percentage': sum_assured_increase_percentage,
        })
        return str(life_assured_sum_assured_id)

    def write_new_policy_life_assured_sum_assured(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyLifeAssuredSumAssured()
        this.policy_life_assured_id = kwargs.get('policy_life_assured_id', None)
        this.initial_sum_assured_amount = kwargs.get('initial_sum_assured_amount', None)
        this.current_sum_assured_amount = kwargs.get('current_sum_assured_amount', None)
        this.share_of_policy_premium_amount = kwargs.get('share_of_policy_premium_amount', None)
        this.sum_assured_increase_percentage = kwargs.get('sum_assured_increase_percentage', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

# #Save policy Loader(s)
    @expose()
    def save_new_policy_loader(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        loader_question_answer_id = kwargs.get('loader_question_answer_id', None)
        if not policy_id or not loader_question_answer_id: return 'false'

        policy_loader_id = self.write_new_policy_loader({
            'policy_id': policy_id,
            'loader_question_answer_id': loader_question_answer_id,
        })
        return str(policy_loader_id)

    def write_new_policy_loader(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyLoader()
        this.policy_id = kwargs.get('policy_id', None)
        this.loader_question_answer_id = kwargs.get('loader_question_answer_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

# #Save Premium and Details
# #Save policy premium
    @expose()
    def save_new_policy_premium(self, *args, **kwargs):
        policy_id = kwargs.get('policy_id', None)
        initial_annual_premium_amount = kwargs.get('initial_annual_premium_amount', None)
        current_annual_premium_amount = kwargs.get('current_annual_premium_amount', initial_annual_premium_amount)
        premium_increase_percentage = kwargs.get('premium_increase_percentage', None)
        policy_premium_payment_method_type_id = kwargs.get('policy_premium_payment_method_type_id', None)
        if not policy_id or not initial_annual_premium_amount or not policy_premium_payment_method_type_id:
            return 'false'
        #Save policy loader
        policy_premium_id = self.write_new_policy_premium({
            'policy_id': policy_id,
            'initial_annual_premium_amount': initial_annual_premium_amount,
            'current_annual_premium_amount': current_annual_premium_amount,
            'premium_increase_percentage': premium_increase_percentage,
            'policy_premium_payment_method_type_id': policy_premium_payment_method_type_id,
        })
        return str(policy_premium_id)

    def write_new_policy_premium(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyPremium()
        this.policy_id = kwargs.get('policy_id', None)
        this.initial_annual_premium_amount = kwargs.get('initial_annual_premium_amount', None)
        this.current_annual_premium_amount = kwargs.get('current_annual_premium_amount', None)
        this.premium_increase_percentage = kwargs.get('premium_increase_percentage', None)
        this.policy_premium_payment_method_type_id = kwargs.get('policy_premium_payment_method_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

# #Save policy premium
    @expose()
    def save_new_policy_premium_payment_schedule(self, *args, **kwargs):
        policy_premium_id = kwargs.get('policy_premium_id', None)
        premium_frequency_id = kwargs.get('premium_frequency_id', None)
        adjustment_factor = kwargs.get('adjustment_factor', None)

        if not policy_premium_id or not premium_frequency_id: return 'false'
        #Save policy premium payment schedule
        schedule_id = self.write_new_policy_premium_payment_schedule({
            'policy_premium_id': policy_premium_id,
            'premium_frequency_id': premium_frequency_id,
            'adjustment_factor': adjustment_factor,
        })
        return str(schedule_id)

    def write_new_policy_premium_payment_schedule(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyPremiumPaymentSchedule()
        this.policy_premium_id = kwargs.get('policy_premium_id', None)
        this.premium_frequency_id = kwargs.get('premium_frequency_id', None)
        this.adjustment_factor = kwargs.get('adjustment_factor', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

# #Save Premium Payment SChedule
    def generate_new_policy_number(self, product_id, *args, **kwargs):
        product = Product.by_id(product_id)
        p_prefix = product.policy_number_prefix.strip()
        product_owner = ProductOwner.by_id(product.product_owner_id)
        print()
        print('CAMILLA: insert class method here as discussed')
        print()
        o_prefix = product_owner.policy_number_prefix.strip()
        now = datetime.now()
        body = now.strftime("%y%m%d%H%M%S%f")
        new_policy_number = o_prefix+p_prefix+body
        return new_policy_number

    def set_cover_from_date(self, cover_from_date=date.today(), wait_period=None, wait_period_type_id=None, *args, **kwargs):
        if wait_period and wait_period_type_id:
            #set the cover from date
            if wait_period_type_id == td.get_id_of_name('product_period_type', 'days'):
                cover_from_date = add_days_to_date(cover_from_date, wait_period)
                return cover_from_date

            if wait_period_type_id == td.get_id_of_name('product_period_type', 'months'):
                cover_from_date = add_months_to_date(cover_from_date, wait_period)
                return cover_from_date

            if wait_period_type_id == td.get_id_of_name('product_period_type', 'calendar_months'):
                cover_from_date = add_months_to_date(first_day_of_month(add_months_to_date(cover_from_date, 1)), wait_period)
                return cover_from_date

            if wait_period_type_id == td.get_id_of_name('product_period_type', 'years'):
                cover_from_date = add_months_to_date(cover_from_date, (wait_period*12))
                return cover_from_date
        return cover_from_date

    def set_cover_to_date(self, cover_from_date=None, cover_period=None, *args, **kwargs):
        cover_to_date = None
        if cover_period and cover_period_type_id:
            #set the cover to date
            if wait_period_type_id == td.get_id_of_name('product_period_type', 'days'):
                cover_to_date = add_days_to_date(cover_from_date, cover_period)
                return cover_to_date

            if wait_period_type_id == td.get_id_of_name('product_period_type', 'months'):
                cover_to_date = add_months_to_date(cover_from_date, cover_period)
                return cover_to_date

            if wait_period_type_id == td.get_id_of_name('product_period_type', 'calendar_months'):
                cover_to_date = add_months_to_date(first_day_of_month(add_months_to_date(cover_from_date, 1)), cover_period)
                return cover_to_date

            if wait_period_type_id == td.get_id_of_name('product_period_type', 'years'):
                cover_to_date = add_months_to_date(cover_from_date, (cover_period*12))
                return cover_to_date

        return cover_to_date

    def write_new_policy_date(self, *args, **kwargs):
        usernow = request.identity['user']
        this = PolicyDate()
        this.product_id = kwargs.get('product_id', None)
        this.policy_date_type_id = kwargs.get('policy_date_type_id', None)
        this.date = kwargs.get('date', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id
