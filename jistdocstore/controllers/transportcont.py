# -*- coding: utf-8 -*-
from tg.decorators import paginate
from tg import expose, flash, require, url, request, redirect, response, tmpl_context
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from tg.predicates import has_permission,has_any_permission,in_any_group 
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jist_transport_reportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import FileStoreProduction
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
from datetime import datetime, date, time
from babel.numbers import format_currency, format_number, format_decimal

from reportlab.platypus import *
__all__ = ['TransportController']


class TransportController(BaseController):
    """Sample controller-wide authorization"""
    
    def __init__(self):
        self.last_saved_new_fleet = ''

    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def index(self):
        redirect('transportcont/menu')

    @expose('jistdocstore.templates.transport.transportindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Transport: Main Menu') 

    ##############################################################################################################
    #########################Start of New Async Code - ###########################################################
    ##############################################################################################################

    @expose('jistdocstore.templates.transport.transportconsole')
    def transport_console(self,**named):
        allactivedrivers = DBS_JistFleetTransport.query(JistFleetDriverList). \
                filter(JistFleetDriverList.active==1). \
                all()
        allactivefleet = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                all()
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                order_by(desc(JistFleetList.id)). \
                all()
        linkedlist = DBS_JistFleetTransport.query(JistTransportFleetLink). \
                order_by(asc(JistTransportFleetLink.id)). \
                all()
        linklistids = []
        for m in linkedlist:
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==m.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()
            linklistids.append({
                                'fleet_id':thisfleet.id,
                                'registration_number':thisfleet.registration_number,
                                'vehicle_description':thisfleet.vehicle_description,
                                'driver': thisdriver.driver_name
                               })

        return dict(page='Transport Console',
                    wip = '',
                    activedrivers = allactivedrivers,
                    activefleet = allactivefleet,
                    transport_resources_list = linklistids,
                    timeperiod = range(1,120),
                    tripsno = range(1,150),
                    kmsno = range(1,1500),
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.transport.fleetconsole')
    def fleet_console(self,**named):
        allactivedrivers = DBS_JistFleetTransport.query(JistFleetDriverList). \
                filter(JistFleetDriverList.active==1). \
                all()
        allactivefleet = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                all()
        return dict(page='Fleet Console',
                    wip = '',
                    activedrivers = allactivedrivers,
                    activefleet = allactivefleet,
                    currentPage=1,
                    value=named,
                    value2=named)

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.transport_req_console')
    def transport_req_console(self,**named):
        """Handle the 'jist console transport'."""
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
                  order_by(desc(JistContracts.jno))
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        return dict(page='Transport Requests Console',
                    myjistid = myid,
                    activeusers = activeusers,
                    wip = contracts)

    @expose()
    def save_new_transport_req(self,**kw):
        """Handle the 'transport req save' page."""
        #for k, w in kw.iteritems():
            #print k, w
        #return  '2222'
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newlist = JistTransportList()
        newlist.jcno = kw['del_jcno'] 
        newlist.date_required = kw['del_date_required']
        newlist.from_place  = kw['from_start']
        newlist.from_area = kw['from_area']
        newlist.from_address = kw['from_address']
        newlist.from_contact = kw['from_contact']
        newlist.to_place  = kw['to_end']
        newlist.to_area  = kw['to_area']
        newlist.to_address = kw['to_address']
        newlist.to_contact = kw['to_contact']
        newlist.special_inst = kw['transport_instructions']
        newlist.request_person = kw['request_person']
        newlist.useridnew = usernow.user_id 
        DBS_JistFleetTransport.add(newlist)
        DBS_JistFleetTransport.flush()
        return str(newlist.id)

    @expose()
    def get_new_waybill_form(self,reqid,**kw):
        htmltbl = """
                    <form id="new_way_bill_form">
                    <fieldset>
                    <legend>Loading Bill Item</legend>
                        <label for="">Req ID</label>
                        <input type="text" value="%s" name="bill_reqid" disabled='disabled' id="bill_reqid" class="text ui-widget-content ui-corner-all" />
                        <label for="">Item</label>
                        <input type="text" name="bill_item" id="bill_item" class="text ui-widget-content ui-corner-all" />
                        <label for="">Description</label>
                        <input type="text" name="bill_description" id="bill_description" class="text ui-widget-content ui-corner-all" />
                        <label for="">Unit</label>
                        <input type="text" name="bill_unit" id="bill_unit" class="text ui-widget-content ui-corner-all" />
                        <label for="">Quantity</label>
                        <input type="text" name="bill_qty" id="bill_qty" class="text ui-widget-content ui-corner-all" />
                        <button class="ui-widget ui-widget-content ui-state-default" id="btn_save_new_way_bill">Add To Loading Bill</button>
                    </fieldset>
                    </form>
                    """%(reqid)
        return htmltbl 

    @expose()
    def save_new_way_bill(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newbill = JistTransportLoadingBill()
        newbill.req_id = kw['bill_reqid']
        newbill.item = kw['bill_item']
        newbill.description = kw['bill_description']
        newbill.unit = kw['bill_unit']
        newbill.qty = kw['bill_qty']
        newbill.active = True
        newbill.useridnew = usernow.user_id
        newbill.useridedited = usernow.user_id
        newbill.dateedited = datetime.now()
        newbill.dateadded = datetime.now()
        DBS_JistFleetTransport.add(newbill)
        DBS_JistFleetTransport.flush()

    @expose()
    def save_edit_way_bill(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        translist = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                filter(JistTransportLoadingBill.id==kw['loading_waybill_id']). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #newbill = JistTransportLoadingBill()
        #newbill.req_id = kw['bill_reqid']
        translist.item = kw['loading_item']
        translist.description = kw['loading_description']
        translist.unit = kw['loading_unit']
        translist.qty = kw['loading_qty']
        #newbill.active = True
        #newbill.useridnew = usernow.user_id
        translist.dateedited = datetime.now()
        translist.useridedited = usernow.user_id
        DBS_JistFleetTransport.flush()

    @expose()
    def get_transportreq_loading_all(self,reqid,**kw):
        wip1 = []
        loadinglist = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                filter(JistTransportLoadingBill.req_id==reqid). \
                filter(JistTransportLoadingBill.active==True). \
                order_by(desc(JistTransportLoadingBill.id)). \
                all()
        outputlist = []
        for k in loadinglist:
            outputlist.append({
                         'id':k.id,
                         'req_id':k.req_id,
                         'item':k.item,
                         'description':k.description,
                         'unit':k.unit,
                         'qty':k.qty,
                         'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                         'dateadded': k.dateadded,
                         'dateedited': k.dateedited,
                         'active':k.active,
                         })
        headers =["ID","Item","Description","Unit","Qty","Added By","Date Added","Date Edited","Active"]
        dictlist = ['id','item','description','unit','qty','useridnew','dateadded','dateedited','active']
        headerwidths=[50,80,300,80,80,80,80,80,80]
        tdclassnames=['','','','','','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_req_loading")
        loadinglist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id==reqid). \
                one()
        usernow = User.by_user_id(loadinglist.request_person)
        htmlbuttonadd = """
                     <button id="btn_add_transport_loading" name="btn_add_transport_loading">Add To Way Bill</button>
                     """
        html = """
               <h4 class="modal-content">
               <span class='spanleft'>Req ID: %s</span>
               <span class='spanleft30'>From: %s</span>
               <span class='spanleft60'> To: %s </span>
               <span class='spanright'> By User: %s</span>
               </h4>
               """%(reqid,loadinglist.from_place, loadinglist.to_place,usernow.user_name)
        htmlbutton = """
                     <button id="btn_close_transport_loading" name="btn_close_transport_loading">Close Loading Bill</button>
                     """
        htmladd_edit = """
                <div id="transport_dialog_loading_new_div"></div> 
                <div id="transport_dialog_loading_edit_div"></div> 
                """
        pdfstring = """
                        <a
                        href='/transportcont/export_transport_waybill_byid_pdf?reqid=%s'> 
                        <img src="/images/pdficon.jpg"></img>Export Waybill To PDF</a><p/>

                    """%(reqid)
        return  htmlbuttonadd + pdfstring+ htmladd_edit  + html + htmltbl + htmlbutton

    @expose()
    def get_transport_list_active_html(self):
        wip1 = []
        datestart = datetime.date(datetime.now()) - timedelta(weeks=5)
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.dateadded > datestart). \
                order_by(desc(JistTransportList.id)). \
                all()
        for k in translist:
            print k

        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            outputlist.append({
                         'id':k.id,
                         'date_required':k.date_required,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':"<img src='/images/staffpics/%s.png'></img>"%k.request_person,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'datescheduled':k.date_scheduled,
                         'loading_items_sum':loadinglist_sum,
                         'doschedule':"<img src='/images/dates.png'></img>",
                         'showloading':"<img src='/images/clipboard_32.png'></img>",
                         'active':k.active,
                         })
        headers =["ID","Date Required","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","Scheduled","","Items On Waybill","Schedule","Way Bill"]
        dictlist = ['id','date_required','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled','spacer',"loading_items_sum","doschedule","showloading"]
        headerwidths=[50,80,100,100,100,100,'',50,80,50,35,50,32,32]
        tdclassnames=['','','','','','','','','','','tdspacer','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        return htmltbl

    @expose()
    def get_transport_list_by_me_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.request_person==usernow.user_id). \
                order_by(desc(JistTransportList.id)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            outputlist.append({
                         'id':k.id,
                         'date_required':k.date_required,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':"<img src='/images/staffpics/%s.png'></img>"%k.request_person,
                         'dateadded':k.dateadded,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'datescheduled':k.date_scheduled,
                         'loading_items_sum':loadinglist_sum,
                         'showloading':"<img src='/images/clipboard_32.png'></img>",
                         'completed':"<img src='/images/%s.png'></img>"%k.completed,
                         'datecompleted':k.date_completed,
                         'active':k.active,
                         })
        headers =["ID","Date Required","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","","Scheduled","Date Scheduled","Items On Waybill","Loading Bill","Completed","Date Completed"]
        dictlist = ['id','date_required','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','spacer','scheduled','datescheduled',"loading_items_sum","showloading","completed","datecompleted"]
        headerwidths=[50,80,100,100,100,100,'',50,80,35,80,50,50,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_my_reqs")
        return htmltbl

    def build_transport_html_table(self,dictlist,headers,headerwidths,outputlist,tdclassnames,tblname):
        htmltbl = """
                    <table id = "%s" width="100%%">
                   """%tblname
        for i,head in enumerate(headers):
            htmltemp1 = """
                    <th width=%s>%s</th>
                        """%(headerwidths[i],head)
            htmltbl = htmltbl + htmltemp1
        
        for i,lab in enumerate(outputlist):
            htmltbl = htmltbl + "<tr>" 
            for i, dict in enumerate(dictlist):
                htmltemp1 = """<td class="%s">%s</td>"""%(tdclassnames[i],lab[dictlist[i]])
                #print htmltemp1
                htmltbl = htmltbl + htmltemp1
            htmltbl = htmltbl + "</tr>" 
        htmltbl = htmltbl + "</table>"
        return htmltbl 
    
    @expose()
    def get_transport_scheduled_trips_html(self):
        wip1 = []
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                order_by(desc(JistTransportList.id)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()
            outputlist.append({
                         'id':k.id,
                         'date_required':k.date_required,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':"<img src='/images/staffpics/%s.png'></img>"%k.request_person,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'datescheduled':k.date_scheduled,
                         'timescheduled':thisschedule.schedule_time,
                         'loading_items_sum':loadinglist_sum,
                         'driver':thisdriver.driver_name,
                         'doschedule':"<img src='/images/dates.png'></img>",
                         'docomplete':"<img src='/images/shopping_cart_accept32.png'></img>",
                         'dounschedule':"<img src='/images/arrow-left.png'></img>",
                         'active':k.active,
                         })
        headers =["ID","Date Required","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","","Date Scheduled",
                "Time Scheduled","Driver","Items On Waybill","Edit Schedule","Un Schedule","Mark Complete"]
        dictlist = ['id','date_required','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','spacer','datescheduled',
                'timescheduled','driver',"loading_items_sum","doschedule","dounschedule","docomplete"]
        headerwidths=[50,80,100,100,100,100,'',50,80,50,35,50,50,50,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_scheduled")
        pdfstring = """
                        <a
                        href='/transportcont/export_all_transport_reqs_scheduled_pdf'><p/> 
                        <img src="/images/pdficon.jpg"></img>Export All Scheduled To PDF</a>
                        

                    """
        return pdfstring + htmltbl

    @expose()
    def schedule_transport_req(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id==kw['req_id']). \
                one()
        #if translist.scheduled == True; Update the info only else create new schedule
        if translist.scheduled: #update the info
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == kw['req_id']). \
                    one()
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            useridcreated = usernow.user_id
            thisschedule.fleet_id = kw['schedule_fleet_id']
            thisschedule.schedule_date = kw['schedule_date_this']
            thisschedule.schedule_time = kw['schedule_timestart']
            thisschedule.estimate_duration_hrs = kw['schedule_duration']
            thisschedule.estimate_kms = kw['schedule_kms']
            thisschedule.estimate_trips = kw['schedule_trips']
            thisschedule.useridedited=useridcreated
            #Update the schedule information in the TransporList Table
            translist.scheduled = 1
            translist.date_scheduled  = kw['schedule_date_this']
        else:   #create new schedule
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            useridcreated = usernow.user_id
            newschedule = JistTransportScheduling()
            newschedule.fleet_id = kw['schedule_fleet_id']
            newschedule.req_id = kw['req_id']
            newschedule.schedule_date = kw['schedule_date_this']
            newschedule.schedule_time = kw['schedule_timestart']
            newschedule.estimate_duration_hrs = kw['schedule_duration']
            newschedule.estimate_kms = kw['schedule_kms']
            newschedule.estimate_trips = kw['schedule_trips']
            newschedule.active = 1 
            newschedule.useridnew=useridcreated
            newschedule.useridedited=useridcreated
            DBS_JistFleetTransport.add(newschedule)
            #Update the schedule information in the TransporList Table
            translist.scheduled = 1
            translist.date_scheduled  = kw['schedule_date_this']
            DBS_JistFleetTransport.flush()
            
    @expose()
    def schedule_transport_req_edit(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id==kw['req_id_edit']). \
                one()
        #if translist.scheduled == True; Update the info only else create new schedule
        if translist.scheduled: #update the info
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == kw['req_id_edit']). \
                    one()
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            useridcreated = usernow.user_id
            thisschedule.fleet_id = kw['schedule_fleet_id_edit']
            thisschedule.schedule_date = kw['schedule_date_edit']
            thisschedule.schedule_time = kw['schedule_timestart_edit']
            thisschedule.estimate_duration_hrs = kw['schedule_duration_edit']
            thisschedule.estimate_kms = kw['schedule_kms_edit']
            thisschedule.estimate_trips = kw['schedule_trips_edit']
            thisschedule.useridedited=useridcreated
            #Update the schedule information in the TransporList Table
            translist.scheduled = 1
            translist.date_scheduled  = kw['schedule_date_edit']
            DBS_JistFleetTransport.flush()
            
    @expose()
    def unschedule_transport_req(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id==kw['req_id']). \
                one()
        #if translist.scheduled == True; Update the info only else create new schedule
        if translist.scheduled: #update the info
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == kw['req_id']). \
                    one()
            #delete thisschedule
            DBS_JistFleetTransport.delete(thisschedule)

            #Update the schedule information in the TransporList Table
            translist.scheduled = 0
            translist.date_scheduled  = None 
            DBS_JistFleetTransport.flush()

    @expose()
    def get_transport_drivers_schedules_by_date_html(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        #driverid = kw['schedule_driver_name']
        scheduledate = kw['schedule_date']

        wip1 = []
        #filter(JistTransportScheduling.fleet_id==driverid). \
        translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                filter(JistTransportList.date_scheduled==scheduledate). \
                order_by(asc(JistTransportScheduling.schedule_time)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()

            outputlist.append({
                         'id':k.id,
                         'date_required':k.date_required,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':"<img src='/images/staffpics/%s.png'></img>"%k.request_person,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'datescheduled':k.date_scheduled,
                         'timescheduled':thisschedule.schedule_time,
                         'loading_items_sum':loadinglist_sum,
                         'driver':thisdriver.driver_name,
                         'active':k.active,
                         })
        headers =["ID","Date Required","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","","Date Scheduled","Time Scheduled","Driver","Items On Waybill"]
        dictlist = ['id','date_required','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','spacer','datescheduled','timescheduled','driver',"loading_items_sum"]
        headerwidths=[50,80,100,100,100,100,'',50,80,50,35,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_transport_drivers_schedule")
        pdfstring = """
                        <a
                        href='/transportcont/export_driver_schedule_bydate_pdf?scheduledate=%s'><p/> 
                        <img src="/images/pdficon.jpg"></img>Export Driver Schedule All - By Date - To PDF</a>

                    """%(scheduledate)
        #print pdfstring
        return pdfstring + htmltbl

    @expose()
    def get_transport_drivers_tripsheets_html(self,**kw):
        for k, w in kw.iteritems():
            print k, w
        print "This here"
        return
        #driverid = kw['schedule_driver_name']
        tripdate = kw['trip_sheet_date']
        tripfleetid = kw['trip_sheet_fleet_id']

        wip1 = []
        #filter(JistTransportScheduling.fleet_id==driverid). \
        translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                filter(JistTransportList.date_scheduled==scheduledate). \
                order_by(asc(JistTransportScheduling.schedule_time)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()

            outputlist.append({
                         'id':k.id,
                         'date_required':k.date_required,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':"<img src='/images/staffpics/%s.png'></img>"%k.request_person,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'datescheduled':k.date_scheduled,
                         'timescheduled':thisschedule.schedule_time,
                         'loading_items_sum':loadinglist_sum,
                         'driver':thisdriver.driver_name,
                         'active':k.active,
                         })
        headers =["ID","Date Required","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","","Date Scheduled","Time Scheduled","Driver","Items On Waybill"]
        dictlist = ['id','date_required','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','spacer','datescheduled','timescheduled','driver',"loading_items_sum"]
        headerwidths=[50,80,100,100,100,100,'',50,80,50,35,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_transport_drivers_schedule")
        pdfstring = """
                        <a
                        href='/transportcont/export_driver_schedule_bydate_pdf?scheduledate=%s'><p/> 
                        <img src="/images/pdficon.jpg"></img>Export Driver Schedule All - By Date - To PDF</a>

                    """%(scheduledate)
        #print pdfstring
        return pdfstring + htmltbl


    @expose()
    def get_transport_drivers_schedules_html(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        driverid = kw['schedule_driver_name']
        scheduledate = kw['schedule_driver_date']

        wip1 = []
        translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                filter(JistTransportList.date_scheduled==scheduledate). \
                filter(JistTransportScheduling.fleet_id==driverid). \
                order_by(asc(JistTransportScheduling.schedule_time)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()

            outputlist.append({
                         'id':k.id,
                         'date_required':k.date_required,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':"<img src='/images/staffpics/%s.png'></img>"%k.request_person,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'datescheduled':k.date_scheduled,
                         'timescheduled':thisschedule.schedule_time,
                         'loading_items_sum':loadinglist_sum,
                         'driver':thisdriver.driver_name,
                         'active':k.active,
                         })
        headers =["ID","Date Required","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","","Date Scheduled","Time Scheduled","Driver","Items On Waybill"]
        dictlist = ['id','date_required','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','spacer','datescheduled','timescheduled','driver',"loading_items_sum"]
        headerwidths=[50,80,100,100,100,100,'',50,80,50,35,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_transport_drivers_schedule")
        pdfstring = """
                        <a
                        href='/transportcont/export_driver_schedule_byid_pdf?fleetid=%s&scheduledate=%s'><p/> 
                        <img src="/images/pdficon.jpg"></img>Export This Driver Schedule To PDF</a>

                    """%(driverid,scheduledate)
        #print pdfstring
        return pdfstring + htmltbl

    @expose()
    def get_edit_dialog_schedule(self,**kw):
        thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                filter(JistTransportScheduling.req_id == kw['req_id_edit']). \
                one()
        thisreq = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id == kw['req_id_edit']). \
                one()
        allactivedrivers = DBS_JistFleetTransport.query(JistFleetDriverList). \
                filter(JistFleetDriverList.active==1). \
                all()
        allactivefleet = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                all()
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                order_by(desc(JistFleetList.id)). \
                all()
        linkedlist = DBS_JistFleetTransport.query(JistTransportFleetLink). \
                order_by(asc(JistTransportFleetLink.id)). \
                all()
        resource_list = []
        for m in linkedlist:
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==m.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()
            resource_list.append({
                                'fleet_id':thisfleet.id,
                                'registration_number':thisfleet.registration_number,
                                'vehicle_description':thisfleet.vehicle_description,
                                'driver': thisdriver.driver_name
                               })
        timeperiod = range(1,120)
        tripsno = range(1,150)
        kmsno = range(1,1500)

        html1 = """
        <div id="dialog_schedule_transport_edit" title="Edit Schedule Transport Trip">
            <form id="dialog_transport_schedule_frm_edit">
                <fieldset>
                    <label for="">Requisition Item</label>
                    <input value="%s" id="req_id_edit" name="req_id_edit" class="text ui-widget-content ui-corner-all" /><br/>
                    <label for="">Transport Resource</label><br/>
                  <select id='schedule_fleet_id_edit' name='schedule_fleet_id_edit' class="text ui-widget-content ui-corner-all" >
                """%thisreq.id
        html2 = ''
        for m in resource_list: 
            if thisschedule.fleet_id == m['fleet_id']:
                html2temp = """
                              <option selected = 'selected' value="%s">%s - %s - %s</option>
                        """%(m['fleet_id'],m['driver'],m['vehicle_description'],m['registration_number'])
                html2 = html2 + html2temp
            else:
                html2temp = """
                              <option value="%s">%s - %s - %s</option>
                        """%(m['fleet_id'],m['driver'],m['vehicle_description'],m['registration_number'])
                html2 = html2 + html2temp


        html3 = """
                  </select>
                  <br/>
                    <label for="">Date To Schedule</label>
                    <input value="%s" id="schedule_date_edit" name="schedule_date_edit" class="text ui-widget-content ui-corner-all" /><br/>

                  <br/>
                    <label for="schedule_est_hours_there_edit">Anticipated Duration (Hrs)</label>
                """%(thisreq.date_scheduled)
        html4 = """
                  <select id='schedule_duration_edit' name='schedule_duration_edit' class="text ui-widget-content ui-corner-all" >
                        """
        for m in timeperiod:
            if thisschedule.estimate_duration_hrs == m:
                html4temp = """
                          <option selected = 'selected' value="%s">%s</option>
                    """%(m,m)
                html4 = html4 + html4temp
            else:
                html4temp = """
                          <option value="%s">%s</option>
                    """%(m,m)
                html4 = html4 + html4temp

        html5 = """
                        </select>
                    <br/>
                    <label for="schedule_trips_edit">Anticipated Trips</label>
                        <select id="schedule_trips_edit" name="schedule_trips_edit" class="text ui-widget-content ui-corner-all">
                """
        html6 = """
                        <option id="schedule_trips_edit" value="">Select one...</option>
                              <option value="${x}">${x}</option>
                          </div>
                """
        for m in timeperiod:
            if thisschedule.estimate_trips == m:
                html6temp = """
                          <option selected = 'selected' value="%s">%s</option>
                    """%(m,m)
                html6 = html6 + html6temp
            else:
                html6temp = """
                          <option value="%s">%s</option>
                    """%(m,m)
                html6 = html6 + html6temp

        html7 = """
                        </select>
                    <br/>
                    <label for="schedule_kms_edit">Anticipated KM's</label>
                    <select id="schedule_kms_edit" name="schedule_kms_edit" class="text ui-widget-content ui-corner-all">
                """
        for m in kmsno:
            if thisschedule.estimate_kms == m:
                html7temp = """
                          <option selected = 'selected' value="%s">%s</option>
                    """%(m,m)
                html7 = html7 + html7temp
            else:
                html7temp = """
                          <option value="%s">%s</option>
                    """%(m,m)
                html7 = html7 + html7temp

        html8 = """
                        </select>
                    <br/>
                    <label for="schedule_timestart_edit">Time To Start</label>
                    <input value='%s' type="text" name="schedule_timestart_edit" id="schedule_timestart_edit" class="ui-widget-content ui-corner-all"/><br/>
                  <br/>
                </fieldset>
            </form>
            </div>

               """%(thisschedule.schedule_time)
        #for m in :
            #if thisschedule.schedule_time == m:
                #html8temp = """
                          #<option selected = 'selected' value="%s">%s</option>
                    #"""%(m,m)
                #html8 = html8 + html8temp
            #else:
                #html8temp = """
                          #<option value="%s">%s</option>
                    #"""%(m,m)
                #html8 = html8 + html8temp

        return html1 + html2 + html3 + html4 + html5 + html6 + html7 + html8 

    @expose()
    def get_edit_dialog_loading(self,**kw):
        loadingbill = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                filter(JistTransportLoadingBill.id==kw['req_id_edit']). \
                one()
        html1 = """
        <div id="dialog_loading_transport_edit" title="Edit Waybill">
            <form id="dialog_loading_frm_edit">
                <fieldset>
                    <label for="">Way Bill ID</label><br/>
                    <input value="%s" id="loading_waybill_id" name="loading_waybill_id" class="text ui-widget-content ui-corner-all" /><br/>
                    <label for="">Item</label><br/>
                    <input id='loading_item' value='%s' name='loading_item' class="text ui-widget-content ui-corner-all" ><br/>
                    <label for="">Description</label><br/>
                    <input id='loading_description' value='%s' name='loading_description' class="text ui-widget-content ui-corner-all" ><br/>
                    <label for="">Unit</label><br/>
                    <input id='loading_unit' value='%s' name='loading_unit' class="text ui-widget-content ui-corner-all" ><br/>
                    <label for="">Qty</label><br/>
                    <input id='loading_qty' value='%s' name='loading_qty' class="text ui-widget-content ui-corner-all" ><br/>
                </fieldset>
                </form>
       </div>
                """%(loadingbill.id,loadingbill.item,loadingbill.description,loadingbill.unit,loadingbill.qty)

        return html1

    @expose()
    def get_new_dialog_loading(self,**kw):
        loadingbill = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id==kw['req_id_edit']). \
                one()
        htmltbl = """
                <div id="dialog_loading_transport_new" title="Add New Waybill">
                    <form id="dialog_loading_frm_new">
                        <fieldset>
                            <label for="">Req ID</label><br/>
                            <input id='loading_req_id_edit' value='%s' name='loading_req_id_edit' class="text ui-widget-content ui-corner-all" ><br/>
                            <label for="">Item</label><br/>
                            <input id='loading_item_edit'name='loading_item_edit' class="text ui-widget-content ui-corner-all" ><br/>
                            <label for="">Description</label><br/>
                            <input id='loading_description_edit' name='loading_description_edit' class="text ui-widget-content ui-corner-all" ><br/>
                            <label for="">Unit</label><br/>
                            <input id='loading_unit_edit' name='loading_unit_edit' class="text ui-widget-content ui-corner-all" ><br/>
                            <label for="">Qty</label><br/>
                            <input id='loading_qty_edit' name='loading_qty_edit' class="text ui-widget-content ui-corner-all" ><br/>
                        </fieldset>
                        </form>
               </div>
                        """%(loadingbill.id)
        return htmltbl 

    @expose()
    def save_new_dialog_loading(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newbill = JistTransportLoadingBill()
        newbill.req_id = kw['loading_req_id_edit']
        newbill.item = kw['loading_item_edit']
        newbill.description = kw['loading_description_edit']
        newbill.unit = kw['loading_unit_edit']
        newbill.qty = kw['loading_qty_edit']
        newbill.active = True
        newbill.useridnew = usernow.user_id
        newbill.useridedited = usernow.user_id
        newbill.dateedited = datetime.now()
        newbill.dateadded = datetime.now()
        DBS_JistFleetTransport.add(newbill)
        DBS_JistFleetTransport.flush()

    @expose()
    def export_all_transport_reqs_scheduled_pdf(self, **kw):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Transport-All-Requisitions-Scheduled-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA3(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        translist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                order_by(desc(JistTransportList.id)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            request_person = User.by_user_id(k.request_person)
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()
            outputdata.append({
                         'id':k.id,
                         'date_added':k.date_required,
                         'time_scheduled':thisschedule.schedule_time,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'request_person':request_person.user_name,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'date_scheduled':thisschedule.schedule_date,
                         'loading_items_sum':loadinglist_sum,
                         'doschedule':"<img src='/images/dates.png'></img>",
                         'showloading':"<img src='/images/clipboard_32.png'></img>",
                         'active':k.active,
                         'driver':thisdriver.driver_name,
                         'trips_booked':thisschedule.estimate_trips,
                         'time_booked':thisschedule.estimate_duration_hrs,
                         })
        for x in outputdata:
            outputlist.append((
                             x['id'],
                             x['date_scheduled'],
                             x['time_scheduled'],
                             Paragraph(x['from_place'],pdffile.styleNormal),
                             Paragraph(x['from_area'],pdffile.styleNormal),
                             Paragraph(x['to_place'],pdffile.styleNormal),
                             Paragraph(x['to_area'],pdffile.styleNormal),
                             Paragraph(x['special_inst'],pdffile.styleNormal),
                             Paragraph(x['request_person'],pdffile.styleNormal),
                             x['dateadded'],
                             Paragraph(x['driver'],pdffile.styleNormal),
                             x['trips_booked'],
                             x['time_booked'],
                              ))
        userdata = {
                'title1_header':'Transport:', 'title1':'All Scheduled Requisitions By Date',
                'title2_header':'', 'title2':'',
                'title3_header':'', 'title3':'',
                'title4_header':'', 'title4':'',
                'datenow_header': "Date", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':'',
                'headerl3_header':'', 'headerl3':'',
                'headerl4_header':' ', 'headerl4':' ',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':' ', 'headerr4':' ',
                } 
        headers =["ID","Date Scheduled","Time Scheduled","From Place","From Area","To Place","To Area","Transport Instructions","Requested By", "Date Added","Driver","Trips","Time/Hrs"]
        dictlist = ['id','date_scheduled','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        headerwidths=[50,80,80,100,100,100,100,150,80,100,50,35,50,32,32]
        tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFTransportReport(userdata,outputlist,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent
        
    @expose()
    def export_driver_schedule_byid_pdf(self, **kw):
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Transport-Driver-Schedule-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        fleetid = kw['fleetid']
        scheduledate = kw['scheduledate']

        wip1 = []
        translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                filter(JistTransportList.date_scheduled==scheduledate). \
                filter(JistTransportScheduling.fleet_id==fleetid). \
                order_by(asc(JistTransportScheduling.schedule_time)). \
                all()
        outputlist = []
        thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.id==fleetid). \
                one()
        thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                filter(JistFleetDriverList.id==thisfleet.driver). \
                one()
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()


            outputdata.append({
                         'id':k.id,
                         'date_added':k.date_required,
                         'time_scheduled':thisschedule.schedule_time,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'date_scheduled':thisschedule.schedule_date,
                         'loading_items_sum':loadinglist_sum,
                         'doschedule':"<img src='/images/dates.png'></img>",
                         'showloading':"<img src='/images/clipboard_32.png'></img>",
                         'active':k.active,
                         'driver':thisdriver.driver_name,
                         'trips_booked':thisschedule.estimate_trips,
                         'time_booked':thisschedule.estimate_duration_hrs,
                         })
        for x in outputdata:
            outputlist.append((
                             x['id'],
                             x['time_scheduled'],
                             Paragraph(x['from_place'],pdffile.styleNormal),
                             Paragraph(x['from_area'],pdffile.styleNormal),
                             Paragraph(x['to_place'],pdffile.styleNormal),
                             Paragraph(x['to_area'],pdffile.styleNormal),
                             Paragraph(x['special_inst'],pdffile.styleNormal),
                             x['trips_booked'],
                             x['time_booked'],
                             x['loading_items_sum'],
                              ))
        userdata = {
                'title1_header':'Transport:', 'title1':'Driver Schedule Sheet ',
                'title2_header':'Driver:', 'title2':thisdriver.driver_name,
                'title3_header':'Fleet Reg:', 'title3':thisfleet.registration_number,
                'title4_header':'', '':'', 'title4':'',
                'datenow_header': "Date", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':'',
                'headerl3_header':'', 'headerl3':'',
                'id_header_header': "", 'id_header':'',
                'headerl4_header':'', 'headerl4':' ',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["ID","Time Booked","From Place","From Area","To Place","To Area","Transport Instructions","Est Trips","Est Hrs","Items"]
        dictlist = ['id','date_scheduled','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        headerwidths=[50,70,100,100,100,100,150,50,40,40,50,32,32]
        tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFTransportReport(userdata,outputlist,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_driver_schedule_bydate_pdf(self, **kw):
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Transport-Driver-Schedule-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        #fleetid = kw['fleetid']
        scheduledate = kw['scheduledate']

        wip1 = []
        #filter(JistTransportScheduling.fleet_id==fleetid). \
        translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.scheduled==True). \
                filter(JistTransportList.date_scheduled==scheduledate). \
                order_by(asc(JistTransportScheduling.schedule_time)). \
                all()
        outputlist = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()


            outputdata.append({
                         'id':k.id,
                         'date_added':k.date_required,
                         'time_scheduled':thisschedule.schedule_time,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'date_scheduled':thisschedule.schedule_date,
                         'loading_items_sum':loadinglist_sum,
                         'doschedule':"<img src='/images/dates.png'></img>",
                         'showloading':"<img src='/images/clipboard_32.png'></img>",
                         'active':k.active,
                         'driver':thisdriver.driver_name,
                         'trips_booked':thisschedule.estimate_trips,
                         'time_booked':thisschedule.estimate_duration_hrs,
                         })
        for x in outputdata:
            outputlist.append((
                             x['id'],
                             x['time_scheduled'],
                             Paragraph(x['from_place'],pdffile.styleNormal),
                             Paragraph(x['from_area'],pdffile.styleNormal),
                             Paragraph(x['to_place'],pdffile.styleNormal),
                             Paragraph(x['to_area'],pdffile.styleNormal),
                             Paragraph(x['special_inst'],pdffile.styleNormal),
                             Paragraph(x['driver'],pdffile.styleNormal),
                             x['trips_booked'],
                             x['time_booked'],
                             x['loading_items_sum'],
                              ))
        userdata = {
                'title1_header':'Transport:', 'title1':'Scheduled Requisitions By Date ',
                'title2_header':':', 'title2':'',
                'title3_header':'', 'title3':'',
                'title4_header':'', '':'', 'title4':'',
                'datenow_header': "Date", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':'',
                'headerl3_header':'', 'headerl3':'',
                'id_header_header': "", 'id_header':'',
                'headerl4_header':'', 'headerl4':' ',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["ID","Time Booked","From Place","From Area","To Place","To Area","Transport Instructions","Driver","Est Trips","Est Hrs","Items"]
        #dictlist = ['id','date_scheduled','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        headerwidths=[40,60,90,90,90,90,100,90,50,50,40,40,40,40,50,32,32]
        tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFTransportReport(userdata,outputlist,headers,headerwidths,10)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent


    @expose()
    def export_transport_waybill_byid_pdf(self, **kw):
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Transport-Waybill-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        reqid = kw['reqid']
        loadinglist = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                filter(JistTransportLoadingBill.req_id==reqid). \
                filter(JistTransportLoadingBill.active==True). \
                order_by(desc(JistTransportLoadingBill.id)). \
                all()
        transportlist = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.id==reqid). \
                one()
        requestuser = User.by_user_id(transportlist.request_person)
        outputlist = []
        for k in loadinglist:
            outputdata.append({
                         'id':k.id,
                         'req_id':k.req_id,
                         'item':k.item,
                         'description':k.description,
                         'unit':k.unit,
                         'qty':k.qty,
                         'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                         'dateadded': k.dateadded,
                         'dateedited': k.dateedited,
                         'active':k.active,
                         'request_person': requestuser.user_name,
                         })
        for x in outputdata:
            outputlist.append((
                             x['id'],
                             x['item'],
                             Paragraph(x['description'],pdffile.styleNormal),
                             Paragraph(x['unit'],pdffile.styleNormal),
                             x['qty'],
                              ))
        userdata = {
                'title1_header':'Transport:', 'title1':'Waybill Sheet ',
                'title2_header':'From:', 'title2':transportlist.from_place,
                'title3_header':'To:', 'title3':transportlist.to_place,
                'title4_header':'Requested By:', 'title4':requestuser.user_name,
                'datenow_header': "Date Printed", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'From Area:', 'headerl1':transportlist.from_area,
                'headerl2_header':'From Address:', 'headerl2':transportlist.from_address,
                'headerl3_header':'From Contact:', 'headerl3':transportlist.from_contact,
                'headerl4_header':'', 'headerl4':' ',
                'id_header_header': "Requisition ID:", 'id_header':transportlist.id,
                'headerr1_header':'To Area', 'headerr1':transportlist.to_area,
                'headerr2_header':'To Address', 'headerr2':transportlist.to_address,
                'headerr3_header':'To Contact', 'headerr3':transportlist.to_contact,
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["ID","Item","Description","Unit","Qty","Qty Received","Date Received","Received By - Name","Person Received Sign"]
        dictlist = ['id','','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        headerwidths=[50,70,150,40,40,70,70,100,100,50,32,32]
        #tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFTransportReport(userdata,outputlist,headers,headerwidths,11)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def get_new_dialog_tripsheet(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        #loadingbill = DBS_JistFleetTransport.query(JistTransportList). \
                #filter(JistTransportList.id==kw['req_id_edit']). \
                #one()
        htmltbl1 = """

        <div id="dialog_trip_sheet_transport" title="Transport Trip Sheet">
            <form id="dialog_transport_trip_sheet_frm">
                <fieldset>
                    <label for="">Scheduled Trip</label><br/>
                  <select id='trip_sheet_schedule_id' name='trip_sheet_schedule_id' class="text ui-widget-content ui-corner-all" >
                   """
        fleetid = kw['trip_sheet_fleet_id']
        scheduledate = kw['trip_sheet_date']
        wip1 = []
        #filter(JistTransportList.date_scheduled==scheduledate). \
        translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                filter(JistTransportList.active==True). \
                filter(JistTransportList.completed==False). \
                filter(JistTransportList.scheduled==True). \
                filter(JistTransportScheduling.fleet_id==fleetid). \
                order_by(asc(JistTransportScheduling.schedule_time)). \
                all()
        outputlist = []
        outputdata = []
        for k in translist:
            loadinglist_sum = DBS_JistFleetTransport.query(JistTransportLoadingBill). \
                    filter(JistTransportLoadingBill.req_id==k.id). \
                    filter(JistTransportLoadingBill.active==True). \
                    value(func.count(JistTransportLoadingBill.id))
            thisschedule = DBS_JistFleetTransport.query(JistTransportScheduling). \
                    filter(JistTransportScheduling.req_id == k.id). \
                    one()
            thisfleet = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==thisschedule.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==thisfleet.driver). \
                    one()
            outputdata.append({
                         'id':k.id,
                         'date_added':k.date_required,
                         'time_scheduled':thisschedule.schedule_time,
                         'from_place':k.from_place,
                         'from_area':k.from_area,
                         'to_place':k.to_place,
                         'to_area':k.to_area,
                         'special_inst':k.special_inst,
                         'dateadded':k.dateadded,
                         'scheduled':"<img src='/images/%s.png'></img>"%k.scheduled,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'date_scheduled':thisschedule.schedule_date,
                         'loading_items_sum':loadinglist_sum,
                         'doschedule':"<img src='/images/dates.png'></img>",
                         'showloading':"<img src='/images/clipboard_32.png'></img>",
                         'active':k.active,
                         'driver':thisdriver.driver_name,
                         'trips_booked':thisschedule.estimate_trips,
                         'time_booked':thisschedule.estimate_duration_hrs,
                         })

        htmltbl2 = ''
        for data in outputdata: 
            htmltbltemp2 = """
                          <option value="%s">%s - %s -%s</option>
                       """%(data['id'],data['id'],data['from_place'],data['to_place'])
            htmltbl2 = htmltbl2 + htmltbltemp2
        htmltbl3 = """
                      </select>
                  <br/>
                    <label for="">Date Of Trip Sheet</label>
                    <input id="trip_sheet_date" value="%s" name="trip_sheet_date" readonly="readonly" class="text ui-widget-content ui-corner-all" /><br/>
                    <br/>
                    <label for="">Driver</label>
                    <input id="trip_sheet_driver" value="%s" name="trip_sheet_driver" readonly="readonly" class="text ui-widget-content ui-corner-all" /><br/>
                    <br/>
                    <label for="trip_sheet_from">Trip Sheet From</label>
                    <input type="text" name="trip_sheet_from" id="trip_sheet_from" class="ui-widget-content ui-corner-all"/><br/>
                    <label for="trip_sheet_to">Trip Sheet To</label>
                    <input type="text" name="trip_sheet_to" id="trip_sheet_to" class="ui-widget-content ui-corner-all"/><br/>
                    <label for="trip_sheet_timestart">Time At Start</label>
                    <input type="text" name="trip_sheet_timestart" id="trip_sheet_timestart" class="ui-widget-content ui-corner-all"/><br/>
                    <label for="trip_sheet_timeend">Time At End</label>
                    <input type="text" name="trip_sheet_timeend" id="trip_sheet_timeend" class="ui-widget-content ui-corner-all"/><br/>
                    <label for="trip_sheet_odometer_start">Odometer Start</label>
                    <input type="text" name="trip_sheet_odometer_start" id="trip_sheet_odometer_start" class="ui-widget-content ui-corner-all"/><br/>
                    <label for="trip_sheet_odometer_end">Odometer End</label>
                    <input type="text" name="trip_sheet_odometer_end" id="trip_sheet_odometer_end" class="ui-widget-content ui-corner-all"/><br/>
                    <label for="trip_sheet_file">Upload Waybill</label>
                    <input type="file" name="trip_sheet_file" id="trip_sheet_file" class="ui-widget-content ui-corner-all"/><br/>

                  """%(scheduledate,fleetid)

        editfleet_form3 = """
                </select><br/>
                <label for="">Close Requisition</label>
                <select id="req_active" name="req_active"  class="text ui-widget-content ui-corner-all">
                          """
        if not fleetid:
            editfleet_form4 = """
                    <option id="edit_fleet_active" value="1" selected="selected">True</option>
                    <option id="edit_fleet_active" value="0">False</option>
                            """
        else:
            editfleet_form4 = """
                    <option id="edit_fleet_active" value="1">True</option>
                    <option id="edit_fleet_active" value="0" selected="selected">False</option>
                    """
        end = """
                </fieldset>
            </form>
        </div>

                            """
        return htmltbl1 + htmltbl2 + htmltbl3  + editfleet_form3 + editfleet_form4 + end

    @expose()
    def save_new_tripsheet(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newtrip = JistTransportDailyTripSheets()
        newtrip.schedule_id = kw['trip_sheet_schedule_id']
        newtrip.fleet_id = kw['trip_sheet_driver']
        newtrip.trip_date = kw['trip_sheet_date']
        newtrip.trip_time_start = kw['trip_sheet_timestart']
        newtrip.trip_time_end = kw['trip_sheet_timeend']
        newtrip.odometer_start = kw['trip_sheet_odometer_start']
        newtrip.odometer_end = kw['trip_sheet_odometer_end']
        newtrip.trip_from = kw['trip_sheet_from']
        newtrip.trip_to = kw['trip_sheet_to']
        newtrip.active = True 
        newtrip.useridnew = usernow.user_id
        newtrip.useridedited = usernow.user_id
        newtrip.dateedited = datetime.now()
        newtrip.dateadded = datetime.now()
        DBS_JistFleetTransport.add(newtrip)
        #print kw['req_active']
        #print kw['trip_sheet_schedule_id']
        if kw['req_active'] == '1':
            translist = DBS_JistFleetTransport.query(JistTransportList).join(JistTransportScheduling). \
                    filter(JistTransportScheduling.id==kw['trip_sheet_schedule_id']). \
                    one()
            #print translist.id
            translist.completed = 1
            translist.active = 0
            translist.date_completed = kw['trip_sheet_date']

        DBS_JistFleetTransport.flush()



    @expose()
    def get_something_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                order_by(desc(JistFleetList.id)). \
                all()
        linkedlist = DBS_JistFleetTransport.query(JistTransportFleetLink). \
                order_by(desc(JistTransportFleetLink.id)). \
                all()
        linklistids = []
        for m in linkedlist:
            linklistids.append(m.fleet_id)
        outputlist = []
        for k in fleetlist:
            if not k.id in linklistids:
                thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                        filter(JistFleetDriverList.id==k.driver). \
                        one()
                outputlist.append({
                             'id':k.id,
                             'vehicle_description':k.vehicle_description,
                             'registration_number':k.registration_number,
                             'driver':thisdriver.driver_name,
                             })
        headers =["ID","Registration","Description","Driver"]
        dictlist = ['id','registration_number','vehicle_description','driver']
        headerwidths=[50,80,100,100]
        tdclassnames=['','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_fleet_resources")
        html = """
               <h3 class="ui-widget-shadow">All Active Fleet</h3>  
               """
        return html + htmltbl

    ##############################################################################################################
    #########################End of New Async Code - Or so I think################################################
    ##############################################################################################################

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.transport_all')
    def view_all(self,**named):
        """Handle the 'wip' page."""
        tmpl_context.widget = spx_fleet_list 
        value = fleet_list_filler.get_value(values={},offset=0,order_by='id',desc=True)
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
        return dict(page='wip',
                    wip = items,
                    currentPage=currentPage,
                    count=count)

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.newfleet')
    def newfleet(self, **kw):
        """Handle the 'new contract' page."""
        tmpl_context.widget = add_new_fleet_form
        return dict(newfleet=kw)

    @expose()
    def savenewfleet(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        if self.last_saved_new_fleet == kw['uniqid']:
            return
        new_fleet = JistFleetList(vehicle_description = kw['vehicle_description'],
                                       registration_number=kw['registration_number'],
                                       vin_number = kw['vin_number'],
                                       engine_number = kw['engine_number'],
                                       n_r_number = kw['n_r_number'],
                                       year_model = kw['year_model'],
                                       date_acquired = kw['date_acquired'],
                                       tare = kw['tare'],
                                       fuel_type = kw['fuel_type'],
                                       tank_capacity = kw['tank_capacity'],
                                       fuel_card_number =kw['fuel_card_number'],
                                       fuel_card_expiry_date=kw['fuel_card_expiry_date'],
                                       ext_colour = kw['ext_colour'],
                                       service_center=kw['service_center'],
                                       service_center_tel_no=kw['service_center_tel_no'],
                                       driver=1,
                                       useridnew=useridcreated,
                                       dateadded = datetime.date(datetime.now())
                                       )
        DBS_JistFleetTransport.add(new_fleet)
        DBS_JistFleetTransport.flush()
        self.last_saved_new_fleet = kw['uniqid']

    @expose('jistdocstore.templates.transport.fleet_edit')
    def edit_fleet(self,*arg,**named):
        val = fleet_edit_filler.get_value(values={'id':arg[0]})
        tmpl_context.widget = edit_fleet_form 
        return dict(page='edit fleet',
                   value=val,
                   action = '/transportcont/saveeditfleet/'+arg[0],
                   editid = arg[0]
                   )

    @expose()
    def saveeditfleet(self,*arg,**kw):
        editfleet = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.id==kw['edit_id']). \
                one()
        editfleet.vehicle_description = kw['edit_vehicle_description']
        editfleet.registration_number=str(kw['edit_registration_number'])
        editfleet.vin_number = str(kw['edit_vin_number'])
        editfleet.engine_number = kw['edit_engine_number']
        editfleet.n_r_number = kw['edit_n_r_number']
        editfleet.year_model = kw['edit_year_model']
        editfleet.date_acquired = kw['edit_date_acquired']
        editfleet.tare = kw['edit_tare']
        editfleet.fuel_type = kw['edit_fuel_type']
        editfleet.tank_capacity = kw['edit_tank_capacity']
        editfleet.fuel_card_number =kw['edit_fuel_card_number']
        editfleet.fuel_card_expiry_date=kw['edit_fuel_card_expiry_date']
        editfleet.ext_colour = kw['edit_ext_colour']
        editfleet.service_center=kw['edit_service_center']
        editfleet.service_center_tel_no=kw['edit_service_center_tel_no']
        editfleet.driver=kw['edit_driver_id']
        editfleet.active = kw['edit_fleet_active']

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.fleet_service_history')
    def service_history(self,**named):
        tmpl_context.widget = spx_fleet_list 
        value = fleet_list_filler.get_value(values={},offset=0,order_by='id',desc=True)
        from tg.decorators import paginate
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='wip',
                    wip = items,
                    currentPage=currentPage,
                    count=count)

    @expose('jistdocstore.templates.transport.fleet_fuel_usage')
    def fuel_usage(self,**named):
        tmpl_context.widget = choose_fleet_form 
        return dict(page='wip',
                    action='/transportcont/redirect_fuel_usage')

    @expose()
    def redirect_fuel_usage(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        redirect("/transportcont/fuel_usage_one/"+kw['registration_number'])

    @expose('jistdocstore.templates.transport.fleet_fuel_usage_one')
    def fuel_usage_one(self,*arg,**named):
        """Handle the 'fuel usage ' page."""
        #tmpl_context.widget = spx_fleet_fuel_usage 
        #value = fleet_fuel_usage_filler.get_value(values={'id':arg[0],},offset=0,order_by='id',desc=True)
        #limit(100). \
        cont = DBS_JistFleetTransport.query(JistFleetFuelUsage). \
                            filter(JistFleetFuelUsage.fleetid==int(arg[0])). \
                            order_by(desc(JistFleetFuelUsage.id)). \
                            all()
        fleetdesc = DBS_JistFleetTransport.query(JistFleetList). \
                            filter(JistFleetList.id==int(arg[0])). \
                            one()
        flt = str(fleetdesc.registration_number) +' '+ str(fleetdesc.vehicle_description) +' '+  str(fleetdesc.driver)
        #for k in cont:
        #    print k.id, k.amount
        #return
        #print cont.id, cont.fleetid, cont.amount
        return dict(page='wip',
                    cont = cont,
                    fleetdescrip = flt,
                    fleetid = arg[0],
                    )

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.new_fuel_slip')
    def newfuelslip(self,*arg, **kw):
        """Handle the 'new contract' page."""
        tmpl_context.widget = add_new_fuelslip_form
        return dict(newfuelslip=kw,
                    fleetid=arg[0])

    @expose()
    def savenewfuelslip(self,*arg,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_fuelslip = JistFleetFuelUsage(fleetid = str(arg[0]),
                                       transaction_date=kw['transaction_date'],
                                       place = kw['place'],
                                       odometer = kw['odometer'],
                                       fuel_qty = kw['fuel_qty'],
                                       amount = kw['amount'],
                                       description = kw['description'],
                                       person = kw['person'],
                                       useridnew=useridcreated,
                                       dateadded = datetime.date(datetime.now())
                                       )
        DBS_JistFleetTransport.add(new_fuelslip)
        DBS_JistFleetTransport.flush()

        flash("New fuelslip entry successfully saved.")

        redirect("/transportcont/fuel_usage_one/"+arg[0])

    @expose('jistdocstore.templates.transport.edit_fuel_slip')
    def edit_fuelslip(self,*arg,**named):
        tmpl_context.widget = edit_fleet_fuel_form 
        val = fuel_edit_filler.get_value(values={'id':arg[0]})
        return dict(page='edit fuelslip',
                   value=val,
                   action = '/transportcont/saveeditfuelslip/'+arg[0],
                   editid = arg[0]
                   )

    @expose()
    #@validate(edit_supplier_form,edit_supplier)
    def saveeditfuelslip(self,*arg,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        editfuelslip = DBS_JistFleetTransport.query(JistFleetFuelUsage). \
                filter(JistFleetFuelUsage.id==int(arg[0])). \
                one()
        editfuelslip.fleetid = kw['fleetid']
        editfuelslip.transaction_date=str(kw['transaction_date'])
        editfuelslip.place = str(kw['place'])
        editfuelslip.odometer = kw['odometer']
        editfuelslip.fuel_qty = kw['fuel_qty']
        editfuelslip.amount = kw['amount']
        editfuelslip.description = kw['description']
        editfuelslip.person = kw['person']
        #flash("Group successfully edited.")
        redirect("/transportcont/fuel_usage_one/"+kw['fleetid'])

    @expose('jistdocstore.templates.transport.fleet_driver_list')
    def fleet_driver_list(self,**named):
        tmpl_context.widget = spx_fleet_drivers 
        value = fleet_drivers_filler.get_value(values={},offset=0,order_by='id',desc=True)
        from tg.decorators import paginate
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='wip',
                    wip = items,
                    currentPage=currentPage,
                    count=count)

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.new_fleet_driver')
    def newdriver(self,*arg, **kw):
        """Handle the 'new contract' page."""
        tmpl_context.widget = add_new_driver_form
        #fleetid=arg[0])
        return dict(newdriver=kw)

    @expose()
    def savenewdriver(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_driver = JistFleetDriverList(
                                       driver_name = kw['driver_name_id'],
                                       id_number = kw['id_number'],
                                       licence_code = kw['licence_code'],
                                       licence_exp_date = kw['licence_exp_date'],
                                       pdp_code = kw['pdp_code'],
                                       pdp_exp_date = kw['pdp_exp_date'],
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now())
                                       )
        DBS_JistFleetTransport.add(new_driver)
        DBS_JistFleetTransport.flush()

    @expose('jistdocstore.templates.transport.edit_fleet_driver')
    def edit_driver(self,*arg,**named):
        tmpl_context.widget = edit_fleet_driver_form 
        val = driver_edit_filler.get_value(values={'id':arg[0]})
        return dict(page='edit driver',
                   value=val,
                   action = '/transportcont/saveeditdriver/'+arg[0],
                   editid = arg[0]
                   )

    @expose()
    #@validate(edit_supplier_form,edit_supplier)
    def saveeditdriver(self,*arg,**kw):
        #del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridedited = usernow.user_id
        editdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                filter(JistFleetDriverList.id==kw['edit_driver_id']). \
                one()
        editdriver.active = kw['edit_driver_active']
        editdriver.driver_name = kw['edit_driver_name_id']
        editdriver.id_number=str(kw['edit_id_number'])
        editdriver.licence_code = kw['edit_licence_code']
        editdriver.licence_exp_date = kw['edit_licence_exp_date']
        editdriver.pdp_code = kw['edit_pdp_code']
        editdriver.pdp_exp_date = kw['edit_pdp_exp_date']
        editdriver.useridedited=useridedited
        editdriver.dateedited = datetime.date(datetime.now())

    @expose('jistdocstore.templates.transport.fleet_maintenance_usage')
    def fleet_maintenance_choose(self,**named):
        tmpl_context.widget = choose_fleet_form 
        return dict(page='wip',
                    action='/transportcont/redirect_maintenance')

    @expose()
    def redirect_maintenance(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        redirect("/transportcont/fleet_maintenance_list/"+kw['registration_number'])

    @expose('jistdocstore.templates.transport.fleet_maintenance_list')
    def fleet_maintenance_list(self,*arg,**named):
        #tmpl_context.widget = spx_fleet_maintenance 
        cont = DBS_JistFleetTransport.query(JistFleetMaintenanceList). \
                            filter(JistFleetMaintenanceList.fleetid==int(arg[0])). \
                            order_by(desc(JistFleetMaintenanceList.id)). \
                            all()
        fleetdesc = DBS_JistFleetTransport.query(JistFleetList). \
                            filter(JistFleetList.id==int(arg[0])). \
                            one()
        flt = str(fleetdesc.registration_number) +' '+ str(fleetdesc.vehicle_description) +' '+  str(fleetdesc.driver)
        #editfleet.vehicle_description = kw['vehicle_description']
        #editfleet.registration_number=str(kw['registration_number'])

                            
        return dict(page='fleet_maintenance_list',
                    cont = cont,
                    fleetid = arg[0],
                    fleetdescrip = flt
                    )

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.new_fleet_maintenance')
    def newmaintenance(self,*arg, **kw):
        """Handle the 'new contract' page."""
        tmpl_context.widget = add_new_maintenance_form
        #fleetid=arg[0])
        return dict(newmaintenance=kw,
                    fleetid=arg[0])

    @expose()
    def savenewmaintenance(self,*arg,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        fleetid = str(arg[0])
        new_maintenance = JistFleetMaintenanceList(
                                       reqid = kw['reqid'],
                                       fleetid = fleetid,
                                       transaction_date =kw['transaction_date'],
                                       supplier = kw['supplier'],
                                       odometer = kw['odometer'],
                                       work_description =kw['work_description'],
                                       next_service = kw['next_service'],
                                       amount = kw['amount'],
                                       person = kw['person'],
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now())
                                       )
        DBS_JistFleetTransport.add(new_maintenance)
        DBS_JistFleetTransport.flush()

        flash("New maintenance entry successfully saved.")

        redirect("/transportcont/fleet_maintenance_list/"+str(fleetid))

    @expose('jistdocstore.templates.transport.edit_fleet_maintenance')
    def edit_maintenance(self,*arg,**named):
        tmpl_context.widget = edit_fleet_maintenance_form 
        val = maintenance_edit_filler.get_value(values={'id':arg[0]})
        return dict(page='edit maintenance',
                   value=val,
                   action = '/transportcont/saveeditmaintenance/'+arg[0],
                   editid = arg[0]
                   )

    @expose()
    def saveeditmaintenance(self,*arg,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridedited = usernow.user_id
        editmaintenance = DBS_JistFleetTransport.query(JistFleetMaintenanceList). \
                filter(JistFleetMaintenanceList.id==int(arg[0])). \
                one()
        editmaintenance.fleetid = kw['fleetid']
        editmaintenance.reqid = kw['reqid']
        editmaintenance.transaction_date =kw['transaction_date']
        editmaintenance.supplier = kw['supplier']
        editmaintenance.odometer = kw['odometer']
        editmaintenance.work_description =kw['work_description']
        editmaintenance.next_service = kw['next_service']
        editmaintenance.amount = kw['amount']
        editmaintenance.person = kw['person']
        editmaintenance.useridedited=useridedited
        editmaintenance.dateedited = datetime.date(datetime.now())
        #flash("Group successfully edited.")
        redirect("/transportcont/fleet_maintenance_list/"+kw['fleetid'])

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.transport.search_fleet_fuel')
    def search_fleet_fuel(self,**named):
        """Handle the 'myoutofoffice' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=SearchFleetFuel(),
                    target="output",
                    action="do_search_fleet_fuel")
        tmpl_context.form = ajax_form 
        #tmpl_context.form = add_new_reception_message

        return dict(page='Fleet Fuel Usage',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_fleet_fuel(self, **kw):
        if not kw['startdate']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                if k == "startdate":
                    #print k,w
                    #rqdate = w.split('/')
                    #print rqdate, type(rqdate)
                    #year = rqdate[0]
                    #print year
                    year =w.split('-')[0]
                    #print year
                    month =w.split('-')[1]
                    day =w.split('-')[2]
        if not kw['enddate']:
            endyear = str(0)
        else :
            for k,w in kw.iteritems():
                if k == "enddate":
                    #print k,w
                    endyear =w.split('-')[0]
                    endmonth =w.split('-')[1]
                    endday =w.split('-')[2]

        #return
        if year==str(0):
            today = datetime.date(datetime.now())
            tup = today.timetuple()
        else:
            today = date(int(year),int(month),int(day))
            tup = today.timetuple()
        if endyear==str(0):
            endtoday = datetime.date(datetime.now())
            endtup = endtoday.timetuple()
        else:
            endtoday = date(int(endyear),int(endmonth),int(endday))
            endtup = endtoday.timetuple()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(today,sttimestart)
        enddate = datetime.combine(endtoday,sttimeend)
        fuelslips = DBS_JistFleetTransport.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                              order_by(desc(JistFleetFuelUsage.transaction_date)).  \
                                              all()
        #print fuelslips
        fuelslips_sum = DBS_JistFleetTransport.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                             value(func.sum(JistFleetFuelUsage.amount))
        locale.setlocale(locale.LC_ALL, '')
        #return
        if not fuelslips_sum:
            totalexcl = 0.00
        else:
            totalexcl = locale.format('%.2f',fuelslips_sum,grouping=True,monetary=True)
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        supplier_text = "<H3 align='left'>Fleet Fuel Usage from %s to %s</H3><p/>"%(datestart,dateend)
        if  fuelslips_sum:
            pdf1 = """<div class=sidebar_total_excl>
                        Total: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/transportcont/export_fleet_fuel_pdf/%s/%s'><p/> 
                        Export to PDF</a>
                        """%(startdate,enddate)
            pdf3 = """
                    </div><p/>
                   """
            pdfstuff = pdf1+pdf2+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total: R %s
                   """%(totalexcl)
            pdf3 = """
                    </div><p/>
                   """
            pdfstuff = pdf1+pdf3

        table = "<table class='tablecontractdata'>"
        headerdata = """
                    <th>Date </th>
                    <th>Reg </th>
                    <th>Vehicle</th>
                    <th>Driver</th>
                    <th>Place</th>
                    <th>Odometer</th>
                    <th>Fuel Qty</th>
                    <th>Amount</th>
                    """

        sitedata = supplier_text +pdfstuff + table + headerdata 
        for k in fuelslips:
            tr = "<tr class='tablestandard'>"
            #sitedatatemp = "<img src='/images/staffpics/%s.png'/></td>"%str(k.for_user)
            fleettemp = DBS_JistFleetTransport.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            transdate =""" 
                            <td>%s</td>
                            """%(k.transaction_date)
            fromperson =""" 
                            <td>%s</td>
                            """%(fleettemp.registration_number)
            callback =""" 
                            <td>%s</td>
                            """%(fleettemp.vehicle_description)
            callagain =""" 
                            <td>%s</td>
                            """%(fleettemp.driver)
            nomsgs =""" 
                            <td>%s</td>
                            """%(k.place)
            messg =""" 
                            <td align=right>%s</td>
                            """%(k.odometer)
            returntel ="<td align=right>%s</td>"%str(k.fuel_qty)
            amount ="<td align=right>%s</td>"%str(k.amount)
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+"</p>"+tr+transdate+ \
                    fromperson+callback+callagain+nomsgs+ \
                    messg+returntel+amount+trclose
        sitedata = sitedata+"</table>"
        return sitedata 

    @expose()
    def export_fleet_fuel_pdf(self,startdate,enddate):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #print datestart, dateend
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        fuelslips = DBS_JistFleetTransport.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                              order_by(desc(JistFleetFuelUsage.transaction_date)).  \
                                              all()
        fuelslips_sum = DBS_JistFleetTransport.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                             value(func.sum(JistFleetFuelUsage.amount))
        locale.setlocale(locale.LC_ALL, '')
        #return
        if not fuelslips_sum:
            totalexcl = 0.00
        else:
            totalexcl = locale.format('%.2f',fuelslips_sum,grouping=True,monetary=True)
        for k in fuelslips:
            fleettemp = DBS_JistFleetTransport.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            wip1.append({'date':k.transaction_date,
                         'reg':fleettemp.registration_number,
                         'description':fleettemp.vehicle_description,
                         'driver':fleettemp.driver,
                         'place':k.place,
                         'odometer':k.odometer,
                         'fuelqty':k.fuel_qty,
                         'amount':k.amount
                         })
        count = len(wip1) 
        #for k in wip1:
        #    print k
        #pointperson_name = User.by_user_id(point).user_name
        userdata.append([datetime.date(datetime.now()),
                        "Fleet Fuel Usage from %s to %s"%(startdate,enddate),
                        ""
                        ])
        headers =["Date","Req","Description","Driver","Place","Odometer","Fuel Qty","Amount"]
        headerwidths=[80,80,150,100,100,60,80,100]
        pdffile.CreatePDFFleetFuelUsage(userdata,wip1,headers,headerwidths,totalexcl)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent
        #redirect('/mngntcont/managepoints/'+str(point))
        #print "Got Here again"

    @expose()
    def do_search_fleet_all(self, **kw):
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
              order_by(desc(JistFleetList.id)).  \
                            all()
        supplier_text = """<H2 align='center'>All Fleet Ever Owned By JIST
            <button class="ui-state-default ui-corner-all" id="add_btn_fleet" style="display:block">Add Fleet Item</button>
                            </H2>
                        <p/>"""
        table = "<table class='tabletabs' id='tblfleetlist'>"
        headerdata = """
                    <th>ID</th>
                    <th>Description</th>
                    <th>Registration No</th>
                    <th>Year Model</th>
                    <th>Date Acquired</th>
                    <th>Vin Number</th>
                    <th>Active</th>
                    <th>Driver</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in fleetlist:
            drv = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id == k.driver).one()
            tr = "<tr class='tabletabs'>"
            fleetbody = """

                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>

                        """%(k.id,
                             k.vehicle_description,
                             k.registration_number,
                             k.year_model,
                             k.date_acquired,
                             k.vin_number,
                             k.active,
                             drv.driver_name
                             )
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+tr+fleetbody+trclose
                       
        sitedata = sitedata+"</table>"
        return sitedata

    @expose()
    def do_search_fleet_active(self, **kw):
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
              filter(JistFleetList.active==1). \
              order_by(desc(JistFleetList.id)).  \
                            all()

        supplier_text = "<H2 align='center'>Active Fleet</H2><p/>"
        table = "<table class='tabletabs' id='tblactivefleetlist'>"
        headerdata = """
                    <th>ID</th>
                    <th>Description</th>
                    <th>Registration No</th>
                    <th>Year Model</th>
                    <th>Date Acquired</th>
                    <th>Vin Number</th>
                    <th>Active</th>
                    <th>Driver</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in fleetlist:
            drv = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id == k.driver).one()
            tr = "<tr class='tabletabs'>"
            fleetbody = """

                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>

                        """%(k.id,
                             k.vehicle_description,
                             k.registration_number,
                             k.year_model,
                             k.date_acquired,
                             k.vin_number,
                             k.active,
                             drv.driver_name
                             )
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+tr+fleetbody+trclose
                       
        sitedata = sitedata+"</table>"
        return sitedata

    @expose()
    def get_edit_fleet_form(self,fleetid, **kw):
        fleetone = DBS_JistFleetTransport.query(JistFleetList). \
              filter(JistFleetList.id==fleetid). \
                            one()
        allactivedrivers = DBS_JistFleetTransport.query(JistFleetDriverList). \
                filter(JistFleetDriverList.active==1). \
                all()
        editfleet_form1 = """
        <form id="edit_fleet_form">
            <fieldset>
        <H3> Edit Fleet Item </H3>
                <label for="">Vehicle ID</label>
            <input type="text" value="%s" name="edit_id" id="edit_id" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Vehicle Description</label>
            <input type="text" value="%s" name="edit_vehicle_description" id="edit_vehicle_description" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Registration Number</label>
            <input type="text" value="%s" name="edit_registration_number" id="edit_registration_number" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Year Model</label>
            <input type="text" value="%s" name="edit_year_model" id="edit_year_model" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Date Acquired</label>
            <input type="text" value="%s" name="edit_date_acquired" id="edit_date_acquired" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Vin Number</label>
            <input type="text" value="%s" name="edit_vin_number" id="edit_vin_number" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Engine Number</label>
            <input type="text" value="%s" name="edit_engine_number" id="edit_engine_number" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">NR Number</label>
            <input type="text" value="%s" name="edit_n_r_number" id="edit_n_r_number" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Tare</label>
            <input type="text" value="%s" name="edit_tare" id="edit_tare" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Fuel Type</label>
            <input type="text" value="%s" name="edit_fuel_type" id="edit_fuel_type" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Tank Capacity</label>
            <input type="text" value="%s" name="edit_tank_capacity" id="edit_tank_capacity" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Fuel Card Number</label>
            <input type="text" value="%s" name="edit_fuel_card_number" id="edit_fuel_card_number" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Fuel Card Expiry Date</label>
            <input type="text" value="%s" name="edit_fuel_card_expiry_date" id="edit_fuel_card_expiry_date" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Exterior Colour</label>
            <input type="text" value="%s" name="edit_ext_colour" id="edit_ext_colour" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Service Center</label>
            <input type="text" value="%s" name="edit_service_center" id="edit_service_center" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Service Center Number</label>
            <input type="text" value="%s" name="edit_service_center_tel_no" id="edit_service_center_tel_no" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Driver</label>
                <select id="edit_driver_id"  class="text ui-widget-content ui-corner-all">
             """%(fleetone.id,
                  fleetone.vehicle_description,
                  fleetone.registration_number,
                  fleetone.year_model,
                  fleetone.date_acquired,
                  fleetone.vin_number,
                  fleetone.engine_number,
                  fleetone.n_r_number,
                  fleetone.tare,
                  fleetone.fuel_type,
                  fleetone.tank_capacity,
                  fleetone.fuel_card_number,
                  fleetone.fuel_card_expiry_date,
                  fleetone.ext_colour,
                  fleetone.service_center,
                  fleetone.service_center_tel_no,
                  )
        editfleet_temp = ""
        editfleet_form2 = ""
        for driver in allactivedrivers: 
            if fleetone.driver == str(driver.id):
                editfleet_temp = """
                              <option value="%s" selected="selected">%s</option>
                          """%(driver.id, driver.driver_name)
                editfleet_form2 = editfleet_form2 + editfleet_temp

            else:
                editfleet_temp = """
                              <option value="%s">%s</option>
                          """%(driver.id, driver.driver_name)
                editfleet_form2 = editfleet_form2 + editfleet_temp
        editfleet_form3 = """
                </select><br/>
                <label for="">Active</label>
                <select id="edit_fleet_active"  class="text ui-widget-content ui-corner-all">
                          """
        if fleetone.active:
            editfleet_form4 = """
                    <option id="edit_fleet_active" value="1" selected="selected">True</option>
                    <option id="edit_fleet_active" value="0">False</option>
                            """
        else:
            editfleet_form4 = """
                    <option id="edit_fleet_active" value="1">True</option>
                    <option id="edit_fleet_active" value="0" selected="selected">False</option>
                            """

        editfleet_form5 = """
                </select>
                </p>
            <button class="ui-state-default ui-corner-all" id="edit_btn_fleet" style="display:block">Edit Fleet Item</button>
            </fieldset>
        </form>
            """
        return editfleet_form1 + editfleet_form2 + editfleet_form3 + editfleet_form4 + editfleet_form5

    @expose()
    def do_search_drivers_all(self, **kw):
        driverlist = DBS_JistFleetTransport.query(JistFleetDriverList). \
              order_by(desc(JistFleetDriverList.id)).  \
                            all()
        supplier_text = """<H2 align='center'>All Drivers Ever:
            <button class="ui-state-default ui-corner-all" id="add_btn_driver" style="display:block">Add New Driver</button>
                            </H2>
                        <p/>"""
        table = "<table class='tabletabs' id='tbldriverlist'>"
        headerdata = """
                    <th>ID</th>
                    <th>Driver Name</th>
                    <th>Driver ID</th>
                    <th>Licence Code</th>
                    <th>Licence Expiry Date</th>
                    <th>PDP Code</th>
                    <th>PDP Exp Date</th>
                    <th>Active</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in driverlist:
            tr = "<tr class='tabletabs'>"
            fleetbody = """

                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>
                            <td>%s</td>

                        """%(k.id,
                             k.driver_name,
                             k.id_number,
                             k.licence_code,
                             k.licence_exp_date,
                             k.pdp_code,
                             k.pdp_exp_date,
                             k.active,
                             )
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+tr+fleetbody+trclose
                       
        sitedata = sitedata+"</table>"
        return sitedata

    @expose()
    def get_edit_driver_form(self,driverid, **kw):
        driverone = DBS_JistFleetTransport.query(JistFleetDriverList). \
              filter(JistFleetDriverList.id==driverid). \
                            one()
        editdriver_form1 = """
        <form id="edit_driver_form">
            <fieldset>
        <H3> Edit Driver </H3>
            <label for="">Driver ID</label>
            <input type="text" value="%s" name="driver_id_edit" id="driver_id_edit" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Driver Name</label>
            <input type="text" value="%s" name="edit_driver_name_id" id="edit_driver_name_id" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">ID Number</label>
            <input type="text" value="%s"  name="edit_id_number" id="edit_id_number" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Licence Code</label>
            <input type="text" value="%s"  name="edit_licence_code" id="edit_licence_code" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">Licence Expiry Date</label>
            <input type="text" value="%s"  name="edit_licence_exp_date" id="edit_licence_exp_date" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">PDP Code</label>
            <input type="text" value="%s"  name="edit_pdp_code" id="edit_pdp_code" class="text ui-widget-content ui-corner-all"/><br/>
            <label for="">PDP Expiry Date</label>
            <input type="text" value="%s"  name="edit_pdp_exp_date" id="edit_pdp_exp_date" class="text ui-widget-content ui-corner-all"/><br/>

             """%(driverone.id,
                  driverone.driver_name,
                  driverone.id_number,
                  driverone.licence_code,
                  driverone.licence_exp_date,
                  driverone.pdp_code,
                  driverone.pdp_exp_date,
                  )
        editdriver_form2 = ""
        editdriver_form3 = """
                </select><br/>
                <label for="">Active</label>
                <select id="edit_driver_active"  class="text ui-widget-content ui-corner-all">
                          """
        if driverone.active:
            editdriver_form4 = """
                    <option id="edit_driver_active" value="1" selected="selected">True</option>
                    <option id="edit_driver_active" value="0">False</option>
                            """
        else:
            editdriver_form4 = """
                    <option id="edit_driver_active" value="1">True</option>
                    <option id="edit_driver_active" value="0" selected="selected">False</option>
                            """

        editdriver_form5 = """
                </select>
                </p>
            <button class="ui-state-default ui-corner-all" id="edit_btn_driver" style="display:block">Edit Driver</button>
            </fieldset>
        </form>
            """
        return editdriver_form1 + editdriver_form2 + editdriver_form3 + editdriver_form4 + editdriver_form5
