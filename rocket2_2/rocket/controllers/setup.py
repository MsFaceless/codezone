# -*- coding: utf-8 -*-
"""Setup controller module"""

from tg import predicates, require, response, use_wsgi_app
from tg import expose, redirect, validate, flash, url, request

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from rocket.model import *

from sqlalchemy import func, desc, asc, or_

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController

from webob.static import FileApp
from reportlab.platypus import Paragraph
from rocket.lib.tg_generic_reportlab import PDFCreator

import rocket.lib.vault_utils as vault

from rocket.lib.type_utils import TypeDictionary as TypeDict
from rocket.controllers.common import CommonController
LIMIT = 20
FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')

SEARCHKEY_CURRENCY = 'Currency_SearchKeyword'
SEARCHKEY_INTERMEDIARY = 'Intermediary_SearchKeyword'
SEARCHKEY_PREMIUMRATE = 'PremiumRate_SearchKeyword'
SEARCHKEY_PRODUCTLOADER = 'ProductLoader_SearchKeyword'
SEARCHKEY_INTERMEDIARYDISCLOSURE = 'IntermediaryDisclosure_SearchKeyword'
SEARCHKEY_BANK = 'Bank_SearchKeyword'

COMMON = CommonController()
TYPEUTIL = TypeDict()
class SetupController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def system_documents(self, *args, **kwargs):
        html = self.get_active_system_document_html(*args, **kwargs)
        javascript = self.get_javascript_system_document_onload()
        title = "System_documents"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_system_document_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_system_document_list(*args, **kwargs)
        selectbox_system_document_type = self.get_selectbox_system_document_type()
        outputlist = []
        for item in dbase_query:
            name = TypeDict().get_pretty_name("system_document_type", item.system_document_type_id)
            outputlist.append({
                'name': "<div class='edit system_document_edit' system_document_id='{1}'>{0}</div>".format(
                    item.name, item.id),
                'description': item.description,
                'system_document_type_id': name,
            })
        dbcolumnlist = [
            'name',
            'description',
            'system_document_type_id',
        ]
        theadlist = [
            'Name',
            'Description',
            'Document Type',
        ]
        tdclasslist = [
            'action_link',
            'text-right',
            'text-right',
        ]
        system_document_table = build_html_table(outputlist, dbcolumnlist, theadlist, "system_document_table", tdclasslist)
        html = f"""
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">System Documents</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_system_document" class="btn btn-primary ml-auto">Create New System Document</button>
                            </div>
                        </div>
                        <div class="row d-flex align-items-center">
                            <div class="col-md-4">
                                <input type="text" class="form-control search" name="searchphrase" placeholder="Search">
                            </div><div class="col-md-4">
                               {selectbox_system_document_type}
                            </div>
                            <div class="col-md-4">
                                <button class="btn btn-primary action_search">Search</button>
                                <button class="btn btn-primary">Reset</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            {system_document_table}
                        </div>
                    </div>
                    </div>
                </div>
            """
        return html

    @expose()
    def get_javascript_system_document_onload(self, *args, **kwargs):
        javascript = """
            $("#create_new_system_document").click(function(){
                $('#dialogdiv').load('/setup/get_modal_new_system_document?', function(data){
                    return false;
                });
            });
            $(".system_document_edit").click(function(){
                var kwargs = 'system_document_id='+$(this).attr('system_document_id');
                $('#dialogdiv').load('/setup/get_modal_edit_system_document?'+kwargs, function(data){
                    return false;
                });
            });
            """
        return javascript

    def get_selectbox_system_document_type(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'system_document_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TypeDict().get_dict_of_types("system_document_type")
        return create_selectbox_html(**kwargs)

    @expose()
    def get_modal_new_system_document(self, *args, **kwargs):
        selectbox_system_document_type = self.get_selectbox_system_document_type()

        html = f"""
            <div class="modal fade" id="dialog_new_system_document" tabindex="-1" role="dialog" aria-labelledby="mysystem_documentLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">New System Document</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_system_document'>
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
    						<label class="col-md-3 col-form-label" required for="description">Description</label>
    						<div class="col-md-9">
    							<input id="description" type="text" name="description" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                                    <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="system_document_type_id">Document Type</label>
    						<div class="col-md-9">
    							{selectbox_system_document_type}
    						</div>
    					</div>
    				</div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_system_document' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary system_document_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_new_system_document');
            $('#save_new_system_document').click(function(){
                 var valid = FormIsValid("#form_new_system_document");
                 if(valid){
                    var formserial = getFormData('#form_new_system_document');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_new_system_document?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/system_documents');
                        };
                        return false;
                    });
                 }
            });
            $('.system_document_back').click(function(){
                $('#dialog_new_system_document').modal('hide');
            });
            $('#dialog_new_system_document').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def get_modal_edit_system_document(self, *args, **kwargs):
        system_document_id = kwargs.get('system_document_id', None)
        if not system_document_id:
            return ''
        this = self.get_system_document_by_id(*args, **kwargs)
        selectbox_system_document_type = self.get_selectbox_system_document_type(this.system_document_type_id)

        if not this:
            return ''
        checked = 'checked' if this.active else ''
        html = f"""
            <div class="modal fade" id="dialog_edit_system_document" tabindex="-1" role="dialog" aria-labelledby="mysystem_documentLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">Edit System Document</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_edit_system_document'>
                                <div style='display: none' class="col-md-6">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="system_document_id">Id</label>
    						<div class="col-md-9">
    							<input id="id" type="text" name="system_document_id" value="{this.id}" class="form-control" required='true'>
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
    						<label class="col-md-3 col-form-label" required for="description">Description</label>
    						<div class="col-md-9">
    							<input id="description" type="text" name="description" value="{this.description}" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                                <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="system_document_type_id">Document Type</label>
    						<div class="col-md-9">
    						{selectbox_system_document_type}
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
                            <button id='save_edit_system_document' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary system_document_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_edit_system_document');
            $('#save_edit_system_document').click(function(){
                 var valid = FormIsValid("#form_edit_system_document");
                 if(valid){
                    var formserial = getFormData('#form_edit_system_document');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_edit_system_document?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/system_documents');
                        };
                        return false;
                    });
                 }
            });
            $('.system_document_back').click(function(){
                $('#dialog_edit_system_document').modal('hide');
            });
            $('#dialog_edit_system_document').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def save_new_system_document(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = SystemDocument()
        this.name = data.get('name', None)
        this.description = data.get('description', None)
        this.system_document_type_id = data.get('system_document_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_system_document(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_system_document_by_id(**data)
        if not this:
            return json.dumps({'success': False, 'data': 'No system_document found for id provided'})
        this.name = data.get('name', None)
        this.description = data.get('description', None)
        this.system_document_type_id = data.get('system_document_type_id', None)
        if not data.get('active', None):
            this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_system_document_by_id(self, *args, **kwargs):
        return DBSession.query(SystemDocument). \
            filter(SystemDocument.id == kwargs.get('system_document_id', None)). \
            first()

    @expose()
    def get_active_system_document_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        name = kwargs.get('name', None)
        description = kwargs.get('description', None)
        system_document_system_document_type_id = kwargs.get('system_document_system_document_type_id', None)

        if name:
            searchphrase = "%" + kwargs['name'] + "%"
            dbase_query = DBSession.query(SystemDocument). \
                filter(SystemDocument.name.like(searchphrase)). \
                filter(SystemDocument.active == 1). \
                order_by(asc(SystemDocument.name)).limit(LIMIT)
        if description:
            searchphrase = "%" + kwargs['description'] + "%"
            dbase_query = DBSession.query(SystemDocument). \
                filter(SystemDocument.description.like(searchphrase)). \
                filter(SystemDocument.active == 1). \
                order_by(asc(SystemDocument.description)).limit(LIMIT)
        if system_document_system_document_type_id:
            dbase_query = DBSession.query(SystemDocument). \
                filter(
                SystemDocument.system_document_system_document_type_id == system_document_system_document_type_id). \
                filter(SystemDocument.active == 1). \
                order_by(asc(SystemDocument.system_document_id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(SystemDocument). \
                filter(SystemDocument.active == 1). \
                order_by(asc(SystemDocument.id)). \
                limit(LIMIT)
        return dbase_query

#######################################################################
# Currency
#######################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def currencies(self, *args, **kwargs):
        html = self.get_active_currency_html(*args, **kwargs)
        javascript = self.get_javascript_currency_onload()
        title = "Currency"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_currency_html(self, *args, **kwargs):

        kwargs['searchkey'] = SEARCHKEY_CURRENCY
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        currencytable   =self.get_currency_htmltable(**kwargs)
        html = f"""
            <div class="row" >
                <div class="col-md-12">
                    <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Currency</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_currency" class="btn btn-primary ml-auto">Add a New Currency</button>
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
                        <div  class="table-responsive" id='div_currency_table'>
                            {currencytable}
                        </div>
                    </div>
                    </div>
                </div>

            """
        javascript = """
        <script>
            $("#create_new_currency").click(function(){
                $('#dialogdiv').load('/setup/get_modal_new_currency?', function(data){
                    return false;
                });
            });

              $('#action_search').click(function(){
                 var kwargs = 'searchphrase='+$('#searchphrase').val();
                 $('#div_currency_table').load('/setup/get_currency_htmltable', kwargs, function(data){
                     return false;
                 });
             })
             $('#btn_reset').click(function(){
              $('#searchphrase').val('').focus();
                 $('#div_currency_table').load('/setup/get_currency_htmltable', 'reset=true', function(data){
                     return false;
                 });
             })
             </script>
             """
        return html + javascript
    @expose()
    def get_currency_htmltable(self, *args, **kwargs):
        dbase_query = self.get_active_currency_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code': "<div class='edit currency_edit' currency_id='{1}'>{0}</div>".format(item.code, item.id),
                'name': item.name,
                'is_home_currency': item.is_home_currency,
            })
        dbcolumnlist = [
            'code',
            'name',
            'is_home_currency',
        ]
        theadlist = [
            'Code',
            ' Name',
            ' Home Currency',
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-right',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "currency_table", tdclasslist)
        javascript="""
       <script>
         $(".currency_edit").click(function(){
                var kwargs = 'currency_id='+$(this).attr('currency_id');
                $('#dialogdiv').load('/setup/get_modal_edit_currency?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """

        return  html +javascript

    @expose()
    def get_javascript_currency_onload(self, *args, **kwargs):
        javascript = """

            """
        return javascript

    def get_selectbox_inactive_currencies(self, *args, **kwargs):
        kwargs['id'] = 'currency_id'
        kwargs['case_sensitive'] = True
        dbase_query = DBSession.query(Currency).filter(Currency.active==False).order_by(asc(Currency.code)).all()
        kwargs['outputlist'] = [{'id': x.id, 'name': f"{x.code}: {x.name}"} for x in dbase_query]
        return create_selectbox_html(**kwargs)

    @expose()
    def get_modal_new_currency(self, *args, **kwargs):
        selectbox_inactive_currencies = self.get_selectbox_inactive_currencies()
        html = f"""
            <div class="modal fade" id="dialog_new_currency" tabindex="-1" role="dialog" aria-labelledby="mycurrencyLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">Add Currency</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_currency'>
                                    <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="code">Code</label>
    						<div class="col-md-9">
    							{selectbox_inactive_currencies}
    						</div>
    					</div>
    				</div>

                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_currency' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary currency_back">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_new_currency');
            $('#save_new_currency').click(function(){
                 var valid = FormIsValid("#form_new_currency");
                 if(valid){
                    var formserial = getFormData('#form_new_currency');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_new_currency?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/currencies');
                        };
                        return false;
                    });
                 }
            });
            $('.currency_back').click(function(){
                $('#dialog_new_currency').modal('hide');
            });
            $('#dialog_new_currency').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def get_modal_edit_currency(self, *args, **kwargs):
        currency_id = kwargs.get('currency_id', None)
        if not currency_id: return ''
        this = self.get_currency_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        is_home_currency = 'checked' if this.is_home_currency else ''
        html = f"""
            <div class="modal fade" id="dialog_edit_currency" tabindex="-1" role="dialog" aria-labelledby="mycurrencyLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">Edit Currency</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_edit_currency'>
                                <div style='display: none' class="col-md-6">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="currency_id">Id</label>
    						<div class="col-md-9">
    							<input id="id" type="text" name="currency_id" value="{this.id}" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                                <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-4 col-form-label" required for="code"> Code</label>
    						<div class="col-md-8">
    							<input id="code" type="text" name="code" value="{this.code}" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                                <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-4 col-form-label" required for="name"> Name</label>
    						<div class="col-md-8">
    							<input id="name" type="text" name="name" value="{this.name}" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                      <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-4 col-form-label" for="is_home_currency" required>{_('Home Currency')}</label>
                                    <div class="col-8">
                                        <div class="form-check">
                                            <label class="form-check-label">
                                                <input class="form-check-input" type="checkbox" name="is_home_currency" id="is_home_currency" {is_home_currency}/>
                                                <span class="form-check-sign"></span>
                                            </label>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
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
                            <button id='save_edit_currency' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary currency_back">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_edit_currency');
            $('#save_edit_currency').click(function(){
                 var valid = FormIsValid("#form_edit_currency");
                 if(valid){
                    var formserial = getFormData('#form_edit_currency');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_edit_currency?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/currencies');
                        };
                        return false;
                    });
                 }
            });
            $('.currency_back').click(function(){
                $('#dialog_edit_currency').modal('hide');
            });
            $('#dialog_edit_currency').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def save_new_currency(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = Currency.by_id_inactive(data.get("currency_id"))
        this.active = True
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_currency(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_currency_by_id(**data)
        if not this: return json.dumps({'success': False, 'data': 'No currency found for id provided'})
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.is_home_currency = True if data.get('is_home_currency', None) else False
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_currency_by_id(self, *args, **kwargs):
        return DBSession.query(Currency). \
            filter(Currency.id == kwargs.get('currency_id', None)). \
            first()

    @expose()
    def get_active_currency_list(self, *args, **kwargs):

        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_CURRENCY
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()

        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(Currency). \
                filter(or_(
                Currency.code.like(searchphrase),
                Currency.name.like(searchphrase),
            )). \
            filter(Currency.active == 1). \
            order_by(asc(Currency.code)).limit(LIMIT)

            return  dbase_query
        else:
            dbase_query = DBSession.query(Currency). \
                filter(Currency.active == 1). \
                order_by(asc(Currency.id)). \
                limit(LIMIT)
        return dbase_query

###############################################################################
# Intermediaries
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def intermediaries(self, *args, **kwargs):
        html = self.get_active_intermediaries_html(*args, **kwargs)
        javascript = self.get_javascript_intermediaries_onload()
        title = _("Intermediaries")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_intermediaries_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_INTERMEDIARY

        searchphrase = COMMON.get_searchphrase(**kwargs)
        intermediariestable= self.get_intermediaries_htmltable(**kwargs)
        html = f"""
		<div class="row">
			<div class="col-md-12">
				<div class="card">
					<div class="card-header">
						<div class="row d-flex">
							<div class="col-md-6">
								<h4 class="card-title">Intermediaries</h4>
							</div>
							<div class="col-md-6 text-right">
								<button id="create_new_intermediaries" class="btn btn-primary ml-auto">Create New Intermediary</button>
							</div>
						</div>
						<div class="row d-flex align-items-center">
							<div class="col-md-4">
								<input type="text" class="form-control search" name="searchphrase" id="searchphrase" value='{searchphrase}' placeholder="Search">
							</div>
							<div class="col-md-8">
							  <button class="btn btn-primary" id='action_search'>Search</button>
                                <button class="btn btn-primary" id='btn_reset'>Reset</button>
							</div>
						</div>
						<hr>
					</div>
					<div class="card-body">
						<div class="table-responsive" id='div_intermediary_table'>
							{intermediariestable}
						</div>
					</div>
				</div>
			</div>
			<div id='div_modal_new_intermediary'></div>
           """
        javascript = """
              <script>
                     $("#create_new_intermediaries").click(function(){
                        $('#div_modal_new_intermediary').load('/setup/get_modal_new_intermediaries?', function(data){
                            return false;
                        });
                    });

                    $('#action_search').click(function(){
                       var kwargs = 'searchphrase='+$('#searchphrase').val();
                       $('#div_intermediary_table').load('/setup/get_intermediaries_htmltable', kwargs, function(data){
                           return false;
                       });
                   })
                   $('#btn_reset').click(function(){
                    $('#searchphrase').val('').focus();
                       $('#div_intermediary_table').load('/setup/get_intermediaries_htmltable', 'reset=true', function(data){
                           return false;
                       });
                   })
                   </script>
                   """
        return html +javascript

    @expose()
    def get_intermediaries_htmltable(self, *args, **kwargs):
        dbase_query = self.get_active_intermediary_list(**kwargs)
        outputlist = []
        for item in dbase_query:
            entity_organisation = EntityOrganisation.by_attr_first("id", item.entity_organisation_id)
            entity_org_type = TYPEUTIL.get_pretty_name("entity_organisation_type",
                                                       entity_organisation.entity_organisation_type_id)
            disclosure = DBSession.query(EntityOrganisationIntermediaryDisclosure).filter(
                EntityOrganisationIntermediaryDisclosure.id == item.entity_intermediary_disclosure_id).one()
            outputlist.append({
                'code': f"<div class='edit edit_intermediary' intermediary_id='{item.id}'>{entity_organisation.code}</div>",
                'entity_org_type': entity_org_type,
                'entity_org_name': entity_organisation.name,
                'disclosure': disclosure.text,
            })
        dbcolumnlist = [
            'code',
            'entity_org_name',
            'entity_org_type',
            'disclosure'
        ]
        theadlist = [
            'Code',
            'Organisation Name',
            'Organisation Type',
            'Disclosure',
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-center',
            'text-center',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "intermediaries_table", tdclasslist)
        javascript ="""
        <script>
            $(".intermediaries_edit").click(function(){
                        var kwargs = 'intermediary_id='+$(this).attr('intermediary_id');
                        $('#div_modal_new_intermediary').load('/setup/get_modal_edit_intermediaries?', kwargs, function(data){
                            return false;
                        });
                    });
                    $(".edit_intermediary").click(function(){
                        var data = {intermediary_id : $(this).attr('intermediary_id')};
                        $.redirect('/setup/edit_intermediary', data);
                    });
        </script>
        """
        return html +javascript


    @expose()
    def get_javascript_intermediaries_onload(self, *args, **kwargs):
        javascript = """


                    """
        return javascript

    @expose()
    def get_modal_new_intermediaries(self, *args, **kwargs):
        dropdown_entity_organisation = self.get_selectbox_entity_organisation()
        dropdown_disclosure_type = self.get_selectbox_disclosure()
        html = f"""
                     <div class="modal fade" id="dialog_new_intermediaries" tabindex="-1" role="dialog" aria-labelledby="myintermediariesLabel" aria-hidden="true">
               <div class="modal-dialog modal-dialog-centered modal-lg">
                   <div class="modal-content">
                       <div class="modal-header">
                           <div class="col-md-6">
                               <h4 class="card-title">New Intermediary</h4>
                           </div>
                       </div>
                       <div class="modal-body">
                           <form id='form_new_intermediaries' class="d-flex flex-wrap">

                               <div class="col-md-12">
                                   <div class="form-group row">
                                       <label class="col-md-3 col-form-label" required for="">{_('Organisation')}</label>
                                         <div class="col-md-9">
                                          {dropdown_entity_organisation}
                                        </div>
                                   </div>
                               </div>
                                <div class="col-md-12">
                                   <div class="form-group row">
                                       <label class="col-md-3 col-form-label" required for="entity_intermediary_disclosure_id">{_('Disclosure')}</label>
                                         <div class="col-md-9">
                                          {dropdown_disclosure_type}
                                        </div>
                                   </div>
                               </div>

                           </form>
                       </div>
                       <div class="modal-footer">
                           <button id='save_new_intermediaries' class="btn btn-primary">Save</button>
                       <button class="btn btn-outline-primary intermediaries_back" data-dismiss="modal">Cancel</button>
                       </div>
                   </div>
               </div>
           </div>


                    """
        javascript = """
                <script>
                    setFormValidation('#form_new_intermediaries');
                    $('#save_new_intermediaries').click(function(){
                         var valid = FormIsValid("#form_new_intermediaries");
                         if(valid){
                            var formserial = getFormData('#form_new_intermediaries');
                            var data = {data : JSON.stringify(formserial)};

                            $.post('/setup/save_new_intermediaries?', data, function(data){
                                var result = JSON.parse(data);
                               if(result.success === true){
                                      $.redirect(result.redirect, {'intermediary_id' : result.intermediary_id});
                                  };
                                return false;
                            });
                         }
                    });
                    $('.intermediaries_back').click(function(){
                        $('#dialog_new_intermediaries').modal('hide');
                    });
                    $('#dialog_new_intermediaries').modal();
                </script>
                """
        return html + javascript

    @expose()
    def get_modal_edit_intermediaries(self, *args, **kwargs):
        dropdown_entity_type = self.get_selectbox_entity_type()
        dropdown_disclosure_id = self.get_selectbox_disclosure_id()
        intermediary_id = kwargs.get('intermediary_id', None)
        if not intermediary_id:
            return ''
        this = self.get_intermediaries_by_id(*args, **kwargs)
        if not this:
            return ''
        checked = 'checked' if this.active else ''
        html = f"""
                    <div class="modal fade" id="dialog_edit_intermediaries" tabindex="-1" role="dialog" aria-labelledby="myintermediariesLabel" aria-hidden="true">
                        <div class="modal-dialog modal-dialog-centered modal-lg">
                            <div class="modal-content">
                                <div class="modal-header">
                                    <div class="col-md-6">
                                        <h4 class="card-title">Edit Intermediary</h4>
                                    </div>
                                </div>
                                <div class="modal-body">
                                    <form id='form_edit_intermediaries'>
                                        <div class="col-md-12">
                                            <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="code">Code</label>
                                                <div class="col-md-9">
                                                    <input id="code" type="text" name="code" value="{this.code}" class="form-control" required='true'>
                                                </div>
                                            </div>
                                        </div>
                                        <div style='display: none' class="col-md-6">
                                                <div class="form-group row">
                                                        <label class="col-md-3 col-form-label" required for="intermediary_id">ID</label>
                                                        <div class="col-md-9">
                                                                <input id="id" type="text" name="intermediary_id" value="{this.id}" class="form-control" required='true'>
                                                        </div>
                                                </div>
                                        </div>
                                        <div class="col-md-12">
                                            <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="entity_type_id" value="{this.entity_type_id}">{_('Entity Type')}</label>
                                                    <div class="col-md-9">
                                                        {dropdown_entity_type}
                                                    </div>
                                            </div>
                                        </div>
                                        <div class="col-md-12">
                                            <div class="form-group row">
                                                <label class="col-md-3 col-form-label" required for="entity_intermediary_disclosure_id" value="{this.entity_intermediary_disclosure_id}">{_('Disclosure Id')}</label>
                                                    <div class="col-md-9">
                                                        {dropdown_disclosure_id}
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
                                    <button id='save_edit_intermediaries' class="btn btn-primary">Save</button>
                                    <button class="btn btn-outline-primary intermediaries_back" data-dismiss="modal">Cancel</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    """
        javascript = """
                <script>
                    setFormValidation('#form_edit_intermediaries');
                    $('#save_edit_intermediaries').click(function(){
                        var valid = FormIsValid("#form_edit_intermediaries");
                        if(valid){
                            var formserial = getFormData('#form_edit_intermediaries');
                            var data = {data : JSON.stringify(formserial)};

                            $.post('/setup/save_edit_intermediaries?', data, function(data){
                                var result = JSON.parse(data);
                                if(result.success === true){
                                    $.redirect('/setup/intermediaries');
                                    };
                                return false;
                                });
                            }
                        });
                    $('.intermediaries_back').click(function(){
                        $('#dialog_edit_intermediaries').modal('hide');
                        });
                    $('#dialog_edit_intermediaries').modal();
                </script>
                """
        return html + javascript

    @expose()
    def save_new_intermediaries(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = EntityOrganisationIntermediary()
        this.entity_organisation_id = data.get('entity_organisation_id', None)
        this.entity_intermediary_disclosure_id = data.get('entity_intermediary_disclosure_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        redirect_url = '/setup/edit_intermediary'
        return json.dumps({'success': True, 'intermediary_id': this.id, 'redirect': redirect_url})

    @expose()
    def save_edit_intermediaries(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data:
            return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_intermediaries_by_id(**data)
        if not this:
            return json.dumps({'success': False, 'data': 'No intermediaries found for id provided'})
        this.code = data.get('code', None)
        this.entity_type_id = data.get('entity_type_id', None)
        this.entity_intermediary_disclosure_id = data.get('entity_intermediary_disclosure_id', None)
        # this.name = data.get('name', None)
        if not data.get('active', None):
            this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_intermediaries_by_id(self, *args, **kwargs):
        return DBSession.query(EntityOrganisationIntermediary). \
            filter(EntityOrganisationIntermediary.id == kwargs.get('intermediary_id', None)). \
            first()
    @expose()
    def get_active_intermediary_list(self, *args, **kwargs):
        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_INTERMEDIARY
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()

        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(EntityOrganisation). \
                filter(or_(
                EntityOrganisation.code.like(searchphrase),
                EntityOrganisation.name.like(searchphrase),
            )). \
            filter(EntityOrganisation.active == 1). \
            order_by(asc(EntityOrganisation.id)).limit(LIMIT)

            link_list = []
            for list in dbase_query:
                entity_organisation = EntityOrganisationIntermediary.by_attr_first('entity_organisation_id', list.id)
                link_list.append(entity_organisation)

            return  link_list
        else:
            dbase_query = DBSession.query(EntityOrganisationIntermediary). \
                filter(EntityOrganisationIntermediary.active == 1). \
                order_by(asc(EntityOrganisationIntermediary.id)). \
                limit(LIMIT)
        return dbase_query

############################################ End of Intermediary

    def get_selectbox_entity_organisation(self, selected=None, *args, **kwargs):
        kwargs['selected'] = selected
        entity_organisation_list = EntityOrganisation.get_all('name')
        kwargs['id'] = 'entity_organisation_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in entity_organisation_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_disclosure(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'entity_intermediary_disclosure_id'
        kwargs['selected'] = selected
        disclosure_list = EntityOrganisationIntermediaryDisclosure.get_all('text')
        kwargs['outputlist'] = [{'id': x.id, 'name': x.text[: 20]} for x in disclosure_list]
        return create_selectbox_html(**kwargs)


###############################################################################
# Edit Intermediaries
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def edit_intermediary(self, *args, **kwargs):
        intermediary_id = kwargs.get('intermediary_id', None)

        if not intermediary_id:
            redirect('/setup/intermediaries')
        intermediary = EntityOrganisationIntermediary.by_id(intermediary_id)
        if not intermediary:
            redirect('/setup/intermediaries')

        html = self.get_edit_intermediary_html(**kwargs)
        javascript = self.get_javascript_edit_intermediary_onload()
        title = self.get_intermediary_title_html(**kwargs)
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_edit_intermediary_html(self, *args, **kwargs):
        intermediary_id = kwargs.get('intermediary_id', None)
        if not intermediary_id: return ''
        # HEADER
        card_header = self.get_edit_intermediary_card_title_html(**kwargs)
        card_organisation_details=self.get_edit_organisation_details_html(**kwargs)
        card_address = self.get_edit_organisation_address_html(**kwargs)
        card_bank_account = self.get_edit_intermediary_bank_html(**kwargs)
        card_intermediary_agent = self.get_intemediary_agent_html(**kwargs)

        html = f"""
        {card_header}
        <div class="row">
            <div class="col-md-12 ml-auto mr-auto">
                <div class="col-md-12 ml-auto mr-auto">
                {card_organisation_details}
                {card_intermediary_agent}
                {card_bank_account}
                {card_address}
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_javascript_edit_intermediary_onload(self, *args, **kwargs):
        javascript = """
        createDatepicker('#termination_date');
        $("#create_new_edit_intermediaries").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_edit_intermediaries?', function(data){
                return false;
            });
        });
        $(".bank_edit").click(function(){
            var kwargs = 'bank_id='+$(this).attr('bank_id');
            $('#dialogdiv').load('/setup/get_modal_edit_bank?', kwargs, function(data){
                return false;
            });
        });
        $('#save_bank').click(function(){
            var valid = FormIsValid("#form_org_bank");
            if(valid){
                var formserial = new Object;
                formserial = getFormData(form_org_bank);
                var kwargs = {intermediary_id : $(this).attr('intermediary_id')};
                var data = {data : JSON.stringify(formserial)};
                $.post('/entity/save_or_edit_bank?', data, function(data){
                    $('#div_bank_html').load('/setup/get_edit_intermediary_bank_html?', kwargs, function(data){
                        return false;
                    });
                    return false;
                });
            }
        });
        $('#save_postal_address').click(function(){
            var valid = FormIsValid("#form_postal_address");
            if(valid){
                var formserial = new Object;
                var kwargs = {intermediary_id : $(this).attr('intermediary_id')};
                formserial = getFormData(form_postal_address);
                var data = {data : JSON.stringify(formserial)};
                $.post('/entity/save_or_edit_address?', data, function(data){
                    $('#div_address_html').load('/setup/get_edit_organisation_address_html?', kwargs, function(data){
                        return false;
                    });
                    return false;
                });
            }
        });
        $('#save_org_intermediary').click(function(){
            var vaild = FormIsValid("#form_entity_intermediary");
            if(vaild){
                var formserial = new Object;
                formserial = getFormData(form_entity_intermediary);
                var data = {data : JSON.stringify(formserial)};
                $.post('/setup/save_edit_entity_org_intermediary?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        /*$('#div_organisation_details_html').load('/setup/get_edit_organisation_details_html?', function(data){
                                       return false;
                                   });
                                   */
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
        return javascript

    def get_intermediary_title_html(self, *args, **kwargs):
        intermediary_id = kwargs.get('intermediary_id')
        if not intermediary_id:
            return ''
        entity_org_intermediary = EntityOrganisationIntermediary.by_id(intermediary_id)
        print(entity_org_intermediary)
        entity_org= EntityOrganisation.by_id(entity_org_intermediary.entity_organisation_id)
        return f"Edit: Intermediary - {entity_org.code}"

    def get_edit_intermediary_card_title_html(self, *args, **kwargs):
        intermediary_id = kwargs.get("intermediary_id")
        intermediary = EntityOrganisationIntermediary.by_id(intermediary_id)
        entity_organisation = EntityOrganisation.by_id(intermediary.entity_organisation_id)
        html = f"""
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-8">
                            <h4 class="card-title">Edit Intermediary: {entity_organisation.code}</h4>
                        </div>
                        <div class="col-md-4 text-right">
                            <button class="btn btn-primary ml-auto" id="intermediaries_back">Back to Intermediaries</button>
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
            $('#intermediaries_back').click(function(){
                $.redirect('/setup/intermediaries');
            });
        </script>
        """
        return html + javascript

    def get_edit_organisation_details_html(self, *args, **kwargs):

        intermediary_id = kwargs.get("intermediary_id")
        if not intermediary_id: return ''
        intermediary= EntityOrganisationIntermediary.by_id(intermediary_id)
        entity_organisation = EntityOrganisation.by_id(intermediary.entity_organisation_id)
        dropdown_entity_organisation = self.get_selectbox_entity_organisation_type(entity_organisation.entity_organisation_type_id)
        if not entity_organisation: return ''
        html = f"""
            <div class="row">
    			<div class="col-md-12">
    				<div class="card">
    					<div class="card-header"> <div class="row d-flex">
    						<div class="col-md-6">
    							<h4 class="card-title">{_('Intermediary Details')}</h4>
    						</div>
    						<div class="col-md-6  text-right">
    							<button id='save_org_intermediary' class="btn btn-primary">Save</button>
    						</div>
    					</div>
    					<hr>
    				</div>
    				<div class="card-body" id="div_organisation_details_html">
    					<form id="form_entity_intermediary" class="row">
	                     <input type="hidden" id="intermediary_id" name="intermediary_id" class="form-control" value="{intermediary_id}"/>
	                     <input  type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>
    						<div class="col-md-6">
    							<div class="form-group row">
    								<label class="col-md-4 col-form-label" required for="code">{_('Intermediary Name')}</label>
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
    											<label class="col-md-4 col-form-label" for="">Intermediary Type</label>
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

    @expose()
    def get_edit_organisation_address_html(self, *args, **kwargs):
        dropdown_country = self.get_selectbox_country(**{'selected': 207})
        intermediary_id = kwargs.get("intermediary_id")
        intermediary = EntityOrganisationIntermediary.by_id(intermediary_id)
        entity_organisation = EntityOrganisation.by_id(intermediary.entity_organisation_id)

        entity_organisation_address = EntityOrganisationAddress.by_attr_first("entity_organisation_id",
                                                                              entity_organisation.id)
        org_address_vault = {}
        if entity_organisation_address:
            org_address_vault = vault.get_address_by_id(entity_organisation_address.address_id)
        dropdown_region = self.get_selectbox_region(**{'selected': org_address_vault.get("region_id", '')})
        html = f"""<div id="div_address_html">
            <div class="row">
                <div class="col-md-6">

                    <div class="card">
                        <div class="card-header">
                            <div class="row d-flex">
                                <div class="col-md-6">
                                    <h4 class="card-title">{_('Postal Address')}</h4>
                                </div>
                                <div class="col-md-6 text-right">
    							<button id='save_postal_address'  intermediary_id ="{intermediary_id}"  class="btn btn-primary">Save</button>
                                </div>
                            </div>
                            <hr>
                        </div>
                        <div class="card-body">
                            <form id="form_postal_address">
                                <div class="row">
                                    <input type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>

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
</div>
            """
        return html

        # ******************************Contact HTML

    @expose()
    def get_intemediary_agent_html(self, *args, **kwargs):

        intermediary_id = kwargs.get("intermediary_id")
        if not intermediary_id: return ''

        dbase_query = EntityOrganisationIntermediaryAgent.by_attr_all('entity_organisation_intermediary_id', intermediary_id)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code': f"<div class='edit edit_intermediary_agent_id' intermediary_id='{intermediary_id}' intermediary_agent_id='{item.id}'>{item.code}</div>",
                'first_name': "Firstname Placholder",
                'surname': "Surname Placeholder",
                'financial_regulatory_number': item.financial_regulatory_number,
                "termination_date": item.termination_date

            })
        dbcolumnlist = [
            'code',
            'first_name',
            'surname',
            'financial_regulatory_number',
            'termination_date'
        ]
        theadlist = [
            'Code',
            'Firstname',
            'Surname',
            'Financial Regulatory Number',
            'Termination Date',
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-center',
            'text-center',
            'text-right',
        ]
        intermediaryagenttable = build_html_table(outputlist, dbcolumnlist, theadlist, "intermediary_agents", tdclasslist)
        html = f"""
            <div id="intermediary_agent_table">
         <div class="row">
             <div class="col-md-12">
                 <div class="card">
                     <div class="card-header">
                         <div class="row d-flex">
                             <div class="col-md-6">
                                 <h4 class="card-title">Intermediary Agent</h4>
                             </div>
                             <div class="col-md-6 text-right">
                                 <button id="create_new_intermediary_agent" intermediary_id="{intermediary_id}"  class="btn btn-primary ml-auto">{_('Create New Agent')}</button>

                             </div>
                         </div>
                         <hr>
                     </div>
                     <div class="card-body">
                         <div class="table-responsive" id="">
                             {intermediaryagenttable}
                         </div>
                     </div>

                 </div>
             </div>
         </div>
</div>
         """
        javascript= """
            <script>
        $(".edit_intermediary_agent_id").click(function(){
                   var kwargs = {intermediary_agent_id : $(this).attr('intermediary_agent_id'), intermediary_id : $(this).attr('intermediary_id')};
                     $('#dialogdiv').load('/setup/get_modal_edit_intermediary_agent?', kwargs, function(data){
                  return false;
                   });
              });

              $("#create_new_intermediary_agent").click(function(){
                 var kwargs = {intermediary_id : $(this).attr('intermediary_id')};

                  $('#dialogdiv').load('/setup/get_modal_new_intermediary_agent?', kwargs, function(data){
                     return false;
                  });
                });
                 </script>
        """
        return html +javascript

    @expose()
    def get_modal_new_intermediary_agent(self, *args, **kwargs):
        intermediary_id = kwargs.get('intermediary_id')
        html = f"""
             <div class="modal fade" id="dialog_new_intermediary_agent" tabindex="-1" role="dialog" aria-labelledby="mytbl_system_documentLabel" aria-hidden="true">
                 <div class="modal-dialog modal-dialog-centered modal-lg">
                     <div class="modal-content">
                         <div class="modal-header">
                             <div class="col-md-6">
                                 <h4 class="card-title">{_('Intermediary Agent')}</h4>
                             </div>
                         </div>
                         <div class="modal-body">
                            <form id='form_new_intermediary_agent'>
                               <div style='display: none' class="col-md-12">
                                    <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="organisation_id">Id</label>
                                    <div class="col-md-9">
                                    <input id="intermediary_id" type="text" name="intermediary_id" value="{intermediary_id}" class="form-control" required='true'>

                                    </div>
                                    </div>
                            </div>
                              <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="code">{_('entity_person_id ')}</label>
                                   <div class="col-md-8">
                                       <input id="entity_person_id" type="number" name="entity_person_id" class="form-control" required='true'>
                                 </div>
                                 </div>
                             </div>
                             <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="value">{_('Code')}</label>
                                   <div class="col-md-8">
                                     <input id="code" type="text" name="code" class="form-control" required='true'>
                                 </div>
                                 </div>
                             </div>
                              <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="value">{_('Financial Regulatory Number')}</label>
                                   <div class="col-md-8">
                                     <input id="financial_regulatory_number" type="text" name="financial_regulatory_number" class="form-control" required='true'>
                                 </div>
                                 </div>
                             </div>
                             <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="value">{_('Termination Date')}</label>
                                   <div class="col-md-8">
                                     <input id="termination_date" type="text" name="termination_date" class="form-control" required='true'>
                                 </div>
                                 </div>
                             </div>

                             </form>
                         </div>
                         <div class="modal-footer">
                             <button id='save_new_intermediary_agent' class="btn btn-primary">Save</button>
                             <button class="btn btn-outline-primary intermediary_agent_back">Cancel</button>
                         </div>
                     </div>
                 </div>
             </div>
             """
        javascript = """
             <script>
             setFormValidation('#form_new_intermediary_agent');
             $('#save_new_intermediary_agent').click(function(){
                  var valid = FormIsValid("#form_new_intermediary_agent");
                  if(valid){
                   var formserial = $('#form_new_intermediary_agent').serialize();
                     $.post('/setup/save_new_intermediary_agent?', formserial, function(data){
                         var result = JSON.parse(data);
                         if(result.success === true){
                            $('#dialog_new_intermediary_agent').modal('hide');
                              var kwargs = { intermediary_id: result.intermediary_id};
                              $('#intermediary_agent_table').load('/setup/get_intemediary_agent_html?', kwargs, function(data){
                                 return false;
                            });
                         };
                         return false;
                     });
                  }
             });
             $('.intermediary_agent_back').click(function(){
                 $('#dialog_new_intermediary_agent').modal('hide');
             });
             $('#dialog_new_intermediary_agent').modal();
             </script>
            """
        return html + javascript

    @expose()
    def get_modal_edit_intermediary_agent(self, *args, **kwargs):
        intermediary_agent_id = kwargs.get('intermediary_agent_id')
        intermediary_id = kwargs.get('intermediary_id')
        this = EntityOrganisationIntermediaryAgent.by_id(intermediary_agent_id)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
                 <div class="modal fade" id="dialog_edit_intermediary_agent" tabindex="-1" role="dialog" aria-labelledby="mytbl_system_documentLabel" aria-hidden="true">
                     <div class="modal-dialog modal-dialog-centered modal-lg">
                         <div class="modal-content">
                             <div class="modal-header">
                                 <div class="col-md-6">
                                     <h4 class="card-title">{_('Edit Intermediary Agent')}</h4>
                                 </div>
                             </div>
                             <div class="modal-body">
                           <form id='form_edit_intermediary_agent'>
                               <div style='display: none' class="col-md-12">
                                    <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="organisation_id">Id</label>
                                    <div class="col-md-9">
                                    <input id="intermediary_agent_id" type="text" name="intermediary_agent_id" value="{intermediary_agent_id}" class="form-control" required='true'>
                                    <input id="intermediary_id" type="text" name="intermediary_id" value="{intermediary_id}" class="form-control" required='true'>

                                    </div>
                                    </div>
                            </div>
                              <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="code">{_('entity_person_id ')}</label>
                                   <div class="col-md-8">
                                       <input id="entity_person_id" type="number" name="entity_person_id" class="form-control" required='true' value="{this.entity_person_id}">
                                 </div>
                                 </div>
                             </div>
                             <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="value">{_('Code')}</label>
                                   <div class="col-md-8">
                                     <input id="code" type="text" name="code" class="form-control" required='true' value="{this.code}">
                                 </div>
                                 </div>
                             </div>
                              <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="value">{_('Financial Regulatory Number')}</label>
                                   <div class="col-md-8">
                                     <input id="financial_regulatory_number" type="text" name="financial_regulatory_number" class="form-control" required='true' value="{this.financial_regulatory_number}">
                                 </div>
                                 </div>
                             </div>
                             <div class="col-md-12">
                                 <div class="form-group row">
                                    <label class="col-md-4 col-form-label" required for="value">{_('Termination Date')}</label>
                                   <div class="col-md-8">
                                     <input id="termination_date" type="text" name="termination_date" class="form-control" required='true' value="{this.termination_date}">
                                 </div>
                                 </div>
                             </div>
                            <div class="col-md-12">
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
                                 <button id='save_edit_intermediary_agent' class="btn btn-primary">Save</button>
                                 <button class="btn btn-outline-primary intermediary_agent_edit_back">Cancel</button>
                             </div>
                         </div>
                     </div>
                 </div>
                 """
        javascript = """
                 <script>
                 setFormValidation('#form_edit_intermediary_agent');
                 $('#save_edit_intermediary_agent').click(function(){
                      var valid = FormIsValid("#form_edit_intermediary_agent");
                            if(valid){
                     var formserial = $('#form_edit_intermediary_agent').serialize();
                     $.post('/setup/save_edit_intermediary_agent?', formserial, function(data){

                         var result = JSON.parse(data);
                         if(result.success === true){
                            $('#dialog_edit_intermediary_agent').modal('hide');
                              var kwargs = { intermediary_id: result.intermediary_id};
                              $('#intermediary_agent_table').load('/setup/get_intemediary_agent_html?', kwargs, function(data){
                                 return false;
                            });
                         };
                         return false;
                     });
                     }
                 });
                 $('.intermediary_agent_edit_back').click(function(){
                     $('#dialog_edit_intermediary_agent').modal('hide');
                 });
                 $('#dialog_edit_intermediary_agent').modal();
                 </script>
                """
        return html + javascript

    @expose()
    def save_new_intermediary_agent(self, *args, **kwargs):

        intermediary_id = kwargs.get('intermediary_id')
        usernow = request.identity['user']
        this = EntityOrganisationIntermediaryAgent()
        this.entity_organisation_intermediary_id = intermediary_id
        this.entity_person_id = kwargs.get('entity_person_id', None)
        this.code = kwargs.get('code', None)
        this.termination_date = str_to_date(kwargs.get('termination_date', None))
        this.financial_regulatory_number =kwargs.get("financial_regulatory_number", None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()

        return json.dumps({'success': True, 'intermediary_id': intermediary_id})


    @expose()
    def save_edit_intermediary_agent(self, *args, **kwargs):

        usernow = request.identity['user']
        this = EntityOrganisationIntermediaryAgent.by_id(kwargs.get('intermediary_agent_id'))
        if not this: return ''
        this.entity_person_id = kwargs.get('entity_person_id', None)
        this.code = kwargs.get('code', None)
        this.termination_date = str_to_date(kwargs.get('termination_date', None))
        this.financial_regulatory_number = kwargs.get("financial_regulatory_number", None)
        if not kwargs.get('active', None): this.active = False
        DBSession.flush()

        return json.dumps({'success': True, 'intermediary_id': kwargs.get("intermediary_id")})

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
        district_id = kwargs.get("district_id", None) # To preselect if it exists
        region_id = kwargs.get("region_id")
        district_list = District.by_attr_all('region_id', region_id)
        kwargs['id'] = 'district_id'
        kwargs['selected'] = district_id if district_id else None # To pre select if it exists
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in district_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_center(self, *args, **kwargs):
        district_id = kwargs.get("district_id")
        center_list = Centre.by_attr_all('district_id', district_id)
        kwargs['id'] = 'centre_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in center_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_currency(self, *args, **kwargs):
        currecy_list = Currency.get_all('name')
        kwargs['id'] = 'currency_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in currecy_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_entity_organisation_type(self, selected= None, *args, **kwargs):
        kwargs['id'] = 'entity_organisation_type_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TYPEUTIL.get_dict_of_types("entity_organisation_type")
        return create_selectbox_html(**kwargs)

    def get_selectbox_bank(self, *args, **kwargs):
        bank_list = Bank.get_all('name')
        kwargs['id'] = 'bank_id'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in bank_list]
        return create_selectbox_html(**kwargs)

    @expose()
    def get_edit_intermediary_bank_html(self, intermediary_id=None, *args, **kwargs):

        intermediary = EntityOrganisationIntermediary.by_id(intermediary_id)
        entity_organisation = EntityOrganisation.by_id(intermediary.entity_organisation_id)
        entity_organisation_bank = EntityOrganisationBankAccountLink.by_attr_first("entity_organisation_id", entity_organisation.id)
        bank_vault = {}
        bank_id = None
        currency_id = None
        if entity_organisation_bank:
            bank_vault = vault.get_bankaccount_by_id(entity_organisation_bank.bank_account_id)
            if bank_vault:
                bank_id = bank_vault.get('id', None)
                currency_id = bank_vault.get('currency_id', None)

        dropdown_bank = self.get_selectbox_bank(**{'selected': bank_id})
        dropdown_currency = self.get_selectbox_currency(**{'selected': currency_id})
        html = f"""
        <div id="div_bank_html">     <div class="row">
                <div class="col-md-12">
                    <div class="card">
                        <div class="card-header">
                            <div class="row d-flex">
                                <div class="col-md-6">
                                    <h4 class="card-title">{_('Bank Details')}</h4>
                                </div>
    	                    <div class="col-md-6  text-right">
    							<button id='save_bank' intermediary_id ="{intermediary_id}" class="btn btn-primary">Save</button>
    						</div>
                            </div>
                            <hr>
                        </div>
                        <div class="card-body">
                            <form id="form_org_bank">
                                <input type="hidden" id="entity_organisation_id" name="entity_organisation_id" class="form-control" value="{entity_organisation.id}"/>

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
            </div></div>

              """
        return html

    def get_selectbox_bank_account(self, *args, **kwargs):
        kwargs['id'] = 'bank_account_type'
        kwargs['outputdict'] = TypeDict().get_dict_of_types("bank_account_type")
        return create_selectbox_html(**kwargs)

    def get_edit_intermediary_save_html(self, intermediary=None, *args, **kwargs):
        if not intermediary:
            return ''
        button_activate = f"""<button id='save_and_activate_intermediary' intermediary_id='{intermediary.id}' class="btn btn-primary" save_and_activate>Save & Activate</button>"""
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_intermediary' class="btn btn-primary">Save</button>
                        {button_activate}
                        <button class="btn btn-outline-primary intermediaries_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $(document).ready(function(){
                $('.intermediaries_back').click(function(){
                    $.redirect('/setup/intermediaries');
                });
                setFormValidation('#form_edit_intermediary');
                $('#save_and_activate_intermediary').click(function(){
                     var valid = FormIsValid("#form_edit_intermediary");
                     if(valid){
                        var formserial = getFormData('#form_edit_intermediary');
                        var data = {data : JSON.stringify(formserial)};

                        $.post('/setup/save_edit_intermediary?', data, function(data){
                            var result = JSON.parse(data);
                            if(result.success === true){
                                //$.redirect('/setup/intermediaries');
                            };
                            return false;
                        });
                     }
                });
            });
        </script>
        """
        return html + javascript


    @expose()
    def save_edit_entity_org_intermediary(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        this = EntityOrganisation.by_id(data.get('entity_organisation_id'))
        if not this: return ''
        this.code = data.get('code'),
        this.name = data.get('name', None)
        this.tax_number = data.get('tax_number', None)
        this.registration_number = data.get('registration_number', None)
        this.financial_regulatory_number = data.get('financial_regulatory_number', None)
        this.entity_organisation_type_id = data.get('entity_organisation_type_id', None)
        this.active = True
        DBSession.flush()
        return json.dumps({'success': True, 'intermediary_id':  data.get('intermediary_id', None)})


###############################################################################
# Banks
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def banks(self, *args, **kwargs):
        html = self.get_active_bank_html(*args, **kwargs)
        javascript = self.get_javascript_bank_onload()
        title = "Bank"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_bank_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_BANK
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        banktable=self.get_bank_htmltable(**kwargs)
        html = f"""
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Bank</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_bank" class="btn btn-primary ml-auto">Create a New Bank</button>
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
                        <div class="table-responsive" id='div_bank'>
                            {banktable}
                        </div>
                    </div>
                    </div>
                </div>
            """
        javascript = """
            <script>
            $("#create_new_bank").click(function(){
                $('#dialogdiv').load('/setup/get_modal_new_bank?', function(data){
                    return false;
                });
            });
                  $('#action_search').click(function(){
                     var kwargs = 'searchphrase='+$('#searchphrase').val();
                     $('#div_bank').load('/setup/get_bank_htmltable', kwargs, function(data){
                         return false;
                     });
                 })
                 $('#btn_reset').click(function(){
                  $('#searchphrase').val('').focus();
                     $('#div_bank').load('/setup/get_bank_htmltable', 'reset=true', function(data){
                         return false;
                     });
                 })
                 </script>
                 """
        return html +javascript
    @expose()
    def get_bank_htmltable(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_bank_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'name': "<div class='edit bank_edit action_link' bank_id='{1}'>{0}</div>".format(item.name, item.id),
            })
        dbcolumnlist = [
            'name',
        ]
        theadlist = [
            'Name',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "bank_table")
        javascript = """
            <script>
          $(".bank_edit").click(function(){
                var kwargs = 'bank_id='+$(this).attr('bank_id');
                $('#dialogdiv').load('/setup/get_modal_edit_bank?', kwargs, function(data){
                    return false;
                });
            });
             </script>
             """
        return  html + javascript

    @expose()
    def get_javascript_bank_onload(self, *args, **kwargs):
        javascript = """


            """
        return javascript

    @expose()
    def get_modal_new_bank(self, *args, **kwargs):
        html = f"""
            <div class="modal fade" id="dialog_new_bank" tabindex="-1" role="dialog" aria-labelledby="mybankLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('New Bank')}</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_bank'>
                                    <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-4 col-form-label" required for="name">Name</label>
    						<div class="col-md-8">
    							<input id="name" type="text" name="name" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_bank' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary bank_back">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_new_bank');
            $('#save_new_bank').click(function(){
                 var valid = FormIsValid("#form_new_bank");
                 if(valid){
                    var formserial = getFormData('#form_new_bank');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_new_bank?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/banks');
                        };
                        return false;
                    });
                 }
            });
            $('.bank_back').click(function(){
                $('#dialog_new_bank').modal('hide');
            });
            $('#dialog_new_bank').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def get_modal_edit_bank(self, *args, **kwargs):
        bank_id = kwargs.get('bank_id', None)
        if not bank_id: return ''
        this = self.get_bank_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
            <div class="modal fade" id="dialog_edit_bank" tabindex="-1" role="dialog" aria-labelledby="mybankLabel"
     aria-hidden="true">
    <div class="modal-dialog modal-dialog-centered modal-lg">
        <div class="modal-content">
            <div class="modal-header">
                <div class="col-md-6">
                    <h4 class="card-title">New Bank</h4>
                </div>
            </div>
            <div class="modal-body">
                <form id='form_edit_bank'>
                    <div style='display: none' class="col-md-6">
                        <div class="form-group row">
                            <label class="col-md-3 col-form-label" required for="bank_id">Id</label>
                            <div class="col-md-9">
                                <input id="id" type="text" name="bank_id" value="{this.id}" class="form-control"
                                       required='true'/>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-12">
                        <div class="form-group row">
                            <label class="col-md-4 col-form-label" required for="name"> Name</label>
                            <div class="col-md-8">
                                <input id="name" type="text" name="name" value="{this.name}" class="form-control"
                                       required='true'/>
                            </div>
                        </div>
                    </div>
                       <div class="col-md-12">
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
                <button id='save_edit_bank' class="btn btn-primary">Save</button>
                <button class="btn btn-outline-primary bank_back">Cancel</button>
            </div>
        </div>
    </div>
