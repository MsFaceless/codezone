# -*- coding: utf-8 -*-
"""UserController controller module"""

import os
import json
import string
from datetime import datetime
from pkg_resources import resource_filename
from tg import expose, require, redirect, validate, flash, url, request, response, predicates

from rocket.lib.base import BaseController
from rocket.lib.email_creator import RocketEmailCreator
from rocket.lib.tgfileuploader import FileUploader
from rocket.lib.tg_utils import *
from rocket.lib.tg_generic_reportlab import PDFCreator, Paragraph

from rocket.model import *

from sqlalchemy import func, desc, asc, or_

from rocket.controllers.common import CommonController

FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
PUBLIC_DIRNAME = os.path.join(FILENAME)
PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
IMAGES_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'images')
STAFFPIC_DIRNAME = os.path.join(IMAGES_DIRNAME, 'user_pictures')

LINK_EXPIRY = 4
PASSWORD_AGE = 11
SEARCHKEY = 'User_SearchKeyword'
SYSTEM_FROM_ADDRESS = 'noreply@rocket.com'
LOGIN_URL = 'http://www.rocket.com/login?id=guid'

COMMON = CommonController()

__all__ = ['UserController']

class UserController(BaseController):

    @expose()
    def get_user_htmltbl(self, *args, **kwargs):
        img_active = "<img src='/images/icon_check.png' />"
        img_inactive = "<img src='/images/icon_cross.png' />"
        outputlist = []
        dbase_query = self.get_user_list(**kwargs)
        for item in dbase_query:
            outputlist.append({
                'username' : f"<div class='user_select' user_id='{item.id}'>{item.username}</div>",
                'name' : item.name,
                'mobile' : item.mobile if item.mobile else '',
                'email' : item.email,
                'active': img_active if item.active else img_inactive,
            })
        dbcolumnlist = ['username', 'name', 'mobile', 'email', 'active']
        theadlist = ['Username', 'Name', 'Mobile', 'Email', 'Active']
        tdclasslist = ['action_link', '', '', '', 'text-right']
        html = build_html_table(outputlist, dbcolumnlist, theadlist, 'user_table', tdclasslist)
        javascript = """
        <script>
        $(".user_select").click(function(){
            var data = {'user_id' : $(this).attr('user_id')};
            $.redirect('/useraccess/edit', data);
        });
        </script>
        """
        return html + javascript

    #@require(predicates.in_any_group('Administrator', 'Users And Access'))
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY
        searchphrase = COMMON.get_searchphrase(**kwargs)
        usertable = self.get_user_htmltbl(**kwargs)
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card col-md-12">
                    <div class="card-header">
                        <div class="row d-flex">
                            <div class="col-md-6">
                                <h4 class="card-title">Users & Access</h4>
                            </div>
                            <div class="col-md-6 text-right">
                                <button class="btn btn-primary ml-auto action_new">Create New User</button>
                            </div>
                        </div>
                        <div class="row d-flex align-items-center">
                            <div class="col-md-4">
                                <input id='search' type="text" class="form-control search" name='searchphrase' placeholder="Search" value='{searchphrase}'>
                            </div>
                            <div class="col-md-8">
                                <button id='btn_search' class="btn btn-primary action_search">Search</button>
                                <button id='btn_reset' class="btn btn-primary">Reset</button>
                            </div>
                        </div>
                        <hr>
                    </div>
                    <div class="card-body">
                        <div id='div_user_table' class="table-responsive">
                            {usertable}
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        $(".action_new").click(function(){
            $.redirect('/useraccess/new');
        });
        $('#btn_search').click(function(){
            var kwargs = 'searchphrase='+$('#search').val();
            $('#div_user_table').load('/useraccess/get_user_htmltbl', kwargs, function(data){
                return false;
            });
        })
        $('#btn_reset').click(function(){
            $('#search').val('').focus();
            $('#div_user_table').load('/useraccess/get_user_htmltbl', 'reset=true', function(data){
                return false;
            });
        })
        """
        title = "Users & Access"
        return dict(title=title, html=html, javascript=javascript)

    #@require(predicates.in_any_group('Administrator', 'UsersAndAccess'))
    @expose('rocket.templates.generic')
    def new(self, *args, **kwargs):
        title = "New User"
        roles_html = self.get_roles_html()
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">New User</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back users_back">Back to Users</button>
                        </div>
                    </div>
                    <div class="card-body">
                        <form id='form_new_user'>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Full Name</label>
                                        <div class="col-md-9">
                                            <input class="form-control" name="name" type="text" required="true">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Username</label>
                                        <div class="col-md-9">
                                            <input class="form-control" name="username" type="text" required="true">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Email</label>
                                        <div class="col-md-9">
                                            <input class="form-control" name="email" type="email" required="true">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">Mobile</label>
                                        <div class="col-md-9">
                                            <input type="text" name="mobile" class="form-control">
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        {roles_html}
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_new_user' class="btn btn-primary">Save</button>
                        <button class="btn btn-outline-primary users_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
       """
        javascript ="""
        setFormValidation('#form_new_user');
        $('#save_new_user').click(function(){
             var valid = FormIsValid("#form_new_user");
             if(valid){

                var role_list = new Array;
                $('.user_role').each(function(){
                    if(this['checked'] === true){
                        var role_id = $(this).attr('role_id');
                        role_list.push(role_id);
                    };
                });

                var formserial = getFormData('#form_new_user');
                formserial['role_list'] = role_list;
                var data = {data : JSON.stringify(formserial)};

                $.post('/useraccess/save_new?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/useraccess/index');
                    };
                    return false;
                });
             }
        });

        $('.users_back').click(function(){
            $.redirect('/useraccess/index');
        });
        """
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def save_new(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        usernow = request.identity.get('user', {})
        this = User()
        this.name = data.get('name', None)
        this.username = data.get('username', None)
        this.email = data.get('email', None)
        this.mobile = data.get('mobile', None)
        this.active = False
        this.added_by = usernow.id
        DBSession.add(this)
        DBSession.flush()
        self.send_magic_link(**{'user_id': this.id})

        for role_id in data.get('role_list', []):
            this_role = DBSession.query(Role). \
                        filter(Role.id==role_id). \
                        one()
            this.roles.append(this_role)
            DBSession.flush()
        return json.dumps({'success' : True})

    @expose()
    def get_roles_html(self, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        user_roles = self.get_user_roles_list(**kwargs)

        roles_list =  DBSession.query(Role). \
                filter(Role.name != 'Developer'). \
                order_by(asc(Role.name)). \
                all()

        inner_html = ""
        for role in roles_list:
            checked = 'checked' if role.name in user_roles else ''
            inner_html += f"""
            <li class="list-item col-3">
                <div class="form-check mt-3">
                    <label class="form-check-label">
                        <input class="form-check-input user_role" role_id='{role.id}' type="checkbox" {checked}>
                        <span class="form-check-sign"></span>
                        {role.name}
                    </label>
                </div>
            </li>
            """
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="col-md-12">
                        <div class="card-header">
                            <h4 class="card-title">Roles</h4>
                        </div>
                    </div>
                    <div class="card-body">
                        <div class="col-12 container">
                            <ul class="list-unstyled row">
                                {inner_html}
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        return html

    #@require(predicates.in_any_group('Administrator', 'UsersAndAccess'))
    @expose('rocket.templates.generic')
    def edit(self, *args, **kwargs):
        usernow = request.identity.get('user', {})
        user_id = kwargs.get('user_id', None)
        if not user_id: redirect('/useraccess/index')
        user = User.by_id(user_id)
        if not user: redirect('/useraccess/index')
        roles_html = self.get_roles_html(**kwargs)
        selectbox_groups = 'selectbox groups'
        title = "Edit User"
        has_administrator = COMMON.check_usernow_has_role('Administrator')
        btn_reset = ""
        if has_administrator:
            btn_reset = f"""<button class='btn btn-danger ml-auto action_reset users_reset' user_id='{user_id}'>Reset Password</button>"""
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card ">
                    <div class="card-header d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">Edit '{user.name}'</h4>
                        </div>
                        <div class="col-md-6 text-right">
                            <button class="btn btn-primary ml-auto action_back users_back">Back to Users</button>
                        </div>
                    </div>
                    <div class="card-body ">
                        <form id='form_edit_user'>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Full Name</label>
                                        <div class="col-md-9">
                                            <input style='display:none' class="form-control" name="user_id" type="text" value="{user.id}">
                                            <input class="form-control" name="name" type="text" required="true" value="{user.name}">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Username</label>
                                        <div class="col-md-9">
                                            <input class="form-control" name="username" type="text" required="true" value="{user.username}">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label" required>Email</label>
                                        <div class="col-md-9">
                                            <input class="form-control" name="email" type="email" required="true" value="{user.email}">
                                        </div>
                                    </div>
                                </div>
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">Mobile</label>
                                        <div class="col-md-9">
                                            <input type="text" name="mobile" class="form-control" value="{user.mobile if user.mobile else ''}">
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-md-6">
                                    <div class="form-group row">
                                        <label class="col-md-3 col-form-label">User Group</label>
                                        <div class="col-md-9">
                                            {selectbox_groups}
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </form>
                    </div>
                </div>
            </div>
        </div>
        {roles_html}
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                    <div class="card-body">
                        <button id='save_edit_user' class="btn btn-primary">Save</button>
                        {btn_reset}
                        <button class="btn btn-outline-primary users_back">Cancel</button>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript ="""
        setFormValidation('#form_edit_user');
        $('#save_edit_user').click(function(){
             var valid = FormIsValid("#form_edit_user");
             if(valid){
                var role_list = new Array;

                $('.user_role').each(function(){
                    if(this['checked'] === true){
                        var role_id = $(this).attr('role_id');
                        role_list.push(role_id);
                    };
                });

                var formserial = getFormData('#form_edit_user');
                formserial['role_list'] = role_list;
                var data = {data : JSON.stringify(formserial)};
                $.post('/useraccess/save_edit?', data, function(data){
                    var result = JSON.parse(data);
                    if(result.success === true){
                        $.redirect('/useraccess/index');
                    };
                    return false;
                });
             }
        });
        $('.users_back').click(function(){
            $.redirect('/useraccess/index');
        });
        $('.users_reset').click(function(){
            var user_id = 'user_id='+$(this).attr('user_id');
            $.post('/useraccess/send_magic_link?', user_id, function(data){
                return false;
            });
        });
        """
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def create_magic_link(self, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        email = kwargs.get('email', None)
        if not (user_id or email): return False
        elif user_id:
            user = User.by_id(user_id)
            if not user: return False
        elif email:
            user = User.by_email(email)
            if not user: return False
        this = UserGuid()
        this.user_id = user_id
        this.guid = self.get_guid()
        this.expires = datetime.now() + timedelta(hours = LINK_EXPIRY)
        DBSession.add(this)
        DBSession.flush()
        domain = request.host_url
        return domain + "/reset/" + this.guid

    @expose()
    def send_magic_link(self, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        magic_link = self.create_magic_link(**kwargs)
        user = User.by_id(user_id)
        if not user: return 'false'
        if not user.email: return 'false'
        e = RocketEmailCreator()
        valid_email = e.validate_email(user.email)
        if not valid_email: return 'false'
        e.add_subject('Password Reset | Rocket')
        e.add_to_address(user.email)
        plain_text = f"""
        Dear {user.name}, \n\n

        To reset your password, please copy the following link and paste it in your browser: {magic_link}<br/>
        """
        e.add_plain_text(plain_text)
        rich_text = f"""
        Dear {user.name};<br/><br/>
        To reset your password, please click on the the following link:<br/>
        <a href="{magic_link}">{magic_link}</a><br/>
        <p>If the link is not clickable, please copy and paste it into your browser.</p>
        """
        e.add_rich_text(rich_text)
        e.send(False)
        if not e: return 'false'
        return 'true'

    def create_password_history(self, *args, **kwargs):
        user = User.by_id(kwargs.get('user_id', None))
        if not user: return False
        password = kwargs.get('password', None)
        if not password: return False
        this = PasswordHistory()
        this.user_id = user.id
        this.password = user.password
        this.added_by = user.id
        DBSession.add(this)
        DBSession.flush()
        return True

    def get_guid(self, *args, **kwargs):
        import hashlib, uuid
        guid = hashlib.md5(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        exists = UserGuid.by_guid(guid)
        if exists: return get_guid()
        return guid

    @expose()
    def save_edit(self, *args, **kwargs):
        data = json.loads(kwargs.get('data', json.dumps({})))
        if not data: return json.dumps({'success' : False})
        this = DBSession.query(User). \
                filter(User.id==data.get('user_id', None)). \
                one()
        this.name = data.get('name', None)
        this.username = data.get('username', None)
        this.email = data.get('email', None)
        this.mobile = data.get('mobile', None)
        DBSession.flush()

        new = [str_to_int(id) for id in data.get('role_list', [])]
        exists = [r.id for r in this.roles]
        roles_to_add = [i for i in new if i not in exists]
        roles_to_remove = [i for i in exists if i not in new]

        for role_id in roles_to_remove:
            try: this_role = DBSession.query(Role).filter(Role.id==role_id).one()
            except: continue
            this.roles.remove(this_role)
            DBSession.flush()
        for role_id in roles_to_add:
            try: this_role = DBSession.query(Role).filter(Role.id==role_id).one()
            except: continue
            this.roles.append(this_role)
            DBSession.flush()
        return json.dumps({'success' : True})

    def get_user_list(self, *args, **kwargs):
        kwargs['searchkey'] = SEARCHKEY
        searchphrase = COMMON.get_searchphrase(**kwargs)
        if searchphrase:
            searchterm = f'%{searchphrase}%'
            dbase_query = DBSession.query(User). \
                    filter(or_(
                        User.username.like(searchterm),
                        User.name.like(searchterm),
                        User.mobile.like(searchterm),
                        User.email.like(searchterm),
                    )). \
                    order_by(asc(User.username)). \
                    all()
        else:
            dbase_query = DBSession.query(User). \
                    order_by(asc(User.username)). \
                    all()
        return dbase_query

    def get_user_roles_list(self, *args, **kwargs):
        user_id = kwargs.get('user_id', None)
        if not user_id: return []
        roles_list = DBSession.query(User). \
                filter(User.id==user_id). \
                one().roles
        return [str(r.name) for r in roles_list]

    @expose('rocket.templates.prelogin')
    def forgot(self, *args, **kwargs):
        html = f"""
        <div class="login-box">
            <div class="container">
                <div class="d-flex justify-content-center h-100">
                    <div class="card">
                        <div class="card-header"> <h3>Forgot your password?</h3> </div>
                        <div class="card-body">
                            <div class="input-group form-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fas fa-envelope"></i></span>
                                </div>
                                <input id="email" class="form-control" type="text" name="email" placeholder="your email address" autofocus="autofocus">
                            </div>
                            <div class="alert alert-success hidden">
                                <button type="button" aria-hidden="true" class="close">
                                    <i class="now-ui-icons ui-1_simple-remove"></i>
                                </button>
                                <span><b> Success!</b><br/>Please check your email for further instructions.</span>
                                <br/><a class="action_link">Click here to return to log in</a>
                            </div>
                            <div class="alert alert-danger hidden">
                                <button type="button" aria-hidden="true" class="close">
                                    <i class="now-ui-icons ui-1_simple-remove"></i>
                                </button>
                                <span><b> Oops!</b><br/>We did not recognise the address you typed, please retype carefully.</span>
                                <br/><a class="action_link">Click here to return to log in</a>
                            </div>
                            <div class="form-group">
                                <button id="forgot_password" type="submit" class="btn float-right action_btn">Reset Password</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

        javascript = """
        $('#forgot_password').click(function(){
            var kwargs = 'email='+$('#email').val();
            $.post('/useraccess/forgot_password?', kwargs, function(data){
                if(data==='true'){
                    $('.alert-success').removeClass('hidden');
                    $('.alert-danger').addClass('hidden');
                    return false;
                } else {
                    $('.alert-danger').removeClass('hidden');
                    $('.alert-success').addClass('hidden');
                    return false;
                }
                return false;
            })
        });
        $('.action_link').click(function(){
            $.redirect('/');
            return false;
        });
        """
        title = "Forgot"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def forgot_password(self, *args, **kwargs):
        user = User.by_email(**{'email': kwargs.get('email', None)})
        if user:
            self.send_magic_link(**{'user_id': user.id})
            return 'true'
        else:
            return 'false'


    @expose('rocket.templates.prelogin')
    def reset(self, *args, **kwargs):
        guid = UserGuid.by_guid(kwargs.get('guid', None))
        if not guid: return False
        user = User.by_id(guid.user_id)
        if not user: return False
        html = f"""
        <div class="login-box">
            <div class="container">
                <div class="d-flex justify-content-center h-100">
                    <div class="card reset">
                        <div class="card-header"> <h5 class="text-white">Welcome back, </h5> <h3>{user.name}</h3> </div>
                        <div class="card-body">
                            <div class="input-group form-group">
                                <span class="policy_text">
                                    <b>Password should </b>
                                    <ul>
                                        <li id="length">
                                            be at least 10 characters long
                                            <i class="fas fa-check-circle green hidden"></i>
                                            <i class="fas fa-times-circle red hidden"></i>

                                        </li>

                                        <li id="uppercase">
                                            contain at least one uppercase character
                                            <i class="fas fa-check-circle green hidden"></i>
                                            <i class="fas fa-times-circle red hidden"></i>

                                        </li>

                                        <li id="special">
                                            contain at least one special character
                                            <i class="fas fa-check-circle green hidden"></i>
                                            <i class="fas fa-times-circle red hidden"></i>

                                        </li>

                                        <li id="digit">
                                            contain at least one digit
                                            <i class="fas fa-check-circle green hidden"></i>
                                            <i class="fas fa-times-circle red hidden"></i>
                                        </li>

                                    </ul>
                                    <b>New password</b>
                                    <ul>
                                        <li id="month">is valid for 1 month</li>
                                        <li id="repeat">
                                            may not be one of your last 12 passwords
                                            <i class="fas fa-check-circle green hidden"></i>
                                            <i class="fas fa-times-circle red hidden"></i>
                                        </li>
                                    </ul>
                                </span>
                            </div>
                            <div class="input-group form-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fas fa-key"></i></span>
                                </div>
                                <input id="new_password" class="form-control" type="password" name="new_password" placeholder="new password" value=""/>
                            </div>
                            <div class="input-group form-group">
                                <div class="input-group-prepend">
                                    <span class="input-group-text"><i class="fas fa-check-double"></i></span>
                                </div>
                                <input id="confirm_password" class="form-control" type="password" name="confirm_password" placeholder="confirm new password"/>
                            </div>
                            <div class="alert alert-danger hidden">
                                <button type="button" aria-hidden="true" class="close">
                                    <i class="now-ui-icons ui-1_simple-remove"></i>
                                </button>
                                <span><b> Oops!</b><br/>Passwords don't match.</span>
                            </div>
                            <div class="form-group">
                                <button id="reset_password" user_id="{user.id}" type="submit" class="btn float-right action_btn">Confirm</button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """
        javascript = """
        // Keyup runs twice if shift key is pressed
        $('#new_password').on('keyup', function(){
            var kwargs = 'password='+$(this).val();
            $.get('/useraccess/validate_password?', kwargs, function(data){
                var response = JSON.parse(data);
                var errors = response.errorlist;

                checkErrors('uppercase', errors);
                checkErrors('digit', errors);
                checkErrors('special', errors);
                checkErrors('length', errors);

                return false;
            });
        });
        $('#confirm_password').focus(function(){
            var kwargs = 'password='+$('#new_password').val();
            kwargs += '&user_id='+$('#reset_password').attr('user_id');
            $.get('/useraccess/password_exists?', kwargs, function(data){
                if(data==='true'){
                    $('#repeat .fa-times-circle').removeClass('hidden');
                    $('#repeat .fa-check-circle').addClass('hidden');
                    return false;
                } else {
                    $('#repeat .fa-times-circle').addClass('hidden');
                    $('#repeat .fa-check-circle').removeClass('hidden');
                };
                return false;
            });
        });
        function checkErrors(selector, thelist){
            var green = $('#'+selector+' .fa-check-circle')
            var red = $('#'+selector+' .fa-times-circle')

            if(thelist.includes(selector)){
                red.removeClass('hidden');
                green.addClass('hidden');
            }else{
                red.addClass('hidden');
                green.removeClass('hidden');
            };
        };
        $('#confirm_password').on('keyup', function(){
            var pass1 = $('#new_password');
            var pass2 = $('#confirm_password');
            if(pass1.val().length === pass2.val().length){
                if(pass1.val() === pass2.val()){
                    $('.alert-danger').removeClass('hidden');

                };
                $('.alert-danger').addClass('hidden');

            }else{
                $('.alert-danger').removeClass('hidden');
            };
        });
        $('#reset_password').click(function(){
            var new_password  = $('#new_password').val();
            var confirm_password  = $('#confirm_password').val();
            if(new_password === confirm_password){
                $('.alert-danger').addClass('hidden');
                var kwargs = 'password='+confirm_password;
                kwargs += '&user_id='+$(this).attr('user_id');
                $.post('/useraccess/reset_password?', kwargs, function(data){
                    if(data==='true'){
                        $.redirect('/login');
                    }
                });

            } else {
                    $('.alert-danger').removeClass('hidden');
                    return false;
            }
            return false;
        });
        """
        title = "Reset"
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def reset_password(self, *args, **kwargs):
        password = kwargs.get('password', None)
        if not password: return 'false'
        valid = self.validate_password(**kwargs)
        success = json.loads(valid).get('success')
        if not success: return 'false'
        user = User.by_id(kwargs.get('user_id', None))
        if not user: return 'false'
        if user.password: self.create_password_history(**kwargs)
        user.password = password
        user.active = True
        DBSession.flush()
        return 'true'

    @expose()
    def validate_password(self, *args, **kwargs):
        password = kwargs.get('password', None)

        errorlist = []
        if not any(char for char in password if char in string.ascii_uppercase):
            errorlist.append('uppercase')

        if not any(char for char in password if char in string.digits):
            errorlist.append('digit')

        if not any(char for char in password if char in string.punctuation):
            errorlist.append('special')

        if not len(password) >= 10:
            errorlist.append('length')

        success = True
        if errorlist: success = False
        return json.dumps({'success' : success, 'errorlist' : errorlist})

    @expose()
    def password_exists(self, *args, **kwargs):
        user = User.by_id(kwargs.get('user_id', None))
        if not user:
            return 'false'
        if not user.password: return 'false'
        kwargs['existing_password'] = user.password
        match = self.validate_hashed_password(**kwargs)
        if match:
            return 'true'
        dbase_query = DBSession.query(PasswordHistory). \
            filter(PasswordHistory.user_id==user.id). \
            order_by(desc(PasswordHistory.id)). \
            limit(PASSWORD_AGE)
        if not dbase_query:
            return 'false'
        for item in dbase_query:
            kwargs['existing_password'] = item.password
            match = self.validate_hashed_password(**kwargs)
            if match:
                return 'true'
        return 'false'

    def validate_hashed_password(self, *args, **kwargs):
        new_pass = kwargs.get('password', None)
        hashed_pass = kwargs.get('existing_password', None)
        if not(new_pass or hashed_pass):
            return False
        hash = sha256()
        hash.update((new_pass + hashed_pass[:64]).encode('utf-8'))
        if hashed_pass[64:] == hash.hexdigest():
            return True
        return False
