# -*- coding: utf-8 -*-
"""LocationController controller module"""

import os
import json
from datetime import datetime
from pkg_resources import resource_filename

from tg import expose, require, redirect, validate, flash, url, request, response
from tg import predicates

from rocket.model import *

from rocket.lib.base import BaseController
from rocket.lib.tg_utils import *
from rocket.lib.tg_generic_reportlab import PDFCreator, Paragraph
from rocket.lib.tgfileuploader import FileUploader
from rocket.controllers.common import CommonController

from sqlalchemy import func, desc, asc

FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
IMAGES_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'images')
CATALOG_DIRNAME = os.path.join(IMAGES_DIRNAME, 'catalog_pictures')

SEARCHKEY = 'Country_SearchKeyword'
COMMON = CommonController()
LIMIT = 20

__all__ = ['LocationController']


class LocationController(BaseController):
    """Docstring for setup."""

    allow_only = predicates.has_any_permission('Administrator', 'CatalogMaintenance')

    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_country_html(*args, **kwargs)
        javascript = self.get_javascript_country_onload(*args, **kwargs)
        title = "Region / District / Centre"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_country_htmltbl(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        dbase_query = Country.get_limit(LIMIT, 'name')
        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"
        outputlist = []
        for item in dbase_query:
            radio = create_radio_html(**{'class' : 'country_select',
                                         'name_key' : 'country_name',
                                         'name_value' : item.name,
                                         'id_key' : 'country_id',
                                         'id_value' : item.id })
            outputlist.append({
                'radio': radio,
                'name': item.name,
                'code': item.code,
                'active': img_active if item.active else img_inactive,
            })
        dbcolumnlist = [
            'radio',
            'name',
            'code',
            'active',
                ]
        theadlist = [
            '',
            'Name',
            'Country Code',
            'Active',
                ]
        tdclasslist = [
            'width_80',
            '',
            '',
            'text-right'
        ]
        html = build_html_table(outputlist, dbcolumnlist, theadlist, "country_table", tdclasslist)
        javascript = """
        <script>
        $(document).ready(function(){
            $('.country_select').click(function(){
                var kwargs = 'country_id=' + $(this).attr('country_id');
                kwargs += '&country_name=' + $(this).attr('country_name');
                $('#div_region').load('/location/get_country_region_html?' + encodeURI(kwargs), function(data){
                    $('#div_district').empty();
                    $('#div_centre').empty();
                    return false;
                });
            })
            $('.country_select:eq(0)').trigger('click');
        });
        </script>
        """
        return html + javascript

    @expose()
    def get_country_html(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY
        searchphrase = COMMON.get_searchphrase(**kwargs)
        countrytable = self.get_country_htmltbl(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-12">
                            <h4 class="card-title">Country</h4>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-4">
                            <input id='search' type="text" class="form-control search" name="searchphrase" placeholder="Search by Name or Country Code" value='{searchphrase}'>
                        </div>
                        <div class="col-md-8">
                            <button id='btn_search' class="btn btn-primary action_search">Search</button>
                            <button id='btn_reset' class="btn btn-primary">Reset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div id='div_country_table' class="table-responsive">
                        {countrytable}
                    </div>
                </div>
            </div>
        </div>
        </div>
        <div id="div_region"  class="row"></div>
        <div id="div_district" class="row"></div>
        <div id="div_centre" class="row"></div>
        """
        return html

    @expose()
    def get_javascript_country_onload(self, *args, **kwargs):
        javascript = """
        $('#btn_search').click(function(){
            var kwargs = 'searchphrase='+$('#search').val();
            $('#div_country_table').load('/location/get_country_htmltbl', kwargs, function(data){
                $('#div_region').empty();
                $('#div_district').empty();
                $('#div_centre').empty();
                return false;
            });
        })
        $('#btn_reset').click(function(){
            $('#search').val('').focus();
            $('#div_country_table').load('/location/get_country_htmltbl', 'reset=true', function(data){
                $('#div_region').empty();
                $('#div_district').empty();
                $('#div_centre').empty();
                return false;
            });
        })
        """
        return javascript

    @expose()
    def get_country_region_html(self, *args, **kwargs):
        country_id = kwargs.get('country_id', None)
        usernow = request.identity.get('user', {})
        dbase_query = Region.by_attr_limit('country_id', country_id, LIMIT)
        outputlist = []
        for item in dbase_query:
            radio = create_radio_html(**{'class' : 'region_select',
                'name_key' : 'region_name',
                'name_value' : item.name,
                'id_key' : 'region_id',
                'id_value' : item.id })
            outputlist.append({
                'radio' : radio,
                'name': f"""<div class='edit edit_dialog_region'
                            region_id='{item.id}'
                            country_id='{kwargs.get('country_id')}'
                            country_name='{kwargs.get('country_name')}'>{item.name}</div>"""
                            })
        dbcolumnlist = [
                'radio',
                'name',
                ]
        theadlist = [
                '',
                'Name',
                ]
        tdclasslist = [
            'width_80',
            'action_link'
        ]
        regiontable = build_html_table(outputlist, dbcolumnlist, theadlist, "region_table", tdclasslist)
        html = f"""
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Regions for {kwargs.get('country_name', '')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="new_dialog_region" country_id="{kwargs.get('country_id')}" country_name="{kwargs.get('country_name')}" class="btn btn-primary ml-auto">Create a new Region</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-4">
                            <input type="text" class="form-control search" name="searchphrase" placeholder="Search">
                        </div>
                        <div class="col-md-8">
                            <button class="btn btn-primary action_search">Search</button>
                            <button class="btn btn-primary">Reset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {regiontable}
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        $(document).ready(function(){
            $('.region_select').click(function(){
                var kwargs = 'region_id=' + $(this).attr('region_id');
                kwargs += '&region_name=' + $(this).attr('region_name');
                $('#div_district').load('/location/get_region_district_html?' + encodeURI(kwargs), function(data){
                    $('#div_centre').empty();
                    return false;
                });
            });
            $('.region_select:eq(0)').trigger('click');

            $('#new_dialog_region').click(function(){
                var kwargs = 'country_id='+ $(this).attr('country_id');
                kwargs += '&country_name=' + $(this).attr('country_name');
                $('#dialogdiv').load('/location/get_dialog_new_region?' + encodeURI(kwargs), function(data){
                    return false;
                });
            });
            $(".edit_dialog_region").click(function(){
                var kwargs = 'country_id='+ $(this).attr('country_id');
                kwargs += '&country_name=' + $(this).attr('country_name');
                kwargs += '&region_id=' + $(this).attr('region_id');
                $('#dialogdiv').load('/location/get_dialog_edit_region?' + encodeURI(kwargs), function(data){
                    return false;
                });
            });
        });
        </script>
        """
        return html + javascript

    @expose()
    def get_dialog_new_region(self, *args, **kwargs):
        html = f"""
        <div class="modal fade" id="dialog_new_region" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">New Region for {kwargs.get('country_name')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_region'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                        <input style='display: none;' id="country_id" type="text" name="country_id" class="form-control"
                                            country_name="{kwargs.get('country_name')}" value="{kwargs.get('country_id')}">
                                        <input id="name" type="text" name="name" maxlength='255' class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_region' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary region_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_new_region');
            $('#save_new_region').click(function(){
                 var valid = FormIsValid("#form_new_region");
                 if(valid){
                    var formserial = getFormData('#form_new_region');
                    var data = {data : JSON.stringify(formserial)};
                    $.post('/location/save_new_region?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $('#dialog_new_region').modal('hide');
                            var kwargs = 'country_id=' + $('#country_id').val();
                            kwargs += '&country_name=' + $('#country_id').attr('country_name');
                            $('#div_region').load('/location/get_country_region_html?' + encodeURI(kwargs), function(data){
                                $('#div_district').empty();
                                $('#div_centre').empty();
                                return false;
                            });
                        };
                        return false;
                    });
                 }
            });
            $('.region_back').click(function(){
                $('#dialog_new_region').modal('hide');
            });
            $('#dialog_new_region').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_new_region(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False})
        this = Country.by_id(data.get('country_id'))
        if not this: return json.dumps({'success': False})
        region = Region()
        region.country_id = data.get('country_id')
        region.name = data.get('name')
        region.added_by = usernow.id
        DBSession.add(region)
        DBSession.flush()
        return json.dumps({'success': True, 'region_id': region.id})

    @expose()
    def get_dialog_edit_region(self, *args, **kwargs):
        region_id = kwargs.get('region_id', None)
        if not region_id: return ''
        this = Region.by_id(region_id)
        if not this: return ''
        selectbox_countries = self.get_selectbox_countries(**{'id': 'country_id', 'required': True, 'selected': this.country_id})
        html = f"""
        <div class="modal fade" id="dialog_edit_region" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Edit Region for {kwargs.get('country_name')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_region'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                        <input style='display: none;' id="country_id" country_name='{kwargs.get('country_name')}'' type="text" name="country_id" class="form-control" value='{kwargs.get('country_id')}'>
                                        <input style='display: none;' id="region_id" type="text" name="region_id" class="form-control" value='{kwargs.get('region_id')}'>
                                        <input id="name" type="text" name="name" class="form-control" maxlength='255' required='true' value='{this.name}'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_edit_region' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary region_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_edit_region');
            $('#save_edit_region').click(function(){
                 var valid = FormIsValid("#form_edit_region");
                 if(valid){
                    var formserial = getFormData('#form_edit_region');
                    var data = {data : JSON.stringify(formserial)};
                    $.post('/location/save_edit_region?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $('#dialog_edit_region').modal('hide');
                            var kwargs = 'country_id=' + $('#country_id').val();
                            kwargs += '&country_name=' + $('#country_id').attr('country_name');
                            $('#div_region').load('/location/get_country_region_html?' + encodeURI(kwargs), function(data){
                                $('#div_district').empty();
                                $('#div_centre').empty();
                                return false;
                            });
                        };
                        return false;
                    });
                 }
            });
            $('.region_back').click(function(){
                $('#dialog_edit_region').modal('hide');
            });
            $('#dialog_edit_region').modal();
        </script>
        """
        return html + javascript

    @expose()
    def get_region_district_html(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        region_id = kwargs.get('region_id', None)
        dbase_query = District.by_attr_limit('region_id', region_id, LIMIT)
        outputlist = []
        for item in dbase_query:
            radio = create_radio_html(**{'class': 'district_select',
                'name_key': 'district_name',
                'name_value': item.name,
                'id_key': 'district_id',
                'id_value': item.id})
            outputlist.append({
                'radio': radio,
                'name': f"""<div class='edit edit_dialog_district action_link'
                                district_id='{item.id}'
                                region_id='{kwargs.get('region_id')}'
                                region_name='{kwargs.get('region_name')}'>{item.name}</div>
                        """})
        dbcolumnlist = [
            'radio',
            'name',
                ]
        theadlist = [
            '',
            'Name',
                ]
        tdclasslist = [
            'width_80',
            'action_link'
        ]
        districttable = build_html_table(outputlist, dbcolumnlist, theadlist, "district_table", tdclasslist)
        html = f"""
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Districts for {kwargs.get('region_name', '')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="new_dialog_district" region_name="{kwargs.get('region_name')}"" region_id="{kwargs.get('region_id')}" class="btn btn-primary ml-auto">Create a new District</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-4">
                            <input type="text" class="form-control search" name="searchphrase" placeholder="Search">
                        </div>
                        <div class="col-md-8">
                            <button class="btn btn-primary action_search">Search</button>
                            <button class="btn btn-primary">Reset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {districttable}
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        $(document).ready(function(){
            $('.district_select').click(function(){
                var kwargs = 'district_id=' + $(this).attr('district_id');
                kwargs += '&district_name=' + $(this).attr('district_name');
                $('#div_centre').load('/location/get_district_centre_html?' + encodeURI(kwargs), function(data){
                    return false;
                });
            })
            $('.district_select:eq(0)').trigger('click');

            $("#new_dialog_district").click(function(){
                var kwargs = "region_id="+ $(this).attr('region_id');
                kwargs += '&region_name=' + $(this).attr('region_name');
                $('#dialogdiv').load('/location/get_dialog_new_district?' + encodeURI(kwargs), function(data){
                    return false;
                });
            });
            $(".edit_dialog_district").click(function(){
                var kwargs = 'region_id='+ $(this).attr('region_id');
                kwargs += '&region_name=' + $(this).attr('region_name');
                kwargs += '&district_id=' + $(this).attr('district_id');
                $('#dialogdiv').load('/location/get_dialog_edit_district?' + encodeURI(kwargs), function(data){
                    return false;
                });
            });
        });
        </script>
        """
        return html + javascript

    @expose()
    def save_edit_region(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False})
        usernow = request.identity.get('user', {})
        this = Country.by_id(data.get('country_id'))
        if not this: return json.dumps({'success': False})
        region = Region.by_id(data.get('region_id', None))
        region.name = data.get('name', None)
        DBSession.flush()
        return json.dumps({'success': True, 'region_id': region.id})

    @expose()
    def get_dialog_new_district(self, *args, **kwargs):
        html = f"""
        <div class="modal fade" id="dialog_new_district" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">New District for for {kwargs.get('region_name')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_district'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                      <input style='display: none;' id="region_id" region_name='{kwargs.get('region_name')}'type="text" name="region_id" class="form-control" value='{kwargs.get('region_id')}'>
                                      <input id="name" type="text" maxlength='255' name="name" class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_district' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary district_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_new_district');
            $('#save_new_district').click(function(){
                 var valid = FormIsValid("#form_new_district");
                 if(valid){
                    var formserial = getFormData('#form_new_district');
                    var data = {data : JSON.stringify(formserial)};
                    $.post('/location/save_new_district?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $('#dialog_new_district').modal('hide');
                            var kwargs = 'region_id=' + $('#region_id').val();
                            kwargs += '&region_name=' + $('#region_id').attr('region_name');
                            $('#div_district').load('/location/get_region_district_html?' + encodeURI(kwargs), function(data){
                                $('#div_centre').empty();
                                return false;
                            });
                        };
                        return false;
                    });
                 }
            });
            $('.district_back').click(function(){
                $('#dialog_new_district').modal('hide');
            });
            $('#dialog_new_district').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_new_district(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False})
        this = Region.by_id(data.get('region_id'))
        if not this: return json.dumps({'success': False})
        usernow = request.identity.get('user', {})
        district = District()
        district.region_id = data.get('region_id')
        district.name = data.get('name')
        district.added_by = usernow.id
        DBSession.add(district)
        DBSession.flush()
        return json.dumps({'success': True, 'district_id': district.id})

    @expose()
    def get_dialog_edit_district(self, *args, **kwargs):
        district_id = kwargs.get('district_id', None)
        if not district_id: return ''
        this = District.by_id(district_id)
        if not this: return ''
        selectbox_regions = self.get_selectbox_regions( **{'id': 'region_id', 'required': True, 'selected': this.region_id})
        html = f"""
        <div class="modal fade" id="dialog_edit_district" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Edit District for {kwargs.get('region_name')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_district'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                        <input style='display: none;' id="region_id" region_name='{kwargs.get('region_name')}' type="text" name="region_id" class="form-control" value='{kwargs.get('region_id')}'>
                                        <input style='display: none;' id="district_id" type="text" name="district_id" class="form-control" value='{kwargs.get('district_id')}'>
                                        <input id="name" type="text" name="name" maxlength='255' class="form-control" required='true' value='{this.name}'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_edit_district' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary district_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_edit_district');
            $('#save_edit_district').click(function(){
                 var valid = FormIsValid("#form_edit_district");
                 if(valid){
                    var formserial = getFormData('#form_edit_district');
                    var data = {data : JSON.stringify(formserial)};

                    $.post('/location/save_edit_district?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $('#dialog_edit_district').modal('hide');
                            var kwargs = 'region_id=' + $('#region_id').val();
                            kwargs += '&region_name=' + $('#region_id').attr('region_name');
                            $('#div_district').load('/location/get_region_district_html?' + encodeURI(kwargs), function(data){
                                $('#div_centre').empty();
                                return false;
                            });
                        };
                        return false;
                    });
                 }
            });
            $('.district_back').click(function(){
                $('#dialog_edit_district').modal('hide');
            });
            $('#dialog_edit_district').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_edit_district(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False})
        this = Region.by_id(data.get('region_id'))
        if not this: return json.dumps({'success': False})
        usernow = request.identity.get('user', {})
        district = District.by_id(data.get('district_id', None))
        district.name = data.get('name', None)
        DBSession.flush()
        return json.dumps({'success': True, 'district_id': district.id})

    @expose()
    def get_district_centre_html(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        district_id = kwargs.get('district_id', None)
        dbase_query = Centre.by_attr_limit('district_id', district_id, LIMIT)
        outputlist = []
        for item in dbase_query:
            name = f"""<div class='edit edit_dialog_centre'
                            centre_id='{item.id}'
                            district_id='{kwargs.get('district_id')}'
                            district_name='{kwargs.get('district_name')}'
                      > {item.name} </div> """
            outputlist.append({
                'name': name,
                            })
        dbcolumnlist = [
                'name',
                ]
        theadlist = [
                'Name',
                ]
        tdclasslist = [
            'action_link'
        ]
        districttable = build_html_table(outputlist, dbcolumnlist, theadlist, "district_table", tdclasslist)
        html = f"""
        <div class="col-md-12">
            <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Centres for {kwargs.get('district_name')}</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button id="new_dialog_centre" district_id="{kwargs.get('district_id')}" district_name="{kwargs.get('district_name')}" class="btn btn-primary ml-auto">Create a new Centre</button>
                        </div>
                    </div>
                    <div class="row d-flex align-items-center">
                        <div class="col-md-4">
                            <input type="text" class="form-control search" name="searchphrase" placeholder="Search">
                        </div>
                        <div class="col-md-8">
                            <button class="btn btn-primary action_search">Search</button>
                            <button class="btn btn-primary">Reset</button>
                        </div>
                    </div>
                    <hr>
                </div>
                <div class="card-body">
                    <div class="table-responsive">
                        {districttable}
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
        $('#new_dialog_centre').click(function(){
            var kwargs = 'district_id='+ $(this).attr('district_id');
            kwargs += '&district_name=' + $(this).attr('district_name');
            $('#dialogdiv').load('/location/get_dialog_new_centre?' + encodeURI(kwargs), function(data){
                return false;
            });
        });

        $(".edit_dialog_centre").click(function(){
            var kwargs = 'district_id='+ $(this).attr('district_id');
            kwargs += '&district_name=' + $(this).attr('district_name');
            kwargs += '&centre_id=' + $(this).attr('centre_id');
            $('#dialogdiv').load('/location/get_dialog_edit_centre?' + encodeURI(kwargs), function(data){
                return false;
            });
        });
        </script>
        """
        return html + javascript

    @expose()
    def get_dialog_new_centre(self, *args, **kwargs):
        html = f"""
        <div class="modal fade" id="dialog_new_centre" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">New Centre for {kwargs.get('district_name')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_new_centre'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                        <input style='display: none;' id='district_id' district_name='{kwargs.get('district_name')}' type='text' name='district_id' class='form-control' value='{kwargs.get('district_id')}'>
                                        <input id="name" type="text" name="name" maxlength='50' class="form-control" required='true'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_new_centre' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary centre_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_new_centre');
            $('#save_new_centre').click(function(){
                 var valid = FormIsValid("#form_new_centre");
                 if(valid){
                    var formserial = getFormData('#form_new_centre');
                    var data = {data : JSON.stringify(formserial)};
                    $.post('/location/save_new_centre?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $('#dialog_new_centre').modal('hide');
                            var kwargs = 'district_id=' + $('#district_id').val();
                            kwargs += '&district_name=' + $('#district_id').attr('district_name');
                            $('#div_centre').load('/location/get_district_centre_html?' + encodeURI(kwargs), function(data){
                                return false;
                            });
                        };
                        return false;
                    });
                 }
            });
            $('.centre_back').click(function(){
                $('#dialog_new_centre').modal('hide');
            });
            $('#dialog_new_centre').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_new_centre(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False})
        this = District.by_id(data.get('district_id'))
        if not this: return json.dumps({'success': False})
        usernow = request.identity.get('user', {})
        centre = Centre()
        centre.district_id = data.get('district_id')
        centre.name = data.get('name')
        centre.added_by = usernow.id
        DBSession.add(centre)
        DBSession.flush()
        return json.dumps({'success': True, 'centre_id': centre.id})

    @expose()
    def get_dialog_edit_centre(self, *args, **kwargs):
        centre_id = kwargs.get('centre_id', None)
        if not centre_id: return ''
        this = Centre.by_id(centre_id)
        if not this: return ''
        selectbox_districts = self.get_selectbox_districts( **{'id': 'district_id', 'required': True, 'selected': this.district_id})
        html = f"""
        <div class="modal fade" id="dialog_edit_centre" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">
            <div class="modal-dialog modal-dialog-centered">
                <div class="modal-content">
                    <div class="modal-header">
                        <div class="col-md-12">
                            <h4 class="card-title">Edit centre for {kwargs.get('district_name')}</h4>
                        </div>
                    </div>
                    <div class="modal-body">
                        <form id='form_edit_centre'>
                            <div class="col-md-12">
                                <div class="form-group row">
                                    <label class="col-md-3 col-form-label" required for="name">Name</label>
                                    <div class="col-md-9">
                                        <input style='display: none;' id="district_id" type="text" district_name='{kwargs.get('district_name')}' name="district_id" class="form-control" value='{kwargs.get('district_id')}'>
                                        <input style='display: none;' id="centre_id" type="text" name="centre_id" class="form-control" value='{kwargs.get('centre_id')}'>
                                        <input id="name" type="text" name="name" maxlength='50' class="form-control" required='true' value='{this.name}'>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button id='save_edit_centre' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary centre_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        <script>
            setFormValidation('#form_edit_centre');
            $('#save_edit_centre').click(function(){
                 var valid = FormIsValid("#form_edit_centre");
                 if(valid){
                    var formserial = getFormData('#form_edit_centre');
                    var data = {data : JSON.stringify(formserial)};
                    $.post('/location/save_edit_centre?', data, function(data){
                        var result = JSON.parse(data);
                        if(result.success === true){
                            $('#dialog_edit_centre').modal('hide');
                            var kwargs = 'district_id=' + $('#district_id').val();
                            kwargs += '&district_name=' + $('#district_id').attr('district_name');
                            $('#div_centre').load('/location/get_district_centre_html?' + encodeURI(kwargs), function(data){
                                return false;
                            });
                        };
                        return false;
                    });
                 }
            });
            $('.centre_back').click(function(){
                $('#dialog_edit_centre').modal('hide');
            });
            $('#dialog_edit_centre').modal();
        </script>
        """
        return html + javascript

    @expose()
    def save_edit_centre(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success': False})
        usernow = request.identity.get('user', {})
        this = District.by_id(data.get('district_id'))
        if not this: return json.dumps({'success': False})
        centre = Centre.by_id(data.get('centre_id'))
        centre.name = data.get('name')
        DBSession.flush()
        return json.dumps({'success': True, 'centre_id': centre.id})

    def get_selectbox_countries(self, *args, **kwargs):
        kwargs['active'] = True
        kwargs['limit'] = 'all'
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in Country.get_all('name')]
        return create_selectbox_html(**kwargs)

    def get_selectbox_regions(self, *args, **kwargs):
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in Region.get_all('name')]
        return create_selectbox_html(**kwargs)

    def get_selectbox_districts(self, *args, **kwargs):
        kwargs['outputlist'] = [{'name': m.name, 'id': m.id} for m in District.get_all('name')]
        return create_selectbox_html(**kwargs)