</div>
            """
        javascript = """
            <script>
            setFormValidation('#form_edit_bank');
            $('#save_edit_bank').click(function(){
                 var valid = FormIsValid("#form_edit_bank");
                 if(valid){
                    var formserial = getFormData('#form_edit_bank');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_edit_bank?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/banks');
                        };
                        return false;
                    });
                 }
            });
            $('.bank_back').click(function(){
                $('#dialog_edit_bank').modal('hide');
            });
            $('#dialog_edit_bank').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def save_new_bank(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = Bank()
        this.name = data.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_bank(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_bank_by_id(**data)
        if not this: return json.dumps({'success': False, 'data': 'No bank found for id provided'})
        this.name = data.get('name', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_bank_by_id(self, *args, **kwargs):
        return DBSession.query(Bank). \
            filter(Bank.id == kwargs.get('bank_id', None)). \
            first()

    @expose()
    def get_active_bank_list(self, *args, **kwargs):

        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_BANK
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()

        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(Bank). \
                filter(Bank.name.like(searchphrase)). \
                filter(Bank.active == 1). \
                order_by(asc(Bank.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(Bank). \
                filter(Bank.active == 1). \
                order_by(asc(Bank.id)). \
                limit(LIMIT)
        return dbase_query


###############################################################################
# Loaders Questions and Answers
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def loaders(self, *args, **kwargs):
        html = self.get_product_loaders_html(*args, **kwargs)
        javascript = self.get_javascript_product_loaders_onload()
        title = _("Product Loaders")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_product_loaders_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_PRODUCTLOADER
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        product_loader_table=self.get_product_loaders_htmltable(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Product Loaders')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_product_loader" class="btn btn-primary ml-auto">{_('New Product Loader')}</button>
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
                    <div class="table-responsive"  id='div_product_loader_table'>
                     {product_loader_table}
                    </div>
                </div>
                </div>
            </div>
        """
        javascript = """
          <script>
            $("#create_new_product_loader").click(function(){
                $('#dialogdiv').load('/setup/get_modal_new_product_loader?', function(data){
                    return false;
                });
            });
                $('#action_search').click(function(){
                   var kwargs = 'searchphrase='+$('#searchphrase').val();
                   $('#div_product_loader_table').load('/setup/get_product_loaders_htmltable', kwargs, function(data){
                       return false;
                   });
               })
               $('#btn_reset').click(function(){
                $('#searchphrase').val('').focus();
                   $('#div_product_loader_table').load('/setup/get_product_loaders_htmltable', 'reset=true', function(data){
                       return false;
                   });
               })
               </script>
               """
        return html +javascript

    @expose()
    def get_product_loaders_htmltable(self, *args, **kwargs):
        outputlist = []
        dbase_query = self.get_loader_questions_list(**kwargs)
        td = TypeDict()
        for item in dbase_query:
            loader_question_premium_effect_type = td.get_pretty_name('loader_question_premium_effect_type',
                                                                     item.loader_question_premium_effect_type_id)
            outputlist.append({
                'loader_name': f"<div class='edit loader_edit' loader_id='{item.id}'>{item.text}</div>",
                'is_active': item.active,
                'loader_question_premium_effect_type': loader_question_premium_effect_type
            })
        dbcolumnlist = [
            'loader_name',
            'loader_question_premium_effect_type',
            'is_active',
        ]
        theadlist = [
            'Loader Name',
            'Question Premium Effect Type',
            'Is Active',
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-right',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "loader_table", tdclasslist)
        javascript = """
          <script>
            $(".loader_edit").click(function(){
              var data = {loader_id : $(this).attr('loader_id')};
              $.redirect('/setup/get_loader_edit', data);
          });

            </script>
          """
        return  html +javascript

    @expose()
    def get_javascript_product_loaders_onload(self, *args, **kwargs):
        javascript = """

        """
        return javascript

    @expose()
    def get_modal_new_product_loader(self, *args, **kwargs):
        dropdown_question_premium_effect = self.get_selectbox_question_premium_effect()
        html = f"""
           <div class="modal fade" id="dialog_new_loader" tabindex="-1" role="dialog" aria-labelledby="myloaderLabel" aria-hidden="true">
               <div class="modal-dialog modal-dialog-centered modal-lg">
                   <div class="modal-content">
                       <div class="modal-header">
                           <div class="col-md-6">
                               <h4 class="card-title">New Loader</h4>
                           </div>
                       </div>
                       <div class="modal-body">
                           <form id='form_new_loader' class="d-flex flex-wrap">
                               <div class="col-md-12">
                                   <div class="form-group row">
                                       <label class="col-md-3 col-form-label" required for="loader_name">Loader Name</label>
                                       <div class="col-md-9">
                                           <input id="loader_name" type="text" name="loader_name" maxlength='100' class="form-control" required='true'>
                                       </div>
                                   </div>
                               </div>
                               <div class="col-md-12">
                                   <div class="form-group row">
                                       <label class="col-md-3 col-form-label" for="loader_question_premium_effect_type_id">{_('Question Premium Effect Type')}</label>
                                         <div class="col-md-9">
                                          {dropdown_question_premium_effect}
                                        </div>
                                   </div>
                               </div>
                           </form>
                       </div>
                       <div class="modal-footer">
                           <button id='save_new_loader' class="btn btn-primary">Save</button>
                       <button class="btn btn-outline-primary product_loader_back" data-dismiss="modal">Cancel</button>
                       </div>
                   </div>
               </div>
           </div>
           """
        javascript = """
       <script>
           setFormValidation('#form_new_loader');
            $('#save_new_loader').click(function(){
                 var valid = FormIsValid("#form_new_loader");
                 if(valid){
                    var formserial = $('#form_new_loader').serialize();
                    $.post('/setup/save_new_loader?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                          $.redirect(result.redirect, {'loader_id' : result.loader_id});
                        };
                        return false;
                    });
                 }
            });
           $('.product_loader_back').click(function(){
                $('#dialog_new_loader').modal('hide');
           });
           $('#dialog_new_loader').modal();
         </script>
        """
        return html + javascript
    @expose()
    def save_new_loader(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestion()
        this.text = kwargs.get('loader_name', None)
        this.loader_question_premium_effect_type_id = kwargs.get('loader_question_premium_effect_type_id')
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        redirect_url = '/setup/get_loader_edit'
        return json.dumps({'success' : True, 'loader_id' : this.id, 'redirect' : redirect_url})


    def get_selectbox_question_premium_effect(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'loader_question_premium_effect_type_id'
        kwargs['selected'] =selected
        kwargs['outputdict'] = TypeDict().get_dict_of_types("loader_question_premium_effect_type")
        return create_selectbox_html(**kwargs)

    @expose()
    def get_loader_questions_list(self, *args, **kwargs):
        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_PRODUCTLOADER
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()
        if searchphrase:
            searchphrase = f'%{searchphrase}%'
            dbase_query = DBSession.query(LoaderQuestion). \
                filter(or_(
                         LoaderQuestion.text.like(searchphrase),
                  )). \
                order_by(asc(LoaderQuestion.text)). \
                limit(LIMIT)
        else:
            dbase_query = DBSession.query(LoaderQuestion). \
                filter(LoaderQuestion.active == kwargs.get('active', True)). \
                order_by(asc(LoaderQuestion.text)). \
                limit(LIMIT)
        return dbase_query


    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def get_loader_edit(self, *args, **kwargs):

        loader_id = kwargs.get('loader_id', None)
        if not loader_id: redirect('/setup/loaders')
        html = self.get_edit_loader_html(*args, **kwargs)
        javascript = self.get_javascript_loader_onload()
        title = self.get_loader_title_html(loader_id)

        return dict(title=title, html=html, javascript=javascript)


    def get_loader_title_html(self, loader_id=None, *args, **kwargs):
        if not loader_id: return ''
        loader = LoaderQuestion.by_id(loader_id)
        if not loader: return ''
        return f"Edit: {loader.text}"


    @expose('rocket.templates.generic')
    def get_edit_loader_html(self, *args, **kwargs):
        loader_id = kwargs.get('loader_id', None)
        loader = LoaderQuestion.by_id(loader_id)
        checked = 'checked' if loader.active else ''
        td = TypeDict()
        dropdown_question_premium_effect = self.get_selectbox_question_premium_effect(loader.loader_question_premium_effect_type_id)
        selected_type = td.get_pretty_name('loader_question_premium_effect_type', loader.loader_question_premium_effect_type_id)
        detail_html = self.get_loader_question_answer_html(**kwargs)

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit '{loader.text}'</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back loader_back">Back to Loader List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_edit_loader' class="d-flex flex-wrap">
                            <div style='display: none' class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="loader_id">Id</label>
                                    <div class="col-md-9">
                                        <input id="id" type="text" name="loader_id" value="{loader.id}" class="form-control"
                                            required='true'>
                                      <input id="selected_type" type="text" name="selected_type" value="{selected_type}" class="form-control"
                                            required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-6 col-form-label" required for="loader_name">Loader Name</label>
                                    <div class="col-md-6">
                                        <input id="loader_name" type="text" maxlength='100' name="loader_name" value="{loader.text}"
                                            class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>

                           <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-6 col-form-label" required for="loader_question_premium_effect_type_id">Question Premium Effect Type</label>
                                    <div class="col-md-6">
                                        {dropdown_question_premium_effect}
                                    </div>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label">Active</label>
                                    <div class="form-check">
                                        <label class="form-check-label">
                                            <input class="form-check-input" type="checkbox" name='active' {checked}>
                                            <span class="form-check-sign"></span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                          </form>
                               <div class="col-md-12 text-right">
                              <button id='save_edit_loader' class="btn btn-primary">Save</button>
                            </div>
                    </div>
                </div>
            </div>
        </div>
          <div id="div_loader_detail" class="row">
             {detail_html}
          </div>
        </div>
        """
        javascript="""
        <script>
           $('.loader_back').click(function(){
                   $.redirect('/setup/loaders');
              });
        </script>
        """
        return html + javascript

    @expose()
    def get_loader_question_answer_html(self, *args, **kwargs):

        loader_id = kwargs.get('loader_id', None)
        outputlist = []
        loader_question =LoaderQuestion.by_id(loader_id)
        dbase_query = LoaderQuestionAnswer.by_attr_all('loader_question_id', loader_id)

        td = TypeDict()
        amount = td.get_id_of_name('loader_question_premium_effect_type', 'amount')
        percentage = td.get_id_of_name('loader_question_premium_effect_type', 'percentage')

        loader_type =loader_question.loader_question_premium_effect_type_id

        for item in dbase_query:
            value = None
            if loader_type == amount:
                this = LoaderQuestionAnswerAmount.by_attr_first('loader_question_answer_id', item.id)
                value = f"Amount:    {this.amount}"

            if loader_type == percentage:
                this = LoaderQuestionAnswerPercentage.by_attr_first('loader_question_answer_id', item.id)
                value = f"{this.percentage}%"

            outputlist.append({
                'answer_text': f"<div class='edit loader_question_answer_edit' loader_id='{loader_id}' loader_question_answer_id='{item.id}'>{item.answer_text}</div>",
                'value': value,
                'is_active': item.active,
            })

        dbcolumnlist = [
            'answer_text',
            'value',
            'is_active',
        ]
        theadlist = [
            'Answer',
            'Type',
            'Is Active',
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-right',
        ]
        loaderedit_table = build_html_table(outputlist, dbcolumnlist, theadlist, "loader_table", tdclasslist)
        html = f"""
               <div class="col-md-12">
        <div id="div_loader_question">
            <div class="card mh_260">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Loader Question List</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_loaderdetail" class="btn btn-primary ml-auto">New Question</button>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div style='display: none' class="col-md-12">
                        <div class="form-group row">
                            <label class="col-md-3 col-form-label" required for="loader_id">Id</label>
                            <div class="col-md-9">
                                <input id="loader_id" type="text" name="loader_id" value="{loader_id}" class="form-control" required='true'>
                            </div>
                        </div>
                    </div>
                    <div class="table-responsive">
                        {loaderedit_table}
                    </div>
                </div>
            </div>
            </div>
        </div>
           """
        javascript="""
        <script>
          $(".loader_question_answer_edit").click(function(){
                   var kwargs = {loader_question_answer_id : $(this).attr('loader_question_answer_id'), 'selected_type': $('#selected_type').attr('value'), 'loader_id': $(this).attr('loader_id')};
                  $('#dialogdiv').load('/setup/get_modal_edit_loader_question?', kwargs, function(data){
                 return false;
                   });
                 console.log(kwargs);
              });
                   $("#create_new_loaderdetail").click(function(){
                var kwargs = {'loader_id': $('#loader_id').attr('value'), 'selected_type': $('#selected_type').attr('value'),
                }
                $('#dialogdiv').load('/setup/get_modal_new_loader_question_answer?', kwargs, function(data){
                    return false;
                });
            });

              </script>
        """
        return html +javascript

    @expose()
    def get_modal_edit_loader_question(self, *args, **kwargs):
        loader_question_answer_id = kwargs.get('loader_question_answer_id', None)
        loader_type = kwargs.get('selected_type')
        loader_id =kwargs.get('loader_id')
        if not loader_question_answer_id: return ''
        this =  LoaderQuestionAnswer.by_id(loader_question_answer_id)
        if not this: return ''
        checked = 'checked' if this.active else ''

        type_fields = ''
        if loader_type == "Amount":
            loader_question_answer = LoaderQuestionAnswerAmount.by_attr_first('loader_question_answer_id', loader_question_answer_id)
            type_fields  = f"""
                  <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="amount">Amount</label>
						<div class="col-md-9">
							<input id="amount" type="text" name="number" class="form-control" required='true' value='{loader_question_answer.amount}'>
						</div>
					</div>
				</div>
                   """
        if loader_type == "Percentage":
            loader_question_percentage = LoaderQuestionAnswerPercentage.by_attr_first('loader_question_answer_id', loader_question_answer_id)
            type_fields = f"""
              <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="percentage">Percentage</label>
						<div class="col-md-9">
							<input id="percentage" type="number" name="percentage" class="form-control" required='true' value='{loader_question_percentage.percentage}'>
						</div>
					</div>
				</div>
                 """
        html = f"""
        <div class="modal fade" id="dialog_edit_loader_question" tabindex="-1" role="dialog" aria-labelledby="mytbl_loader_questionLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit Loader Answer</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                       <form id='form_edit_loader_question_answer'>
		                    <div style='display: none' class="col-md-6">
			<div class="form-group row">
				<label class="col-md-3 col-form-label" required for="loader_question_answer_id">Id</label>
				<div class="col-md-9">
					<input id="id" type="text" name="loader_question_answer_id" value="{this.id}" class="form-control" required='true'>
					<input id="loader_id" type="text" name="loader_id" value="{loader_id}" class="form-control" required='true'>
				</div>
			</div>
		 </div>
	                    	<div class="col-md-12">
			                    <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="answer_text">Answer Text</label>
		                    		<div class="col-md-9">
					              <input id="answer_text" type="text" name="answer_text" value="{this.answer_text}" class="form-control" required='true'>
			                	</div>
		                    	</div>
	                    	</div>
                          {type_fields}
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
                        <button id='save_edit_loader_question' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary loader_question_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_edit_loader_question_answer');
        $('#save_edit_loader_question').click(function(){
             var valid = FormIsValid("#form_edit_loader_question_answer");
             if(valid){
                var formserial = getFormData('#form_edit_loader_question_answer');
                $.post('/setup/save_edit_loaderdetails?', formserial, function(data){
                    var result = JSON.parse(data);

                    if(result.success === true){
                       $('#dialog_edit_loader_question').modal('hide');
                            $('#div_loader_question').load('/setup/get_loader_question_answer_html?', result, function(data){
                                 return false;
                            });

                    };
                    return false;
                });
             }
        });
        $('.loader_question_back').click(function(){
            $('#dialog_edit_loader_question').modal('hide');
        });
        $('#dialog_edit_loader_question').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_active_loader_question_list(self, *args, **kwargs):
        loader_question_id = kwargs.get('loader_id', None)

        if loader_question_id:
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
                filter(
                LoaderQuestionAnswer.loader_question_id == loader_question_id). \
                filter(LoaderQuestionAnswer.active == 1). \
                order_by(asc(LoaderQuestionAnswer.loader_question_id)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(LoaderQuestionAnswer). \
                filter(LoaderQuestionAnswer.active == 1). \
                order_by(asc(LoaderQuestionAnswer.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def get_javascript_loader_onload(self, *args, **kwargs):
        javascript = """
        $('#save_edit_loader').click(function(){
            var valid = FormIsValid("#form_edit_loader");
            if(valid){
                var formserial = $('#form_edit_loader').serialize();
                $.post('/setup/save_edit_loader_detail?', formserial, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect(result.redirect, {'loader_id' : result.loader_id});
                    };
                    return false;
                });
            }
        });
        """
        return javascript

    @expose()
    def get_modal_new_loader_question_answer(self, *args, **kwargs):
        loader_id = kwargs.get('loader_id', None)
        selected_type= kwargs.get('selected_type', None)
        input_field= selected_type.lower()
        html = f"""
        <div class="modal fade" id="dialog_new_loader_question_answer" tabindex="-1" role="dialog" aria-labelledby="myloaderdetailLabel"
            aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Loader Detail</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_loaderdetail'>
                            <div class="col-md-12 hidden">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="loader_id">Loader _Id</label>
                                    <div class="col-md-9">
                                        <input id="loader_id" type="text" name="loader_id" class="form-control" required='true' value='{loader_id}'>
                                        <input id="selected_type" type="text" name="selected_type" class="form-control" required='true' value='{selected_type}'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-12">
                                    <div class="form-group row">
                                      <label class="col-md-4 col-form-label" required for="answer_text">Answer</label>
                                      <div class="col-md-8">
                                         <input id="answer_text" type="text" name="answer_text" class="form-control" required='true'>
                                       </div>
                                    </div>
                             </div>
                               <div class="col-md-12">
                                    <div id="hide_field" >
                                      <div class="form-group row">
                                         <label class="col-md-4 col-form-label" for="">{selected_type}</label>
                                            <div class="col-md-8">
                                              <input id="{input_field}" type="text" name="{input_field}" class="form-control" required='true'>
                                            </div>
                                     </div>
                                    </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_loaderdetail' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary loader_question_answer_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        $(document).ready(function(){
            if($('#selected_type').attr('value') =='None')
            {
              $("#hide_field").hide();
            }
            setFormValidation('#form_new_loaderdetail');
            $('#save_new_loaderdetail').click(function(){
                 var valid = FormIsValid("#form_new_loaderdetail");
                 if(valid){
                    var formserial = $('#form_new_loaderdetail').serialize();
                    $.post('/setup/save_new_loaderdetails?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                           $.redirect(result.redirect, {'loader_id' : result.loader_id});
                        };
                        return false;
                    });
                 }
            });
            $('.loader_question_answer_back').click(function(){
                $('#dialog_new_loader_question_answer').modal('hide');
            });
            $('#dialog_new_loader_question_answer').modal();
        });
        </script>
     	"""
        return html + javascript


    @expose()
    def save_edit_loader_detail(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestion.by_id(kwargs.get('loader_id'))
        if not this: return ''
        this.text = kwargs.get('loader_name', None)
        this.loader_question_premium_effect_type_id = kwargs.get('loader_question_premium_effect_type_id')
        this.added_by = usernow.id
        DBSession.flush()
        redirect_url = '/setup/get_loader_edit'
        return json.dumps({'success' : True, 'loader_id' : kwargs.get('loader_id'), 'redirect' : redirect_url})

# New Questions
    @expose()
    def save_new_loaderdetails(self, *args, **kwargs):
        dict_loader_question_answer = {
            'loader_question_id': kwargs.get('loader_id'),
            'answer_text': kwargs.get("answer_text"),
        }
        loader_question_answer_id = self.save_new_loader_question_answer(**dict_loader_question_answer)

        percentage = kwargs.get('percentage', None)
        if percentage:
            dict_percentage = {
                'loader_question_answer_id' : loader_question_answer_id,
                'percentage' : kwargs.get('percentage'),
            }
            self.save_new_loader_question_answer_percentage(**dict_percentage)
        amount = kwargs.get('amount', None)
        if amount:
            dict_amount = {
                'loader_question_answer_id': loader_question_answer_id,
                'amount' : kwargs.get("amount"),
            }
            self.save_new_loader_question_answer_amount(**dict_amount)

        loader_id= kwargs.get("loader_id")
        redirect_url = '/setup/get_loader_edit'

        return json.dumps({'success' : True, 'loader_id' : loader_id, 'redirect' : redirect_url})

    @expose()
    def save_new_loader_question_answer(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestionAnswer()
        this.loader_question_id = kwargs.get('loader_question_id', None)
        this.answer_text = kwargs.get('answer_text', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_loader_question_answer_amount(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestionAnswerAmount()
        this.loader_question_answer_id = kwargs.get('loader_question_answer_id', None)
        this.amount = kwargs.get('amount', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id

    @expose()
    def save_new_loader_question_answer_percentage(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestionAnswerPercentage()
        this.loader_question_answer_id = kwargs.get('loader_question_answer_id', None)
        this.percentage = kwargs.get('percentage', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return this.id


 # Question Edits
    @expose()
    def save_edit_loaderdetails(self, *args, **kwargs):

        dict_loader_question_answer = {
            'loader_question_answer_id': kwargs.get('loader_question_answer_id'),
            'answer_text': kwargs.get("answer_text"),
            'active': kwargs.get("active")

        }
        self.save_edit_loader_question_answer(**dict_loader_question_answer)

        percentage = kwargs.get('percentage', None)
        if percentage:
            dict_percentage = {
                'loader_question_answer_id' : kwargs.get('loader_question_answer_id'),
                'percentage' : kwargs.get('percentage'),
                'active': kwargs.get("active")
            }
            self.save_edit_loader_question_answer_percentage(**dict_percentage)

        amount = kwargs.get('amount', None)
        if amount:
            dict_amount = {
                'loader_question_answer_id': kwargs.get('loader_question_answer_id'),
                'amount' : kwargs.get("amount"),
                'active' : kwargs.get("active")
            }
            self.save_edit_loader_question_answer_amount(**dict_amount)

        return json.dumps({'success' : True, 'loader_id': kwargs.get('loader_id')})

    @expose()
    def save_edit_loader_question_answer(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestionAnswer.by_id(kwargs.get('loader_question_answer_id'))
        if not this: return ''
        this.answer_text = kwargs.get('answer_text', None)
        this.added_by = usernow.id
        if not kwargs.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True})

    @expose()
    def save_edit_loader_question_answer_amount(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestionAnswerAmount.by_attr_first('loader_question_answer_id', kwargs.get('loader_question_answer_id'))
        if not this: return ''
        this.amount = kwargs.get('amount', None)
        this.added_by = usernow.id
        if not kwargs.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True })

    @expose()
    def save_edit_loader_question_answer_percentage(self, *args, **kwargs):
        usernow = request.identity['user']
        this = LoaderQuestionAnswerPercentage.by_attr_first('loader_question_answer_id', kwargs.get('loader_question_answer_id'))
        if not this: return ''
        this.percentage = kwargs.get('percentage', None)
        this.added_by = usernow.id
        if not kwargs.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True})


###############################################################################
# Premium Rates
###############################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def premium_rates(self, *args, **kwargs):
        html = self.get_product_premium_rate_html(*args, **kwargs)
        javascript = self.get_javascript_product_premium_rate_onload()
        title = "Product Premium Rate"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_product_premium_rate_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_PREMIUMRATE
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        product_premium_rate_table= self.get_product_premium_htmltable(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Product Premium Rates')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_product_premium_rate" class="btn btn-primary ml-auto">{_('Create New Product Premium Rate')}</button>
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
                    <div class="table-responsive" id='div_premium_rate'>
                        {product_premium_rate_table}
                    </div>
                </div>
                </div>
            </div>
        """
        javascript = """
         <script>
         $("#create_new_product_premium_rate").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_product_premium_rate?', function(data){
                return false;
            });
            });
               $('#action_search').click(function(){
                  var kwargs = 'searchphrase='+$('#searchphrase').val();
                  $('#div_premium_rate').load('/setup/get_product_premium_htmltable', kwargs, function(data){
                      return false;
                  });
              })
              $('#btn_reset').click(function(){
               $('#searchphrase').val('').focus();
                  $('#div_premium_rate').load('/setup/get_product_premium_htmltable', 'reset=true', function(data){
                      return false;
                  });
              })
              </script>
              """
        return html +javascript
    @expose()
    def get_product_premium_htmltable(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_product_premium_rate_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code': "<div class='edit product_premium_rate_edit' product_premium_rate_id='{1}'>{0}</div>".format(
                    item.code, item.id),
                'name': item.name,
                'base_value': item.base_value, })

        dbcolumnlist = [
            'code',
            'name',
            'base_value',
        ]
        theadlist = [
            'Code',
            'Name',
            'Base Value',
        ]
        tdclasslist = [
            'action_link',
            'text-right',
            'text-right',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "product_premium_rate_table", tdclasslist)
        javascript= """
        <script>
              $(".product_premium_rate_edit").click(function(){
            var data = {product_premium_rate_id : $(this).attr('product_premium_rate_id')};
            $.redirect('/setup/get_product_premium_edit', data);
        });
        </script>
        """
        return  html+ javascript

    @expose()
    def get_javascript_product_premium_rate_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript

    @expose()
    def get_modal_new_product_premium_rate(self, *args, **kwargs):
        html = """
        <div class="modal fade" id="dialog_new_product_premium_rate" tabindex="-1" role="dialog" aria-labelledby="myproduct_premium_rateLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">New Product Premium Rate</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_product_premium_rate'>
                                <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-4 col-form-label" required for="code">Code</label>
						<div class="col-md-8">
							<input id="code" type="text" name="code" class="form-control" required='true'>
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
						<label class="col-md-4 col-form-label" required for="base_value">Base Value</label>
						<div class="col-md-8">
							<input id="base_value" type="number" name="base_value" class="form-control" required='true'>
						</div>
					</div>
				</div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_product_premium_rate' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_premium_rate_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_new_product_premium_rate');
        $('#save_new_product_premium_rate').click(function(){
             var valid = FormIsValid("#form_new_product_premium_rate");
             if(valid){
                var formserial = $('#form_new_product_premium_rate').serialize();

                $.post('/setup/save_new_product_premium_rate?', formserial, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                      console.log(result);
                      $.redirect(result.redirect, {'product_premium_rate_id' : result.product_premium_rate_id});
                      };
                  return false;
                });
             }
        });
        $('.product_premium_rate_back').click(function(){
            $('#dialog_new_product_premium_rate').modal('hide');
        });
        $('#dialog_new_product_premium_rate').modal();
        </script>
     	"""
        return html + javascript


    @expose()
    def save_new_product_premium_rate(self, *args, **kwargs):
        if not kwargs: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = BenefitRateTable()
        this.code = kwargs.get('code', None)
        this.name = kwargs.get('name', None)
        this.base_value = kwargs.get('base_value', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()

        redirect_url = '/setup/get_product_premium_edit'
        return json.dumps({'success': True, 'product_premium_rate_id': this.id, 'redirect': redirect_url})

    @expose()
    def save_edit_product_premium_rate(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_product_premium_rate_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No product_premium_rate found for id provided'})
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        this.base_value = data.get('base_value', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

    @expose()
    def get_product_premium_rate_list(self, *args, **kwargs):
        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_PREMIUMRATE
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()
        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(BenefitRateTable). \
                filter(or_(
                BenefitRateTable.code.like(searchphrase),
                BenefitRateTable.name.like(searchphrase),
            )). \
                filter(BenefitRateTable.active == 1). \
                order_by(asc(BenefitRateTable.code)).limit(LIMIT)
            return dbase_query
        else:
            dbase_query = DBSession.query(BenefitRateTable). \
                filter(BenefitRateTable.active == 1). \
                order_by(asc(BenefitRateTable.id)). \
                limit(LIMIT)
        return dbase_query

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def get_product_premium_edit(self, *args, **kwargs):
        product_premium_rate_id = kwargs.get('product_premium_rate_id', None)
        if not product_premium_rate_id: redirect('/setup/premium_rates')
        html = self.get_edit_product_premium_rate_html(*args, **kwargs)
        javascript = self.get_javascript_product_premium_rate_edit_onload()
        title = self.get_product_premium_rate_title_html(product_premium_rate_id)

        return dict(title=title, html=html, javascript=javascript)

    def get_product_premium_rate_title_html(self, product_premium_rate_id=None, *args, **kwargs):
        if not product_premium_rate_id: return ''
        product_premium_rate = BenefitRateTable.by_id(product_premium_rate_id)
        if not product_premium_rate: return ''
        return f"Edit: {product_premium_rate.name}"

    @expose('rocket.templates.generic')
    def get_edit_product_premium_rate_html(self, *args, **kwargs):
        product_premium_rate_id = kwargs.get('product_premium_rate_id', None)
        product_premium_rate = BenefitRateTable.by_id(product_premium_rate_id)
        checked = 'checked' if product_premium_rate.active else ''

        product_premium_rate_line_item_table = self.get_premium_rate_line_item_html(**kwargs)

        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit '{product_premium_rate.name}'</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back product_premium_back">Back to Product Premium Rate List</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_edit_loader' class="d-flex flex-wrap">
                            <div style='display: none' class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="product_premium_rate_id">Id</label>
                                    <div class="col-md-9">
                                        <input id="product_premium_rate_id" type="text" name="product_premium_rate_id" value="{product_premium_rate.id}" class="form-control"
                                            required='true'>

                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-6 col-form-label" required for="name">{_('Product Premium Rate Name')}</label>
                                    <div class="col-md-6">
                                        <input id="name" type="text" maxlength='100' name="name" value="{product_premium_rate.name}"
                                            class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                             <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-6 col-form-label" required for="code">{_('Product Premium Rate Code')}</label>
                                    <div class="col-md-6">
                                        <input id="code" type="text" maxlength='100' name="code" value="{product_premium_rate.code}"
                                            class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-6 col-form-label" required for="base_value">{_('Base Value')}</label>
                                    <div class="col-md-6">
                                        <input id="base_value" type="number" maxlength='1000'  max="1000" name="base_value" value="{product_premium_rate.base_value}"
                                            class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>

                            <div class="col-md-6">
                                <div class="form-group row">
                                    <label class="col-md-6 col-form-label">Active</label>
                                    <div class="form-check">
                                        <label class="form-check-label">
                                            <input class="form-check-input" type="checkbox" name='active' {checked}>
                                            <span class="form-check-sign"></span>
                                        </label>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>

        {product_premium_rate_line_item_table}
        """
        javascript = """
         <script>
            $('.product_premium_back').click(function(){
                    $.redirect('/setup/premium_rates');
               });
         </script>
         """
        return html + javascript

    @expose()
    def get_premium_rate_line_item_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_premium_rate_line_item_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:

            gender = TYPEUTIL.get_pretty_name("person_gender_type", item.gender_id)
            outputlist.append({
                'gender' : f"<div class='edit product_premium_rate_line_item_edit' product_premium_rate_line_item_id='{item.id}'>{gender}</div>",
                'maximum_age' : item.maximum_age,
                'minimum_age' : item.minimum_age,
                'rate_factor' : item.rate_factor,
                             })
        dbcolumnlist=[
                'gender',
                'maximum_age',
                'minimum_age',
                'rate_factor',
                    ]
        theadlist=[
                'Gender',
                'Maximum Age',
                'Minimum Age',
                'Rate Factor',
                ]
        tdclasslist = [
            'action_link',
            '',
            '',
            'text-right',
        ]
        product_premium_rate_line_itemtable = build_html_table(outputlist, dbcolumnlist, theadlist, "product_premium_rate_line_item_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Product Premium Rate Line Item')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="create_new_product_premium_rate_line_item" class="btn btn-primary ml-auto">{_('New Product Premium Rate Line')}</button>
                        </div>
                    </div>

                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {product_premium_rate_line_itemtable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_premium_rate_line_item_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)
        product_premium_rate_id = kwargs.get('product_premium_rate_id', None)
        gender_id = kwargs.get('product_premium_rate_line_item_gender_id', None)
        maximum_age = kwargs.get('maximum_age', None)
        minimum_age = kwargs.get('minimum_age', None)
        rate_factor = kwargs.get('rate_factor', None)
        if searchphrase:
            dbase_query = DBSession.query(BenefitRateTableLineItem). \
		    filter(BenefitRateTableLineItem.product_premium_rate_id==product_premium_rate_id). \
                    filter(BenefitRateTableLineItem.active==1). \
		    order_by(asc(BenefitRateTableLineItem.product_premium_rate_id)). \
                    limit(LIMIT)
        else:
            dbase_query = DBSession.query(BenefitRateTableLineItem). \
		    filter(BenefitRateTableLineItem.product_premium_rate_id==product_premium_rate_id). \
                    filter(BenefitRateTableLineItem.active==1). \
		    order_by(asc(BenefitRateTableLineItem.product_premium_rate_id)). \
                    limit(LIMIT)
        return dbase_query

    @expose()
    def get_javascript_product_premium_rate_edit_onload(self, *args, **kwargs):
        javascript = """
      $("#create_new_product_premium_rate_line_item").click(function(){
       var kwargs = {'product_premium_rate_id': $('#product_premium_rate_id').attr('value')};

       $('#dialogdiv').load('/setup/get_modal_new_product_premium_rate_line_item?', kwargs, function(data){
          return false;
           });
        });


       $(".product_premium_rate_line_item_edit").click(function(){

          var data = {product_premium_rate_line_item_id : $(this).attr('product_premium_rate_line_item_id'), 'product_premium_rate_id': $('#product_premium_rate_id').attr('value')};
          console.log(data);
           $('#dialogdiv').load('/setup/get_modal_edit_product_premium_rate_line_item?', data, function(data){
             return false;
           });
        });
        //loader_back
        """
        return javascript

    @expose()
    def get_modal_new_product_premium_rate_line_item(self, *args, **kwargs):
        product_premium_rate_id = kwargs.get('product_premium_rate_id')
        dropdown_gender = self.get_selectbox_gender()
        html = f"""
            <div class="modal fade" id="dialog_new_product_premium_rate" tabindex="-1" role="dialog" aria-labelledby="myproduct_premium_rateLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-12">
                                <h4 class="card-title">New Product Premium Rate</h4>
                            </div>
                        </div>
                <div class="modal-body">
                 <form id='form_new_product_premium_rate_line_item'>
                     <div style='display: none' class="col-md-6">
                 <div class="form-group row">
                        <label class="col-md-3 col-form-label" required for="product_premium_rate_id">Id</label>
                         <div class="col-md-9">
                              <input id="product_premium_rate_id" type="text" name="product_premium_rate_id" value="{product_premium_rate_id}" class="form-control" required='true'>
                        </div>
                    </div>
                </div>
                   <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-6 col-form-label" required for="gender_id">Gender </label>
						<div class="col-md-6">
						{dropdown_gender}
						</div>
					</div>
				</div>
                 <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-6 col-form-label" required for="maximum_age">Maximum Age</label>
						<div class="col-md-6">
							<input id="maximum_age" type="number"  min="1"  name="maximum_age" class="form-control" required='true'>
						</div>
					</div>
				</div>
                    <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-6 col-form-label" required for="minimum_age">Minimum Age</label>
						<div class="col-md-6">
							<input id="minimum_age" type="number" name="minimum_age" class="form-control" required='true'>
						</div>
					</div>
				</div>
              <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-6 col-form-label" required for="rate_factor">Rate Factor</label>
						<div class="col-md-6">
							<input id="rate_factor" type="number" name="rate_factor" class="form-control" required='true'>
						</div>
					</div>
				 </div>
                        </form>
                        </div>
                        <div class="modal-footer">
                              <button id='save_new_product_premium_rate_line_item' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary product_premium_rate_line_item_back" data-dismiss="modal">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
              setFormValidation('#form_new_product_premium_rate_line_item');
              $('#save_new_product_premium_rate_line_item').click(function(){
                 var valid = FormIsValid("#form_new_product_premium_rate_line_item");
                 if(valid){
                    var formserial = $('#form_new_product_premium_rate_line_item').serialize();
                    $.post('/setup/save_new_product_premium_rate_line_item?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                           $.redirect(result.redirect, {'product_premium_rate_id' : result.product_premium_rate_id});
                        };
                        return false;
                    });
                 }
            });
           $('.product_premium_rate_line_item_back').click(function(){
               $('#dialog_new_product_premium_rate').modal('hide');
             });
             $('#dialog_new_product_premium_rate').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def get_modal_edit_product_premium_rate_line_item(self, *args, **kwargs):

        product_premium_rate_line_item_id= kwargs.get('product_premium_rate_line_item_id')
        product_premium_rate_id =kwargs.get('product_premium_rate_id')


        this = self.get_product_premium_rate_line_item_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        dropdown_gender = self.get_selectbox_gender(this.gender_id)
        html = f"""
                <div class="modal fade" id="dialog_edit_product_premium_rate_line" tabindex="-1" role="dialog" aria-labelledby="myproduct_premium_rateLabel" aria-hidden="true">
                    <div class="modal-dialog modal-dialog-centered modal-lg">
                        <div class="modal-content">
                            <div class="modal-header">
                                <div class="col-md-12">
                                    <h4 class="card-title">Edit</h4>
                                </div>
                            </div>
                    <div class="modal-body">
                         <form id='form_edit_product_premium_rate_line_item'>
                                <div style='display: none' class="col-md-6">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="tbl_product_premium_rate_line_item_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="product_premium_rate_line_item_id" value="{product_premium_rate_line_item_id}" class="form-control" required='true'>
							<input id="id" type="text" name="product_premium_rate_id" value="{product_premium_rate_id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-12">
					            <div class="form-group row">
					            	<label class="col-md-3 col-form-label" required for="gender_id">Gender</label>
					            	    <div class="col-md-9">
						                    {dropdown_gender}
					                	</div>
					                </div>
				                </div>
                                <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="maximum_age">Maximum Age</label>
						<div class="col-md-9">
							<input id="maximum_age" type="text" name="maximum_age" value="{this.maximum_age}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="minimum_age">Minimum Age</label>
						<div class="col-md-9">
							<input id="minimum_age" type="text" name="minimum_age" value="{this.minimum_age}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                                <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="rate_factor">Rate Factor</label>
						<div class="col-md-9">
							<input id="rate_factor" type="text" name="rate_factor" value="{this.rate_factor}" class="form-control" required='true'>
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
                                  <button id='save_edit_product_premium_rate_line_item' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary product_premium_rate_line_item_back" data-dismiss="modal">Cancel</button>
                            </div>
                        </div>
                    </div>
                </div>

                """
        javascript = """
                <script>
                  setFormValidation('#form_edit_product_premium_rate_line_item');
                  $('#save_edit_product_premium_rate_line_item').click(function(){
                     var valid = FormIsValid("#form_edit_product_premium_rate_line_item");
                     if(valid){
                        var formserial = $('#form_edit_product_premium_rate_line_item').serialize();

                        $.post('/setup/save_edit_product_premium_rate_line_item?', formserial, function(data){
                            var result = JSON.parse(data);
                            if(result.success === true){
                              $.redirect(result.redirect, {'product_premium_rate_id' : result.product_premium_rate_id});
                            };
                            return false;
                        });
                     }
                });
               $('.product_premium_rate_line_item_back').click(function(){
                   $('#dialog_edit_product_premium_rate_line').modal('hide');
                 });
                $('#dialog_edit_product_premium_rate_line').modal();
                </script>
             	"""
        return html + javascript

    @expose()
    def get_product_premium_rate_line_item_by_id(self, *args, **kwargs):
        return DBSession.query(BenefitRateTableLineItem). \
            filter(BenefitRateTableLineItem.id == kwargs.get('product_premium_rate_line_item_id', None)). \
            first()


    @expose()
    def save_new_product_premium_rate_line_item(self, *args, **kwargs):

        usernow = request.identity['user']
        this = BenefitRateTableLineItem()
        this.product_premium_rate_id = kwargs.get('product_premium_rate_id', None)
        this.gender_id = kwargs.get('gender_id', None)
        this.maximum_age = kwargs.get('maximum_age', None)
        this.minimum_age = kwargs.get('minimum_age', None)
        this.rate_factor = kwargs.get('rate_factor', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()

        product_premium_rate_id = kwargs.get("product_premium_rate_id")
        redirect_url = '/setup/get_product_premium_edit'

        return json.dumps({'success': True, 'product_premium_rate_id': product_premium_rate_id, 'redirect': redirect_url})

    @expose()
    def save_edit_product_premium_rate_line_item(self, *args, **kwargs):

        usernow = request.identity['user']
        this = self.get_product_premium_rate_line_item_by_id(**kwargs)
        if not this: return json.dumps({'success' : False})

        this.gender_id = kwargs.get('gender_id', None)
        this.maximum_age = kwargs.get('maximum_age', None)
        this.minimum_age = kwargs.get('minimum_age', None)
        this.rate_factor = kwargs.get('rate_factor', None)
        if not kwargs.get('active', None): this.active = False
        DBSession.flush()


        product_premium_rate_id = kwargs.get("product_premium_rate_id")


        redirect_url = '/setup/get_product_premium_edit'
        return json.dumps({'success': True, 'product_premium_rate_id': product_premium_rate_id, 'redirect': redirect_url})


    def get_selectbox_gender(self, selected=None, *args, **kwargs):
        kwargs['id'] = 'gender_id'
        kwargs['selected'] = selected
        kwargs['outputdict'] = TypeDict().get_dict_of_types("person_gender_type")
        return create_selectbox_html(**kwargs)

    @expose()
    def get_product_premium_rate_by_id(self, *args, **kwargs):
        return DBSession.query(BenefitRateTable). \
            filter(BenefitRateTable.id == kwargs.get('product_premium_rate_id', None)). \
            first()

###############################################################################
# Product Cover Exclusion
###############################################################################
    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def cover_exclusions(self, *args, **kwargs):
        html = self.get_active_cover_exclusions_html(*args, **kwargs)
        javascript = self.get_javascript_cover_exclusions_onload()
        title = _("Cover & Exclusions")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_cover_exclusions_html(self, *args, **kwargs):
        detailtable= self.get_cover_and_exclusion_html(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Cover & Exclusions')}</h4>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    {detailtable}
                </div>
            </div>
        </div>
        """
        return html

    @expose()
    def get_javascript_cover_exclusions_onload(self, *args, **kwargs):
        javascript = """
        checkboxCheckOptions('.product_benefit_exclusion', 'cover_and_exclusion_type_id', '/setup/save_new_product_benefit_exclusion_link?', '/setup/save_delete_product_benefit_exclusion_link?');
        checkboxCheckOptions('.benefit_cover', 'cover_and_exclusion_type_id', '/setup/save_new_benefit_cover_link?', '/setup/save_delete_benefit_cover_link?');
        checkboxCheckOptions('.cover', 'cover_and_exclusion_type_id', '/setup/save_new_cover_link?', '/setup/save_delete_cover_link?');
        """
        return javascript

    @expose()
    def get_cover_and_exclusion_html(self, *args, **kwargs):
        usernow = request.identity['user']
        td = TypeDict()
        dbase_query = td.get_dict_of_types('cover_and_exclusion_type')

        #Product Benefit Cover Link
        cover_and_exclusion_list = BenefitCoverLink.get_all('cover_and_exclusion_type_id')
        cover_and_exclusion_link = [int(x.cover_and_exclusion_type_id) for x in cover_and_exclusion_list]

        #Product Benefit Exclusion Link
        product_benefit_exclusion_list = BenefitExclusionLink.get_all('cover_and_exclusion_type_id')
        product_benefit_exclusion_link = [int(x.cover_and_exclusion_type_id) for x in product_benefit_exclusion_list]


        #Product Cover Link
        benefit_cover_list = BenefitCoverLink.get_all('cover_and_exclusion_type_id')
        benefit_cover_link = [int(x.cover_and_exclusion_type_id) for x in benefit_cover_list]

        outputlist = []
        for id, name in dbase_query.items():

            pretty_name = td.get_pretty_name('cover_and_exclusion_type', id)

            checked_benefit_cover = ''
            checked_benefit_exclusion=''
            checked_benefit_cover=''
            if id in cover_and_exclusion_link:
                checked_benefit_cover = "checked"
            if id in product_benefit_exclusion_link:
                checked_benefit_exclusion = "checked"
            if id in benefit_cover_link:
                checked_benefit_cover = "checked"

            outputlist.append({
                'name': f"<div class='edit product_premium_rate_edit' cover_and_exclusion_id='{id}'>{pretty_name}</div>",
                'benefit_cover': f"""<input class="form-check-input benefit_cover" cover_and_exclusion_type_id='{id}' name="is_benefit_cover" id="is_benefit_cover" type="checkbox" {checked_benefit_cover}>""",
                'cover':   f"""<input class="form-check-input cover" cover_and_exclusion_type_id='{id}' name="is_benefit_cover" id="is_benefit_cover" type="checkbox" {checked_benefit_cover}>""",
                'product_benefit_exclusion':  f"""<input class="form-check-input product_benefit_exclusion" cover_and_exclusion_type_id='{id}' name="is_benefit_exclusion" id="is_benefit_exclusion" type="checkbox" {checked_benefit_exclusion}>""",
            })
        theadlist = [
            'Name',
            'Product Cover',
            'Benefit Cover',
            'Benefit Exclusion'
        ]
        dbcolumnlist = [
            'name',
            'benefit_cover',
            'cover',
            'product_benefit_exclusion'
        ]
        tdclasslist = [
            'action_link',
            'text-center',
            'text-center',
            'text-center',
        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "entity_table", tdclasslist)

    @expose()
    def save_delete_cover_link(self, *args, **kwargs):
        usernow = request.identity['user']
        this = DBSession.query(BenefitCoverLink). \
                filter(BenefitCoverLink.cover_and_exclusion_type_id==kwargs.get('cover_and_exclusion_type_id', None)). \
                first()
        DBSession.delete(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_new_cover_link(self, *args, **kwargs):
        usernow = request.identity['user']
        this = BenefitCoverLink()
        this.cover_and_exclusion_type_id = kwargs.get('cover_and_exclusion_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_delete_benefit_cover_link(self, *args, **kwargs):
        usernow = request.identity['user']
        this = DBSession.query(BenefitCoverLink). \
            filter(BenefitCoverLink.cover_and_exclusion_type_id == kwargs.get(
            'cover_and_exclusion_type_id', None)). \
            first()
        DBSession.delete(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_new_benefit_cover_link(self, *args, **kwargs):
        usernow = request.identity['user']
        this = BenefitCoverLink()
        this.cover_and_exclusion_type_id = kwargs.get('cover_and_exclusion_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_new_product_benefit_exclusion_link(self, *args, **kwargs):
        usernow = request.identity['user']
        this = BenefitExclusionLink()
        this.cover_and_exclusion_type_id = kwargs.get('cover_and_exclusion_type_id', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return 'true'

    @expose()
    def save_delete_product_benefit_exclusion_link(self, *args, **kwargs):
        usernow = request.identity['user']
        this = DBSession.query(BenefitExclusionLink). \
            filter(BenefitExclusionLink.cover_and_exclusion_type_id == kwargs.get(
            'cover_and_exclusion_type_id', None)). \
            first()
        DBSession.delete(this)
        DBSession.flush()
        return 'true'

#######################################################################
# Mail Merge
#######################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def mail_merge(self, *args, **kwargs):
        html = self.get_active_mail_merge_html(*args, **kwargs)
        javascript = self.get_javascript_mail_merge_onload()
        title = _("Mail Merge")
        return dict(title=title, html=html, javascript=javascript)


    @expose()
    def get_javascript_mail_merge_onload(self, *args, **kwargs):
        javascript = """
        $("#create_new_mail_merge").click(function(){
            $('#dialogdiv').load('/setup/get_modal_new_mail_merge?', function(data){
                return false;
            });
        });
        exportFile('#download_mail_merge', '/setup/download_mail_merge', focus=true);
        $(".mail_merge_edit").click(function(){
            var kwargs = 'mail_merge_id='+$(this).attr('mail_merge_id');
            $('#dialogdiv').load('/setup/get_modal_edit_mail_merge?', kwargs, function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def download_mail_merge(self, *args, **kwargs):
        datenow = datetime.date(datetime.now())
        pdf_file_name = f"Mail Merge {datenow}.pdf"
        output_pdf_filepath = os.path.join(PDF_DIRNAME, pdf_file_name)
        pdffile = PDFCreator(**{'filename': output_pdf_filepath})
        headers = [
            'Code',
            'Name'
        ]
        headerwidths = [
            200,
            200,
        ]
        outputlist = []
        dbase_query = MailMerge.get_all('name')
        for item in dbase_query:
            outputlist.append((
                Paragraph(checknullvalue(item.code), pdffile.styleNormal),
                Paragraph(checknullvalue(item.name), pdffile.styleNormal),
            ))
        userdata = {
            'header': 'Mail Merge',
            'right1_header': 'Date Printed', 'right1_content': str(datenow),
        }
        pdffile.CreatePDF_Table_Portrait(userdata, outputlist, headers, headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+pdf_file_name+'"'
        filecontent = FileApp(output_pdf_filepath)
        return use_wsgi_app(filecontent)

    @expose()
    def get_active_mail_merge_html(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_mail_merge_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'code' : "<div class='edit mail_merge_edit' mail_merge_id='{1}'>{0}</div>".format(item.code, item.id),
                'name' : item.name,
                             })
        dbcolumnlist=[
                'code',
                'name',
                    ]
        theadlist=[
                'Code',
                'Name',
                ]
        tdclasslist = [
            'action_link',
            'text-right',
        ]

        mail_mergetable = build_html_table(outputlist, dbcolumnlist, theadlist, "mail_merge_table", tdclasslist)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Mail Merge')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="download_mail_merge" class="btn btn-secondary ml-auto">Download Mail Merge</button>
                            <button id="create_new_mail_merge" class="btn btn-primary ml-auto">Create New Mail Merge</button>
                        </div>
                    </div>

                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {mail_mergetable}
                    </div>
                </div>
                </div>
            </div>
        """
        return html

    @expose()
    def get_modal_new_mail_merge(self, *args, **kwargs):
        html = f"""
            <div class="modal fade" id="dialog_new_mail_merge" tabindex="-1" role="dialog" aria-labelledby="mytbl_mail_mergeLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">{_('New Mail Merge')}</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_mail_merge'>
                                    <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="code">{_('Code')}</label>
    						<div class="col-md-9">
    							<input id="code" type="text" name="code" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                                    <div class="col-md-12">
    					<div class="form-group row">
    						<label class="col-md-3 col-form-label" required for="name">{_('Name')}</label>
    						<div class="col-md-9">
    							<input id="name" type="text" name="name" class="form-control" required='true'>
    						</div>
    					</div>
    				</div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_mail_merge' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary mail_merge_back">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_new_mail_merge');
            $('#save_new_mail_merge').click(function(){
                 var valid = FormIsValid("#form_new_mail_merge");
                 if(valid){

                   var formserial = $('#form_new_mail_merge').serialize();
                    $.post('/setup/save_new_mail_merge?', formserial, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                           location.reload();
                        };
                        return false;
                    });
                 }
            });
            $('.mail_merge_back').click(function(){
                $('#dialog_new_mail_merge').modal('hide');
            });
            $('#dialog_new_mail_merge').modal();
            </script>
         	"""
        return html + javascript

    # @expose()
    # def get_modal_edit_tbl_mail_merge(self, *args, **kwargs):
    #     mail_merge_id = kwargs.get('mail_merge_id', None)
    #     if not mail_merge_id: return ''
    #     this = self.get_mail_merge_by_id(*args, **kwargs)
    #     if not this: return ''
    #     checked = 'checked' if this.active else ''
    #     html = f"""
    #         <div class="modal fade" id="dialog_edit_tbl_mail_merge" tabindex="-1" role="dialog" aria-labelledby="mytbl_mail_mergeLabel" aria-hidden="true">
    #             <div class="modal-dialog modal-dialog-centered modal-lg">
    #                 <div class="modal-content">
    #                     <div class="modal-header">
    #                         <div class="col-md-6">
    #                             <h4 class="card-title">New Tbl_mail_merge</h4>
    #                         </div>
    #                     </div>
    #                     <div class="modal-body">
    #                         <form id='form_edit_tbl_mail_merge'>
    #                             <div style='display: none' class="col-md-6">
    # 					<div class="form-group row">
    # 						<label class="col-md-3 col-form-label" required for="tbl_mail_merge_id">Id</label>
    # 						<div class="col-md-9">
    # 							<input id="id" type="text" name="tbl_mail_merge_id" value="{this.id}" class="form-control" required='true'>
    # 						</div>
    # 					</div>
    # 				</div>
    #                             <div class="col-md-6">
    # 					<div class="form-group row">
    # 						<label class="col-md-3 col-form-label" required for="code">Code</label>
    # 						<div class="col-md-9">
    # 							<input id="code" type="text" name="code" value="{this.code}" class="form-control" required='true'>
    # 						</div>
    # 					</div>
    # 				</div>
    #                             <div class="col-md-6">
    # 					<div class="form-group row">
    # 						<label class="col-md-3 col-form-label" required for="name">Name</label>
    # 						<div class="col-md-9">
    # 							<input id="name" type="text" name="name" value="{this.name}" class="form-control" required='true'>
    # 						</div>
    # 					</div>
    # 				</div>
    #                             <div class="form-group row">
    #                               <label class="col-4 col-form-label" for="active" required>Active</label>
    #                               <div class="col-8"><div class="form-check">
    #                                 <input class="form-check-input" type="checkbox" name="active" id="active" {checked}/></div>
    #                               </div>
    #                             </div>
    #                         </form>
    #                     </div>
    #                     <div class="modal-footer">
    #                         <button id='save_edit_tbl_mail_merge' class="btn btn-primary">Save</button>
    #                         <button class="btn btn-outline-primary tbl_mail_merge_back">Cancel</button>
    #                     </div>
    #                 </div>
    #             </div>
    #         </div>
    #         """
    #     javascript = """
    #         <script>
    #         setFormValidation('#form_edit_tbl_mail_merge');
    #         $('#save_edit_tbl_mail_merge').click(function(){
    #              var valid = FormIsValid("#form_edit_mail_merge");
    #              if(valid){
    #                 var formserial = getFormData('#form_edit_mail_merge');
    #                 var data = {data : JSON.stringify(formserial)};
    #
    #                 $.post('/setup/mail_merge?', data, function(data){
    #                     var result = JSON.parse(data);
    #                     if(result.success === true){
    #                         $.redirect('/setup /save_edit_mail_merge');
    #                     };
    #                     return false;
    #                 });
    #              }
    #         });
    #         $('.tbl_mail_merge_back').click(function(){
    #             $('#dialog_edit_tbl_mail_merge').modal('hide');
    #         });
    #         $('#dialog_edit_tbl_mail_merge').modal();
    #         </script>
    #      	"""
    #     return html + javascript
    @expose()
    def get_modal_edit_mail_merge(self, *args, **kwargs):
        mail_merge_id = kwargs.get('mail_merge_id', None)
        if not mail_merge_id: return ''
        this = self.get_mail_merge_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
        <div class="modal fade" id="dialog_edit_mail_merge" tabindex="-1" role="dialog" aria-labelledby="mytbl_mail_mergeLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Edit Mail Merge')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_mail_merge'>
                            <div style='display: none' class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="mail_merge_id">Id</label>
						<div class="col-md-9">
							<input id="id" type="text" name="mail_merge_id" value="{this.id}" class="form-control" required='true'>
						</div>
					</div>
				</div>
                            <div class="col-md-12">
					<div class="form-group row">
						<label class="col-md-3 col-form-label" required for="code">Code</label>
						<div class="col-md-9">
							<input id="code" type="text" name="code" value="{this.code}" class="form-control" required='true'>
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
                        <button id='save_edit_mail_merge' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary mail_merge_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        setFormValidation('#form_edit_mail_merge');
        $('#save_edit_mail_merge').click(function(){
             var valid = FormIsValid("#form_edit_mail_merge");
             if(valid){
                var formserial = getFormData('#form_edit_mail_merge');
                var data = {data : JSON.stringify(formserial)};

                $.post('/setup/save_edit_mail_merge?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){

                          $.redirect('/setup/mail_merge', data);
                    };
                    return false;
                });
             }
        });
        $('.mail_merge_back').click(function(){
            $('#dialog_edit_mail_merge').modal('hide');
        });
        $('#dialog_edit_mail_merge').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def save_new_mail_merge(self, *args, **kwargs):
        usernow = request.identity['user']
        this = MailMerge()
        this.code = kwargs.get('code', None)
        this.name = kwargs.get('name', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True})


    @expose()
    def get_mail_merge_by_id(self, *args, **kwargs):
        return DBSession.query(MailMerge). \
            filter(MailMerge.id==kwargs.get('mail_merge_id', None)). \
            first()

    @expose()
    def get_active_mail_merge_list(self, *args, **kwargs):
        searchphrase = kwargs.get('searchphrase', None)

        code = kwargs.get('code', None)
        name = kwargs.get('name', None)

        if code:
            searchphrase = "%"+kwargs['code']+"%"
            dbase_query = DBSession.query(MailMerge). \
			filter(MailMerge.code.like(searchphrase)). \
                        filter(MailMerge.active==1). \
			order_by(asc(MailMerge.code)).limit(LIMIT)
        if name:
            searchphrase = "%"+kwargs['name']+"%"
            dbase_query = DBSession.query(MailMerge). \
			filter(MailMerge.name.like(searchphrase)). \
                        filter(MailMerge.active==1). \
			order_by(asc(MailMerge.name)).limit(LIMIT)
        else:
            dbase_query = DBSession.query(MailMerge). \
                filter(MailMerge.active==1). \
                order_by(asc(MailMerge.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def save_edit_mail_merge(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False, 'data' : 'No data provided'})
        usernow = request.identity['user']
        this = self.get_mail_merge_by_id(**data)
        if not this: return json.dumps({'success' : False, 'data' : 'No text merge found for id provided'})
        this.code = data.get('code', None)
        this.name = data.get('name', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success' : True, 'data' : this.id})

#######################################################################
# Disclosure
#######################################################################

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def intermediary_disclosure(self, *args, **kwargs):
        html = self.get_active_intermediary_disclosure_html(*args, **kwargs)
        javascript = self.get_javascript_intermediary_disclosure_onload()
        title = "Disclosure"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_intermediary_disclosure_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY_INTERMEDIARYDISCLOSURE
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        intermediary_disclosuretable = self.get_intermediary_disclosure_htmltable(**kwargs)
        html = f"""
            <div class="row">
                <div class="col-md-12">
                    <div class="card">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Disclosure</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button id="create_new_intermediary_disclosure" class="btn btn-primary ml-auto">Create a New Disclosure</button>
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
                        <div class="table-responsive" id='div_intermediary_disclosure'>
                            {intermediary_disclosuretable}
                        </div>
                    </div>
                    </div>
                </div>
            """
        javascript = """
           <script>
                 $("#create_new_intermediary_disclosure").click(function(){
                $('#dialogdiv').load('/setup/get_modal_new_intermediary_disclosure?', function(data){
                    return false;
                });
            });
                 $('#action_search').click(function(){
                    var kwargs = 'searchphrase='+$('#searchphrase').val();
                    $('#div_intermediary_disclosure').load('/setup/get_intermediary_disclosure_htmltable', kwargs, function(data){
                        return false;
                    });
                })
                $('#btn_reset').click(function(){
                 $('#searchphrase').val('').focus();
                    $('#div_intermediary_disclosure').load('/setup/get_intermediary_disclosure_htmltable', 'reset=true', function(data){
                        return false;
                    });
                })
                </script>
                """
        return html + javascript
    @expose()
    def get_intermediary_disclosure_htmltable(self, *args, **kwargs):
        usernow = request.identity['user']
        dbase_query = self.get_active_intermediary_disclosure_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'text': "<div class='edit intermediary_disclosure_edit action_link' intermediary_disclosure_id='{1}'>{0}</div>".format(
                    item.text, item.id),
            })
        dbcolumnlist = [
            'text',
        ]
        theadlist = [
            'Text',
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "intermediary_disclosure_table")
        javascript = """
           <script>
              $(".intermediary_disclosure_edit").click(function(){
                  var kwargs = 'intermediary_disclosure_id='+$(this).attr('intermediary_disclosure_id');
                  $('#dialogdiv').load('/setup/get_modal_edit_intermediary_disclosure?', kwargs, function(data){
                      return false;
                  });
              });
            </script>
              """
        return  html+ javascript

    @expose()
    def get_javascript_intermediary_disclosure_onload(self, *args, **kwargs):
        javascript = """


            """
        return javascript

    @expose()
    def get_modal_new_intermediary_disclosure(self, *args, **kwargs):
        html = """
            <div class="modal fade" id="dialog_new_intermediary_disclosure" tabindex="-1" role="dialog" aria-labelledby="myintermediary_disclosureLabel" aria-hidden="true">
                <div class="modal-dialog modal-dialog-centered modal-lg">
                    <div class="modal-content">
                        <div class="modal-header">
                            <div class="col-md-6">
                                <h4 class="card-title">New Disclosure</h4>
                            </div>
                        </div>
                        <div class="modal-body">
                            <form id='form_new_intermediary_disclosure'>
                           <div class="col-md-12">
    					        <div class="form-group row">
    						        <label class="col-md-4 col-form-label" required for="text">Text</label>
    						        <div class="col-md-8">
    						           <textarea required="true" name='text' type="text" class="form-control" rows="3" maxlength='1024'></textarea>
    						       </div>
    					</div>
    				</div>
                            </form>
                        </div>
                        <div class="modal-footer">
                            <button id='save_new_intermediary_disclosure' class="btn btn-primary">Save</button>
                            <button class="btn btn-outline-primary intermediary_disclosure_back">Cancel</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_new_intermediary_disclosure');
            $('#save_new_intermediary_disclosure').click(function(){
                 var valid = FormIsValid("#form_new_intermediary_disclosure");
                 if(valid){
                    var formserial = getFormData('#form_new_intermediary_disclosure');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_new_intermediary_disclosure?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/intermediary_disclosure');
                        };
                        return false;
                    });
                 }
            });
            $('.intermediary_disclosure_back').click(function(){
                $('#dialog_new_intermediary_disclosure').modal('hide');
            });
            $('#dialog_new_intermediary_disclosure').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def get_modal_edit_intermediary_disclosure(self, *args, **kwargs):
        intermediary_disclosure_id = kwargs.get('intermediary_disclosure_id', None)
        if not intermediary_disclosure_id: return ''
        this = self.get_intermediary_disclosure_by_id(*args, **kwargs)
        if not this: return ''
        checked = 'checked' if this.active else ''
        html = f"""
            <div class="modal fade" id="dialog_edit_intermediary_disclosure" tabindex="-1" role="dialog"
         aria-labelledby="myintermediary_disclosureLabel" aria-hidden="true">
        <div class="modal-dialog modal-dialog-centered modal-lg">
            <div class="modal-content">
                <div class="modal-header">
                    <div class="col-md-6">
                        <h4 class="card-title">Edit Disclosure</h4>
                    </div>
                </div>
                <div class="modal-body">
                    <form id='form_edit_intermediary_disclosure'>
                        <div style='display: none' class="col-md-6">
                            <div class="form-group row">
                                <label class="col-md-3 col-form-label" required for="intermediary_disclosure_id">Id</label>
                                <div class="col-md-9">
                                    <input id="id" type="text" name="intermediary_disclosure_id" value="{this.id}"
                                           class="form-control" required='true'/>
                                </div>
                            </div>
                        </div>
                        <div class="col-md-12">
                            <div class="form-group row">
                                <label class="col-md-4 col-form-label" required for="text"> Text</label>
                                <div class="col-md-8">
                                    <textarea required="true" name='text' type="text" class="form-control" rows="3" maxlength='1024'>{this.text}</textarea>
                                </div>
                            </div>
                        </div>
                       <div class="col-md-12">
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
                    <button id='save_edit_intermediary_disclosure' class="btn btn-primary">Save</button>
                    <button class="btn btn-outline-primary intermediary_disclosure_back">Cancel</button>
                </div>
            </div>
        </div>
    </div>
            """
        javascript = """
            <script>
            setFormValidation('#form_edit_intermediary_disclosure');
            $('#save_edit_intermediary_disclosure').click(function(){
                 var valid = FormIsValid("#form_edit_intermediary_disclosure");
                 if(valid){
                    var formserial = getFormData('#form_edit_intermediary_disclosure');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/setup/save_edit_intermediary_disclosure?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $.redirect('/setup/intermediary_disclosure');
                        };
                        return false;
                    });
                 }
            });
            $('.intermediary_disclosure_back').click(function(){
                $('#dialog_edit_intermediary_disclosure').modal('hide');
            });
            $('#dialog_edit_intermediary_disclosure').modal();
            </script>
         	"""
        return html + javascript

    @expose()
    def save_new_intermediary_disclosure(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = EntityOrganisationIntermediaryDisclosure()
        this.text = data.get('text', None)
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def save_edit_intermediary_disclosure(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False, 'data': 'No data provided'})
        usernow = request.identity['user']
        this = self.get_intermediary_disclosure_by_id(**data)
        if not this: return json.dumps(
            {'success': False, 'data': 'No intermediary_disclosure found for id provided'})
        this.text = data.get('text', None)
        if not data.get('active', None): this.active = False
        DBSession.flush()
        return json.dumps({'success': True, 'data': this.id})

    @expose()
    def get_intermediary_disclosure_by_id(self, *args, **kwargs):
        return DBSession.query(EntityOrganisationIntermediaryDisclosure). \
            filter(EntityOrganisationIntermediaryDisclosure.id == kwargs.get('intermediary_disclosure_id', None)). \
            first()

    @expose()
    def get_active_intermediary_disclosure_list(self, *args, **kwargs):
        usernow = request.identity.get('user')
        kwargs['searchkey'] = SEARCHKEY_INTERMEDIARYDISCLOSURE
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()
        if searchphrase:
            searchphrase = "%" + searchphrase + "%"
            dbase_query = DBSession.query(EntityOrganisationIntermediaryDisclosure). \
                filter(EntityOrganisationIntermediaryDisclosure.text.like(searchphrase)). \
                filter(EntityOrganisationIntermediaryDisclosure.active == 1). \
                order_by(asc(EntityOrganisationIntermediaryDisclosure.text)).limit(LIMIT)
            return  dbase_query
        else:
            dbase_query = DBSession.query(EntityOrganisationIntermediaryDisclosure). \
                filter(EntityOrganisationIntermediaryDisclosure.active == 1). \
                order_by(asc(EntityOrganisationIntermediaryDisclosure.id)). \
                limit(LIMIT)
        return dbase_query

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def password_test(self, *args, **kwargs):
        html = self.get_password_test(*args, **kwargs)
        javascript = self.get_javascript_password_test()
        title = "Password Test"
        return dict(title=title, html=html, javascript=javascript)
    @expose()
    def get_password_test(self, *args, **kwargs):
        html = f"""
             <div class="card">
			<div class="card-header">
				<div class="row d-flex">
					<div class="col-md-6">
						<h4 class="card-title">Password Test </h4>
					</div>

				</div>
	<div class="row d-flex">
			<div class="col-md-12">
				<hr>
				<div class="col-md-12">
