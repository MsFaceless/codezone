# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission
from tg.decorators import paginate
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

#from tw.jquery import AjaxForm
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
from jistdocstore.lib.jist3yrbuildingreportlab import * 
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
import random
from tg import session
#from tw.jquery import TreeView
import xlwt
from xlwt import Workbook, Style
from xlrd import open_workbook
from xlutils.copy import copy

from babel.numbers import format_currency, format_number, format_decimal
from decimal import Decimal
from jistdocstore.lib.jistfileuploader import qqFileUploader
import json
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
estimating_dirname = os.path.join(public_dirname, 'estimating_docs')
pdf_dirname = os.path.join(public_dirname, 'pdf')
est_excel_dirname = os.path.join(estimating_dirname, 'excel')
est_excel_template_dir = os.path.join(estimating_dirname, 'templates')
UPLOAD_DIRECTORY = os.path.join(estimating_dirname ,"pictures/")
__all__ = ['Estimating_3yr_Ess_HSF_Controller']


class Estimating_3yr_Ess_HSF_Controller(BaseController):
    """Sample controller-wide authorization"""
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))
    def __init__(self):
        self.tender_number = "445Q"

    @expose()
    def index(self):
        redirect('est3yresshsfcont/ess_3yr_hsf_fencing_console')

    #*********************************************************************
    #********* Tender 2013-2018**********************
    ########### 3yr ESS HSF Tender ##########
    #*********************************************************************

    @expose('jistdocstore.templates.estimating.ess_3yr_hsf_fencing_console')
    def ess_3yr_hsf_console(self,**named):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        sites = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFSites). \
               order_by(asc(JistEstimating3yrEssHSFSites.id)).all()
        boq = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFItems). \
               order_by(asc(JistEstimating3yrEssHSFItems.id)).all()
        return dict(page='Ess 3yr HSF Estimate Console',
                    contracts = contracts,
                    users = activeusers,
                    boq = boq,
                    myjistid = myid,
                    sites = sites
                    )
    @expose()
    def get_estimate_sites(self,**kw):
        html = ''
        html1 = """<table id='estimate_sites_table' class='table_estdata'>
                   <th> ID</th>
                   <th> Date</th>
                   <th> Site Name</th>
                   <th> Description</th>
                   <th> Province</th>
                   <th> Area</th>
                   <th> Coordinates</th>
                   <th> WONumber</th>
                   <th> Supervisor</th>
                   <th> Edit</th>
                   <th> Open</th>
                """
        html3 = """
                            </table>
                """
        if kw['switch']=="All":
            sites = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFSites). \
                   order_by(desc(JistEstimating3yrEssHSFSites.id)).all()
            #sites = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                   #order_by(desc(JistEstimating3yrBuildingSites.id)).all()
            temphtml1 = ""
            html2 = ""
            for scp in sites:
                temphtml1 = """
                            <tr> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td>  
                            <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                            </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                            </td></tr>
                            """%(scp.id,scp.date,scp.name,scp.description,scp.province,scp.area,scp.coordinates,scp.wonumber,scp.supervisor)
                html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        elif kw['switch']=="SearchName":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFSites). \
                    filter(JistEstimating3yrEssHSFSites.name.like(searchphrase)). \
                   order_by(desc(JistEstimating3yrEssHSFSites.id)).all()
            
            temphtml1 = ""
            html2 = ""
            for scp in sites:
                temphtml1 = """
                            <tr> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td>  
                            <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                            </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                            </td></tr>
                            """%(scp.id,scp.date,scp.name,scp.description,scp.province,scp.area,scp.coordinates,scp.wonumber,scp.supervisor)
                html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        elif kw['switch']=="SearchDescription":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFSites). \
                    filter(JistEstimating3yrEssHSFSites.description.like(searchphrase)). \
                   order_by(desc(JistEstimating3yrEssHSFSites.id)).all()
            
            temphtml1 = ""
            html2 = ""
            for scp in sites:
                temphtml1 = """
                            <tr> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td>  
                            <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                            </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                            </td></tr>
                            """%(scp.id,scp.date,scp.name,scp.description,scp.province,scp.area,scp.coordinates,scp.wonumber,scp.supervisor)
                html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        else:
            return html

    @expose()
    def save_new_estimate_sites(self,**kw):
        #for k,w in enumerate(kw):
            #print k,w,kw[w]
        if kw['sitename'] == '':
            return
        name = kw['sitename']
        coordinates = kw['coordinates']
        province = kw['province']
        area = kw['area']
        description = kw['description']
        wonumber = kw['wonumber']
        supervisor = kw['supervisor']
        visit_by = kw['visit_by']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_site = JistEstimating3yrEssHSFSites(name = name,
                                       description=description,
                                       wonumber = wonumber,
                                       supervisor = supervisor,
                                       date = datetime.date(datetime.now()),
                                       area = area,
                                       coordinates = coordinates,
                                       visit_by = visit_by,
                                       province = province,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssHSF.add(new_site)
        DBS_Jist3yrEssHSF.flush()
        return

    @expose()
    def get_edit_estimate_sites(self,**kw):
        site = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFSites). \
                filter(JistEstimating3yrEssHSFSites.id == kw['siteid']). \
                one()
        html = """
                        <form id ='frm_edit_est_new_site'>
                        <fieldset>
                            <label for="edit_siteid">Name</label> 
                            <input type="text" value = "%s" name="edit_siteid" id="edit_siteid" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_sitename">Name</label>
                            <input type="text" value = "%s" name="edit_sitename" id="edit_sitename" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_description">Description</label>
                            <input type="text" value = "%s" name="edit_description" id="edit_description" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_wonumber">WONumber</label>
                            <input type="text" value = "%s" name="edit_wonumber" id="edit_wonumber" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_supervisor">Supervisor</label>
                            <input type="text" value = "%s" name="edit_supervisor" id="edit_supervisor" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_coordinates">Coordinates</label>
                            <input type="text" value = "%s" name="edit_coordinates" id="edit_coordinates" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_area">Area</label>
                            <input type="text" value = "%s" name="edit_area" id="edit_area" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_province">Province</label>
                            <input type="text" value = "%s" name="edit_province" id="edit_province" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_visit_by">Visit By</label>
                            <input type="text" value = "%s" name="edit_visit_by" id="edit_visit_by" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_edit_new_site_hsf">Edit Site</button> 
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_cancel_edit_site_hsf">Cancel</button>
                        </fieldset>
                        </form>
               """%(site.id,site.name,site.description,site.wonumber,site.supervisor,site.coordinates,site.area,site.province,site.visit_by)
        return html
        
    @expose()
    def save_edit_estimate_sites(self,**kw):
        site = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFSites). \
                filter(JistEstimating3yrEssHSFSites.id == kw['edit_siteid']). \
                one()
        name = kw['edit_sitename']
        coordinates = kw['edit_coordinates']
        province = kw['edit_province']
        area = kw['edit_area']
        description = kw['edit_description']
        wonumber = kw['edit_wonumber']
        supervisor = kw['edit_supervisor']
        visit_by = kw['edit_visit_by']
        site.name = name
        site.coordinates = coordinates
        site.province = province
        site.area = area
        site.description = description
        site.wonumber = wonumber
        site.supervisor = supervisor
        site.visit_by = visit_by
       
    @expose()
    def get_estimate_quote_list(self,**kw):
        quotelist = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuotes). \
                filter(JistEstimating3yrEssHSFQuotes.idsite == kw['siteid']). \
                order_by(desc(JistEstimating3yrEssHSFQuotes.id)).all()
        html = """
               <table id="quote_list">
               <th>Quote No </th>
               <th>Quote Date</th>
               """
        html2 = '' 
        for quote in quotelist:
            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   </tr>

                   """%(quote.id,quote.estdate)
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def get_estimate_quote_items(self,**kw):
        quoteitems = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.idquote == kw['quoteid']). \
                order_by(asc(JistEstimating3yrEssHSFQuoteBQItems.id)).all()
        quoteitemsvalue = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.idquote == kw['quoteid']). \
                value(func.sum(JistEstimating3yrEssHSFQuoteBQItems.total))

        html = """
               <h3 class="ui-widget-shadow">Quote Number: %s 
               <span style="float:right">%s</span>
                    <a href="/est3yresshsfcont/ajaxexport_excelquote/%s">
                    <img id="export_excel_est" src="/images/x-office-document.png" align="right"></img>
                    </a>
               </h3>
               <table id="quote_items">
               <th>ID </th>
               <th>Description</th>
               <th>Unit</th>
               <th>Quantity</th>
               <th>Price</th>
               <th>Total</th>
               <th>Edit</th>
               <th>Delete</th>
               """%(kw['quoteid'],quoteitemsvalue,kw['quoteid'])
        html2 = '' 
        for quote in quoteitems:
            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td align="right">%s</td>
                   <td align="right">%s</td>
                   <td align="right">%s</td>
                    <td width="25px" ><img  id="edit_quoteitem" src="/images/Edit-16.png"></img></td>
                    <td width='25px'> <img  id="delete_quoteitem" src="/images/delete.png"> </img></td>
                   </tr>

                   """%(quote.id,quote.description,quote.units,quote.quantity,quote.price,quote.total)
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def get_estimate_quote_items_edit(self,**kw):
        quoteitem = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.id == kw['itemid']). \
                one()
        html = """
                        <form id ='frm_edit_est_quote_item'>
                        <fieldset>
                            <label for="edit_quoteid">ID</label> <input type="text" value = "%s" name="edit_quoteid" id="edit_quoteid" class="text ui-widget-content ui-corner-all" disabled="true" />
                            <br/>
                            <label for="edit_description">Description</label>
                            <input type="text" value = "%s" name="edit_description" id="edit_description" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_unit">Unit</label>
                            <input type="text" value = "%s" name="edit_unit" id="edit_unit" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_quantity">Quantity</label>
                            <input type="text" value = "%s" name="edit_quantity" id="edit_quantity" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_price">Price</label>
                            <input type="text" value = "%s" name="edit_price" id="edit_price" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <label for="edit_total">Total</label>
                            <input type="text" value = "%s" name="edit_total" id="edit_total" value="" class="text ui-widget-content ui-corner-all" />
                            <br/>
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_edit_quote_item">Edit Item</button> 
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_cancel_edit_item">Cancel</button>
                        </fieldset>
                        </form>
               """%(quoteitem.id,quoteitem.description,quoteitem.units,quoteitem.quantity,quoteitem.price,quoteitem.total)
        return html

    @expose()
    def save_edit_estimate_item(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        quoteitem = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.id == kw['itemid']). \
                one()
        description = kw['edit_description']
        unit = kw['edit_unit']
        quantity = kw['edit_quantity']
        price = kw['edit_price']
        total = kw['edit_total']
        quoteitem.description = description
        quoteitem.unit = unit
        quoteitem.quantity = quantity 
        quoteitem.price = price 
        quoteitem.total = total 

    @expose()
    def ajaxaddnewquotefull(self,jcno, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_quote = JistEstimating3yrEssHSFQuotes(
                                       idsite = jcno,
                                       estdate = datetime.date(datetime.now()),
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssHSF.add(new_quote)
        DBS_Jist3yrEssHSF.flush()
        scp_items = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFItems). \
                    all()
        #print new_quote
        for item in scp_items:
            new_quote_bqitem = JistEstimating3yrEssHSFQuoteBQItems(
                                           idquote = new_quote.id,
                                           idbqitem = item.id,
                                           description = item.description,
                                           units = item.units,
                                           #quantity = item.quantity,
                                           price = item.price,
                                           #total = item.total,
                                           useridnew=useridcreated,
                                           useridedited=useridcreated,
                                           dateadded = datetime.date(datetime.now()),
                                           dateedited = datetime.date(datetime.now()),
                                           timeedited =datetime.time(datetime.now()),
                                           )
            DBS_Jist3yrEssHSF.add(new_quote_bqitem)
        DBS_Jist3yrEssHSF.flush()
            #print new_quote_bqitem
    
    @expose()
    def ajaxdeletequoteitem(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        quoteitem = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.id == kw['itemid']). \
                one()
        DBS_Jist3yrEssHSF.delete(quoteitem)
        return

    @expose()
    def ajaxaddnewquote_oneitem(self,quoteid,bqitemid, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        item = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFItems). \
                filter(JistEstimating3yrEssHSFItems.id == int(bqitemid)). \
                    one()
        new_quote_bqitem = JistEstimating3yrEssHSFQuoteBQItems(
                                       idquote = quoteid,
                                       idbqitem = item.id,
                                       description = item.description,
                                       units = item.units,
                                       #quantity = item.quantity,
                                       price = item.price,
                                       #total = item.total,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssHSF.add(new_quote_bqitem)
        DBS_Jist3yrEssHSF.flush()

    @expose()
    def ajaxaddnewquoteempty(self,jcno, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_quote = JistEstimating3yrEssHSFQuotes(
                                       idsite = jcno,
                                       estdate = datetime.date(datetime.now()),
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssHSF.add(new_quote)
        DBS_Jist3yrEssHSF.flush()

    @expose()
    def ajaxexport_excelquote(self,quoteid, **kw):
        quoteitems = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.idquote == quoteid). \
                order_by(asc(JistEstimating3yrEssHSFQuoteBQItems.id)).all()
        quoteitemsvalue = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFQuoteBQItems). \
                filter(JistEstimating3yrEssHSFQuoteBQItems.idquote == quoteid). \
                value(func.sum(JistEstimating3yrEssHSFQuoteBQItems.total))
        #for k, w in kw.iteritems():
        #    print k, w
        #print datestart, dateend
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.xls'
        filename = os.path.join(est_excel_dirname, str(fname))
        #print filename
        templatename = "HSFTemplate.xls"
        templatewb = open_workbook(os.path.join(est_excel_template_dir,templatename), formatting_info=True, on_demand=True) 
        #wb = Workbook()
        wb = copy(templatewb)
        #ws = wb.add_sheet('Type examples')
        ws = wb.get_sheet(0)
        rowno = 17
        style = xlwt.XFStyle()
        #style.num_format_str = '"R"#,##0.00_);("R"#,##'
        style.num_format_str = '#,##0.00_);(#,##'

        for quoteitem in quoteitems:
            #ws.row(rowno).write(0,quoteitem.id)
            ws.row(rowno).write(1,quoteitem.description)
            ws.row(rowno).write(3,quoteitem.units)
            ws.row(rowno).write(4,quoteitem.quantity)
            ws.row(rowno).write(5,quoteitem.price,style=style)
            ws.row(rowno).write(6,quoteitem.total,style=style)
            rowno += 1
        """
        ws.row(0).write(0,u'\xa3')
        ws.row(0).write(1,'Text')
        ws.row(1).write(0,3.1415)
        ws.row(1).write(1,15)
        ws.row(1).write(2,265L)
        ws.row(1).write(3,Decimal('3.65'))
        ws.row(2).set_cell_number(0,3.1415)
        ws.row(2).set_cell_number(1,15)
        ws.row(2).set_cell_number(2,265L)
        ws.row(2).set_cell_number(3,Decimal('3.65'))
        ws.row(3).write(0,date(2009,3,18))
        ws.row(3).write(1,datetime(2009,3,18,17,0,1))
        ws.row(3).write(2,time(17,1))
        ws.row(4).set_cell_date(0,date(2009,3,18))
        ws.row(4).set_cell_date(1,datetime(2009,3,18,17,0,1))
        ws.row(4).set_cell_date(2,time(17,1))
        ws.row(5).write(0,False)
        ws.row(5).write(1,True)
        ws.row(6).set_cell_boolean(0,False)
        ws.row(6).set_cell_boolean(1,True)
        ws.row(7).set_cell_error(0,0x17)
        ws.row(7).set_cell_error(1,'#NULL!')
        ws.row(8).write( 0,'',Style.easyxf('pattern: pattern solid, fore_colour green;'))
        ws.row(8).write( 1,None,Style.easyxf('pattern: pattern solid, fore_colour blue;'))
        ws.row(9).set_cell_blank( 0,Style.easyxf('pattern: pattern solid, fore_colour yellow;'))
        ws.row(10).set_cell_mulblanks( 5,10,Style.easyxf('pattern: pattern solid, fore_colour red;'))
        """
        wb.save(filename)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def estuploadfile(self,*arg,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #print os.geteuid()
        #print os.getlogin()
        pictakenby =  kw['pictakenby']
        picjcno =  kw['picjcno']
        picdate =  kw['picdate']
        picdescription = kw['picdescription']
        picsubject = kw['picsubject']
        if not picdate:
            picdate = datetime.date(datetime.now()) 
        if picjcno == 'None':
            picjcno = 0
        #print picjcno
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        uploader = qqFileUploader(int(pictakenby),kw,UPLOAD_DIRECTORY, [".jpg",".jpeg",".JPG",".JPEG", ".png", ".ico", ".*"], 2147483648)
        #print uploader.getName()
        big_file_path, thumb_path = uploader.handleUpload()
        #print big_file_path, thumb_path
        big_file_base = os.path.basename(big_file_path) 
        thumb_file_base = os.path.basename(thumb_path) 
        usersharetable = []
        new_file = JistEstimating3yrEssHSFPhotos(filename=big_file_base,
                                       filesubject = picsubject,
                                       jcno = picjcno,
                                       takenby=pictakenby,
                                       description=picdescription,
                                       datetaken=picdate,
                                       thumbname = thumb_file_base,
                                       useridnew=usernow.user_id,
                                       )
        #for col in new_file.__table__._columns:
        #    print col
        #return
        DBS_Jist3yrEssHSF.add(new_file)
        DBS_Jist3yrEssHSF.flush()
        return json.dumps({"success": True})

    @expose()
    def get_photos_by_site(self,siteid,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        htmlheader = """
                    <div class="">
                    <h5 class="ui-widget-header">Picture Uploads For SiteNo %s .</h5>
                    """%(siteid)
        htmlout = ''
        thisuploads = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFPhotos). \
                filter(JistEstimating3yrEssHSFPhotos.jcno==int(siteid)). \
                all()
        for thisupload in thisuploads[::-1]:
            userpath = os.path.join('/estimating_docs/pictures', str(thisupload.takenby))
            thumbpath = os.path.join(userpath, 'thumbs')
            bigpicpath = os.path.join(userpath, 'pics')
            srcthumb = os.path.join(thumbpath, thisupload.thumbname)
            srcpic = os.path.join(bigpicpath, thisupload.filename)
            
            htmltemp = """
                                    <img  class="thumb_clicked" value="%s" src="%s" alt="" width="80px" height="80px" />
                        """%(thisupload.filename,srcthumb)
            htmlout = htmlout + htmltemp
        htmlclose = """
                    </div>
                    """
        return htmlheader + htmlout + htmlclose

    @expose('jistdocstore.templates.estimating.jist_estimating_pic_viewer')
    def estimating_pic_viewer(self,**kw):
        fname = kw['fname']
        thisupload = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFPhotos). \
                filter(JistEstimating3yrEssHSFPhotos.filename==fname). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #print myuploadlist_bydate
        userpath = os.path.join('/estimating_docs/pictures', str(thisupload.takenby))
        #thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        #srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        userowner = User.by_user_id(thisupload.takenby)
        return dict(page='JIST Estimating: ESS HSF Picture Viewer',
                   appname = 'HSF3yrEss',
                   srcpic=srcpic,
                   srcid=thisupload.pic_id,
                   thisupload=thisupload,
                   owner=userowner.user_name,
                   )

def isnumeric(value):
    return str(value).replace(".", "").replace("-", "").isdigit()





