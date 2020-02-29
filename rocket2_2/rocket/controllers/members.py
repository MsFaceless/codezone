# -*- coding: utf-8 -*-
"""Member controller module"""

from tg import predicates, require
from tg import expose, redirect, validate, flash, url, request

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from rocket.model import *

from sqlalchemy import func, desc, asc

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController
import rocket.lib.vault_utils as vault
from rocket.lib.type_utils import TypeDictionary as TypeDict

LIMIT = 20
TYPEUTIL = TypeDict()
class MemberController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_active_member_html(*args, **kwargs)
        javascript = self.get_javascript_member_onload()
        title = _("Members")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_member_html(self, *args, **kwargs):
        usernow = request.identity['user']
        selectbox_products = kwargs.get('selectbox_products', '')
        membertable = self.get_member_html_table(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Members')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_member" class="btn btn-primary ml-auto">{_('Create New Member')}</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-4">
                            <input type="text" class="form-control search" name="searchphrase" placeholder="{_('Search by ID Number, Name or Surname')}">
                        </div>
                        <div class="col-md-4">
                            <button class="btn btn-primary action_search">{_('Search')}</button>
                            <button class="btn btn-primary">{_('Reset')}</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {membertable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_member_html_table(self, *args, **kwargs):
        outputlist = []
        dbase_query = EntityPerson.get_limit(LIMIT, 'person_id')
        for entity_person in dbase_query:
            try: personobj = vault.get_personobj_by_id(entity_person.person_id)
            except: personobj = {'detail': '', 'person': {}}
            detail = personobj.get('detail', None)
            if detail: continue
            person = personobj.get('person', {})

            identity_number = None
            identitylist = personobj.get('identities', [])
            if len(identitylist) >= 1:
                identity_number = identitylist[0].get('number', None)

            mobile = None
            contactlist = personobj.get('contacts', [])
            if len(contactlist) >= 1:
                mobile = contactlist[0].get('value', None)

            outputlist.append({
                'idnumber': f"<div class='member_edit' entity_person_id='{entity_person.id}'>{identity_number}</div>",
                'name': person.get('firstname', ''),
                'surname': person.get('surname', ''),
                'mobile': mobile,
                             })
        dbcolumnlist=[
                'idnumber',
                'name',
                'surname',
                'mobile',
                    ]
        theadlist=[
                _('ID Number'),
                _('First Name'),
                _('Surname'),
                _('Mobile Number'),
                ]
        tdclasslist = [
                'action_link',
                '',
                '',
                'text-right',
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "member_table", tdclasslist)

    @expose()
    def get_javascript_member_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_member").click(function(){
            $.redirect('/members/new_member');
        });
        $(".member_edit").click(function(){
            var data = {entity_person_id : $(this).attr('entity_person_id')};
            $.redirect('/members/edit_member', data);
        });
        """
        return javascript


    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit_member(self, *args, **kwargs):
        entity_person_id = kwargs.get('entity_person_id', None)
        if not entity_person_id: redirect('/members/index')
        entity_person = EntityPerson.by_id(entity_person_id)
        try:
            personobj = vault.get_personobj_by_id(entity_person.person_id)
        except:
            redirect('/members/new_member')
        person_vault = personobj.get('person', {})
        kwargs["person_vault"] = personobj
        kwargs["entity_person_id"] = entity_person_id

        html = self.get_edit_member_html(**kwargs)
        javascript = self.get_javascript_edit_member_onload()
        title =f"""Edit: {person_vault.get('firstname', '')}"""
        return dict(title=title, html=html, javascript=javascript)

    def get_javascript_edit_member_onload(self, *args, **kwargs):
        javascript ="""
        createDatepicker('#date_of_birth');
        createDatepicker('#register_date');
        setFormValidation('#form_edit_member');
           setFormValidation('#form_member_bank');
        $('#btn_save_edit_member').click(function(){
             var valid = FormIsValid("#form_edit_member");
             if(valid){
                var formserial = $('#form_edit_member').serialize();
                console.log(formserial);
               $.post('/members/save_edit_memberobj?', formserial, function(data){
                   var result = JSON.parse(data);
                    if(result.success === true){
                      $.redirect(result.redirect, {'entity_person_id' : result.entity_person_id});
                    };
                    return false;
                });
             }
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



        """
        return  javascript

    def get_edit_member_html(self, *args, **kwargs):

        card_header = self.get_edit_member_card_title_html(**kwargs)
        card_member_details = self.edit_member_details(**kwargs)
        card_member_address = self.get_edit_member_address_html(**kwargs)
        card_member_bank = self.get_edit_member_bank_html(**kwargs)
        card_member_contact = self.get_edit_member_contact_html(**kwargs)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                    {card_member_details}
                    {card_member_contact}
                    {card_member_address}
                    {card_member_bank}
                </div>
            </div>
        </div>
        """
        return html

    def get_edit_member_card_title_html(self, *args, **kwargs):

        person_vault = kwargs.get('person_vault')
        person = person_vault.get("person", None)
        if not person_vault: return ''
        html = f"""
          <div class="col-md-12">
              <div class="card">
                  <div class="card-header">
                      <div class="row d-flex">
                          <div class="col-md-8">
                              <h4 class="card-title">Edit : {person.get('firstname', '')} </h4>
                          </div>
                          <div class="col-md-4 text-right">
                              <button class="btn btn-primary ml-auto members_back">Back to Members</button>
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
             $('.members_back').click(function(){
                   $.redirect('/members/index');
              });
          </script>
          """
        return html + javascript

    def edit_member_details(self, *args, **kwargs):
        entity_person_id = kwargs.get('entity_person_id')
        person_vault = kwargs.get('person_vault')
        person = person_vault.get("person", None)

        identity_number = None
        identity_type_id = None
        identitylist = person_vault.get('identities', [])
        if len(identitylist) >= 1:
            identity_number = identitylist[0].get('number', None)
            identity_type_id =identitylist[0].get('identity_type_id', None)

        mobile = None
        contactlist = person_vault.get('contacts', [])
        if len(contactlist) >= 1:
            mobile = contactlist[0].get('value', None)

        dropdown_title = self.get_selectbox_person_title_type(**{'selected': person.get('person_title_type_id')})
        dropdown_identity_type = self.get_selectbox_identity_type(**{'selected': identity_type_id})
        dropdown_gender = self.get_selectbox_gender_type(**{'selected': person.get('person_gender_type_id')})
        dropdown_language = self.get_selectbox_language(**{'selected': person.get('language_id')})

        html = f"""
        <div class="row">
			<div class="col-md-12">
				<div class="card ">
					<div class="card-header d-flex">
						<div class="col-md-6">
							<h4 class="card-title">{_('Edit Member')}</h4>
						</div>
						<div class="col-md-6 text-right">
                              <button id='btn_save_edit_member' class="btn btn-primary">{_('Save')}</button>
						</div>
					</div>
					<div class="card-body ">
						<form id="form_edit_member">
                                <input  type="hidden" id="entity_person_id" name="entity_person_id" class="form-control" value="{entity_person_id}"/>
							<div class="row">
								<div class="col-md-6">
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Title')}</label>
											<div class="col-md-9">
												{dropdown_title}
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('First Name')}</label>
											<div class="col-md-9">
												<input type="text" name='name' class="form-control" required="true" maxlength='50' value="{person.get('firstname', '')}">
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Identity Type')}</label>
											<div class="col-md-9">
												{dropdown_identity_type}
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Date of Birthday')}</label>
											<div class="col-md-9">
												<input type="text" class="form-control" name="date_of_birth" id="date_of_birth" value="{person.get('date_of_birth', '')}">
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Mobile')}</label>
											<div class="col-md-9">
												<input type="text" name='mobile' class="form-control" required="true" value="{mobile}">
											</div>
										</div>
									</div>

								</div>
								<div class="col-md-6">
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Gender')}</label>
											<div class="col-md-9">
												{dropdown_gender}
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Surname')}</label>
											<div class="col-md-9">
												<input type="text" name='surname' class="form-control" required="true" maxlength='50' value="{person.get('surname', '')}">
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('ID Number')}</label>
											<div class="col-md-9">
												<input class="form-control" type="text" name="number" required="true" maxlength='50' value="{identity_number}">
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label" required>{_('Language')}</label>
											<div class="col-md-9">
												{dropdown_language}
											</div>
										</div>
									</div>
									<div class="col-md-12">
										<div class="form-group row">
											<label class="col-md-3 col-form-label required">{_('Register Date')}</label>
											<div class="col-md-9">
												<input type="text" name='register_date' id='register_date' class="form-control" value="{person.get('added', '')}">
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
        javascript = """
       <script>

        </script>
        """
        return html+javascript

    # ******************************Contact HTML
    @expose()
    def get_edit_member_contact_html(self, *args, **kwargs):
        entity_person_id = kwargs.get('entity_person_id')
        dbase_query = []
        outputlist = []
        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"
        for item in dbase_query:
            contact_type = ContactType.by_attr_first("id", item.contact_type_id)
            outputlist.append({
                'name': f"<div class='edit edit_contact'  entity_person_id='{entity_person_id}' contact_id='{item.id}'>{item.name}</div>",
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
        <div id= "div_contact_table">
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Contacts</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_contact" entity_person_id='{entity_person_id}' class="btn btn-primary ml-auto">Create New Contact</button>

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
        </div>
        """
        javascript ="""
        <script>
             $("#create_new_contact").click(function(){
                 var kwargs = {entity_person_id : $(this).attr('entity_person_id')};
                  $('#dialogdiv').load('/members/get_modal_new_contact?', kwargs, function(data){
                     return false;
                  });
                });
        </script>
        """
        return html +javascript

    @expose()
    def get_modal_new_contact(self, *args, **kwargs):
        entity_person_id = kwargs.get('entity_person_id')
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
                                    <label class="col-md-3 col-form-label" required for="entity_person_id">Id</label>
                                    <div class="col-md-9">

                                        <input id="entity_person_id" type="text" name="entity_person_id" value="{entity_person_id}" class="form-control" required='true'>
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
                    $.post('/members/save_new_member_contact?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                             $('#dialog_new_contact').modal('hide');
                            $('#div_contact_table').load('/members/get_edit_member_contact_html?', result, function(data){
                                 return false;
                            });
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
    def save_new_member_contact(self, *args, **kwargs):
        entity_person_id = kwargs.get('entity_person_id')
        print("Vault Placeholder for Save Contact")
        print(kwargs)

        redirect_url = '/members/edit_member'
        return json.dumps({'success': True, 'entity_person_id': entity_person_id, 'redirect': redirect_url})

    @expose()
    def get_edit_member_bank_html(self, *args, **kwargs):
        entity_person_id = kwargs.get('entity_person_id')
        person_vault = kwargs.get('person_vault')
        person = person_vault.get("person", None)

        bank_vault = {}
        bank_id = None
        currency_id = None
        person_bank_link = []
        if person_bank_link:
            bank_vault = vault.get_bankaccount_by_id({person.get('id', '')})
            if bank_vault:
                bank_id = bank_vault.get('id', None)
                currency_id = bank_vault.get('currency_id', None)
        dropdown_bank = self.get_selectbox_bank(**{'selected': bank_id})
        dropdown_currency = self.get_selectbox_currency(**{'selected': currency_id})
        html = f"""
<div id="div_bank_table">
   <div class="row">
			<div class="col-md-12">
				<div class="card ">
					<div class="card-header d-flex">
						<div class="col-md-6">
							<h4 class="card-title">{_('Edit Bank')}</h4>
						</div>
						<div class="col-md-6 text-right">
                             <button id='save_edit_bank' class="btn btn-primary">{_('Save')}</button>
						</div>
					</div>
					<div class="card-body ">
					     <form id="form_member_bank">
                            <input type="hidden" id="entity_person_id" name="entity_person_id" class="form-control" value="{entity_person_id}"/>

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
</div>
              """
        javascript = """
         <script>

            $('#save_edit_bank').click(function(){
                 var valid = FormIsValid("#form_member_bank");
                 if(valid){
                  var formserial = $('#form_member_bank').serialize();
                  console.log(formserial);
                    $.post('/members/save_new_member_bank?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                $.redirect(result.redirect, {'entity_person_id' : result.entity_person_id});
                        };
                        return false;
                    });
                 }
            });
         </script>
         """
        return html + javascript

    @expose()
    def get_edit_member_address_html(self, *args, **kwargs):
        dropdown_country = self.get_selectbox_country(**{'selected': 207})

        org_address_vault = {}
        # if entity_organisation_address:
        #     org_address_vault = vault.get_address_by_id(entity_organisation_address.address_id)
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

    @expose('rocket.templates.generic')
    def new_member(self, *args, **kwargs):
        title = _("New Member")
        dropdown_title = self.get_selectbox_person_title_type()
        dropdown_identity_type = self.get_selectbox_identity_type()
        dropdown_gender = self.get_selectbox_gender_type()
        dropdown_language = self.get_selectbox_language()
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card ">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('New Member')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back members_back">{_('Back to Members')}</button>
                        </div>
                    </div>
                    <div class="card-body ">
                        <form id="form_new_member">
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Title')}</label>
                                            <div class="col-md-9">
                                                {dropdown_title}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('First Name')}</label>
                                            <div class="col-md-9">
                                                <input type="text" name='name' class="form-control" required="true" maxlength='50'>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Identity Type')}</label>
                                            <div class="col-md-9">
                                                {dropdown_identity_type}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Date of Birthday')}</label>
                                            <div class="col-md-9">
                                                <input type="text" class="form-control" name="date_of_birth" id="date_of_birth">
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Mobile')}</label>
                                            <div class="col-md-9">
                                                <input type="text" name='mobile' class="form-control" required="true">
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Gender')}</label>
                                            <div class="col-md-9">
                                                {dropdown_gender}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Surname')}</label>
                                            <div class="col-md-9">
                                                <input type="text" name='surname' class="form-control" required="true" maxlength='50'>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('ID Number')}</label>
                                            <div class="col-md-9">
                                                <input class="form-control" type="text" name="number" required="true" maxlength='50'>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label" required>{_('Language')}</label>
                                            <div class="col-md-9">
                                                {dropdown_language}
                                            </div>
                                        </div>
                                    </div>
                                    <div class="col-md-12">
                                        <div class="form-group row">
                                            <label class="col-md-3 col-form-label required">{_('Register Date')}</label>
                                            <div class="col-md-9">
                                                <input type="text" name='register_date' id='register_date' class="form-control">
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
        <div class="row">
            <div class="col-md-12">
                <div class="card ">
                    <div class="card-body">
                        <button id="btn_save_new_member" class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary members_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        createDatepicker('#date_of_birth');
        createDatepicker('#register_date');
        setFormValidation('#form_new_member');
        $('#btn_save_new_member').click(function(){
             var valid = FormIsValid("#form_new_member");
             if(valid){
                var formserial = $('#form_new_member').serialize();
                console.log(formserial);
                $.post('/members/save_new_memberobj?', formserial, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect(result.redirect, {'entity_person_id' : result.entity_person_id});
                    };
                    return false;
                });
             }
        });
        $('.members_back').click(function(){
            $.redirect('/members/index');
        });
        """
        return dict(title=title, html=html, javascript=javascript)

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

    def get_selectbox_contact(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'contact_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("contact_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_identity_type(self, *args, **kwargs):
        kwargs['outputlist'] = self.identity_type_list
        kwargs['id'] = 'identity_type_id'
        return create_selectbox_html(**kwargs)

    def get_selectbox_gender_type(self, *args, **kwargs):
        kwargs['outputlist'] = self.person_gender_type_list
        kwargs['id'] = 'person_gender_type_id'
        return create_selectbox_html(**kwargs)

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

    def get_selectbox_person_title_type(self, selected= None, *args, **kwargs):
        kwargs['id'] = 'person_title_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TypeDict().get_dict_of_types("person_title_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_identity_type(self, selected= None, *args, **kwargs):
        kwargs['id'] = 'identity_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TypeDict().get_dict_of_types("person_identity_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_gender_type(self, selected= None, *args, **kwargs):
        kwargs['id'] = 'person_gender_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TypeDict().get_dict_of_types("person_gender_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_language(self, selected= None, *args, **kwargs):
        language_list = Language.get_all('name')
        kwargs['id'] = 'language_id'
        kwargs['selected'] = selected
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in language_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_bank(self, *args, **kwargs):
        bank_list = Bank.get_all('name')
        kwargs['id'] = 'bank_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in bank_list]
        return create_selectbox_html(**kwargs)
    def get_selectbox_currency(self, *args, **kwargs):
        currecy_list = Currency.get_all('name')
        kwargs['id'] = 'currency_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in currecy_list]
        return create_selectbox_html(**kwargs)

    @expose()
    def save_new_memberobj(self, *args, **kwargs):

        contact_type_mobile = TYPEUTIL.get_id_of_name('contact_type', 'mobile')
        usernow = request.identity['user']
        dict_person = {
            "surname": kwargs.get('surname'),
            "firstname" : kwargs.get('name'),
            "preferred_name" : kwargs.get('name'),
            "person_gender_type_id" : kwargs.get('person_gender_type_id'),
            "person_title_type_id" : kwargs.get('person_title_type_id'),
            "date_of_birth" : str_to_date(kwargs.get('date_of_birth')).isoformat(),
            "language_id" : kwargs.get('language_id'),
            "identity_type_id" : kwargs.get('identity_type_id'),
            "number" : kwargs.get('number'),
            "contact_type_id" : contact_type_mobile,
            "value" : kwargs.get('mobile'),
            "register_date" : str_to_date(kwargs.get('register_date')).isoformat(),
            'added_by' : usernow.id,
            'added' : datetime.now().isoformat(),
            'active': True,
        }

        vault_person = vault.save_new_vault_person(**dict_person)
        person_id = vault_person.get('person_id')

        dict_member = {"person_id": person_id, }
        entity_person_id = self.save_new_entity_person(**dict_member)

        redirect_url = '/members/edit_member'
        return json.dumps({'success': True, 'entity_person_id': entity_person_id, 'redirect': redirect_url})


    @expose()
    def save_edit_memberobj(self, *args, **kwargs):
        print("Update Vault Placeholder")

        redirect_url = '/members/edit_member'
        return json.dumps({'success': True, 'entity_person_id': kwargs.get('entity_person_id'), 'redirect': redirect_url})


    @expose()
    def save_new_memberobj_batch(self, *args, **kwargs):
        print(kwargs)
        member_dict = {}

        dict_person = {
            'surname' : kwargs.get('surname'),
            'firstname' : kwargs.get('first_name'),
            'preferred_name' : kwargs.get('first_name'),
            'person_gender_type_id' : 3,
            'person_title_type_id' : 1,
            'date_of_birth' : kwargs.get('birthdate'),
            'language_id' : 1,
        }

        member_dict.update({'person': dict_person})
        usernow = request.identity['user']
        member_dict['person']['added_by'] = usernow.id

        dict_person_identity = {
            'identity_type_id' : 1,
            'number' : kwargs.get('identity_number'),
        }
        member_dict.update({'identity': dict_person_identity})

        contact_type_mobile = 1

        dict_person_contact = {
            'contact_type_id' : contact_type_mobile,
            'value' : kwargs.get('mobile'),
        }
        member_dict.update({'contact': dict_person_contact})

        dict_member = {
            'register_date' : datetime.now(),
        }

        vault_person = vault.save_new_vault_person_batch(**member_dict)
        person_id = vault_person.get('person_id')

        member_dict.update(vault_person)
        dict_member['person_id'] = person_id

        member_id = self.save_new_entity_person(**dict_member)
        if not member_id: return json.dumps({'success' : False})

        dict_member_comment = {
            'member_id' : member_id,
            'comment' : kwargs.get('comment'),
        }
        #self.save_new_member_comment(**dict_member_comment)

        return json.dumps({'success' : True})

    @expose()
    def save_new_entity_person(self, *args, **kwargs):
        usernow = request.identity['user']
        entity_id = self.save_new_entity(**kwargs)
        this = EntityPerson()
        this.entity_id = entity_id
        this.person_id = kwargs.get("person_id")
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_entity(self, *args, **kwargs):
        person = TYPEUTIL.get_id_of_name('entity_type', 'person')
        usernow = request.identity['user']
        this = Entity()
        this.entity_type_id = person
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_member_bank(self, *args, **kwargs):
        print("Bank Vault Placeholder")
        print(kwargs)

        """
            data = json.loads(kwargs.get('data', json.dumps({})))
        usernow = request.identity['user']
        entity_person_id = data.get('entity_person_id')
        entity_person = EntityPerson.by_id(entity_person_id)
        bank_account_type_id = TYPEUTIL.get_id_of_name('bank_account_type', 'commercial')

        dict_organisation_bank = {
            'bank_id': data.get('bank_id'),
            'bank_account_type_id': bank_account_type_id,
            'account_number': data.get('account_number'),
            'account_holder': data.get('account_holder'),
            'branch_code': data.get('branch_code'),
            'iban': data.get('iban'),
            'swift_code': '000000000000000',
            'currency_id': data.get('currency_id'),
            'entity_person_id': entity_person_id,
            'added_by': usernow.id,
            'active': 1
        }

        check_personbankaccount_link = vault.get_personbankaccount_link_by_person_id
        if not check_personbankaccount_link:
            bank_vault= vault.save_new_organisation_bankaccount(**dict_organisation_bank)
            bank_account_id = bank_vault.get('id', None)
            person_bankaccount_link_dict ={
                "person_id": entity_person.person_id,
                "bank_account_id": bank_account_id,
            }
            vault.create_personbankaccount_link(**person_bankaccount_link_dict)
        else:
            bank_account_id = check_personbankaccount_link.get('bank_account_id', None)
            #Updates Bank Account
            dict_person_bank_update = {
                "id": bank_account_id,
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
            vault.update_organisation_bank(**dict_person_bank_update)
        """

        redirect_url = '/members/edit_member'
        return json.dumps({'success': True, 'entity_person_id': kwargs.get('entity_person_id'), 'redirect': redirect_url})
