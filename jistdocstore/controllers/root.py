# -*- coding: utf-8 -*-
"""Main Controller"""

from tg import expose, flash, require, url, lurl, request, redirect, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg import predicates
from jistdocstore import model
from jistdocstore.model import DBS_ContractData, metadata2

from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
from tg.decorators import paginate
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController

from jistdocstore.lib.base import BaseController
from jistdocstore.controllers.error import ErrorController

from jistdocstore.controllers.secure import SecureController
from jistdocstore.controllers.managementcont import ManagementController
from jistdocstore.controllers.topmanagement import TopManagementController
from jistdocstore.controllers.labourcont import LabourController
from jistdocstore.controllers.logisticscont import LogisticsController
from jistdocstore.controllers.marketingcont import MarketingController
from jistdocstore.controllers.productioncont import ProductionController
from jistdocstore.controllers.contractscont import ContractsController
from jistdocstore.controllers.estimatingcont import EstimatingController
from jistdocstore.controllers.vettingcont import VettingController
from jistdocstore.controllers.fleetcont import FleetController
from jistdocstore.controllers.transportcont import TransportController
from jistdocstore.controllers.receptioncont import ReceptionController
from jistdocstore.controllers.accountscont import AccountsController
from jistdocstore.controllers.invoicingcont import InvoicingController
from jistdocstore.controllers.manufacturecont import ManufacturingController
from jistdocstore.controllers.est5yreskomfencingcont import Estimating_5yr_Eskom_Fencing_Controller 
from jistdocstore.controllers.est3yresshsfcont import Estimating_3yr_Ess_HSF_Controller 
from jistdocstore.controllers.est3yresspalisadecont import Estimating_3yr_Ess_Palisade_Controller 
from jistdocstore.controllers.cctvcont import CCTVController
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model import * 
from datetime import datetime, time, date
import shutil
import os
import string
import re
from pkg_resources import resource_filename
import subprocess
from tg import session
import locale
#from ming import Session
#from ming.odm import ThreadLocalODMSession


public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')

__all__ = ['RootController']


class RootController(BaseController):
    """
    The root controller for the jistdocstore application.

    All the other controllers and WSGI applications should be mounted on this
    controller. For example::

        panel = ControlPanelController()
        another_app = AnotherWSGIApplication()

    Keep in mind that WSGI applications shouldn't be mounted directly: They
    must be wrapped around with :class:`tg.controllers.WSGIAppController`.

    """
    secc = SecureController()
    admin = AdminController(model, DBS_ContractData, config_type=TGAdminConfig)

    mngntcont = ManagementController()
    topmngntcont = TopManagementController()
    labourcont = LabourController()
    logisticscont = LogisticsController()
    marketingcont = MarketingController()
    productioncont = ProductionController()
    contractscont = ContractsController()
    estimatingcont = EstimatingController()
    vettingcont = VettingController()
    manufacturecont = ManufacturingController()
    transportcont = TransportController()
    fleetcont = FleetController()
    accountscont = AccountsController()
    invoicingcont = InvoicingController()
    receptioncont = ReceptionController()
    cctvcont = CCTVController()
    est5yreskomfencingcont = Estimating_5yr_Eskom_Fencing_Controller()
    est3yresspalisadecont = Estimating_3yr_Ess_Palisade_Controller()
    est3yresshsfcont = Estimating_3yr_Ess_HSF_Controller()

    error = ErrorController()

    def _before(self, *args, **kw):
        tmpl_context.project_name = "Jistdocstore"

    @expose('jistdocstore.templates.index')
    def index(self):
        """Handle the front-page."""
        redirect('/myjistconsole')
        #return dict(page='index')


    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.myjistconsole')
    def myjistconsole(self,**named):
        """Handle the 'myjistconsole'."""
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id

        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()

        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        pointlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            if point:
                if point.user_id == 1:
                    pointlist.append({'user_id':point.user_id,
                                      'user_name':point.user_name,
                                      'display_name':point.display_name
                                      })
                user = User.by_user_id(point.user_id)
                userpermissions = user.permissions
                for permis in userpermissions:
                    #print permis.permission_name
                    if permis.permission_name=='productionmanage':
                        pointlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name,
                                          'display_name':point.display_name
                                          })

        return dict(page='My JIST Console',
                    contracts = contracts,
                    users = activeusers,
                    myjistid = myid,
                    points = pointlist)



    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.mypoints')
    def mypoints(self,**named):
        """Handle the 'mypoints' page."""
        tmpl_context.widget = spx_contracts_table 
        value = mycontracts_filler.get_value(values={},offset=0,order_by='jno',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print currentPage
        #print currentPage.page
        #print currentPage.previous_page
        return dict(page='myjist',
                    wip = items,
                    thiscurrentPage=currentPage,
                    count=count)

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.mysiteagentspages')
    def my_site_agent_contracts(self,**named):
        """Handle the 'site_agent_contracts' page."""
        tmpl_context.widget = spx_contracts_table 
        value = contracts_siteagent_filler.get_value(values={},offset=0,order_by='jno',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print currentPage
        #print currentPage.page
        #print currentPage.previous_page
        return dict(page='myjist',
                    wip = items,
                    thiscurrentPage=currentPage,
                    count=count)

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.myjistpages')
    def myjist(self,**named):
        """Handle the 'myjistpages'."""
        return dict(page='My JIST Main Menu')


    #################################################################################
    #############Boiler Plate Code Starts############################################

    @expose('jistdocstore.templates.about')
    def about(self):
        """Handle the 'about' page."""
        return dict(page='about')

    @expose('jistdocstore.templates.environ')
    def environ(self):
        """This method showcases TG's access to the wsgi environment."""
        return dict(page='environ', environment=request.environ)

    @expose('jistdocstore.templates.data')
    @expose('json')
    def data(self, **kw):
        """This method showcases how you can use the same controller for a data page and a display page"""
        return dict(page='data', params=kw)
    @expose('jistdocstore.templates.index')
    #@require(predicates.has_permission('manage', msg=l_('Only for managers')))
    def manage_permission_only(self, **kw):
        """Illustrate how a page for managers only works."""
        return dict(page='managers stuff')

    @expose('jistdocstore.templates.index')
    @require(predicates.is_user('editor', msg=l_('Only for the editor')))
    def editor_user_only(self, **kw):
        """Illustrate how a page exclusive for the editor works."""
        return dict(page='editor stuff')

    @expose('jistdocstore.templates.login')
    def login(self, came_from=lurl('/')):
        """Start the user login."""
        login_counter = request.environ.get('repoze.who.logins', 0)
        if login_counter > 0:
            flash(_('Wrong credentials'), 'warning')
        return dict(page='login', login_counter=str(login_counter),
                    came_from=came_from)

    @expose()
    def post_login(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on successful
        authentication or redirect her back to the login page if login failed.

        """
        if not request.identity:
            login_counter = request.environ.get('repoze.who.logins', 0) + 1
            redirect('/login',
                params=dict(came_from=came_from, __logins=login_counter))
        userid = request.identity['repoze.who.userid']
        flash(_('Welcome back, %s!') % userid)
        redirect(came_from)

    @expose()
    def post_logout(self, came_from=lurl('/')):
        """
        Redirect the user to the initially requested page on logout and say
        goodbye as well.

        """
        flash(_('We hope to see you soon!'))
        redirect(came_from)
