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
from PIL import Image
from PIL.ExifTags import TAGS
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
estimating_dirname = os.path.join(public_dirname, 'estimating_docs')
pdf_dirname = os.path.join(public_dirname, 'pdf')
est_excel_dirname = os.path.join(estimating_dirname, 'excel')
est_excel_template_dir = os.path.join(estimating_dirname, 'templates')
UPLOAD_DIRECTORY = os.path.join(estimating_dirname ,"pictures/")

__all__ = ['Estimating_3yr_Ess_Palisade_Controller']


class Estimating_3yr_Ess_Palisade_Controller(BaseController):
    """Sample controller-wide authorization"""
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))
    def __init__(self):
        self.tender_number = "445Q"

    @expose()
    def index(self):
        redirect('est3yresspalisadecont/ess_3yr_palisade_console')

    #*********************************************************************
    #********* Tender 2013-2015**********************
    ########### 3yr ESS Palisade Tender ##########
    #*********************************************************************

    @expose('jistdocstore.templates.spf.spfindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='ESS 3yr Palisade Contract: Main Menu') 

    @expose('jistdocstore.templates.spf.ess_3yr_palisade_fencing_console')
    def ess_3yr_palisade_console(self,**named):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
               order_by(asc(JistEstimating3yrEssPalisadeSites.id)).all()
        boq = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeItems). \
               order_by(asc(JistEstimating3yrEssPalisadeItems.id)).all()
        return dict(page='Ess 3yr Palisade Estimate Console',
                    contracts = contracts,
                    users = activeusers,
                    boq = boq,
                    myjistid = myid,
                    sites = sites
                    )

    @expose('jistdocstore.templates.spf.ess_3yr_palisade_fencing_production_console')
    def ess_3yr_palisade_production_console(self,**named):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
               order_by(asc(JistEstimating3yrEssPalisadeSites.id)).all()
        boq = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
               order_by(asc(JistEstimating3yrEssPalisadeStandardMaterialList.id)).all()
        return dict(page='Ess 3yr Palisade Production Console',
                    contracts = contracts,
                    users = activeusers,
                    boq = boq,
                    myjistid = myid,
                    sites = sites
                    )

    @expose('jistdocstore.templates.spf.ess_3yr_palisade_fencing_jjmc_console')
    def ess_3yr_palisade_jjmc_console(self,**named):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
               order_by(asc(JistEstimating3yrEssPalisadeSites.id)).all()
        boq = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
               order_by(asc(JistEstimating3yrEssPalisadeStandardMaterialList.id)).all()
        return dict(page='Ess 3yr Palisade JJMC Console',
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
            sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                   order_by(desc(JistEstimating3yrEssPalisadeSites.id)).all()
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
            sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                    filter(JistEstimating3yrEssPalisadeSites.name.like(searchphrase)). \
                   order_by(desc(JistEstimating3yrEssPalisadeSites.id)).all()
            
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
        elif kw['switch']=="SearchArea":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                    filter(JistEstimating3yrEssPalisadeSites.area.like(searchphrase)). \
                   order_by(desc(JistEstimating3yrEssPalisadeSites.id)).all()
            
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
        new_site = JistEstimating3yrEssPalisadeSites(name = name,
                                       description=description,
                                       wonumber = wonumber,
                                       supervisor = supervisor,
                                       date = datetime.date(datetime.now()),
                                       area = area,
                                       coordinates = coordinates,
                                       visit_by = visit_by,
                                       province = province,
                                       active = 1,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssPalisade.add(new_site)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def get_edit_estimate_sites(self,**kw):
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
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
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_edit_new_site_palisade">Edit Site</button> 
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_cancel_edit_site_palisade">Cancel</button>
                        </fieldset>
                        </form>
               """%(site.id,site.name,site.description,site.wonumber,site.supervisor,site.coordinates,site.area,site.province,site.visit_by)
        return html
        
    @expose()
    def save_edit_estimate_sites(self,**kw):
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == kw['edit_siteid']). \
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
        quotelist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.idsite == kw['siteid']). \
                order_by(desc(JistEstimating3yrEssPalisadeQuotes.id)).all()
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
    def get_estimate_quote_list_all(self,**kw):
        quotelist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                order_by(desc(JistEstimating3yrEssPalisadeQuotes.id)).all()
        quoteitemsvalue_all = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
        if not quoteitemsvalue_all: quoteitemsvalue_all = 0
        allquotes = format_decimal(quoteitemsvalue_all, format='#,##0.00;-#0.00',locale='en')
        html = """
               <h3 class="ui-widget-shadow">All Quotes 
               <span style="float:right">%s</span>
               </h3>
               <table id="quote_list_all">
               <th>Quote No </th>
               <th>Site ID </th>
               <th>Site Name </th>
               <th>Quote Date</th>
               <th>WO Number</th>
               <th>Total Excl</th>
               """%(allquotes)
        html2 = '' 
        for quote in quotelist:
            site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                    filter(JistEstimating3yrEssPalisadeSites.id == quote.idsite). \
                    one()
            quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                    filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quote.id). \
                    value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
            if not quoteitemsvalue: quoteitemsvalue = 0
            quoteitemstotal = format_decimal(quoteitemsvalue, format='#,##0.00;-#0.00',locale='en')
            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td align='right'>%s</td>
                   </tr>

                   """%(quote.id,site.id,site.name,quote.estdate,site.wonumber,quoteitemstotal)
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def get_estimate_quote_items(self,**kw):
        quote_scopes = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteScope). \
                filter(JistEstimating3yrEssPalisadeQuoteScope.idquote == kw['quoteid']). \
                all()
        quoteitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == kw['quoteid']). \
                all()
        quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == kw['quoteid']). \
                value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
        html = """
               <p/>
               <h3 class="ui-widget-shadow">Quote Number: %s 
               <span style="float:right">%s</span>
                    <a href="/est3yresspalisadecont/ajaxexport_excelquote/%s">
                    <img id="export_excel_est" src="/images/x-office-document.png" align="right"></img>
                    </a>
                    <a href="/est3yresspalisadecont/export_quote_by_id_pdf/%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
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
               """%(kw['quoteid'],quoteitemsvalue,kw['quoteid'],kw['quoteid'])
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
                   </table><p/>
                """

        html4 = """
                <div id = "estimate_quote_scope"></div>
                <button name="button_quote_create_scope" id="button_quote_create_scope">Add Quotation Scope</button> 
                <p/>
               <h3 class="ui-widget-shadow">Scope for Quote Number: %s 
               <span style="float:right"></span>
                    <a href="/est3yresspalisadecont/export_quote_scope_pdf/%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a>
               </h3>
               <table id="quote_scope_items">
               <th>ID </th>
               <th>Description</th>
               <th>Unit</th>
               <th>Quantity</th>
               <th>Delete</th>
               """%(kw['quoteid'],kw['quoteid'])
        html5 = '' 
        for quote in quote_scopes:
            scope = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                    filter(JistEstimating3yrEssPalisadeSiteSOW.id == quote.idscope). \
                    one()
            htmltemp5 = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td width='80px' align="right">%s</td>
                    <td width='25px'> <img  id="delete_quoteitem" src="/images/delete.png"> </img></td>
                   </tr>
                   """%(quote.id,scope.scope,scope.unit,scope.quantity)
            html5 = html5 + htmltemp5
        html6 = """
                   </table>
                """
        return html + html2 + html3 + html4 + html5 + html6

    @expose()
    def get_form_quote_scopes(self,**kw):
        scopes = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                filter(JistEstimating3yrEssPalisadeSiteSOW.idsite == kw['siteid']). \
                all()

        formupdate3 = """
                      <label for="%s">%s</label>
                      <select id="id_scope_dropdown" name="id_scope_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("scope_dropdown","All Site Scopes")
        for sts in scopes:
            formupdate3temp = """

                            <option value="%s">%s</option>

                              """%(sts.id,sts.scope)
        
            formupdate3 = formupdate3 + formupdate3temp 

        formupdate3 = formupdate3 + "</select>"
        html = """
                    <form id="frm_edit_quote_scope">
                    <fieldset>
                      <label for="%s">%s</label>
                      <input  id="%s" name="%s" value="%s" style="display:block"/>
                        %s
                      <button id="save_quote_scope">Add Scope To Quote</button>
                    </fieldset>
                    </form>
              """%('quoteid','Quote ID','quoteid','quoteid',kw['quoteid'],formupdate3)

        return html
    
    @expose()
    def save_quote_scope(self,**kw):
        #for k,w in enumerate(kw):
            #print k,w
        idquote = kw['quoteid']
        idscope = kw['id_scope_dropdown']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        newscope = JistEstimating3yrEssPalisadeQuoteScope(
                                       idquote = idquote,
                                       idscope = idscope,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssPalisade.add(newscope)
        DBS_Jist3yrEssPalisade.flush()

    
    @expose()
    def get_estimate_quote_items_edit(self,**kw):
        quoteitem = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.id == kw['itemid']). \
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
        quoteitem = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.id == kw['itemid']). \
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
        new_quote = JistEstimating3yrEssPalisadeQuotes(
                                       idsite = jcno,
                                       estdate = datetime.date(datetime.now()),
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssPalisade.add(new_quote)
        DBS_Jist3yrEssPalisade.flush()
        scp_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeItems). \
                    all()
        #print new_quote
        for item in scp_items:
            new_quote_bqitem = JistEstimating3yrEssPalisadeQuoteBQItems(
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
            DBS_Jist3yrEssPalisade.add(new_quote_bqitem)
        DBS_Jist3yrEssPalisade.flush()
            #print new_quote_bqitem

    @expose()
    def ajaxdeletequoteitem(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        quoteitem = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.id == kw['itemid']). \
                one()
        DBS_Jist3yrEssPalisade.delete(quoteitem)
        return

    @expose()
    def ajaxaddnewquote_oneitem(self,quoteid,bqitemid, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        item = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeItems). \
                filter(JistEstimating3yrEssPalisadeItems.id == int(bqitemid)). \
                    one()
        new_quote_bqitem = JistEstimating3yrEssPalisadeQuoteBQItems(
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
        DBS_Jist3yrEssPalisade.add(new_quote_bqitem)
        DBS_Jist3yrEssPalisade.flush()

    @expose()
    def ajaxaddnewquoteempty(self,jcno, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_quote = JistEstimating3yrEssPalisadeQuotes(
                                       idsite = jcno,
                                       estdate = datetime.date(datetime.now()),
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssPalisade.add(new_quote)
        DBS_Jist3yrEssPalisade.flush()

    @expose()
    def ajaxexport_excelquote(self,quoteid, **kw):
        quoteitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                all()
        quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
        #for k, w in kw.iteritems():
        #    print k, w
        #print datestart, dateend
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.xls'
        filename = os.path.join(est_excel_dirname, str(fname))
        #print filename
        templatename = "SteelPalisadeTemplate.xls"
        templatewb = open_workbook(os.path.join(est_excel_template_dir,templatename), formatting_info=True, on_demand=True) 
        #wb = Workbook()
        wb = copy(templatewb)
        #ws = wb.add_sheet('Type examples')
        ws = wb.get_sheet(0)
        rowno = 16
        style = xlwt.XFStyle()
        #style.num_format_str = '"R"#,##0.00_);("R"#,##'
        style.num_format_str = '#,##0.00_);(#,##'

        for quoteitem in quoteitems:
            item = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeItems). \
                    filter(JistEstimating3yrEssPalisadeItems.id == int(quoteitem.idbqitem)). \
                        one()
            ws.row(rowno).write(0,item.itemno)
            ws.row(rowno).write(1,quoteitem.description)
            ws.row(rowno).write(2,quoteitem.units)
            ws.row(rowno).write(3,quoteitem.quantity)
            ws.row(rowno).write(4,quoteitem.price,style=style)
            ws.row(rowno).write(5,quoteitem.total,style=style)
            rowno += 1
        #Add The Top Data
        quote = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.id == quoteid). \
                one()
        sitequotelist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.idsite == quote.idsite). \
                order_by(desc(JistEstimating3yrEssPalisadeQuotes.id)).all()
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == quote.idsite). \
                one()

        rowtop = 6
        coltop = 2
        ws.row(rowtop).write(coltop,quote.estdate)
        ws.row(rowtop+1).write(coltop,site.name)
        ws.row(rowtop+2).write(coltop,site.wonumber)
        ws.row(rowtop+3).write(coltop+2,site.id)
        ws.row(rowtop+4).write(coltop,quote.id)
        ws.row(rowtop+5).write(coltop,site.supervisor)
        allquotes = ','.join([str(quote.id) for quote in sitequotelist])
        ws.row(rowtop+7).write(coltop,allquotes)

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
        new_file = JistEstimating3yrEssPalisadePhotos(filename=big_file_base,
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
        DBS_Jist3yrEssPalisade.add(new_file)
        DBS_Jist3yrEssPalisade.flush()
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
        thisuploads = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                filter(JistEstimating3yrEssPalisadePhotos.jcno==int(siteid)). \
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
        thisupload = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                filter(JistEstimating3yrEssPalisadePhotos.filename==fname). \
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
        if not thisupload.defaultpic:
            thisupload.defaultpic = False
        return dict(page='JIST Estimating: ESS Palisade Picture Viewer',
                   appname = 'Palisade3yrEss',
                   srcpic=srcpic,
                   srcid=thisupload.pic_id,
                   blndefaultpic=thisupload.defaultpic,
                   thisupload=thisupload,
                   owner=userowner.user_name,
                   )

    @expose()
    def rotate_pic(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        if kw["appname"] == 'Palisade3yrEss':
            thisupload = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                    filter(JistEstimating3yrEssPalisadePhotos.pic_id==kw["currentpicid"]). \
                    one()
        if kw["appname"] == 'HSF3yrEss':
            thisupload = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFPhotos). \
                    filter(JistEstimating3yrEssHSFPhotos.pic_id==kw["currentpicid"]). \
                    one()
        if kw["appname"] == 'Eskom5yrFencing':
            thisupload = DBS_Jist5yrEskomFencing.query(JistEstimating5yrEskomFencingPhotos). \
                    filter(JistEstimating5yrEskomFencingPhotos.pic_id==kw["currentpicid"]). \
                    one()
        userpath = os.path.join(UPLOAD_DIRECTORY, str(thisupload.takenby))
        thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        img = Image.open(srcpic)
        imgthumb = Image.open(srcthumb)
        #img = img.rotate(90,expand=True)
        img = img.transpose(Image.ROTATE_90)
        imgthumb = imgthumb.transpose(Image.ROTATE_90)
        img.save(srcpic,quality=100)
        imgthumb.save(srcthumb,quality=100)
        #im = Image.open(srcpic)
        #im.show()
        """
        exifdict = im._getexif()
        if exifdict:
            for k in exifdict.keys():
                if k in TAGS.keys():
                    print TAGS[k], exifdict[k]
                else:
                    print k, exifdict[k]
                return
        """

    @expose()
    def setdefault_pic(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        if kw["appname"] == 'Palisade3yrEss':
            thisupload = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                    filter(JistEstimating3yrEssPalisadePhotos.pic_id==kw["currentpicid"]). \
                    one()
        if kw["appname"] == 'HSF3yrEss':
            thisupload = DBS_Jist3yrEssHSF.query(JistEstimating3yrEssHSFPhotos). \
                    filter(JistEstimating3yrEssHSFPhotos.pic_id==kw["currentpicid"]). \
                    one()
        if kw["appname"] == 'Eskom5yrFencing':
            thisupload = DBS_Jist5yrEskomFencing.query(JistEstimating5yrEskomFencingPhotos). \
                    filter(JistEstimating5yrEskomFencingPhotos.pic_id==kw["currentpicid"]). \
                    one()
        thisupload.defaultpic = not thisupload.defaultpic

    @expose()
    def get_default_pic(self,**kw):
        siteid = kw['siteid']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        htmlheader = """
                    <div class="">
                    <h5 class="ui-widget-header">Default Pic For SiteNo %s .</h5>
                    """%(siteid)
        htmlout = ''
        thisuploads = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                filter(JistEstimating3yrEssPalisadePhotos.jcno==int(siteid)). \
                filter(JistEstimating3yrEssPalisadePhotos.defaultpic==True). \
                all()
        for thisupload in thisuploads[::-1]:
            userpath = os.path.join('/estimating_docs/pictures', str(thisupload.takenby))
            thumbpath = os.path.join(userpath, 'thumbs')
            bigpicpath = os.path.join(userpath, 'pics')
            srcthumb = os.path.join(thumbpath, thisupload.thumbname)
            srcpic = os.path.join(bigpicpath, thisupload.filename)
            htmltemp = """
                                    <img  class="thumb_clicked" value="%s" src="%s" alt="" width="640px" height="480px" />
                        """%(thisupload.filename,srcpic)
            htmlout = htmlout + htmltemp
        htmlclose = """
                    </div>
                    """
        return htmlheader + htmlout + htmlclose
    
    @expose()
    def get_site_scope(self,**kw):
        scopeitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                filter(JistEstimating3yrEssPalisadeSiteSOW.idsite == kw['siteid']). \
                all()
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
                one()
        html = """
                
                <p/>
                <button class="ui-widget ui-widget-content ui-state-default" id="button_add_new_site_scope">Add Scope Item</button>
                <p/>
               <h3 class="ui-widget-shadow">Estimate Scoped Items for Site: %s 
               <span style="float:right"></span>
                    <a href="/est3yresspalisadecont/export_site_scope_pdf/%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a>
               </h3>
               <table id="site_scope_items">
               <th>ID </th>
               <th>Description</th>
               <th>Unit</th>
               <th>Quantity</th>
               <th>Edit</th>
               <th>Delete</th>
               """%(site.name,site.id)
        html2 = '' 
        for scope in scopeitems:
            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td align="right">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                    <td width='25px'> <img  id="delete_scopeitem" src="/images/delete.png"> </img></td>
                   </tr>

                   """%(scope.id,scope.scope,scope.unit,scope.quantity)
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def get_despatch_by_jcno(self,**kw):
        despatchitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.jcno == kw['sitejcno']). \
                all()
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==kw['sitejcno']). \
               one()
        html = """
                
                <p/>
               <h3 class="ui-widget-shadow">Items Despatched For JCNo: %s 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_scope_pdf/%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
               <table id="tbl_despatch_by_jcno">
               <th>ID </th>
               <th>Description</th>
               <th>Qty</th>
               <th>Despatched To:</th>
               <th>Comment</th>
               <th>Date Despatched</th>
               """%(contract.site,contract.jno)
        html2 = '' 
        for scope in despatchitems:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()
            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td width="250px">%s</td>
                   <td width="25px">%s</td>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="25px">%s</td>
                   </tr>

                   """%(scope.id,matlist.description,scope.qty,scope.despatch_to,scope.comment,scope.date_despatch)
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def ajaxAddSiteScope(self,jno_id,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeSiteSOW(idsite=jno_id,
                                      scope=kw['newscopedescription'],
                                      unit=kw['newscopeunit'],
                                      quantity=kw['newscopeqty'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def ajaxEditSiteScope(self,scopeid,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        scopesite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                filter(JistEstimating3yrEssPalisadeSiteSOW.id == scopeid). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        scopesite.scope=kw['editsitescopedescription']
        scopesite.unit=kw['editsitescopeunit']
        scopesite.quantity=kw['editsitescopeqty']
        scopesite.useridedited = usernow.user_id
        scopesite.dateedited = datetime.date(datetime.now())
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def ajaxDeleteSiteScope(self,scopeid,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        scopesite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                filter(JistEstimating3yrEssPalisadeSiteSOW.id == scopeid). \
                one()
        DBS_Jist3yrEssPalisade.delete(scopesite)
        return

    @expose()
    def ajaxDeleteQuoteScope(self,scopeid,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        scopesite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteScope). \
                filter(JistEstimating3yrEssPalisadeQuoteScope.id == scopeid). \
                one()
        DBS_Jist3yrEssPalisade.delete(scopesite)
        return

    @expose()
    def ajaxAddQuoteScope(self,jno_id,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeQuoteScope(
                                      idquote=kw['quoteid'],
                                      idscope=kw['scopeid'],
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def export_quote_by_id_pdf(self,quoteid, **kw):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        wip1 = []
        userdata = {}
        quoteitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                all()
        quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
        #Add The Top Data
        quote = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.id == quoteid). \
                one()
        sitequotelist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.idsite == quote.idsite). \
                order_by(desc(JistEstimating3yrEssPalisadeQuotes.id)).all()
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == quote.idsite). \
                one()
        allquotes = ','.join([str(quote.id) for quote in sitequotelist])
        if not quoteitemsvalue: quoteitemsvalue = 0
        quoteitemstotal = format_decimal(quoteitemsvalue, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in quoteitems:
            item = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeItems). \
                    filter(JistEstimating3yrEssPalisadeItems.id == int(k.idbqitem)). \
                        one()
            wip1.append({ 'id':k.id,
                          'item':item.itemno,
                          'description':k.description,
                            'units': k.units,
                            'quantity': k.quantity,
                            'price':k.price,
                            'total':k.total,
                            'useridnew':k.useridnew,
                            'useridedited':k.useridedited,
                            'dateedited':k.dateedited,
                            'timeedited':k.timeedited,
                         })
        count = len(wip1) 
        userdata = {'date':datetime.date(datetime.now()),
                'project':site.name,
                'wonumber':site.wonumber,
                'supervisor':site.supervisor,
                'header1':'Steel Palisade - Schedule or Rates',
                'siteid':site.id,
                'area':site.area,
                'quoteno':quote.id,
                'tenderno':'285Q/2012/13',
                'prevquotes':allquotes,
                'totalexcl':quoteitemstotal,
                } 
        headers =["Item","Description","Units","Qty","Price","Total Excl"]
        headerwidths=[80,250,80,80,120]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        fname = "SPF-Quote-"+str(quote.id)+'-'+site.name+'-'+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        pdffile.CreatePDFESSPalisadeQuote(userdata,wip1,headers,headerwidths,quoteitemstotal)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_site_scope_pdf(self,siteid, **kw):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        wip1 = []
        userdata = {}
        scopeitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                filter(JistEstimating3yrEssPalisadeSiteSOW.idsite == siteid). \
                all()
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == siteid). \
                one()
        thisupload = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                filter(JistEstimating3yrEssPalisadePhotos.jcno==int(siteid)). \
                filter(JistEstimating3yrEssPalisadePhotos.defaultpic==True). \
                first()
        #for thisupload in thisuploads[::-1]:
        picpath = os.path.join(estimating_dirname,'pictures')
        userpath = os.path.join(picpath, str(thisupload.takenby))
        thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        quoteitemstotal = 0
        defaultimgpth = ''
        for k in scopeitems:
            wip1.append({ 'id':k.id,
                          'description':k.scope,
                            'units': k.unit,
                            'quantity': k.quantity,
                         })
        count = len(wip1) 
        userdata = {'date':datetime.date(datetime.now()),
                'project':site.name,
                'wonumber':site.wonumber,
                'supervisor':site.supervisor,
                'header1':'Steel Palisade - Site Scope Of Work ',
                'siteid':site.id,
                'area':site.area,
                #'quoteno':quote.id,
                'tenderno':'285Q/2012/13',
                #'prevquotes':allquotes,
                #'totalexcl':quoteitemstotal,
                } 
        headers =["Description","Units","Qty"]
        headerwidths=[250,80,80]
        fname = "SPF-SiteScope-"+site.name+'-'+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        pdffile.CreatePDFESSPalisadeSiteScope(userdata,wip1,headers,headerwidths,0,srcpic)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_quote_scope_pdf(self,quoteid, **kw):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = {}
        quoteitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                all()
        quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
        #Add The Top Data
        quote = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.id == quoteid). \
                one()
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == quote.idsite). \
                one()
        scopeitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteScope). \
                filter(JistEstimating3yrEssPalisadeQuoteScope.idquote == quoteid). \
                all()
        #site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
        #        filter(JistEstimating3yrEssPalisadeSites.id == site.id). \
        #        one()
        thisupload = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                filter(JistEstimating3yrEssPalisadePhotos.jcno== site.id). \
                filter(JistEstimating3yrEssPalisadePhotos.defaultpic==True). \
                first()
        sitequotelist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.idsite == quote.idsite). \
                order_by(desc(JistEstimating3yrEssPalisadeQuotes.id)).all()
        #for thisupload in thisuploads[::-1]:
        picpath = os.path.join(estimating_dirname,'pictures')
        userpath = os.path.join(picpath, str(thisupload.takenby))
        thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        quoteitemstotal = 0
        defaultimgpth = ''
        allquotes = ','.join([str(quote.id) for quote in sitequotelist])
        if not quoteitemsvalue: quoteitemsvalue = 0
        quoteitemstotal = format_decimal(quoteitemsvalue, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in scopeitems:
            scope = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                    filter(JistEstimating3yrEssPalisadeSiteSOW.id == k.idscope). \
                    one()
            wip1.append({ 'id':k.id,
                          'description':scope.scope,
                            'units': scope.unit,
                            'quantity': scope.quantity,
                         })
        count = len(wip1) 
        userdata = {'date':datetime.date(datetime.now()),
                'project':site.name,
                'wonumber':site.wonumber,
                'supervisor':site.supervisor,
                'header1':'Steel Palisade - Quote Scope Of Work ',
                'siteid':site.id,
                'area':site.area,
                'quoteno':quote.id,
                'tenderno':'285Q/2012/13',
                'prevquotes':allquotes,
                'totalexcl':quoteitemstotal,
                } 
        headers =["Description","Units","Qty"]
        headerwidths=[250,80,80]
        fname = "SPF-QuoteScope-"+str(quote.id)+'-'+site.name+'-'+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        pdffile.CreatePDFESSPalisadeQuoteScope(userdata,wip1,headers,headerwidths,0,srcpic)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    ##############################
    #Production Sections Starts
    ##############################
    ##############################

    @expose()
    def get_new_estimate_contract_link(self,**kw):
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        estsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                all()
        html = """
                    <form id ='frm_est_new_contract_link'>
                    <fieldset>

               """

        formupdate3 = """
                      <label for="%s">%s</label>
                      <select id="id_jcno_dropdown" name="jcno_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("scope_dropdown","All JCNo")
        for sts in contracts:
            formupdate3temp = """

                            <option value="%s">%s-%s-%s</option>

                              """%(sts.jno,sts.jno,sts.site,sts.description)
        
            formupdate3 = formupdate3 + formupdate3temp 
        formupdate3 = formupdate3 + "</select>" +"<div id='booleancontractlinked'></div>"

        formupdate4 = """
                      <label for="%s">%s</label>
                      <select id="id_estsite_dropdown" name="estsite_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("scope_dropdown","All Estimate Sites")
        for sts in estsites:
            formupdate4temp = """

                            <option value="%s">%s-%s-%s</option>

                              """%(sts.id,sts.id,sts.name,sts.area)
        
            formupdate4 = formupdate4 + formupdate4temp 
        formupdate4 = formupdate4 + "</select>" +"<div id='booleanestsitelinked'></div>"



        html2 = '' 
        for scope in estsites:
            htmltemp = """

                       """
            html2 = html2 + htmltemp
        html3 = """
                <button class="button_do_link ui-widget ui-widget-content ui-state-default" id="button_do_add_new_site_link">Link Site and JCNo</button>
                <button class="button_do_link ui-widget ui-widget-content ui-state-default" id="button_cancel_new_site_link">Cancel</button>
                   </fieldset></form>
                """
        return html + formupdate3+ formupdate4 + html2 + html3

    @expose()
    def save_new_estimate_contract_link(self,**kw):
        #for k,w in kw.iteritems():
            #print k,w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_link = JistEstimating3yrEssPalisadeJCNOEstLink(
                                       jcnoid = kw['jcno_dropdown'],
                                       siteid = kw['estsite_dropdown'],
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrEssPalisade.add(new_link)
        DBS_Jist3yrEssPalisade.flush()

    @expose()
    def get_edit_estimate_contracts_link(self,**kw):
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
                one()
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==kw['contractid']). \
                one()
        html = """
                        <form id ='frm_edit_est_new_site'>
                        <fieldset>

               """
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        estsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                all()

        formupdate3 = """
                      <label for="%s">%s</label>
                      """
        html4 = self.producehtmllistjcnobox('jnothisname',int(contract.jno),contracts)
        html5 = self.producehtmllistestsitebox('estthisname',int(site.id),estsites)
        html3 = """

                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_edit_contract_link">Link Site and JCNo</button>
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_do_cancel_edit_contract_link">Cancel</button>
                        </fieldset>
                        </form>

                """
        #html4 = self.producehtmllistjcnobox('thisname',600,contracts)
        return html + formupdate3+ html4 + html5 + html3

    @expose()
    def get_estimate_contracts_linked(self,**kw):
        html = ''
        html1 = """<table id='estimate_contracts_table' class='table_estdata'>
                   <th> Console ID</th>
                   <th> Est ID</th>
                   <th> JCNo</th>
                   <th> Date</th>
                   <th> Site Name</th>
                   <th> Description</th>
                   <th> Area</th>
                   <th> WONumber</th>
                   <th> Supervisor</th>
                   <th> Edit</th>
                   <th> Open</th>
                """
        html3 = """
                            </table>
                """
        if kw['switch']=="All":
            linkedsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   order_by(desc(JistEstimating3yrEssPalisadeJCNOEstLink.id)).all()
            #sites = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                   #order_by(desc(JistEstimating3yrBuildingSites.id)).all()
            temphtml1 = ""
            html2 = ""
            for thissite in linkedsites:
                scp = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                        filter(JistEstimating3yrEssPalisadeSites.id==int(thissite.siteid)). \
                        one()
                temphtml1 = """
                            <tr> <td width="80px"> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td>  
                            <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                            </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                            </td></tr>
                            """%(thissite.id,scp.id,thissite.jcnoid,scp.date,scp.name,scp.description,scp.area,scp.wonumber,scp.supervisor)
                html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        elif kw['switch']=="SearchName":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            linkedsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   order_by(desc(JistEstimating3yrEssPalisadeJCNOEstLink.id)).all()
            sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                    filter(JistEstimating3yrEssPalisadeSites.name.like(searchphrase)). \
                   order_by(desc(JistEstimating3yrEssPalisadeSites.id)).all()
            temphtml1 = ""
            html2 = ""
            for thissite in linkedsites:
                for site in sites:
                    if site.id == thissite.siteid:
                        scp = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                                filter(JistEstimating3yrEssPalisadeSites.id==int(thissite.siteid)). \
                                one()
                        temphtml1 = """
                                    <tr> <td width="80px"> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td>  
                                    <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                                    </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                                    </td></tr>
                                    """%(thissite.id,scp.id,thissite.jcnoid,scp.date,scp.name,scp.description,scp.area,scp.wonumber,scp.supervisor)

                        html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        elif kw['switch']=="SearchArea":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            linkedsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   order_by(desc(JistEstimating3yrEssPalisadeJCNOEstLink.id)).all()
            sites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                    filter(JistEstimating3yrEssPalisadeSites.area.like(searchphrase)). \
                   order_by(desc(JistEstimating3yrEssPalisadeSites.id)).all()
            
            temphtml1 = ""
            html2 = ""
            for thissite in linkedsites:
                for site in sites:
                    if site.id == thissite.siteid:
                        scp = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                                filter(JistEstimating3yrEssPalisadeSites.id==int(thissite.siteid)). \
                                one()
                        temphtml1 = """
                                    <tr> <td width="80px"> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td>  
                                    <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                                    </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                                    </td></tr>
                                    """%(thissite.id,scp.id,thissite.jcnoid,scp.date,scp.name,scp.description,scp.area,scp.wonumber,scp.supervisor)

                        html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        else:
            return html

    @expose()
    def get_link_contract(self,**kw):
        linkedsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
               filter(JistEstimating3yrEssPalisadeJCNOEstLink.jcnoid==int(kw['id_jcno'])).all()
        if linkedsites:
            html = """
                        Linked To Site: %s
                        
                   """%(linkedsites[0].siteid)
        else:
            html = """
                    Not Linked 
                   """
        return html

    @expose()
    def get_contract_data_jcno(self,**kw):
        #site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
        #        filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
        #        one()
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==kw['id_jcno']). \
                one()
        html = """
                    Linked To Site: %s
                    
               """%(linkedsites[0].siteid)
        html = """
                Not Linked 
               """
        return html

    @expose()
    def get_link_estsite(self,**kw):
        linkedsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
               filter(JistEstimating3yrEssPalisadeJCNOEstLink.siteid==int(kw['id_estsite'])).all()
        if linkedsites:
            html = """
                        Linked To JCNo: %s
                        
                   """%(linkedsites[0].jcnoid)
        else:
            html = """
                    Not Linked 
                   """
        return html

    @expose()
    def get_site_quotelist_andquotes(self,**kw):
        quotelist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuotes). \
                filter(JistEstimating3yrEssPalisadeQuotes.idsite == kw['siteid']). \
                order_by(desc(JistEstimating3yrEssPalisadeQuotes.id)).all()
        returnhtml = ''
        for thisquote in quotelist:
            quote_scopes = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteScope). \
                    filter(JistEstimating3yrEssPalisadeQuoteScope.idquote == thisquote.id). \
                    all()
            quoteitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                    filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == thisquote.id). \
                    all()
            quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                    filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == thisquote.id). \
                    value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
            html = """
                   <p/>
                   <h3 class="ui-widget-shadow">Quote Number: %s 
                   <span style="float:right">%s</span>
                   </h3>
                   <table id="quote_items">
                   <th>ID </th>
                   <th>Description</th>
                   <th>Unit</th>
                   <th>Quantity</th>
                   <th>Price</th>
                   <th>Total</th>
                   """%(thisquote.id,quoteitemsvalue)
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
                       </tr>

                       """%(quote.id,quote.description,quote.units,quote.quantity,quote.price,quote.total)
                html2 = html2 + htmltemp
            html3 = """
                       </table><p/>
                    """

            html4 = """
                    <div id = "estimate_quote_scope"></div>
                    <button value="%s" name="button_contract_create_scope" class="button_contract_create_scope">Add As Contract Scope</button> 

                    <p/>
                   <h3 class="ui-widget-shadow">Scope for Quote Number: %s 
                   <span style="float:right"></span>
                        <a href="/est3yresspalisadecont/export_quote_scope_pdf/%s">
                        <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                        </a>
                   </h3>
                   <table id="quote_scope_items">
                   <th>ID </th>
                   <th>Description</th>
                   <th>Unit</th>
                   <th>Quantity</th>
                   <th>Delete</th>
                   """%(thisquote.id,thisquote.id,thisquote.id)
            html5 = '' 
            for quote in quote_scopes:
                scope = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                        filter(JistEstimating3yrEssPalisadeSiteSOW.id == quote.idscope). \
                        one()
                htmltemp5 = """
                       <tr>
                       <td>%s</td>
                       <td>%s</td>
                       <td>%s</td>
                       <td width='80px' align="right">%s</td>
                        <td width='25px'> <img  id="delete_quoteitem" src="/images/delete.png"> </img></td>
                       </tr>
                       """%(quote.id,scope.scope,scope.unit,scope.quantity)
                html5 = html5 + htmltemp5
            html6 = """
                       </table>
                    """

            returnhtml = returnhtml + html + html2 + html3 + html4 + html5 + html6
        return returnhtml

    def producehtmllistjcnobox(self,idname,selected_one,thelist):
        html2 =""" <select name="%s" id="%s">"""%(idname,idname)
        for k in thelist:
            if k.jno == selected_one:
                html2temp = """
                                <option value="%s" selected="selected" style="display: block" class="text ui-widget-content ui-corner-all">%s-%s</option>
                        """%(k.jno,k.jno,k.site)
                html2 = html2 + html2temp
            else:
                html2temp = """
                                <option value="%s" style="display: block" class="text ui-widget-content ui-corner-all">%s-%s</option>
                        """%(k.jno,k.jno,k.site)
                html2 = html2 + html2temp

        return html2 +"</select>"

    def producehtmllistestsitebox(self,idname,selected_one,thelist):
        html2 =""" <select name="%s" id="%s">"""%(idname,idname)
        for k in thelist:
            if k.id == selected_one:
                html2temp = """
                                <option value="%s" selected="selected" style="display: block" class="text ui-widget-content ui-corner-all">%s-%s</option>
                        """%(k.id,k.id,k.name)
                html2 = html2 + html2temp
            else:
                html2temp = """
                                <option value="%s" style="display: block" class="text ui-widget-content ui-corner-all">%s-%s</option>
                        """%(k.id,k.id,k.name)
                html2 = html2 + html2temp

        return html2 +"</select>"

    @expose()
    def save_new_scope_to_jcno(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        jcno = kw['jcno']
        estid = kw['siteid']
        quoteid = kw['quoteid']
        quote_scopes = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteScope). \
                filter(JistEstimating3yrEssPalisadeQuoteScope.idquote == quoteid). \
                all()
        quoteitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                all()
        quoteitemsvalue = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeQuoteBQItems). \
                filter(JistEstimating3yrEssPalisadeQuoteBQItems.idquote == quoteid). \
                value(func.sum(JistEstimating3yrEssPalisadeQuoteBQItems.total))
        linkedsites = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
               filter(JistEstimating3yrEssPalisadeJCNOEstLink.jcnoid==int(kw['jcno'])).first()
        linkedsites.quoteid = quoteid
        html5 = '' 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        for quote in quote_scopes:
            scope = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                    filter(JistEstimating3yrEssPalisadeSiteSOW.id == quote.idscope). \
                    one()
            newscopes = JistContractScope(jno=jcno,
                                          item='',
                                          description = scope.scope,
                                          unit = scope.unit,
                                          qty = scope.quantity,
                                          useridnew = usernow.user_id,
                                          useridedited = usernow.user_id,
                                          dateadded = datetime.date(datetime.now()),
                                          dateedited = datetime.date(datetime.now())
                                          )                              
            DBS_ContractData.add(newscopes)
        DBS_ContractData.flush()

    @expose()
    def ajaxAddStandardItem(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeStandardMaterialList(
                                      description=kw['newlistdescription'],
                                      size=kw['newlistsize'],
                                      length=kw['newlistlength'],
                                      height=kw['newlistheight'],
                                      weight=kw['newlistweight'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def ajaxEditStandardItem(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        scopesite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == kw['editlistid']). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        scopesite.description=kw['editlistdescription']
        scopesite.size=kw['editlistsize']
        scopesite.length=kw['editlistlength']
        scopesite.height=kw['editlistheight']
        scopesite.weight=kw['editlistweight']
        scopesite.useridedited = usernow.user_id
        scopesite.dateedited = datetime.date(datetime.now())
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def ajaxAddSiteRequirement(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeSiteRequirements(
                                      linkid=kw['linkid'],
                                      matlistid=kw['newlistdescription'],
                                      qty=int(kw['newlistqty']),
                                      instruction=kw['newlist_instruction'],
                                      date_req=kw['newlist_date_req'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def get_site_requirements(self,**kw):
        scopeitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.linkid == int(kw['linkid'])). \
                all()
        linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
               filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==int(kw['linkid'])).one()
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
               one()
        #site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                #filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
                #one()

        html = """
                <p/>
               <h3 class="ui-widget-shadow">Estimated Material Items for Contract: %s 
               <span style="float:right"></span>
                    <a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a>
               </h3>
               <table id="site_requirement_items">
               <th>ID </th>
               <th>Description</th>
               <th>Quantity</th>
               <th>Instruction</th>
               <th>Date Required</th>
               <th>Added By</th>
               <th>Date Added</th>
               <th>Edited By</th>
               <th>Date Edited</th>
               <th>Edit</th>
               """%(contract.site,linkedsite.id)
        html2 = '' 
        for scope in scopeitems:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()

            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="80px" align='right'>%s</td>
                   <td width="180px">%s</td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                   </tr>

                   """%(scope.id,matlist.description,scope.qty,scope.instruction,scope.date_req,
                           scope.useridnew,
                           scope.dateadded,
                           scope.useridedited,
                           scope.dateedited,
                           )
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def get_edit_site_requirements(self,**kw):
        #site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                #filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
                #one()
        requirement = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.id == int(kw['requireid'])). \
                one()
        matlistone = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == requirement.matlistid). \
                one()
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()


        html1 = """
                <div id="dialog_edit_site_requirements" title="Edit Item To Site">
                    <form id="edit_site_requirements_form">
                    <fieldset>
                        <label for="editlistid">ID</label><br/>
                        <input type="text" value="%s" name="editlistid" id="editlistid" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="editlistdescription">Description</label><br/>
                        <select id="editlistdescription" name="editlistdescription">
                """%(requirement.id)
        html2 = ''
        for mat in matlistall:
            if mat.id == matlistone.id:
                html2temp = """
                                       <option value="%s" selected="selected" >%s</option>
                            """%(mat.id,mat.description)
            else:
                html2temp = """
                                       <option value="%s" >%s</option>
                            """%(mat.id,mat.description)
            html2 = html2 + html2temp

        html3 = """
                        </select><br/>
                        <!--label for="editlistunit">Unit</label><br/>
                        <input type="text" name="editlistunit" id="editlistunit" class="text ui-widget-content ui-corner-all" /><br/-->
                        <label for="editlistqty">Qty</label><br/>
                        <input type="text" value="%s" name="editlistqty" id="editlistqty" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="editlist_instruction">Instruction</label><br/>
                        <input type="text" value="%s" name="editlist_instruction" id="editlist_instruction" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="editlist_date_req">Date Required</label><br/>
                        <input type="text" date="%s" name="editlist_date_req" id="editlist_date_req" class="text ui-widget-content ui-corner-all" /><br/>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_do_edit_site_requirements">Edit Site Requirements</button> 
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_cancel_edit_site_requirements">Cancel</button> 
                
                    </fieldset>
                    </form>
                </div>
            """%(requirement.qty,requirement.instruction,requirement.date_req)
        return html1 + html2 + html3
    
    @expose()
    def ajaxEditSiteRequirements(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        requirement = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.id == int(kw['editlistid'])). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        requirement.matlistid=kw['editlistdescription']
        requirement.qty=kw['editlistqty']
        requirement.instruction=kw['editlist_instruction']
        requirement.date_req=kw['editlist_date_req']
        requirement.useridedited = usernow.user_id
        requirement.dateedited = datetime.date(datetime.now())
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def export_site_requirements_pdf(self, **kw):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        wip1 = []
        userdata = {}
        requirementitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.linkid == int(kw['linkid'])). \
                all()
        linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
               filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==int(kw['linkid'])).one()
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
               one()
        #requirement = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                #filter(JistEstimating3yrEssPalisadeSiteRequirements.id == int(kw['requireid'])). \
                #one()
        #matlistone = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                #filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == requirement.matlistid). \
                #one()
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()

        #scopeitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteSOW). \
                #filter(JistEstimating3yrEssPalisadeSiteSOW.idsite == siteid). \
                #all()
        site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                filter(JistEstimating3yrEssPalisadeSites.id == linkedsite.siteid). \
                one()
        thisupload = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadePhotos). \
                filter(JistEstimating3yrEssPalisadePhotos.jcno==linkedsite.siteid). \
                filter(JistEstimating3yrEssPalisadePhotos.defaultpic==True). \
                first()
        #for thisupload in thisuploads[::-1]:
        picpath = os.path.join(estimating_dirname,'pictures')
        userpath = os.path.join(picpath, str(thisupload.takenby))
        thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        quoteitemstotal = 0
        defaultimgpth = ''
        for k in requirementitems:
            matlistone = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == k.matlistid). \
                    one()
            wip1.append({ 'id':k.id,
                          'description':matlistone.description,
                            'units': 'Each',
                            'quantity': k.qty,
                            'instruction': k.instruction,
                         })
        count = len(wip1) 
        userdata = {'date':datetime.date(datetime.now()),
                'project':site.name,
                'wonumber':site.wonumber,
                'supervisor':site.supervisor,
                'header1':'Steel Palisade - Site Material List ',
                'siteid':site.id,
                'area':site.area,
                'jcno':contract.jno,
                'tenderno':'285Q/2012/13',
                #'prevquotes':allquotes,
                #'totalexcl':quoteitemstotal,
                } 
        headers =["Description","Units","Qty","Manufacturing Instruction"]
        headerwidths=[220,50,40,130]
        fname = "SPF-MaterialList-"+site.name+'-'+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        pdffile.CreatePDFESSPalisadeSiteMatList(userdata,wip1,headers,headerwidths,0,srcpic)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def get_non_standard_list(self,**kw):
        scopeitems = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == int(1)). \
                all()
        #site = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSites). \
                #filter(JistEstimating3yrEssPalisadeSites.id == kw['siteid']). \
                #one()

        html = """
                <p/>
               <h3 class="ui-widget-shadow">SPF Non Standard Item List 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
               <table id="site_requirement_items">
               <th>ID </th>
               <th>JCNo </th>
               <th>Description</th>
               <th>Quantity</th>
               <th>Instruction</th>
               <th>Date Required</th>
               <th>Added By</th>
               <th>Date Added</th>
               <th>Edited By</th>
               <th>Date Edited</th>
               <th>Edit</th>
               """%('linkedsite.id')
        html2 = '' 
        for scope in scopeitems:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()
            linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==scope.linkid).one()
            contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
                   one()

            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="80px" align='right'>%s</td>
                   <td width="180px">%s</td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                   </tr>

                   """%(scope.id,contract.jno,matlist.description,scope.qty,scope.instruction,scope.date_req,
                           scope.useridnew,
                           scope.dateadded,
                           scope.useridedited,
                           scope.dateedited,
                           )
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html + html2 + html3

    @expose()
    def get_stores_stock_html(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        html = """
                <button class="ui-widget ui-widget-content ui-state-default" id="button_get_stores_receive">Stores Receive</button> 
                <button class="ui-widget ui-widget-content ui-state-default" id="button_get_stores_despatch">Stores Despatch</button> 
                <button class="ui-widget ui-widget-content ui-state-default" id="button_get_stores_return">Stores Return</button> 
                <button class="ui-widget ui-widget-content ui-state-default" id="button_get_stores_stock_level">Stores Stock Level</button> 
                <p/>
               <h3 class="ui-widget-shadow">SPF Stores Data 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
                """
        return html

    @expose()
    def get_stores_stock_level_html(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        formupdate3 = '' 
        formupdate3 = """
                      <label for="%s">%s</label>
                      <select id="select_mat_dropdown" name="select_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("select_mat_dropdown","Select To View Booked Material ")
        for scope in matlistall:
            formupdate3temp = """

                            <option value="%s">%s</option>

                              """%(scope.id,scope.description)
            formupdate3 = formupdate3 + formupdate3temp 

        formupdate3 = formupdate3 + "</select>"
        html3 = """
                """
        return formupdate3 + html3

    @expose()
    def get_stores_stock_data(self,**kw):
        matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == kw['listid']). \
                one()
        requirement_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                all()
        requirement_items_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeSiteRequirements.qty))
        requirement_received_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresReceiveList). \
                filter(JistEstimating3yrEssPalisadeStoresReceiveList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresReceiveList.qty))
        despatched_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresDespatchList.qty))
        if requirement_items_total:
            req_total = requirement_items_total
        else:
            req_total = 0
        if requirement_received_total:
            receive_total = requirement_received_total
        else:
            receive_total = 0
        if despatched_total:
            despatch_total = despatched_total
        else:
            despatch_total = 0
        stocknow = receive_total - despatch_total
        futurestock = receive_total - req_total 

        html0 = """
                <table>
                <th colspan=2>Store Totals: %s</th>
                <tr>
                <td width="280px">Total Stores Received:</td>
                <td width="80px" align="right" >%s</td></tr><tr>
                <td>Total Stores Despatch:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Stock Now:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Booked:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Future Stock:</td>
                <td align="right">%s</td></tr>
                </tr></table>
                   
                """%(matlist.description,receive_total,despatch_total,stocknow,req_total,futurestock)
        html = """
                <p/>
               <h3 class="ui-widget-shadow">SPF Booked Items 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
               <table id="tbl_stores_stock_data">
               <th>ID </th>
               <th>JCNo </th>
               <th>Description</th>
               <th>Quantity</th>
               <th>Instruction</th>
               <th>Date Required</th>
               <th>Added By</th>
               <th>Date Added</th>
               <th>Edited By</th>
               <th>Date Edited</th>
               <th>Edit</th>
               """%('linkedsite.id')
        html2 = '' 
        for scope in requirement_items:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()
            linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==scope.linkid).one()
            contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
                   one()

            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="80px" align='right'>%s</td>
                   <td width="180px">%s</td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                   </tr>

                   """%(scope.id,contract.jno,matlist.description,scope.qty,scope.instruction,scope.date_req,
                           scope.useridnew,
                           scope.dateadded,
                           scope.useridedited,
                           scope.dateedited,
                           )
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html0 + html + html2 + html3

    @expose()
    def get_stores_receive_form(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        html1 = """
                    <form id="stores_receive_form">
                    <fieldset>
                        <!--label for="stores_receiveid">ID</label><br/>
                        <input type="text" name="stores_receiveid" id="stores_receiveid" class="text ui-widget-content ui-corner-all" /><br/-->
                        <label for="select_mat_dropdown">Choose and Item</label><br/>
                      <select id="select_mat_dropdown" name="select_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        html2 = ''
        for mat in matlistall:
            html2temp = """
                                   <option value="%s" >%s</option>
                        """%(mat.id,mat.description)
            html2 = html2 + html2temp

        html3 = """
                        </select><br/>
                        <label for="stores_receiveqty">Qty</label><br/>
                        <input type="text" name="stores_receiveqty" id="stores_receiveqty" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_receive_received_from">Received From</label><br/>
                        <input type="text" name="stores_receive_from" id="stores_receive_from" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_receive_date">Date Received</label><br/>
                        <input type="text" name="stores_receive_date" id="stores_receive_date" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_receive_comment">Comment</label><br/>
                        <input type="text" name="stores_receive_comment" id="stores_receive_comment" class="text ui-widget-content ui-corner-all" /><br/>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_new_mat_receive">Save New Material Receipt</button> 
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_cancel_mat_receive">Cancel</button> 
                
                    </fieldset>
                    </form>
            """
        return html1 + html2 + html3

    @expose()
    def get_stores_receive_selectbox(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        html1 = """
                    <form id="stores_receive_selectbox">
                    <fieldset>
                        <!--label for="stores_receiveid">ID</label><br/>
                        <input type="text" name="stores_receiveid" id="stores_receiveid" class="text ui-widget-content ui-corner-all" /><br/-->
                        <label for="select_mat_dropdown_receive">Choose and Item To View Receiving</label><br/>
                      <select id="select_mat_dropdown_receive" name="select_mat_dropdown_receive" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        html2 = ''
        for mat in matlistall:
            html2temp = """
                                   <option value="%s" >%s</option>
                        """%(mat.id,mat.description)
            html2 = html2 + html2temp

        html3 = """
                    </fieldset>
                    </form>
            """
        return html1 + html2 + html3

    @expose()
    def ajaxAddNewStoresReceive(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeStoresReceiveList(
                                      matlistid=kw['select_mat_dropdown'],
                                      qty=kw['stores_receiveqty'],
                                      received_from=kw['stores_receive_from'],
                                      comment=kw['stores_receive_comment'],
                                      date_received=kw['stores_receive_date'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def get_stores_receive_data(self,**kw):
        matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == kw['listid']). \
                one()
        #newscopes = JistEstimating3yrEssPalisadeStoresReceiveList(
        requirement_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                all()
        receiving_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresReceiveList). \
                filter(JistEstimating3yrEssPalisadeStoresReceiveList.matlistid == matlist.id). \
                all()
        requirement_items_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeSiteRequirements.qty))
        requirement_received_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresReceiveList). \
                filter(JistEstimating3yrEssPalisadeStoresReceiveList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresReceiveList.qty))
        despatched_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresDespatchList.qty))
        if requirement_items_total:
            req_total = requirement_items_total
        else:
            req_total = 0
        if requirement_received_total:
            receive_total = requirement_received_total
        else:
            receive_total = 0
        if despatched_total:
            despatch_total = despatched_total
        else:
            despatch_total = 0
        stocknow = receive_total - despatch_total
        futurestock = receive_total - req_total 


        html0 = """
                <table>
                <th colspan=3>Store Totals: %s </th>
                <tr>
                <td width="280px">Total Stores Received: </td>
                <td width="80px" align="right" >%s</td></tr><tr>
                <td>Total Stores Despatch:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Stock Now:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Booked:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Future Stock:</td>
                <td align="right">%s</td></tr>
                </tr></table>
                   
                """%(matlist.description,receive_total,despatch_total,stocknow,req_total,futurestock)
        html = """
                <p/>
               <h3 class="ui-widget-shadow">SPF Received Items 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
               <table id="tbl_stores_stock_data">
               <th>ID </th>
               <th>Description</th>
               <th>Quantity</th>
               <th>Comment</th>
               <th>Date Received</th>
               <th>Added By</th>
               <th>Date Added</th>
               <th>Edited By</th>
               <th>Date Edited</th>
               <th>Edit</th>
               """%('linkedsite.id')
        html2 = '' 
        for scope in receiving_items:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()
            #linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   #filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==scope.linkid).one()
            #contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
                   #one()

            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="80px" align='right'>%s</td>
                   <td width="180px">%s</td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                   </tr>
                   """%(scope.id,matlist.description,scope.qty,scope.comment,scope.date_received,
                           scope.useridnew,
                           scope.dateadded,
                           scope.useridedited,
                           scope.dateedited,
                           )
            html2 = html2 + htmltemp
        html3 = """
                   </table>
                """
        return html0 + html + html2 + html3

    @expose()
    def get_stores_stock_despatch_html(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        formupdate3 = '' 
        formupdate3 = """
                      <label for="%s">%s</label>
                      <select id="select_mat_dropdown_despatch" name="select_mat_dropdown_despatch" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("select_mat_dropdown_despatch","Select To View Despatched Material ")
        for scope in matlistall:
            formupdate3temp = """

                            <option value="%s">%s</option>

                              """%(scope.id,scope.description)
            formupdate3 = formupdate3 + formupdate3temp 

        formupdate3 = formupdate3 + "</select>"
        html3 = """
                """
        return formupdate3 + html3

    @expose()
    def get_stores_despatch_data(self,**kw):
        matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == kw['listid']). \
                one()
        requirement_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                all()
        despatched_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.matlistid == matlist.id). \
                all()
        requirement_items_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeSiteRequirements.qty))
        requirement_received_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresReceiveList). \
                filter(JistEstimating3yrEssPalisadeStoresReceiveList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresReceiveList.qty))
        despatched_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresDespatchList.qty))
        if requirement_items_total:
            req_total = requirement_items_total
        else:
            req_total = 0
        if requirement_received_total:
            receive_total = requirement_received_total
        else:
            receive_total = 0
        if despatched_total:
            despatch_total = despatched_total
        else:
            despatch_total = 0
        stocknow = receive_total - despatch_total
        futurestock = receive_total - req_total 

        html0 = """
                <table>
                <th colspan=2>Store Totals: %s</th>
                <tr>
                <td width="280px">Total Stores Received:</td>
                <td width="80px" align="right" >%s</td></tr><tr>
                <td>Total Stores Despatch:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Stock Now:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Booked:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Future Stock:</td>
                <td align="right">%s</td></tr>
                </tr></table>
                   
                """%(matlist.description,receive_total,despatch_total,stocknow,req_total,futurestock)
        html = """
                <p/>
               <h3 class="ui-widget-shadow">SPF Despatched Items 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
               <table id="tbl_stores_stock_data">
               <th>ID </th>
               <th>JCNo </th>
               <th>Description</th>
               <th>Quantity</th>
               <th>Despatch To</th>
               <th>Date Despatched</th>
               <th>Comment </th>
               <th>Added By</th>
               <th>Date Added</th>
               <th>Edited By</th>
               <th>Date Edited</th>
               <th>Edit</th>
               """%('linkedsite.id')
        html2 = '' 
        for scope in despatched_items:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()
            #linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   #filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==scope.linkid).one()
            #contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
                   #one()

            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="80px" align='right'>%s</td>
                   <td width="80px">%s</td>
                   <td width="180px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                   </tr>

                   """%(scope.id,scope.jcno,matlist.description,scope.qty,scope.despatch_to,scope.date_despatch,scope.comment,
                           scope.useridnew,
                           scope.dateadded,
                           scope.useridedited,
                           scope.dateedited,
                           )
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html0 + html + html2 + html3

    @expose()
    def get_stores_despatch_form(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        html1 = """
                    <form id="stores_despatch_form">
                    <fieldset>
                        <!--label for="stores_despatchid">ID</label><br/>
                        <input type="text" name="stores_despatchid" id="stores_despatchid" class="text ui-widget-content ui-corner-all" /><br/-->
                        <label for="select_mat_dropdown">Choose and Item To Despatch</label><br/>
                      <select id="select_mat_dropdown" name="select_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        html2 = ''
        for mat in matlistall:
            html2temp = """
                                   <option value="%s" >%s</option>
                        """%(mat.id,mat.description)
            html2 = html2 + html2temp

        html3 = """
                        </select><br/>
                        <label for="select_mat_dropdown_jcno">Choose A JCNo To Return From</label><br/>
                      <select id="select_mat_dropdown_jcno" name="select_mat_dropdown_jcno" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        html4 = ''
        for mat in contracts:
            html4temp = """
                                   <option value="%s" >%s</option>
                        """%(mat.jno,str(mat.jno) + "-" + mat.site)
            html4 = html4 + html4temp


        html5 = """
                        </select><br/>
                        <label for="stores_despatchqty">Qty</label><br/>
                        <input type="text" name="stores_despatchqty" id="stores_despatchqty" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_despatch_to">Despatched To Person/Place</label><br/>
                        <input type="text" name="stores_despatch_to" id="stores_despatch_to" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_despatch_date">Date Despatched</label><br/>
                        <input type="text" name="stores_despatch_date" id="stores_despatch_date" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_despatch_comment">Comment</label><br/>
                        <input type="text" name="stores_despatch_comment" id="stores_despatch_comment" class="text ui-widget-content ui-corner-all" /><br/>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_new_mat_despatch">Save New Despatch Note</button> 
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_cancel_mat_despatch">Cancel</button> 
                
                    </fieldset>
                    </form>
            """
        return html1 + html2 + html3 + html4 + html5

    @expose()
    def ajaxAddNewStoresDespatch(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeStoresDespatchList(
                                      matlistid=kw['select_mat_dropdown'],
                                      jcno=kw['select_mat_dropdown_jcno'],
                                      qty=kw['stores_despatchqty'],
                                      despatch_to=kw['stores_despatch_to'],
                                      comment=kw['stores_despatch_comment'],
                                      date_despatch=kw['stores_despatch_date'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return

    @expose()
    def get_stores_stock_return_html(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        formupdate3 = '' 
        formupdate3 = """
                      <label for="%s">%s</label>
                      <select id="select_mat_dropdown_return" name="select_mat_dropdown_return" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("select_mat_dropdown_return","Select To View Returned Material ")
        for scope in matlistall:
            formupdate3temp = """

                            <option value="%s">%s</option>

                              """%(scope.id,scope.description)
            formupdate3 = formupdate3 + formupdate3temp 

        formupdate3 = formupdate3 + "</select>"
        html3 = """
                """
        return formupdate3 + html3

    @expose()
    def get_stores_return_data(self,**kw):
        matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == kw['listid']). \
                one()
        requirement_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                all()
        despatched_items = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.matlistid == matlist.id). \
                all()
        requirement_items_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeSiteRequirements). \
                filter(JistEstimating3yrEssPalisadeSiteRequirements.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeSiteRequirements.qty))
        requirement_received_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresReceiveList). \
                filter(JistEstimating3yrEssPalisadeStoresReceiveList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresReceiveList.qty))
        despatched_total = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStoresDespatchList). \
                filter(JistEstimating3yrEssPalisadeStoresDespatchList.matlistid == matlist.id). \
                value(func.sum(JistEstimating3yrEssPalisadeStoresDespatchList.qty))
        if requirement_items_total:
            req_total = requirement_items_total
        else:
            req_total = 0
        if requirement_received_total:
            receive_total = requirement_received_total
        else:
            receive_total = 0
        if despatched_total:
            despatch_total = despatched_total
        else:
            despatch_total = 0
        stocknow = receive_total - despatch_total
        futurestock = receive_total - req_total 
        html0 = """
                <table>
                <th colspan=2>Store Totals: %s</th>
                <tr>
                <td width="280px">Total Stores Received:</td>
                <td width="80px" align="right" >%s</td></tr><tr>
                <td>Total Stores Despatch:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Stock Now:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Booked:</td>
                <td align="right">%s</td></tr><tr>
                <td>Total Future Stock:</td>
                <td align="right">%s</td></tr>
                </tr></table>
                   
                """%(matlist.description,receive_total,despatch_total,stocknow,req_total,futurestock)
        html = """
                <p/>
               <h3 class="ui-widget-shadow">SPF Returned Items 
               <span style="float:right"></span>
                    <!--a href="/est3yresspalisadecont/export_site_requirements_pdf?linkid=%s">
                    <img id="export_excel_est" src="/images/pdficon.jpg" align="right"></img>
                    </a-->
               </h3>
               <table id="tbl_stores_stock_data">
               <th>ID </th>
               <th>JCNo </th>
               <th>Description</th>
               <th>Quantity</th>
               <th>Despatch To</th>
               <th>Date Despatched</th>
               <th>Comment </th>
               <th>Added By</th>
               <th>Date Added</th>
               <th>Edited By</th>
               <th>Date Edited</th>
               <th>Edit</th>
               """%('linkedsite.id')
        html2 = '' 
        for scope in despatched_items:
            matlist = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                    filter(JistEstimating3yrEssPalisadeStandardMaterialList.id == scope.matlistid). \
                    one()
            #linkedsite = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeJCNOEstLink). \
                   #filter(JistEstimating3yrEssPalisadeJCNOEstLink.id==scope.linkid).one()
            #contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==linkedsite.jcnoid). \
                   #one()

            htmltemp = """
                   <tr>
                   <td>%s</td>
                   <td>%s</td>
                   <td>%s</td>
                   <td >%s</td>
                   <td width="80px" align='right'>%s</td>
                   <td width="80px">%s</td>
                   <td width="180px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td  align="left" >
                    <img src="/images/staffpics/%s.png"
                        align="center"/>
                    </td>
                   <td width="80px">%s</td>
                    <td width="25px" ><img  id="edit_scopeitem" src="/images/Edit-16.png"></img></td>
                   </tr>

                   """%(scope.id,scope.jcno,matlist.description,scope.qty,scope.despatch_to,scope.date_despatch,scope.comment,
                           scope.useridnew,
                           scope.dateadded,
                           scope.useridedited,
                           scope.dateedited,
                           )
            html2 = html2 + htmltemp
        html3 = """

                   </table>
                """
        return html0 + html + html2 + html3

    @expose()
    def get_stores_return_form(self,**kw):
        matlistall = DBS_Jist3yrEssPalisade.query(JistEstimating3yrEssPalisadeStandardMaterialList). \
                all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        html1 = """
                    <form id="stores_return_form">
                    <fieldset>
                        <!--label for="stores_returnid">ID</label><br/>
                        <input type="text" name="stores_returnid" id="stores_returnid" class="text ui-widget-content ui-corner-all" /><br/-->
                        <label for="select_mat_dropdown">Choose An Item To Return</label><br/>
                      <select id="select_mat_dropdown" name="select_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        html2 = ''
        for mat in matlistall:
            html2temp = """
                                   <option value="%s" >%s</option>
                        """%(mat.id,mat.description)
            html2 = html2 + html2temp

        html3 = """
                        </select><br/>
                        <label for="select_mat_dropdown_jcno">Choose A JCNo To Despatch To</label><br/>
                      <select id="select_mat_dropdown_jcno" name="select_mat_dropdown_jcno" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        html4 = ''
        for mat in contracts:
            html4temp = """
                                   <option value="%s" >%s</option>
                        """%(mat.jno,str(mat.jno) + "-" + mat.site)
            html4 = html4 + html4temp


        html5 = """
                        </select><br/>
                        <label for="stores_returnqty">Qty</label><br/>
                        <input type="text" name="stores_returnqty" id="stores_returnqty" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_return_to">returned To Person/Place</label><br/>
                        <input type="text" name="stores_return_to" id="stores_return_to" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_return_date">Date returned</label><br/>
                        <input type="text" name="stores_return_date" id="stores_return_date" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="stores_return_comment">Comment</label><br/>
                        <input type="text" name="stores_return_comment" id="stores_return_comment" class="text ui-widget-content ui-corner-all" /><br/>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_new_mat_return">Save New return Note</button> 
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_cancel_mat_return">Cancel</button> 
                    </fieldset>
                    </form>
            """
        return html1 + html2 + html3 + html4 + html5

    @expose()
    def ajaxAddNewStoresReturn(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistEstimating3yrEssPalisadeStoresReturnList(
                                      matlistid=kw['select_mat_dropdown'],
                                      jcno=kw['select_mat_dropdown_jcno'],
                                      qty=kw['stores_returnqty'],
                                      return_by=kw['stores_return_to'],
                                      comment=kw['stores_return_comment'],
                                      date_returned=kw['stores_return_date'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_Jist3yrEssPalisade.add(newscopes)
        DBS_Jist3yrEssPalisade.flush()
        return



def isnumeric(value):
    return str(value).replace(".", "").replace("-", "").isdigit()


