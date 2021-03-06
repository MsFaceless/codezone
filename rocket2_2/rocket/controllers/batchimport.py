# -*- coding: utf-8 -*-
"""BatchImportController controller module"""

import os, json
from webob.static import FileApp
from datetime import datetime
from pkg_resources import resource_filename
from rocket.lib.type_utils import TypeDictionary

from tg import expose, require, redirect, validate, flash, url, request, response
from tg import predicates, use_wsgi_app

from rocket.model import *

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController
from rocket.lib.tgfileuploader import FileUploader
from rocket.lib.tg_generic_reportlab import PDFCreator, Paragraph

from rocket.lib.old_batchimport import *
#from rocket.lib.member_import import MemberImport

from rocket.controllers.common import CommonController
from rocket.controllers.product import ProductController

from sqlalchemy import func, desc, asc, or_

FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
EXCEL_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'excel')
IMAGES_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'images')
CATALOG_DIRNAME = os.path.join(IMAGES_DIRNAME, 'catalog_pictures')

LIMIT = 20
TYPEUTIL = TypeDictionary()
MINS_TO_WAIT_FOR_IMPORT_CONTINUE = 30
SEARCHKEY = 'BatchImport_SearchKeyword'

COMMON = CommonController()
PRODUCTCONT = ProductController()

__all__ = ['BatchImportController']

