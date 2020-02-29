# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl
from tg import request, redirect, tmpl_context

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from tg.exceptions import HTTPFound
from tg import predicates

from rocket import model
from rocket.model import DBSession

from rocket.lib.sidebar import Sidebar
from rocket.lib.base import BaseController

from rocket.controllers.error import ErrorController
from rocket.controllers.secure import SecureController
from rocket.controllers.profile import ProfileController
from rocket.controllers.members import MemberController
from rocket.controllers.entity import EntityController
from rocket.controllers.product import ProductController
from rocket.controllers.product_new import ProductController
from rocket.controllers.policy import PolicyController
from rocket.controllers.claim import ClaimController
from rocket.controllers.reports import ReportController
from rocket.controllers.useraccess import UserController
from rocket.controllers.batchimport import BatchImportController
from rocket.controllers.setup import SetupController
from rocket.controllers.location import LocationController

from rocket.lib.type_utils import *  # Delete this

__all__ = ['RootController']


class RootController(BaseController):

    secc = SecureController()
    error = ErrorController()
    profile = ProfileController()
    members = MemberController()
    entity = EntityController()
    product = ProductController()
    product_new = ProductController()
    policy = PolicyController()
    claim = ClaimController()
    reports = ReportController()
    useraccess = UserController()
    batchimport = BatchImportController()
    setup = SetupController()
    location = LocationController()

    def _before(self, *args, **kw): tmpl_context.project_name = "rocket"

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self):
        html = Sidebar().welcome()
        javascript = ""
        title = l_('Rocket')
        return dict(title=title, html=html, javascript=javascript)

    @expose('rocket.templates.login')
    def login(self, came_from=lurl('/'), failure=None, login=''):
        login_counter = request.environ.get('repoze.who.logins', 0)
        title = l_('Login')
        return dict(title=title, login_counter=str(login_counter), came_from=came_from, login=login)

    @expose()
    def post_login(self, came_from=lurl('/')):
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                     params=dict(came_from=came_from, __logins=login_counter))
        return HTTPFound(location=came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        return HTTPFound(location=came_from)

    @require(predicates.not_anonymous())
    @expose()
    def get_sidebar_html(self):
        return Sidebar().get_sidebar_html()
