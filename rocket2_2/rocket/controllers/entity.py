# -*- coding: utf-8 -*-
"""Entity Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.exceptions import HTTPFound
from tg import predicates
from rocket import model
from rocket.controllers.secure import SecureController
from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_
from rocket.model import *
from rocket.model import DBSession

from rocket.lib.base import BaseController
from rocket.controllers.error import ErrorController

from rocket.lib.tg_utils import *
from rocket.lib.sidebar import Sidebar
from rocket.lib.type_utils import TypeDictionary as TypeDict
from sqlalchemy import func, desc, asc, or_
import rocket.lib.vault_utils as vault
from rocket.controllers.common import CommonController


COMMON = CommonController()
SEARCHKEY_ENTITY = 'Entity_SearchKeyWord'
LIMIT = 20
TYPEUTIL = TypeDict()

__all__ = ['EntityController']


class EntityController(BaseController):
    """Docstring for entity."""

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_active_entity_html(*args, **kwargs)
        javascript = self.get_javascript_entity_onload()
        title = "Organisations"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_entity_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_ENTITY
        searchphrase = COMMON.get_searchphrase(**kwargs)
        entitytable=self.get_entity_htmltable(kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Organisations')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_entity" class="btn btn-primary ml-auto">New Organisation</button>
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
                    <div class="table-responsive" id= 'div_entity'>
                        {entitytable}
                    </div>
                </div>
                </div>
            </div>
        """
        javascript="""
        <script>
          $("#create_new_entity").click(function(){
                $('#dialogdiv').load('/entity/get_modal_new_entity?', function(data){
                    return false;
                });
            });
              $('#action_search').click(function(){
                 var kwargs = 'searchphrase='+$('#searchphrase').val();
                 $('#div_entity').load('/entity/get_entity_htmltable', kwargs, function(data){
                     return false;
                 });
             }) 
             $('#btn_reset').click(function(){
              $('#searchphrase').val('').focus();
                 $('#div_entity').load('/entity/get_entity_htmltable', 'reset=true', function(data){
                     return false;
                 });
             })
        </script>
        """
        return html +javascript
    @expose()
    def get_entity_htmltable(self, *args, **kwargs):
        dbase_query = self.get_active_entity_organisation_list(**kwargs)
        outputlist = []
        for item in dbase_query:
            entity_type = TYPEUTIL.get_pretty_name("entity_organisation_type", item.entity_organisation_type_id)
            outputlist.append({
                'code': f"<div class='edit entity_edit' entity_id='{item.entity_id}'>{item.code}</div>",
                'entity_type': entity_type,
                'name': item.name,
                'registration_number': item.registration_number,
                'tax_number': item.tax_number,
            })
        theadlist = [
            'Code',
            'Name',
            'Type',
            'Tax Number',
            'Registration Number'
        ]
        dbcolumnlist = [
            'code',
            'name',
            'entity_type',
            'tax_number',
            'registration_number',
        ]
        tdclasslist = [
            'action_link',
            'text-right',
            'text-center',
            'text-center',
            'text-right',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "entity_table", tdclasslist)
        javascript = """
           <script>
        
        $(".entity_edit").click(function(){
            var data = {entity_id : $(this).attr('entity_id')};
          $.redirect('/entity/edit_organisation', data);
        });
            </script>
            """
        return  html + javascript

    @expose()
    def get_javascript_entity_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript

    @expose()
    def get_active_entity_organisation_list(self, *args, **kwargs):
        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_ENTITY
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()
        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(EntityOrganisation). \
                filter(or_(
                EntityOrganisation.code.like(searchphrase),
                EntityOrganisation.name.like(searchphrase),
                EntityOrganisation.tax_number.like(searchphrase),
                EntityOrganisation.registration_number.like(searchphrase),
                EntityOrganisation.financial_regulatory_number.like(searchphrase),
            )). \
                filter(EntityOrganisation.active == 1). \
                order_by(asc(EntityOrganisation.name)).limit(LIMIT)

            return  dbase_query

        else:
            dbase_query = DBSession.query(EntityOrganisation). \
                filter(EntityOrganisation.active == 1). \
                order_by(asc(EntityOrganisation.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def get_modal_new_entity(self, *args, **kwargs):

        dropdown_entity_organisation = self.get_selectbox_entity_organisation()
        dropdown_billing_frequency = self.get_selectbox_billing_frequency()
        entity_type = TYPEUTIL.get_id_of_name('entity_type', 'organisation')
        html = f"""
        <div class="modal fade" id="dialog_new_entity" tabindex="-1" role="dialog" aria-labelledby="myentityLabel" aria-hidden="true">
			<div class="modal-dialog  modal-xl ">
				<div class="modal-content">
					<div class="modal-header">
						<div class="col-md-6">
							<h4 class="card-title">Organisation Record</h4>
						</div>
					</div>
					<div class="modal-body">
						<form id='form_new_entity'>
							<div class='row'>
								<div style='display: none' class="col-md-6">
									<div class="form-group row">
										<label class="col-md-3 col-form-label" required for="">Entity Type Default to Organisation</label>
										<div class="col-md-9">
											<input id="entity_type_id" type="text" name="entity_type_id" value="{entity_type}" class="form-control"
											required='true'>
										</div>
									</div>
								</div>
								<div class ="col-md-6">
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" required
											for="code">Code</label>
											<div class="col-md-8">
												<input id="code" type="text" name="code" class="form-control"
												required='true'>
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" required for="code">Tax Number</label>
											<div class="col-md-8">
												<input id="tax_number" type="text" name="tax_number" class="form-control" required='true'>
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" for="financial_regulatory_number">Financial Reg</label>
											<div class="col-md-8">
												<input id="financial_regulatory_number" type="text" name="financial_regulatory_number" class="form-control">
											</div>
										</div>
									</div>

								</div>
								<div class='col-md-6'>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" required
											for="name">Name</label>
											<div class="col-md-8">
												<input id="name" type="text" name="name" class="form-control"
												required='true'>
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" required for="registration_number">Reg Number</label>
											<div class="col-md-8">
												<input id="registration_number" type="text" name="registration_number" class="form-control" required='true'>
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" for="">Organisation Type</label>
											<div class="col-md-8">
												{dropdown_entity_organisation}
											</div>
										</div>
									</div>
								</div>
							</div>
							<hr>
							<div class="row">
								<div class="form-check col-md-12" style=" padding-bottom: 15px;">
									<label class="form-check-label">
										<input class="form-check-input user_role" name="is_insurer" id="is_insurer" type="checkbox">
										<span class="form-check-sign">Is Insurer</span>
									</label>
								</div>
								<div class="form-check col-md-12" style=" padding-bottom: 15px;">
									<label class="form-check-label">
										<input class="form-check-input user_role" name="is_product_owner" id="is_product_owner" type="checkbox">
										<span class="form-check-sign">Is Product Owner</span>
									</label>
									<div class="row" >
										<div class="col-md-4"></div>
										<div class="col-md-8">
											<div id="product_owner_fields" style="display: none;">
												<div class="form-group row">
													<label class="col-md-4 col-form-label" for="">Policy Number Prefix</label>
													<div class="col-md-8">
														<input id="policy_number_prefix" type="text" name="policy_number_prefix" class="form-control">
													</div>
												</div>

											</div>
										</div>
									</div>
								</div >
								<div class="form-check col-md-12" style=" padding-bottom: 15px;">
									<label class="form-check-label">
										<input class="form-check-input user_role" name="is_client" id="is_client" type="checkbox">
										<span class="form-check-sign">Is Client</span>
									</label>
									<div class="row">
										<div class="col-md-4"></div>
										<div class="col-md-8">
											<div id="is_client_fields" style="display: none;">
												<div class="form-group row">
													<label class="col-md-4 col-form-label" for="">Billing Frequency</label>
													<div class="col-md-8">
														{dropdown_billing_frequency}
													</div>
												</div>

											</div>
										</div>
									</div>
								</div>
							</div>
						</form>
					</div>
					<div class="modal-footer">
						<button id='save_new_entity' class="btn btn-primary">Save</button>
						<button class="btn btn-outline-primary entity_back">Cancel</button>
					</div>
				</div>
			</div>
		</div>
         """
        javascript = """
        <script>
        setFormValidation('#form_new_entity');

        createClickHideShow('#is_client', '#is_client_fields')
        createClickHideShow('#is_product_owner', '#product_owner_fields')

        $('#save_new_entity').click(function(){
             var valid = FormIsValid("#form_new_entity");
             if(valid){

                var formserial = $('#form_new_entity').serialize();
                console.log(formserial);

                $.post('/entity/save_new_entityobj?', formserial, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                         $.redirect(result.redirect, {'entity_id' : result.entity_id});
                    };
                    return false;
                });
             }
        });
        $('.entity_back').click(function(){
            $('#dialog_new_entity').modal('hide');
        });
        $('#dialog_new_entity').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_entityobj(self, *args, **kwargs):
        dict_entity = {
            'entity_type_id': kwargs.get('entity_type_id'),
        }
        entity_id = self.save_new_entity(**dict_entity)

        dict_entity_organisation = {
            'entity_id': entity_id,
            'entity_organisation_type_id': kwargs.get('entity_organisation_type_id'),
            'code': kwargs.get('code'),
            'name': kwargs.get('name'),
            'tax_number': kwargs.get('tax_number'),
            'registration_number': kwargs.get('registration_number'),
            'financial_regulatory_number': kwargs.get('financial_regulatory_number'),
        }
        entity_organisation_id = self.save_new_entity_organisation(**dict_entity_organisation)

        is_product_owner = kwargs.get('is_product_owner', False)
        if is_product_owner:
            dict_product_owner = {
                'entity_organisation_id': entity_organisation_id,
                'policy_number_prefix': kwargs.get('policy_number_prefix'),
            }
            self.save_new_product_owner(**dict_product_owner)

        is_insurer = kwargs.get('is_insurer', False)
        if is_insurer:
            dict_insurer = {
                'entity_organisation_id': entity_organisation_id,
            }
            self.save_new_insurer(**dict_insurer)

        is_client = kwargs.get('is_client', False)
        if is_client:
            dict_entity_client = {
                'entity_organisation_id': entity_organisation_id,
                'billing_frequency_id': kwargs.get('billing_frequency_type_id'),
            }
            self.save_new_entity_client(**dict_entity_client)

        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': entity_id, 'redirect': redirect_url})

    @expose()
    def save_new_insurer(self, *args, **kwargs):
        usernow = request.identity['user']
        this = EntityOrganisationInsurer()
        this.entity_organisation_id = kwargs.get('entity_organisation_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_product_owner(self, *args, **kwargs):
        usernow = request.identity['user']
        this = EntityOrganisationProductOwner()
        this.entity_organisation_id = kwargs.get('entity_organisation_id', None)
        this.policy_number_prefix = kwargs.get('policy_number_prefix', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_entity_client(self, *args, **kwargs):
        usernow = request.identity['user']
        this = EntityOrganisationClient()
        this.entity_organisation_id = kwargs.get('entity_organisation_id', None)
        this.billing_frequency_id = kwargs.get('billing_frequency_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_entity(self, *args, **kwargs):
        usernow = request.identity['user']
        this = Entity()
        this.entity_type_id = kwargs.get('entity_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_entity_organisation(self, *args, **kwargs):
        usernow = request.identity['user']

        this = EntityOrganisation()
        this.entity_id = kwargs.get('entity_id', None)
        this.entity_organisation_type_id = kwargs.get('entity_organisation_type_id', None)
        this.code = kwargs.get('code', None)
        this.name = kwargs.get('name', None)
        this.tax_number = kwargs.get('tax_number', None)
        this.registration_number = kwargs.get('registration_number', None)
        this.financial_regulatory_number = kwargs.get('financial_regulatory_number', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    def get_selectbox_mail_option(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'mail_option_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("mail_option_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_currency(self, *args, **kwargs):
        currecy_list = Currency.get_all('name')
        kwargs['id'] = 'currency_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in currecy_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_entity_organisation(self, selected= None, *args, **kwargs):
        kwargs['id'] = 'entity_organisation_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("entity_organisation_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_bank(self, *args, **kwargs):
        bank_list = Bank.get_all('name')
        kwargs['id'] = 'bank_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in bank_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_contact(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'entity_organisation_contact_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("contact_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_message_batch(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'message_batch_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("message_batch_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_billing_frequency(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'billing_frequency_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("billing_frequency_type")
        return create_selectbox_html(**kwargs)

    # ****************************************************Entity View
    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit_organisation(self, *args, **kwargs):
        entity_id = kwargs.get('entity_id', None)
        if not entity_id: redirect('/entity/index')
        entity = Entity.by_id(entity_id)
        if not entity: redirect('/entity/index')
        entity_organisation = EntityOrganisation.by_attr_first('entity_id', entity_id)
        if not entity_organisation: redirect('/entity/index')
        kwargs['entity_organisation'] = entity_organisation
        kwargs['entity'] = entity

        html = self.get_edit_organisation_html(**kwargs)
        javascript = self.get_javascript_edit_organisation_onload()
        title = self.get_organisation_title_html(**kwargs)
        return dict(title=title, html=html, javascript=javascript)

    def get_edit_organisation_html(self, *args, **kwargs):
        entity_organisation = kwargs.get('entity_organisation')

        if not entity_organisation: return ''

        card_header = self.get_edit_organisation_card_title_html(**kwargs)
        card_organisation_details = self.get_edit_organisation_details_html(**kwargs)
        card_organisation_address = self.get_edit_organisation_address_html(**kwargs)
        card_organisation_contact = self.get_edit_organisation_contact_html(**kwargs)
        card_organisation_bank = self.get_edit_organisation_bank_html(**kwargs)
        entity_product_insurer_card = self.get_entity_product_insurer_card(**kwargs)
        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    {card_organisation_details}
                    {card_organisation_address}
                    {card_organisation_contact}
                    {card_organisation_bank}
                    {entity_product_insurer_card}
                </div>

            </div>
        </div>
        """
        return html
    @expose()
    def get_product_owner_and_insurer_html(self, *args, **kwargs):
        entity_organisation = kwargs.get('entity_organisation')

        product_owner = EntityOrganisationProductOwner.by_attr_first("entity_organisation_id", entity_organisation.id)
        insurer = EntityOrganisationInsurer.by_attr_first("entity_organisation_id", entity_organisation.id)

        product_fields = ''
        insurer_fields = ''
        if product_owner:

            product_fields = f"""
            <input type="hidden" id="product_owner_id" name="product_owner_id" class="form-control" value="{product_owner.id}"/>
            <div class="form-group row">
                <label class="col-md-4 col-form-label" for="">Policy Number Prefix</label>
                <div class="col-md-8">
                    <input id="policy_number_prefix" type="text" name="policy_number_prefix" class="form-control" value="{product_owner.policy_number_prefix}">
                </div></div>

            """
        if insurer:
            checked = 'checked'
            insurer_fields = f"""
            <input  type="hidden" id="insurer_id" name="insurer_id" class="form-control" value="{insurer.id}"/>
            <div class="form-group row">
                <label class="col-md-4 col-form-label" for="active" >Is Insurer</label>
                <div class="col-md-8">
                    <div class="form-check">
                        <label class="form-check-label">
                            <input class="form-check-input" type="checkbox" name="is_insurer" id="is_insurer" {checked}/>
                            <span class="form-check-sign"></span>
                        </label>
                    </div>
                </div>
            </div>
            """
        html = f"""
        <div class="card">
            <div class="card-header">
                <div class="row d-flex">
                    <div class="col-md-6">
                        <h4 class="card-title">Product Owner Details  </h4>
                    </div>
	                    <div class="col-md-6  text-right">
							<button id='save_product_owner' class="btn btn-primary">Save</button>
						</div>
                </div>
                <div class="row d-flex">
                    <div class="col-md-12">
                        <hr>
                        <div class="col-md-12">
                            <form id = "form_product_owner" >
  	                            <input type="hidden" id="entity_id" name="entity_id" class="form-control" value="{entity_organisation.entity_id}"/>
  	                             <input type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>
                                {product_fields}
                                {insurer_fields}
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        </div>
        """
        return html

    @expose()
    def get_entity_client_html(self, *args, **kwargs):
        entity_organisation_client= kwargs.get('entity_organisation_client')
        entity_organisation = kwargs.get('entity_organisation', None)
        dropdown_billing_frequency = self.get_selectbox_billing_frequency(entity_organisation_client.billing_frequency_id)
        html = f"""
        <div class="card">
            <div class="card-header">
                <div class="row d-flex">
                    <div class="col-md-6">
                        <h4 class="card-title">Entity Client Details </h4>
                    </div>
                    <div class="col-md-6  text-right">
							<button id='save_entity_client' class="btn btn-primary">Save</button>
						</div>
                </div>
                <div class="row d-flex">
                    <div class="col-md-12">
                        <hr>
                        <div class="col-md-12">
                            <form id ="form_entity_client" class="">
                                <input type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>
                              	<input type="hidden" id="entity_id" name="entity_id" class="form-control" value="{entity_organisation.entity_id}"/>
                                <div class="form-group row">
                                    <label class="col-md-4 col-form-label" for="">Billing Frequency</label>
                                    <div class="col-md-8">
                                        {dropdown_billing_frequency}
                                    </div>
                                </div>
                            </form>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_entity_product_insurer_card(self, *args, **kwargs):

        entity_organisation = kwargs.get('entity_organisation', None)
        kwargs['entity_organisation'] = entity_organisation
        entity_client_card = ''
        product_owner_and_insure_card = ''
        is_client = EntityOrganisationClient.by_attr_first('entity_organisation_id', entity_organisation.id)
        if is_client:
            kwargs['entity_organisation_client'] = is_client
            entity_client_card = self.get_entity_client_html(**kwargs)

        is_product_owner = EntityOrganisationProductOwner.by_attr_first('entity_organisation_id', entity_organisation.id)
        is_insurer = EntityOrganisationInsurer.by_attr_first('entity_organisation_id', entity_organisation.id)
        if is_product_owner or is_insurer:
            product_owner_and_insure_card = self.get_product_owner_and_insurer_html(**kwargs)

        html = f"""
        <div class="row">
            <div class="col-md-6">{entity_client_card}</div>
            <div class="col-md-6">{product_owner_and_insure_card}</div>
        </div>
        """
        return html

    @expose()
    def get_edit_organisation_address_html(self, *args, **kwargs):
        dropdown_country = self.get_selectbox_country(**{'selected': 207})

        entity_organisation = kwargs.get('entity_organisation')
        entity = kwargs.get('entity')
        entity_organisation_address = EntityOrganisationAddress.by_attr_first("entity_organisation_id", entity_organisation.id)
        org_address_vault = {}
        if entity_organisation_address:
            org_address_vault = vault.get_address_by_id(entity_organisation_address.address_id)
        dropdown_region = self.get_selectbox_region(**{'selected': org_address_vault.get("region_id", '')})
        html = f"""
        <div class="row">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Postal Address')}</h4>
                            </div>
                            <div class="col-md-6 text-right">
							<button id='save_postal_address' class="btn btn-primary">Save</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <form id="form_postal_address">
                            <div class="row">
                                <input type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>
                                <input type="hidden" id="entity_id" name="entity_id" class="form-control" value="{entity_organisation.entity_id}"/>
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">Address Line</label>
                                        <div class="col-md-9">
                                            <input type="text" id= "address_line" class="form-control" maxlength='255' name="address_line" value='{org_address_vault.get("address_line", '')}'>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('City')}</label>
                                        <div class="col-md-9">
                                            <input type="text" class="form-control" maxlength='255' name="city"  id="city" value='{org_address_vault.get("city", '')}'>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Postal Code')}</label>
                                        <div class="col-md-9">
                                            <input type="text" class="form-control" maxlength='255' id="postal_code" name="postal_code" value='{org_address_vault.get("postal_code", '')}'>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Country')}</label>
                                        <div class="col-md-9">
                                            {dropdown_country}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Region')}</label>
                                        <div class="col-md-9">
                                            {dropdown_region}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div id="div_district"></div>
                            <div id="div_centre"></div>
                        </form>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Street Address')}</h4>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <form id="form_street_address">
                            <div class="row">
                                <input type="hidden" id="organisation_id" name="organisation_id" class="form-control" value="{entity_organisation.id}"/>
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">Address Line</label>
                                        <div class="col-md-9">
                                            <input type="text" id= "address_line" class="form-control" maxlength='255' name="address_line" value='{org_address_vault.get("address_line", '')}'>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('City')}</label>
                                        <div class="col-md-9">
                                            <input type="text" class="form-control" maxlength='255' name="city"  id="city" value='{org_address_vault.get("city", '')}'>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Postal Code')}</label>
                                        <div class="col-md-9">
                                            <input type="text" class="form-control" maxlength='255' id="postal_code" name="postal_code" value='{org_address_vault.get("postal_code", '')}'>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Country')}</label>
                                        <div class="col-md-9">
                                            {dropdown_country}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">{_('Region')}</label>
                                        <div class="col-md-9">
                                            {dropdown_region}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div id="div_district"></div>
                            <div id="div_centre"></div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    def get_selectbox_country(self, *args, **kwargs):
        country_list = Country.get_all('name')
        kwargs['id'] = 'country_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in country_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_region(self, *args, **kwargs):
        country_id = kwargs.get("country_id")
        region_list = Region.by_attr_all('country_id', 207)
        kwargs['id'] = 'region_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in region_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_district(self, *args, **kwargs):
        district_id = kwargs.get("district_id", None)  # To preselect if it exists
        region_id = kwargs.get("region_id")
        district_list = District.by_attr_all('region_id', region_id)
        kwargs['id'] = 'district_id'
        kwargs['selected'] = district_id if district_id else None  # To pre select if it exists
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in district_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_center(self, *args, **kwargs):
        district_id = kwargs.get("district_id")
        center_list = Centre.by_attr_all('district_id', district_id)
        kwargs['id'] = 'centre_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in center_list]
        return create_selectbox_html(**kwargs)

    @expose()
    def get_edit_organisation_bank_html(self, *args, **kwargs):
        entity_organisation = kwargs.get('entity_organisation')
        entity = kwargs.get('entity')

        entity_organisation_bank = EntityOrganisationBankAccountLink.by_attr_first("entity_organisation_id", entity_organisation.id)
        bank_vault = {}
        bank_id = None
        currency_id= None
        if entity_organisation_bank:
            bank_vault = vault.get_bankaccount_by_id(entity_organisation_bank.bank_account_id)
            if bank_vault:
                bank_id = bank_vault.get('id', None)
                currency_id = bank_vault.get('currency_id', None)
        dropdown_bank = self.get_selectbox_bank(**{'selected': bank_id})
        dropdown_currency = self.get_selectbox_currency(**{'selected': currency_id})
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('Bank Details')}</h4>
                            </div>
	                    <div class="col-md-6  text-right">
							<button id='save_bank' class="btn btn-primary">Save</button>
						</div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <form id="form_org_bank">
                            <input type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>
                            <input type="hidden" id="entity_id" name="entity_id" class="form-control" value="{entity_organisation.entity_id}"/>
                            <div  class="row">
                                <div class="col-md-6">
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label">Bank</label>
                                            <div class="col-md-9">
                                                {dropdown_bank}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label">Account number</label>
                                            <div class="col-md-9">
                                                <input type="text" class="form-control" maxlength='255' name="account_number"  id="account_number" value='{bank_vault.get("account_number", '')}'>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label">Currency</label>
                                            <div class="col-md-9">
                                                {dropdown_currency}
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label">Branch Code</label>
                                            <div class="col-md-9">
                                                <input type="text" class="form-control" maxlength='50' name="branch_code"  id="branch_code" value='{bank_vault.get("branch_code", '')}'>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label">Account Holder</label>
                                            <div class="col-md-9">
                                                <input type="text" class="form-control" maxlength='255' name="account_holder" id="account_holder" value='{bank_vault.get("account_holder", '')}'>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label">IBAN</label>
                                            <div class="col-md-9">
                                                <input type="text" class="form-control" maxlength='255' name="iban"  id="iban" value='{bank_vault.get("iban", '')}'>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
          """
        return html

    # ******************************Contact HTML
    @expose()
    def get_edit_organisation_contact_html(self, *args, **kwargs):
        entity_organisation = kwargs.get('entity_organisation')
        dbase_query = EntityOrganisationContact.by_attr_all('entity_organisation_id', entity_organisation.id)
        outputlist = []
        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"
        for item in dbase_query:

            contact_type = ContactType.by_attr_first("id", item.entity_organisation_contact_type_id)
            outputlist.append({
                'name': f"<div class='edit edit_contact' entity_id='{entity_organisation.entity_id}' entity_organisation_id='{entity_organisation.id}' contact_id='{item.id}'>{item.name}</div>",
                'value': item.value,
                'type': contact_type.name,
                'prefeered':  img_active if item.preferred else img_inactive,
            })
        dbcolumnlist = [
            'name',
            'type',
            'value',
            'prefeered'
        ]
        theadlist = [
            'Name',
            'Type',
            'Value',
            'Preferred'
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-center',
            'text-right',
        ]
        contacttable = build_html_table(outputlist, dbcolumnlist, theadlist, "contact_details", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Contacts</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_contact" entity_organisation_id="{entity_organisation.id}" entity_id='{entity_organisation.entity_id}' class="btn btn-primary ml-auto">Create New Contact</button>

                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {contacttable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_modal_new_contact(self, *args, **kwargs):
        entity_organisation_id = kwargs.get('entity_organisation_id')
        entity_id = kwargs.get('entity_id')
        dropdown_contact = self.get_selectbox_contact()
        html = f"""
            <div class="modal fade" id="dialog_new_contact" tabindex="-1" role="dialog" aria-labelledby="mytbl_system_documentLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">New Contact</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_contact'>
                              <div style='display: none' class="col-md-12">
					                <div class="form-group row">
					            	<label class="col-md-3 col-form-label" required for="organisation_id">Id</label>
					            	<div class="col-md-9">
						        	<input id="entity_organisation_id" type="text" name="entity_organisation_id" value="{entity_organisation_id}" class="form-control" required='true'>
                                        <input id="entity_id" type="text" name="entity_id" value="{entity_id}" class="form-control" required='true'>
					            	</div>
				                	</div>
			            	</div>
                             <div class="col-md-12">
                                <div class="form-group row">
                                   <label class="col-md-4 col-form-label" required for="code">{_('Contact Type ')}</label>
                                  <div class="col-md-8">
                                    {dropdown_contact}
                                </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                   <label class="col-md-4 col-form-label" required for="value">{_('Name')}</label>
                                  <div class="col-md-8">
                                    <input id="name" type="text" name="name" class="form-control" required='true'>
                                </div>
                                </div>
                            </div>
                             <div class="col-md-12">
                                <div class="form-group row">
                                   <label class="col-md-4 col-form-label" required for="value">{_('Value')}</label>
                                  <div class="col-md-8">
                                    <input id="value" type="text" name="value" class="form-control" required='true'>
                                </div>
                                </div>
                            </div>
                           <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-4 col-form-label" for="active" required>Preferred</label>
                                    <div class="col-8">
                                        <div class="form-check">
                                            <label class="form-check-label">
                                                <input class="form-check-input" type="checkbox" name="preferred" id="preferred" >
                                                <span class="form-check-sign"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_contact' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary contact_back">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_new_contact');
            $('#save_new_contact').click(function(){
                 var valid = FormIsValid("#form_new_contact");
                 if(valid){

                  var formserial = $('#form_new_contact').serialize();
                    $.post('/entity/save_new_organisation_contact?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                               $.redirect(result.redirect, {'entity_id' : result.entity_id});
                        };
                        return false;
                    });
                 }
            });
            $('.contact_back').click(function(){
                $('#dialog_new_contact').modal('hide');
            });
            $('#dialog_new_contact').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def get_modal_edit_contact(self, *args, **kwargs):

        entity_organisation_id = kwargs.get('entity_organisation_id')
        entity_id = kwargs.get('entity_id')
        contact_id = kwargs.get('contact_id')
        this = EntityOrganisationContact.by_id(contact_id)
        if not this: return ''
        checked = 'checked' if this.active else ''
        preferred = 'checked' if this.preferred else ''

        dropdown_contact = self.get_selectbox_contact(this.entity_organisation_contact_type_id)
        html = f"""
                <div class="modal fade" id="dialog_edit_contact" tabindex="-1" role="dialog" aria-labelledby="mytbl_system_documentLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <div class="col-md-6">
                                    <h4 class="card-title">Edit Contact</h4>
                                </div>
                            </div>
                            <div class="modal-body">
                                <form id='form_edit_contact'>
                                  <div style='display: none' class="col-md-12">
    					                <div class="form-group row">
    					            	<label class="col-md-3 col-form-label" required for="organisation_id">Id</label>
    					            	<div class="col-md-9">
                                          <input id="entity_organisation_id" type="text" name="entity_organisation_id" value="{entity_organisation_id}" class="form-control" required='true'>
                                        <input id="entity_id" type="text" name="entity_id" value="{entity_id}" class="form-control" required='true'>
                                              <input id="contact_id" type="text" name="contact_id" value="{contact_id}" class="form-control" required='true'>
    					            	</div>
    				                	</div>
    			            	</div>
                                 <div class="col-md-12">
                                    <div class="form-group row">
                                       <label class="col-md-4 col-form-label" required for="code">{_('Contact Type ')}</label>
                                      <div class="col-md-8">
                                        {dropdown_contact}
                                    </div>
                                    </div>
                                </div>
                                 <div class="col-md-12">
                                    <div class="form-group row">
                                       <label class="col-md-4 col-form-label" required for="value">{_('Name')}</label>
                                      <div class="col-md-8">
                                        <input id="value" type="text" name="name" value="{this.name}" class="form-control" required='true'>
                                    </div>
                                    </div>
                                </div>
                                <div class="col-md-12">
                                    <div class="form-group row">
                                       <label class="col-md-4 col-form-label" required for="value">{_('Value')}</label>
                                      <div class="col-md-8">
                                        <input id="value" type="text" name="value" value="{this.value}" class="form-control" required='true'>
                                    </div>
                                    </div>
                                </div>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-4 col-form-label" for="active" required>{_('Preferred')}</label>
                                    <div class="col-8">
                                        <div class="form-check">
                                            <label class="form-check-label">
                                                <input class="form-check-input" type="checkbox" name="preferred" id="preferred" {preferred}/>
                                                <span class="form-check-sign"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div><div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-4 col-form-label" for="active" required>Active</label>
                                    <div class="col-8">
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
                                <button id='save_edit_contact' class="btn btn-primary">Save</button>
                                <button class="btn btn-outline-primary contact_edit_back">Cancel</button>
                            </div>
                        </div>
                    </div>
                </div>
                """
        javascript = """
                <script>
                setFormValidation('#form_edit_contact');
                $('#save_edit_contact').click(function(){
                     var valid = FormIsValid("#form_edit_contact");
                     if(valid){

                      var formserial = $('#form_edit_contact').serialize();
                        $.post('/entity/save_edit_organisation_contact?', formserial, function(data){
                               var result = JSON.parse(data);

                            if(result.success === true){
                                  $.redirect(result.redirect, {'entity_id' : result.entity_id});
                            };
                            return false;
                        });
                     }
                });
                $('.contact_edit_back').click(function(){
                    $('#dialog_edit_contact').modal('hide');
                });
                $('#dialog_edit_contact').modal();
                </script>
             	"""
        return html + javascript

    @expose()
    def save_new_organisation_contact(self, *args, **kwargs):
        entity_id = kwargs.get('entity_id')
        usernow = request.identity['user']
        this = EntityOrganisationContact()
        this.entity_organisation_id = kwargs.get('entity_organisation_id', None)
        this.entity_organisation_contact_type_id = kwargs.get('entity_organisation_contact_type_id', None)
        this.value = kwargs.get('value', None)
        this.name = kwargs.get('name', None)
        if kwargs.get('preferred', None): this.preferred = True
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': entity_id, 'redirect': redirect_url})

    #
    @expose()
    def save_edit_organisation_contact(self, *args, **kwargs):

        entity_id = kwargs.get('entity_id')
        usernow = request.identity['user']
        this = EntityOrganisationContact.by_id(kwargs.get('contact_id'))
        if not this: return ''
        this.name = kwargs.get('name', None)
        this.value = kwargs.get('value', None)
        this.entity_organisation_contact_type_id = kwargs.get('entity_organisation_contact_type_id', None)
        if not kwargs.get('active', None): this.active = False
        if kwargs.get('preferred', None): this.preferred = True
        DBSession.flush()

        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': entity_id, 'redirect': redirect_url})

    # ****************************End of Contact HTML
    @expose()
    def get_district_html(self, *args, **kwargs):
        dropdown_district = self.get_selectbox_district(**kwargs)
        html = f"""
        <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">{_('District')}</label>
                        <div class="col-md-9">
                             {dropdown_district}
                        </div>
                    </div>
                </div>
            </div>
        """
        javascript = """
        <script>
         $("#district_id").change(function () {
                var district_id = $('#district_id option:selected').val();
                var kwargs ={'district_id': district_id};

               $('#div_centre').load('/entity/get_center_html', kwargs, function(data){
                return false;
               });

             });
        $('#district_id').trigger('change');
        </script>
        """
        return html + javascript

    @expose()
    def get_center_html(self, *args, **kwargs):
        dropdown_center = self.get_selectbox_center(**kwargs)
        html = f"""
        <div class="row">
                <div class="col-md-12">
                    <div class="form-group row">
                        <label class="col-md-3 col-form-label">{_('Center')}</label>
                        <div class="col-md-9">
                             {dropdown_center}
                        </div>
                    </div>
                </div>
            </div>
        """
        javascript = """
        <script>
         $("#district_id").change(function () {
                var district_id = $('#district_id option:selected').val();
                var kwargs ={'district_id': district_id};

               $('#div_centre').load('/entity/get_center_html', kwargs, function(data){
                return false;
               });

             });
        </script>
        """
        return html + javascript

    def get_organisation_title_html(self, *args, **kwargs):

        entity_organisation = kwargs.get('entity_organisation')
        if not entity_organisation: return ''
        return f"Edit: {entity_organisation.name} "

    def get_javascript_edit_organisation_onload(self, *args, **kwargs):

        javascript = """
            $('.organisation_back').click(function(){
                $.redirect('/entity/index');
            });
             createDatepicker('#end_date');
             createDatepicker('#start_date');
             createDatepicker('#last_payment_date');
             createDatepicker('#last_invoice_date');
             createDatepicker('#register_date');

                $('.organisation_back').click(function(){
                  $.redirect('/entity/index');
              });

              $("#region_id").change(function () {
                var region_id = $('#region_id option:selected').val();
                var kwargs ={'region_id': region_id};

               $('#div_district').load('/entity/get_district_html', kwargs, function(data){
                // $('#div_district').empty();
                 //$('#div_centre').empty();
                return false;
               });

             });
             $("#region_id").trigger('change');

            $("#create_new_contact").click(function(){
                 var kwargs = {entity_organisation_id : $(this).attr('entity_organisation_id'), entity_id : $(this).attr('entity_id')};
                  $('#dialogdiv').load('/entity/get_modal_new_contact?', kwargs, function(data){
                     return false;
                  });
                });

              $(".edit_contact").click(function(){
                   var kwargs = {contact_id : $(this).attr('contact_id'), entity_organisation_id : $(this).attr('entity_organisation_id') , entity_id : $(this).attr('entity_id')};
                     $('#dialogdiv').load('/entity/get_modal_edit_contact?', kwargs, function(data){
                  return false;
                   });
              });

               setFormValidation('#form_entity_organisation');
               setFormValidation('#form_org_bank');
               setFormValidation('#form_product_owner');
                setFormValidation('#form_entity_client');
               setFormValidation('#form_postal_address');

	         $('#save_organisation').click(function(){
	        	var valid_organisation = FormIsValid("#form_entity_organisation");
	        	if(valid_organisation){
		        	var formserial = new Object;
		        	formserial = getFormData(form_entity_organisation);
		        	var data = {data : JSON.stringify(formserial)};
		        	    $.post('/entity/save_edit_entity_obj?', data, function(data){
				        var result = JSON.parse(data);
			    	        if(result.success === true){
					            $.redirect(result.redirect, {'entity_id' : result.entity_id});
			            	};
			        	return false;
		        	});
	        	}
	        });

	           $('#save_postal_address').click(function(){
	        	var valid = FormIsValid("#form_postal_address");
	        	if(valid){
		        	var formserial = new Object;
		        	formserial = getFormData(form_postal_address);
		        	var data = {data : JSON.stringify(formserial)};
		        	    $.post('/entity/save_or_edit_address?', data, function(data){
				        var result = JSON.parse(data);
			    	        if(result.success === true){
					            $.redirect(result.redirect, {'entity_id' : result.entity_id});
			            	};
			        	return false;
		        	});
	        	}
	        });
	         $('#save_bank').click(function(){
	        	var valid = FormIsValid("#form_org_bank");
	        	if(valid){
		        	var formserial = new Object;
		        	formserial = getFormData(form_org_bank);
		        	var data = {data : JSON.stringify(formserial)};
		        	    $.post('/entity/save_or_edit_bank?', data, function(data){
				        var result = JSON.parse(data);
			    	        if(result.success === true){
					            $.redirect(result.redirect, {'entity_id' : result.entity_id});
			            	};
			        	return false;
		        	});
	        	}
	        });
	          $('#save_entity_client').click(function(){
	        	var valid = FormIsValid("#form_entity_client");
	        	if(valid){
		        	var formserial = new Object;
		        	formserial = getFormData(form_entity_client);
		        	var data = {data : JSON.stringify(formserial)};
		        	    $.post('/entity/save_edit_entity_client?', data, function(data){
				        var result = JSON.parse(data);
			    	        if(result.success === true){
					            $.redirect(result.redirect, {'entity_id' : result.entity_id});
			            	};
			        	return false;
		        	});
	        	}
	        });
	         $('#save_product_owner').click(function(){
	        	var valid = FormIsValid("#form_product_owner");
	        	if(valid){
		        	var formserial = new Object;
		        	formserial = getFormData(form_product_owner);
		        	var data = {data : JSON.stringify(formserial)};
		        	console.log(data);
		        	    $.post('/entity/save_edit_product_owner?', data, function(data){
				        var result = JSON.parse(data);
			    	      if(result.success === true){
					          $.redirect(result.redirect, {'entity_id' : result.entity_id});
			            	};
			        	return false;
		        	});
	        	}
	        });
        """
        return javascript

    def get_edit_organisation_details_html(self, *args, **kwargs):
        entity_organisation = kwargs.get('entity_organisation')
        dropdown_entity_organisation = self.get_selectbox_entity_organisation(entity_organisation.entity_organisation_type_id)
        if not entity_organisation: return ''
        html = f"""
        <div class="row">
			<div class="col-md-12">
				<div class="card">
					<div class="card-header"> <div class="row d-flex">
						<div class="col-md-6">
							<h4 class="card-title">{_('Organisation Details')}</h4>
						</div>
						<div class="col-md-6  text-right">
							<button id='save_organisation' class="btn btn-primary">Save</button>
						</div>
					</div>
					<hr>
				</div>
				<div class="card-body">
					<form id="form_entity_organisation" class="row">
                    	<input type="hidden" id="entity_id" name="entity_id" class="form-control" value="{entity_organisation.entity_id}"/>
	                    <input  type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>
						<div class="col-md-6">
							<div class="form-group row">
								<label class="col-md-4 col-form-label" required for="code">{_('Organisation Name')}</label>
								<div class="col-md-8">
									<input id="name" type="text" name="name" class="form-control" value="{entity_organisation.name}"required='true'>
								</div>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group row">
								<label class="col-md-4 col-form-label" required for="code">{_('Tax Number')}</label>
								<div class="col-md-8">
									<input id="tax_number" type="text" name="tax_number" class="form-control" value="{entity_organisation.tax_number}"required='true'>
								</div>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group row">
								<label class="col-md-4 col-form-label" required for="code">{_('Registration Number')}</label>
								<div class="col-md-8">
									<input id="registration_number" type="text" name="registration_number" class="form-control" value="{entity_organisation.registration_number}"required='true'>
								</div>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group row">
								<label class="col-md-4 col-form-label" required for="code">{_('Regulatory Number')}</label>
								<div class="col-md-8">
									<input id="financial_regulatory_number" type="text" name="financial_regulatory_number" class="form-control" value="{entity_organisation.financial_regulatory_number}"required='true'>
								</div>
							</div>
						</div>
						<div class="col-md-6">
							<div class="form-group row">
								<label class="col-md-4 col-form-label"  for="code">{_('Code')}</label>
								<div class="col-md-8">
									<input id="code" type="text" name="code" class="form-control" value="{entity_organisation.code}" >
								</div>
							</div>
						</div>
                    <div class="col-md-6">
										<div class="form-group row">
											<label class="col-md-4 col-form-label" for="">Organisation Type</label>
											<div class="col-md-8">
												{dropdown_entity_organisation}
											</div>
										</div>
									</div>

					</form>

				</div>
			</div>
		</div>
        </div>
        """
        return html

    def get_edit_organisation_card_title_html(self, *args, **kwargs):
        entity_organisation = kwargs.get('entity_organisation')

        if not entity_organisation: return ''

        html = f"""
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-8">
                            <h4 class="card-title">Edit : {entity_organisation.name} </h4>
                        </div>
                        <div class="col-md-4 text-right">
                            <button class="btn btn-primary ml-auto organisation_back">Back to Organisation</button>
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

        </script>
        """
        return html + javascript

    @expose()
    def save_edit_entity_obj(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        this = EntityOrganisation.by_id(data.get('entity_organisation_id'))
        if not this: return ''
        this.code =data.get('code'),
        this.name = data.get('name', None)
        this.tax_number = data.get('tax_number', None)
        this.registration_number = data.get('registration_number', None)
        this.financial_regulatory_number = data.get('financial_regulatory_number', None)
        this.entity_organisation_type_id = data.get('entity_organisation_type_id', None)
        this.active = True
        DBSession.flush()
        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': data.get('entity_id'), 'redirect': redirect_url})

    @expose()
    def save_edit_entity_client(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))

        usernow = request.identity['user']
        this = EntityOrganisationClient.by_id(data.get('entity_organisation_id'))
        if not this: return ''
        this.billing_frequency_id = data.get('billing_frequency_type_id', None)
        this.added_by = usernow.id
        this.active = True
        DBSession.flush()
        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': data.get('entity_id'), 'redirect': redirect_url})

    @expose()
    def save_edit_product_owner(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        usernow = request.identity['user']

        if data.get('is_insurer'):
            this = EntityOrganisationInsurer.by_id(data.get('insurer_id'))
            if not this: return ''
            this.added_by = usernow.id
            this.active = False
            DBSession.add(this)
            DBSession.flush()

        if data.get('policy_number_prefix'):
            this = EntityOrganisationProductOwner.by_id(data.get('product_owner_id'))
            if not this: return ''
            this.policy_number_prefix = data.get('policy_number_prefix', None)
            this.added_by = usernow.id
            this.active = True
            DBSession.flush()

        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': data.get('entity_id'), 'redirect': redirect_url})

    @expose()
    def save_or_edit_address(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        usernow = request.identity['user']
        entity_organisation_id = data.get('entity_organisation_id')

        entity_organisation_address_type_id = TYPEUTIL.get_id_of_name('address_type', 'postal')
        dict_postal_address = {
            'address_line': data.get('address_line'),
            'city': data.get('city'),
            'address_type_id': entity_organisation_address_type_id,
            'postal_code': data.get('postal_code'),
            'country_id': data.get('country_id'),
            'region_id': data.get('region_id'),
            'district_id': data.get('district_id'),
            'centre_id': data.get('centre_id'),
            "latitude": 0,
            "longitude": 0,
            'added_by': usernow.id
        }
        check_address = EntityOrganisationAddress.by_attr_first('entity_organisation_id', entity_organisation_id)
        if not check_address:
            vault_org_address = vault.save_new_organisation_address(**dict_postal_address)
            address_id = vault_org_address.get('id')
            if not address_id: return ''
            if address_id:
                dict_organisation_address_link = {
                    'entity_organisation_address_type_id':entity_organisation_address_type_id,
                    'address_id': address_id,
                    'entity_organisation_id':data.get('entity_organisation_id'),
                }
                self.save_new_organisation_address(**dict_organisation_address_link)
        else:
            this = EntityOrganisationAddress.by_attr_first('entity_organisation_id', entity_organisation_id)
            dict_postal_address_update = {
                'id': this.address_id,
                'address_line': data.get('address_line'),
                'city': data.get('city'),
                'address_type_id': entity_organisation_address_type_id,
                'postal_code': data.get('postal_code'),
                'country_id': data.get('country_id'),
                'region_id': data.get('region_id'),
                'district_id': data.get('district_id'),
                'centre_id': data.get('centre_id'),
                "latitude": 0,
                "longitude": 0,
                'added_by': usernow.id
            }
            vault.update_organisation_address(**dict_postal_address_update)

        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': data.get('entity_id'), 'redirect': redirect_url})

    @expose()
    def save_or_edit_bank(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        usernow = request.identity['user']
        entity_organisation_id = data.get('entity_organisation_id')
        bank_account_type_id = TYPEUTIL.get_id_of_name('bank_account_type', 'commercial')
        # Spot For Swift Code
        dict_organisation_bank = {
            'bank_id': data.get('bank_id'),
            'bank_account_type_id': bank_account_type_id,
            'account_number': data.get('account_number'),
            'account_holder': data.get('account_holder'),
            'branch_code': data.get('branch_code'),
            'iban': data.get('iban'),
            'swift_code': '000000000000000',
            'currency_id': data.get('currency_id'),
            'organisation_id': entity_organisation_id,
            'added_by': usernow.id,
            'active': 1
        }
        check_bank = EntityOrganisationBankAccountLink.by_attr_first('entity_organisation_id', entity_organisation_id)
        if not check_bank:
            vault_org_bank = vault.save_new_organisation_bankaccount(**dict_organisation_bank)
            bank_account_id = vault_org_bank.get('id')
            if not bank_account_id: return ''
            if bank_account_id:
                dict_organisation_bank_link = {
                    'bank_account_id': bank_account_id,
                    'entity_organisation_id': entity_organisation_id,
                }
                self.save_new_organisation_bankaccount(**dict_organisation_bank_link)
        else:
            this = EntityOrganisationBankAccountLink.by_attr_first('entity_organisation_id', entity_organisation_id)
            dict_organisation_bank_update = {
                "id": this.bank_account_id,
                "bank_id": data.get('bank_id'),
                "bank_account_type_id": bank_account_type_id,
                "swift_code": "00000000000000",
                "account_number": data.get('account_number'),
                "account_holder": data.get('account_holder'),
                "branch_code": data.get('branch_code'),
                "iban": data.get('iban'),
                "currency_id": data.get('currency_id'),
                "added_by": usernow.id,
                "active": 1,
            }
            vault.update_organisation_bank(**dict_organisation_bank_update)

        redirect_url = '/entity/edit_organisation'
        return json.dumps({'success': True, 'entity_id': data.get('entity_id'), 'redirect': redirect_url})

    @expose()
    def save_new_organisation_address(self, *args, **kwargs):
        usernow = request.identity['user']
        this = EntityOrganisationAddress()
        this.address_id = kwargs.get('address_id', None)
        this.entity_organisation_id = kwargs.get('entity_organisation_id', None)
        this.entity_organisation_address_type_id = kwargs.get('entity_organisation_address_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_organisation_bankaccount(self, *args, **kwargs):
        usernow = request.identity['user']
        this = EntityOrganisationBankAccountLink()
        this.bank_account_id = kwargs.get('bank_account_id', None)
        this.entity_organisation_id = kwargs.get('entity_organisation_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id
