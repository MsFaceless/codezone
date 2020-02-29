# -*- coding: utf-8 -*-
"""Profile controller module"""

from tg import predicates, require
from tg import expose, redirect, validate, flash, url, request

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from rocket.model import *

from sqlalchemy import func, desc, asc

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController

LIMIT = 20

class ProfileController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def index(self, *args, **kwargs):
        html = self.get_active_profile_html(*args, **kwargs)
        javascript = self.get_javascript_profile_onload()
        title = _("My Profile")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_profile_html(self, *args, **kwargs):
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('My Profile')}</h4>
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

    @expose()
    def get_javascript_profile_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript
