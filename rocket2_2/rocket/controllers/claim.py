# -*- coding: utf-8 -*-
"""Claim controller module"""

from tg import predicates, require
from tg import expose, redirect, validate, flash, url, request

from tg.i18n import ugettext as _
from tg.i18n import lazy_ugettext as l_

from rocket.model import *

from sqlalchemy import func, desc, asc

from rocket.lib.tg_utils import *
from rocket.lib.base import BaseController

LIMIT = 20

class ClaimController(BaseController):

    def __init__(self, *args, **kwargs):
        pass

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def registration(self, *args, **kwargs):
        html = self.get_active_claim_registration_html(*args, **kwargs)
        javascript = self.get_javascript_claim_registration_onload()
        title = _("Claim Registration")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_claim_registration_html(self, *args, **kwargs):
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Claim Registration')}</h4>
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
    def get_javascript_claim_registration_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def management(self, *args, **kwargs):
        html = self.get_active_claim_management_html(*args, **kwargs)
        javascript = self.get_javascript_claim_management_onload()
        title = _("Claim Management")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_claim_management_html(self, *args, **kwargs):
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Claim Management')}</h4>
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
    def get_javascript_claim_management_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript

    @require(predicates.not_anonymous())
    @expose('rocket.templates.generic')
    def approval(self, *args, **kwargs):
        html = self.get_active_claim_approval_html(*args, **kwargs)
        javascript = self.get_javascript_claim_approval_onload()
        title = _("Claim Approval")
        return dict(title=title, html=html, javascript=javascript)

    @expose()
    def get_active_claim_approval_html(self, *args, **kwargs):
        html = f"""
        <div class="row">
            <div class="col-md-12">
                <div class="card">
                <div class="card-header">
                    <div class="row d-flex">
                        <div class="col-md-6">
                            <h4 class="card-title">{_('Claim Approval')}</h4>
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
    def get_javascript_claim_approval_onload(self, *args, **kwargs):
        javascript = """
        """
        return javascript
