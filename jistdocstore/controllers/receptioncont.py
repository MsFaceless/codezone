# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission
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
__all__ = ['ReceptionController']


class ReceptionController(BaseController):
    """Sample controller-wide authorization"""
    
    #The predicate that must be met for all the actions in this controller:
    allow_only = has_any_permission('manage','reception',msg=l_('Only for people with the "manage" permission'))

    @expose()
    def index(self):
        redirect('receptioncont/menu')

    @expose('jistdocstore.templates.receptionindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Reception: Main Menu') 

    @expose('jistdocstore.templates.receptionconsole')
    def reception_console(self,**named):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        statcodeall  = DBS_ContractData.query(JistContractStatusCodes).all()
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
                    productionlist.append({'user_id':point.user_id,
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
                for permis in userpermissions:
                    #print permis.permission_name
                    if permis.permission_name=='production':
                        productionlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name,
                                          'display_name':point.display_name
                                          })
        thishourrange = [hours for hours in range(06,20)]
        thisminrange =  [minutes for minutes in range(00,60,15)]
        thistimerange = [(thishour,thismin) for thishour in thishourrange for thismin in thisminrange]
        #for x in range(0,61,15):
        #    print x
        return dict(page='Reception Console',
                    userlist =productionlist, 
                    wip = contracts,
                    timeperiod = range(1,9),
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.telephone_message_new')
    def telephone_messages(self,**named):
        """Handle the 'telephone messages' page."""
        #ajax_form = AjaxForm(id="myAjaxForm",
        #            fields=ReceptionTelephoneMessage(),
        #            target="output",
        #            action="do_save_new_message")
        #tmpl_context.form = ajax_form 
        tmpl_context.form = add_new_reception_message

        return dict(page='Telephone messages search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def do_save_new_message(self, **kw):
        #listname = ['call_again','call_back','no_message']
        #for k,w in kw.iteritems():
        #    print k, w
        #return
        #del kw['sprox_id']
        newmessage = JistReceptionTelephoneMessages()
        #for k,w in kw.iteritems():
        #    print k,w
        #print kw['call_again']
        #print kw['call_back']
        #print kw['no_message']
        #newmessage.call_again = kw['call_again']
        #newmessage.call_back =kw['call_back']
        #newmessage.no_message =kw['no_message']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newmessage.to_user = kw['toperson']
        newmessage.from_person =kw['telephonecall_person_calling']
        newmessage.message =kw['telephonecall_message']
        newmessage.return_tel =kw['telephonecall_returnno']
        newmessage.useridnew = usernow.user_id
        DBS_ContractData.add(newmessage)
        #DBS_ContractData.flush()
        #redirect('/receptioncont/telephone_messages')

    #@require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.telephone_messages_all')
    def telephone_messages_all(self,**named):
        """Handle the 'telephone messages' page."""
        ajax_form = AjaxForm(id="myAjaxForm1",
                    fields=ReceptionTelephoneDateMessage(),
                    target="output",
                    action="do_search_telephone_messages")
        tmpl_context.form = ajax_form 
        #tmpl_context.form = add_new_reception_message

        return dict(page='Telephone messages search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)
    
    @expose()
    #@validate(ajax_form)
    def do_search_telephone_messages(self, **kw):
        if not kw['dateadded']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                requestdate = w.split('-')
                year =w.split('-')[0]
                month =w.split('-')[1]
                day =w.split('-')[2]
        if year==str(0):
            today = datetime.date(datetime.now())
            tup = today.timetuple()
        else:
            today = date(int(year),int(month),int(day))
            tup = today.timetuple()
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(today,sttimestart)
        enddate = datetime.combine(today,sttimeend)
        openorders = DBS_ContractData.query(JistReceptionTelephoneMessages).filter(JistReceptionTelephoneMessages.dateadded>=startdate). \
                                              filter(JistReceptionTelephoneMessages.dateadded<=enddate). \
                                              order_by(desc(JistReceptionTelephoneMessages.dateadded)).  \
                                              all()
        datenow = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        supplier_text = "<H3 align='center'>Messages For %s</H3><p/>"%datenow
        table = "<table class='tablecontractdata'>"

        headerdata = """
                    <th>To User</th>
                    <th>From Person </th>
                    <th>Message</th>
                    <th>Return Tel Number</th>
                    <th>Added By</th>
                    <th>Date Time Added</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in openorders:
            tr = "<tr class='tablestandard'><td>"
            sitedatatemp = "<img src='/images/staffpics/%s.png' align=right/></td>"%str(k.to_user)
            fromperson =""" 
                            <td>%s</td>
                            """%(k.from_person)
            messg =""" 
                            <td>%s</td>
                            """%(k.message)
            returntel =""" 
                            <td width=20>%s</td>
                            """%(k.return_tel)
            whoadded ="<td><img src='/images/staffpics/%s.png'/></td>"%str(k.useridnew)
            added =""" 
                            <td>%s</td>
                            """%(k.dateadded)
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+"</p>"+tr+sitedatatemp+ \
                    fromperson+ \
                    messg+returntel+whoadded+added+trclose
        sitedata = sitedata+"</table>"
        return sitedata 

    #@require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.outofoffice_movement_new')
    def out_of_office_movement_new(self,**named):
        """Handle the 'telephone messages' page."""
        #ajax_form = AjaxForm(id="myAjaxForm",
        #            fields=ReceptionTelephoneMessage(),
        #            target="output",
        #            action="do_save_new_message")
        #tmpl_context.form = ajax_form 
        tmpl_context.form = add_new_out_of_office_notice

        return dict(page='Telephone Messages New',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def do_save_new_out_of_office_movement(self, **kw):
        newnotice = JistOutOfOfficeNotices()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #for k, w in kw.iteritems():
        #    print k,w
        #print
        #for col in newnotice.__table__._columns:
        #    print col
        #return
        
        if kw['toperson'] == 0:
            kw['toperson'] = 1
        elif kw['toperson'] == '':
            kw['toperson'] = 1
        newnotice.for_user = kw['toperson']
        if kw['outofoffice_otherdestination'] <> "":
            newnotice.other_destination =kw['outofoffice_otherdestination']
        else:
            newnotice.site = kw['sitename']
        newnotice.purpose =kw['outofoffice_purpose']
        newnotice.est_hours_there =kw['outofoffice_est_hours_there']
        newnotice.time_start = kw['outofoffice_timestart']
        newnotice.useridnew = usernow.user_id
        DBS_ContractData.add(newnotice)
        #DBS_ContractData.flush()
        #redirect('/receptioncont/out_of_office_movement_new')

    #@require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.outofoffice_movement_all')
    def out_of_office_movement_all(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=OutOfOfficeDateMovments(),
                    target="output",
                    action="do_search_outofoffice_movements")
        tmpl_context.form = ajax_form 
        #tmpl_context.form = add_new_reception_message

        return dict(page='Out of Office search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_outofoffice_movements(self, **kw):
        if not kw['dateadded']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                requestdate = w.split('-')
                year =w.split('-')[0]
                month =w.split('-')[1]
                day =w.split('-')[2]
        if year==str(0):
            today = datetime.date(datetime.now())
            tup = today.timetuple()
        else:
            today = date(int(year),int(month),int(day))
            tup = today.timetuple()
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(today,sttimestart)
        enddate = datetime.combine(today,sttimeend)
        openorders = DBS_ContractData.query(JistOutOfOfficeNotices).filter(JistOutOfOfficeNotices.dateadded>=startdate). \
                                              filter(JistOutOfOfficeNotices.dateadded<=enddate). \
                                              order_by(desc(JistOutOfOfficeNotices.dateadded)).  \
                                              all()
        datenow = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        supplier_text = "<H3 align='center'>Out Of Office Movements For %s</H3><p/>"%datenow
        table = "<table class='tablecontractdata'>"
        headerdata = """
                    <th>For User</th>
                    <th>Site </th>
                    <th>Other Destination</th>
                    <th>Purpose</th>
                    <th>Est Hr There</th>
                    <th>Time Start</th>
                    <th>Added By</th>
                    <th>Date Time Added</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in openorders:
            tr = "<tr class='tablestandard'><td>"
            sitedatatemp = "<img src='/images/staffpics/%s.png'/></td>"%str(k.for_user)
            if k.site:
                thissite = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==k.site).one()
                fromperson =""" 
                                <td>%s</td>
                                """%(thissite.site)
                #print k.site
            else:
                fromperson =""" 
                                <td>%s</td>
                                """%(k.site)

            callback =""" 
                            <td>%s</td>
                            """%(k.other_destination)
            callagain =""" 
                            <td>%s</td>
                            """%(k.purpose)
            nomsgs =""" 
                            <td>%s</td>
                            """%(k.est_hours_there)
            messg =""" 
                            <td>%s</td>
                            """%(k.time_start)
            returntel ="<td><img src='/images/staffpics/%s.png'/></td>"%str(k.useridnew)
            added =""" 
                            <td>%s</td>
                            """%(k.dateadded)
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+"</p>"+tr+sitedatatemp+ \
                    fromperson+callback+callagain+nomsgs+ \
                    messg+returntel+added+trclose
        sitedata = sitedata+"</table>"
        return sitedata 