class BatchImportController(BaseController):
    """Docstring for batchimport."""

    allow_only = predicates.has_any_permission('Administrator', 'Membership')

    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_active_batchimport_html(*args, **kwargs)
        javascript = self.get_javascript_batchimport_onload()
        title = "Batch Import"
        kwargs = {
            'import_type_id' : 3,
            #'filename' : 'small_purchase.xlsx',
            #'filename' : 'small.xlsx',
        }
        #result = PurchaseImport(**kwargs).start_import()
        #result = MemberImport(**kwargs).start_import()
        #print(result)
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_batchimport_htmltbl(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        outputlist = []
        dbase_query = self.get_active_batchimport_list(**kwargs)
        for item in dbase_query:
            group_name = ''
            #rocket_group = GroupRocket.by_id(**{'id' : item.group_id})
            #if rocket_group:
            #    group_name = None
            #reject_html = f"<div class='batchimport_error action_link' batch_import_id='{item.id}'>{item.rejected_count}</div>" if item.rejected_count > 0 else item.rejected_count

            '''
            if item.total_count == (item.accepted_count + item.rejected_count):
                continue_html = "<img src='/images/icon_check.png' alt='Complete' title='Batch Import Complete'/>"
            else:
                #too_soon = item.added > add_minutes_to_date(datetime.now(), -MINS_TO_WAIT_FOR_IMPORT_CONTINUE)
                too_soon = True
                if not item.active: continue_html = "<img src='/images/icon_check.png' alt='Complete' title='Batch Import Complete'/>"
                elif item.active and not too_soon: continue_html = f"<div class='batchimport_continue action_link' batch_import_id='{item.id}'>Continue</div>"
                else: continue_html = f""" <div class="fa-1x"> <i class="text-dark fas fa-spinner fa-pulse"></i> </div> """
            '''
            continue_html = "<img src='/images/icon_check.png' alt='Complete' title='Batch Import Complete'/>"

            reject_html = item.rejected_count
            import_type = TYPEUTIL.get_name('batch_import_type', item.import_type_id)
            if not import_type: import_type = ""
            #continue_html = f"<div class='batchimport_continue action_link' batch_import_id='{item.id}'>Continue</div>"
            outputlist.append({
                'id' : f"<div class='batchimport_audit' batch_import_id='{item.id}'>{item.id}</div>",
                #'import_type_id' : get_name_from_id(ImportType, item.import_type_id),
                'import_type_id' : import_type.capitalize(),
                'group_id' : group_name,
                #'processed' : item.processed,
                'total_count' : item.total_count,
                'accepted_count' : item.accepted_count,
                #'pre_purchase_count' : item.pre_purchase_count,
                'rejected_count' : reject_html,
                'notes' : item.notes,
                'empty' : continue_html,
                             })
        dbcolumnlist=[
                'id',
                'import_type_id',
                'group_id',
                #'processed',
                'total_count',
                'accepted_count',
                #'pre_purchase_count',
                'rejected_count',
                'notes',
                'empty',
                    ]
        theadlist=[
                '',
                'Import Type',
                'Group',
                #'Processed',
                'Total',
                'Accepted',
                #'Pre-Purchase',
                'Rejected',
                'Notes',
                '',
                ]
        tdclasslist = [
                'action_link',
                '',
                '',
                #'',
                '',
                '',
                #'',
                '',
                '',
                'text-right',
                ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "batchimport_table", tdclasslist)
        javascript = """
        <script>
            $(".batchimport_audit").click(function(){
                var kwargs = 'batch_import_id='+$(this).attr('batch_import_id');
                $('#dialogdiv').load('/batchimport/get_modal_audit_batchimport?', kwargs, function(data){
                    return false;
                });
            });
            $(".batchimport_error").click(function(){
                var kwargs = {batch_import_id: $(this).attr('batch_import_id')};
                $.redirect('/batchimport/errors', kwargs);
            });
            $(".batchimport_continue").click(function(){
                $(this).html('<div class="fa-1x"> <i class="text-dark fas fa-spinner fa-pulse"></i> </div>');
                var kwargs = 'batch_import_id='+$(this).attr('batch_import_id');
                $.post('/batchimport/restart_batch_import?', kwargs, function(data){
                    return false;
                });
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_import_stats(self):
        returnable = ""
        if hasattr(self, 'running_import'):
            running_import = getattr(self, 'running_import')
            if running_import:
                if running_import.complete:
                    self.running_import = False
                    return returnable
            if running_import:
                if not running_import.complete: returnable = f"""
                <div>
                    <span>{self.running_import.import_type_name} Import Running</span>
                    <span class='ml-3'>Currently at Step: {self.running_import.import_status}</span>
                </div>
                <div>
                    <span class='ml-3'>Accepted: {self.running_import.accepted}</span>
                    <span class='ml-3'>Rejected: {self.running_import.rejected}</span>
                    <span class='ml-3'>Total: {self.running_import.total}</span>
                </div>
                    <script type='text/javascript'>
                        function refreshImportStats(){{
                            $('#import_stats').load('/batchimport/get_import_stats?', function(){{
                                return false
                            }});
                        }};
                        setTimeout(refreshImportStats, 1000);
                    </script>
                        """
        return returnable

    @expose()
    def get_active_batchimport_html(self, *args, **kwargs):
        print()
        kwargs['searchkey'] = SEARCHKEY
        usernow = request.identity.get('user', {})
        searchphrase = COMMON.get_searchphrase(**kwargs)
        batchimporttable = self.get_batchimport_htmltbl(**kwargs)
        import_stats = self.get_import_stats()
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Batch Import</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="refresh" class="btn btn-danger ml-auto">Refresh</button>
                            <button id="download_template" class="btn btn-primary ml-auto" data-toggle="modal">Download Template</button>
                            <button id="create_new_batchimport" class="btn btn-primary ml-auto" data-toggle="modal">Create New Batch Import</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">

                        <div class="col-md-6 d-flex">
                            <div class="col-md-8">
                                <input id='search' type="text" class="form-control search" name="searchphrase" placeholder="Search by Import Type or Group" value='{searchphrase}'>
                            </div>
                            <div class="col">
                                <button id='btn_search' class="btn btn-primary action_search">Search</button>
                                <button id='btn_reset' class="btn btn-primary">Reset</button>
                            </div>
                        </div>

                        <div class="col-md-6 d-flex text-right">
                            <div id="import_stats">
                                {import_stats}
                            </div>
                        </div>

                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div id='div_batchimport_table' class="table-responsive">
                        {batchimporttable}
                    </div>
                </div>
                </div>
            </div>
            <div id='dialogdiv'></div>
        """
        return html

    @expose()
    def get_javascript_batchimport_onload(self, *args, **kwargs):
        javascript = """
        $("#refresh").click(function(){
            location.reload();
        });
        $("#download_template").click(function(){
            $('#dialogdiv').load('/batchimport/get_modal_download_template?', function(data){
                return false;
            });
        });
        $("#create_new_batchimport").click(function(){
            $('#dialogdiv').load('/batchimport/get_modal_new_batch_import?', function(data){
                return false;
            });
        });
        $('#btn_search').click(function(){
            var kwargs = 'searchphrase='+$('#search').val();
            $('#div_batchimport_table').load('/batchimport/get_batchimport_htmltbl', kwargs, function(data){
                return false;
            });
        });
        $('#btn_reset').click(function(){
            $('#search').val('').focus();
            $('#div_batchimport_table').load('/batchimport/get_batchimport_htmltbl', 'reset=true', function(data){
                return false;
            });
        });
        """
        return javascript

    @expose()
    def get_modal_download_template(self, *args, **kwargs):
        selectbox_importtypes = self.get_selectbox_import_type(**{'id': 'import_type_id', 'required': True})
        html = f"""
        <div class="modal fade" id="dialog_new_member_import" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">Download Template</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                            <i class="now-ui-icons ui-1_simple-remove"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id='new_member_import'>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Template Type</label>
                                        <div class="col-md-9">
                                            {selectbox_importtypes}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='btn_start_download' class="btn btn-primary">Download</button>
                        <button class="btn btn-outline-primary members_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $("#btn_start_download").click(function(){
                var selected = $('#import_type_id option:selected').val();
                var href_with_formserial = '/batchimport/download_template?import_type_id=' + selected;
                window.location = href_with_formserial
            });
            $('.members_back').click(function(){
                $('#dialog_new_member_import').modal('hide');
            });
            $('#dialog_new_member_import').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_modal_new_batch_import(self, *args, **kwargs):
        selectbox_importtypes = self.get_selectbox_import_type(**{'id': 'import_type_id', 'required': True})
        html = f"""
        <div class="modal fade" id="dialog_new_batch_import" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <h4 class="modal-title">New Batch Import</h4>
                        <button type="button" class="close" data-dismiss="modal" aria-hidden="true">
                            <i class="now-ui-icons ui-1_simple-remove"></i>
                        </button>
                    </div>
                    <div class="modal-body">
                        <form id='new_batch_import'>
                            <div class="row">
                                <div class="col-md-12">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Import Type</label>
                                        <div class="col-md-9">
                                            {selectbox_importtypes}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div id="div_product_selectbox" class="row">
                            </div>
                        </form>
                        <div class="row">
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <div class='dropzone' id='dropzone_batch_import'></div>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button id='btn_start_import' class="btn btn-primary">Import</button>
                        <button class="btn btn-outline-primary batches_back" data-dismiss="modal">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            $(document).ready(function(){
                $('#import_type_id').change(function(){
                    var import_type_id = $('#import_type_id option:selected').val();
                    if(import_type_id){
                        var kwargs = 'import_type_id='+import_type_id;
                        $('#div_product_selectbox').load('/batchimport/get_batch_import_product_owner_selectbox_html?', kwargs, function(data){
                            return false;
                        });
                    }else{
                        $('#div_product_selectbox').empty();
                    };
                });

                setFormValidation('#new_batch_import');
                var batchDropzone = new Dropzone('#dropzone_batch_import', {
                    maxFiles: 1,
                    maxFilesize: 256,
                    parallelUploads: 1,
                    uploadMultiple: false,
                    autoProcessQueue: false,
                    acceptedFiles: '.xls, .xlsx, .ods',
                    url: '/batchimport/handle_file_upload',
                    params: {
                        // To pass extra keys into the uploader
                    },
                    success: function(file, response){
                        var result = JSON.parse(response);
                        if(result.success === true){
                            var product_owner_id = $('#product_owner_id option:selected').val();
                            var formserial = 'import_type_id='+$('#import_type_id option:selected').val();
                            formserial += '&filename='+result.name;
                            formserial += product_owner_id ? '&product_owner_id='+product_owner_id : '';
                            $.post('/batchimport/start_new_batch_import?'+formserial, function(data){
                                return false;
                            });
                            setTimeout(function(){
                                $('#dialog_new_batch_import').modal('hide');
                                $.redirect('/batchimport/index');
                            }, 1000);
                        };
                    },
                });
                $("#btn_start_import").click(function(){
                    var valid = FormIsValid('#new_batch_import');
                    if(valid){
                        batchDropzone.processQueue();
                    };
                });
                $('.batches_back').click(function(){
                    $('#dialog_new_batch_import').modal('hide');
                });
                $('#dialog_new_batch_import').modal();
            });
        </script>
        """
        return html + javascript

    @expose()
    def get_batch_import_product_owner_selectbox_html(self, *args, **kwargs):
        import_type_id = str_to_int(kwargs.get('import_type_id', None))
        purchase = TYPEUTIL.get_id_of_name('batch_import_type', 'purchase')
        if not import_type_id == purchase: return ''
        selectbox = PRODUCTCONT.get_selectbox_product_owner(**{'id' : 'product_owner_id'})
        return f"""
        <div class="col-md-12">
            <div class="form-group row">
                <label class="col-md-3 col-form-label" required>Product Owner</label>
                <div class="col-md-9">
                    {selectbox}
                </div>
            </div>
        </div>
        """

    @expose()
    def get_batch_import_audit_table(self, *args, **kwargs):
        dbase_query = self.get_active_batchimportaudit_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'audit_date_time' : item.audit_date_time,
                'audit' : item.audit,
                             })
        dbcolumnlist=[
                'audit_date_time',
                'audit',
                    ]
        theadlist=[
                'Date',
                'Audit',
                ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "batchimportaudit_table")

    @expose()
    def get_batch_import_info_html(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        batchimport = self.get_batchimport_by_id(**kwargs)
        img_active = "<span class='now-ui-icons ui-1_check text-green font-weight-bold'>"
        img_inactive = "<span class='now-ui-icons ui-1_simple-remove text-red font-weight-bold'>"
        #is_complete_load = img_active if batchimport.is_complete_load else img_inactive
        #is_complete_update = img_active if batchimport.is_complete_update else img_inactive
        is_complete_load = img_active
        is_complete_update = img_active
        import_type = TYPEUTIL.get_pretty_name('import_type', batchimport.import_type_id)
        #rocket = GroupRocket.by_id(**{'id' : batchimport.group_id})
        #group_name = group.get('name') if group else ''
        group_name = ""
        html = f"""
        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Type</label>
            <span class='font-italic'>{import_type}</span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Created</label>
            <span class='font-italic'>{batchimport.added}</span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Group</label>
            <span class='font-italic'>{group_name}</span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Accepted</label>
            <span class='font-italic'>{batchimport.accepted_count}</span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Total</label>
            <span class='font-italic'>{batchimport.total_count}</span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Rejected</label>
            <span class='font-italic'>{batchimport.rejected_count}</span>
        </div>

        <!--
        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Pre Purchased</label>
            <span class='font-italic'>pre purchase</span>
        </div>
        -->

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Printed</label>
            <span class='font-italic'></span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Captured</label>
            <span class='font-italic'>{usernow.name}</span>
        </div>

        <div class="row col-md-6">
            <label class="col-md-6 col-form-label">Printed By</label>
            <span class='font-italic'>{usernow.name}</span>
        </div>

        <div class="row col-md-6 d-flex align-items-center">
            <label class="col-md-6 col-form-label">Load Complete?</label>
            {is_complete_load}
        </div>

        <div class="row col-md-6 d-flex align-items-center">
            <label class="col-md-6 col-form-label">Update Complete?</label>
            {is_complete_update}
        </div>

        <div class="row col-md-12">
            <label class="col-md-3 col-form-label">File Name</label>
            <span class='font-italic'>{batchimport.filename}</span>
        </div>

        """
        return html

    @expose()
    def get_modal_audit_batchimport(self, *args, **kwargs):
        batch_import_id = kwargs.get('batch_import_id', None)
        if not batch_import_id: return ''
        batch_import_info = self.get_batch_import_info_html(**kwargs)
        batch_import_audit_table = self.get_batch_import_audit_table(**kwargs)
        html = f"""
        <div class="modal fade" id="dialog_audit_batchimport" tabindex="-1" role="dialog" aria-labelledby="mybatchimportLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered modal-lg">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-6">
                            <h4 class="card-title">Batch Import Audit Log</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <div class="row col-md-12 d-flex f">
                            {batch_import_info}
                        </div>
                        <div id='div_audit_table row col-md-12'>
                            {batch_import_audit_table}
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button class="btn btn-outline-primary batchimport_back" data-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <style>
            #div_audit_table {
                max-height: 300px;
                overflow-y: auto;
            };
        </style>
        <script>
        $('.batchimport_back').click(function(){
            $('#dialog_audit_batchimport').modal('hide');
        });
        $('#dialog_audit_batchimport').modal();
        </script>
     	"""
        return html + javascript

    @expose()
    def get_batch_import_error_table(self, *args, **kwargs):
        dbase_query = self.get_active_batchimporterror_list(*args, **kwargs)
        outputlist = []
        for item in dbase_query:
            outputlist.append({
                'added' : item.added,
                'message' : item.message,
                             })
            #outputlist.append({
            #    'added' : item.added,
            #    'idnumber' : '',
            #    'member' : '',
            #    'description' : '',
            #    'price' : '',
            #    'payment' : '',
            #    'message' : item.message,
            #                 })
        dbcolumnlist=[
                'added',
                'message',
                    ]
        #dbcolumnlist=[
        #        'added',
        #        'idnumber',
        #        'member',
        #        'description',
        #        'price',
        #        'payment',
        #        'message',
        #            ]
        theadlist=[
                'Date',
                'Error',
                ]
        #theadlist=[
        #        'Date',
        #        'ID Number',
        #        'Member',
        #        'Description',
        #        'Price',
        #        'Payment',
        #        'Error',
        #        ]
        return build_html_table(outputlist, dbcolumnlist, theadlist, "batchimporterror_table")

    @expose('rocket.templates.generic')
    def errors(self, *args, **kwargs):
        batch_import_id = kwargs.get('batch_import_id', None)
        if not batch_import_id: redirect('/batchimport/index')
        batch_import_error_table = self.get_batch_import_error_table(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Batch Import Errors</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn btn-primary batchimport_back">Back to Batch Imports</button>
                            <button class="btn btn-primary">Export to Excel</button>
                        </div>
                    </div>
                </div>
                <div class="card-body">
                    <div id='div_error_table' class="table-responsive">
                        {batch_import_error_table}
                    </div>
                </div>
                </div>
            </div>
            <style>
                #div_error_table {{
                    max-height: 550px;
                    overflow-y: auto;
                }};
            </style>
        """
        javascript = """
        $('.batchimport_back').click(function(){
            $.redirect('/batchimport/index');
        });
     	"""
        title = "Batch Import Errors"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_batchimport_by_id(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        return DBSession.query(BatchImport). \
            filter(BatchImport.id==kwargs.get('batch_import_id', None)). \
            first()

    @expose()
    def get_active_batchimport_list(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['searchkey'] = SEARCHKEY
        searchphrase = COMMON.get_searchphrase(**kwargs).lower()
        if searchphrase:
            kwargs['searchphrase'] = searchphrase
            groupidlist = []
            importtypelist = [x.value for x in ImportType if searchphrase in str(x.name).lower()]
            dbase_query = DBSession.query(BatchImport). \
                filter(or_(
                    BatchImport.import_type_id.in_(importtypelist),
                    BatchImport.group_id.in_(groupidlist),
                )). \
                order_by(desc(BatchImport.id)). \
                limit(LIMIT)
        else:
            dbase_query = DBSession.query(BatchImport). \
                order_by(desc(BatchImport.id)). \
                limit(LIMIT)
        return dbase_query

    def get_selectbox_import_type(self, *args, **kwargs):
        import_type_list = []
        import_type_list = [record for record in BatchImportType.get_all('id') if record.name.lower() != 'default']
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in import_type_list]
        return create_selectbox_html(**kwargs)

    def get_selectbox_import_type(self, *args, **kwargs):
        import_type_list = []
        import_type_list = [record for record in BatchImportType.get_all('id') if record.name.lower() != 'default']
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in import_type_list]
        return create_selectbox_html(**kwargs)

    @expose()
    def handle_file_upload(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        kwargs['user_id'] = usernow.id
        kwargs['upload_dir'] = EXCEL_DIRNAME
        kwargs['size_limit'] = 256000000 # 256 MB
        kwargs['allowed_extensions'] = ['.xls', '.xlsx', '.ods']
        uploader = FileUploader(**kwargs)
        return uploader.handle_file_upload()

    @expose()
    def start_new_batch_import(self, *args, **kwargs):
        import_type = str_to_int(kwargs.get('import_type_id', None))
        if not import_type: return ''
        filename = kwargs.get('filename', None)
        if not filename: return ''
        member = TYPEUTIL.get_id_of_name('batch_import_type', 'member')
        family = TYPEUTIL.get_id_of_name('batch_import_type', 'family')
        purchase = TYPEUTIL.get_id_of_name('batch_import_type', 'purchase')
        usernow = request.identity.get('user', {})
        if import_type == member:
            return MemberImport(**kwargs).start_import()

        if import_type == purchase:
            return PurchaseImport(**kwargs).start_import()

        return ''

        if hasattr(self, 'running_import'): return "Already Importing"
        import_type = str_to_int(kwargs.get('import_type_id', None))
        if not import_type: return ''
        filename = kwargs.get('filename', None)
        if not filename: return ''
        member = TYPEUTIL.get_id_of_name('batch_import_type', 'member')
        family = TYPEUTIL.get_id_of_name('batch_import_type', 'family')
        purchase = TYPEUTIL.get_id_of_name('batch_import_type', 'purchase')
        usernow = request.identity.get('user', {})
        if import_type == member:
            kwargs['import_type_id'] = member
            kwargs['user_id'] = usernow.id
            kwargs['session'] = DBSession
            kwargs['language_id'] = 1
            kwargs['language_type_id'] = 1
            member_import = MemberImport(kwargs)
            self.running_import = member_import
            member_import.start_import()
            #CallToBatchImport(filename, import_type).run_batch_import()
        if import_type == family:
            print('Placeholder start the family import')
        if import_type == purchase:
            print('Placeholder start the purchase import')
        return ''

    @expose()
    def download_template(self, *args, **kwargs):
        import_type_id = str_to_int(kwargs.get('import_type_id', None))
        if not import_type_id: return ''
        member = TYPEUTIL.get_id_of_name('batch_import_type', 'member')
        family = TYPEUTIL.get_id_of_name('batch_import_type', 'family')
        purchase = TYPEUTIL.get_id_of_name('batch_import_type', 'purchase')
        if import_type_id  == member: filename = 'Member Import Template.xlsx'
        elif import_type_id == purchase: filename = 'Policy Import Template.xlsx'
        elif import_type_id == family: filename = 'Family Import Template.xlsx'
        else: filename = None
        filepath = os.path.join(EXCEL_DIRNAME, str(filename))
        if not os.path.exists(filepath): return ''
        response.headers["Content-Type"] = 'application/vnd.ms-excel'
        response.headers["Content-Disposition"] = 'attachment; filename="'+filename+'"'
        filecontent = FileApp(filepath)
        return use_wsgi_app(filecontent)

    @expose()
    def get_active_batchimportaudit_list(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        searchphrase = kwargs.get('searchphrase', None)
        batch_import_id = kwargs.get('batch_import_id', None)
        if searchphrase:
            dbase_query = DBSession.query(BatchImportAudit). \
                filter(BatchImportAudit.audit.like(searchphrase)). \
                order_by(asc(BatchImportAudit.audit)). \
                limit(LIMIT)
        elif batch_import_id:
            dbase_query = DBSession.query(BatchImportAudit). \
                filter(BatchImportAudit.batch_import_id==batch_import_id). \
                order_by(desc(BatchImportAudit.id)). \
                all()
        else:
            dbase_query = DBSession.query(BatchImportAudit). \
                order_by(asc(BatchImportAudit.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def get_active_batchimporterror_list(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        batch_import_id = kwargs.get('batch_import_id', None)
        if batch_import_id:
            dbase_query = DBSession.query(BatchImportError). \
                filter(BatchImportError.batch_import_id==batch_import_id). \
                order_by(desc(BatchImportError.id)). \
                all()
        else:
            dbase_query = DBSession.query(BatchImportError). \
                order_by(asc(BatchImportError.id)). \
                limit(LIMIT)
        return dbase_query

    @expose()
    def restart_batch_import(self, *args, **kwargs):
        batch_import_id = str_to_int(kwargs.get('batch_import_id', None))
        import_type = str_to_int(kwargs.get('import_type_id', None))
        if not batch_import_id: return ''
        batchimport = BatchImport.by_id(batch_import_id)
        if not batchimport: return ''
        if batchimport.import_type_id == ImportType.Member.value:
            MemberImportRecovery(**kwargs).restart_import()
        if import_type == ImportType.Family.value:
            return FamilyImport(**kwargs).restart_import()
        if batchimport.import_type_id == ImportType.Purchase.value:
            PurchaseImportRecovery(**kwargs).restart_import()
        return ''
