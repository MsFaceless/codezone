# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
from tg.decorators import paginate

#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
#from tw.jquery import AjaxForm
#from tw.jquery import FlexiGrid
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import FileStoreProduction
from jistdocstore.model import DBS_JistBuying, metadata5
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
from babel.numbers import format_currency, format_number, format_decimal
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
current_purchase_req_id = 0 
current_purchase_order_id = 0 
current_purchase_order_items = [] 
__all__ = ['VettingController']


class VettingController(BaseController):
    """Sample controller-wide authorization"""
    
    #The predicate that must be met for all the actions in this controller:
    allow_only = has_any_permission('manage','accountsmanage','buyingmanage',
                                msg=l_('Only for people with the "manage" permission'))

    @expose()
    def index(self):
        redirect('vettingcont/menu')

    @expose('jistdocstore.templates.vettingindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Vetting Main Menu') 
