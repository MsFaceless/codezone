# -*- coding: utf-8 -*-
"""Product controller module"""

from webob.static import FileApp
from tg import predicates, require
from tg import response, use_wsgi_app
from tg import expose, redirect, validate, flash, url, request

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from rocket.model import *

from sqlalchemy import func, desc, asc ,  or_

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController
from rocket.lib.type_utils import TypeDictionary
from rocket.lib.tgfileuploader import FileUploader
from rocket.lib.contract_document import ContractDocument
from rocket.controllers.common import CommonController
FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
UPLOADS_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'uploads')
SEARCHKEY_PRODUCTALLOCATION = 'BenefitAllocation_SearchKeyword'
SEARCHKEY_GENERALLEDGERACCOUNTS ='GeneralLedgerAccount_SearchKeyword'
SEARCHKEY_PRODUCT ='Product_SearchKeyword'
SEARCHKEY_CLAIMQUESTION ='ClaimQuestions_SearchKeyword'
LIMIT = 20
TYPEUTIL = TypeDictionary()
COMMON = CommonController()
class ProductController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

###############################################################################
# Product - Voucher, Traditional
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_product_html(*args, **kwargs)
        javascript = self.get_javascript_product_onload()
        title = _("Products")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_product_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_PRODUCT
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)

        selectbox_product_states = self.get_selectbox_product_states(**{ 'id' : 'product_state_id', 'class_names': 'col-md-4', })
        selectbox_product_types = self.get_selectbox_product_types(**{ 'id' : 'product_type_id', 'class_names': 'col-md-4', })
        producttable = self.get_product_htmltable(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Products</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_product" class="btn btn-primary ml-auto">Create New Product</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-8 d-flex">
                            <input type="text" class="form-control search" name="searchphrase"  id='searchphrase'  value='{searchphrase}' placeholder="Search by Code or Description"">
                            {selectbox_product_states}
                            {selectbox_product_types}
                        </div>
                        <div class="col-md-4 pl-0">
                            <button class="btn btn-primary" id='action_search'>Search</button>
                           <button class="btn btn-primary" id='btn_reset'>Reset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div id='div_product_table' class="table-responsive">
                        {producttable}
                    </div>
                </div>
                </div>
            </div>
        """
        javascript = """
            <script>
                $("#create_product").click(function(){
                    $('#dialogdiv').load('/product/get_modal_new_product?', function(data){
                    return false;
                    });
                });
                  $('#action_search').click(function(){
                     var kwargs = 'searchphrase='+$('#searchphrase').val();
                     $('#div_product_table').load('/product/get_product_htmltable', kwargs, function(data){
                         return false;
                     });
                 })
                 $('#btn_reset').click(function(){
                  $('#searchphrase').val('').focus();
                     $('#div_product_table').load('/product/get_product_htmltable', 'reset=true', function(data){
                         return false;
                     });
                 })
                 </script>
                 """
        return html +javascript

    @expose()
    def get_javascript_product_onload(self, *args, **kwargs):
        javascript = """

        """
        return javascript

    @expose()
    def get_product_htmltable(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"
        outputlist = []
        dbase_query = self.get_active_product_list(**kwargs)

        sandbox = TYPEUTIL.get_id_of_name('product_state_type', 'sandbox')
        voucher = TYPEUTIL.get_id_of_name('product_type', 'voucher')
        traditional = TYPEUTIL.get_id_of_name('product_type', 'traditional')
        short_term_services = TYPEUTIL.get_id_of_name('product_type', "short_term_-_services")
        short_term_assets = TYPEUTIL.get_id_of_name('product_type', "short_term_-_assets")

        for item in dbase_query:

            disable_text = 'disable' if item.active else 'enable'

            code = item.code
            if item.product_type_id == voucher:
                code = f"<div class='edit voucher_product_edit' product_id='{item.id}'>{item.code}</div>"

            if item.product_type_id == traditional:
                code = f"<div class='edit traditional_product_edit' product_id='{item.id}'>{item.code}</div>"

            if item.product_type_id == short_term_services:
                code = f"<div class='edit short_term_product_edit' product_id='{item.id}'>{item.code}</div>"

            if item.product_type_id == short_term_assets:
                code = f"<div class='edit short_term_product_edit' product_id='{item.id}'>{item.code}</div>"

            product_type_name = TYPEUTIL.get_pretty_name('product_type', item.product_type_id)
            product_state_name = TYPEUTIL.get_pretty_name('product_state_type', item.product_state_id)

            product_assured_type_name = None
            if item.product_assured_type_id:
                product_assured_type_name = TYPEUTIL.get_pretty_name('product_assured_type', item.product_assured_type_id)

            outputlist.append({
                'code' : code,
                'name' : item.name,
                'product_assured_type_id' : product_assured_type_name,
                #'price' : getcurrency(item.price),
                'product_type_id' : product_type_name,
                'state' : product_state_name,
                'active' : img_active if item.active else img_inactive,
                'disable' : f"<div class='product_active' active='{item.active}' product_id='{item.id}' desc='{item.name}'>{disable_text}</div>",
                })
        dbcolumnlist=[
                'code',
                'name',
                'product_assured_type_id',
                #'price',
                'product_type_id',
                'state',
                'active',
                'disable',
                ]
        theadlist=[
                'Code',
                'Name',
                'Assured Type',
                #'Purchase Price',
                'Product Type',
                'Product State',
                'Active',
                '',
                ]
        tdclasslist = [
                'action_link',
                '',
                '',
                #'',
                '',
                '',
                'text-center',
                'action_link text-right',
                ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "product_table", tdclasslist)
        javascript = """
        <script>
            $(".voucher_product_edit").click(function(){
                var data = {product_id : $(this).attr('product_id')};
                $.redirect('/product/edit_voucher', data);
            });
            $(".traditional_product_edit").click(function(){
                var data = {product_id : $(this).attr('product_id')};
                $.redirect('/product/edit_traditional', data);
            });
            $(".short_term_product_edit").click(function(){
                var data = {product_id : $(this).attr('product_id')};
                $.redirect('/product/edit_short_term', data);
            });
            $(".product_edit").click(function(){
                var data = {product_id : $(this).attr('product_id')};
                $.redirect('/product/edit', data);
            });
            $(".product_view").click(function(){
                var data = {product_id : $(this).attr('product_id')};
                $.redirect('/product/view', data);
            });
            $(".product_active").click(function(){
                var text = $(this).html();
                var desc = $(this).attr('desc');
                var result = window.confirm("Are you sure you want to " + text + " '" + desc + "'?");
                if(result === true){
                    var data = 'product_id='+$(this).attr('product_id');
                    $.post('/product/save_product_active?', data, function(data){
                        $.redirect('/product/index');
                        return false;
                    });
                }
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_active_product_list(self, *args, **kwargs):

        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_PRODUCT
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()

        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(Product). \
                filter(or_(
                Product.code.like(searchphrase),
                Product.name.like(searchphrase),
            )). \
            filter(Product.active == 1). \
            order_by(asc(Product.code)).limit(LIMIT)

            return  dbase_query
        else:
            dbase_query = DBSession.query(Product). \
                filter(Product.active == 1). \
                order_by(asc(Product.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def get_modal_new_product(self, *args, **kwargs):
        selectbox_product_types = self.get_selectbox_product_types()
        html = f"""
        <div class="modal fade" id="dialog_new_product" tabindex="-1" role="dialog" aria-labelledby="myproductLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">New Product</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-5 col-form-label" required for="product_type_id">Product Type</label>
                                    <div class="col-md-7">
                                        {selectbox_product_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-5 col-form-label" required for="code">Code</label>
                                    <div class="col-md-7">
                                        <input id="code" type="text" name="code" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-5 col-form-label" required for="name">Description</label>
                                    <div class="col-md-7">
                                        <input id="name" type="text" name="name" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary" id="product_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_new_product');
            $('#save_new_product').click(function(){
                 var valid = FormIsValid("#form_new_product");
                 if(valid){
                    var formserial = $('#form_new_product').serialize();

                    $.post('/product/save_new_product?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect(result.redirect, {'product_id' : result.product_id});
                        };
                        return false;
                    });
                 }
            });
            $('#product_back').click(function(){
                $('#dialog_new_product').modal('hide');
            });
            $('#dialog_new_product').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_new_product(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_type_id = kwargs.get('product_type_id', None)

        sandbox = TYPEUTIL.get_id_of_name('product_state_type', 'sandbox')

        this = Product()
        this.product_type_id = product_type_id
        this.code = kwargs.get('code', None)
        this.name = kwargs.get('name', None)
        this.product_state_id = sandbox
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()

        voucher = TYPEUTIL.get_id_of_name('product_type', 'voucher')
        traditional = TYPEUTIL.get_id_of_name('product_type', 'traditional')
        short_term_services = TYPEUTIL.get_id_of_name('product_type', "short_term_-_services")
        short_term_assets = TYPEUTIL.get_id_of_name('product_type', "short_term_-_assets")

        redirect_url = '/product/index'
        if int(product_type_id) == voucher: redirect_url = '/product/edit_voucher'
        if int(product_type_id) == traditional: redirect_url = '/product/edit_traditional'
        if int(product_type_id) == short_term_services: redirect_url = '/product/edit_short_term'
        if int(product_type_id) == short_term_assets: redirect_url = '/product/edit_short_term'

        return json.dumps({'success' : True, 'product_id' : this.id, 'redirect' : redirect_url})

# ********************* Product Voucher & Traditional ***********************************#

    def get_selectbox_product_states(self, *args, **kwargs):
        kwargs['id'] = 'product_state_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_state_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_types(self, *args, **kwargs):
        kwargs['id'] = 'product_type_id'
        kwargs['required'] = True
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_cover_types(self, *args, **kwargs):
        outputlist = []
        linklist = ProductCoverLink.get_all('id')
        for i in linklist:
            name = TYPEUTIL.get_pretty_name('benefit_cover_and_exclusion_type', i.benefit_cover_and_exclusion_type_id)
            if name: outputlist.append({ 'id' : i.id, 'name' : name, })
        kwargs['required'] = True
        kwargs['id'] = 'benefit_cover_link_id'
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_cover_types(self, *args, **kwargs):
        outputlist = []
        linklist = ProductBenefitCoverLink.get_all('id')
        for i in linklist:
            name = TYPEUTIL.get_pretty_name('benefit_cover_and_exclusion_type', i.benefit_cover_and_exclusion_type_id)
            if name: outputlist.append({ 'id' : i.id, 'name' : name, })
        kwargs['required'] = True
        kwargs['id'] = 'product_benefit_cover_link_id'
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_exclusion_types(self, *args, **kwargs):
        outputlist = []
        linklist = ProductBenefitExclusionLink.get_all('id')
        for i in linklist:
            name = TYPEUTIL.get_pretty_name('benefit_cover_and_exclusion_type', i.benefit_cover_and_exclusion_type_id)
            if name: outputlist.append({ 'id' : i.id, 'name' : name, })
        kwargs['required'] = True
        kwargs['id'] = 'product_benefit_exclusion_link_id'
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_exclusion_expiry_types(self, *args, **kwargs):
        kwargs['id'] = 'product_benefit_exclusion_expiry_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_exclusion_expiry_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_period_effect_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'product_period_effect_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_period_effect_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_period_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'product_period_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_period_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_assured_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'product_assured_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_assured_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_relationship_types(self, *args, **kwargs):
        selected = kwargs.get('selected', None)
        if selected:
            kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_life_assured_relationship_type")
        else:
            product_id = kwargs.get('product_id', None)
            usedlist = ProductLifeAssured.by_attr_all('product_id', product_id)
            usedlist = [int(x.relationship_type_id) for x in usedlist]
            typedict = TYPEUTIL.get_dict_of_types("product_life_assured_relationship_type")
            kwargs['outputlist'] = [{'id' : k, 'name' : v} for k, v in typedict.items() if k not in usedlist]
        kwargs['required'] = True
        kwargs['id'] = 'relationship_type_id'
        return create_selectbox_html(**kwargs)

    def get_selectbox_life_assured_sum_assured_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'product_life_assured_sum_assured_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_life_assured_sum_assured_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_premium_rates(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'product_premium_rate_id'
        dbase_query = RateTable.get_all('code')
        kwargs['outputlist'] = [{'name' : x.code, 'id' : x.id} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_owner(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = kwargs.get('id', 'product_owner_id')
        outputlist = []
        dbase_query = EntityOrganisationProductOwner.get_all('entity_organisation_id')
        for i in dbase_query:
            ent = EntityOrganisation.by_id(i.entity_organisation_id)
            if ent: outputlist.append({'id' : i.id, 'name' : ent.name})
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_insurer(self, *args, **kwargs):
        kwargs['required'] = True
        outputlist = []
        dbase_query = EntityOrganisationInsurer.get_all('entity_organisation_id')
        for i in dbase_query:
            ent = EntityOrganisation.by_id(i.entity_organisation_id)
            if ent: outputlist.append({'id' : i.id, 'name' : ent.name})
        kwargs['id'] = 'insurer_id'
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_price_types(self, *args, **kwargs):
        kwargs['id'] = 'product_price_initial_setup_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_price_initial_setup_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_currency(self, *args, **kwargs):
        dbase_query = Currency.get_all('code')
        kwargs['id'] = 'currency_id'
        kwargs['case_sensitive'] = True
        kwargs['outputlist'] = [{'name' : x.code, 'id' : x.id} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_system_documents(self, product_id=None, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'system_document_id'
        usedlist = ProductSystemDocumentLink.by_attr_all('product_id', product_id)
        usedlist = [int(x.system_document_id) for x in usedlist]
        product = TYPEUTIL.get_id_of_name('system_document_type', 'product')
        dbase_query = SystemDocument.by_attr_all('system_document_type_id', product)
        outputlist = []
        for x in dbase_query:
            if x.id not in usedlist:
                outputlist.append({
                    'id' : x.id,
                    'name' : f"{x.name}: {x.description}",
                })
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_welcome_documents(self, product_id=None, *args, **kwargs):
        """
        usedlist = ProductSystemDocumentLink.by_attr_all('product_id', product_id)
        usedlist = [int(x.system_document_id) for x in usedlist]
        outputlist = []
        for x in dbase_query:
            if x.id not in usedlist:
                outputlist.append({
                    'id' : x.id,
                    'name' : f"{x.name}: {x.description}",
                })
        kwargs['outputlist'] = outputlist
        """
        welcome = TYPEUTIL.get_id_of_name('system_document_type', 'welcome')
        dbase_query = SystemDocument.by_attr_all('system_document_type_id', welcome)
        kwargs['outputlist'] = [{'name' : f"{x.name}: {x.description}", 'id' : x.id} for x in dbase_query]
        kwargs['required'] = True
        kwargs['id'] = 'system_document_id'
        return create_selectbox_html(**kwargs)

    def get_selectbox_claim_questions(self, benefit_id=None, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'claim_question_id'
        usedlist = ProductBenefitClaimQuestionLink.by_attr_all('product_benefit_id', benefit_id)
        usedlist = [int(x.claim_question_id) for x in usedlist]
        dbase_query = ClaimQuestion.get_all('text')
        outputlist = []
        for x in dbase_query:
            if x.id not in usedlist:
                outputlist.append({
                    'id' : x.id,
                    'name' : x.text,
                })
        kwargs['outputlist'] = outputlist
        return create_selectbox_html(**kwargs)

    def get_selectbox_purchase_types(self, *args, **kwargs):
        kwargs['id'] = 'product_purchase_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_purchase_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_period_types(self, *args, **kwargs):
        kwargs['id'] = kwargs.get('id', 'product_period_type_id')
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_period_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_allocation_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = kwargs.get('id', 'product_allocation_type_id')
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_allocation_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_allocations(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = kwargs.get('id', 'product_allocation_id')
        dbase_query = BenefitAllocation.get_all('name')
        kwargs['outputlist'] = [{'name' : x.name, 'id' : x.id} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    def get_selectbox_glaccounts(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = kwargs.get('id', 'gl_account_id')
        dbase_query = GeneralLedgerAccount.get_all('name')
        kwargs['outputlist'] = [{'name' : x.name, 'id' : x.id} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    def get_selectbox_allocation_calculation_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = kwargs.get('id', 'product_allocation_calculation_type_id')
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_allocation_calculation_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_benefit_asset_temp_types(self, *args, **kwargs):
        kwargs['required'] = True
        kwargs['id'] = 'product_benefit_asset_temp_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_asset_temp_type")
        return create_selectbox_html(**kwargs)

    def get_product_benefit_selectbox_benefit_cover_types(self, product_id=None, *args, **kwargs):
        if not product_id: return None
        product = Product.by_id(product_id)
        benefit_count = ProductBenefit.by_attr_count('product_id', product_id)
        benlink = None
        if benefit_count == 0:
            link = ProductCoverLink.by_id(product.benefit_cover_link_id)
            if link:
                benlink = ProductBenefitCoverLink.by_attr_first('benefit_cover_and_exclusion_type_id', link.benefit_cover_and_exclusion_type_id)
                if benlink:
                    selected_benefit_cover_type = benlink.id

        return self.get_selectbox_benefit_cover_types(**{
            'selected' : benlink.id if benlink else None,
        })

    def get_product_benefit_selectbox_benefit_types(self, product_id=None, *args, **kwargs):
        if not product_id: return ''
        main = TYPEUTIL.get_id_of_name('product_benefit_type', 'main_benefit')
        benefit_count = ProductBenefit.by_attr_count('product_id', product_id)
        return self.get_selectbox_benefit_types(**{
            'selected' : main if benefit_count == 0 else None,
        })

    def get_selectbox_benefit_types(self, *args, **kwargs):
        kwargs['id'] = kwargs.get('id', 'product_benefit_type_id')
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_sum_assured_effect_types(self, *args, **kwargs):
        kwargs['id'] = 'product_benefit_effect_on_sum_assured_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_effect_on_sum_assured_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_sum_assured_share_types(self, *args, **kwargs):
        kwargs['id'] = 'product_benefit_share_of_sum_assured_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_share_of_sum_assured_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_stated_benefits(self, *args, **kwargs):
        kwargs['id'] = 'share_of_sum_assured_stated_benefit_id'
        dbase_query = StatedBenefit.get_all('name')
        kwargs['outputlist'] = [{'name' : x.name, 'id' : x.id} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_price_effect_types(self, *args, **kwargs):
        kwargs['id'] = 'product_benefit_effect_on_price_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_effect_on_price_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_benefit_price_share_types(self, *args, **kwargs):
        kwargs['id'] = 'product_benefit_share_of_price_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_benefit_share_of_price_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_product_frequency_types(self, *args, **kwargs):
        kwargs['id'] = 'product_frequency_type_id'
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("product_frequency_type")
        return create_selectbox_html(**kwargs)

    def get_product_title_html(self, product_id=None, *args, **kwargs):
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''
        return f"Edit: {product.code} - {product.name}"

    def get_edit_product_card_title_html(self, product=None, *args, **kwargs):
        if not product: return ''
        product_type_name = TYPEUTIL.get_pretty_name('product_type', product.product_type_id)
        html = f"""
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-8">
                            <h4 class="card-title">Edit {product_type_name} Product: {product.code} - {product.name}</h4>
                        </div>
                        <div class="col-md-4 text-right">
                            <button product_id="{product.id}" class="btn btn-primary ml-auto" id="product_back">Back to Products</button>
                        </div>
                    </div>
                    <div class="row d-flex">
                        <div class="col-md-12">
                            <hr>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#product_back').click(function(){
                $.redirect('/product/index');
            });
        </script>
        """
        return html + javascript

    def get_edit_product_details_html(self, product=None, *args, **kwargs):
        if not product: return ''

        selectbox_cover_types = self.get_selectbox_cover_types(**{
            'selected' : product.benefit_cover_link_id if product.benefit_cover_link_id else None,
        })

        selectbox_assured_types = self.get_selectbox_assured_types(**{
            'selected' : product.product_assured_type_id if product.product_assured_type_id else None,
        })

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Product Details')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Cover Type')}</label>
                                    <div class="col-md-9">
                                        {selectbox_cover_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Assured Type')}</label>
                                    <div class="col-md-9">
                                        {selectbox_assured_types}
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

    def get_edit_product_age_limits_html(self, product=None, *args, **kwargs):
        if not product: return ''

        maturation_html = ''
        traditional = TYPEUTIL.get_id_of_name('product_type', 'traditional')
        if int(product.product_type_id) == traditional:
            maturation_html = f"""
            <div class="col-md-6">
                <div class="form-group row">
                    <label class="col-md-3 col-form-label">{_('Maturation Age')}</label>
                    <div class="col-md-9">
                        <input id="maturation_age" type="number" name="maturation_age" class="form-control">
                    </div>
                </div>
            </div>
            """

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Age Limits')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Min Age')}</label>
                                    <div class="col-md-9">
                                        <input id="minimum_age" type="number" name="minimum_age" class="form-control" required='true' value="0">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label">{_('Max Age')}</label>
                                    <div class="col-md-9">
                                        <input id="maximum_age" type="number" name="maximum_age" class="form-control">
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            {maturation_html}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_edit_product_group_details_html(self, product=None, *args, **kwargs):
        if not product: return ''
        selectbox_product_owner = self.get_selectbox_product_owner(**{
            'selected' : product.product_owner_id if product.product_owner_id else None,
        })
        selectbox_insurer = self.get_selectbox_insurer(**{
            'selected' : product.insurer_id if product.insurer_id else None,
        })
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Group Details')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Product Owner')}</label>
                                    <div class="col-md-9">
                                        {selectbox_product_owner}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label">{_('Insurer')}</label>
                                    <div class="col-md-9">
                                        {selectbox_insurer}
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

    def get_edit_product_pricing_html(self, product=None, *args, **kwargs):
        if not product: return ''

        product_purchase_type_id = None
        if product.product_purchase_type_id:
            product_purchase_type_id = product.product_purchase_type_id

        product_price_initial_setup_type_id = None
        if product.product_price_initial_setup_type_id:
            product_price_initial_setup_type_id = product.product_price_initial_setup_type_id

        disabled = False
        class_names = ''
        voucher = TYPEUTIL.get_id_of_name('product_type', 'voucher')
        if int(product.product_type_id) == voucher:
            class_names = 'product_voucher'
            disabled = True

            if not product_purchase_type_id:
                product_purchase_type_id = TYPEUTIL.get_id_of_name('product_purchase_type', 'group')

            if not product_price_initial_setup_type_id:
                product_price_initial_setup_type_id = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium')

        selectbox_currency = self.get_selectbox_currency(**{
            'selected' : product.currency_id if product.currency_id else None,
        })
        selectbox_purchase_type = self.get_selectbox_purchase_types(**{
            'selected' : product_purchase_type_id,
        })
        selectbox_product_price_type = self.get_selectbox_product_price_types(**{
            'disabled' : disabled,
            'class_names' : class_names,
            'selected' : product_price_initial_setup_type_id,
        })

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Pricing')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Currency')}</label>
                                    <div class="col-md-9">
                                        {selectbox_currency}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Purchase Type')}</label>
                                    <div class="col-md-9">
                                        {selectbox_purchase_type}
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Price Type')}</label>
                                    <div class="col-md-9">
                                        {selectbox_product_price_type}
                                    </div>
                                </div>
                            </div>
                            <div id='price_type_fields' class="col-md-6">
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_edit_product_voucher_durations_html(self, product=None, *args, **kwargs):
        if not product: return ''
        days = TYPEUTIL.get_id_of_name('product_period_type', 'days')
        active_period = self.get_product_period_active_by_product_id(product.id)
        waiting_period = self.get_product_period_waiting_by_product_id(product.id)
        selectbox_period_type_active = self.get_selectbox_period_types(**{
            'id' : 'active_period_type_id',
            'selected' : active_period.product_period_type_id if active_period else days,
            })
        selectbox_period_type_waiting = self.get_selectbox_period_types(**{
            'id' : 'waiting_period_type_id',
            'selected' : waiting_period.product_period_type_id if waiting_period else days,
            })
        active_time_period = active_period.time_period if active_period else ''
        waiting_time_period = waiting_period.time_period if waiting_period else ''
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Durations')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="row">
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required>{_('Active Period')}</label>
                                    <div class="col-md-9">
                                        <input id="active_period" value="{active_time_period}" type="number" name="active_period" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label">{_('Period Type')}</label>
                                    <div class="col-md-9">
                                        {selectbox_period_type_active}
                                    </div>
                                </div>
                            </div>
                        <div class="row">
                        </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label">{_('Waiting Period')}</label>
                                    <div class="col-md-9">
                                        <input id="waiting_period" value="{waiting_time_period}" type="number" name="waiting_period" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label">{_('Period Type')}</label>
                                    <div class="col-md-9">
                                        {selectbox_period_type_waiting}
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

    def get_edit_product_save_html(self, product=None, *args, **kwargs):
        if not product: return ''
        sandbox = TYPEUTIL.get_id_of_name('product_state_type', 'sandbox')
        button_activate = ''
        if product.product_state_id == sandbox:
            button_activate = f"""<button id='product_activate' product_id='{product.id}' class="btn btn-primary">Save & Activate</button>"""
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='product_save' class="btn btn-primary">Save</button>
                        {button_activate}
                        <button class="btn btn-outline-primary products_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('.products_back').click(function(){
                $.redirect('/product/index');
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_message_textarea_html(self, *args, **kwargs):
        text = kwargs.get('text', '')
        name = kwargs.get('name', None)
        label = kwargs.get('label', None)
        maxlength = kwargs.get('maxlength', 255)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="form-group row">
                    <label class="col-md-3 col-form-label">{label}</label>
                    <div class="col-md-9">
                        <textarea name='{name}' type="text" class="form-control" rows="2" maxlength='{maxlength}'>{text}</textarea>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_product_messaging_html(self, product=None, *args, **kwargs):
        if not product: return ''
        hidden_input_product_id = get_hidden_input(**{'id': 'product_id', 'value': product.id})

        popover = self.get_popover_text_merge_html(**kwargs)
        confirmation = TYPEUTIL.get_id_of_name('product_message_type', 'confirmation')
        confirmation_message = self.get_product_message_active_by_product_id_and_message_type(product.id, confirmation)
        confirmation = self.get_message_textarea_html(**{
            'name' : 'confirmation_text',
            'label' : 'Purchase Confirmation',
            'text' : confirmation_message.content if confirmation_message else '',
            })

        reminder = TYPEUTIL.get_id_of_name('product_message_type', 'reminder')
        reminder_message = self.get_product_message_active_by_product_id_and_message_type(product.id, reminder)
        reminder_text = self.get_message_textarea_html(**{
            'name' : 'reminder_text',
            'label' : 'Advanced Reminder',
            'text' : reminder_message.content if reminder_message else '',
            })

        refund = TYPEUTIL.get_id_of_name('product_message_type', 'refund')
        refund_message = self.get_product_message_active_by_product_id_and_message_type(product.id, refund)
        refund_text = self.get_message_textarea_html(**{
            'name' : 'refund_text',
            'label' : 'Refund',
            'text' : refund_message.content if refund_message else '',
            })

        claim = TYPEUTIL.get_id_of_name('product_message_type', 'claim')
        claim_message = self.get_product_message_active_by_product_id_and_message_type(product.id, claim)
        claim_text = self.get_message_textarea_html(**{
            'name' : 'claim_text',
            'label' : 'Redemption / Claim',
            'text' : claim_message.content if claim_message else '',
            })

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Product Messaging</h4>
                            </div>
                            <div class="col-md-6">
                                {popover}
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <form id='form_product_messaging'>
                            {hidden_input_product_id}
                            {confirmation}
                            {reminder_text}
                            {refund_text}
                            {claim_text}
                        </form>
                    </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='product_messaging_save' class="btn btn-primary">Save</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#product_messaging_save').click(function(){
                var formserial = $('#form_product_messaging').serialize();
                $.post('/product/save_edit_product_messaging?', formserial, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_lives_assured_html(self, product_id=None, *args, **kwargs):
        product_id = kwargs.get('product_id', product_id)
        if not product_id: return ''

        amount = TYPEUTIL.get_id_of_name('product_life_assured_sum_assured_type', 'amount')
        percentage = TYPEUTIL.get_id_of_name('product_life_assured_sum_assured_type', 'percentage')

        dbase_query = ProductLifeAssured.by_attr_all('product_id', product_id)
        outputlist = []
        for item in dbase_query:

            relationship = TYPEUTIL.get_pretty_name('product_life_assured_relationship_type', item.relationship_type_id)

            age_range = f"{item.minimum_age} and higher"
            if item.has_maximum_age:
                max_age = ProductLifeAssuredMaxAge.by_attr_first('product_life_assured_id', item.id)
                if max_age: age_rage = f"{item.minimum_age} to {max_age.maximum_age}"

            value = None
            if item.product_life_assured_sum_assured_type_id == amount:
                this = ProductLifeAssuredSumAssuredAmount.by_attr_first('product_life_assured_id', item.id)
                if this: value = f"Amount: {this.amount}"

            if item.product_life_assured_sum_assured_type_id == percentage:
                this = ProductLifeAssuredSumAssuredPercentage.by_attr_first('product_life_assured_id', item.id)
                if this: value = f"{this.percentage}%"

            outputlist.append({
                'relationship_type_id' : f"<div class='edit life_assured_edit action_link' life_assured_id='{item.id}'>{relationship}</div>",
                'age_range' : age_range,
                'value' : value,
                })
        dbcolumnlist=[
                'relationship_type_id',
                'age_range',
                'value',
                ]
        theadlist=[
                'Relationship Type',
                'Age Range',
                'Value',
                ]
        life_assuredtable = build_html_table(outputlist, dbcolumnlist, theadlist, "life_assured_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Assured</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_life_assured" product_id="{product_id}" class="btn btn-primary ml-auto">Add a Assured Type</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {life_assuredtable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_life_assured").click(function(){
                var kwargs = 'product_id='+$(this).attr('product_id');
                $('#dialogdiv').load('/product/get_modal_life_assured?', kwargs, function(data){
                    return false;
                });
            });
            $(".life_assured_edit").click(function(){
                var kwargs = 'life_assured_id='+$(this).attr('life_assured_id');
                kwargs += '&product_id='+$('#product_back').attr('product_id');
                $('#dialogdiv').load('/product/get_modal_life_assured?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_life_assured(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        life_assured_id = kwargs.get('life_assured_id', None)

        title = 'New Assured Type'
        life_assured, max_age = None, None
        if life_assured_id:
            title = 'Edit Assured Type'
            life_assured = ProductLifeAssured.by_id(life_assured_id)
            if life_assured.has_maximum_age:
                max_age = ProductLifeAssuredMaxAge.by_attr_first('product_life_assured_id', life_assured.id)

        selectbox_relationship_types = self.get_selectbox_relationship_types(**{
            'product_id' : product_id,
            'selected' : life_assured.relationship_type_id if life_assured else None,
        })

        selectbox_life_assured_sum_assured_types = self.get_selectbox_life_assured_sum_assured_types(**{
            'selected' : life_assured.product_life_assured_sum_assured_type_id if life_assured else None,
        })

        maximum_lives = life_assured.maximum_lives if life_assured else 1
        minimum_age = life_assured.minimum_age if life_assured else 1
        maximum_age = max_age.maximum_age if max_age else ''

        hidden_input_product_id = get_hidden_input(**{'id': 'product_id', 'value': product_id})
        html = f"""
        <div class="modal fade" id="dialog_life_assured" tabindex="-1" role="dialog" aria-labelledby="mylife_assuredLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_life_assured'>
                            {hidden_input_product_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="relationship_type_id">Relationship Type</label>
                                    <div class="col-md-9">
                                        {selectbox_relationship_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="maximum_lives">Max Lives</label>
                                    <div class="col-md-9">
                                        <input type="number" class="form-control" name='maximum_lives' id='maximum_lives' value="{maximum_lives}" required>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="minimum_age">From Age</label>
                                    <div class="col-md-9">
                                        <input type="number" class="form-control" name='minimum_age' id='minimum_age' value="{minimum_age}" required>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="maximum_age">To Age</label>
                                    <div class="col-md-9">
                                        <input type="number" class="form-control" name='maximum_age' id='maximum_age' value="{maximum_age}">
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_life_assured_sum_assured_type_id">Sum Assured Effect</label>
                                    <div class="col-md-9">
                                        {selectbox_life_assured_sum_assured_types}
                                    </div>
                                </div>
                            </div>
                            <div id='life_assured_type_fields' class="col-md-12">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_life_assured' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary life_assured_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#product_life_assured_sum_assured_type_id').change(function(){
                var selected_sum_assured_type = $('#product_life_assured_sum_assured_type_id option:selected').val();
                var selected_relationship_type = $('#relationship_type_id option:selected').val();
                var kwargs = 'product_life_assured_sum_assured_type_id='+selected_sum_assured_type;
                kwargs += '&relationship_type_id='+selected_relationship_type;
                kwargs += '&product_id='+$('#product_back').attr('product_id');
                $('#life_assured_type_fields').load('/product/get_life_assured_type_html?', kwargs, function(data){
                    return false;
                });
            });
            $('#product_life_assured_sum_assured_type_id').trigger('change');

            var form_id = '#form_life_assured'
            setFormValidation(form_id);
            $('#save_life_assured').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $('#dialog_life_assured').modal('hide');
                    $.post('/product/save_life_assured?', formserial, function(data){
                        $('#tab3').load('/product/get_lives_assured_html?', formserial, function(data){
                            return false;
                        });
                        return false;
                    });
                 }
            });
            $('.life_assured_back').click(function(){
                $('#dialog_life_assured').modal('hide');
            });
            $('#dialog_life_assured').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_product_allocation_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
        if not product_id: return ''
        dbase_query = BenefitAllocationLink.by_attr_all('product_id', product_id)
        outputlist = []
        for item in dbase_query:
            alloc = BenefitAllocation.by_id(item.product_allocation_id)

            value = ''
            amount = BenefitAllocationLinkCalculationAmount.by_attr_first('product_allocation_link_id', item.id)
            if amount: value = f"Amount: {getcurrency(amount.amount)}"

            factor = BenefitAllocationLinkCalculationFactor.by_attr_first('product_allocation_link_id', item.id)
            if factor: value = f"Factor: {factor.factor}"

            percentage = BenefitAllocationLinkCalculationPercentage.by_attr_first('product_allocation_link_id', item.id)
            if percentage: value = f"{percentage.percentage} %"

            glaccount = GeneralLedgerAccount.by_id(item.gl_account_id)

            outputlist.append({
                'name' : f"<div class='edit product_allocation_edit action_link' product_allocation_link_id='{item.id}'>{alloc.name}</div>",
                'allocation_type' : TYPEUTIL.get_pretty_name('product_allocation_type', item.product_allocation_type_id),
                'value' : value,
                'gl_account_id' : glaccount.name,
                })
        dbcolumnlist=[
                'name',
                'allocation_type',
                'value',
                'gl_account_id',
                ]
        theadlist=[
                'Name',
                'Allocation Type',
                'Amount, Factor, %',
                'GL Account',
                ]
        tdclasslist = [
                '',
                '',
                'text-right',
                '',
                ]
        product_allocation_htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "product_allocation_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Allocations</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_product_allocation" product_id="{product_id}" class="btn btn-primary ml-auto">Create New Allocation</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {product_allocation_htmltbl}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_product_allocation").click(function(){
                var kwargs = 'product_id='+$(this).attr('product_id');
                $('#dialogdiv').load('/product/get_modal_product_allocation?', kwargs, function(data){
                    return false;
                });
            });
            $(".product_allocation_edit").click(function(){
                var kwargs = 'product_allocation_link_id='+$(this).attr('product_allocation_link_id');
                kwargs += '&product_id='+$('#product_back').attr('product_id');
                $('#dialogdiv').load('/product/get_modal_product_allocation?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_product_allocation(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        product_allocation_link_id = kwargs.get('product_allocation_link_id', None)

        link = None
        title = "New Product Allocation"
        hidden_input_link_id = ''
        if product_allocation_link_id:
            title = "Edit Product Allocation"
            link = BenefitAllocationLink.by_id(product_allocation_link_id)
            hidden_input_link_id = get_hidden_input(**{'id': 'product_allocation_link_id', 'value': product_allocation_link_id})

        selectbox_allocation_types = self.get_selectbox_allocation_types(**{
            'selected' : link.product_allocation_type_id if link else None,
        })
        selectbox_allocations = self.get_selectbox_allocations(**{
            'selected' : link.product_allocation_id if link else None,
        })
        selectbox_glaccounts = self.get_selectbox_glaccounts(**{
            'selected' : link.gl_account_id if link else None,
        })
        selectbox_allocation_calculation_types = self.get_selectbox_allocation_calculation_types(**{
            'selected' : link.product_allocation_calculation_type_id if link else None,
        })
        hidden_input_product_id = get_hidden_input(**{'id': 'product_id', 'value': product_id})
        html = f"""
        <div class="modal fade" id="dialog_product_allocation" tabindex="-1" role="dialog" aria-labelledby="myproduct_allocationLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_product_allocation'>
                            {hidden_input_link_id}
                            {hidden_input_product_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_allocation_type_id">Allocation Type</label>
                                    <div class="col-md-9">
                                        {selectbox_allocation_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_allocation_id">Allocation</label>
                                    <div class="col-md-9">
                                        {selectbox_allocations}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="gl_account_id">GL Account</label>
                                    <div class="col-md-9">
                                        {selectbox_glaccounts}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_allocation_calculation_type_id">Calculation Type</label>
                                    <div class="col-md-9">
                                        {selectbox_allocation_calculation_types}
                                    </div>
                                </div>
                            </div>
                            <div id='calculation_type_fields' class="col-md-12">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_product_allocation_link' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_allocation_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#product_allocation_calculation_type_id').change(function(){
                var selected = $('#product_allocation_calculation_type_id option:selected').val();
                var kwargs = 'product_allocation_calculation_type_id='+selected;
                var link_id = $('#product_allocation_link_id').val()
                if(link_id){
                    kwargs += '&product_allocation_link_id='+link_id;
                };
                $('#calculation_type_fields').load('/product/get_calculation_type_html?', kwargs, function(data){
                    return false;
                });
            });
            $('#product_allocation_calculation_type_id').trigger('change');

            var form_id = '#form_product_allocation'
            setFormValidation(form_id);
            $('#save_product_allocation_link').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $('#dialog_product_allocation').modal('hide');
                    $.post('/product/save_product_allocation_link?', formserial, function(data){
                        $('#tab3').load('/product/get_product_allocation_html?', formserial, function(data){
                            return false;
                        });
                        return false;
                    });
                 }
            });
            $('.product_allocation_back').click(function(){
                $('#dialog_product_allocation').modal('hide');
            });
            $('#dialog_product_allocation').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_calculation_type_html(self, *args, **kwargs):
        link_id = kwargs.get('product_allocation_link_id', None)
        selected_type_id = int(kwargs.get('product_allocation_calculation_type_id', 0))
        if not selected_type_id: return ''
        link = None
        if link_id:
            link = BenefitAllocationLink.by_id(link_id)

        amount = TYPEUTIL.get_id_of_name('product_allocation_calculation_type', 'amount')
        factor = TYPEUTIL.get_id_of_name('product_allocation_calculation_type', 'factor')
        percentage = TYPEUTIL.get_id_of_name('product_allocation_calculation_type', 'percentage')

        name, value = '', ''
        if selected_type_id == amount:
            name = 'amount'
            if link:
                amount = BenefitAllocationLinkCalculationAmount.by_attr_first('product_allocation_link_id', link_id)
                if amount: value = amount.amount

        if selected_type_id == factor:
            name = 'factor'
            if link:
                factor = BenefitAllocationLinkCalculationFactor.by_attr_first('product_allocation_link_id', link_id)
                if factor: value = factor.factor

        if selected_type_id == percentage:
            name = 'percentage'
            if link:
                percent = BenefitAllocationLinkCalculationPercentage.by_attr_first('product_allocation_link_id', link_id)
                if percent: value = percent.percentage

        return f"""
        <div class="form-group row">
            <label class="col-md-3 col-form-label" required for="{name}">{name.title()}</label>
            <div class="col-md-9">
                <input id="{name}" value="{value}" type="number" name="{name}" class="form-control" required='true'>
            </div>
        </div>
        """

    @expose()
    def get_life_assured_type_html(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        relationship_type_id= kwargs.get('relationship_type_id', None)
        selected_type_id = int(kwargs.get('product_life_assured_sum_assured_type_id', 0))
        if not selected_type_id: return ''

        exists = DBSession.query(ProductLifeAssured). \
                filter(ProductLifeAssured.product_id==product_id). \
                filter(ProductLifeAssured.relationship_type_id == relationship_type_id). \
                filter(ProductLifeAssured.active == True). \
                first()

        amount = TYPEUTIL.get_id_of_name('product_life_assured_sum_assured_type', 'amount')
        percentage = TYPEUTIL.get_id_of_name('product_life_assured_sum_assured_type', 'percentage')

        name, value = '', ''
        if selected_type_id == amount:
            name = 'amount'
            if exists:
                amount = ProductLifeAssuredSumAssuredAmount.by_attr_first('product_life_assured_id', exists.id)
                if amount: value = amount.amount

        if selected_type_id == percentage:
            name = 'percentage'
            if exists:
                percent = ProductLifeAssuredSumAssuredPercentage.by_attr_first('product_life_assured_id', exists.id)
                if percent: value = percent.percentage

        return f"""
        <div class="form-group row">
            <label class="col-md-3 col-form-label" required for="{name}">{name.title()}</label>
            <div class="col-md-9">
                <input id="{name}" type="number" name="{name}" class="form-control" value="{value}" required='true'>
            </div>
        </div>
        """

    @expose()
    def get_product_traditional_contract_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
        if not product_id: return ''
        popover = self.get_popover_text_merge_html(**kwargs)
        hidden_input_product_id = get_hidden_input(**{'id': 'contract_product_id', 'value': product_id})

        contract =  TYPEUTIL.get_id_of_name('product_message_type', 'contract'),
        product_message = DBSession.query(ProductMessage). \
                filter(ProductMessage.product_id == product_id). \
                filter(ProductMessage.product_message_type_id == contract). \
                filter(ProductMessage.active == True). \
                first()
        media = None
        if product_message:
            media = ProductMessageMedia.by_attr_first('product_message_id', product_message.id)

        line_start = media.line_start if media else ''
        content = product_message.content if product_message else ''
        file_path = media.file_path if media else None
        dropzone_html = """
        <div class="col-md-9">
            <div class='dropzone' id='dropzone_product_contract'></div>
        </div>
        """
        if file_path:
            dropzone_html = f"""
            <div class="col-md-4">
                <div class='dropzone' id='dropzone_product_contract'></div>
            </div>
            <div class="col-md-5">
                <img style='max-height: 150px;' src='/uploads/{file_path}' />
            </div>
            """

        html = f"""
        <div class="card">
            <div class="card-header">
                <div class="row d-flex">
                    <div class="col-md-6">
                        <h4 class="card-title">Contract Setup</h4>
                    </div>
                    <div class="col-md-6 text-right">
                        <button id='btn_save_and_preview' product_id='{product_id}' class="btn btn-secondary ml-auto">Save and Preview</button>
                        <button id='btn_save' product_id='{product_id}' class="btn btn-primary ml-auto action_new">Save</button>
                    </div>
                </div>
            </div>
            <div class="card-body">
                <div class="row">
                    <div class="col-md-12">
                        <div class="form-group row">
                            <label class="col-md-3 col-form-label">Backgound</label>
                            {dropzone_html}
                        </div>
                    </div>
                </div>
                <form id='form_product_contract'>
                    {hidden_input_product_id}
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-md-3 col-form-label" required>Line Start</label>
                                <div class="col-md-9">
                                    <input type="text" class="form-control" name='line_start' value="{line_start}" required>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="row">
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-md-3 col-form-label" required>Text</label>
                                <div class="col-md-9 position-relative">
                                    {popover}
                                    <textarea type="text" name='content' class="form-control" rows="9" maxlength='1024' required>{content}</textarea>
                                </div>
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
        """
        javascript = """
        <script>
            $(document).ready(function(){
                var form_id = '#form_product_contract'
                setFormValidation(form_id);

                var contractDropzone = new Dropzone('#dropzone_product_contract', {
                    maxFiles: 1,
                    maxFilesize: 256,
                    parallelUploads: 1,
                    uploadMultiple: false,
                    autoProcessQueue: false,
                    acceptedFiles: '.png, .jpeg, .jpg',
                    url: '/product/handle_file_upload',
                    params: {
                        // To pass extra keys into the uploader
                    },
                    success: function(file, response){
                        var result = JSON.parse(response);
                        if(result.success === true){
                            var formserial = $(form_id).serialize();
                            formserial += '&file_path='+result.name;
                            $.post('/product/save_product_contract?', formserial, function(data){
                                var kwargs = 'product_id='+$('#product_back').attr('product_id');
                                $('#div_system_document_link_html').load('/product/get_product_traditional_contract_html?', kwargs, function(data){
                                    return false;
                                });
                                return false;
                            });
                        };
                    },
                });
                $('#btn_save').click(function(){
                     var valid = FormIsValid(form_id);
                     if(valid){

                        if(contractDropzone.files.length > 0){
                            contractDropzone.processQueue();

                        }else{
                            var formserial = $(form_id).serialize();
                            $.post('/product/save_product_contract?', formserial, function(data){
                                return false;
                            });

                        };
                     };
                });
                $('#btn_save_and_preview').click(function(){
                    $('#btn_save').trigger('click');
                    setTimeout(function(){
                        var formserial = 'product_id='+$('#product_back').attr('product_id');
                        var href_with_formserial = '/product/preview_contract?'+formserial;
                        $.get(href_with_formserial, function(data){
                            if(data != ''){
                                var win = window.open(href_with_formserial, '_blank');
                                win.focus();
                            };
                            return false;
                        });
                    }, 500);

                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def handle_file_upload(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['user_id'] = usernow.id
        kwargs['upload_dir'] = UPLOADS_DIRNAME
        kwargs['size_limit'] = 256000000 # 256 MB
        kwargs['allowed_extensions'] = ['.png', '.jpeg', '.jpg']
        uploader = FileUploader(**kwargs)
        return uploader.handle_file_upload()

    @expose()
    def handle_welcome_upload(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['user_id'] = usernow.id
        kwargs['upload_dir'] = UPLOADS_DIRNAME
        kwargs['size_limit'] = 256000000 # 256 MB
        kwargs['allowed_extensions'] = ['.doc', '.docx', '.pdf']
        uploader = FileUploader(**kwargs)
        return uploader.handle_file_upload()

    @expose()
    def download_welcome(self, *args, **kwargs):
        link_id = kwargs.get('link_id', None)
        if not link_id: return ''
        link = ProductSystemDocumentLink.by_id(link_id)
        if not link: return ''
        output_pdf_filepath = os.path.join(UPLOADS_DIRNAME, link.file_path)
        if not os.path.exists(output_pdf_filepath): return ''
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+remove_hash_from_filename(link.file_path)+'"'
        filecontent = FileApp(output_pdf_filepath)
        return use_wsgi_app(filecontent)

    @expose()
    def preview_contract(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''
        contract =  TYPEUTIL.get_id_of_name('product_message_type', 'contract'),
        product_message = DBSession.query(ProductMessage). \
                filter(ProductMessage.product_id == product_id). \
                filter(ProductMessage.product_message_type_id == contract). \
                filter(ProductMessage.active == True). \
                first()
        if not product_message: return ''
        media = ProductMessageMedia.by_attr_first('product_message_id', product_message.id)
        if not media: return ''
        datenow = datetime.date(datetime.now())
        pdf_file_name = f"{product.code} Contract Preview {datenow}.pdf"
        output_pdf_filepath = os.path.join(PDF_DIRNAME, pdf_file_name)
        image_path = os.path.join(UPLOADS_DIRNAME, media.file_path)
        sane_text = self.get_sane_text(product_message.content)
        doc = ContractDocument(**{
            'filepath' : output_pdf_filepath,
            'line_start' : media.line_start,
            'image_path' : image_path,
            'wording' : sane_text,
        })
        doc.create_pdf()
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+pdf_file_name+'"'
        filecontent = FileApp(output_pdf_filepath)
        return use_wsgi_app(filecontent)

    def get_sane_text(self, text):
        import re
        sane_text = str(text).replace('\n', '<br/>\n')
        match = re.findall(r'\{.+?\}', sane_text)
        for m in match:
            middle = m[1: -1]
            sane = m.replace(middle, f"<b>{middle}</b>")
            sane_text = sane_text.replace(m, sane)
        return sane_text

    @expose()
    def get_system_document_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
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
        button_html = ''
        product = TYPEUTIL.get_id_of_name('system_document_type', 'product')
        count_system_docs = SystemDocument.by_attr_count('system_document_type_id', product)
        if count_system_docs > len(dbase_query):
            button_html = f"""
            <button id='create_product_system_document_link' product_id='{product_id}' class="btn btn-primary ml-auto action_new">Link New Document</button>
            """
        html = f"""
        <div class="card">
            <div class="card-header">
                <div class="row d-flex">
                    <div class="col-md-6">
                        <h4 class="card-title">Product Documents</h4>
                    </div>
                    <div class="col-md-6 text-right">
                        {button_html}
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

    @expose()
    def get_modal_new_product_system_document_link(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        hidden_input_product_id = get_hidden_input(**{'id': 'product_id', 'value': product_id})
        selectbox_system_documents = self.get_selectbox_product_system_documents(product_id)
        html = f"""
        <div class="modal fade" id="dialog_new_product_system_document_link" tabindex="-1" role="dialog" aria-labelledby="myproduct_system_document_linkLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Link New Document</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product_system_document_link'>
                            {hidden_input_product_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Document</label>
                                    <div class="col-md-9">
                                        {selectbox_system_documents}
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product_system_document_link' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_system_document_link_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            var form_id = '#form_new_product_system_document_link'
            setFormValidation(form_id);
            $('#save_new_product_system_document_link').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $('#dialog_new_product_system_document_link').modal('hide');
                    $.post('/product/save_new_product_system_document_link?', formserial, function(data){
                        var kwargs = 'product_id='+$('#product_back').attr('product_id');
                        $('#div_system_document_html').load('/product/get_system_document_html?', kwargs, function(data){
                            return false;
                        });
                        return false;
                    });
                 }
            });
            $('.product_system_document_link_back').click(function(){
                $('#dialog_new_product_system_document_link').modal('hide');
            });
            $('#dialog_new_product_system_document_link').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_product_system_document_link(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        this = ProductSystemDocumentLink()
        this.product_id = kwargs.get('product_id', None)
        this.system_document_id = kwargs.get('system_document_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_delete_product_system_document_link(self, *args, **kwargs):
        link_id = kwargs.get('link_id', None)
        this = ProductSystemDocumentLink.by_id(link_id)
        DBSession.delete(this)
        DBSession.flush()
        return 'true'

    @expose()
    def get_product_contract_documents_html(self, product=None, *args, **kwargs):
        if not product: return ''

        contract_html = ''
        traditional = TYPEUTIL.get_id_of_name('product_type', 'traditional')
        short_term_services = TYPEUTIL.get_id_of_name('product_type', "short_term_-_services")
        short_term_assets = TYPEUTIL.get_id_of_name('product_type', "short_term_-_assets")

        if product.product_type_id == traditional:
            contract_html = self.get_product_traditional_contract_html(product)

        if product.product_type_id == short_term_services:
            contract_html = self.get_product_short_term_contract_html(product)

        if product.product_type_id == short_term_assets:
            contract_html = self.get_product_short_term_contract_html(product)

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

    def get_popover_text_merge_html(self, *args, **kwargs):
        dbase_query = MailMerge.get_all('name')
        inner_html = ''
        for text in dbase_query:
            inner_html += f"""
            <div class='row'>
                <span class='col-6'>
                    {text.code}
                </span
                <span class='col-6'>
                    {text.name}
                </span>
            </div>
            """
        html = f"""
        <i class="now-ui-icons travel_info text-merge"
           id="text_merge"
           title="Options"
           data-content="{inner_html}">
        </i>
        """
        javascript = """
        <script>
            $(document).ready(function(){
                $('#text_merge').popover({
                    html : true,
                })
                $('.nav-link').click(function(){
                    $('#text_merge').popover('hide');
                })
            });
        </script>
        """
        return html + javascript

    @expose()
    def save_product_active(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        product = Product.by_id(product_id)
        product.active = False
        DBSession.flush()
        return 'true'

    @expose()
    def save_edit_product(self, *args, **kwargs):
        voucher_id = kwargs.get('voucher_product_id', None)
        traditional_id = kwargs.get('traditional_product_id', None)
        short_term_id = kwargs.get('short_term_product_id', None)
        if voucher_id:
            return self.save_edit_voucher(**kwargs)
        if traditional_id:
            kwargs['product_id'] = traditional_id
            return self.save_edit_non_voucher(**kwargs)
        if short_term_id:
            kwargs['product_id'] = short_term_id
            return self.save_edit_non_voucher(**kwargs)
        return 'false'

    def save_or_update_product_price(self, product_id=None, *args, **kwargs):
        usernow = request.identity.get('user', {})
        if not product_id: return False
        price = ProductPrice.by_attr_first('product_id', product_id)
        if not price:
            price = ProductPrice()
            price.product_id = product_id
            price.price = kwargs.get('price', None)
            price.added_by = usernow.id
            DBSession.add(price)
            DBSession.flush()
        else:
            price.price = kwargs.get('price', None)
            DBSession.flush()
        return True

    def save_or_update_product_sum_assured(self, product_id=None, *args, **kwargs):
        usernow = request.identity.get('user', {})
        if not product_id: return False
        sum_assured = ProductSumAssured.by_attr_first('product_id', product_id)
        if not sum_assured:
            sum_assured = ProductSumAssured()
            sum_assured.product_id = product_id
            sum_assured.sum_assured = kwargs.get('sum_assured', None)
            sum_assured.added_by = usernow.id
            DBSession.add(sum_assured)
            DBSession.flush()
        else:
            sum_assured.sum_assured = kwargs.get('sum_assured', None)
            DBSession.flush()
        return True

    def get_product_period_active_by_product_id(self, product_id=None, *args, **kwargs):
        if not product_id: return None
        active = TYPEUTIL.get_id_of_name('product_period_effect_type', 'active')
        return DBSession.query(ProductPeriod). \
                filter(ProductPeriod.product_id == product_id). \
                filter(ProductPeriod.product_period_effect_type_id == active). \
                filter(ProductPeriod.active == True). \
                first()

    def get_product_period_waiting_by_product_id(self, product_id=None, *args, **kwargs):
        if not product_id: return None
        waiting = TYPEUTIL.get_id_of_name('product_period_effect_type', 'waiting')
        return DBSession.query(ProductPeriod). \
                filter(ProductPeriod.product_id == product_id). \
                filter(ProductPeriod.product_period_effect_type_id == waiting). \
                filter(ProductPeriod.active == True). \
                first()

    @expose()
    def save_edit_product_messaging(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.get('product_id', None)
        if not product_id: return 'false'

        claim_text = kwargs.get('claim_text', None)
        refund_text = kwargs.get('refund_text', None)
        reminder_text = kwargs.get('reminder_text', None)
        confirmation_text = kwargs.get('confirmation_text', None)

        if claim_text:
            kwargs = {
                'content' : claim_text,
                'product_id' : product_id,
                'product_message_type_id' : TYPEUTIL.get_id_of_name('product_message_type', 'claim'),
            }
            self.save_or_update_product_message(**kwargs)

        if refund_text:
            kwargs = {
                'content' : refund_text,
                'product_id' : product_id,
                'product_message_type_id' : TYPEUTIL.get_id_of_name('product_message_type', 'refund'),
            }
            self.save_or_update_product_message(**kwargs)

        if reminder_text:
            kwargs = {
                'content' : reminder_text,
                'product_id' : product_id,
                'product_message_type_id' : TYPEUTIL.get_id_of_name('product_message_type', 'reminder'),
            }
            self.save_or_update_product_message(**kwargs)

        if confirmation_text:
            kwargs = {
                'content' : confirmation_text,
                'product_id' : product_id,
                'product_message_type_id' : TYPEUTIL.get_id_of_name('product_message_type', 'confirmation'),
            }
            self.save_or_update_product_message(**kwargs)

        return 'true'

    def get_product_message_active_by_product_id_and_message_type(self, product_id=None, product_message_type_id=None, *args, **kwargs):
        if not product_id: return None
        if not product_message_type_id: return None
        return DBSession.query(ProductMessage). \
                filter(ProductMessage.product_id==product_id). \
                filter(ProductMessage.product_message_type_id==product_message_type_id). \
                filter(ProductMessage.active==True). \
                first()

    @expose()
    def save_product_contract(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['product_id'] = kwargs.get('contract_product_id', None)
        kwargs['product_message_type_id'] = TYPEUTIL.get_id_of_name('product_message_type', 'contract')
        product_message_id = self.save_or_update_product_message(**kwargs)
        media = ProductMessageMedia.by_attr_first('product_message_id', product_message_id)
        file_path = kwargs.get('file_path', None)
        if not media:
            media = ProductMessageMedia()
            media.product_message_id = product_message_id
            media.line_start = kwargs.get('line_start', None)
            media.file_path = file_path
            media.added_by = usernow.id
            DBSession.add(media)
            DBSession.flush()
        else:
            media.line_start = kwargs.get('line_start', None)
            if file_path: media.file_path = file_path
            DBSession.flush()
        return 'true'

    def save_or_update_product_message(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.get('product_id', None)
        if not product_id: return False
        product_message_type_id = kwargs.get('product_message_type_id', None)
        content = kwargs.get('content', None)
        product_message = self.get_product_message_active_by_product_id_and_message_type(product_id, product_message_type_id)
        if not product_message:
            product_message = ProductMessage()
            product_message.product_id = product_id
            product_message.product_message_type_id = product_message_type_id
            product_message.content = content
            product_message.added_by = usernow.id
            DBSession.add(product_message)
            DBSession.flush()
        else:
            product_message.content = content
            DBSession.flush()
        return product_message.id

    @expose()
    def check_lives_assured_tab_must_exist(self, *args, **kwargs):
        selected = kwargs.get('product_assured_type_id', None)
        product_assured_type_name = TYPEUTIL.get_name('product_assured_type', selected)
        if 'family' in product_assured_type_name: return 'true'
        return 'false'

    @expose()
    def save_product_allocation_link(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_allocation_link_id = kwargs.get('product_allocation_link_id', None)
        if product_allocation_link_id:
            link = BenefitAllocationLink.by_id(product_allocation_link_id)
            link.product_id = kwargs.get('product_id', None)
            link.gl_account_id = kwargs.get('gl_account_id', None)
            link.product_allocation_id = kwargs.get('product_allocation_id', None)
            link.product_allocation_type_id = kwargs.get('product_allocation_type_id', None)
            link.product_allocation_calculation_type_id = kwargs.get('product_allocation_calculation_type_id', None)
            DBSession.flush()
        else:
            link = BenefitAllocationLink()
            link.product_id = kwargs.get('product_id', None)
            link.gl_account_id = kwargs.get('gl_account_id', None)
            link.product_allocation_id = kwargs.get('product_allocation_id', None)
            link.product_allocation_type_id = kwargs.get('product_allocation_type_id', None)
            link.product_allocation_calculation_type_id = kwargs.get('product_allocation_calculation_type_id', None)
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()
            kwargs['product_allocation_link_id'] = link.id

        amount = kwargs.get('amount', None)
        if amount:
            self.save_or_update_product_allocation_calculation_amount(**kwargs)
            self.delete_old_factors(link.id)
            self.delete_old_percentages(link.id)

        factor = kwargs.get('factor', None)
        if factor:
            self.save_or_update_product_allocation_calculation_factor(**kwargs)
            self.delete_old_amounts(link.id)
            self.delete_old_percentages(link.id)

        percentage = kwargs.get('percentage', None)
        if percentage:
            self.save_or_update_product_allocation_calculation_percentage(**kwargs)
            self.delete_old_amounts(link.id)
            self.delete_old_factors(link.id)

        return 'true'

    def save_or_update_product_allocation_calculation_amount(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        link_id = kwargs.get('product_allocation_link_id', None)
        if not link_id: return False
        amount = kwargs.get('amount', None)
        if not amount: return False
        calc = BenefitAllocationLinkCalculationAmount.by_attr_first('product_allocation_link_id', link_id)
        if calc:
            calc.amount = amount
            DBSession.flush()
        else:
            calc = BenefitAllocationLinkCalculationAmount()
            calc.product_allocation_link_id = link_id
            calc.amount = amount
            calc.added_by = usernow.id
            DBSession.add(calc)
            DBSession.flush()
        return True

    def save_or_update_product_allocation_calculation_factor(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        link_id = kwargs.get('product_allocation_link_id', None)
        if not link_id: return False
        factor = kwargs.get('factor', None)
        if not factor: return False
        calc = BenefitAllocationLinkCalculationFactor.by_attr_first('product_allocation_link_id', link_id)
        if calc:
            calc.factor = factor
            DBSession.flush()
        else:
            calc = BenefitAllocationLinkCalculationFactor()
            calc.product_allocation_link_id = link_id
            calc.factor = factor
            calc.added_by = usernow.id
            DBSession.add(calc)
            DBSession.flush()
        return True

    def save_or_update_product_allocation_calculation_percentage(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        link_id = kwargs.get('product_allocation_link_id', None)
        if not link_id: return False
        percentage = kwargs.get('percentage', None)
        if not percentage: return False
        calc = BenefitAllocationLinkCalculationPercentage.by_attr_first('product_allocation_link_id', link_id)
        if calc:
            calc.percentage = percentage
            DBSession.flush()
        else:
            calc = BenefitAllocationLinkCalculationPercentage()
            calc.product_allocation_link_id = link_id
            calc.percentage = percentage
            calc.added_by = usernow.id
            DBSession.add(calc)
            DBSession.flush()
        return True

    def delete_old_amounts(self, link_id=None, *args, **kwargs):
        oldlist = BenefitAllocationLinkCalculationAmount.by_attr_all('product_allocation_link_id', link_id)
        for item in oldlist:
            DBSession.delete(item)
            DBSession.flush()

    def delete_old_factors(self, link_id=None, *args, **kwargs):
        oldlist = BenefitAllocationLinkCalculationFactor.by_attr_all('product_allocation_link_id', link_id)
        for item in oldlist:
            DBSession.delete(item)
            DBSession.flush()

    def delete_old_percentages(self, link_id=None, *args, **kwargs):
        oldlist = BenefitAllocationLinkCalculationPercentage.by_attr_all('product_allocation_link_id', link_id)
        for item in oldlist:
            DBSession.delete(item)
            DBSession.flush()

    @expose()
    def save_life_assured(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        maximum_age = kwargs.get('maximum_age', None)

        life = ProductLifeAssured()
        life.product_id = kwargs.get('product_id', None)
        life.relationship_type_id = kwargs.get('relationship_type_id', None)
        life.maximum_lives = kwargs.get('maximum_lives', None)
        life.minimum_age = kwargs.get('minimum_age', None)
        life.has_maximum_age = True if maximum_age else False
        life.product_life_assured_sum_assured_type_id = kwargs.get('product_life_assured_sum_assured_type_id', None)
        life.added_by = usernow.id
        DBSession.add(life)
        DBSession.flush()

        maximum_age = kwargs.get('maximum_age', None)
        if maximum_age:
            this = ProductLifeAssuredMaxAge()
            this.product_life_assured_id = life.id
            this.maximum_age = maximum_age
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()

        amount = kwargs.get('amount', None)
        if amount:
            this = ProductLifeAssuredSumAssuredAmount()
            this.product_life_assured_id = life.id
            this.amount = amount
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()

        percentage = kwargs.get('percentage', None)
        if percentage:
            this = ProductLifeAssuredSumAssuredPercentage()
            this.product_life_assured_id = life.id
            this.percentage = percentage
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        return 'true'

    @expose()
    def save_new_product_period(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        period = ProductPeriod()
        period.product_id = kwargs.get('product_id', None)
        period.product_period_effect_type_id = kwargs.get('product_period_effect_type_id', None)
        period.product_period_type_id = kwargs.get('product_period_type_id', None)
        period.time_period = kwargs.get('time_period', None)
        period.added_by = usernow.id
        DBSession.add(period)
        DBSession.flush()
        return 'true'

    @expose()
    def get_product_benefits_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
        if not product_id: return ''
        if not product: product = Product.by_id(product_id)
        html = self.get_product_benefit_htmltbl(product, **kwargs)
        javascript = self.get_javascript_product_benefit_onload()
        return html + javascript

    @expose()
    def get_product_benefit_htmltbl(self, product=None, *args, **kwargs):
        if not product: return ''
        product_id = product.id

        short_term_services = TYPEUTIL.get_id_of_name('product_type', "short_term_-_services")
        short_term_assets = TYPEUTIL.get_id_of_name('product_type', "short_term_-_assets")
        if product.product_type_id == short_term_services \
        or product.product_type_id == short_term_assets:
            fields_html = f"""
            <div id='benefit_exclusion_fields' class="col-md-4"></div>
            <div id='benefit_question_fields' class="col-md-4"></div>
            <div id='benefit_description_fields' class="col-md-4"></div>
            """
        else:
            fields_html = f"""
            <div id='benefit_exclusion_fields' class="col-md-6"></div>
            <div id='benefit_question_fields' class="col-md-6"></div>
            """

        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"

        sum_assured_amount = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'amount')
        sum_assured_percentage = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'percentage')
        sum_assured_stated_benefit = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'stated_benefit')

        price_amount = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'amount')
        price_percentage = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'percentage')

        outputlist = []
        dbase_query = ProductBenefit.by_attr_all('product_id', product_id)
        for item in dbase_query:

            cover_link = None
            link = ProductBenefitCoverLink.by_id(item.product_benefit_cover_link_id)
            if link: cover_link = TYPEUTIL.get_pretty_name('benefit_cover_and_exclusion_type', link.benefit_cover_and_exclusion_type_id)

            benefit_type = None
            if item.product_benefit_type_id:
                benefit_type = TYPEUTIL.get_pretty_name('product_benefit_type', item.product_benefit_type_id)

            sum_assured = TYPEUTIL.get_pretty_name('product_benefit_effect_on_sum_assured_type', item.product_benefit_effect_on_sum_assured_type_id)

            if item.product_benefit_share_of_sum_assured_type_id == sum_assured_amount:
                link = ProductBenefitShareOfSumAssuredAmount.by_attr_first('product_benefit_id', item.id)
                if link: sum_assured = f"Amount {sum_assured}: {link.amount}"

            if item.product_benefit_share_of_sum_assured_type_id == sum_assured_percentage:
                link = ProductBenefitShareOfSumAssuredPercentage.by_attr_first('product_benefit_id', item.id)
                if link: sum_assured = f"Percent {sum_assured}: {link.percentage}"

            if item.product_benefit_share_of_sum_assured_type_id == sum_assured_stated_benefit:
                link = ProductBenefitShareOfSumAssuredStatedBenefit.by_attr_first('product_benefit_id', item.id)
                if link: sum_assured = f"Stated Benefit {sum_assured}: {link.stated_benefit_id}"

            price = TYPEUTIL.get_pretty_name('product_benefit_effect_on_price_type', item.product_benefit_effect_on_price_type_id)

            if item.product_benefit_share_of_price_type_id == price_amount:
                link = ProductBenefitShareOfPriceAmount.by_attr_first('product_benefit_id', item.id)
                if link: price = f"Amount {price}: {link.amount}"

            if item.product_benefit_share_of_price_type_id == price_percentage:
                link = ProductBenefitShareOfPricePercentage.by_attr_first('product_benefit_id', item.id)
                if link: price = f"Percent {price}: {link.percentage}"

            outputlist.append({
                'product_benefit_type_id' : f"<div class='edit product_benefit_edit' product_benefit_id='{item.id}'>{benefit_type}</div>",
                'cover_link_id' : cover_link,
                'name' : item.name,
                'price' : price,
                'sum_assured' : sum_assured,
                'maturity_age' : item.maturity_age,
                'number_of_claims' : item.number_of_claims,
                'is_compulsory' : img_active if item.is_compulsory else img_inactive,
                'claim_terminates_policy' : img_active if item.claim_terminates_policy else img_inactive,
                'allow_multiple_payouts' : img_active if item.allow_multiple_payouts else img_inactive,
                'open' : f"<div class='open_product_benefit_exclusion' benefit_id='{item.id}'>open</div>",
                             })
        dbcolumnlist=[
                'product_benefit_type_id',
                'cover_link_id',
                'name',
                'price',
                'sum_assured',
                'maturity_age',
                'number_of_claims',
                'is_compulsory',
                'claim_terminates_policy',
                'allow_multiple_payouts',
                'open',
                    ]
        theadlist=[
                'Benefit Type',
                'Cover Type',
                'Name',
                'Price',
                'Sum Assured',
                'Maturity Age',
                'Num Claims',
                'Compulsory',
                'Claim Terminates Policy',
                'Allow Multi Payouts',
                '',
                ]
        tdclasslist = [
                'action_link',
                '',
                '',
                '',
                '',
                '',
                '',
                'text-center',
                'text-center',
                'text-center',
                'text-right action_link',
        ]
        htmltbl = build_html_table(outputlist, dbcolumnlist, theadlist, "product_benefit_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Benefit</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_product_benefit" product_id="{product_id}" class="btn btn-primary ml-auto">Create New Benefit</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {htmltbl}
                    </div>
                </div>
                </div>
            </div>
        </div>
        <div class="row">
            {fields_html}
        </div>
        """
        return html

    @expose()
    def get_javascript_product_benefit_onload(self, *args, **kwargs):
        javascript = """
        <script>
            $("#create_product_benefit").click(function(){
                var kwargs = 'product_id='+$(this).attr('product_id');
                $('#dialogdiv').load('/product/get_modal_product_benefit?', kwargs, function(data){
                    return false;
                });
            });
            $(".product_benefit_edit").click(function(){
                var kwargs = 'product_benefit_id='+$(this).attr('product_benefit_id');
                kwargs += '&product_id='+$('#product_back').attr('product_id');
                $('#dialogdiv').load('/product/get_modal_product_benefit?', kwargs, function(data){
                    return false;
                });
            });
            $(".open_product_benefit_exclusion").click(function(){
                var kwargs = 'benefit_id='+$(this).attr('benefit_id');
                $('#benefit_exclusion_fields').load('/product/get_product_benefit_exclusion_htmltbl?', kwargs, function(data){
                    return false;
                });
                $('#benefit_question_fields').load('/product/get_product_benefit_question_htmltbl?', kwargs, function(data){
                    return false;
                });
                $('#benefit_description_fields').load('/product/get_product_benefit_description_htmltbl?', kwargs, function(data){
                    return false;
                });
            });
            $(".open_product_benefit_exclusion:eq(0)").trigger('click');
        </script>
        """
        return javascript

    @expose()
    def get_modal_product_benefit(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''

        short_term_services = TYPEUTIL.get_id_of_name('product_type', "short_term_-_services")
        short_term_assets = TYPEUTIL.get_id_of_name('product_type', "short_term_-_assets")

        if product.product_type_id == short_term_services \
        or product.product_type_id == short_term_assets:
            return self.get_modal_new_product_benefit_short_term(**kwargs)

        return self.get_modal_new_product_benefit_non_short_term(**kwargs)

    @expose()
    def get_product_benefit_asset_premium_rate_fields(self, *args, **kwargs):
        asset_type_id = int(kwargs.get('product_benefit_asset_temp_type_id', 0))
        if not asset_type_id: return ''
        dbase_query = DBSession.query(RateTable). \
                filter(RateTable.product_benefit_asset_temp_type_id==asset_type_id). \
                filter(RateTable.active==True). \
                all()
        kwargs['required'] = True
        kwargs['id'] = 'product_benefit_asset_premium_rate_temp_id'
        kwargs['outputlist'] = [{'name' : x.name, 'id' : x.id} for x in dbase_query]
        selectbox_asset_rates = create_selectbox_html(**kwargs)
        return f"""
        <div class="form-group row">
            <label class="col-md-4 col-form-label" required for="product_benefit_asset_premium_rate_temp_id">Rate Table</label>
            <div class="col-md-8">
                {selectbox_asset_rates}
            </div>
        </div>
        """

    @expose()
    def get_modal_new_product_benefit_short_term(self, *args, **kwargs):
        product_benefit_id = kwargs.get('product_benefit_id', None)
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''
        benefit, asset = None, None
        title = 'New Benefit'
        if product_benefit_id:
            benefit = ProductBenefit.by_id(product_benefit_id)
            if benefit:
                title = 'Edit Benefit'
                asset = ProductBenefitAssetTemp.by_attr_first('product_benefit_id', product_benefit_id)
        description = asset.description if asset else ''
        selectbox_benefit_types = self.get_product_benefit_selectbox_benefit_types(product_id)
        selectbox_benefit_cover_types = self.get_product_benefit_selectbox_benefit_cover_types(product_id)
        selectbox_benefit_asset_types = self.get_selectbox_product_benefit_asset_temp_types(**{
            'selected' : asset.product_benefit_asset_temp_type_id if asset else None,
        })
        hidden_input_product_id = get_hidden_input(**{'id': 'benefit_product_id', 'value': product_id})
        html = f"""
        <div class="modal fade" id="dialog_new_product_benefit" tabindex="-1" role="dialog" aria-labelledby="myproduct_benefitLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product_benefit'>
                            {hidden_input_product_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="name">Name</label>
                                    <div class="col-md-8">
                                        <input id="name" type="text" name="name" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_type_id">Benefit Type</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="cover_link_id">Cover Type</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_cover_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_asset_temp_type_id">Asset Type</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_asset_types}
                                    </div>
                                </div>
                            </div>
                            <div id='div_asset_premium_rate_fields' class="col-md-12">
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="description">Description</label>
                                    <div class="col-md-8">
                                        <textarea required="true" name='description' type="text" class="form-control" rows="4" maxlength='1024'>{description}</textarea>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label"></label>
                                    <div class="form-check col-md-8" style="padding-bottom: 15px;">
                                        <label class="form-check-label">
                                            <input class="form-check-input" name="is_compulsory" id="is_compulsory" type="checkbox">
                                            <span class="form-check-sign">Compulsory</span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product_benefit' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_benefit_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#product_benefit_asset_temp_type_id').change(function(){
                var selected = $('#product_benefit_asset_temp_type_id option:selected').val();
                var kwargs = 'product_benefit_asset_temp_type_id='+selected;
                $('#div_asset_premium_rate_fields').load('/product/get_product_benefit_asset_premium_rate_fields?', kwargs, function(data){
                    return false;
                });
            });
            $('#product_benefit_asset_temp_type_id').trigger('change');

            var form_id = '#form_new_product_benefit'
            setFormValidation(form_id);

            $('#save_new_product_benefit').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    $('#dialog_new_product_benefit').modal('hide');
                    var formserial = $(form_id).serialize();
                    $.post('/product/save_new_product_benefit?', formserial, function(data){
                        var kwargs = 'product_id='+data;
                        $('.tab-pane').last().load('/product/get_product_benefits_html', kwargs, function(data){
                            return false;
                        });
                        return false;
                    });
                 }
            });
            $('.product_benefit_back').click(function(){
                $('#dialog_new_product_benefit').modal('hide');
            });
            $('#dialog_new_product_benefit').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_modal_new_product_benefit_non_short_term(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''
        selectbox_benefit_types = self.get_product_benefit_selectbox_benefit_types(product_id)
        selectbox_benefit_cover_types = self.get_product_benefit_selectbox_benefit_cover_types(product_id)
        selectbox_benefit_sum_assured_effect_types = self.get_selectbox_benefit_sum_assured_effect_types()
        selectbox_benefit_sum_assured_share_types = self.get_selectbox_benefit_sum_assured_share_types()
        selectbox_benefit_price_effect_types = self.get_selectbox_benefit_price_effect_types()
        selectbox_benefit_price_share_types = self.get_selectbox_benefit_price_share_types()
        hidden_input_product_id = get_hidden_input(**{'id': 'benefit_product_id', 'value': product_id})
        html = f"""
        <div class="modal fade" id="dialog_new_product_benefit" tabindex="-1" role="dialog" aria-labelledby="myproduct_benefitLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">New Benefit</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product_benefit'>
                            {hidden_input_product_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_type_id">Benefit Type</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="cover_link_id">Cover Type</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_cover_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="name">Name</label>
                                    <div class="col-md-8">
                                        <input id="name" type="text" name="name" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" for="maturity_age">Maturity Age</label>
                                    <div class="col-md-8">
                                        <input id="maturity_age" type="number" name="maturity_age" class="form-control">
                                    </div>
                                </div>
                            </div>
                            <div class="form-check col-md-12" style="padding-bottom: 15px;">
                                <label class="form-check-label">
                                    <input class="form-check-input" name="limit_claims" id="limit_claims" type="checkbox" checked>
                                    <span class="form-check-sign">Limit Claims</span>
                                </label>
                            </div>
                            <div id='limit_claim_fields' class="col-md-12"></div>
                            <div class="form-check col-md-12" style="padding-bottom: 15px;">
                                <label class="form-check-label">
                                    <input class="form-check-input" name="is_compulsory" id="is_compulsory" type="checkbox">
                                    <span class="form-check-sign">Compulsory</span>
                                </label>
                            </div>
                            <div class="form-check col-md-12" style="padding-bottom: 15px;">
                                <label class="form-check-label">
                                    <input class="form-check-input" name="allow_multiple_payouts" id="allow_multiple_payouts" type="checkbox">
                                    <span class="form-check-sign">Allow Multiple Payouts Per Claim</span>
                                </label>
                            </div>
                            <div id='benefit_payment_frequency_fields' class="col-md-12"></div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_effect_on_sum_assured_type_id">Sum Assured Effect</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_sum_assured_effect_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_share_of_sum_assured_type_id">Sum Assured Share</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_sum_assured_share_types}
                                    </div>
                                </div>
                            </div>
                            <div id='benefit_sum_assured_fields' class="col-md-12">
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_effect_on_price_type_id">Premium Effect</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_price_effect_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="product_benefit_share_of_price_type_id">Premium Share</label>
                                    <div class="col-md-8">
                                        {selectbox_benefit_price_share_types}
                                    </div>
                                </div>
                            </div>
                            <div id='benefit_price_fields' class="col-md-12"></div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product_benefit' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_benefit_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#limit_claims').change(function(){
                var checked = $(this).is(':checked');
                if(checked){
                    $('#limit_claim_fields').load('/product/get_product_benefit_limit_claim_fields?', function(data){
                        return false;
                    });
                }else{
                    $('#limit_claim_fields').empty();
                };
            });
            $('#limit_claims').trigger('change');

            $('#allow_multiple_payouts').change(function(){
                var checked = $(this).is(':checked');
                if(checked){
                    $('#benefit_payment_frequency_fields').load('/product/get_product_benefit_payment_frequency_fields?', function(data){
                        return false;
                    });
                }else{
                    $('#benefit_payment_frequency_fields').empty();
                };
            });

            $('#product_benefit_share_of_sum_assured_type_id').change(function(){
                var selected = $('#product_benefit_share_of_sum_assured_type_id option:selected').val();
                var kwargs = 'product_benefit_share_of_sum_assured_type_id='+selected;
                $('#benefit_sum_assured_fields').load('/product/get_product_benefit_sum_assured_fields?', kwargs, function(data){
                    return false;
                });
            });
            $('#product_benefit_share_of_sum_assured_type_id').trigger('change');

            $('#product_benefit_share_of_price_type_id').change(function(){
                var selected = $('#product_benefit_share_of_price_type_id option:selected').val();
                var kwargs = 'product_benefit_share_of_price_type_id='+selected;
                $('#benefit_price_fields').load('/product/get_product_benefit_price_fields?', kwargs, function(data){
                    return false;
                });
            });
            $('#product_benefit_share_of_price_type_id').trigger('change');

            var form_id = '#form_new_product_benefit'
            setFormValidation(form_id);

            $('#save_new_product_benefit').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    $('#dialog_new_product_benefit').modal('hide');
                    var formserial = $(form_id).serialize();
                    $.post('/product/save_new_product_benefit?', formserial, function(data){
                        var kwargs = 'product_id='+data;
                        $('.tab-pane').last().load('/product/get_product_benefits_html', kwargs, function(data){
                            return false;
                        });
                        return false;
                    });
                 }
            });
            $('.product_benefit_back').click(function(){
                $('#dialog_new_product_benefit').modal('hide');
            });
            $('#dialog_new_product_benefit').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_product_benefit_limit_claim_fields(self, *args, **kwargs):
        return f"""
        <div class="form-group row">
            <label class="col-md-4 col-form-label" required for="number_of_claims">Num Claims</label>
            <div class="col-md-8">
                <input id="number_of_claims" type="number" value="1" name="number_of_claims" class="form-control" required='true'>
            </div>
        </div>
        <div class="form-check col-md-12" style="padding-bottom: 15px;">
            <label class="form-check-label">
                <input class="form-check-input" name="claim_terminates_policy" id="claim_terminates_policy" type="checkbox">
                <span class="form-check-sign">Claim Terminates Policy</span>
            </label>
        </div>
        """

    @expose()
    def get_product_benefit_payment_frequency_fields(self, *args, **kwargs):
        selectbox_product_frequency = self.get_selectbox_product_frequency_types()
        return f"""
        <div class="form-group row">
            <label class="col-md-4 col-form-label" required for="product_frequency_type_id">Frequency Type</label>
            <div class="col-md-8">
                {selectbox_product_frequency}
            </div>
        </div>
        <div class="form-group row">
            <label class="col-md-4 col-form-label" required for="number_of_payments">Num Payouts</label>
            <div class="col-md-8">
                <input id="number_of_payments" type="number" name="number_of_payments" class="form-control" required='true'>
            </div>
        </div>
        """

    @expose()
    def get_product_benefit_sum_assured_fields(self, *args, **kwargs):
        selected = kwargs.get('product_benefit_share_of_sum_assured_type_id', None)
        if not selected: return ''
        selected = int(selected)
        amount = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'amount')
        none = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'none')
        percentage = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'percentage')
        stated_benefit = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'stated_benefit')
        if selected == none:
            return ''

        if selected == amount:
            return f"""
            <div class="form-group row">
                <label class="col-md-4 col-form-label" required for="share_of_sum_assured_amount">Sum Assured Amount</label>
                <div class="col-md-8">
                    <input id="share_of_sum_assured_amount" type="number" name="share_of_sum_assured_amount" class="form-control" required='true'>
                </div>
            </div>
            """

        if selected == percentage:
            return f"""
            <div class="form-group row">
                <label class="col-md-4 col-form-label" required for="share_of_sum_assured_percentage">Sum Assured Percentage</label>
                <div class="col-md-8">
                    <input id="share_of_sum_assured_percentage" type="number" name="share_of_sum_assured_percentage" class="form-control" required='true'>
                </div>
            </div>
            """

        if selected == stated_benefit:
            selectbox_stated_benefits = self.get_selectbox_stated_benefits()
            return f"""
            <div class="form-group row">
                <label class="col-md-4 col-form-label" required for="share_of_sum_assured_stated_benefit_id">Sum Assured Stated Benefit</label>
                <div class="col-md-8">
                    {selectbox_stated_benefits}
                </div>
            </div>
            """

        return ''

    @expose()
    def get_product_benefit_price_fields(self, *args, **kwargs):
        selected = kwargs.get('product_benefit_share_of_price_type_id', None)
        if not selected: return ''
        selected = int(selected)
        amount = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'amount')
        none = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'none')
        percentage = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'percentage')
        if selected == none:
            return ''

        if selected == amount:
            return f"""
            <div class="form-group row">
                <label class="col-md-4 col-form-label" required for="share_of_price_amount">Premium Amount</label>
                <div class="col-md-8">
                    <input id="share_of_price_amount" type="number" name="share_of_price_amount" class="form-control" required='true'>
                </div>
            </div>
            """

        if selected == percentage:
            return f"""
            <div class="form-group row">
                <label class="col-md-4 col-form-label" required for="share_of_price_percentage">Premium Percentage</label>
                <div class="col-md-8">
                    <input id="share_of_price_percentage" type="number" name="share_of_price_percentage" class="form-control" required='true'>
                </div>
            </div>
            """

        return ''

    @expose()
    def save_new_product_benefit(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.get('benefit_product_id', None)
        product = Product.by_id(product_id)
        short_term_services = TYPEUTIL.get_id_of_name('product_type', "short_term_-_services")
        short_term_assets = TYPEUTIL.get_id_of_name('product_type', "short_term_-_assets")
        if product.product_type_id == short_term_services \
        or product.product_type_id == short_term_assets:
            return self.save_new_product_benefit_short_term(**kwargs)
        return self.save_new_product_benefit_non_short_term(**kwargs)

    @expose()
    def save_new_product_benefit_short_term(self, *args, **kwargs):
        usernow = request.identity.get('user', {})

        is_compulsory = kwargs.get('is_compulsory', None)
        is_compulsory = True if is_compulsory else False

        ben = ProductBenefit()
        ben.product_id = kwargs.get('benefit_product_id', None)
        ben.name = kwargs.get('name', None)
        ben.product_benefit_type_id = kwargs.get('product_benefit_type_id', None)
        ben.product_benefit_cover_link_id = kwargs.get('product_benefit_cover_link_id', None)
        ben.is_compulsory = is_compulsory
        ben.added_by = usernow.id
        ben.product_benefit_share_of_price_type_id = 2 # No change
        ben.product_benefit_share_of_sum_assured_type_id = 2 # No change
        ben.product_benefit_effect_on_price_type_id = 2 # No change
        ben.product_benefit_effect_on_sum_assured_type_id = 3 # No change
        DBSession.add(ben)
        DBSession.flush()

        link = ProductBenefitAssetPremiumRateLinkTemp()
        link.product_benefit_id = ben.id
        link.product_benefit_asset_temp_type_id = kwargs.get('product_benefit_asset_temp_type_id', None)
        link.product_benefit_asset_premium_rate_temp_id = kwargs.get('product_benefit_asset_premium_rate_temp_id', None)
        link.added_by = usernow.id
        DBSession.add(link)
        DBSession.flush()

        ass = ProductBenefitAssetTemp()
        ass.product_benefit_id = ben.id
        ass.product_benefit_asset_temp_type_id = kwargs.get('product_benefit_asset_temp_type_id', None)
        ass.description = kwargs.get('description', None)
        ass.added_by = usernow.id
        DBSession.add(ass)
        DBSession.flush()
        return str(ben.product_id)

    @expose()
    def save_new_product_benefit_non_short_term(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.get('benefit_product_id', None)

        is_compulsory = kwargs.get('is_compulsory', None)
        is_compulsory = True if is_compulsory else False

        claim_terminates_policy = kwargs.get('claim_terminates_policy', None)
        claim_terminates_policy = True if claim_terminates_policy else False

        allow_multiple_payouts = kwargs.get('allow_multiple_payouts', None)
        allow_multiple_payouts = True if allow_multiple_payouts else False

        ben = ProductBenefit()
        ben.product_id = product_id
        ben.name = kwargs.get('name', None)
        ben.maturity_age = str_to_int(kwargs.get('maturity_age', None))
        ben.number_of_claims = kwargs.get('number_of_claims', None)
        ben.product_benefit_type_id = kwargs.get('product_benefit_type_id', None)
        ben.product_benefit_cover_link_id = kwargs.get('product_benefit_cover_link_id', None)
        ben.product_benefit_share_of_price_type_id = kwargs.get('product_benefit_share_of_price_type_id', None)
        ben.product_benefit_share_of_sum_assured_type_id = kwargs.get('product_benefit_share_of_sum_assured_type_id', None)
        ben.product_benefit_effect_on_price_type_id = kwargs.get('product_benefit_effect_on_price_type_id', None)
        ben.product_benefit_effect_on_sum_assured_type_id = kwargs.get('product_benefit_effect_on_sum_assured_type_id', None)
        ben.is_compulsory = is_compulsory
        ben.claim_terminates_policy = claim_terminates_policy
        ben.allow_multiple_payouts = allow_multiple_payouts
        ben.added_by = usernow.id
        DBSession.add(ben)
        DBSession.flush()

        if allow_multiple_payouts:
            freq = ProductBenefitPaymentFrequency()
            freq.product_benefit_id = ben.id
            freq.number_of_payments = kwargs.get('number_of_payments', None)
            freq.product_frequency_type_id = kwargs.get('product_frequency_type_id', None)
            freq.added_by = usernow.id
            DBSession.add(freq)
            DBSession.flush()

        sum_assured_amount = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'amount')
        sum_assured_percentage = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'percentage')
        sum_assured_stated_benefit = TYPEUTIL.get_id_of_name('product_benefit_share_of_sum_assured_type', 'stated_benefit')

        if int(ben.product_benefit_share_of_sum_assured_type_id) == sum_assured_amount:
            ben_amount = ProductBenefitShareOfSumAssuredAmount()
            ben_amount.product_benefit_id = ben.id
            ben_amount.amount = kwargs.get('share_of_sum_assured_amount', None)
            ben_amount.added_by = usernow.id
            DBSession.add(ben_amount)
            DBSession.flush()

        if int(ben.product_benefit_share_of_sum_assured_type_id) == sum_assured_percentage:
            ben_percentage = ProductBenefitShareOfSumAssuredPercentage()
            ben_percentage.product_benefit_id = ben.id
            ben_percentage.percentage = kwargs.get('share_of_sum_assured_percentage', None)
            ben_percentage.added_by = usernow.id
            DBSession.add(ben_percentage)
            DBSession.flush()

        if int(ben.product_benefit_share_of_sum_assured_type_id) == sum_assured_stated_benefit:
            ben_stated_benefit = ProductBenefitShareOfSumAssuredStatedBenefit()
            ben_stated_benefit.product_benefit_id = ben.id
            ben_stated_benefit.stated_benefit = kwargs.get('share_of_sum_assured_stated_benefit_id', None)
            ben_stated_benefit.added_by = usernow.id
            DBSession.add(ben_stated_benefit)
            DBSession.flush()

        price_amount = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'amount')
        price_percentage = TYPEUTIL.get_id_of_name('product_benefit_share_of_price_type', 'percentage')

        if int(ben.product_benefit_share_of_price_type_id) == price_amount:
            ben_amount = ProductBenefitShareOfPriceAmount()
            ben_amount.product_benefit_id = ben.id
            ben_amount.amount = kwargs.get('share_of_price_amount', None)
            ben_amount.added_by = usernow.id
            DBSession.add(ben_amount)
            DBSession.flush()

        if int(ben.product_benefit_share_of_price_type_id) == price_percentage:
            ben_percentage = ProductBenefitShareOfPricePercentage()
            ben_percentage.product_benefit_id = ben.id
            ben_percentage.percentage = kwargs.get('share_of_price_percentage', None)
            ben_percentage.added_by = usernow.id
            DBSession.add(ben_percentage)
            DBSession.flush()

        return str(product_id)

    @expose()
    def get_product_benefit_description_htmltbl(self, *args, **kwargs):
        benefit_id = kwargs.get('benefit_id', None)
        if not benefit_id: return ''
        asset = ProductBenefitAssetTemp.by_attr_first('product_benefit_id', benefit_id)
        description = asset.description if asset else ''
        asset_type = ''
        if asset:
            asset_type = TYPEUTIL.get_pretty_name('product_benefit_asset_temp_type', asset.product_benefit_asset_temp_type_id)
        link = ProductBenefitAssetPremiumRateLinkTemp.by_attr_first('product_benefit_id', benefit_id)
        rate_table = None
        if link:
            rate = RateTable.by_id(link.product_benefit_asset_premium_rate_temp_id)
            rate_table = rate.name
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-12">
                                <h4 class="card-title">Asset Description</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            Asset: {asset_type} - {description}
                            <br/>
                            Rate Table: {rate_table}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_product_benefit_question_htmltbl(self, *args, **kwargs):
        benefit_id = kwargs.get('benefit_id', None)
        if not benefit_id: return ''
        benefit = ProductBenefit.by_id(benefit_id)
        if not benefit: return ''
        dbase_query = ProductBenefitClaimQuestionLink.by_attr_all('product_benefit_id', benefit_id)
        outputlist = []
        for item in dbase_query:
            question = ClaimQuestion.by_id(item.claim_question_id)
            answer = ClaimQuestionAnswer.by_id(item.claim_question_correct_answer_id)
            outputlist.append({
                'text' : f"<div class='edit benefit_claim_question_edit action_link' benefit_id='{benefit_id}' benefit_claim_question_id='{item.id}'>{question.text}</div>",
                'answers' : f"<div class='benefit_claim_question_answer' benefit_claim_question_id='{item.id}'>{answer.answer_text}</div>",
                             })
        dbcolumnlist=[
                'text',
                'answers',
                    ]
        theadlist=[
                'Name',
                'Correct Answer',
                ]
        tdclasslist = [
                '',
                'text-right action_link',
        ]
        claimquestiontable = build_html_table(outputlist, dbcolumnlist, theadlist, "benefit_claim_question_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-7">
                            <h4 class="card-title">Questions for: {benefit.name}</h4>
                        </div>
                        <div class="col-md-5 text-right">
                            <button id="link_benefit_claim_question" benefit_id="{benefit_id}" class="btn btn-primary ml-auto">Link Claim Question</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {claimquestiontable}
                    </div>
                </div>
                </div>
            </div>
        </div>
        <div class="row">
            <div class="col-md-12" id='benefit_claim_question_fields'>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#link_benefit_claim_question").click(function(){
                var kwargs = 'benefit_id='+$(this).attr('benefit_id');
                $('#dialogdiv').load('/product/get_modal_benefit_claim_question?', kwargs, function(data){
                    return false;
                });
            });
            $(".benefit_claim_question_edit").click(function(){
                var kwargs = 'benefit_claim_question_id='+$(this).attr('benefit_claim_question_id');
                kwargs += '&benefit_id='+$(this).attr('benefit_id');
                $('#dialogdiv').load('/product/get_modal_benefit_claim_question?', kwargs, function(data){
                    return false;
                });
            });
            $(".benefit_claim_question_answer").click(function(){
                var kwargs = 'benefit_claim_question_id='+$(this).attr('benefit_claim_question_id');
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_benefit_claim_question(self, *args, **kwargs):
        benefit_id = kwargs.get('benefit_id', None)
        if not benefit_id: return ''
        benefit = ProductBenefit.by_id(benefit_id)
        if not benefit: return ''
        question = None
        hidden_input_question_id = ''
        question_id = kwargs.get('benefit_claim_question_id', None)
        if question_id:
            question = ClaimQuestion.by_id(question_id)
            hidden_input_question_id = get_hidden_input(**{'id': 'benefit_claim_question_id', 'value': question_id})
        hidden_input_benefit_id = get_hidden_input(**{'id': 'product_benefit_id', 'value': benefit_id})
        selectbox_claim_questions = self.get_selectbox_claim_questions(benefit_id)
        html = f"""
        <div class="modal fade" id="dialog_benefit_claim_question" tabindex="-1" role="dialog" aria-labelledby="mybenefit_claim_questionLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Claim Question for: {benefit.name}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_benefit_claim_question'>
                            {hidden_input_benefit_id}
                            {hidden_input_question_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="text">Question Text</label>
                                    <div class="col-md-9">
                                        {selectbox_claim_questions}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12" id='div_question_answer_fields'>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_benefit_claim_question' benefit_id="{benefit_id}" class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary benefit_claim_question_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#claim_question_id').change(function(){
                var selected = $('#claim_question_id option:selected').val();
                var kwargs = 'claim_question_id='+selected;
                $('#div_question_answer_fields').load('/product/get_claim_question_answers_html?', kwargs, function(data){
                    return false;
                });
            });
            $('#claim_question_id').trigger('change');

            var form_id = '#form_benefit_claim_question';
            setFormValidation(form_id);
            $('#save_benefit_claim_question').click(function(){
                 var benefit_id = $(this).attr('benefit_id');
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $('#dialog_benefit_claim_question').modal('hide');
                    $.post('/product/save_benefit_claim_question?', formserial, function(data){
                        $('.open_product_benefit_exclusion[benefit_id='+benefit_id+']').trigger('click');
                        return false;
                    });
                 }
            });
            $('.benefit_claim_question_back').click(function(){
                $('#dialog_benefit_claim_question').modal('hide');
            });
            $('#dialog_benefit_claim_question').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_benefit_claim_question(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        link = ProductBenefitClaimQuestionLink()
        link.product_benefit_id = kwargs.get('product_benefit_id', None)
        link.claim_question_id = kwargs.get('claim_question_id', None)
        link.claim_question_correct_answer_id = kwargs.get('claim_question_correct_answer_id', None)
        link.added_by = usernow.id
        DBSession.add(link)
        DBSession.flush()
        return 'true'

    @expose()
    def get_product_benefit_exclusion_htmltbl(self, *args, **kwargs):
        benefit_id = kwargs.get('benefit_id', None)
        if not benefit_id: return ''
        benefit = ProductBenefit.by_id(benefit_id)
        if not benefit: return ''

        infinite = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'infinite')
        days = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_days')
        count = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_premiums')

        outputlist = []
        dbase_query = ProductBenefitExclusion.by_attr_all('product_benefit_id', benefit_id)
        for item in dbase_query:

            link = ProductBenefitExclusionLink.by_id(item.product_benefit_exclusion_link_id)
            exclusion_link = TYPEUTIL.get_pretty_name('benefit_cover_and_exclusion_type', link.benefit_cover_and_exclusion_type_id)
            expiry_type = TYPEUTIL.get_pretty_name('product_benefit_exclusion_expiry_type', item.product_benefit_exclusion_expiry_type_id)

            expiry = None
            if item.product_benefit_exclusion_expiry_type_id == infinite:
                expiry = "Infinite"

            if item.product_benefit_exclusion_expiry_type_id == days:
                link = ProductBenefitExclusionExpiryDays.by_attr_first('product_benefit_exclusion_id', item.id)
                expiry = f"{link.number_of_days} Days"

            if item.product_benefit_exclusion_expiry_type_id == count:
                link = ProductBenefitExclusionExpiryCount.by_attr_first('product_benefit_exclusion_id', item.id)
                expiry = f"{link.count} Premiums"

            outputlist.append({
                'product_benefit_exclusion_link_id' : f"<div class='edit product_benefit_exclusion_edit' product_benefit_exclusion_id='{item.id}'>{exclusion_link}</div>",
                'product_benefit_exclusion_expiry_type_id' : expiry_type,
                'expiry' : expiry,
                             })
        dbcolumnlist=[
                'product_benefit_exclusion_link_id',
                'product_benefit_exclusion_expiry_type_id',
                'expiry',
                    ]
        theadlist=[
                'Exclusion',
                'Expiry',
                'Expiry',
                ]
        tdclasslist = [
                '',
                '',
                'text-right',
        ]
        product_benefit_exclusiontable = build_html_table(outputlist, dbcolumnlist, theadlist, "product_benefit_exclusion_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-8">
                            <h4 class="card-title">Exclusions for: {benefit.name}</h4>
                        </div>
                        <div class="col-md-4 text-right">
                            <button id="create_product_benefit_exclusion" benefit_id="{benefit_id}" class="btn btn-primary ml-auto">Add Exclusion</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {product_benefit_exclusiontable}
                    </div>
                </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_product_benefit_exclusion").click(function(){
                var kwargs = 'benefit_id='+$(this).attr('benefit_id');
                $('#dialogdiv').load('/product/get_modal_new_product_benefit_exclusion?', kwargs, function(data){
                    return false;
                });
            });
            $(".product_benefit_exclusion_edit").click(function(){
                var kwargs = 'product_benefit_exclusion_id='+$(this).attr('product_benefit_exclusion_id');
                $('#dialogdiv').load('/product/get_modal_edit_product_benefit_exclusion?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_new_product_benefit_exclusion(self, *args, **kwargs):
        benefit_id = kwargs.get('benefit_id', None)
        if not benefit_id: return ''
        benefit = ProductBenefit.by_id(benefit_id)
        if not benefit: return ''
        hidden_input_benefit_id = get_hidden_input(**{'id': 'benefit_id', 'value': benefit_id})
        selectbox_benefit_exclusion_types = self.get_selectbox_benefit_exclusion_types(**kwargs)
        selectbox_benefit_exclusion_expiry_types = self.get_selectbox_benefit_exclusion_expiry_types()
        html = f"""
        <div class="modal fade" id="dialog_new_product_benefit_exclusion" tabindex="-1" role="dialog" aria-labelledby="myproduct_benefit_exclusionLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">New Exclusion for: {benefit.name}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product_benefit_exclusion'>
                            {hidden_input_benefit_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_benefit_exclusion_link_id">Exclusion Type</label>
                                    <div class="col-md-9">
                                        {selectbox_benefit_exclusion_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_benefit_exclusion_expiry_type_id">Expiry Type</label>
                                    <div class="col-md-9">
                                        {selectbox_benefit_exclusion_expiry_types}
                                    </div>
                                </div>
                            </div>
                            <div id="expiry_type_fields" class="col-md-12">
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product_benefit_exclusion' benefit_id="{benefit_id}" class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_benefit_exclusion_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $('#product_benefit_exclusion_expiry_type_id').change(function(){
                var selected = $('#product_benefit_exclusion_expiry_type_id option:selected').val();
                var kwargs = 'product_benefit_exclusion_expiry_type_id='+selected;
                $('#expiry_type_fields').load('/product/get_product_benefit_expiry_type_fields?', kwargs, function(data){
                    return false;
                });
            });
            $('#product_benefit_exclusion_expiry_type_id').trigger('change');

            var form_id = '#form_new_product_benefit_exclusion'
            setFormValidation(form_id);
            $('#save_new_product_benefit_exclusion').click(function(){
                 var benefit_id = $(this).attr('benefit_id');
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $('#dialog_new_product_benefit_exclusion').modal('hide');
                    $.post('/product/save_new_product_benefit_exclusion?', formserial, function(data){
                        $('.open_product_benefit_exclusion[benefit_id='+benefit_id+']').trigger('click');
                        return false;
                    });
                 };
            });
            $('.product_benefit_exclusion_back').click(function(){
                $('#dialog_new_product_benefit_exclusion').modal('hide');
            });
            $('#dialog_new_product_benefit_exclusion').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_product_benefit_expiry_type_fields(self, *args, **kwargs):
        selected = kwargs.get('product_benefit_exclusion_expiry_type_id', None)
        if not selected: return ''
        selected = int(selected)
        infinite = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'infinite')
        days = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_days')
        count = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_premiums')

        if selected == infinite:
            return ""

        if selected == days:
            return f"""
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="exclusion_expiry_days">Num Days</label>
                <div class="col-md-9">
                    <input id="exclusion_expiry_days" type="number" name="exclusion_expiry_days" class="form-control" required='true'>
                </div>
            </div>
            """

        if selected == count:
            return f"""
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="exclusion_expiry_count">Num Premiums</label>
                <div class="col-md-9">
                    <input id="exclusion_expiry_count" type="number" name="exclusion_expiry_count" class="form-control" required='true'>
                </div>
            </div>
            """

        return ''

    @expose()
    def save_new_product_benefit_exclusion(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        this = ProductBenefitExclusion()
        this.product_benefit_id = kwargs.get('benefit_id', None)
        this.product_benefit_exclusion_link_id = kwargs.get('product_benefit_exclusion_link_id', None)
        this.product_benefit_exclusion_expiry_type_id = kwargs.get('product_benefit_exclusion_expiry_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()

        days = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_days')
        count = TYPEUTIL.get_id_of_name('product_benefit_exclusion_expiry_type', 'number_of_premiums')

        if int(this.product_benefit_exclusion_expiry_type_id) == days:
            link = ProductBenefitExclusionExpiryDays()
            link.product_benefit_exclusion_id = this.id
            link.number_of_days = kwargs.get('exclusion_expiry_days', None)
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()

        if int(this.product_benefit_exclusion_expiry_type_id) == count:
            link = ProductBenefitExclusionExpiryCount()
            link.product_benefit_exclusion_id = this.id
            link.count = kwargs.get('exclusion_expiry_count', None)
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()

        return 'true'

# ********************* Product Voucher Only ********************************************#

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit_voucher(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: redirect('/product/index')
        product = Product.by_id(product_id)
        if not product: redirect('/product/index')
        html = self.get_edit_voucher_html(*args, **kwargs)
        javascript = self.get_javascript_edit_voucher_onload()
        title = self.get_product_title_html(product_id)
        return dict(title=title, html=html, javascript=javascript)

    def get_edit_voucher_html(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''

        # HEADER
        card_header = self.get_edit_product_card_title_html(product)

        # Commented out as Age Limits are on LifeAssured not directly on Product
        #card_product_age_limits = self.get_edit_product_age_limits_html(product)

        # TAB 1
        hidden_input_product_id = get_hidden_input(**{'id': 'voucher_product_id', 'value': product_id})
        card_product_details = self.get_edit_product_details_html(product)
        card_product_group_details = self.get_edit_product_group_details_html(product)
        card_product_pricing = self.get_edit_product_pricing_html(product)
        card_product_durations = self.get_edit_product_voucher_durations_html(product)
        card_btn_save = self.get_edit_product_save_html(product)
        form_edit_voucher_product = f"""
        <form id='form_edit_voucher_product'>
            {hidden_input_product_id}
            {card_product_details}
            {card_product_group_details}
            {card_product_pricing}
            {card_product_durations}
        </form>
        {card_btn_save}
        """

        # TAB 2
        product_messaging_html = self.get_product_messaging_html(product)

        # TAB 3
        lives_assured_html = self.get_lives_assured_html(product_id)

        # TAB 4
        product_allocation_html = self.get_product_allocation_html(product)

        # TAB 5
        contract_documents_html = self.get_product_contract_documents_html(product)

        # TAB 6
        benefits_html = self.get_product_benefits_html(product)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    <ul class="nav nav-pills nav-pills-primary justify-content-center" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#tab1" role="tablist">
                                Details
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab2" role="tablist">
                                Messaging
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab3" role="tablist">
                                Assured
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab4" role="tablist">
                                Allocations
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab5" role="tablist">
                                Contract & Docs
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab6" role="tablist">
                                Benefits
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="tab-content tab-space tab-subcategories">
                    <div class="tab-pane active" id="tab1">
                        {form_edit_voucher_product}
                    </div>
                    <div class="tab-pane" id="tab2">
                        {product_messaging_html}
                    </div>
                    <div class="tab-pane" id="tab3">
                        {lives_assured_html}
                    </div>
                    <div class="tab-pane" id="tab4">
                        {product_allocation_html}
                    </div>
                    <div class="tab-pane" id="tab5">
                        {contract_documents_html}
                    </div>
                    <div class="tab-pane" id="tab6">
                        {benefits_html}
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_javascript_edit_product_onload(self, *args, **kwargs):
        javascript = """
        $('#product_price_initial_setup_type_id').change(function(){
            var selected = $('#product_price_initial_setup_type_id option:selected').val();
            var kwargs = 'product_price_initial_setup_type_id='+selected;
            kwargs += '&product_id='+$('#product_back').attr('product_id');
            $('#price_type_fields').load('/product/get_price_type_html?', kwargs, function(data){
                return false;
            });
        });
        $('#product_price_initial_setup_type_id').trigger('change');
        """
        return javascript

    def get_javascript_edit_voucher_onload(self, *args, **kwargs):
        javascript = self.get_javascript_edit_product_onload()
        javascript += """
        var form_id = '#form_edit_voucher_product'
        setFormValidation(form_id);
        $('#product_save').click(function(){
             $('#product_price_initial_setup_type_id').prop('disabled', false);
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/product/save_edit_product?', formserial, function(data){
                    return false;
                });
             };
        });
        """
        return javascript

    @expose()
    def get_price_type_html(self, *args, **kwargs):
        selected_type_id = kwargs.get('product_price_initial_setup_type_id', 0)
        if not selected_type_id: return ''
        product_id = kwargs.get('product_id', None)
        product = Product.by_id(product_id)

        rate_table = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'rate_table')
        fixed_premium = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium')
        select_premium = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'select_premium')
        fixed_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_sum_assured')
        select_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'select_sum_assured')
        fixed_premium_and_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium_and_sum_assured')

        selected_type_id = int(selected_type_id)
        if selected_type_id == rate_table:
            selectbox_premium_rates = self.get_selectbox_premium_rates(**{
                'selected' : product.product_premium_rate_id if product.product_premium_rate_id else None,
            })
            return f"""
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="product_premium_rate_id">Premium</label>
                <div class="col-md-9">
                    {selectbox_premium_rates}
                </div>
            </div>
            """

        if selected_type_id == fixed_premium:
            price = ProductPrice.by_attr_first('product_id', product_id)
            price = price.price if price and price.price else ''
            if price: price = getcurrency(price)
            return f"""
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="price">Premium</label>
                <div class="col-md-9">
                    <input id="price" value="{price}" type="number" name="price" class="form-control" required='true'>
                </div>
            </div>
            """

        if selected_type_id == select_premium:
            return ''

        if selected_type_id == fixed_sum_assured:
            sum_assured = ProductSumAssured.by_attr_first('product_id', product_id)
            sum_assured = sum_assured.sum_assured if sum_assured and sum_assured.sum_assured else ''
            if sum_assured: sum_assured = getcurrency(sum_assured)
            return f"""
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="sum_assured">Sum Assured</label>
                <div class="col-md-9">
                    <input id="sum_assured" value="{sum_assured}" type="number" name="sum_assured" class="form-control" required='true'>
                </div>
            </div>
            """

        if selected_type_id == select_sum_assured:
            return ''

        if selected_type_id == fixed_premium_and_sum_assured:
            price = ProductPrice.by_attr_first('product_id', product_id)
            price = price.price if price and price.price else ''
            if price: price = getcurrency(price)
            sum_assured = ProductSumAssured.by_attr_first('product_id', product_id)
            sum_assured = sum_assured.sum_assured if sum_assured and sum_assured.sum_assured else ''
            if sum_assured: sum_assured = getcurrency(sum_assured)
            return f"""
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="price">Premium</label>
                <div class="col-md-9">
                    <input id="price" value="{price}" type="number" name="price" class="form-control" required='true'>
                </div>
            </div>
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required for="sum_assured">Sum Assured</label>
                <div class="col-md-9">
                    <input id="sum_assured" value="{sum_assured}" type="number" name="sum_assured" class="form-control" required='true'>
                </div>
            </div>
            """

        return ''

    @expose()
    def save_edit_voucher(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.get('voucher_product_id', None)
        fixed_premium = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium')

        product = Product.by_id(product_id)
        product.product_owner_id = kwargs.get('product_owner_id', None)
        product.insurer_id = kwargs.get('insurer_id', None)
        product.product_assured_type_id = kwargs.get('product_assured_type_id', None)
        product.currency_id = kwargs.get('currency_id', None)
        product.benefit_cover_link_id = kwargs.get('benefit_cover_link_id', None)
        product.product_purchase_type_id = kwargs.get('product_purchase_type_id', None)
        product.product_price_initial_setup_type_id = fixed_premium
        DBSession.flush()

        self.save_or_update_product_price(product_id, **kwargs)

        active_period = self.get_product_period_active_by_product_id(product_id)
        if not active_period:
            active_period = ProductPeriod()
            active_period.product_id = product_id
            active_period.product_period_effect_type_id = active
            active_period.product_period_type_id = kwargs.get('active_period_type_id', None)
            active_period.time_period = kwargs.get('active_period')
            active_period.added_by = usernow.id
            DBSession.add(active_period)
            DBSession.flush()
        else:
            active_period.product_period_type_id = kwargs.get('active_period_type_id', None)
            active_period.time_period = kwargs.get('active_period')
            DBSession.flush()

        waiting_time_period = kwargs.get('waiting_period')
        if waiting_time_period:
            waiting_period = self.get_product_period_waiting_by_product_id(product_id)
            if not waiting_period:
                waiting_period = ProductPeriod()
                waiting_period.product_id = product_id
                waiting_period.product_period_effect_type_id = waiting
                waiting_period.product_period_type_id = kwargs.get('waiting_period_type_id', None)
                waiting_period.time_period = kwargs.get('waiting_period')
                waiting_period.added_by = usernow.id
                DBSession.add(waiting_period)
                DBSession.flush()
            else:
                waiting_period.product_period_type_id = kwargs.get('waiting_period_type_id', None)
                waiting_period.time_period = waiting_time_period
                DBSession.flush()

        return 'true'

# ********************* Product Short Term Services Only ****************************************#

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit_short_term(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: redirect('/product/index')
        product = Product.by_id(product_id)
        if not product: redirect('/product/index')
        html = self.get_edit_short_term_html(*args, **kwargs)
        javascript = self.get_javascript_edit_short_term_onload()
        title = self.get_product_title_html(product_id)
        return dict(title=title, html=html, javascript=javascript)

    def get_edit_short_term_html(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''

        # HEADER
        card_header = self.get_edit_product_card_title_html(product)

        # Commented out as Age Limits are on LifeAssured not directly on Product
        #card_product_age_limits = self.get_edit_product_age_limits_html(product)

        # TAB 1
        hidden_input_product_id = get_hidden_input(**{'id': 'short_term_product_id', 'value': product_id})
        card_product_details = self.get_edit_product_details_html(product)
        card_product_group_details = self.get_edit_product_group_details_html(product)
        card_product_pricing = self.get_edit_product_pricing_html(product)
        card_product_durations = self.get_edit_product_durations_html(product)
        card_btn_save = self.get_edit_product_save_html(product)
        form_edit_short_term_product = f"""
        <form id='form_edit_short_term_product'>
            {hidden_input_product_id}
            {card_product_details}
            {card_product_group_details}
            {card_product_pricing}
        </form>
        <div id='product_period_fields'>
            {card_product_durations}
        </div>
        {card_btn_save}
        """

        # TAB 2
        product_messaging_html = self.get_product_messaging_html(product)

        # TAB 3
        product_allocation_html = self.get_product_allocation_html(product)

        # TAB 4
        contract_documents_html = self.get_product_contract_documents_html(product)

        # TAB 5
        loaders_html = self.get_product_loaders_html(product)

        # TAB 6
        benefits_html = self.get_product_benefits_html(product)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    <ul class="nav nav-pills nav-pills-primary justify-content-center" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#tab1" role="tablist">
                                Details
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab2" role="tablist">
                                Messaging
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab3" role="tablist">
                                Allocations
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab4" role="tablist">
                                Contract & Docs
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab5" role="tablist">
                                Loaders
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab6" role="tablist">
                                Benefits
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="tab-content tab-space tab-subcategories">
                    <div class="tab-pane active" id="tab1">
                        {form_edit_short_term_product}
                    </div>
                    <div class="tab-pane" id="tab2">
                        {product_messaging_html}
                    </div>
                    <div class="tab-pane" id="tab3">
                        {product_allocation_html}
                    </div>
                    <div class="tab-pane" id="tab4">
                        {contract_documents_html}
                    </div>
                    <div class="tab-pane" id="tab5">
                        {loaders_html}
                    </div>
                    <div class="tab-pane" id="tab6">
                        {benefits_html}
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_javascript_edit_short_term_onload(self, *args, **kwargs):
        javascript = self.get_javascript_edit_product_onload()
        javascript += """
        // SHORT TERM SERVICES
        var form_id = '#form_edit_short_term_product'
        setFormValidation(form_id);
        $('#product_save').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/product/save_edit_product?', formserial, function(data){
                    return false;
                });
             };
        });
        """
        return javascript

    @expose()
    def get_product_short_term_contract_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
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
                                <h4 class="card-title">Welcome Package</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="link_new_document" class="btn btn-primary ml-auto">Upload New Welcome Document</button>
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

                /*
                $.get(href_with_formserial, function(data){
                    console.log(data);
                    if(data != ''){
                        var win = window.open(href_with_formserial, '_blank');
                        win.focus();
                    };
                    return false;
                });
                */
            });
            $("#link_new_document").click(function(){
                var kwargs = 'product_id='+$("#product_back").attr('product_id');
                $('#dialogdiv').load('/product/get_modal_new_welcome_link?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_new_welcome_link(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        hidden_input_product_id = get_hidden_input(**{'id': 'product_id', 'value': product_id})
        selectbox_welcome_documents = self.get_selectbox_product_welcome_documents(product_id)
        html = f"""
        <div class="modal fade" id="dialog_new_welcome_link" tabindex="-1" role="dialog" aria-labelledby="mywelcome_package_linkLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Upload New Welcome Document</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_welcome_link'>
                            {hidden_input_product_id}
                            <div class="form-group row">
                                <label class="col-md-3 col-form-label" required for="name">Document</label>
                                <div class="col-md-9">
                                    {selectbox_welcome_documents}
                                </div>
                            </div>
                        </form>
                        <div class="form-group row">
                            <label class="col-md-3 col-form-label" required for="name">Upload</label>
                            <div class="col-md-9">
                                <div class='dropzone' id='dropzone_product_welcome'></div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_welcome_link' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary welcome_package_link_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_new_welcome_link'
        setFormValidation(form_id);
        var welcomeDropzone = new Dropzone('#dropzone_product_welcome', {
            maxFiles: 1,
            maxFilesize: 256,
            parallelUploads: 1,
            uploadMultiple: false,
            autoProcessQueue: false,
            acceptedFiles: '.doc, .docx, .pdf',
            url: '/product/handle_welcome_upload',
            params: {
                // To pass extra keys into the uploader
            },
            success: function(file, response){
                var result = JSON.parse(response);
                if(result.success === true){
                    var formserial = $(form_id).serialize();
                    formserial += '&file_path='+result.name;
                    $('#dialog_new_welcome_link').modal('hide');
                    $.post('/product/save_new_product_welcome_document_link?', formserial, function(data){
                        var kwargs = 'product_id='+$('#product_back').attr('product_id');
                        $('#div_system_document_link_html').load('/product/get_product_short_term_contract_html?', kwargs, function(data){
                            return false;
                        });
                        return false;
                    });
                };
            },
        });
        $('#save_new_welcome_link').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                welcomeDropzone.processQueue();
             }
        });
        $('.welcome_package_link_back').click(function(){
            $('#dialog_new_welcome_link').modal('hide');
        });
        $('#dialog_new_welcome_link').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_product_welcome_document_link(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.get('product_id', None)
        system_document_id = kwargs.get('system_document_id', None)
        link = DBSession.query(ProductSystemDocumentLink). \
                filter(ProductSystemDocumentLink.product_id == product_id). \
                filter(ProductSystemDocumentLink.system_document_id == system_document_id). \
                filter(ProductSystemDocumentLink.active == True). \
                first()
        if not link:
            link = ProductSystemDocumentLink()
            link.product_id = product_id
            link.system_document_id = system_document_id
            link.file_path = kwargs.get('file_path', None)
            link.added_by = usernow.id
            DBSession.add(link)
            DBSession.flush()
        else:
            link.file_path = kwargs.get('file_path', None)
            DBSession.flush()
        return 'true'

# ********************* Product Traditional Only ****************************************#

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit_traditional(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: redirect('/product/index')
        product = Product.by_id(product_id)
        if not product: redirect('/product/index')
        html = self.get_edit_traditional_html(*args, **kwargs)
        javascript = self.get_javascript_edit_traditional_onload()
        title = self.get_product_title_html(product_id)
        return dict(title=title, html=html, javascript=javascript)

    def get_edit_traditional_html(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        product = Product.by_id(product_id)
        if not product: return ''

        # HEADER
        card_header = self.get_edit_product_card_title_html(product)

        # Commented out as Age Limits are on LifeAssured not directly on Product
        #card_product_age_limits = self.get_edit_product_age_limits_html(product)

        # TAB 1
        hidden_input_product_id = get_hidden_input(**{'id': 'traditional_product_id', 'value': product_id})
        card_product_details = self.get_edit_product_details_html(product)
        card_product_group_details = self.get_edit_product_group_details_html(product)
        card_product_pricing = self.get_edit_product_pricing_html(product)
        card_product_durations = self.get_edit_product_durations_html(product)
        card_btn_save = self.get_edit_product_save_html(product)
        form_edit_traditional_product = f"""
        <form id='form_edit_traditional_product'>
            {hidden_input_product_id}
            {card_product_details}
            {card_product_group_details}
            {card_product_pricing}
        </form>
        <div id='product_period_fields'>
            {card_product_durations}
        </div>
        {card_btn_save}
        """

        # TAB 2
        product_messaging_html = self.get_product_messaging_html(product)

        # TAB 3
        lives_assured_html = self.get_lives_assured_html(product_id)

        # TAB 4
        product_allocation_html = self.get_product_allocation_html(product)

        # TAB 5
        contract_documents_html = self.get_product_contract_documents_html(product)

        # TAB 6
        loaders_html = self.get_product_loaders_html(product)

        # TAB 7
        benefits_html = self.get_product_benefits_html(product)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    <ul class="nav nav-pills nav-pills-primary justify-content-center" role="tablist">
                        <li class="nav-item">
                            <a class="nav-link active" data-toggle="tab" href="#tab1" role="tablist">
                                Details
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab2" role="tablist">
                                Messaging
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab3" role="tablist">
                                Assured
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab4" role="tablist">
                                Allocations
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab5" role="tablist">
                                Contract & Docs
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab6" role="tablist">
                                Loaders
                            </a>
                        </li>
                        <li class="nav-item">
                            <a class="nav-link" data-toggle="tab" href="#tab7" role="tablist">
                                Benefits
                            </a>
                        </li>
                    </ul>
                </div>
                <div class="tab-content tab-space tab-subcategories">
                    <div class="tab-pane active" id="tab1">
                        {form_edit_traditional_product}
                    </div>
                    <div class="tab-pane" id="tab2">
                        {product_messaging_html}
                    </div>
                    <div class="tab-pane" id="tab3">
                        {lives_assured_html}
                    </div>
                    <div class="tab-pane" id="tab4">
                        {product_allocation_html}
                    </div>
                    <div class="tab-pane" id="tab5">
                        {contract_documents_html}
                    </div>
                    <div class="tab-pane" id="tab6">
                        {loaders_html}
                    </div>
                    <div class="tab-pane" id="tab7">
                        {benefits_html}
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_javascript_edit_traditional_onload(self, *args, **kwargs):
        javascript = self.get_javascript_edit_product_onload()
        javascript += """
        // TRADITIONAL
        var form_id = '#form_edit_traditional_product'
        setFormValidation(form_id);
        $('#product_save').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $.post('/product/save_edit_product?', formserial, function(data){
                    return false;
                });
             };
        });
        """
        return javascript

    @expose()
    def get_edit_product_durations_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
        if not product_id: return ''
        dbase_query = ProductPeriod.by_attr_all('product_id', product_id)
        outputlist = []
        for item in dbase_query:

            effect_type = TYPEUTIL.get_pretty_name('product_period_effect_type', item.product_period_effect_type_id)
            period_type = TYPEUTIL.get_pretty_name('product_period_type', item.product_period_type_id)

            outputlist.append({
                'name' : f"<div class='edit product_period_edit' effect_type_id='{item.id}'>{effect_type}</div>",
                'period' : item.time_period,
                'period_type' : period_type,
                })
        dbcolumnlist=[
                'name',
                'period',
                'period_type',
                ]
        theadlist=[
                'Name',
                'Period',
                'Period Type',
                ]
        period_typetable = build_html_table(outputlist, dbcolumnlist, theadlist, "period_type_table")
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Durations')}</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button product_id='{product_id}' id="btn_new_product_period" class="btn btn-primary ml-auto">Add a new Duration</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {period_typetable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#btn_new_product_period").click(function(){
                var kwargs = 'product_id='+$(this).attr('product_id');
                $('#dialogdiv').load('/product/get_modal_new_product_period?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_new_product_period(self, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if not product_id: return ''
        hidden_input_product_id = get_hidden_input(**{'id': 'product_id', 'value': product_id})
        selectbox_period_effect_types = self.get_selectbox_period_effect_types()
        selectbox_period_types = self.get_selectbox_period_types()
        html = f"""
        <div class="modal fade" id="dialog_new_product_period" tabindex="-1" role="dialog" aria-labelledby="myproduct_periodLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Duration / Period</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product_period'>
                            {hidden_input_product_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_period_effect_type_id">Period Effect Type</label>
                                    <div class="col-md-9">
                                        {selectbox_period_effect_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_period_type_id">Period Type</label>
                                    <div class="col-md-9">
                                        {selectbox_period_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="time_period">Period</label>
                                    <div class="col-md-9">
                                        <input id="time_period" type="number" name="time_period" class="form-control">
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product_period' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_period_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            var form_id = '#form_new_product_period'
            setFormValidation(form_id);
            $('#save_new_product_period').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $.post('/product/save_new_product_period?', formserial, function(data){
                        $('#product_period_fields').load('/product/get_edit_product_durations_html?', formserial, function(data){
                            $('#dialog_new_product_period').modal('hide');
                            return false;
                        });
                        return false;
                    });
                 }
            });
            $('.product_period_back').click(function(){
                $('#dialog_new_product_period').modal('hide');
            });
            $('#dialog_new_product_period').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_product_loaders_html(self, product=None, *args, **kwargs):
        product_id = kwargs.get('product_id', None)
        if product and not product_id: product_id = product.id
        if not product_id: return ''
        if not product: product = Product.by_id(product_id)
        if not product: return ''
        available_inner, used_inner = self.get_available_used_product_loader_html(product_id)
        html = f"""
        <div class="row">
            {used_inner}
            {available_inner}
        </div>
        """
        javascript = """
        <script>
            function SegmentClick(selector, href){
                $(selector).click(function(data){
                    var product_id = $(this).attr('product_id');
                    var kwargs = 'product_id='+product_id;
                    kwargs += '&loader_question_id='+$(this).attr('loader_question_id');
                    $.post(href, kwargs, function(data){
                        $('#tab6').load('/product/get_product_loaders_html', kwargs, function(data){
                            return false;
                        });
                    });
                });
            };
            SegmentClick('#div_used .loader_segment', '/product/save_delete_productloader');
            SegmentClick('#div_available .loader_segment', '/product/save_new_productloader');
        </script>
        """
        return html + javascript

    @expose()
    def save_delete_productloader(self, *args, **kwargs):
        this = DBSession.query(ProductLoaderLink). \
                filter(ProductLoaderLink.product_id==kwargs.get('product_id')). \
                filter(ProductLoaderLink.loader_question_id==kwargs.get('loader_question_id')). \
                one()
        DBSession.delete(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_new_productloader(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        link = ProductLoaderLink()
        link.product_id = kwargs.get('product_id', None)
        link.loader_question_id = kwargs.get('loader_question_id', None)
        link.added_by = usernow.id
        DBSession.add(link)
        DBSession.flush()
        return 'true'

    def get_available_used_product_loader_html(self, product_id=None, *args, **kwargs):
        avail, used = '', ''
        loaderlist = LoaderQuestion.get_all('text')
        linklist = ProductLoaderLink.by_attr_all('product_id', product_id)
        idlist = [int(x.loader_question_id) for x in linklist]
        for item in loaderlist:
            effect = TYPEUTIL.get_pretty_name('loader_question_premium_effect_type', item.loader_question_premium_effect_type_id)
            answer_count = LoaderQuestionAnswer.by_attr_count('loader_question_id', item.id)
            element = f"""
                <div class='loader_segment' product_id='{product_id}' loader_question_id='{item.id}'>
                    {item.text} (Effect: {effect}) (Questions: {answer_count})
                </div> """
            if int(item.id) in idlist: used += element
            else: avail += element
        used = f"""
        <div class="col-md-6">
            <div class="card mh_260">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Attached Loaders</h4>
                        </div>
                        <div class="col-md-6 text-right">
                        </div>
                    </div>
                </div>
                <div id='div_used' class="card-body">
                    {used}
                </div>
            </div>
        </div>
        """
        avail = f"""
        <div class="col-md-6">
            <div class="card mh_260">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Available Loaders</h4>
                        </div>
                        <div class="col-md-6 text-right">
                        </div>
                    </div>
                </div>
                <div id='div_available' class="card-body">
                    {avail}
                </div>
            </div>
        </div>
        """
        return avail, used

    @expose()
    def save_edit_non_voucher(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        product_id = kwargs.pop('product_id', None)
        price_type = int(kwargs.get('product_price_initial_setup_type_id', 0))

        # Update the Product
        product = Product.by_id(product_id)
        if not product: return 'false'
        product.product_owner_id = kwargs.get('product_owner_id', None)
        product.insurer_id = kwargs.get('insurer_id', None)
        product.product_assured_type_id = kwargs.get('product_assured_type_id', None)
        product.currency_id = kwargs.get('currency_id', None)
        product.benefit_cover_link_id = kwargs.get('benefit_cover_link_id', None)
        product.product_purchase_type_id = kwargs.get('product_purchase_type_id', None)
        product.product_price_initial_setup_type_id = price_type
        DBSession.flush()

        benefit_based = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'benefit_based')
        if price_type == benefit_based:
            pass

        rate_table = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'rate_table')
        if price_type == rate_table:
            product.product_premium_rate_id = kwargs.get('product_premium_rate_id', None)
            DBSession.flush()

        fixed_premium = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium')
        if price_type == fixed_premium:
            self.save_or_update_product_price(product_id, **kwargs)

        fixed_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_sum_assured')
        if price_type == fixed_sum_assured:
            self.save_or_update_product_sum_assured(product_id, **kwargs)

        fixed_premium_and_sum_assured = TYPEUTIL.get_id_of_name('product_price_initial_setup_type', 'fixed_premium_and_sum_assured')
        if price_type == fixed_premium_and_sum_assured:
            self.save_or_update_product_price(product_id, **kwargs)
            self.save_or_update_product_sum_assured(product_id, **kwargs)

        return 'true'

###############################################################################
# Allocations
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def allocations(self, *args, **kwargs):
        html = self.get_allocations_html(*args, **kwargs)
        javascript = self.get_javascript_allocations_onload()
        title = "Allocations"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_allocations_html(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['searchkey'] = SEARCHKEY_PRODUCTALLOCATION
        searchphrase = COMMON.get_searchphrase(**kwargs)
        allocationstable=  self.get_allocation_htmltable(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Allocations</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_allocations" class="btn btn-primary ml-auto">Create New Allocation</button>
                        </div>
                    </div>
                      <div class="row d-flex align-items-center">
                            <div class="col-md-4">
                                <input type="text" class="form-control search" name="searchphrase"  id='searchphrase'  value='{searchphrase}' placeholder="Search">
                            </div>
                            <div class="col-md-8">
                                <button class="btn btn-primary" id='action_search'>Search</button>
                                <button class="btn btn-primary" id='btn_reset'>Reset</button>
                            </div>
                        </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive" id='div_allocation_table'>
                        {allocationstable}
                    </div>
                </div>
                </div>
            </div>
        """
        javascript = """
              <script>
             $("#create_allocations").click(function(){
                $('#dialogdiv').load('/product/get_modal_new_allocations?', function(data){
                    return false;
                });
            });
                    $('#action_search').click(function(){
                       var kwargs = 'searchphrase='+$('#searchphrase').val();
                       $('#div_allocation_table').load('/product/get_allocation_htmltable', kwargs, function(data){
                           return false;
                       });
                   })
                   $('#btn_reset').click(function(){
                    $('#searchphrase').val('').focus();
                       $('#div_allocation_table').load('/product/get_allocation_htmltable', 'reset=true', function(data){
                           return false;
                       });
                   })
                   </script>
                   """
        return html + javascript

    @expose()
    def get_allocation_htmltable(self, *args, **kwargs):
        dbase_query = self.get_allocations_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'name': f"<div class='allocations_edit' allocation_id='{item.id}'>{item.name}</div>",
            })
        dbcolumnlist = [
            'name',
        ]
        theadlist = [
            'Name',
        ]
        tdclasslist = [
            'action_link',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "allocations_table", tdclasslist)
        javascript = """
           <script>
              $(".allocations_edit").click(function(){
                var kwargs = 'allocation_id='+$(this).attr('allocation_id');
                $('#dialogdiv').load('/product/get_modal_edit_allocations?', kwargs, function(data){
                    return false;
                });
            });
            </script>
            """
        return  html+javascript
    @expose()
    def get_javascript_allocations_onload(self, *args, **kwargs):
        javascript = """


            """
        return javascript

    @expose()
    def get_modal_new_allocations(self, *args, **kwargs):
        html = """
            <div class="modal fade" id="dialog_new_allocations" tabindex="-1" role="dialog" aria-labelledby="myallocationsLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">New Allocation</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_allocations'>
                                <div class="col-md-12">
                                    <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required for="name">Name</label>
                                            <div class="col-md-9">
                                                    <input id="name" type="text" name="name" class="form-control" required='true'>
                                            </div>
                                    </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_allocations' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary allocations_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
        <script>
            setFormValidation('#form_new_allocations');
            $('#save_new_allocations').click(function(){
                 var valid = FormIsValid("#form_new_allocations");
                 if(valid){
                    var formserial = getFormData('#form_new_allocations');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/product/save_new_allocations?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/product/allocations');
                        };
                        return false;
                    });
                 }
            });
            $('.allocations_back').click(function(){
                $('#dialog_new_allocations').modal('hide');
            });
            $('#dialog_new_allocations').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_edit_allocations(self, *args, **kwargs):
        allocation_id = kwargs.get('allocation_id', None)
        if not allocation_id:
            return ''
        this = self.get_allocations_by_id(*args, **kwargs)
        if not this:
            return ''
        checked = 'checked' if this.active else ''
        html = f"""
            <div class="modal fade" id="dialog_edit_allocations" tabindex="-1" role="dialog" aria-labelledby="myallocationsLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">Edit Allocation</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_edit_allocations'>
                                <div style='display: none' class="col-md-6">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="allocation_id">ID</label>
                                                <div class="col-md-9">
                                                        <input id="id" type="text" name="allocation_id" value="{this.id}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="name">Name</label>
                                                <div class="col-md-9">
                                                        <input id="name" type="text" name="name" value="{this.name}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                              <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-3 col-form-label" for="active" required>Active</label>
                                    <div class="col-9">
                                        <div class="form-check">
                                            <label class="form-check-label">
                                                <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/>
                                                <span class="form-check-sign"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_edit_allocations' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary allocations_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
        <script>
            setFormValidation('#form_edit_allocations');
            $('#save_edit_allocations').click(function(){
                var valid = FormIsValid("#form_edit_allocations");
                if(valid){
                    var formserial = getFormData('#form_edit_allocations');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/product/save_edit_allocations?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/product/allocations');
                            };
                        return false;
                        });
                    }
                });
            $('.allocations_back').click(function(){
                $('#dialog_edit_allocations').modal('hide');
                });
            $('#dialog_edit_allocations').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_new_allocations(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity.get('user', {})
        this = BenefitAllocation()
        this.name = data.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_allocations(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity.get('user', {})
        this = self.get_allocations_by_id(**data)
        if not this:
            return json.dumps({'success': False, 'data': 'No allocations found for id provided'})
        this.name = data.get('name', None)
        if not data.get('active', None):
            this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_allocations_by_id(self, *args, **kwargs):
        return DBSession.query(BenefitAllocation). \
                filter(BenefitAllocation.id == kwargs.get('allocation_id', None)). \
                first()

    @expose()
    def get_allocations_list(self, *args, **kwargs):

        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_PRODUCTALLOCATION
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()

        if searchphrase:
            searchphrase = "%" + searchphrase+ "%"
            dbase_query = DBSession.query(BenefitAllocation). \
                    filter(BenefitAllocation.name.like(searchphrase)). \
                    filter(BenefitAllocation.active == 1). \
                    order_by(asc(BenefitAllocation.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(BenefitAllocation). \
                    filter(BenefitAllocation.active == 1). \
                    order_by(asc(BenefitAllocation.id)). \
                    limit(LIMIT)
        return dbase_query

###############################################################################
# General Ledger Accounts - GL Accounts
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def glaccounts(self, *args, **kwargs):
        html = self.get_general_ledger_accounts_html(*args, **kwargs)
        javascript = self.get_javascript_general_ledger_accounts_onload()
        title = "General Ledger Accounts"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_general_ledger_accounts_html(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['searchkey'] = SEARCHKEY_GENERALLEDGERACCOUNTS
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        general_ledger_accountstable=self.get_general_ledger_accounts_htmltable(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">General Ledger Accounts</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_general_ledger_accounts" class="btn btn-primary ml-auto">Create New General Ledger Account</button>
                        </div>
                    </div>
               <div class="row d-flex align-items-center">
                            <div class="col-md-4">
                                <input type="text" class="form-control search" name="searchphrase"  id='searchphrase'  value='{searchphrase}' placeholder="Search">
                            </div>
                            <div class="col-md-8">
                                <button class="btn btn-primary" id='action_search'>Search</button>
                                <button class="btn btn-primary" id='btn_reset'>Reset</button>
                            </div>
                        </div>
                </div>
                <div class="card-body">
                    <div class="table-responsive" id='div_gl_account'>
                        {general_ledger_accountstable}
                    </div>
                </div>
                </div>
            </div>
            """
        javascript = """
                <script>
                      $("#create_general_ledger_accounts").click(function(){
            $('#dialogdiv').load('/product/get_modal_new_general_ledger_accounts?', function(data){
                return false;
                });
            });
                      $('#action_search').click(function(){
                         var kwargs = 'searchphrase='+$('#searchphrase').val();
                         $('#div_gl_account').load('/product/get_general_ledger_accounts_htmltable', kwargs, function(data){
                             return false;
                         });
                     })
                     $('#btn_reset').click(function(){
                      $('#searchphrase').val('').focus();
                         $('#div_gl_account').load('/product/get_general_ledger_accounts_htmltable', 'reset=true', function(data){
                             return false;
                         });
                     })
                     </script>
                     """
        return html +javascript

    @expose()
    def get_general_ledger_accounts_htmltable(self, *args, **kwargs):
        dbase_query = self.get_general_ledger_accounts_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'name': "<div class='edit general_ledger_accounts_edit' general_ledger_accounts_id='{1}'>{0}</div>".format(
                    item.name, item.id),
                'debit_account': item.debit_account,
                'credit_account': item.credit_account,
                'gl_key': item.gl_key,
            })
        dbcolumnlist = [
            'name',
            'debit_account',
            'credit_account',
            'gl_key',
        ]
        theadlist = [
            'Name',
            'Debit Account',
            'Credit Account',
            'GL Key',
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-center',
            'text-right',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, 'glaccounttable', tdclasslist)
        javascript = """
            <script>
              $(".general_ledger_accounts_edit").click(function(){
                  var kwargs = 'general_ledger_accounts_id='+$(this).attr('general_ledger_accounts_id');
                  $('#dialogdiv').load('/product/get_modal_edit_general_ledger_accounts?', kwargs, function(data){
                      return false;
                      });
                  });
                  </script>
              """
        return html + javascript

    @expose()
    def get_javascript_general_ledger_accounts_onload(self, *args, **kwargs):
        javascript ="""
        """
        return javascript

    @expose()
    def get_modal_new_general_ledger_accounts(self, *args, **kwargs):
        html = """
            <div class="modal fade" id="dialog_new_general_ledger_accounts" tabindex="-1" role="dialog" aria-labelledby="mygeneral_ledger_accountsLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">New General Ledger Account</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_general_ledger_accounts'>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="name">Name</label>
                                                <div class="col-md-9">
                                                        <input id="name" type="text" name="name" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="debit_account">Debit Account</label>
                                                <div class="col-md-9">
                                                        <input id="debit_account" type="text" name="debit_account" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="credit_account">Credit Account</label>
                                                <div class="col-md-9">
                                                        <input id="credit_account" type="text" name="credit_account" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="gl_key">Gl Key</label>
                                                <div class="col-md-9">
                                                        <input id="gl_key" type="text" name="gl_key" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_general_ledger_accounts' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary general_ledger_accounts_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
        <script>
            setFormValidation('#form_new_general_ledger_accounts');
            $('#save_new_general_ledger_accounts').click(function(){
                var valid = FormIsValid("#form_new_general_ledger_accounts");
                if(valid){
                    var formserial = getFormData('#form_new_general_ledger_accounts');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/product/save_new_general_ledger_accounts?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/product/glaccounts');
                            };
                        return false;
                        });
                    }
                });
            $('.general_ledger_accounts_back').click(function(){
                $('#dialog_new_general_ledger_accounts').modal('hide');
                });
            $('#dialog_new_general_ledger_accounts').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_edit_general_ledger_accounts(self, *args, **kwargs):
        general_ledger_accounts_id = kwargs.get('general_ledger_accounts_id', None)
        if not general_ledger_accounts_id:
            return ''
        this = self.get_general_ledger_accounts_by_id(*args, **kwargs)
        if not this:
            return ''
        checked = 'checked' if this.active else ''
        html = f"""
            <div class="modal fade" id="dialog_edit_general_ledger_accounts" tabindex="-1" role="dialog" aria-labelledby="mygeneral_ledger_accountsLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">Edit General Ledger Account</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_edit_general_ledger_accounts'>
                                <div style='display: none' class="col-md-6">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="general_ledger_accounts_id">ID</label>
                                                <div class="col-md-9">
                                                        <input id="id" type="text" name="general_ledger_accounts_id" value="{this.id}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="name">Name</label>
                                                <div class="col-md-9">
                                                        <input id="name" type="text" name="name" value="{this.name}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="debit_account">Debit Account</label>
                                                <div class="col-md-9">
                                                        <input id="debit_account" type="text" name="debit_account" value="{this.debit_account}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="credit_account">Credit Account</label>
                                                <div class="col-md-9">
                                                        <input id="credit_account" type="text" name="credit_account" value="{this.credit_account}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                <div class="col-md-12">
                                        <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="gl_key">Gl Key</label>
                                                <div class="col-md-9">
                                                        <input id="gl_key" type="text" name="gl_key" value="{this.gl_key}" class="form-control" required='true'>
                                                </div>
                                        </div>
                                </div>
                                 <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-3 col-form-label" for="active" required>Active</label>
                                    <div class="col-9">
                                        <div class="form-check">
                                            <label class="form-check-label">
                                                <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/>
                                                <span class="form-check-sign"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_edit_general_ledger_accounts' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary general_ledger_accounts_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
        <script>
            setFormValidation('#form_edit_general_ledger_accounts');
            $('#save_edit_general_ledger_accounts').click(function(){
                var valid = FormIsValid("#form_edit_general_ledger_accounts");
                if(valid){
                    var formserial = getFormData('#form_edit_general_ledger_accounts');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/product/save_edit_general_ledger_accounts?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/product/glaccounts');
                            };
                        return false;
                        });
                    }
                });
            $('.general_ledger_accounts_back').click(function(){
                $('#dialog_edit_general_ledger_accounts').modal('hide');
            });
            $('#dialog_edit_general_ledger_accounts').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_new_general_ledger_accounts(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity.get('user', {})
        this = GeneralLedgerAccount()
        this.name = data.get('name', None)
        this.debit_account = data.get('debit_account', None)
        this.credit_account = data.get('credit_account', None)
        this.gl_key = data.get('gl_key', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_general_ledger_accounts(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity.get('user', {})
        this = self.get_general_ledger_accounts_by_id(**data)
        if not this:
            return json.dumps(
                    {'success': False, 'data': 'No general_ledger_accounts found for id provided'})
        this.name = data.get('name', None)
        this.debit_account = data.get('debit_account', None)
        this.credit_account = data.get('credit_account', None)
        this.gl_key = data.get('gl_key', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_general_ledger_accounts_by_id(self, *args, **kwargs):
        return DBSession.query(GeneralLedgerAccount). \
                filter(GeneralLedgerAccount.id == kwargs.get('general_ledger_accounts_id', None)). \
                first()

    @expose()
    def get_general_ledger_accounts_list(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_GENERALLEDGERACCOUNTS
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()
        if searchphrase:
            searchphrase = "%" + searchphrase+ "%"
            dbase_query = DBSession.query(GeneralLedgerAccount). \
                filter(or_(GeneralLedgerAccount.gl_key.like(searchphrase),
                GeneralLedgerAccount.name.like(searchphrase),
                GeneralLedgerAccount.debit_account.like(searchphrase),
                 GeneralLedgerAccount.credit_account.like(searchphrase),
            )). \
                filter(GeneralLedgerAccount.active == 1). \
                order_by(asc(GeneralLedgerAccount.name)).limit(LIMIT)
            return dbase_query

        else:
            dbase_query = DBSession.query(GeneralLedgerAccount). \
                    filter(GeneralLedgerAccount.active == 1). \
                    order_by(asc(GeneralLedgerAccount.id)). \
                    limit(LIMIT)
        return dbase_query

###############################################################################
# Product - Claim Questions and Answers
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def claim_questions(self, *args, **kwargs):
        html = self.get_active_claim_question_html(*args, **kwargs)
        javascript = self.get_javascript_claim_question_onload()
        title = "Claim Question"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_claim_question_html(self, *args, **kwargs):
        usernow = request.identity['user']

        kwargs['searchkey'] = SEARCHKEY_CLAIMQUESTION
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        claim_questiontable= self.get_active_claim_questions_htmltable(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Claim Question</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_claim_question" class="btn btn-primary ml-auto">Create New Claim Question</button>
                            </div>
                        </div>
                         <div class="row d-flex align-items-center">
                            <div class="col-md-4">
                                <input type="text" class="form-control search" name="searchphrase"  id='searchphrase'  value='{searchphrase}' placeholder="Search">
                            </div>
                            <div class="col-md-8">
                                <button class="btn btn-primary" id='action_search'>Search</button>
                                <button class="btn btn-primary" id='btn_reset'>Reset</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive" id='div_claim_questions_table'>
                            {claim_questiontable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id='div_claim_question_answer_fields'></div>
        """
        javascript = """
            <script>
                $("#create_claim_question").click(function(){
                    $('#dialogdiv').load('/product/get_modal_claim_question?', function(data){
                        return false;
                    });
                });
                  $('#action_search').click(function(){
                     var kwargs = 'searchphrase='+$('#searchphrase').val();
                     $('#div_claim_questions_table').load('/product/get_active_claim_questions_htmltable', kwargs, function(data){
                         return false;
                     });
                 })
                 $('#btn_reset').click(function(){
                  $('#searchphrase').val('').focus();
                     $('#div_claim_questions_table').load('/product/get_active_claim_questions_htmltable', 'reset=true', function(data){
                         return false;
                     });
                 })
                 </script>
                 """
        return html + javascript
    @expose()
    def get_active_claim_questions_htmltable(self, *args, **kwargs):
        dbase_query = self.get_active_claim_questions_list(**kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'text' : f"<div class='edit claim_question_edit action_link' claim_question_id='{item.id}'>{item.text}</div>",
                'open' : f"<div class='claim_question_open action_link text-right' claim_question_id='{item.id}'>open</div>",
                             })
        dbcolumnlist=[
                'text',
                'open',
                    ]
        theadlist=[
                'Question Text',
                '',
                ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "claim_question_table")
        javascript = """
            <script>
              $(".claim_question_edit").click(function(){
            var kwargs = 'claim_question_id='+$(this).attr('claim_question_id');
            $('#dialogdiv').load('/product/get_modal_claim_question?', kwargs, function(data){
                return false;
            });
        });
             </script>
             """
        return  html+ javascript
    @expose()
    def get_active_claim_questions_list(self, *args, **kwargs):
        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_CLAIMQUESTION
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()

        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(ClaimQuestion). \
                filter(or_(
                ClaimQuestion.text.like(searchphrase),
            )). \
            filter(ClaimQuestion.active == 1). \
            order_by(asc(ClaimQuestion.text)).limit(LIMIT)

            return  dbase_query
        else:
            dbase_query = DBSession.query(ClaimQuestion). \
                filter(ClaimQuestion.active == 1). \
                order_by(asc(ClaimQuestion.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def get_javascript_claim_question_onload(self, *args, **kwargs):
        javascript = """


        """
        return javascript

    @expose()
    def get_modal_claim_question(self, *args, **kwargs):
        claim_question_id = kwargs.get('claim_question_id', None)
        question = None
        title = 'New Claim Question'
        hidden_input = ''
        if claim_question_id:
            question = ClaimQuestion.by_id(claim_question_id)
            if question: title = 'Edit Claim Question'
            hidden_input = get_hidden_input(**{'id': 'claim_question_id', 'value': claim_question_id})
        text = question.text if question else ''
        checked = 'checked' if question and question.active else ''
        html = f"""
        <div class="modal fade" id="dialog_claim_question" tabindex="-1" role="dialog" aria-labelledby="myclaim_questionLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_claim_question'>
                            {hidden_input}
                            <div class="form-group row">
                                <label class="col-md-3 col-form-label" required for="text">Question Text</label>
                                <div class="col-md-9">
                                    <textarea name='text' type="text" class="form-control" rows="4" maxlength='1024'>{text}</textarea>
                                </div>
                            </div>
                            <div class="form-check col-md-12" style=" padding-bottom: 15px;">
                                <label class="form-check-label">
                                    <input class="form-check-input" name="active" id="active" type="checkbox">
                                    <span class="form-check-sign">Active</span>
                                </label>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_claim_question' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary claim_question_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            var form_id = '#form_claim_question'
            setFormValidation(form_id);
            $('#save_claim_question').click(function(){
                 var valid = FormIsValid(form_id);
                 if(valid){
                    var formserial = $(form_id).serialize();
                    $.post('/product/save_claim_question?', formserial, function(data){
                        $.redirect('/product/claim_questions');
                        return false;
                    });
                 }
            });
            $('.claim_question_back').click(function(){
                $('#dialog_claim_question').modal('hide');
            });
            $('#dialog_claim_question').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_claim_question(self, *args, **kwargs):
        usernow = request.identity['user']
        claim_question_id = kwargs.get('claim_question_id', None)
        if not claim_question_id:
            this = ClaimQuestion()
            this.text = kwargs.get('text', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = ClaimQuestion.by_id(claim_question_id)
            if not this: return 'false'
            this.text = kwargs.get('text', None)
            this.active = True if kwargs.get('active', None) else False
            DBSession.flush()
        return str(this.id)

    @expose()
    def get_claim_question_answers_html(self, *args, **kwargs):
        claim_question_id = kwargs.get('claim_question_id', None)
        if not claim_question_id: return ''
        question =  ClaimQuestion.by_id(claim_question_id)
        if not question: return ''
        kwargs['id'] = 'claim_question_correct_answer_id'
        dbase_query = ClaimQuestionAnswer.by_attr_all('claim_question_id', claim_question_id)
        kwargs['outputlist'] = [{'name' : x.answer_text, 'id' : x.id} for x in dbase_query]
        selectbox = create_selectbox_html(**kwargs)
        return f"""
        <div class="form-group row">
            <label class="col-md-3 col-form-label" required for="claim_question_correct_answer_id">Correct Answer</label>
            <div class="col-md-9">
                {selectbox}
            </div>
        </div>
        """

# ********************* Product Benefit Asset Type Rates - TEMP ********************************************#

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def asset_rates(self, *args, **kwargs):
        html = self.get_active_asset_rate_html(*args, **kwargs)
        javascript = self.get_javascript_asset_rate_onload()
        title = "Short Term Asset Rates"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_asset_rate_html(self, *args, **kwargs):
        dbase_query = RateTable.get_all('code')
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code' : "<div class='edit asset_rate_edit' asset_rate_id='{1}'>{0}</div>".format(item.code, item.id),
                'name' : item.name,
                'product_benefit_asset_temp_type_id' : TYPEUTIL.get_pretty_name('product_benefit_asset_temp_type', item.product_benefit_asset_temp_type_id),
                'open' : f"<div class='asset_rate_open' asset_rate_id='{item.id}'>open</div>",
                             })
        dbcolumnlist=[
                'code',
                'name',
                'product_benefit_asset_temp_type_id',
                'open',
                    ]
        theadlist=[
                'Code',
                'Name',
                'Asset Type',
                '',
                ]
        tdclasslist = [
                'action_link',
                '',
                '',
                'action_link text-right',
        ]
        asset_ratetable = build_html_table(outputlist, dbcolumnlist, theadlist, "asset_rate_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Short Term Asset Rates</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_asset_rate" class="btn btn-primary ml-auto">Create New Asset Rate</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {asset_ratetable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div id='div_asset_rate_items_fields'></div>
        """
        return html

    @expose()
    def get_javascript_asset_rate_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_asset_rate").click(function(){
            $('#dialogdiv').load('/product/get_modal_asset_rate?', function(data){
                return false;
            });
        });
        $(".asset_rate_edit").click(function(){
            var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
            $('#dialogdiv').load('/product/get_modal_asset_rate?'+kwargs, function(data){
                return false;
            });
        });
        $(".asset_rate_open").click(function(){
            var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
            $('#div_asset_rate_items_fields').load('/product/get_asset_rate_line_items?', kwargs, function(data){
                return false;
            });
        });
        $(".asset_rate_open:eq(0)").trigger('click');
        """
        return javascript

    @expose()
    def get_modal_asset_rate(self, *args, **kwargs):
        asset_rate_id = kwargs.get('asset_rate_id', None)
        rate = None
        hidden_input = ''
        title = 'New Asset Rate'
        if asset_rate_id:
            rate = RateTable.by_id(asset_rate_id)
            hidden_input = get_hidden_input(**{'id': 'asset_rate_id', 'value': asset_rate_id})
            title = 'Edit Asset Rate'
        selectbox_benefit_asset_types = self.get_selectbox_product_benefit_asset_temp_types(**{
            'selected' : rate.product_benefit_asset_temp_type_id if rate else None,
        })
        code = rate.code if rate else ''
        name = rate.name if rate else ''
        html = f"""
        <div class="modal fade" id="dialog_new_asset_rate" tabindex="-1" role="dialog" aria-labelledby="myasset_rateLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_asset_rate'>
                            {hidden_input}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_benefit_asset_temp_type_id">Asset Type</label>
                                    <div class="col-md-9">
                                        {selectbox_benefit_asset_types}
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="code">Code</label>
                                    <div class="col-md-9">
                                        <input id="code" type="text" maxlength='10' name="code" class="form-control" value="{code}" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                        <input id="name" type="text" name="name" class="form-control" value="{name}" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_asset_rate' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary asset_rate_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_asset_rate'
        setFormValidation();
        $('#save_asset_rate').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $('#form_asset_rate').serialize();;
                $.post('/product/save_asset_rate?', formserial, function(data){
                    $.redirect('/product/asset_rates');
                    return false;
                });
             }
        });
        $('.asset_rate_back').click(function(){
            $('#dialog_new_asset_rate').modal('hide');
        });
        $('#dialog_new_asset_rate').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_asset_rate(self, *args, **kwargs):
        usernow = request.identity['user']
        asset_rate_id = kwargs.get('asset_rate_id', None)
        if not asset_rate_id:
            this = RateTable()
            this.product_benefit_asset_temp_type_id = kwargs.get('product_benefit_asset_temp_type_id', None)
            this.code = kwargs.get('code', None)
            this.name = kwargs.get('name', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = RateTable.by_id(asset_rate_id)
            this.product_benefit_asset_temp_type_id = kwargs.get('product_benefit_asset_temp_type_id', None)
            this.code = kwargs.get('code', None)
            this.name = kwargs.get('name', None)
            DBSession.flush()
        return str(this.id)

    @expose()
    def get_asset_rate_line_items(self, *args, **kwargs):
        asset_rate_id = kwargs.get('asset_rate_id', None)
        if not asset_rate_id: return ''
        rate = RateTable.by_id(asset_rate_id)
        if not rate: return ''
        vehicle = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'vehicle')
        employee = TYPEUTIL.get_id_of_name('product_benefit_asset_temp_type', 'employee')

        if rate.product_benefit_asset_temp_type_id == vehicle:
            return self.get_asset_vehicle_rate_line_items(rate)

        if rate.product_benefit_asset_temp_type_id == employee:
            return self.get_asset_employee_rate_line_items(rate)

        return self.get_asset_turnover_rate_line_items(rate)

    @expose()
    def get_asset_vehicle_rate_line_items(self, rate=None, *args, **kwargs):
        if not rate: return ''
        dbase_query = ProductBenefitAssetPremiumRateVehicleLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', rate.id)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'description' : f"<div class='edit asset_vehicle_line_item_edit' asset_rate_id='{rate.id}' asset_line_item_id='{item.id}'>{item.description}</div>",
                'insured_amount' : getcurrency(item.insured_amount),
                'uninsured_amount' : getcurrency(item.uninsured_amount),
                'third_party_amount' : getcurrency(item.third_party_amount),
                             })
        dbcolumnlist=[
                'description',
                'insured_amount',
                'uninsured_amount',
                'third_party_amount',
                    ]
        theadlist=[
                'Description',
                'Insured Amount',
                'Uninsured Amount',
                'Third Party Amount',
                ]
        tdclasslist = [
                'action_link',
                'text-right',
                'text-right',
                'text-right',
        ]
        asset_line_itemtable = build_html_table(outputlist, dbcolumnlist, theadlist, "asset_line_item_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Line Items for: {rate.code}</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_asset_line_item" asset_rate_id="{rate.id}" class="btn btn-primary ml-auto">Create New Asset Rate Line Item</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {asset_line_itemtable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_asset_line_item").click(function(){
                var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
                $('#dialogdiv').load('/product/get_modal_asset_vehicle_line_item?', kwargs, function(data){
                    return false;
                });
            });
            $(".asset_vehicle_line_item_edit").click(function(){
                var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
                kwargs += '&asset_line_item_id='+$(this).attr('asset_line_item_id');
                $('#dialogdiv').load('/product/get_modal_asset_vehicle_line_item?'+kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_asset_vehicle_line_item(self, *args, **kwargs):
        asset_rate_id = kwargs.get('asset_rate_id', None)
        asset_line_item_id = kwargs.get('asset_line_item_id', None)
        if not asset_rate_id: return ''
        item = None
        title = 'New Asset Rate Line Item'
        hidden_input_line_item_id = ''
        if asset_line_item_id:
            item = ProductBenefitAssetPremiumRateVehicleLineItemTemp.by_id(asset_line_item_id)
            title = 'Edit Asset Rate Line Item'
            hidden_input_line_item_id = get_hidden_input(**{'id': 'asset_line_item_id', 'value': asset_line_item_id})
        hidden_input = get_hidden_input(**{'id': 'product_benefit_asset_premium_rate_temp_id', 'value': asset_rate_id})
        description = item.description if item else ''
        insured = getcurrency(item.insured_amount) if item else ''
        uninsured = getcurrency(item.uninsured_amount) if item else ''
        third_party = getcurrency(item.third_party_amount) if item else ''
        html = f"""
        <div class="modal fade" id="dialog_asset_line_item" tabindex="-1" role="dialog" aria-labelledby="myasset_line_itemLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_asset_line_item'>
                            {hidden_input}
                            {hidden_input_line_item_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="description">Description</label>
                                    <div class="col-md-9">
                                        <input id="description" value="{description}" type="text" name="description" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="insured_amount">Insured Amount</label>
                                    <div class="col-md-9">
                                        <input id="insured_amount" value="{insured}" type="number" name="insured_amount" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="uninsured_amount">Uninsured Amount</label>
                                    <div class="col-md-9">
                                        <input id="uninsured_amount" value="{uninsured}" type="number" name="uninsured_amount" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="third_party_amount">Third Party Amount</label>
                                    <div class="col-md-9">
                                        <input id="third_party_amount" value="{third_party}" type="number" name="third_party_amount" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_asset_vehicle_line_item' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary asset_line_item_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_asset_line_item';
        setFormValidation(form_id);
        $('#save_asset_vehicle_line_item').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $('#dialog_asset_line_item').modal('hide');
                $.post('/product/save_asset_vehicle_line_item?', formserial, function(data){
                    var asset_rate_id = $('#product_benefit_asset_premium_rate_temp_id').val();
                    $('.asset_rate_open[asset_rate_id='+asset_rate_id+']').trigger('click');
                    return false;
                });
             }
        });
        $('.asset_line_item_back').click(function(){
            $('#dialog_asset_line_item').modal('hide');
        });
        $('#dialog_asset_line_item').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_asset_vehicle_line_item(self, *args, **kwargs):
        usernow = request.identity['user']
        asset_line_item_id = kwargs.get('asset_line_item_id', None)
        if not asset_line_item_id:
            this = ProductBenefitAssetPremiumRateVehicleLineItemTemp()
            this.product_benefit_asset_premium_rate_temp_id = kwargs.get('product_benefit_asset_premium_rate_temp_id', None)
            this.description = kwargs.get('description', None)
            this.insured_amount = kwargs.get('insured_amount', None)
            this.uninsured_amount = kwargs.get('uninsured_amount', None)
            this.third_party_amount = kwargs.get('third_party_amount', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = ProductBenefitAssetPremiumRateVehicleLineItemTemp.by_id(asset_line_item_id)
            this.description = kwargs.get('description', None)
            this.insured_amount = kwargs.get('insured_amount', None)
            this.uninsured_amount = kwargs.get('uninsured_amount', None)
            this.third_party_amount = kwargs.get('third_party_amount', None)
            DBSession.flush()
        return 'true'

    @expose()
    def get_asset_employee_rate_line_items(self, rate=None, *args, **kwargs):
        if not rate: return ''
        dbase_query = ProductBenefitAssetPremiumRateEmployeeLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', rate.id)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'minimum_employees_coverable' : f"<div class='edit asset_employee_line_item_edit' asset_rate_id='{rate.id}' asset_line_item_id='{item.id}'>{item.minimum_employees_coverable}</div>",
                'maximum_employees_coverable' : item.maximum_employees_coverable,
                'amount' : getcurrency(item.amount),
                             })
        dbcolumnlist=[
                'minimum_employees_coverable',
                'maximum_employees_coverable',
                'amount',
                    ]
        theadlist=[
                'Min Employees',
                'Max Employees',
                'Amount',
                ]
        tdclasslist = [
                'action_link',
                '',
                'text-right',
        ]
        asset_line_itemtable = build_html_table(outputlist, dbcolumnlist, theadlist, "asset_line_item_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Line Items for: {rate.code}</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_asset_line_item" asset_rate_id="{rate.id}" class="btn btn-primary ml-auto">Create New Asset Rate Line Item</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {asset_line_itemtable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_asset_line_item").click(function(){
                var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
                $('#dialogdiv').load('/product/get_modal_asset_employee_line_item?', kwargs, function(data){
                    return false;
                });
            });
            $(".asset_employee_line_item_edit").click(function(){
                var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
                kwargs += '&asset_line_item_id='+$(this).attr('asset_line_item_id');
                $('#dialogdiv').load('/product/get_modal_asset_employee_line_item?'+kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_asset_employee_line_item(self, *args, **kwargs):
        asset_rate_id = kwargs.get('asset_rate_id', None)
        asset_line_item_id = kwargs.get('asset_line_item_id', None)
        if not asset_rate_id: return ''
        item = None
        title = 'New Asset Rate Line Item'
        hidden_input_line_item_id = ''
        if asset_line_item_id:
            item = ProductBenefitAssetPremiumRateEmployeeLineItemTemp.by_id(asset_line_item_id)
            title = 'Edit Asset Rate Line Item'
            hidden_input_line_item_id = get_hidden_input(**{'id': 'asset_line_item_id', 'value': asset_line_item_id})
        hidden_input = get_hidden_input(**{'id': 'product_benefit_asset_premium_rate_temp_id', 'value': asset_rate_id})
        insured = getcurrency(item.minimum_employees_coverable) if item else ''
        uninsured = getcurrency(item.maximum_employees_coverable) if item else ''
        third_party = getcurrency(item.amount) if item else ''
        html = f"""
        <div class="modal fade" id="dialog_asset_line_item" tabindex="-1" role="dialog" aria-labelledby="myasset_line_itemLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_asset_line_item'>
                            {hidden_input}
                            {hidden_input_line_item_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="minimum_employees_coverable">Min Employees</label>
                                    <div class="col-md-9">
                                        <input id="minimum_employees_coverable" value="{insured}" type="number" name="minimum_employees_coverable" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="maximum_employees_coverable">Max Employees</label>
                                    <div class="col-md-9">
                                        <input id="maximum_employees_coverable" value="{uninsured}" type="number" name="maximum_employees_coverable" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="amount">Amount</label>
                                    <div class="col-md-9">
                                        <input id="amount" value="{third_party}" type="number" name="amount" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_asset_employee_line_item' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary asset_line_item_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_asset_line_item';
        setFormValidation(form_id);
        $('#save_asset_employee_line_item').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $('#dialog_asset_line_item').modal('hide');
                $.post('/product/save_asset_employee_line_item?', formserial, function(data){
                    var asset_rate_id = $('#product_benefit_asset_premium_rate_temp_id').val();
                    $('.asset_rate_open[asset_rate_id='+asset_rate_id+']').trigger('click');
                    return false;
                });
             }
        });
        $('.asset_line_item_back').click(function(){
            $('#dialog_asset_line_item').modal('hide');
        });
        $('#dialog_asset_line_item').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_asset_employee_line_item(self, *args, **kwargs):
        usernow = request.identity['user']
        asset_line_item_id = kwargs.get('asset_line_item_id', None)
        if not asset_line_item_id:
            this = ProductBenefitAssetPremiumRateEmployeeLineItemTemp()
            this.product_benefit_asset_premium_rate_temp_id = kwargs.get('product_benefit_asset_premium_rate_temp_id', None)
            this.description = kwargs.get('description', None)
            this.minimum_employees_coverable = kwargs.get('minimum_employees_coverable', None)
            this.maximum_employees_coverable = kwargs.get('maximum_employees_coverable', None)
            this.amount = kwargs.get('amount', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = ProductBenefitAssetPremiumRateEmployeeLineItemTemp.by_id(asset_line_item_id)
            this.description = kwargs.get('description', None)
            this.minimum_employees_coverable = kwargs.get('minimum_employees_coverable', None)
            this.maximum_employees_coverable = kwargs.get('maximum_employees_coverable', None)
            this.amount = kwargs.get('amount', None)
            DBSession.flush()
        return 'true'

    @expose()
    def get_asset_turnover_rate_line_items(self, rate=None, *args, **kwargs):
        if not rate: return ''
        dbase_query = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_attr_all('product_benefit_asset_premium_rate_temp_id', rate.id)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'minimum_turnover' : f"<div class='edit asset_turnover_line_item_edit' asset_rate_id='{rate.id}' asset_line_item_id='{item.id}'>{item.minimum_turnover}</div>",
                'maximum_turnover' : item.maximum_turnover,
                'amount' : getcurrency(item.amount),
                             })
        dbcolumnlist=[
                'minimum_turnover',
                'maximum_turnover',
                'amount',
                    ]
        theadlist=[
                'Min Turnover',
                'Max Turnover',
                'Amount',
                ]
        tdclasslist = [
                'action_link',
                '',
                'text-right',
        ]
        asset_line_itemtable = build_html_table(outputlist, dbcolumnlist, theadlist, "asset_line_item_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Line Items for: {rate.code}</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_asset_line_item" asset_rate_id="{rate.id}" class="btn btn-primary ml-auto">Create New Asset Rate Line Item</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {asset_line_itemtable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#create_asset_line_item").click(function(){
                var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
                $('#dialogdiv').load('/product/get_modal_asset_turnover_line_item?', kwargs, function(data){
                    return false;
                });
            });
            $(".asset_turnover_line_item_edit").click(function(){
                var kwargs = 'asset_rate_id='+$(this).attr('asset_rate_id');
                kwargs += '&asset_line_item_id='+$(this).attr('asset_line_item_id');
                $('#dialogdiv').load('/product/get_modal_asset_turnover_line_item?'+kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_asset_turnover_line_item(self, *args, **kwargs):
        asset_rate_id = kwargs.get('asset_rate_id', None)
        asset_line_item_id = kwargs.get('asset_line_item_id', None)
        if not asset_rate_id: return ''
        item = None
        title = 'New Asset Rate Line Item'
        hidden_input_line_item_id = ''
        if asset_line_item_id:
            item = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_id(asset_line_item_id)
            title = 'Edit Asset Rate Line Item'
            hidden_input_line_item_id = get_hidden_input(**{'id': 'asset_line_item_id', 'value': asset_line_item_id})
        hidden_input = get_hidden_input(**{'id': 'product_benefit_asset_premium_rate_temp_id', 'value': asset_rate_id})
        insured = getcurrency(item.minimum_turnover) if item else ''
        uninsured = getcurrency(item.maximum_turnover) if item else ''
        third_party = getcurrency(item.amount) if item else ''
        html = f"""
        <div class="modal fade" id="dialog_asset_line_item" tabindex="-1" role="dialog" aria-labelledby="myasset_line_itemLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">{title}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_asset_line_item'>
                            {hidden_input}
                            {hidden_input_line_item_id}
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="minimum_turnover">Min Turnover</label>
                                    <div class="col-md-9">
                                        <input id="minimum_turnover" value="{insured}" type="number" name="minimum_turnover" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="maximum_turnover">Max Turnover</label>
                                    <div class="col-md-9">
                                        <input id="maximum_turnover" value="{uninsured}" type="number" name="maximum_turnover" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="amount">Amount</label>
                                    <div class="col-md-9">
                                        <input id="amount" value="{third_party}" type="number" name="amount" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_asset_turnover_line_item' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary asset_line_item_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        var form_id = '#form_asset_line_item';
        setFormValidation(form_id);
        $('#save_asset_turnover_line_item').click(function(){
             var valid = FormIsValid(form_id);
             if(valid){
                var formserial = $(form_id).serialize();
                $('#dialog_asset_line_item').modal('hide');
                $.post('/product/save_asset_turnover_line_item?', formserial, function(data){
                    var asset_rate_id = $('#product_benefit_asset_premium_rate_temp_id').val();
                    $('.asset_rate_open[asset_rate_id='+asset_rate_id+']').trigger('click');
                    return false;
                });
             }
        });
        $('.asset_line_item_back').click(function(){
            $('#dialog_asset_line_item').modal('hide');
        });
        $('#dialog_asset_line_item').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_asset_turnover_line_item(self, *args, **kwargs):
        usernow = request.identity['user']
        asset_line_item_id = kwargs.get('asset_line_item_id', None)
        if not asset_line_item_id:
            this = ProductBenefitAssetPremiumRateTurnoverLineItemTemp()
            this.product_benefit_asset_premium_rate_temp_id = kwargs.get('product_benefit_asset_premium_rate_temp_id', None)
            this.description = kwargs.get('description', None)
            this.minimum_turnover = kwargs.get('minimum_turnover', None)
            this.maximum_turnover = kwargs.get('maximum_turnover', None)
            this.amount = kwargs.get('amount', None)
            this.added_by = usernow.id
            DBSession.add(this)
            DBSession.flush()
        else:
            this = ProductBenefitAssetPremiumRateTurnoverLineItemTemp.by_id(asset_line_item_id)
            this.description = kwargs.get('description', None)
            this.minimum_turnover = kwargs.get('minimum_turnover', None)
            this.maximum_turnover = kwargs.get('maximum_turnover', None)
            this.amount = kwargs.get('amount', None)
            DBSession.flush()
        return 'true'
