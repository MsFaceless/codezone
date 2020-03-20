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
__all__ = ['AccountsController']


class AccountsController(BaseController):
    """Sample controller-wide authorization"""
    
    #The predicate that must be met for all the actions in this controller:
    allow_only = has_any_permission('manage','accounts','accountsmanage', msg=l_('Only for people with the "manage" permission'))

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
        redirect('accountscont/menu')

    @expose('jistdocstore.templates.accounts.accountsindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Accounts: Main Menu') 

    @expose('jistdocstore.templates.invoicing.invoicingconsole')
    def invoicing_console(self,**named):
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()

        return dict(page='Invoicing Console',
                    invoices = invoices,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.accounts.payreqconsole')
    def payreq_console(self,**named):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        statcodeall  = DBS_ContractData.query(JistContractStatusCodes).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        payee_list = DBS_JistInvoicing.query(JistPaymentPayee). \
                all()
        pointlist = []
        productionlist = []
        accountslist = []
        percentlist = [x for x in range(101)]
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
        return dict(page='Payment Requisition Console',
                    userlist =productionlist, 
                    wip = contracts,
                    percentlist = percentlist,
                    payee_list = payee_list,
                    timeperiod = range(1,9),
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.management.financialconsole')
    def financial_console(self,**named):
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

        return dict(page='Financial Console',
                    wip = '',
                    currentPage=1,
                    points = pointlist,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.accounts.search_invoices_date')
    def search_invoices_date(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=InvoiceDateComboSearch(),
                    target="output",
                    action="do_search_invoices_dates")

        tmpl_context.form = ajax_form 

        return dict(page='suppliersearch',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def do_search_paymentreqs_all(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        #sttimestart = time(0,0,0)
        #sttimeend = time(23,59,59)
        #startdate = datetime.combine(today,sttimestart)
        #enddate = datetime.combine(endtoday,sttimeend)
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        sitedata = "<table class='tableinvoicelist'>"
        headerdata = """
                    <th>ID </th>
                    <th>Date </th>
                    <th>PO Number</th>
                    <th>Payee</th>
                    <th>Req By</th>
                    <th>JCNo</th>
                    <th>Purchase Req</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Rate</th>
                    <th>Total Excl</th>
                    <th>Total Vat</th>
                    <th>Total Incl</th>
                    <th>Must Pay Date</th>
                    <th>Promised Pay Date</th>
                    <th>Payed</th>
                    <th>Date Payed</th>
                    <th>Active</th>
                    <th>Added By</th>
                    <th>Edited By</th>
                    """
        sitedata = sitedata + headerdata
        for k in paymentreqs:
            #totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            #contract = DBS_ContractData.query(JistContracts).get(k.contract)
            #statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            #point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            #user_name = point.user_name
            #if k.id > 970 and k.id < 1000:
            #    print k.id, k.payreq_description
            #print k.id, k.payreq_description
            sitedatatemp = """
                            <tr>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td align='left'>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.payreq_date,
                                    k.payreq_ponumber,
                                    payee.payee_name,
                                    k.payreq_by,
                                    k.payreq_jcno,
                                    k.payreq_purchasereq_number,
                                    k.payreq_description,
                                    k.payreq_unit,
                                    k.payreq_qty,
                                    k.payreq_rate,
                                    k.payreq_total_excl,
                                    k.payreq_total_vat,
                                    k.payreq_total_incl,
                                    k.payreq_must_pay_date,
                                    k.payreq_promised_pay_date,
                                    k.payreq_paid,
                                    k.payreq_date_paid,
                                    k.payreq_active,
                                    k.useridnew,
                                    k.useridedited,
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def do_search_paymentreqs_notapproved(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.payreq_approved_bln==0). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        paymentalldatetotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_approved_bln==0). \
                         filter(JistPaymentReqs.payreq_paid==0). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentalldatetotal: paymentalldatetotal = 0
        totalpayments = format_decimal(paymentalldatetotal, format='#,##0.00;-#0.00',locale='en')
        sitedata = """

                <div id="payreq_edit" title="Edit Payment Req" style="display:none"> 
                </div>
                <h2 class="ui-widget-header paymentheader">Payments Not Approved 
                <span style="float:right; margin-right:90px">
                <a href='/accountscont/export_payment_notapproved'> 
                <img src="/images/pdficon.jpg"></img>
                </a>
                %s
                </span> 
                </h2>
                """%(totalpayments)
        sitedata = sitedata + "<table class='tableinvoicelist' id='tbl_pay_reqs_notapproved'>"
        headerdata = """
                    <th>ID </th>
                    <th>Date </th>
                    <th>Payee</th>
                    <th>Description</th>
                    <th>Total Incl</th>
                    <th>Must Pay Date</th>
                    <th>Added By</th>
                    <th>Approve</th>
                    <th>Split Payment</th>
                    <th>Edit </th>
                    """
        sitedata = sitedata + headerdata
        for k in paymentreqs:
            if not k.payreq_total_incl: k.payreq_total_incl = 0
            totalpayment = format_decimal(k.payreq_total_incl, format='#,##0.00;-#0.00',locale='en')
            userid_new =  DBS_ContractData.query(User).filter(User.user_id==k.useridnew).one()
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            sitedatatemp = """
                            <tr>
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
                            <td width='25px'>
                            <img src="/images/staffpics/%s.png"></img></a>
                            </td>
                            <td width='25px'>
                            <img src="/images/approve_32.png"></img></a>
                            </td>
                            <td width='25px'>
                            <img src="/images/cashslip.png"></img></a>
                            </td>
                            <td width='25px'>
                            <img src="/images/cashslip.png"></img></a>
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.payreq_date,
                                    payee.payee_name,
                                    k.payreq_description,
                                    totalpayment,
                                    k.payreq_must_pay_date,
                                    userid_new.user_id,
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        jscript = """
                    <script>
                        var thistable = document.GetElementByID("pay_reqs_notapproved")
                        sortable.makeSortable(thistable)

                    </script>

                  """
        return sitedata  

    @expose()
    def do_search_paymentreqs_unpaid_approved(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.payreq_approved_bln==1). \
                     filter(JistPaymentReqs.payreq_paid==0). \
                     order_by(desc(JistPaymentReqs.payreq_date_topay)). \
                     all()
        paymentalldatetotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_approved_bln==1). \
                         filter(JistPaymentReqs.payreq_paid==0). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentalldatetotal: paymentalldatetotal = 0
        totalpayments = format_decimal(paymentalldatetotal, format='#,##0.00;-#0.00',locale='en')
        sitedata = """
                <h2 class="ui-widget-header paymentheader">Total Payments Approved Not Paid
                <span style="float:right; margin-right:90px">
                <a href='/accountscont/export_payment_approved_unpaid'> 
                <img src="/images/pdficon.jpg"></img>
                </a>
                %s
                </span> 
                </h2>
                """%(totalpayments)
        sitedata = sitedata + "<table class='tableinvoicelist' id='tbl_pay_reqs_unpaid_approved'>"
        headerdata = """
                    <th>ID </th>
                    <th>Date </th>
                    <th>Payee</th>
                    <th>Description</th>
                    <th>Total Incl</th>
                    <th>Must Pay Date</th>
                    <th>Added By</th>
                    <th>Un-Approve</th>
                    <th>Set Payment Date</th>
                    <th>Prov Payment Date</th>
                    """
        sitedata = sitedata + headerdata
        for k in paymentreqs:
            if not k.payreq_total_incl: k.payreq_total_incl = 0
            totalpayment = format_decimal(k.payreq_total_incl, format='#,##0.00;-#0.00',locale='en')
            userid_new =  DBS_ContractData.query(User).filter(User.user_id==k.useridnew).one()
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            sitedatatemp = """
                            <tr>
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
                            <td width="70px" align='right'>%s
                            </td>
                            <td width="25px">
                            <img src="/images/staffpics/%s.png"></img></a>
                            </td>
                            <td width="25px">
                            <img src="/images/approve_not_32.png"></img></a>
                            </td>
                            <td width="25px">
                            <img src="/images/dates.png"></img></a>
                            </td>
                            <td width="70px">
                            %s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.payreq_date,
                                    payee.payee_name,
                                    k.payreq_description,
                                    totalpayment,
                                    k.payreq_must_pay_date,
                                    userid_new.user_id,
                                    k.payreq_date_topay,
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        jscript = """
                    <script>
                        var thistable = document.GetElementByID("pay_reqs_notapproved")
                        sortable.makeSortable(thistable)

                    </script>

                  """
        return sitedata  

    @expose()
    def do_search_paymentreqs_paymentlist(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        paymentreqsdate = DBS_JistInvoicing.query(func.distinct(JistPaymentReqs.payreq_date_topay)). \
                     filter(JistPaymentReqs.payreq_paid==0). \
                     filter(JistPaymentReqs.payreq_approved_bln==1). \
                     order_by(asc(JistPaymentReqs.payreq_date_topay)). \
                     all()
        paymentalldatetotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_paid==0). \
                         filter(JistPaymentReqs.payreq_approved_bln==1). \
                         filter(JistPaymentReqs.payreq_date_topay <> None). \
                         filter(JistPaymentReqs.payreq_date_topay <> '0000-00-00'). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentalldatetotal: paymentalldatetotal = 0
        totalpayments = format_decimal(paymentalldatetotal, format='#,##0.00;-#0.00',locale='en')
        sitedata = """
                <h2 class="ui-widget-header paymentheader">All Payments To Be Done Total: 
                <span style="float:right; margin-right:90px">
                %s
                </span> 
                </h2>
                """%(totalpayments)
        tabledata = """
                   <table class='tableinvoicelist'>
                    <th>ID </th>
                    <th>Date </th>
                    <th>PO Number</th>
                    <th>Payee</th>
                    <th>Description</th>
                    <th>Total Incl</th>
                    <th>Must Pay Date</th>
                    <th>Added By</th>
                    <th>Approved</th>
                    <th>Approved By</th>
                    <th>Approved Date</th>
                    """
        footerdata = "</table>"
        for payment in paymentreqsdate:
            if payment[0]: 
                paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                             filter(JistPaymentReqs.payreq_date_topay==payment[0]). \
                             filter(JistPaymentReqs.payreq_paid==0). \
                             filter(JistPaymentReqs.payreq_approved_bln==1). \
                             order_by(desc(JistPaymentReqs.id)). \
                             all()
                paymentreqtotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                                 filter(JistPaymentReqs.payreq_date_topay==payment[0]). \
                                 filter(JistPaymentReqs.payreq_paid==0). \
                                 filter(JistPaymentReqs.payreq_approved_bln==1). \
                                 value(func.sum(JistPaymentReqs.payreq_total_incl))
                if not paymentreqtotal: paymentreqtotal = 0
                totalpayment = format_decimal(paymentreqtotal, format='#,##0.00;-#0.00',locale='en')
                htmlheader = """
                            <h2 class="ui-widget-header paymentheader">Payments To Be
                            Done:  %s 
                            <span style="float:right; margin-right:90px">
                            <img class="paymentreq_paid" value="%s" src="/images/prices_32.png" title="Mark as Paid"></img>
                            <a href='/accountscont/export_payment_topay_bydate/%s'> 
                            <img src="/images/pdficon.jpg"></img>
                            </a>
                            %s
                            </span> 
                            </h2>
                            """%(payment[0],payment[0],payment[0],totalpayment)
                sitedata = sitedata +tabledata+ htmlheader
                for k in paymentreqs:
                    payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
                    useradded = User.by_user_id(k.useridnew)
                    userapproved = User.by_user_id(k.userid_approved)
                    userreqby = User.by_user_id(k.payreq_by)
                    if not k.payreq_total_incl: k.payreq_total_incl = 0
                    totalpayment = format_decimal(k.payreq_total_incl, format='#,##0.00;-#0.00',locale='en')
                    sitedatatemp = """
                                    <tr>
                                    <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td align='right'>%s </td>
                                    <td align='right'>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td>  
                                    <p/>
                                    </tr>
                                    """ % (k.id,
                                            k.payreq_date,
                                            k.payreq_ponumber,
                                            payee.payee_name,
                                            k.payreq_description,
                                            totalpayment,
                                            k.payreq_must_pay_date,
                                            useradded.user_name,
                                            k.payreq_approved_bln,
                                            userapproved.user_name,
                                            k.payreq_approved_date
                                           )
                    sitedata = sitedata + sitedatatemp
                sitedata = sitedata +footerdata + "</p>"
        #sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def do_search_paymentreqs_paid(self, **kw):
        try:
            datestart = kw['startdate']
            dateend = kw['enddate']
        except:
            datestart = None
            dateend = None

        if not datestart:
            todaydate = datetime.date(datetime.now()) 
            datestart = datetime.date(datetime.now()) - timedelta(weeks=10)
            dateend = datetime.date(datetime.now()) 
        if not dateend:
            dateend = datetime.date(datetime.now()) 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        paymentreqsdate = DBS_JistInvoicing.query(func.distinct(JistPaymentReqs.payreq_date_paid)). \
                     filter(JistPaymentReqs.payreq_paid==1). \
                     filter(JistPaymentReqs.payreq_approved_bln==1). \
                     filter(JistPaymentReqs.payreq_date_paid>=datestart). \
                     filter(JistPaymentReqs.payreq_date_paid<=dateend). \
                     order_by(desc(JistPaymentReqs.payreq_date_paid)). \
                     all()
        paymentalldatetotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_paid==1). \
                         filter(JistPaymentReqs.payreq_approved_bln==1). \
                         filter(JistPaymentReqs.payreq_date_paid !=  None). \
                         filter(JistPaymentReqs.payreq_date_paid>=datestart). \
                         filter(JistPaymentReqs.payreq_date_paid<=dateend). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentalldatetotal: paymentalldatetotal = 0
        totalpayments = format_decimal(paymentalldatetotal, format='#,##0.00;-#0.00',locale='en')
        sitedata = """
                <h2 class="ui-widget-header paymentheader">Payments Done From: %s To: %s 
                <span style="float:right; margin-right:90px">
                %s
                </span> 
                </h2>
                """%(datestart,dateend,totalpayments)
        tabledata = """
                   <table class='tblpaymentlist'>
                    <th>ID </th>
                    <th>Date </th>
                    <th>PO Number</th>
                    <th>Payee</th>
                    <th>Description</th>
                    <th>Total Incl</th>
                    <th>Must Pay Date</th>
                    <th>Active</th>
                    <th>Added By</th>
                    <th>Approved</th>
                    <th>Approved By</th>
                    <th>Approved Date</th>
                    <th>Un-Pay</th>
                    """
        footerdata = "</table>"
        for payment in paymentreqsdate:
            if payment[0]: 
                paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                            filter(JistPaymentReqs.payreq_date_paid==payment[0]). \
                             filter(JistPaymentReqs.payreq_paid==1). \
                             filter(JistPaymentReqs.payreq_approved_bln==1). \
                             order_by(desc(JistPaymentReqs.id)). \
                             all()
                paymentreqtotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                                 filter(JistPaymentReqs.payreq_date_paid==payment[0]). \
                                 filter(JistPaymentReqs.payreq_paid==1). \
                                 filter(JistPaymentReqs.payreq_approved_bln==1). \
                                 value(func.sum(JistPaymentReqs.payreq_total_incl))
                totalpayment = format_decimal(paymentreqtotal, format='#,##0.00;-#0.00',locale='en')
                htmlheader = """
                            <h2 class="ui-widget-header paymentheader">Payments Done:  %s 
                            <span style="float:right; margin-right:90px">
                            <a href='/accountscont/export_payment_complete_bydate/%s'> 
                            <img src="/images/pdficon.jpg"></img></a>
                            %s
                            </span> 
                            </h2>
                            """%(payment[0],payment[0],totalpayment)
                sitedata = sitedata +tabledata+ htmlheader
                for k in paymentreqs:
                    if not k.payreq_total_incl: k.payreq_total_incl = 0
                    totalpayment = format_decimal(k.payreq_total_incl, format='#,##0.00;-#0.00',locale='en')
                    payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
                    useradded = User.by_user_id(k.useridnew)
                    userapproved = User.by_user_id(k.userid_approved)
                    userreqby = User.by_user_id(k.payreq_by)

                    sitedatatemp = """
                                    <tr>
                                    <td>%s </td> <td>%s </td> <td>%s </td> <td align='left'>%s </td> <td>%s </td> <td align='right'>%s </td>
                                    <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td>
                                    <td width="25px" ><img class="unpay_pay_req" src="/images/Edit-16.png"></img></td>
                                    <p/>
                                    </tr>
                                    """ % (k.id,k.payreq_date,
                                            k.payreq_ponumber,
                                            payee.payee_name,
                                            k.payreq_description,
                                            totalpayment,
                                            k.payreq_must_pay_date,
                                            k.payreq_active,
                                            useradded.user_name,
                                            k.payreq_approved_bln,
                                            userapproved.user_name,
                                            k.payreq_approved_date,
                                           )
                    sitedata = sitedata + sitedatatemp
                sitedata = sitedata +footerdata + "</p>"
        #sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def export_payment_topay_bydate(self,vardate, **kw):
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
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                    filter(JistPaymentReqs.payreq_date_topay==vardate). \
                     filter(JistPaymentReqs.payreq_paid==0). \
                     filter(JistPaymentReqs.payreq_approved_bln==1). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        paymentreqtotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_date_topay==vardate). \
                         filter(JistPaymentReqs.payreq_paid==0). \
                         filter(JistPaymentReqs.payreq_approved_bln==1). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentreqtotal: paymentreqtotal = 0
        totalpayment = format_decimal(paymentreqtotal, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in paymentreqs:
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            useradded = User.by_user_id(k.useridnew)
            userapproved = User.by_user_id(k.userid_approved)
            userreqby = User.by_user_id(k.payreq_by)
            print k.payreq_by
            wip1.append({ 'id':k.id,
                          'req_date':k.payreq_date,
                            'po_number': k.payreq_ponumber,
                            'name': payee.payee_name,
                            'req_by':userreqby.user_name,
                            'jcno':k.payreq_jcno,
                            'req_number':k.payreq_purchasereq_number,
                            'description':k.payreq_description,
                            'unit':k.payreq_unit,
                            'qty':k.payreq_qty,
                            'rate':k.payreq_rate,
                            'totalexcl':k.payreq_total_excl,
                            'vat':k.payreq_total_vat,
                            'totalincl':k.payreq_total_incl,
                            'must_pay':k.payreq_must_pay_date,
                            'active':k.payreq_active,
                            'useridnew':useradded.user_name,
                            'useridedited':k.useridedited,
                            'approved':k.payreq_approved_bln,
                            'userid_approved':userapproved.user_name,
                            'approved_date':k.payreq_approved_date,
                            'req_date_paid':k.payreq_date_paid,
                         })
        count = len(wip1) 
        #outinvoices_total = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Provisional Outstanding Payments For "+ vardate,
                  vardate      ])
        headers =["Payment ID","Req Date","Payee","Approved Date","Next Date","Total Including"]
        headerwidths=[80,80,250,80,80,120]
        pdffile.CreatePDFPaymentsToPayByDate(userdata,wip1,headers,headerwidths,totalpayment)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_payment_complete_bydate(self,vardate, **kw):
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
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                    filter(JistPaymentReqs.payreq_date_paid==vardate). \
                     filter(JistPaymentReqs.payreq_paid==1). \
                     filter(JistPaymentReqs.payreq_approved_bln==1). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        paymentreqtotal = DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_date_paid==vardate). \
                         filter(JistPaymentReqs.payreq_paid==1). \
                         filter(JistPaymentReqs.payreq_approved_bln==1). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentreqtotal: paymentreqtotal = 0
        totalpayment = format_decimal(paymentreqtotal, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in paymentreqs:
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            wip1.append({ 'id':k.id,
                          'req_date':k.payreq_date,
                            'po_number': k.payreq_ponumber,
                            'name': payee.payee_name,
                            'req_by':k.payreq_by,
                            'jcno':k.payreq_jcno,
                            'req_number':k.payreq_purchasereq_number,
                            'description':k.payreq_description,
                            'unit':k.payreq_unit,
                            'qty':k.payreq_qty,
                            'rate':k.payreq_rate,
                            'totalexcl':k.payreq_total_excl,
                            'vat':k.payreq_total_vat,
                            'totalincl':k.payreq_total_incl,
                            'must_pay':k.payreq_must_pay_date,
                            'active':k.payreq_active,
                            'useridnew':k.useridnew,
                            'useridedited':k.useridedited,
                            'approved':k.payreq_approved_bln,
                            'userid_approved':k.userid_approved,
                            'approved_date':k.payreq_approved_date,
                            'req_date_paid':k.payreq_date_paid,
                         })
        count = len(wip1) 
        #outinvoices_total = format_decimal(invoices_total_incl,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
            "Completed Payments For "+ vardate,
                  vardate      ])
        headers =["Payment ID","Req Date","Payee","Date Paid","Total Including"]
        headerwidths=[80,80,250,80,120]
        pdffile.CreatePDFPaymentsPaidByDate(userdata,wip1,headers,headerwidths,totalpayment)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_payment_notapproved(self, **kw):
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
        userdata = []
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.payreq_approved_bln==0). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        paymentreqtotal= DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_approved_bln==0). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentreqtotal: paymentreqtotal = 0
        totalpayment = format_decimal(paymentreqtotal, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in paymentreqs:
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            wip1.append({ 'id':k.id,
                          'req_date':k.payreq_date,
                            'po_number': k.payreq_ponumber,
                            'name': payee.payee_name,
                            'req_by':k.payreq_by,
                            'jcno':k.payreq_jcno,
                            'req_number':k.payreq_purchasereq_number,
                            'description':k.payreq_description,
                            'unit':k.payreq_unit,
                            'qty':k.payreq_qty,
                            'rate':k.payreq_rate,
                            'totalexcl':k.payreq_total_excl,
                            'vat':k.payreq_total_vat,
                            'totalincl':k.payreq_total_incl,
                            'must_pay':k.payreq_must_pay_date,
                            'active':k.payreq_active,
                            'useridnew':k.useridnew,
                            'useridedited':k.useridedited,
                            'approved':k.payreq_approved_bln,
                            'userid_approved':k.userid_approved,
                            'approved_date':k.payreq_approved_date,
                            'req_date_paid':k.payreq_date_paid,
                         })
        count = len(wip1) 
        userdata.append([datetime.date(datetime.now()),
            "Payments Not Approved",
                        ])
        headers =["Payment ID","Req Date","Payee","","Total Including"]
        headerwidths=[80,80,250,80,120]
        pdffile.CreatePDFPaymentsPaidByDate(userdata,wip1,headers,headerwidths,totalpayment)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_payment_approved_unpaid(self, **kw):
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
        userdata = []
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.payreq_approved_bln==1). \
                         filter(JistPaymentReqs.payreq_paid==0). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        paymentreqtotal= DBS_JistInvoicing.query(JistPaymentReqs). \
                         filter(JistPaymentReqs.payreq_approved_bln==1). \
                         filter(JistPaymentReqs.payreq_paid==0). \
                         value(func.sum(JistPaymentReqs.payreq_total_incl))
        if not paymentreqtotal: paymentreqtotal = 0
        totalpayment = format_decimal(paymentreqtotal, format='#,##0.00;-#0.00',locale='en')
        totalamount = 0
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        for k in paymentreqs:
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            wip1.append({ 'id':k.id,
                          'req_date':k.payreq_date,
                            'po_number': k.payreq_ponumber,
                            'name': payee.payee_name,
                            'req_by':k.payreq_by,
                            'jcno':k.payreq_jcno,
                            'req_number':k.payreq_purchasereq_number,
                            'description':k.payreq_description,
                            'unit':k.payreq_unit,
                            'qty':k.payreq_qty,
                            'rate':k.payreq_rate,
                            'totalexcl':k.payreq_total_excl,
                            'vat':k.payreq_total_vat,
                            'totalincl':k.payreq_total_incl,
                            'must_pay':k.payreq_must_pay_date,
                            'active':k.payreq_active,
                            'useridnew':k.useridnew,
                            'useridedited':k.useridedited,
                            'approved':k.payreq_approved_bln,
                            'userid_approved':k.userid_approved,
                            'approved_date':k.payreq_approved_date,
                            'req_date_paid':k.payreq_date_paid,
                         })
        count = len(wip1) 
        userdata.append([datetime.date(datetime.now()),
            "Payments Approved Not Paid",
                        ])
        headers =["Payment ID","Req Date","Payee","Next Payment","Total Including"]
        headerwidths=[80,80,250,80,120]
        pdffile.CreatePDFPaymentsPaidByDate(userdata,wip1,headers,headerwidths,totalpayment)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def toggle_payreq_approved(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='accountsmanage':
                logged = True
        if not logged: return "Only for the Accounts Manager"
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.id==kw["payreqid"]). \
                     one()
        #print paymentreqs             
        if not paymentreqs.payreq_approved_bln: 
            paymentreqs.payreq_approved_date = datetime.date(datetime.now())
        else:
            paymentreqs.payreq_approved_date = None 

        paymentreqs.payreq_approved_bln = not paymentreqs.payreq_approved_bln
        paymentreqs.userid_approved = usernow.user_id 

    @expose()
    def do_split_payment_req_unapproved(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='accounts':
                logged = True
        if not logged: return "Only for the Accounts People"
        reqold = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.id==kw["payreqid"]). \
                     one()
        reqnew = JistPaymentReqs()
        reqnew.payreq_date = reqold.payreq_date 
        reqnew.payreq_ponumber = reqold.payreq_ponumber 
        reqnew.payreq_payee= reqold.payreq_payee
        reqnew.payreq_by= reqold.payreq_by
        reqnew.payreq_jcno= reqold.payreq_jcno
        reqnew.payreq_purchasereq_number= reqold.payreq_purchasereq_number
        strbetween = " -"
        newstring = "Split Payment - Original Total: %s"%kw["split_req_total_incl"]
        reqnew.payreq_description= strbetween.join((reqold.payreq_description,newstring))
        reqnew.payreq_unit= reqold.payreq_unit
        reqnew.payreq_qty= reqold.payreq_qty
        reqnew.payreq_rate= reqold.payreq_rate
        #reqnew.payreq_total_excl= reqold.payreq_total_excl
        #reqnew.payreq_total_vat= reqold.payreq_total_vat
        reqnew.payreq_total_incl= kw['split_req_total_incl_paynow'] 
        reqnew.payreq_must_pay_date= kw['split_req_must_pay_date'] 
        reqnew.payreq_paid= 0 
        #reqnew.payreq_date_paid= reqold.payreq_paid
        #reqnew.payreq_active= reqold.payreq_active
        reqnew.useridnew= reqold.useridnew
        #reqnew.useridedited= reqold.useridedited
        reqnew.payreq_approved_bln= reqold.payreq_approved_bln
        reqnew.userid_approved= reqold.userid_approved
        reqnew.payreq_approved_date= reqold.payreq_approved_date

        reqold.payreq_total_incl = kw['split_req_total_incl_balance']
        reqold.payreq_description= strbetween.join((reqold.payreq_description,newstring))
        #print reqnew.payreq_date
        #print reqnew

        DBS_JistInvoicing.add(reqnew)
        DBS_JistInvoicing.flush()
 
    @expose()
    def get_new_payment_req(self,**kw):
        thisone = DBS_JistInvoicing.query(JistPaymentPayee). \
                filter(JistPaymentPayee.id == kw['payeeid']).one()
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        payee_list = DBS_JistInvoicing.query(JistPaymentPayee).all()
        pointlist = []
        productionlist = []
        accountslist = []
        percentlist = [x for x in range(101)]
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
        html1 = """
                <form id="pay_req_new_form">
                <fieldset>
                    <label for="pay_req_date">Requisition Date</label>
                    <input type="text" name="pay_req_date" id="pay_req_date" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_ponumber">P.O. Number</label>
                    <input type="text" name="pay_req_ponumber" id="pay_req_ponumber" class="text ui-widget-content ui-corner-all"/><br/>
                   <label for="pay_req_payee">Choose an Existing Payee</label>
                    <input type="text" value="%s" name="pay_req_payee" id="pay_req_payee" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_by">Req By</label>
                        <select name="pay_req_by"  class="text ui-widget-content ui-corner-all">
                        <option id="pay_req_by" value="">Select one...</option>

               """%(thisone.payee_name)
        html2 = ''
        for person in productionlist:
            htmltemp2 = """
                                  <option name="pay_req_by" value="%s">%s</option>
                    """%(person['user_id'],person['user_name'])
            html2 = html2 + htmltemp2 
        html3 = """
                          </div>
                        </select>
                    <br/>
                    <label for="pay_req_jcno">JCNo</label>
                        <select name="pay_req_jcno"  class="text ui-widget-content ui-corner-all">
                        <option name="pay_req_jcno" value="">Select one...</option>
               """
        html4 = ''
        for cont in contracts:
            htmltemp4 ="""
              <option name="pay_req_jcno" value="%s">%s</option>
                     """%(cont.jno,cont.jno)
            html4 = html4 + htmltemp4
        html5 =""" 
                          </div>
                        </select>
                    <br/>
                    <label for="pay_req_description">Description</label>
                    <input type="text" name="pay_req_description" id="pay_req_description" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_unit">Unit</label>
                    <input type="text" name="pay_req_unit" id="pay_req_unit" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_qty">Qty</label>
                    <input type="text" name="pay_req_qty" id="pay_req_qty" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_rate">Rate</label>
                    <input type="text" name="pay_req_rate" id="pay_req_rate" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_total_excl">Total Excl</label>
                    <input type="text" name="pay_req_total_excl" id="pay_req_total_excl" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_total_vat">Total Vat</label>
                    <input type="text" name="pay_req_total_vat" id="pay_req_total_vat" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_total_incl">Total Incl</label>
                    <input type="text" name="pay_req_total_incl" id="pay_req_total_incl" class="text ui-widget-content ui-corner-all"/><br/>
                    <label for="pay_req_must_pay_date">Must Pay Date</label>
                    <input type="text" name="pay_req_must_pay_date" id="pay_req_must_pay_date" class="text ui-widget-content ui-corner-all"/><br/>
                    <!--label for="pay_req_promised_pay_date">Promised Pay Date</label>
                    <input type="text" name="pay_req_promised_pay_date" id="pay_req_promised_pay_date" class="text ui-widget-content ui-corner-all"/><br/-->
                    <button class="ui-state-default ui-corner-all"
                        id="btn_pay_req_new" style="display:block">Add New Payment Requisition</button>
                </fieldset>
                </form>
                """
        return html1 + html2 + html3 + html4 + html5

    @expose()
    def do_save_new_payment_req(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        reqnew = JistPaymentReqs()
        reqnew.payreq_date = kw['pay_req_date'] 
        reqnew.payreq_ponumber = kw['pay_req_ponumber'] 
        reqnew.payreq_payee =  kw['payeeid']  
        reqnew.payreq_by= kw['pay_req_by']
        #reqnew.payreq_jcno= kw['payreq_jcno']
        #reqnew.payreq_purchasereq_number= kw['payreq_purchasereq_number']
        reqnew.payreq_description= kw['pay_req_description']
        reqnew.payreq_unit= kw['pay_req_unit']
        reqnew.payreq_qty= kw['pay_req_qty']
        reqnew.payreq_rate= kw['pay_req_rate']
        reqnew.payreq_total_excl= kw['pay_req_total_excl']
        reqnew.payreq_total_vat= kw['pay_req_total_vat']
        reqnew.payreq_total_incl= kw['pay_req_total_incl'] 
        reqnew.payreq_must_pay_date= kw['pay_req_must_pay_date'] 
        reqnew.payreq_paid= 0 
        #reqnew.payreq_date_paid= kw['payreq_paid']
        #reqnew.payreq_active= kw['payreq_active']
        reqnew.payreq_active= 1 
        reqnew.useridnew= useridcreated 
        reqnew.useridedited=  useridcreated
        #reqnew.payreq_approved_bln= kw['payreq_approved_bln']
        reqnew.userid_approved= 1
        #reqnew.payreq_approved_date= kw['payreq_approved_date']
        #print reqnew.payreq_date
        #print reqnew
        DBS_JistInvoicing.add(reqnew)
        DBS_JistInvoicing.flush()

    @expose()
    def set_req_paymentdate(self,**kw):
        paymentreq = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.id ==kw["payreqid"]). \
                     one()
        paymentreq.payreq_date_topay = kw["payreq_paymentdate"]

    @expose()
    def set_req_paymentpaid(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='accountsmanage':
                logged = True
        if not logged: return "Only for the Accounts Manager People"
        #reqold = DBS_JistInvoicing.query(JistPaymentReqs). \
                     #filter(JistPaymentReqs.id==kw["payreqid"]). \
                     #one()
        paymentreq = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.payreq_date_topay ==kw["payreqdate"]). \
                     all()
        for payment in paymentreq:
            payment.payreq_paid = 1 
            payment.payreq_date_paid = payment.payreq_date_topay 

    @expose()
    def set_req_payment_unpaid(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='accountsmanage':
                logged = True
        if not logged: return "Only for the Accounts Manager People"
        #reqold = DBS_JistInvoicing.query(JistPaymentReqs). \
                     #filter(JistPaymentReqs.id==kw["payreqid"]). \
                     #one()
        paymentreq = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.id ==kw["payreqid"]). \
                     one()
        paymentreq.payreq_paid = 0 
        paymentreq.payreq_date_paid = None 

    @expose()
    def get_edit_paymentreq(self,**kw):
        thisone = DBS_JistInvoicing.query(JistPaymentReqs). \
                filter(JistPaymentReqs.id == kw['payreqid']). \
                one()
        """
        reqnew.payreq_date = kw['pay_req_date'] 
        reqnew.payreq_ponumber = kw['pay_req_ponumber'] 
        reqnew.payreq_payee =  kw['payeeid']  
        reqnew.payreq_by= kw['pay_req_by']
        #reqnew.payreq_jcno= kw['payreq_jcno']
        #reqnew.payreq_purchasereq_number= kw['payreq_purchasereq_number']
        reqnew.payreq_description= kw['pay_req_description']
        reqnew.payreq_unit= kw['pay_req_unit']
        reqnew.payreq_qty= kw['pay_req_qty']
        reqnew.payreq_rate= kw['pay_req_rate']
        reqnew.payreq_total_excl= kw['pay_req_total_excl']
        reqnew.payreq_total_vat= kw['pay_req_total_vat']
        reqnew.payreq_total_incl= kw['pay_req_total_incl'] 
        reqnew.payreq_must_pay_date= kw['pay_req_must_pay_date'] 
        """
        html = """
                <form id ='frm_payreq_edit'>
                <fieldset>
                    <label for="pay_req_id_edit">ID</label>
                    <input type="text" name="pay_req_id_edit" id="pay_req_id_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_date_edit">Date</label>
                    <input type="text" name="pay_req_date_edit" id="pay_req_date_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_ponumber_edit">PO Number</label>
                    <input type="text" name="pay_req_ponumber_edit" id="pay_req_ponumber_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_description_edit">Description</label>
                    <input type="text" name="pay_req_description_edit" id="pay_req_description_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_unit_edit">Unit</label>
                    <input type="text" name="pay_req_unit_edit" id="pay_req_unit_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_qty_edit">Qty</label>
                    <input type="text" name="pay_req_qty_edit" id="pay_req_qty_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_rate_edit">Rate</label>
                    <input type="text" name="pay_req_rate_edit" id="pay_req_rate_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_excl_edit">Excl Amount</label>
                    <input type="text" name="pay_req_excl_edit" id="pay_req_excl_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_vat_edit">Vat Amount</label>
                    <input type="text" name="pay_req_vat_edit" id="pay_req_vat_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_incl_edit">Incl Amount</label>
                    <input type="text" name="pay_req_incl_edit" id="pay_req_incl_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="pay_req_must_pay_edit">Must Pay Date</label>
                    <input type="text" name="pay_req_must_pay_edit" id="pay_req_must_pay_edit" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_do_add_payreq_edit">Edit Payment</button>
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_do_cancel_payreq_edit">Cancel</button>
                </fieldset>
                </form>
               """%(thisone.id,thisone.payreq_date,thisone.payreq_ponumber,
                   thisone.payreq_description,thisone.payreq_unit,
                   thisone.payreq_qty,thisone.payreq_rate,thisone.payreq_total_excl,
                   thisone.payreq_total_vat,thisone.payreq_total_incl,thisone.payreq_must_pay_date)
        return html
        
    @expose()
    def save_edit_payreq(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        thisone = DBS_JistInvoicing.query(JistPaymentReqs). \
                filter(JistPaymentReqs.id == kw['pay_req_id_edit']). \
                one()
        thisone.payreq_date = kw['pay_req_date_edit'] 
        thisone.payreq_ponumber = kw['pay_req_ponumber_edit'] 
        thisone.payreq_description= kw['pay_req_description_edit']
        thisone.payreq_unit= kw['pay_req_unit_edit']
        thisone.payreq_qty= kw['pay_req_qty_edit']
        thisone.payreq_rate= kw['pay_req_rate_edit']
        thisone.payreq_total_excl= kw['pay_req_excl_edit']
        thisone.payreq_total_vat= kw['pay_req_vat_edit']
        thisone.payreq_total_incl= kw['pay_req_incl_edit'] 
        thisone.payreq_must_pay_date= kw['pay_req_must_pay_edit'] 

    @expose()
    def get_edit_payee(self,**kw):
        thisone = DBS_JistInvoicing.query(JistPaymentPayee). \
                filter(JistPaymentPayee.id == kw['payee_id']). \
                one()
        html = """
            <div id="add_new_payee_edit" title="Edit Payee" style="display:block">
                <form id ='frm_new_payee_edit'>
                <fieldset>
                    <label for="payee_editid">ID</label>
                    <input type="text" name="payee_editid" id="payee_editid" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="payee_editname">Name</label>
                    <input type="text" name="payee_editname" id="payee_editname" value = "%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="address1_edit">Address1</label> 
                    <input type="text" name="address1_edit" id="address1_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="address2_edit">Address2</label> 
                    <input type="text" name="address2_edit" id="address2_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="address3_edit">Address3</label>
                    <input type="text" name="address3_edit" id="address3_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="address4_edit">Address4</label> 
                    <input type="text" name="address4_edit" id="address4_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="">VAT No</label> 
                    <input type="text" name="vat_no" id="vat_no" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="bank_edit">Bank</label> 
                    <input type="text" name="bank_edit" id="bank_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="branch_edit">Branch Code</label> 
                    <input type="text" name="branch_edit" id="branch_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="accno_edit">Acc No</label> 
                    <input type="text" name="accno_edit" id="accno_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="contact_edit">Contact</label> 
                    <input type="text" name="contact_edit" id="contact_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="email_edit">Email</label> 
                    <input type="text" name="email_edit" id="email_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="phone_edit">Phone</label> 
                    <input type="text" name="phone_edit" id="phone_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <label for="fax_edit">Fax</label> 
                    <input type="text" name="fax_edit" id="fax_edit" value="%s" class="text ui-widget-content ui-corner-all" />
                    <br/>
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_do_add_payee_edit">Edit Payee</button>
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_do_cancel_new_payee_edit">Cancel</button>
                </fieldset>
                </form>
            </div>
               """%(thisone.id,thisone.payee_name,thisone.payee_add1,thisone.payee_add2,thisone.payee_add3,thisone.payee_add4,thisone.payee_vat_no,
                       thisone.payee_bank,thisone.payee_branch,thisone.payee_accno,thisone.payee_contact,thisone.payee_email,
                       thisone.payee_tel,thisone.payee_fax)
        return html
        
    @expose()
    def save_edit_payee(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        thispayee = kw['payee_editid']
        thisone = DBS_JistInvoicing.query(JistPaymentPayee). \
                filter(JistPaymentPayee.id == kw['payee_editid']). \
                one()
        thisone.payee_name = kw['payee_editname']
        thisone.payee_add1 = kw['address1_edit']
        thisone.payee_add2 = kw['address2_edit']
        thisone.payee_add3 = kw['address3_edit']
        thisone.payee_add4 = kw['address4_edit']
        thisone.payee_vat_no = kw['vat_no']
        thisone.payee_bank = kw['bank_edit']
        thisone.payee_branch = kw['branch_edit']
        thisone.payee_accno = kw['accno_edit']
        thisone.payee_contact = kw['contact_edit']
        thisone.payee_email = kw['email_edit']
        thisone.payee_tel = kw['phone_edit']
        thisone.payee_fax= kw['fax_edit']

    @expose()
    def do_save_new_payee(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        payeenew = JistPaymentPayee()
        payeenew.payee_name = kw['payeename'] 
        payeenew.payee_add1 = kw['address1'] 
        payeenew.payee_add2 = kw['address2'] 
        payeenew.payee_add3 = kw['address3'] 
        payeenew.payee_add4 = kw['address4'] 
        payeenew.payee_vat_no = kw['vat_no'] 
        payeenew.payee_bank = kw['bank'] 
        payeenew.payee_branch = kw['branch'] 
        payeenew.payee_accno = kw['accno'] 
        payeenew.payee_contact = kw['contact'] 
        payeenew.payee_email = kw['email'] 
        payeenew.payee_tel = kw['phone'] 
        payeenew.payee_fax = kw['fax'] 
        DBS_JistInvoicing.add(payeenew)
        DBS_JistInvoicing.flush()

    @expose()
    def get_payees_list(self,**kw):
        html = ''
        html1 = """<table id='get_payee_table' class='table_estdata'>
                   <th> ID</th>
                   <th> Name</th>
                   <th> Add 1</th>
                   <th> Add 2</th>
                   <th> Add 3</th>
                   <th> Add 4</th>
                   <th> Vat No</th>
                   <th> Bank</th>
                   <th> Branch</th>
                   <th> Acc No</th>
                   <th> Contact</th>
                   <th> Email</th>
                   <th> Phone</th>
                   <th> Fax</th>
                   <th> Edit</th>
                   <th> Open</th>
                """
        html3 = """
                            </table>
                """
        if kw['switch']=="All":
            sites = DBS_JistInvoicing.query(JistPaymentPayee). \
                   order_by(desc(JistPaymentPayee.id)).all()
            #sites = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                   #order_by(desc(JistEstimating3yrBuildingSites.id)).all()
            temphtml1 = ""
            html2 = ""
            for scp in sites:
                temphtml1 = """
                <tr> <td> %s </td> <td> %s </td><td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td><td> %s </td>
                            <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                            </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                                    <br/>
                            </td></tr>
                            """%(scp.id,scp.payee_name,scp.payee_add1,scp.payee_add2,scp.payee_add3,scp.payee_add4,scp.payee_vat_no,
                                    scp.payee_bank,scp.payee_branch,scp.payee_accno,scp.payee_contact,scp.payee_email,scp.payee_tel,scp.payee_fax)
                html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        elif kw['switch']=="SearchName":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_JistInvoicing.query(JistPaymentPayee). \
                    filter(JistPaymentPayee.payee_name.like(searchphrase)). \
                   order_by(desc(JistPaymentPayee.id)).all()
            
            temphtml1 = ""
            html2 = ""
            for scp in sites:
                temphtml1 = """
                <tr> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td> <td> %s </td><td> %s </td>
                            <td width="25px" ><img  id="toggle_poitems" src="/images/Edit-16.png">
                            </img></td> <td width="25px" ><img  id="toggle_poitems" src="/images/project-open.png"></img>
                            </td></tr>
                            """%(scp.id,scp.payee_name,scp.payee_add1,scp.payee_add2,scp.payee_add3,scp.payee_add4,scp.payee_vat_no,
                                    scp.payee_bank,scp.payee_branch,scp.payee_accno,scp.payee_contact,scp.payee_email,scp.payee_tel,scp.payee_fax)
                html2 = html2 + temphtml1
            html =  html1 + html2 + html3
            return html
        else:
            return html

    @expose()
    def get_payee_history(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        #sttimestart = time(0,0,0)
        #sttimeend = time(23,59,59)
        #startdate = datetime.combine(today,sttimestart)
        #enddate = datetime.combine(endtoday,sttimeend)
        payeecode = kw['payeeid']
        paymentreqs = DBS_JistInvoicing.query(JistPaymentReqs). \
                     filter(JistPaymentReqs.payreq_payee==payeecode). \
                     order_by(desc(JistPaymentReqs.id)). \
                     all()
        sitedata = "<table class='tableinvoicelist'>"
        headerdata = """
                    <th>ID </th>
                    <th>Date </th>
                    <th>PO Number</th>
                    <th>Payee</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Rate</th>
                    <th>Total Excl</th>
                    <th>Total Vat</th>
                    <th>Total Incl</th>
                    <th>Must Pay Date</th>
                    <th>Paid</th>
                    <th>Date Paid</th>
                    <th>Active</th>
                    <th>Approved</th>
                    <th>Approved By</th>
                    <th>Approved Date</th>
                    """
        sitedata = sitedata + headerdata
        for k in paymentreqs:
            #totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            if k.payreq_by == 0 or k.payreq_by == '': k.payreq_by = 1
            req_by = DBS_ContractData.query(User).filter(User.user_id==k.payreq_by).one()
            req_add = DBS_ContractData.query(User).filter(User.user_id==k.useridnew).one()
            #req_edited = DBS_ContractData.query(User).filter(User.user_id==k.useridedited).one() 
            req_approved = DBS_ContractData.query(User).filter(User.user_id==k.userid_approved).one() 
            payee = DBS_JistInvoicing.query(JistPaymentPayee).filter(JistPaymentPayee.id==k.payreq_payee).one() 
            sitedatatemp = """
                            <tr>
                            <td>%s </td> <td>%s </td> <td>%s </td> <td align='left'>%s </td> <td>%s </td> <td>%s </td> <td>%s </td>
                            <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td> <td>%s </td>
                            <td>%s </td> <td>%s </td> <td>%s </td> 
                            </tr>
                            """ % (k.id,k.payreq_date,
                                    k.payreq_ponumber,
                                    payee.payee_name,
                                    k.payreq_description,
                                    k.payreq_unit,
                                    k.payreq_qty,
                                    k.payreq_rate,
                                    k.payreq_total_excl,
                                    k.payreq_total_vat,
                                    k.payreq_total_incl,
                                    k.payreq_must_pay_date,
                                    k.payreq_paid,
                                    k.payreq_date_paid,
                                    k.payreq_active,
                                    k.payreq_approved_bln,
                                    req_approved.user_name,
                                    k.payreq_approved_date,
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

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
                     value(func.sum(JistInvoicesList.value_excl))
        locale.setlocale(locale.LC_ALL, '')

        #print invoices_total
        #return
        if invoices_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        invoice_text = "<H3 align='left'> Invoices For Period From: %s To  %s</H3><p/>"%(datestart,dateend)
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/accountscont/export_invoice_dates_pdf/%s/%s'><p/> 
                        <img src="/images/pdficon.jpg"></img></a>
                   """%(startdate,enddate)
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
                            <a href='/accountscont/invoice_one/%s'>%s
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
        #print filename
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
                     value(func.sum(JistInvoicesList.value_excl))
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
            totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            #totalin = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            #contract = DBS_ContractData.query(JistContracts).get(k.contract)
            #statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            #point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            #user_name = point.user_name
            #invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
            #              filter(JistInvoicesPayments.invoiceid==k.id). \
            #              all()
            #pdate = ""
            #pmount = 0
            #pamount = 0
            #balance = 0
            #bal = 0
            #for p in invoice_payments:
            #    #print p.paymentdate, p.amount
            #    pdate = pdate + str(p.paymentdate)
            #    pmount = pmount + p.amount
            #pamount = format_decimal(pmount,format='#,##0.00;-#0.00',locale='en')
            #bal = k.value_incl - pmount
            #totalbal = totalbal + bal
            #inbalance = format_decimal(bal,format='#,##0.00;-#0.00',locale='en')
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
            "Invoices From %s To %s"%(startdate,enddate),
                        ""
                        ])
        headers =["Inv No","Date","Client","Total Excl","JCNo","Site Name","Point Person"]
        headerwidths=[70,70,120,70,70,100,100]
        pdffile.CreatePDFInvoicesTime(userdata,wip1,headers,headerwidths,outinvoices_total)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose('jistdocstore.templates.accounts.search_invoices_clients_date')
    def search_invoices_clients_date(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=InvoiceDateClientComboSearch(),
                    target="output",
                    action="do_search_invoices_clients_dates")

        tmpl_context.form = ajax_form 

        return dict(page='clientdatesearch',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_invoices_clients_dates(self, **kw):
        if not kw['startdate']:
            year = str(0)
        else:
            for k,w in kw.iteritems():
                if k == "startdate":
                    year =w.split('-')[0]
                    month =w.split('-')[1]
                    day =w.split('-')[2]
        if not kw['enddate']:
            endyear = str(0)
        else :
            for k,w in kw.iteritems():
                if k == "enddate":
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
                      filter(JistInvoicesList.client==kw['client_name']). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.client==kw['client_name']). \
                      filter(JistInvoicesList.invdate>=startdate). \
                      filter(JistInvoicesList.invdate<=enddate). \
                     value(func.sum(JistInvoicesList.value_excl))

        locale.setlocale(locale.LC_ALL, '')
        if invoices_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        invoice_text = """<H3 align='left'> 
                            Invoices for period from: %s to  %s for %s
                            </H3><p/>
                            """%(datestart,dateend,kw['client_name'])
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/accountscont/export_invoice_clients_dates_pdf/%s/%s/%s'><p/> 
                        <img src="/images/pdficon.jpg"></img></a>
                   """%(startdate,enddate,kw['client_name'])
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
                            <a href='/accountscont/invoice_one/%s'>%s
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
                     value(func.sum(JistInvoicesList.value_excl))
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
            totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            contract = DBS_ContractData.query(JistContracts).get(k.contract)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            #totalin = format_decimal(k.value_incl,format='#,##0.00;-#0.00',locale='en')
            #contract = DBS_ContractData.query(JistContracts).get(k.contract)
            #statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.contract).one()
            #point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            #user_name = point.user_name
            #invoice_payments = DBS_JistInvoicing.query(JistInvoicesPayments). \
            #              filter(JistInvoicesPayments.invoiceid==k.id). \
            #              all()
            #pdate = ""
            #pmount = 0
            #pamount = 0
            #balance = 0
            #bal = 0
            #for p in invoice_payments:
            #    #print p.paymentdate, p.amount
            #    pdate = pdate + str(p.paymentdate)
            #    pmount = pmount + p.amount
            #pamount = format_decimal(pmount,format='#,##0.00;-#0.00',locale='en')
            #bal = k.value_incl - pmount
            #totalbal = totalbal + bal
            #inbalance = format_decimal(bal,format='#,##0.00;-#0.00',locale='en')
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
        headers =["Inv No","Date","Client","Total Excl","JCNo","Site Name","Point Person"]
        headerwidths=[70,70,120,70,70,100,100]
        pdffile.CreatePDFInvoicesClientsTime(userdata,wip1,headers,headerwidths,outinvoices_total)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose('jistdocstore.templates.accounts.search_invoices_contracts')
    def search_invoices_contracts(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=InvoiceContractSearch(),
                    target="output",
                    action="do_search_invoices_contracts")

        tmpl_context.form = ajax_form 

        return dict(page='contract search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
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
                        href='/accountscont/export_invoice_contracts_pdf/%s'><p/> 
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
                            <a href='/accountscont/invoice_one/%s'>%s
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

    @expose('jistdocstore.templates.accounts.search_invoices_payment_time')
    def search_invoices_payment_time(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=InvoicesPaymentTime(),
                    target="output",
                    action="do_search_invoices_payment_time")

        tmpl_context.form = ajax_form 

        return dict(page='contract search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
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
                        href='/accountscont/export_invoice_payment_time_pdf/%s/%s'> 
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
                            <a href='/accountscont/invoice_payment_edit/%s'>%s
                            </a>
                            <td>
                            <a href='/accountscont/invoice_one/%s'>%s
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

    @expose('jistdocstore.templates.accounts.search_invoices_unpaid')
    def search_invoices_unpaid(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=InvoicesUnpaid(),
                    target="output",
                    action="do_search_invoices_unpaid")

        tmpl_context.form = ajax_form 

        return dict(page='Unpaid Invoices',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
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
                        href='/accountscont/export_invoices_unpaid'> 
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
                            <a href='/accountscont/invoice_one/%s'>%s
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

    @expose('jistdocstore.templates.accounts.search_invoices_balances')
    def search_invoices_balances(self,**named):
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
        wip = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()

        return dict(page='Different Invoices Views',
                    points = pointlist,
                    wip = wip,
                    )

    @expose()
    #@validate(ajax_form)
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
                        href='/accountscont/export_invoices_balance'> 
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
                                <a href='/accountscont/invoice_one/%s'>%s
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
            if diff <> 0: 
                wip1.append({'invnumber':k.invoiceno,
                              'invdate':k.invdate,
                              'client':k.client,
                              'site':contract.site,
                              'totalexcl':k.value_incl,
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

    @expose('jistdocstore.templates.accounts.search_invoices_vs_payment_time')
    def search_invoices_vs_payments_time(self,**named):
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=InvoicesPaymentTime(),
                    target="output",
                    action="do_search_invoices_vs_payment_time")

        tmpl_context.form = ajax_form 

        return dict(page='invoices vs payments search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

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
                    href='/accountscont/export_invoice_vs_payments_pdf/%s/%s'><p/> 
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
                            <a href='/accountscont/invoice_one/%s'>%s
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

    @expose('jistdocstore.templates.accounts.payment_new')
    def invoice_payment_new(self,**named):
        tmpl_context.form = add_new_inv_payment 
        #val = edit_inv_payment_form_filler.get_value(values={'id':830})
        #tmpl_context.form = edit_Inv_Payment_form 
        return dict(page='New Uer',
                    wip = '',
                    currentPage=1,
                    value2=named)

    @expose('jistdocstore.templates.accounts.payment_edit')
    def invoice_payment_edit(self,*arg,**named):
        #tmpl_context.form = add_new_inv_payment 
        val = edit_inv_payment_form_filler.get_value(values={'id':arg[0]})
        tmpl_context.form = edit_Inv_Payment_form 
        return dict(page='Invoice Payment Edit',
                    wip = '',
                    currentPage=1,
                    value=val,
                    value2=named)

    @expose('jistdocstore.templates.accounts.view_balance_completion')
    def view_invoices_balance_completion(self,*arg,**named):
        import random
        wip1 = []
        userdata = []
        contractbalance = 0
        invoices_total_incl = 0
        wip_contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=='False').all()
        for contr in wip_contracts:
            jcnoint = int(contr.jno)
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==contr.jno).one()
            statusprop = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==contr.jno). \
                         value(func.sum(JistInvoicesList.value_excl))
            contract_total = DBS_ContractData.query(JistContractOrderItems). \
                          filter(JistContractOrderItems.jno==contr.jno). \
                         value(func.sum(JistContractOrderItems.total))
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            if not invoices_total_excl:
                invoices_total_excl = 0
            if not contract_total:
                contract_total = 0
            locale.setlocale(locale.LC_ALL, '')
            contractb = contract_total - invoices_total_excl
            inclamount = float(contractb) * float(1.14)
            contractbalance_excl = format_decimal(contractb,format='#,##0.00;-#0.00',locale='en')
            contractbalance_incl = format_decimal(inclamount,format='#,##0.00;-#0.00',locale='en')
            contract_total = format_decimal(contract_total,format='#,##0.00;-#0.00',locale='en')
            invoices_total_excl = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
            wip1.append({
                          'jcno':contr.jno,
                          'client':contr.client,
                          'site':contr.site,
                          'contr_value_excl':contract_total,
                          'inv_totalexcl':invoices_total_excl,
                          'contr_balance_excl': contractbalance_excl,
                          'contr_balance_incl': contractbalance_incl,
                          'point':user_name,
                          'status':statusprop.status,
                         })
            from tg.decorators import paginate
            count = len(wip1) 
            page =int( named.get( 'page', '1' ))
            currentPage = paginate.Page(
                wip1, page, item_count=count,
                items_per_page=5,
            )
            items = currentPage.items
        tmpl_context.form = jcno_wip_list_box 
        return dict(page='Contract-Invoicing-Items-Balances Views',
                    wip = items,
                    selfname = 'view_invoices_balance_completion',
                    thiscurrentPage=currentPage,
                    value2='',
                    action='/accountscont/invoices_pipe')

    @expose()
    def invoices_pipe(self,**kw):
        redirect("/accountscont/view_invoices_items_balances/"+kw['site'])

    @expose('jistdocstore.templates.accounts.view_item_invoice_balances')
    def view_invoices_items_balances(self,jno,**named):
        locale.setlocale(locale.LC_ALL, '')
        import random
        wip1 = []
        userdata = []
        contractbalance = 0
        invoices_total_incl = 0
        contr = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno).one()
        #for contr in wip_contracts:
        #jcnoint = int(contr.jno)
        statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==contr.jno).one()
        statusprop = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
        #invoices = DBS_JistInvoicing.query(JistInvoicesList). \
        #              filter(JistInvoicesList.blnpayed==N).all()
        #if statusprop.id > 5: print statusprop.status
        #print invoices
        #invoices = DBS_JistInvoicing.query(JistInvoicesList).filter(JistInvoicesList.contract==jcnoint).all()
        invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==contr.jno). \
                     value(func.sum(JistInvoicesList.value_excl))
        contract_total = DBS_ContractData.query(JistContractOrderItems). \
                      filter(JistContractOrderItems.jno==contr.jno). \
                     value(func.sum(JistContractOrderItems.total))
        #print invoices_total_excl
        #contract = DBS_ContractData.query(JistContracts).get(k.contract)
        point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
        user_name = point.user_name
        if not invoices_total_excl:
            invoices_total_excl = 0
        if not contract_total:
            contract_total = 0
        contractb = contract_total - invoices_total_excl
        inclamount = float(contractb) * float(1.14)
        contractbalance_excl = format_decimal(contractb,format='#,##0.00;-#0.00',locale='en')
        contractbalance_incl = format_decimal(inclamount,format='#,##0.00;-#0.00',locale='en')
        contract_total = format_decimal(contract_total,format='#,##0.00;-#0.00',locale='en')
        invoices_total_excl = format_decimal(invoices_total_excl,format='#,##0.00;-#0.00',locale='en')
        wip1.append({
                      'jcno':contr.jno,
                      'client':contr.client,
                      'site':contr.site,
                      'contr_value_excl':contract_total,
                      'inv_totalexcl':invoices_total_excl,
                      'contr_balance_excl': contractbalance_excl,
                      'contr_balance_incl': contractbalance_incl,
                      'point':user_name,
                      'status':statusprop.status,
                     })
        from tg.decorators import paginate
        count = len(wip1) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            wip1, page, item_count=count,
            items_per_page=5,
        )
        items = currentPage.items
        return dict(page='Contract-Items-Balances Views',
                    wip = items,
                    selfname = 'view_invoices_items_balances',
                    thiscurrentPage=currentPage,
                    value2='')

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
        #flash("New Payment for Inv:%s, successfully saved."%kw['invoiceid'])

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
                                <table class='tableinvoicesitems'>
                                <th>Inv No</th>
                                <th>Date</th>
                                <th>Client</th>
                                <th>Value Excl</th>
                                <th>Value Vat</th>
                                <th>Value Incl</th>
                                <th>Items</th>
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
                        <td>
                            <img src="/images/orderitems.png"
                            onclick="loadXMLDocInvItems(%s)">
                            </img>
                        </td>
                        </tr>
                        """%(scp.id,scp.invdate,scp.client,
                             scp.value_excl,scp.value_vat,scp.value_incl,scp.id)
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
                                <table class='tableinvorderitems'>
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
                scopeitem=str(scp.item),
                scopedescription=scp.description,
                scopeunit=scp.unit,
                scopeqty=scp.qty,
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
                    'jcno':jcno[0],
                    'scopeitem':scopeitem[0],
                    'scopedescription':scopedescription[0],
                    'scopeunit':scopeunit[0],
                    'scopeqty':scopeqty[0],
                    'invidno': invidno,
                    'invqty': invqty,
                                    })
            html1 = """
                                <table class='tableinvorderitems'>
                                <th>JCNo</th>
                                <th>Item</th>
                                <th>Description</th>
                                <th>Unit</th>
                                <th>Qty</th>
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
                        """%(scp['jcno'],scp['scopeitem'],scp['scopedescription'],
                             scp['scopeunit'],scp['scopeqty'])
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
            #invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
            #              filter(JistInvoicesList.contract==jno). \
            #             value(func.sum(JistInvoicesList.value_excl))
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
                                <table class='tableinvoicesitems'>
                                <th>Inv No</th>
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
                        """%(scp.invid,scp.item,scp.description,
                             scp.unit,scp.qty,scp.price,scp.total)
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
        grandtotalinclsum = format_decimal(Decimal(grandincl),format='#,##0.00;-#0.00',locale='en')
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

