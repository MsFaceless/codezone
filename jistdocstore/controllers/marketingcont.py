# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, Any
from tg.decorators import paginate
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import JistFileStoreMarketing
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
from babel.numbers import format_currency, format_number, format_decimal
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')

__all__ = ['MarketingController']


class MarketingController(BaseController):
    """Sample controller-wide authorization"""
    
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))

    allow_only = Any(
            has_permission('manage'),
            has_permission('marketingmanage'),
            has_permission('marketing'),
                     msg=l_('Only for people with the "marketing" permission'))
    @expose()
    def index(self):
        redirect('marketingcont/menu')

    @expose('jistdocstore.templates.marketing.marketingindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Marketing: Main Menu') 
    

    @expose('jistdocstore.templates.marketing.marketing_clients_all')
    def view_all_clientleads(self,**named):
        """Handle the 'client_leads' page."""
        tmpl_context.widget = spx_marketing_client_list
        value = marketing_client_list_filler.get_value(values={},offset=0,order_by='id',desc=True)
        from tg.decorators import paginate
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        #LastMonthLastDate = datetime.today.adddays(0 - datetime.today.day);
        LastMonthLastDate = datetime.today()
        #LastMonthFirstDate = LastMonthLastDate.adddays(1 - LastMonthLastDate.day);
        #print LastMonthLastDate  #,LastMonthFirstDate
        #return

        items = currentPage.items
        return dict(page='View All Active Clients / Leads',
                    wip = items,
                    selfname = 'view_all_clientleads',
                    thiscurrentPage=currentPage,
                    count=count)

    @expose('jistdocstore.templates.marketing.marketing_client_new')
    def add_new_client_lead(self, **kw):
        """Handle the 'new contract' page."""
        tmpl_context.form = add_new_mar_client_form
        return dict(page='Add New Client / Lead',
                    selfname = 'add_new_client_lead',
                    action='/marketingcont/savenewclientlead'
                    )

    @expose()
    def savenewclientlead(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_lead = JistMarketingClientLeads(
                            date = kw['date'],
                            client_name = kw['client_name'],
                            contact_person = kw['contact_person'],
                            site_location = kw['site_location'],
                            contact_tel = kw['contact_tel'],
                            point_person = kw['point_person'],
                            last_followup_date = kw['last_followup_date'],
                            next_followup_date = kw['next_followup_date'],
                            comments = kw['comments'],
                            dateedited = datetime.date(datetime.now()), 
                            dateadded = datetime.date(datetime.now()), 
                            useridnew = usernow.user_id,
                            useridedited = usernow.user_id 
                                       )

        DBS_JistMarketing.add(new_lead)
        DBS_JistMarketing.flush()

        flash("New Client Lead successfully saved.")

        redirect("/marketingcont/view_all_clientleads")
                
    @expose('jistdocstore.templates.marketing.marketing_edit_client_one')
    def editclientleadone(self,*arg,**named):
        val = clientlead_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = clientlead_list_form 

        return dict(page='Edit Clients / Leads Data',
                   action='/marketingcont/saveeditclientleadone/'+str(arg[0]),
                   value=val,
                   )

    @expose()
    def saveeditclientleadone(self,*arg,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        leaddata = DBS_JistMarketing.query(JistMarketingClientLeads). \
                filter(JistMarketingClientLeads.id==arg[0]). \
                one()
        leaddata.date = kw['date']
        leaddata.client_name = kw['client_name']
        leaddata.contact_person = kw['contact_person']
        leaddata.site_location = kw['site_location']
        leaddata.contact_tel = kw['contact_tel']
        leaddata.point_person = kw['point_person']
        leaddata.last_followup_date = kw['last_followup_date']
        leaddata.next_followup_date = kw['next_followup_date']
        leaddata.comments = kw['comments']
        leaddata.dateedited = datetime.date(datetime.now()) 
        leaddata.useridedited = usernow.user_id 
        if type(kw['active'])==list:
            leaddata.active = 1
        elif type(kw['active'])==unicode:
            leaddata.active = 0
        else:
            pass

        flash("Client / Lead Data successfully edited.")
        redirect("/marketingcont/view_all_clientleads")

    @expose('jistdocstore.templates.marketing.marketing_clients_one')
    def view_one_client_lead(self,leadid,**named):
        """Handle the 'client_leads' page."""
        clientdata=DBS_JistMarketing.query(JistMarketingClientLeads).get(leadid)

        return dict(page='View One Client: ',
                    #wip = items,
                    clientdata = clientdata,
                    selfname = 'view_one_client_lead',
                    )
