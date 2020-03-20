# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
from tg.decorators import paginate

from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 
from jistdocstore.model import DBS_JistInvoicing, metadata7
from jistdocstore.model import JistInvoicesList 
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
import locale
from decimal import Decimal
from datetime import datetime, time, date
import calendar

public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
current_purchase_req_id = 0 
current_purchase_order_id = 0 
current_purchase_order_items = [] 
from babel.numbers import format_currency, format_number, format_decimal
VAT_RATE = 0.14        
__all__ = ['InvoicingController']


class InvoicingController(BaseController):
    """Sample controller-wide authorization"""
    
    #The predicate that must be met for all the actions in this controller:
    allow_only = has_any_permission('manage','administrationmanage','accountsmanage', msg=l_('Only for people with the "manage" permission'))

    def __init__(self):
        self.ListCIDBCategories = ['None','GB', 'SQ', 'CE', 'ME']
        self.ListTrueFalse = ['False','True']
        self.ListWorkCategory = ['Fencing - Normal','Fencing - High Security',
                                'Building','Maintenance','Carports',
                                'Manufacturing','CCTV','Supply Only',
                                'Administrative','Software','Network Support' 
                                ]

    @expose()
    def index(self):
        redirect('invoicingcont/menu')

    @expose('jistdocstore.templates.invoicing.accountsindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Accounts: Main Menu') 

    @expose('jistdocstore.templates.invoicing.production_invoicingconsole')
    def production_invoicing_console(self,**named):
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invclients = DBS_JistInvoicing.query(func.distinct(JistInvoicesList.client))
        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                order_by(desc(JistContracts.jno)). \
                all()
        #for inv in invoices:
        #    for col in inv.__table__._columns:
        #        print col
        #return
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
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
        return dict(page='Production Invoicing Console',
                    invoices = invoices,
                    clientlist = invclients,
                    points = pointlist,
                    wip = wip,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.invoicing.invoicingconsole')
    def invoicing_console(self,**named):
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invclients = DBS_JistInvoicing.query(func.distinct(JistInvoicesList.client))
                     
        return dict(page='Invoicing Console',
                    invoices = invoices,
                    clientlist = invclients,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.accounts.payreqconsole')
    def payreq_console(self,**named):
        return dict(page='Payment Requisition Console',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.management.financialconsole')
    def financial_console(self,**named):
        return dict(page='Financial Console',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def do_search_invoices_dates(self, **kw):
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
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     value(func.sum(JistInvoicesList.value_incl))
        locale.setlocale(locale.LC_ALL, '')

        if invoices_total is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        invoice_text = "<H3 align='left'> Invoices For Period From: %s To  %s</H3><p/>"%(datestart,dateend)
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalincl)
            pdf2 = """
                        <a
                        href='/invoicingcont/export_invoice_dates_pdf/%s/%s'><p/> 
                        <img src="/images/pdficon.jpg"></img></a>
                   """%(startdate,enddate)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf2+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalincl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf3

        sitedata = "<div class='div_tableinvlist'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Invoice Number </th>
                    <th>Invoice Date</th>
                    <th>Client</th>
                    <th>Total Incl</th>
                    <th>JCNo</th>
                    <th>Site Name</th>
                    <th>Point Person</th>
                    """
        sitedata = invoice_text +pdfstuff+sitedata + headerdata
        for k in invoices:
            totalincl = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/invoicingcont/invoice_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.invoiceno,
                                    k.invdate,
                                    k.client,
                                    totalincl,
                                    k.contract,
                                    contract.site,
                                    str(user_name), 
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def export_invoice_dates_pdf(self,startdate,enddate):
        import random
        #for k, w in kw.iteritems():
        #    print k, w
        #print datestart, dateend
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     value(func.sum(JistInvoicesList.value_incl))
        if invoices_total_excl is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
        payments_total = 0
        for p in invoices:
            invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                          filter(JistInvoicesPayments.invoiceid==p.id). \
                         all()
            if invoice_payments:
                for r in invoice_payments:
                    payments_total = payments_total + r.amount
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            totalincl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            wip1.append({'invnumber':k.invoiceno,
                          'invdate':k.invdate,
                         'client':k.client,
                         'totalincl':totalincl,
                         'jno':contract.jno,
                         'sitename':contract.site,
                         'pointperson':user_name,
                         })
        count = len(wip1) 
        outinvoices_total = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Invoices From %s To %s"%(startdate,enddate),
                        ""
                        ])
        headers =["Inv No","Date","Client","Total Incl","JCNo","Site Name","Point Person"]
        headerwidths=[70,70,120,70,70,100,100]
        pdffile.CreatePDFInvoicesTime(userdata,wip1,headers,headerwidths,outinvoices_total)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def do_search_invoices_clients_dates(self, **kw):
        #for k, w in kw.iteritems():
        #    print k, w
        if not kw['clientstartdate']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                if k == "clientstartdate":
                    year =w.split('-')[0]
                    month =w.split('-')[1]
                    day =w.split('-')[2]
        if not kw['clientenddate']:
            endyear = str(0)
        else :
            for k,w in kw.iteritems():
                if k == "clientenddate":
                    endyear =w.split('-')[0]
                    endmonth =w.split('-')[1]
                    endday =w.split('-')[2]

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
        clientstartdate = datetime.combine(today,sttimestart)
        clientenddate = datetime.combine(endtoday,sttimeend)
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==kw['clientname']). \
                      filter(JistInvoicesList.invdate>=clientstartdate). \
                      filter(JistInvoicesList.invdate<=clientenddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==kw['clientname']). \
                      filter(JistInvoicesList.invdate>=clientstartdate). \
                      filter(JistInvoicesList.invdate<=clientenddate). \
                     value(func.sum(JistInvoicesList.value_incl))

        locale.setlocale(locale.LC_ALL, '')
        if invoices_total is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        invoice_text = """<H3 align='left'> 
                            Invoices for period from: %s to  %s for %s
                            </H3><p/>
                            """%(datestart,dateend,kw['clientname'])
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalincl)
            pdf2 = """
                        <a
                        href='/invoicingcont/export_invoice_clients_dates_pdf/%s/%s/%s'><p/> 
                        <img src="/images/pdficon.jpg"></img></a>
                   """%(clientstartdate,clientenddate,kw['clientname'])
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf2+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalincl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf3

        sitedata = "<div class='div_tableinvlist'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Invoice Number </th>
                    <th>Invoice Date</th>
                    <th>Client</th>
                    <th>Total Incl</th>
                    <th>JCNo</th>
                    <th>Site Name</th>
                    <th>Point Person</th>
                    """
        sitedata = invoice_text +pdfstuff+sitedata + headerdata
        for k in invoices:
            totalincl = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/invoicingcont/invoice_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.invoiceno,
                                    k.invdate,
                                    k.client,
                                    totalincl,
                                    k.contract,
                                    contract.site,
                                    str(user_name), 
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def do_search_invoices_clients_only(self, **kw):
        #for k, w in kw.iteritems():
        #    print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==kw['clientname']). \
                     order_by(desc(JistInvoicesList.id)). \
                     limit(20)
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==kw['clientname']). \
                     value(func.sum(JistInvoicesList.value_incl))


        sitedata ="""<label for=''>Use Invoice Details Below With Order Number Above</label><br/>
                  <select id='oldinvoiceselected'>
                  """
        sitedata = sitedata 
        for k in invoices:
            totalincl = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            try:
                point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
                user_name = point.user_name
            except:
                point = DBS_ContractData.query(User).filter(User.user_id==1).one()
                user_name = point.user_name
            sitedatatemp = """
                            <option value = '%s'>%s-%s-%s-%s</option>
                            """ % (k.id,k.invoiceno,
                                    k.invdate,
                                    k.client,
                                    totalincl,
                                   )
            sitedata = sitedata + sitedatatemp
        sitedata = sitedata +"</select>"
        return sitedata+"</div>" 

    @expose()
    def get_invoice_client_info(self, **kw):
        try:
            invoice = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.id==kw['invid']). \
                          one()
            invclient = DBS_JistInvoicing.query(JistInvoicesClients). \
                          filter(JistInvoicesClients.invoiceid==kw['invid']). \
                          one()
            contract = DBS_ContractData.query(JistContracts).get(kw['contractid'])
        except:
            return
        clientdata = """        
            <div id="inv_client_details_div" style="display: none">
                <form id = "inv_client_details_form">
                 <fieldset>
                <label for="">Invoice Date</label>
                <input type="text" value="%s" name="inv_date" id="inv_date" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Client Name</label>
                <input type="text" value="%s" name="inv_client_name" id="inv_client_name" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Order Number: </label>
                <input type="text" value="%s" name="order_number" id="order_number" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Our JCNo: </label>
                <input type="text" value="%s" name="jcno" id="jcno" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Address Line1</label>
                <input type="text" value="%s" name="address_line1" id="address_line1" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Address Line2</label>
                <input type="text" value="%s" name="address_line2" id="address_line2" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Address Line3</label>
                <input type="text" value="%s" name="address_line3" id="address_line3" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">VAT Number: </label>
                <input type="text" value="%s" name="vat_number" id="vat_number" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Name</label>
                <input type="text" value="%s" name="delvToname" id="delvToname" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Address Line 1</label>
                <input type="text" value="%s" name="delvToadd1" id="delvToadd1" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Address Line 2</label>
                <input type="text" value="%s" name="delvToadd2" id="delvToadd2" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Contact Person</label>
                <input type="text" value="%s" name="delvTocontperson" id="delvTocontperson" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Contact Tel</label>
                <input type="text" value="%s" name="delvToconttel" id="delvToconttel" class="text ui-widget-content ui-corner-all"/><br/>
                <button id="button_new_invoice_old_info" >Use This Info To Create A New Invoice</button>
                </fieldset>
                </form>
            </div>
            """%(invoice.invdate,
                 invoice.client,
                 contract.orderno,
                 contract.jno,
                 invclient.add1, 
                 invclient.add2, 
                 invclient.add3, 
                 invclient.vatno, 
                 invclient.delvToname, 
                 invclient.delvToadd1, 
                 invclient.delvToadd2, 
                 invclient.delvTocontperson, 
                 invclient.delvToconttel, 
                 )
        return clientdata

    @expose()
    def get_invoice_client_edit_info(self, **kw):
        try:
            invoice = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.id==kw['invid']). \
                          one()
            invclient = DBS_JistInvoicing.query(JistInvoicesClients). \
                          filter(JistInvoicesClients.invoiceid==kw['invid']). \
                          one()
            contract = DBS_ContractData.query(JistContracts).get(invoice.contract)
        except:
            return
        clientdata = """        
            <div id="inv_client_details_edit" style="display: block">
                <form id = "inv_client_details_form_edit">
                 <fieldset>
                <label for="">Invoice Date</label>
                <input type="text" value="%s" name="inv_date_edit"
                id="inv_date_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Client Name</label>
                <input type="text" value="%s" name="inv_client_name_edit"
                id="inv_client_name_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Order Number: </label>
                <input type="text" value="%s" name="order_number_edit"
                id="order_number_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Our JCNo: </label>
                <input type="text" value="%s" name="jcno_edit"
                id="jcno_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Address Line1</label>
                <input type="text" value="%s" name="address_line1_edit"
                id="address_line1_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Address Line2</label>
                <input type="text" value="%s" name="address_line2_edit"
                id="address_line2_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Address Line3</label>
                <input type="text" value="%s" name="address_line3_edit"
                id="address_line3_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">VAT Number: </label>
                <input type="text" value="%s" name="vat_number_edit"
                id="vat_number_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Name</label>
                <input type="text" value="%s" name="delvToname_edit"
                id="delvToname_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Address Line 1</label>
                <input type="text" value="%s" name="delvToadd1_edit"
                id="delvToadd1_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Address Line 2</label>
                <input type="text" value="%s" name="delvToadd2_edit"
                id="delvToadd2_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Contact Person</label>
                <input type="text" value="%s" name="delvTocontperson_edit"
                id="delvTocontperson_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <label for="">Del To: Contact Tel</label>
                <input type="text" value="%s" name="delvToconttel_edit"
                id="delvToconttel_edit" class="text ui-widget-content ui-corner-all"/><br/>
                <button id="button_edit_client_data_edit" >Edit Invoice Client Data</button>
                </fieldset>
                </form>
            </div>
            """%(invoice.invdate,
                 invoice.client,
                 invoice.ordernumber,
                 contract.jno,
                 invclient.add1, 
                 invclient.add2, 
                 invclient.add3, 
                 invclient.vatno, 
                 invclient.delvToname, 
                 invclient.delvToadd1, 
                 invclient.delvToadd2, 
                 invclient.delvTocontperson, 
                 invclient.delvToconttel, 
                 )
        return clientdata

    @expose()
    def export_invoice_clients_dates_pdf(self,startdate,enddate,clientname):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==clientname). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==clientname). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     value(func.sum(JistInvoicesList.value_incl))
        if invoices_total_excl is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
        payments_total = 0
        for p in invoices:
            invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                          filter(JistInvoicesPayments.invoiceid==p.id). \
                         all()
            #print invoice_payments[0].id
            if invoice_payments:
                for r in invoice_payments:
                    payments_total = payments_total + r.amount
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            totalexcl = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            wip1.append({'invnumber':k.invoiceno,
                          'invdate':k.invdate,
                         'client':k.client,
                         'totalexcl':totalexcl,
                         'jno':contract.jno,
                         'sitename':contract.site,
                         'pointperson':user_name,
                         })
        count = len(wip1) 
        #outbalance_total = format_decimal(totalbal,format='#,##0.00;-#0.00',locale='en')
        #outpayments_total= format_decimal(payments_total,format='#,##0.00;-#0.00',locale='en')
        outinvoices_total = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Invoices For Client: %s from %s to %s"%(clientname,startdate,enddate),
                        ""
                        ])
        headers =["Inv No","Date","Client","Total Incl","JCNo","Site Name","Point Person"]
        headerwidths=[70,70,120,70,70,100,100]
        pdffile.CreatePDFInvoicesClientsTime(userdata,wip1,headers,headerwidths,outinvoices_total)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def do_search_invoices_contracts(self, **kw):
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==kw['contract_name']). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==kw['contract_name']). \
                     value(func.sum(JistInvoicesList.value_excl))

        contract = DBS_ContractData.query(JistContracts).get(kw['contract_name'])
        locale.setlocale(locale.LC_ALL, '')
        #print invoices_total
        #return
        if invoices_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        #datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        #dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        invoice_text = """<H3 align='left'> 
                            Invoices for contract: %s - %s - %s - %s 
                            </H3><p/>
                            """%(contract.jno,contract.client,contract.site,contract.description)
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/invoicingcont/export_invoice_contracts_pdf/%s'><p/> 
                        <img src="/images/pdficon.jpg"></img></a>
                   """%(kw['contract_name'])
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf2+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf3

        sitedata = "<div class='div_tableinvlist'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Invoice Number </th>
                    <th>Invoice Date</th>
                    <th>Client</th>
                    <th>Total Excl</th>
                    <th>JCNo</th>
                    <th>Site Name</th>
                    <th>Point Person</th>
                    """
        sitedata = invoice_text +pdfstuff+sitedata + headerdata
        for k in invoices:
            totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/invoicingcont/invoice_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.invoiceno,
                                    k.invdate,
                                    k.client,
                                    totalexcl,
                                    k.contract,
                                    contract.site,
                                    str(user_name), 
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def export_invoice_contracts_pdf(self,jno):
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
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==jno). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total_incl = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==jno). \
                     value(func.sum(JistInvoicesList.value_excl))

        contract = DBS_ContractData.query(JistContracts).get(jno)
        if invoices_total_incl is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        #datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        #dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            wip1.append({'invnumber':k.invoiceno,
                          'invdate':k.invdate,
                          'client':k.client,
                          'totalexcl':k.value_excl,
                         })
        count = len(wip1) 
        outinvoices_total = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Invoices For Contract: %s - %s - %s - %s"%(contract.jno,contract.client,contract.site,contract.description),
                        ])
        headers =["Inv No","Inv Date","Client","Total Excl"]
        headerwidths=[70,70,100,70]
        pdffile.CreatePDFInvoicesContract(userdata,wip1,headers,headerwidths,outinvoices_total)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def do_search_invoices_payment_time(self, **kw):
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
        payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.paymentdate>=startdate). \
                     filter(JistInvoicesPayments.paymentdate<=enddate). \
                     order_by(desc(JistInvoicesPayments.invoiceid)). \
                     all()
        payments_total = DBS_JistInvoicing.query(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.paymentdate>=startdate). \
                     filter(JistInvoicesPayments.paymentdate<=enddate). \
                     value(func.sum(JistInvoicesPayments.amount))

        #contract = DBS_ContractData.query(JistContracts).get(kw['contract_name'])
        locale.setlocale(locale.LC_ALL, '')
        if payments_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(payments_total,format='#,##0.00;-#0.00',locale='en')
        invoice_text = """<H3 align='left'> 
                            Invoice Payments for period: %s to %s 
                            </H3><p/>
                            """%(startdate,enddate)
        if payments_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/invoicingcont/export_invoice_payment_time_pdf/%s/%s'> 
                        <img src="/images/pdficon.jpg"></img></a>
                   """%(startdate,enddate)
            pdf3 = """
                        </div>
                    """
            pdfstuff = pdf1+pdf2+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalexcl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf3

        sitedata = "<div class='div_tableinvlist'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Payment ID </th>
                    <th>Invoice Number </th>
                    <th>Payment Date</th>
                    <th>Total Incl</th>
                    """
        sitedata = invoice_text +pdfstuff+sitedata + headerdata
        for k in payments:
            totalexcl = format_decimal(k.amount,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/invoicingcont/invoice_payment_edit/%s'>%s
                            </a>
                            <td>
                            <a href='/invoicingcont/invoice_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.id,
                                    k.invoiceid,k.invoiceid,
                                    k.paymentdate,
                                    k.amount
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def do_search_invoices_unpaid(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     outerjoin(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.id == None). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                     outerjoin(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.id == None). \
                     value(func.sum(JistInvoicesList.value_incl))
        locale.setlocale(locale.LC_ALL, '')
        if invoices_total is None:
            totalexcl = 0.00
        else:
            #totalexcl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
            totalexcl = format_decimal(invoices_total, format='#,##0.00;-#0.00',locale='en')
        invoice_text = """<H3 align='left'> 
                            Invoice Payments for period: %s to %s 
                            </H3><p/>
                            """%('','')
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        <H3>Invoices Outstanding</H3><p/>
                        Total Incl Vat: <br/> R %s
                        <p/>
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/invoicingcont/export_invoices_unpaid'> 
                            <img src="/images/pdficon.jpg">
                            </img>
                        </a>
                   """
            pdf3 = """
                        </div>
                    """
            pdfstuff = pdf1+pdf2+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: R %s
                   """%(totalexcl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf3
        sitedata = "<div class='div_tableinvlist'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Invoice Number </th>
                    <th>Date </th>
                    <th>Client </th>
                    <th>Site</th>
                    <th>Point</th>
                    <th>Total Invoice</th>
                    <th>Sum of Payments</th>
                    <th>Balance</th>
                    """
        #sitedata = invoice_text +pdfstuff+sitedata + headerdata
        sitedata = pdfstuff+sitedata + headerdata
        for k in invoices:
            totalincl = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==contract.jno).one()
            status = {}
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            try:
                agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
                status = {'pointperson':statusall.pointperson,
                          'siteagent':statusall.siteagent}
            except:
                status = {'pointperson':1,
                          'siteagent':'1'}
            thisperson = DBS_ContractData.query(User).filter(User.user_id==status['pointperson']).one()
            payment_tot = DBS_JistInvoicing.query(JistInvoicesPayments). \
                         filter(JistInvoicesPayments.invoiceid==k.id). \
                         value(func.sum(JistInvoicesPayments.amount))
            if not payment_tot: payment_tot = 0
            #payment_total = format_decimal(payment_tot,format='#,##0.00;-#0.00',locale='en')
            payment_total = format_decimal(payment_tot, format='#,##0.00;-#0.00',locale='en')
            if not payment_total: payment_total = 0
            if not k.value_incl: k.value_incl = 0
            diff = Decimal(k.value_incl) - Decimal(str(payment_tot))
            #diffs = format_decimal(diff,format='#,##0.00;-#0.00',locale='en')
            diffs = format_decimal(diff, format='#,##0.00;-#0.00',locale='en')
            #print contract.site
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/invoicingcont/invoice_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            </tr>
                            """ % (k.id,k.id,
                                    k.invdate,
                                    k.client,
                                    contract.site,
                                    thisperson.user_name,
                                    totalincl,
                                    payment_total,
                                    diffs 
                                   )
            sitedata = sitedata + sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def export_invoices_unpaid(self):
        import random
        locale.setlocale(locale.LC_ALL, '')
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     outerjoin(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.id == None). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                     outerjoin(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.id == None). \
                     value(func.sum(JistInvoicesList.value_incl))

        if invoices_total is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            wip1.append({'invnumber':k.invoiceno,
                          'invdate':k.invdate,
                          'client':k.client,
                          'site':contract.site,
                          'totalexcl':format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
                         })
        count = len(wip1) 
        outinvoices_total = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Unpaid Invoices",
                        ])
        headers =["Inv No","Inv Date","Client","Site Name","Total Incl"]
        headerwidths=[70,70,200,200,70]
        pdffile.CreatePDFInvoicesUnpaid(userdata,wip1,headers,headerwidths,outinvoices_total)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def do_search_invoices_balances(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     join(JistInvoicesPayments). \
                     filter(JistInvoicesList.value_incl<>JistInvoicesPayments.amount). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                     join(JistInvoicesPayments). \
                     filter(JistInvoicesList.value_incl<>JistInvoicesPayments.amount). \
                     value(func.sum(JistInvoicesList.value_incl))
        payments_total = DBS_JistInvoicing.query(JistInvoicesList). \
                     join(JistInvoicesPayments). \
                     filter(JistInvoicesList.value_incl<>JistInvoicesPayments.amount). \
                     value(func.sum(JistInvoicesPayments.amount))
        locale.setlocale(locale.LC_ALL, '')
        if invoices_total is None:
            totalexcl = 0.00
        else:
            #totalexcl = format_decimal(invoices_total,grouping=True)
            totalexcl = format_decimal(invoices_total, format='#,##0.00;-#0.00',locale='en')
        if payments_total is None:
            totalpayments = 0.00
        else:
            #totalpayments = format_decimal(payments_total,grouping=True)
            totalpayments = format_decimal(payments_total, format='#,##0.00;-#0.00',locale='en')
        #print "Total Payments %s"%totalpayments
        invoice_text = """<H3 align='left'> 
                            Invoice Payments with Balances 
                            </H3><p/>
                            """
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        <H3>Invoices with Balances</H3><p/>
                        Total Incl Vat: <br/>R %s
                        <p/>
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/invoicingcont/export_invoices_balance'> 
                            <img src="/images/pdficon.jpg">
                            </img>
                        </a>
                   """
            pdf4 = """
                        Total Payments Incl Vat: <br/> R %s
                        <p/>
                   """%(totalpayments)
            pdf5 = """
                        </div>
                    """
            pdfstuff = pdf1+pdf4+pdf2+pdf5
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Incl Vat: <br/>R %s
                   """%(totalexcl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff = pdf1+pdf3

        sitedata = "<div class='div_tableinvlist'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Invoice Number </th>
                    <th>Date </th>
                    <th>Client </th>
                    <th>Site</th>
                    <th>Point</th>
                    <th>Total Invoice</th>
                    <th>Sum of Payments</th>
                    <th>Balance</th>
                    """
        #sitedata = invoice_text +pdfstuff+sitedata + headerdata
        sitedata = pdfstuff+sitedata + headerdata
        for k in invoices:
            #totalincl = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            totalincl = format_decimal(k.value_incl, format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==contract.jno).one()
            status = {}
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            try:
                agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
                status = {'pointperson':statusall.pointperson,
                          'siteagent':statusall.siteagent}
            except:
                status = {'pointperson':1,
                          'siteagent':'1'}
            #print status['pointperson'], contract.jno
            thisperson = DBS_ContractData.query(User).filter(User.user_id==status['pointperson']).one()
            payment_tot = DBS_JistInvoicing.query(JistInvoicesPayments). \
                         filter(JistInvoicesPayments.invoiceid==k.id). \
                         value(func.sum(JistInvoicesPayments.amount))
            #payment_total = format_decimal(payment_tot,format='#,##0.00;-#0.00',locale='en')
            payment_total = format_decimal(payment_tot, format='#,##0.00;-#0.00',locale='en')
            #print payment_tot
            if not payment_total: payment_total = 0
            if not k.value_incl: k.value_incl = 0
            diff = float(k.value_incl) - float(payment_tot)
            diffs = format_decimal(diff, format='#,##0.00;-#0.00',locale='en')
            #print diffs
            if diff <> 0: 
                sitedatatemp = """
                                <tr>
                                <td>
                                <a href='/invoicingcont/invoice_one/%s'>%s
                                </a>
                                </td>
                                <td>%s
                                </td>
                                <td>%s
                                </td>
                                <td>%s
                                </td>
                                <td>%s
                                </td>
                                <td align='right'>%s
                                </td>
                                <td align='right'>%s
                                </td>
                                <td align='right'>%s
                                </td>
                                </tr>
                                """ %(k.id,k.id,
                                        k.invdate,
                                        k.client,
                                        contract.site,
                                        thisperson.user_name,
                                        totalincl,
                                        payment_total,
                                        diffs,
                                       )
                #str(diffs), 
                sitedata = sitedata + sitedatatemp
        sitedata = sitedata +"</table></div>"
        #print sitedata
        return sitedata 

    @expose()
    def export_invoices_balance(self):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     join(JistInvoicesPayments). \
                     filter(JistInvoicesList.value_incl<>JistInvoicesPayments.amount). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                     join(JistInvoicesPayments). \
                     filter(JistInvoicesList.value_incl<>JistInvoicesPayments.amount). \
                     value(func.sum(JistInvoicesList.value_incl))
        payments_total = DBS_JistInvoicing.query(JistInvoicesList). \
                     join(JistInvoicesPayments). \
                     filter(JistInvoicesList.value_incl<>JistInvoicesPayments.amount). \
                     value(func.sum(JistInvoicesPayments.amount))
        if invoices_total is None:
            totalincl = 0.00
        else:
            #totalincl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
            totalincl = format_decimal(invoices_total, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            payment_tot = DBS_JistInvoicing.query(JistInvoicesPayments). \
                         filter(JistInvoicesPayments.invoiceid==k.id). \
                         value(func.sum(JistInvoicesPayments.amount))
            #payment_total = format_decimal(payment_tot,format='#,##0.00;-#0.00',locale='en')
            payment_total = format_decimal(payment_tot, format='#,##0.00;-#0.00',locale='en')
            if not payment_total: payment_total = 0
            if not k.value_incl: k.value_incl = 0
            diff = Decimal(k.value_incl) - Decimal(str(payment_tot))
            #diffs = format_decimal(diff,format='#,##0.00;-#0.00',locale='en')
            diffs = format_decimal(diff, format='#,##0.00;-#0.00',locale='en')
            invincl =format_decimal(k.value_incl, format='#,##0.00;-#0.00',locale='en')
            if diff <> 0: 
                wip1.append({'invnumber':k.invoiceno,
                              'invdate':k.invdate,
                              'client':k.client,
                              'site':contract.site,
                              'totalexcl':invincl,
                              'payment':payment_total,
                              'balance': diffs
                             })
        count = len(wip1) 
        outinvoices_total = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Invoices with Balances",
                        ])
        headers =["Inv No","Inv Date","Client","Site Name",
                  "Total Invoice","Payment Total","Balance"]
        headerwidths=[70,70,200,200,70,70,70]
        pdffile.CreatePDFInvoicesBalances(userdata,wip1,headers,headerwidths,outinvoices_total)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_invoice_payment_time_pdf(self,startdate,enddate):
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
        payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.paymentdate>=startdate). \
                     filter(JistInvoicesPayments.paymentdate<=enddate). \
                     order_by(desc(JistInvoicesPayments.invoiceid)). \
                     all()
        payments_total = DBS_JistInvoicing.query(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.paymentdate>=startdate). \
                     filter(JistInvoicesPayments.paymentdate<=enddate). \
                     value(func.sum(JistInvoicesPayments.amount))

        #contract = DBS_ContractData.query(JistContracts).get(kw['contract_name'])
        #            payments_total = payments_total + r.amount
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in payments:
            wip1.append({'payid':k.id,
                          'invnumber':k.invoiceid,
                          'invdate':k.paymentdate,
                         'totalincl':k.amount,
                         })
        count = len(wip1) 
        outpayments_total = format_decimal(payments_total,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Invoices vs Payments From: %s to %s"%(startdate,enddate),
                        ""
                        ])
        headers =["Payment ID","Inv No","Payment Date","Total Incl"]
        headerwidths=[80,70,70,70]
        pdffile.CreatePDFInvoicesPaymentTime(userdata,wip1,headers,headerwidths,outpayments_total)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def do_search_invoices_vs_payment_time(self, **kw):
        if not kw['startdate']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                if k == "startdate":
                    #print k,w
                    #rqdate = w.split('-')
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
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total_incl = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     value(func.sum(JistInvoicesList.value_incl))
        payments_total = 0
        for p in invoices:
            invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                          filter(JistInvoicesPayments.invoiceid==p.id). \
                         all()
            #print invoice_payments[0].id
            if invoice_payments:
                for r in invoice_payments:
                    payments_total = payments_total + r.amount
                    #print r.amount

        locale.setlocale(locale.LC_ALL, '')
        if invoices_total_incl is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        totalamount = 0
        #payments_total = 0
        invoice_text1 = "<H3 align='left'> Invoices vs Payments for period from %s to  %s</H3>"%(datestart,dateend)
        if invoices_total_incl:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Invoices Incl: \n R %s
                   """%(totalincl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff1 = pdf1+pdf3
        else:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Invoices Incl: \n R %s
                   """%(totalincl)
            pdf3 = """
                        </div>
                        <p/>
                    """
            pdfstuff1 = pdf1+pdf3

        if payments_total is None:
            totalpayments = 0.00
        else:
            totalpayments = format_decimal(payments_total,format='#,##0.00;-#0.00',locale='en')
        #if payments_total:
        pdf1 = """<div class=sidebar_total_excl>
                    Total Payments Incl: \n R %s
               """%(totalpayments)
        pdf2 = """
                    <a
                    href='/invoicingcont/export_invoice_vs_payments_pdf/%s/%s'><p/> 
                    <img src="/images/pdficon.jpg"></img></a>
               """%(startdate,enddate)
        pdf3 = """
                    </div>
                """
        pdfstuff = pdfstuff1+pdf1+pdf2+pdf3
        #else:
        #    pdf1 = """<div class=sidebar_total_excl>
        #                Total Payments Incl: \n  R %s
        #           """%(totalpayments)
        #    pdf3 = """
        #                </div>
        #            """
        #    pdfstuff = pdfstuff1+pdf1+pdf3
        
        sitedata = "<div class='div_tableinvvspay'><table class='tableinvoicelist'>"
        headerdata = """
                    <th>Inv Number </th>
                    <th>Inv Date </th>
                    <th>Client </th>
                    <th>Total Incl</th>
                    <th>Site Name</th>
                    <th>Point Person</th>
                    <th>Payment Date</th>
                    <th>Payment Amount</th>
                    <th>Balance Incl</th>
                    """
        sitedata = invoice_text1+pdfstuff+sitedata + headerdata
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            totalin = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                          filter(JistInvoicesPayments.invoiceid==k.id). \
                          all()
            pdate = ""
            pmount = 0
            pamount = 0
            balance = 0
            bal = 0
            for p in invoice_payments:
                #print p.paymentdate, p.amount
                pdate = pdate + str(p.paymentdate)
                pmount = pmount + p.amount
            pamount = format_decimal(pmount,format='#,##0.00;-#0.00',locale='en')
            bal = k.value_incl - pmount
            totalbal = totalbal + bal
            balance = format_decimal(bal,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/invoicingcont/invoice_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.invoiceno,
                                    k.invdate,
                                    k.client,
                                    totalin,
                                    contract.site,
                                    str(user_name), 
                                    pdate,
                                    pamount,
                                    balance 
                                   )
            totalbalance = format_decimal(totalbal,format='#,##0.00;-#0.00',locale='en')
            pdf5 = """<div class=sidebar_balance_outstanding>
                        Total Balance Outstanding Incl: \n R %s
                   """%(totalbalance)
            pdf6 = """
                        </div>
                        <p/>
                    """
            pdfstuff4 = pdf5+pdf6
            sitedata = sitedata + sitedatatemp 
        sitedata = sitedata +"</table></div>" + pdfstuff4
        return sitedata 

    @expose()
    def export_invoice_vs_payments_pdf(self,startdate,enddate):
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
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total_incl = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     value(func.sum(JistInvoicesList.value_incl))
        if invoices_total_incl is None:
            totalincl = 0.00
        else:
            totalincl = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        payments_total = 0
        for p in invoices:
            invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                          filter(JistInvoicesPayments.invoiceid==p.id). \
                         all()
            #print invoice_payments[0].id
            if invoice_payments:
                for r in invoice_payments:
                    payments_total = payments_total + r.amount
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in invoices:
            totalin = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                          filter(JistInvoicesPayments.invoiceid==k.id). \
                          all()
            pdate = ""
            pmount = 0
            pamount = 0
            balance = 0
            bal = 0
            for p in invoice_payments:
                #print p.paymentdate, p.amount
                pdate = pdate + str(p.paymentdate)
                pmount = pmount + p.amount
            pamount = format_decimal(pmount,format='#,##0.00;-#0.00',locale='en')
            bal = k.value_incl - pmount
            totalbal = totalbal + bal
            inbalance = format_decimal(bal,format='#,##0.00;-#0.00',locale='en')
            wip1.append({'invnumber':k.invoiceno,
                          'invdate':k.invdate,
                         'client':k.client,
                         'totalincl':totalin,
                         'sitename':contract.site,
                         'pointperson':user_name,
                         'paydate':pdate,
                         'payamount':pamount,
                         'balance':inbalance,
                         })
        count = len(wip1) 
        outbalance_total = format_decimal(totalbal,format='#,##0.00;-#0.00',locale='en')
        outpayments_total= format_decimal(payments_total,format='#,##0.00;-#0.00',locale='en')
        outinvoices_total = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Invoices vs Payments From: %s to %s"%(startdate,enddate),
                        ""
                        ])
        headers =["Inv No","Date","Client","Total Incl","Site Name","Point Person","Payment Date","Amount Paid","Balance"]
        headerwidths=[70,70,120,70,150,80,70,70,70]
        pdffile.CreatePDFInvoicesVSPayment(userdata,wip1,headers,headerwidths,outinvoices_total,outpayments_total,outbalance_total)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def savenewinvoice(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return '100'
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        if not kw['invdate']:
            return
        if not kw['client']:
            return
        new_inv = JistInvoicesList()
        new_inv.invdate = kw['invdate']
        new_inv.ordernumber = kw['ordernumber']
        new_inv.client = kw['client']
        new_inv.contract = kw['contract']
        DBS_JistInvoicing.add(new_inv)
        DBS_JistInvoicing.flush()
        new_inv.invoiceno = new_inv.id
        return str(new_inv.id)

    @expose()
    def savenewinvoice_clientdata(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_inv = JistInvoicesClients()
        new_inv.invoiceid = kw['invoiceid'] 
        new_inv.add1 = kw['add1'] 
        new_inv.add2 = kw['add2'] 
        new_inv.add3 = kw['add3'] 
        new_inv.vatno = kw['vatno'] 
        new_inv.delvToname = kw['delvToname'] 
        new_inv.delvToadd1 = kw['delvToadd1'] 
        new_inv.delvToadd2 = kw['delvToadd2'] 
        new_inv.delvTocontperson = kw['delvTocontperson'] 
        new_inv.delvToconttel = kw['delvToconttel'] 
        DBS_JistInvoicing.add(new_inv)
        DBS_JistInvoicing.flush()

    @expose()
    def saveeditinvoice_clientdata(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        if not kw['inv_date_edit']:
            return
        if not kw['inv_client_name_edit']:
            return
        new_inv= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['invid'])). \
                      one()
        new_inv.invdate = kw['inv_date_edit']
        new_inv.ordernumber = str(kw['order_number_edit'])
        new_inv.client = kw['inv_client_name_edit']
        new_inv.contract = kw['jcno_edit']
        client_inv= DBS_JistInvoicing.query(JistInvoicesClients). \
                      filter(JistInvoicesClients.invoiceid==int(kw['invid'])). \
                      one()

        client_inv.add1 = kw['address_line1_edit'] 
        client_inv.add2 = kw['address_line2_edit'] 
        client_inv.add3 = kw['address_line3_edit'] 
        client_inv.vatno = kw['vat_number_edit'] 
        client_inv.delvToname = kw['delvToname_edit'] 
        client_inv.delvToadd1 = kw['delvToadd1_edit'] 
        client_inv.delvToadd2 = kw['delvToadd2_edit'] 
        client_inv.delvTocontperson = kw['delvTocontperson_edit'] 
        client_inv.delvToconttel = kw['delvToconttel_edit'] 

    @expose()
    def savenewinvoice_data(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_inv = JistInvoicesData()
        new_inv.invid = int(kw['invid'])
        new_inv.item = kw['item'] 
        new_inv.description = kw['description'] 
        new_inv.unit = kw['unit'] 
        new_inv.qty = kw['qty'] 
        new_inv.price = kw['price'] 
        new_inv.total = kw['total'] 
        new_inv.orderitemsid = kw['orderitemsid'] 
        DBS_JistInvoicing.add(new_inv)
        DBS_JistInvoicing.flush()
        invoice_total_excl = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.invid==int(kw['invid'])). \
                     value(func.sum(JistInvoicesData.total))
        invoice= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['invid'])). \
                      one()

        totalexcl = Decimal(invoice_total_excl).quantize(Decimal('1.00'))
        totalvat = (float(invoice_total_excl))*VAT_RATE
        thisvat  = Decimal(totalvat).quantize(Decimal('1.00'))
        totalinl = Decimal(totalvat,2)+ Decimal(invoice_total_excl,2)
        totalincl = Decimal(totalinl).quantize(Decimal('1.00'))

        invoice.value_excl = totalexcl 
        invoice.value_vat = thisvat 
        invoice.value_incl = totalincl 
        thisreturnstring = str(totalexcl)+","+str(thisvat)+","+str(totalincl)
        return str(thisreturnstring) 

    @expose()
    def saveaddinvoiceitem_data(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_inv = JistInvoicesData()
        new_inv.invid = int(kw['invid'])
        new_inv.item = kw['ivn_item_edit'] 
        new_inv.description = kw['ivn_description_edit'] 
        new_inv.unit = kw['ivn_unit_edit'] 
        new_inv.qty = kw['ivn_qty_edit'] 
        new_inv.price = kw['ivn_price_edit'] 
        new_inv.total = kw['ivn_total_edit'] 
        #new_inv.orderitemsid = kw['orderitemsid'] 
        DBS_JistInvoicing.add(new_inv)
        DBS_JistInvoicing.flush()
        invoice_total_excl = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.invid==int(kw['invid'])). \
                     value(func.sum(JistInvoicesData.total))
        invoice= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['invid'])). \
                      one()

        totalexcl = Decimal(invoice_total_excl).quantize(Decimal('1.00'))
        totalvat = (float(invoice_total_excl))*VAT_RATE
        thisvat  = Decimal(totalvat).quantize(Decimal('1.00'))
        totalinl = Decimal(totalvat,2)+ Decimal(invoice_total_excl,2)
        totalincl = Decimal(totalinl).quantize(Decimal('1.00'))

        invoice.value_excl = totalexcl 
        invoice.value_vat = thisvat 
        invoice.value_incl = totalincl 
        thisreturnstring = str(totalexcl)+","+str(thisvat)+","+str(totalincl)
        return str(thisreturnstring) 


    @expose()
    def savenewinvoice_totals(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        invoice= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['invid'])). \
                      one()
        invoice.value_excl = kw['excl'] 
        invoice.value_vat =  kw['vat'] 
        invoice.value_incl = kw['incl'] 

    @expose()
    def saveeditinvoice_data(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        edit_inv = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.id==int(kw['ivn_id_edit'])). \
                      one()
        edit_inv.item = kw['ivn_item_edit'] 
        edit_inv.description = kw['ivn_description_edit'] 
        edit_inv.unit = kw['ivn_unit_edit'] 
        edit_inv.qty = kw['ivn_qty_edit'] 
        edit_inv.price = kw['ivn_price_edit'] 
        edit_inv.total = kw['ivn_total_edit'] 
        #DBS_JistInvoicing.add(new_inv)
        #DBS_JistInvoicing.flush()
        invoice_total_excl = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.invid==int(kw['ivn_invid_edit'])). \
                     value(func.sum(JistInvoicesData.total))
        invoice= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['ivn_invid_edit'])). \
                      one()

        totalexcl = Decimal(invoice_total_excl).quantize(Decimal('1.00'))
        totalvat = (float(invoice_total_excl))*VAT_RATE
        thisvat  = Decimal(totalvat).quantize(Decimal('1.00'))
        totalinl = Decimal(totalvat,2)+ Decimal(invoice_total_excl,2)
        totalincl = Decimal(totalinl).quantize(Decimal('1.00'))

        invoice.value_excl = totalexcl 
        invoice.value_vat = thisvat 
        invoice.value_incl = totalincl 
        #thisreturnstring = str(totalexcl)+","+str(thisvat)+","+str(totalincl)
        return  

    @expose()
    def savedeleteinvoice_data(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        edit_inv = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.id==int(kw['ivn_id_edit'])). \
                      one()
        DBS_JistInvoicing.delete(edit_inv)
        invoice_total_excl = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.invid==int(kw['ivn_invid_edit'])). \
                     value(func.sum(JistInvoicesData.total))
        invoice= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['ivn_invid_edit'])). \
                      one()

        totalexcl = Decimal(invoice_total_excl).quantize(Decimal('1.00'))
        totalvat = (float(invoice_total_excl))*VAT_RATE
        thisvat  = Decimal(totalvat).quantize(Decimal('1.00'))
        totalinl = Decimal(totalvat,2)+ Decimal(invoice_total_excl,2)
        totalincl = Decimal(totalinl).quantize(Decimal('1.00'))

        invoice.value_excl = totalexcl 
        invoice.value_vat = thisvat 
        invoice.value_incl = totalincl 
        #thisreturnstring = str(totalexcl)+","+str(thisvat)+","+str(totalincl)
        return  

    @expose()
    def savetotalsinvoice_data(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #print
        #return
        invoice= DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(kw['ivn_invid_edit'])). \
                      one()

        invoice.value_excl = kw['invs_totalexcl_edit'] 
        invoice.value_vat =  kw['invs_totalvat_edit']
        invoice.value_incl =  kw['invs_totalincl_edit']
        #thisreturnstring = str(totalexcl)+","+str(thisvat)+","+str(totalincl)
        return  

    @expose()
    def export_invoice_single_pdf(self,invid):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = "Jist-Invoice-"+invid+".pdf"
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        invdetails = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.id==int(invid)). \
                     one()
        clientdetails = DBS_JistInvoicing.query(JistInvoicesClients). \
                      filter(JistInvoicesClients.invoiceid==int(invid)). \
                     one()
        invdescriptiondata = DBS_JistInvoicing.query(JistInvoicesData). \
                      filter(JistInvoicesData.invid==int(invid)). \
                     all()
        pdffile.CreatePDFInvoice(invid,invdetails,clientdetails,invdescriptiondata)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent


    @expose()
    def savenewinvoicepayment(self,invid,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        amt = DBS_JistInvoicing.query(JistInvoicesList). \
                filter(JistInvoicesList.id == invid).one()
        new_payment = JistInvoicesPayments()
        new_payment.invoiceid = invid
        if not kw['paymentdate']:
            return
        new_payment.paymentdate= kw['paymentdate']
        if kw['paymentamount']:
            new_payment.amount=kw['paymentamount']
        else:
            new_payment.amount=amt.value_incl
        #print new_payment.amount
        #return
        DBS_JistInvoicing.add(new_payment)
        DBS_JistInvoicing.flush()

    @expose()
    def save_edit_invoice_payment(self,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        edit_payment = DBS_JistInvoicing.query(JistInvoicesPayments). \
                filter(JistInvoicesPayments.id == kw['edit_activepaymentid']).one()
        edit_payment.paymentdate= kw['edit_paymentdate']
        if kw['edit_paymentamount']:
            edit_payment.amount=kw['edit_paymentamount']

    @expose()
    def toggleinvoicescontract(self,jno,**kw):
        if jno:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==int(jno)).one()
            statusprop = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            invoices_contract = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==int(jno)). \
                          all()
            invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==jno). \
                         value(func.sum(JistInvoicesList.value_excl))
            if not invoices_total_excl: invoices_total_excl = 0
            inv_total_excl = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
            html0 = """
                        <table class='tableinvoicesitems'>
                        <tr>
                        <td>
                        Total Invoice Values Excl
                        </td>
                        <td align='right'>
                        %s
                        </td>
                        </tr>
                        </table>
                        <p/>



                    """%(inv_total_excl)
            html1 = """
                                <table id='tblinvoices_contract' class='tableinvoicesitems'>
                                <th>Inv No</th>
                                <th>Date</th>
                                <th>Client</th>
                                <th>Value Excl</th>
                                <th>Value Vat</th>
                                <th>Value Incl</th>
                    """
            temphtml1 = ""
            html2 = ""
            for scp in invoices_contract:
                temphtml1 = """
                        <tr>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        </tr>
                        """%(scp.id,scp.invdate,scp.client,
                             scp.value_excl,scp.value_vat,scp.value_incl)
                html2 = html2 + temphtml1

            html3 = """
                                </table>

                    """
            html =  html1 + html2 + html3
            #<a href='/cctvcont/getfacialonelive/192.168.0.96/axi'>
            #<img src=%s width=80></img>
            #</a>
            return html

    @expose()
    def toggleorderitems(self,jno,**kw):
        if jno:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==int(jno)).one()
            statusprop = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            scope = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno).all()
            invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==jno). \
                         value(func.sum(JistInvoicesList.value_excl))
            contract_total = DBS_ContractData.query(JistContractOrderItems). \
                          filter(JistContractOrderItems.jno==jno). \
                         value(func.sum(JistContractOrderItems.total))
            if not contract_total: contract_total = 0.00
            cont_total_excl = format_decimal(contract_total,format='#,##0.00;-#0.00',locale='en')
            html0 = """
                        <table class='tableinvorderitems'>
                        <tr>
                        <td>
                        Total Order Values Excl
                        </td>
                        <td align='right'>
                        %s
                        </td>
                        </tr>
                        </table>
                        <p/>
                    """%(cont_total_excl)
            html1 = """
                                <table  class='tableinvorderitems'>
                                <th>JCNo</th>
                                <th>Item</th>
                                <th>Description</th>
                                <th>Unit</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Total</th>
                    """
            temphtml1 = ""
            html2 = ""
            for scp in scope:
                temphtml1 = """
                        <tr>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        </tr>
                        """%(scp.jno,scp.item,scp.description,
                             scp.unit,scp.qty,scp.price,scp.total)
                html2 = html2 + temphtml1
            html3 = """
                                </table>
                    """
            html = html1 + html2 + html3
            #<a href='/cctvcont/getfacialonelive/192.168.0.96/axi'>
            #<img src=%s width=80></img>
            #</a>
            return html

    @expose()
    def toggleorderitemsbalances(self,jno,**kw):
        if jno:
            scope = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno).all()
            invs_all = []
            invoices_contract = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==int(jno)). \
                          all()
            for scp in scope:
                jcno=jno,
                orderitemid=str(scp.id),
                scopeitem=str(scp.item),
                scopedescription=scp.description,
                scopeunit=scp.unit,
                scopeqty=scp.qty,
                scopeprice=scp.price,
                scopetotal=scp.total,
                invidno=''
                invqty=''
                invitem=''
                for inv in invoices_contract:
                    invitems = DBS_JistInvoicing.query(JistInvoicesData). \
                                  filter(JistInvoicesData.invid==int(inv.id)). \
                                  all()
                    for item in invitems:
                        if item.item==scp.item:
                            invidno = item.invid
                            invqty = item.qty
                invs_all.append({ 
                    'orderitemid':orderitemid[0],
                    'jcno':jcno[0],
                    'scopeitem':scopeitem[0],
                    'scopedescription':scopedescription[0],
                    'scopeunit':scopeunit[0],
                    'scopeqty':scopeqty[0],
                    'scopeprice': scopeprice[0],
                    'scopetotal': scopetotal[0],
                    'invidno': invidno,
                    'invqty': invqty,
                                    })
            html1 = """
                                <table id='tblinvoices_orderitems'class='tableinvorderitems'>
                                <th>OrderItem ID</th>
                                <th>JCNo</th>
                                <th>Item</th>
                                <th>Description</th>
                                <th>Unit</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Total</th>
                    """
            contractshtml = ""
            for inv in invoices_contract:
                contractshtml = contractshtml +"<th>Inv %s</th>"%inv.id
            len_invoices_contract = len(invoices_contract)
            temphtml1 = ""
            html2 = ""
            for scp in invs_all:
                temphtml1 = """
                        <tr>
                        <td width='20px' >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td>
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        """%(scp['orderitemid'],scp['jcno'],scp['scopeitem'],scp['scopedescription'],
                             scp['scopeunit'],scp['scopeqty'],
                             scp['scopeprice'],scp['scopetotal'])
                for i in range(len_invoices_contract):
                    if scp['invidno'] ==invoices_contract[i].id:
                        temphtml1 = temphtml1 + "<td align='right'>%s</td>"%scp['invqty']
                    else:
                        temphtml1 = temphtml1 + "<td></td>"
                        
                html2 = html2 + temphtml1 + "</tr>"
                
            html3 = """
                                </table>
                    """
            html = html1+contractshtml + html2 + html3
            return html

    @expose()
    def toggleinvoiceitems(self,invid,**kw):
        if invid == 0: # to cater for emptyness
            html = """
                    No Invoices Selected
                   """
            return html
        if invid:
            #statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==int(jno)).one()
            #statusprop = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            invoice_items = DBS_JistInvoicing.query(JistInvoicesData). \
                          filter(JistInvoicesData.invid==int(invid)). \
                          all()
            invoiceslist = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.id==int(invid)). \
                          one()
            inv_total_excl = 0
            #if not invoices_total_excl: invoices_total_excl = 0
            #inv_total_excl = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
            html0 = """
                        <table class='tableinvoicesitems'>
                        <tr>
                        <td>
                        Total Invoice Values Excl
                        </td>
                        <td align='right'>
                        %s
                        </td>
                        </tr>
                        </table>
                        <p/>



                    """%(inv_total_excl)
            html1 = """
                                <table id='tblinv_single_item_table' class='tableinvoicesitems'>
                                <th>ID</th>
                                <th>Item</th>
                                <th>Description</th>
                                <th>Unit</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Total</th>
                    """
            temphtml1 = ""
            html2 = ""
            for scp in invoice_items:
                temphtml1 = """
                        <tr>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        </td>
                        <td align='right' >
                        %s
                        </td>
                        </tr>
                        """%(scp.id,scp.item,scp.description,
                             scp.unit,scp.qty,scp.price,scp.total)
                html2 = html2 + temphtml1

            html3 = """
                        </table>
                        <p/>
                        <form id="inv_new_totals_edit">
                        <fieldset>
                                <table id="tbl_inv_new_totals_edit" class="tableinvoicesitems">
                                    <tr>
                                      <td>
                                            <label for="invs_totalexcl_edit">Total Excl</label>
                                      </td><td>
                                            <input type="text" value="%s" name="invs_totalexcl_edit"
                                            id="invs_totalexcl_edit" class="text ui-widget-content ui-corner-all" />
                                      </td><td>
                                            <label for="invs_totalvat_edit">Total VAT</label>
                                      </td><td>
                                            <input type="text" value="%s" name="invs_totalvat_edit"
                                            id="invs_totalvat_edit" class="text ui-widget-content ui-corner-all" />
                                      </td><td>
                                            <label for="invs_totalincl">Total Incl</label>
                                      </td><td>
                                            <input type="text" value="%s" name="invs_totalincl_edit"
                                            id="invs_totalincl_edit" class="text ui-widget-content ui-corner-all" />
                                      </td><td>
                                        <a href='/invoicingcont/export_invoice_single_pdf/%s'> 
                                        <img src="/images/pdficon.jpg"></img></a>
                                      </td
                                    </tr>
                                    <tr><td>
                                      <button class="ui-state-default ui-corner-all"
                                          id="button_change_sums_invoice">Change Totals Of Invoice</button>
                                    </td></tr>
                                </table>
                        </fieldset>
                        </form>

                    """%(invoiceslist.value_excl,invoiceslist.value_vat,invoiceslist.value_incl,invid)
            html =  html1 + html2 + html3
            #<a href='/cctvcont/getfacialonelive/192.168.0.96/axi'>
            #<img src=%s width=80></img>
            #</a>
            return html

    @expose()
    def ajax_contracts_wip_balances(self,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()

        locale.setlocale(locale.LC_ALL, '')
        grandtotalexcl = 0
        for thisites in contracts:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==thisites.jno).one()
            status = {}
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            try:
                agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
                status = {'pointperson':statusall.pointperson,
                          'siteagent':statusall.siteagent}
            except:
                status = {'pointperson':statusall.pointperson,
                          'siteagent':'1'}
            siteagent = DBS_ContractData.query(User).filter(User.user_id==status['pointperson']).one()
            invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==thisites.jno). \
                         value(func.sum(JistInvoicesList.value_excl))
            if invoices_total_excl is None:
                totalexcl_invoices = 0.00
                invoices_total_excl = 0.00
                totalexcl_invoices = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
            else:
                totalexcl_invoices = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
                
            totalexcl_contractvalue = DBS_ContractData.query(JistContractOrderItems). \
                    filter(JistContractOrderItems.jno==thisites.jno). \
                    value(func.sum(JistContractOrderItems.total))
            if totalexcl_contractvalue is None:
                totalexcl_contract = 0.00
                totalexcl_contractvalue = 0.00
                totalexcl_contract = format_decimal(totalexcl_contractvalue,format='#,##0.00;-#0.00',locale='en')
            else:
                totalexcl_contract = format_decimal(totalexcl_contractvalue,format='#,##0.00;-#0.00',locale='en')
            totalexcl_diff_temp = Decimal(totalexcl_contractvalue) - Decimal(invoices_total_excl)
            totalincl_diff_temp = (float(totalexcl_contractvalue)-float(invoices_total_excl))*VAT_RATE+(float(totalexcl_diff_temp))
            totalexcl_diff = format_decimal(totalexcl_diff_temp,format='#,##0.00;-#0.00',locale='en')
            totalincl_diff = format_decimal(totalincl_diff_temp,format='#,##0.00;-#0.00',locale='en')
            grandtotalexcl = grandtotalexcl + totalexcl_diff_temp
            dictsites.append({'jno':thisites.jno,
                          'orderno':thisites.orderno,
                         'orderdate':thisites.orderdate,
                         'client':thisites.client,
                         'description':thisites.description,
                         'site':thisites.site,
                         'contact':thisites.contact,
                         'tel':thisites.tel,
                         'fax':thisites.fax,
                         'cell':thisites.cell,
                         'workcategory':thisites.workcategory,
                         'cidbcategory':thisites.cidbcategory,
                         'cidbrating':thisites.cidbrating,
                         'groupjno':thisites.groupjno,
                         'completed':thisites.completed,
                         'pointperson':siteagent.user_name,
                         'totalexcl_contractvalue':totalexcl_contract,
                         'totalexcl_invoices':totalexcl_invoices,
                         'totalexcl_diff':totalexcl_diff,
                         'totalincl_diff':totalincl_diff,
                         'status':statcode.status,
                         })

        grandtotalexclsum = format_decimal(grandtotalexcl,format='#,##0.00;-#0.00',locale='en')
        grandvat = float(grandtotalexcl) * VAT_RATE
        grandincl = float(grandvat) + float(grandtotalexcl)
        grandtotalinclsum = format_decimal(grandincl,format='#,##0.00;-#0.00',locale='en')
        grandvatsum = format_decimal(grandvat,format='#,##0.00;-#0.00',locale='en')

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """
                            <p id='contractheader'>Contracts In Progress: 
                            </p>
                            <table class='table_estdata' >
                            <tr>
                            <td>
                            Total WIP Balance Excl:
                            </td><td align='right'>
                            %s
                            </td><td>
                            Total WIP Balance Vat:
                            </td><td align='right'>
                             %s
                            </td><td>
                            Total WIP Balance Incl:
                            </td><td align='right'>
                             %s
                            </td></tr>
                            </table>
                            <table id='contracts_wip_table' class='table_estdata'>
                            <th>JCNo</th>
                            <th>Order Date</th>
                            <th>Client</th>
                            <th>Site Name</th>
                            <th>Description</th>
                            <th>Point</th>
                            <th>Status</th>
                            <th>Contract Excl</th>
                            <th>Invoiced Excl</th>
                            <th>Balance Excl</th>
                            <th>Balance Incl</th>
                """%(grandtotalexclsum, grandvatsum, grandtotalinclsum)
        temphtml1 = ""
        html2 = ""
        for scp in dictsites:
            #print scp["name"]
            temphtml1 = """
                    <tr>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                        <td>
                            %s
                        </td>
                        <td>
                            %s
                        </td>
                        <td>
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                    </tr>
                    """%(scp["jno"],scp["orderdate"],scp["client"],scp["site"],
                            scp["description"],scp["pointperson"],scp["status"],
                            scp["totalexcl_contractvalue"],scp["totalexcl_invoices"],scp["totalexcl_diff"],scp["totalincl_diff"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax_contracts_completed_balances(self,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.completed=="True"). \
                filter(JistContracts.jno > 1000). \
               order_by(desc(JistContracts.jno)).all()
        locale.setlocale(locale.LC_ALL, '')
        grandtotalexcl = 0
        for thisites in contracts:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==thisites.jno).one()
            status = {}
            try:
                agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
                status = {'pointperson':statusall.pointperson,
                          'siteagent':statusall.siteagent}
            except:
                status = {'pointperson':statusall.pointperson,
                          'siteagent':'1'}
            siteagent = DBS_ContractData.query(User).filter(User.user_id==status['pointperson']).one()
            invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==thisites.jno). \
                         value(func.sum(JistInvoicesList.value_excl))
            if invoices_total_excl is None:
                totalexcl_invoices = 0.00
                invoices_total_excl = 0.00
                totalexcl_invoices = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
            else:
                totalexcl_invoices = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
                
            totalexcl_contractvalue = DBS_ContractData.query(JistContractOrderItems). \
                    filter(JistContractOrderItems.jno==thisites.jno). \
                    value(func.sum(JistContractOrderItems.total))
            if totalexcl_contractvalue is None:
                totalexcl_contract = 0.00
                totalexcl_contractvalue = 0.00
                totalexcl_contract = format_decimal(totalexcl_contractvalue,format='#,##0.00;-#0.00',locale='en')
            else:
                totalexcl_contract = format_decimal(totalexcl_contractvalue,format='#,##0.00;-#0.00',locale='en')
            totalexcl_diff_temp = Decimal(totalexcl_contractvalue) - Decimal(invoices_total_excl)
            totalincl_diff_temp = (float(totalexcl_contractvalue)-float(invoices_total_excl))*VAT_RATE+(float(totalexcl_diff_temp))
            totalexcl_diff = format_decimal(totalexcl_diff_temp,format='#,##0.00;-#0.00',locale='en')
            totalincl_diff = format_decimal(totalincl_diff_temp,format='#,##0.00;-#0.00',locale='en')
            grandtotalexcl = grandtotalexcl + totalexcl_diff_temp
        
            dictsites.append({'jno':thisites.jno,
                          'orderno':thisites.orderno,
                         'orderdate':thisites.orderdate,
                         'client':thisites.client,
                         'description':thisites.description,
                         'site':thisites.site,
                         'contact':thisites.contact,
                         'tel':thisites.tel,
                         'fax':thisites.fax,
                         'cell':thisites.cell,
                         'workcategory':thisites.workcategory,
                         'cidbcategory':thisites.cidbcategory,
                         'cidbrating':thisites.cidbrating,
                         'groupjno':thisites.groupjno,
                         'completed':thisites.completed,
                         'pointperson':siteagent.user_name,
                         'totalexcl_contractvalue':totalexcl_contract,
                         'totalexcl_invoices':totalexcl_invoices,
                         'totalexcl_diff':totalexcl_diff,
                         'totalincl_diff':totalincl_diff,
                         })

        grandtotalexclsum = format_decimal(grandtotalexcl,format='#,##0.00;-#0.00',locale='en')
        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """
                            <p id='contractheader'>Contracts Completed: 
                            %s
                            </p>
                            <table id='contracts_wip_table' class='table_estdata'>
                            <th>JCNo</th>
                            <th>Order Date</th>
                            <th>Client</th>
                            <th>Site Name</th>
                            <th>Description</th>
                            <th>Point</th>
                            <th>Contract Excl</th>
                            <th>Invoiced Excl</th>
                            <th>Balance Excl</th>
                            <th>Balance Incl</th>
                """%grandtotalexclsum
        temphtml1 = ""
        html2 = ""
        for scp in dictsites:
            #print scp["name"]
            temphtml1 = """
                    <tr>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                        <td>
                            %s
                        </td>
                        <td>
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                        <td align="right">
                            %s
                        </td>
                    </tr>
                    """%(scp["jno"],scp["orderdate"],scp["client"],scp["site"],
                            scp["description"],scp["pointperson"],
                            scp["totalexcl_contractvalue"],scp["totalexcl_invoices"],scp["totalexcl_diff"],scp["totalincl_diff"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax_get_payment_info(self,invid,**kw):
        invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                      filter(JistInvoicesPayments.invoiceid==int(invid)). \
                     all()
        #print invoice_payments[0].id
        invpayments = []
        payments_total = 0
        if invoice_payments:
            for r in invoice_payments:
                payments_total = payments_total + r.amount
                inv_one = DBS_JistInvoicing.query(JistInvoicesList). \
                        filter(JistInvoicesList.id == r.invoiceid).one()
                invpayments.append({'invoiceid':inv_one.id,
                                    'invoice_amount':inv_one.value_incl,
                                    'payment_id':r.id,
                                    'invoice_payment_date':r.paymentdate,
                                    'invoice_payment_amount':r.amount,
                                    })
                #print r.invoiceid, r.paymentdate, r.amount

        locale.setlocale(locale.LC_ALL, '')
        sitedata = """<div class='div_tableinvvspay'>
                    <table id='tblpaymentlist' class='tableinvoicelist'>
                    
                    """
        headerdata = """
                    <th>Inv No </th>
                    <th>Inv Amount </th>
                    <th>Payment ID </th>
                    <th>Payment Date</th>
                    <th>Payment Amount</th>
                    """
        sitedata = sitedata + headerdata
        totalbal = 0
        totalbalance = 0
        pdate = ""
        pmount = 0
        pamount = 0
        balance = 0
        bal = 0
        for k in invpayments: 
            sitedatatemp = """
                            <tr>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (
                                    k['invoiceid'],
                                    k['invoice_amount'],
                                    k['payment_id'],
                                    k['invoice_payment_date'],
                                    k['invoice_payment_amount'],
                                   )
            sitedata = sitedata + sitedatatemp
        sitedata = sitedata +"</table></div>" 
        return sitedata 

    @expose()
    def ajax_get_payments_paid_date(self,**kw):
        if not kw['clientstartdatepayment']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                if k == "clientstartdatepayment":
                    year =w.split('-')[0]
                    month =w.split('-')[1]
                    day =w.split('-')[2]
        if not kw['clientenddatepayment']:
            endyear = str(0)
        else :
            for k,w in kw.iteritems():
                if k == "clientenddatepayment":
                    endyear =w.split('-')[0]
                    endmonth =w.split('-')[1]
                    endday =w.split('-')[2]
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
        payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.paymentdate>=startdate). \
                     filter(JistInvoicesPayments.paymentdate<=enddate). \
                     order_by(desc(JistInvoicesPayments.invoiceid)). \
                     all()
        payments_total = DBS_JistInvoicing.query(JistInvoicesPayments). \
                     filter(JistInvoicesPayments.paymentdate>=startdate). \
                     filter(JistInvoicesPayments.paymentdate<=enddate). \
                     value(func.sum(JistInvoicesPayments.amount))
        invpayments = []
        payments_total = 0
        for inv_one in payments:
            #for col in inv_one.__table__._columns:
            #    print col
            #return
            invoice = DBS_JistInvoicing.query(JistInvoicesList). \
                         filter(JistInvoicesList.id == inv_one.invoiceid). \
                         one()
            contract = DBS_ContractData.query(JistContracts).get(invoice.contract)
            #for col in contract.__table__._columns:
            #    print col
            #grandtotalexclsum = format_decimal(grandtotalexcl,format='#,##0.00;-#0.00',locale='en')
            invpayments.append({'invoiceid':invoice.id,
                                'invoice_amount':format_decimal(invoice.value_incl,format='#,##0.00;-#0.00',locale='en'),
                                'jcno':contract.jno,
                                'client':invoice.client,
                                'site':contract.site,
                                'payment_id':inv_one.id,
                                'invoice_payment_date':inv_one.paymentdate,
                                'invoice_payment_amount':format_decimal(inv_one.amount,format='#,##0.00;-#0.00',locale='en'),
                                })
            #print r.invoiceid, r.paymentdate, r.amount
        locale.setlocale(locale.LC_ALL, '')
        sitedata = """<div class='div_tableinvvspay'>
                    <table id='tblpaymentlist' class='tableinvoicelist'>
                    
                    """
        headerdata = """
                    <th>Inv No </th>
                    <th>Inv Amount </th>
                    <th>JCNo </th>
                    <th>Client </th>
                    <th>Site </th>
                    <th>Payment ID </th>
                    <th>Payment Date</th>
                    <th>Payment Amount</th>
                    """
        sitedata = sitedata + headerdata
        totalbal = 0
        totalbalance = 0
        pdate = ""
        pmount = 0
        pamount = 0
        balance = 0
        bal = 0
        for k in invpayments: 
            sitedatatemp = """
                            <tr>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (
                                    k['invoiceid'],
                                    k['invoice_amount'],
                                    k['jcno'],
                                    k['client'],
                                    k['site'],
                                    k['payment_id'],
                                    k['invoice_payment_date'],
                                    k['invoice_payment_amount'],
                                   )
            sitedata = sitedata + sitedatatemp
        sitedata = sitedata +"</table></div>" 
        return sitedata 