<form  id="form" >
						<div class="form-group">
							<label for="desc">Password:</label>
							<input type="password" class="form-control" name="pass" id="pass" required>
						</div>
                         <span id="result"></span>
                            <div class="form-group">
						<div class="form-group">
							<label for="desc">Confirm Password:</label>
							<input type="password" class="form-control pass" name="confpass" id="confpass" required>
						</div>
						<div class="form-group">
							<span class="error" style="color:red"></span><br />
						</div>

					</form>
		<button id='login_test' class="btn btn-primary">Save</button>

				</div>


			</div>
		</div>
			</div>
		</div>
                """
        return  html

    def get_javascript_password_test(self, *args, **kwargs):
        javascript ="""
        var allowsubmit = false;
		$(function(){
			$('#confpass').keyup(function(e){
				var pass = $('#pass').val();
				var confpass = $(this).val();
				if(pass == confpass){
					$('.error').text('');
					allowsubmit = true;
				}else{
					$('.error').text('Password not matching');
					allowsubmit = false;
				}
			});
			$('#pass').keyup(function(e){
			 var pass = $('#pass').val();
                 if(pass.match(/[A-Z]/g)) {
                       console.log("Upper case");
                       	allowsubmit = true;
                 }
                 if(pass.match(/[a-z]/g)) {
                       console.log("Small letters");
                       	allowsubmit = true;
             }
             if(pass.match(/[0-9]/g)) {
                     console.log("Number");
            	allowsubmit = true;
             }
            if(pass.match(/([!, %, &, @, #, $, ^, *, ?, _, ~])/)) {
                console.log("Special Character avalaible");
             	allowsubmit = true;
             }
             if(pass.length >= 10){
              console.log("10 and more ");
              allowsubmit = true;
             }else {console.log("Password less than 10 minimum character");
              	allowsubmit = false;
              	}

			});

			   $('#login_test').click(function(){
				var pass = $('#pass').val();
				var confpass = $('#confpass').val();

				if(pass == confpass){
				allowsubmit = true;
				}
				if(allowsubmit){
					console.log(pass);
					return true;
				}else{
					return false;
				}
			});
		});
        """
        return javascript
