# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
#from tg.decorators import paginate

from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import FileStoreProduction
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
from decimal import Decimal
import locale
from datetime import datetime, time, date
import calendar
from babel.numbers import format_currency, format_number, format_decimal
import json

public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')

__all__ = ['ManagementController']


class ManagementController(BaseController):
    """Sample controller-wide authorization"""
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))
    allow_only = Any(
            has_permission('manage'),
            has_permission('productionmanage'),
                     msg=l_('Only for people with the "production manager" permission'))
    def __init__(self):
        self.last_saved_site_rnd = 0
        self.last_saved_scope_rnd = 0
        self.last_saved_bqitem_rnd = 0
        self.last_saved_quoteno = 0
        self.last_saved_scopelist = "" 
        self.last_saved_editscope = "" 
        self.last_saved_budgetcontract = 0 
        self.building_3yr_tender_number = "445Q"
        self.last_saved_item_description = ""
        self.ListCIDBCategories = ['None','GB', 'SQ', 'CE', 'ME']
        self.ListTrueFalse = ['False','True']
        self.ListWorkCategory = ['Fencing - Normal','Fencing - High Security',
                                'Building','Maintenance','Carports',
                                'Manufacturing','CCTV','Supply Only',
                                'Administrative','Software','Network Support' 
                                ]

    @expose()
    def index(self):
        redirect('mngntcont/menu')

    @expose('jistdocstore.templates.management.managementindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Management: Main Menu') 
    
    @expose('jistdocstore.templates.management.managepoints')
    def managepoints(self,**kw):
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
        return dict(page='Point Contracts',
                    points = pointlist,
                    )

    @expose()
    def ajaxgetmanagepoints(self,usrid='1',**kw):
        if not usrid:
            usrid = '1'
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='productionmanage':
                logged = True
        if not logged: return "Only for People with the Production Manager Rights"
        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(usrid)). \
                order_by(desc(JistContracts.jno)). \
                all()
        #for k in wip:
        #    print k
        wip1 = []
        user = User.by_user_id(int(usrid))
        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        for w in wip:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==w.jno).one()
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==w.jno).one()
                planstartdate = conplandates.planstartdate
                planenddate = conplandates.planenddate
                #print planstartdate,planenddate
            except:
                conplandates = 'None'
                planstartdate = 'None' 
                planenddate = 'None' 

            wip1.append({'jno':w.jno,
                         'client':w.client,
                         'site':w.site,
                         'ordernumber':w.orderno,
                         'description':w.description,
                         'status':statcode.status,
                         'pointperson':statusall.pointperson,
                         'planstart':planstartdate,
                         'planend':planenddate,
                         })
        html1 = """


               <h2 class="effect6">
               <span class='spanleft'>Point Contracts for %s </span>
                <span class='spanright'>
                        Last updated: %s 
                        <a href="/mngntcont/exportsinglepointpdf/%s">
                        <img src="/images/pdficon.jpg"></img>
                        </a>

               </span>
               </h2>
                        </p>
                            <table id= 'points_contract_table' class='table_estdata'>
                            <th>JCno</th>
                            <th>Order Number</th>
                            <th>Client</th>
                            <th>Site</th>
                            <th>Description</th>
                            <th>Status</th>
                            <th>Plan Start</th>
                            <th>Plan End</th>
                """%(user.user_name,dt,user.user_id)
        temphtml1 = ""
        html2 = ""
        for scp in wip1:
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
                    <td>
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
                    <td>
                    %s
                    </td>
                    </tr>
                    """%(scp['jno'],scp['ordernumber'],scp['client'],scp['site'],scp['description'],scp['status'],scp['planstart'],scp['planend'])
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def exportsinglepointpdf(self,point):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
        pdffile = CreatePDF(filename)
        userdata = []
        contractdata = []
        try:
            conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
        except:
            conplandates = None

        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==point). \
                order_by(desc(JistContracts.jno)). \
                all()
        wip1 = []
        for w in wip:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==w.jno).one()
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==w.jno).one()
                #print type(conplandates)
                #print conplandates.planstartdate
                #planstart = str(conplandates.planstartdate).split(' ')[0]
                #planend = str(conplandates.planenddate).split(' ')[0],
                planstartdate = conplandates.planstartdate
                planenddate = conplandates.planenddate
            except:
                conplandates = 'None'
                planstartdate = 'None' 
                planenddate = 'None' 

            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            wip1.append({'jno':w.jno,
                         'client':w.client,
                         'site':w.site,
                         'description':w.description,
                         'planstart':planstartdate,
                         'planend':planenddate,
                         'status':statcode.status,
                         'pointperson':statusall.pointperson
                         })
        
        count = len(wip1) 
        pointperson_name = User.by_user_id(point).user_name
        userdata.append([datetime.date(datetime.now()),
                        "Point Contracts For %s"%pointperson_name,
                        ""
                        ])
        headers =["JCNo","Client","Site","Description","Plan Start","Plan End","Status"]
        headerwidths=[40,120,200,200,60,60,80]
        pdffile.CreatePDFPointContracts(userdata,wip1,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose('jistdocstore.templates.management.managesiteagents')
    def managesiteagents(self,usrid=0,**kw):
        if not usrid:
            usrid = '1'
        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.siteagent==usrid). \
                order_by(desc(JistContracts.jno)). \
                all()
        wip1 = []
        tmpl_context.widget = status_siteagent_changer 
        for w in wip:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==w.jno).one()
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            wip1.append({'jno':w.jno,
                         'client':w.client,
                         'site':w.site,
                         'description':w.description,
                         'status':statcode.status,
                         'pointperson':statusall.siteagent
                         })
        
        count = len(wip1) 
        page =int( kw.get( 'page', '1' ))
        currentPage = paginate.Page(
            wip1, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View All Site Agent Contracts Per User',
                    wip = items,
                    thiscurrentPage=currentPage,
                    point = usrid,
                    selfname="managesiteagents",
                    value = usrid,
                    action='/mngntcont/getmanagedsiteagents',
                    count=count)

    @expose()
    def getmanagedsiteagents(self,*args,**kw):
        if not kw['siteagent']:
            point = 1
        else:
            point = kw['siteagent']
        redirect('/mngntcont/managesiteagents/'+str(point))


    @expose('jistdocstore.templates.contracts.contractoverview')
    def contractoverview(self,**kw):
        todaydate = datetime.date(datetime.now()) 
        endtoday = datetime.date(datetime.now())
        endtup = endtoday.timetuple()
        #2year = 104 weeks 4yrs = 208 weeks
        twoyearsago = datetime.date(datetime.now()) - timedelta(weeks=304)
        #print twoyearsago
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        contractscompleted = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="True"). \
                filter(JistContracts.orderdate > twoyearsago). \
               order_by(desc(JistContracts.jno)).all()
        newcontractfields = ['clientname',
                             'sitename',
                             'orderno',
                             'orderdate',
                             'description',
                             'contact',
                             'tel',
                             'fax',
                             'cell',
                             'workcategory',
                             'cidbcategory',
                             'cidbrating',
                             'groupjno',
                             'completed',
                             'pointperson',
                             'siteagent',
                             ]
        editcontractfields = ['editsitejcno',
                              'editsiteclientname',
                             'editsitename',
                             'editsiteorderno',
                             'editsiteorderdate',
                             'editsitedescription',
                             'editsitecontact',
                             'editsitetel',
                             'editsitefax',
                             'editsitecell',
                             'editsiteworkcategory',
                             'editsitecidbcategory',
                             'editsitecidbrating',
                             'editsitegroupjno',
                             'editsitecompleted',
                             'editsitepointperson',
                             'editsiteagent',
                             ]
        addorderitem = ['item',
                             'item_description',
                             'unit',
                             'qty',
                             'price',
                             'total',
                             ]
        editorderitem = ['edit_id',
                            'edit_item',
                             'edit_item_description',
                             'edit_unit',
                             'edit_qty',
                             'edit_price',
                             'edit_total',
                             ]

        return dict(page='Contract Overview',
                    wip = contracts,
                    completed = contractscompleted,
                    currentPage=1,
                    value=kw,
                    newcontractfields = newcontractfields,
                    editcontractfields = editcontractfields,
                    addorderitem=addorderitem,
                    editorderitem=editorderitem,
                    cidbcategories = self.ListCIDBCategories,
                    cidbratings = range(11),
                    trueorfalse = self.ListTrueFalse,
                    workcategories = self.ListWorkCategory,
                    value2=kw
                    )

    @expose()
    def ajaxshowsubconalljcnosummary(self,*arg,**named):
        try:
            if not arg[0]:
                jcno = 500 
            else:
                jcno = arg[0] 
        except:
            jcno = 500 
        jcno = str(jcno)
        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                join(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                filter(JistSubconPaymentRunsList.active==True). \
                order_by(desc(JistSubconPaymentRunsData.paylist_id)). \
                all()
        emps = DBS_JistLabour.query(JistSubconList). \
                all()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        paymentrun = []
        for k in subcondata:
            payrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                    filter(JistSubconPaymentRunsList.id==k.paylist_id). \
                    one()
            totalex = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                    filter(JistSubconPaymentRunsData.paylist_id==k.paylist_id). \
                    filter(JistSubconPaymentRunsData.jcno==jcno). \
                    value(func.sum(JistSubconPaymentRunsData.total_excl))
            emps = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.id==k.sub_id). \
                    one()
            paymentrun.append({'pay_date':payrun.payment_date,
                                'payment_number':payrun.id,
                                'subcon':emps.trading_name,
                                'totalexcl':totalex,
                                
                                })

        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')
        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """

                        <H2 class='effect6'>Subcontractors for %s <br/>Last updated: %s 
                        <a href="/labourcont/export_subcon_jcnoall_summary_pdf/%s">
                        <img src="/images/pdficon.jpg"></img>
                        </a>
                        </H2>
                            <table class='table_estdata'>
                            <th>Payment Date</th>
                            <th>Payment Number</th>
                            <th>Subcon</th>
                            <th align="right">Total Excl</th>
                """%(jcno,dt,jcno)
        temphtml1 = ""
        html2 = ""
        for scp in paymentrun:
            temphtml1 = """
                    <tr>
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
                    </tr>
                    """%(scp['pay_date'],scp['payment_number'],scp['subcon'],scp['totalexcl'])
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxgetcontractbudgetold(self,*arg,**named):
        try:
            if not arg[0]:
                jcno = 500 
            else:
                jcno = arg[0] 
        except:
            jcno = 500 
        jcno = str(jcno)
        """
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')
        """
        budgetlist = []
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.budget_jno==jcno). \
                filter(JistContractBudget.active==True). \
                order_by(desc(JistContractBudget.id)). \
                all()
        for k in budgetdata:
            budgetlist.append({'item':k.budget_item,
                                'description':k.budget_description,
                                'unit':k.budget_unit,
                                'qty':k.budget_qty,
                                'rate':k.price_rate,
                                'rate_material':k.rate_material,
                                'rate_markup':k.rate_markup,
                                'rate_labour':k.rate_labour,
                                'rate_transport':k.rate_transport,
                                'rate_healthsafety':k.rate_healthsafety,
                                'rate_overheads':k.rate_overheads,
                                'rate_specialist':k.rate_specialist,
                                'rate_markup_specialist':k.rate_markup_specialist,
                                'rate_other':k.rate_other,
                                
                                })

        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """
                    <p id="contractheader">

                        Budgets for %s <br/>Last updated: %s 
                        <a href="/labourcont/export_subcon_jcnoall_summary_pdf/%s">
                        <img src="/images/pdficon.jpg"></img>
                        </a>
                        </p>
                            <table class='table_estdata'>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th>Qty</th>
                            <th>Mat Rate</th>
                            <th>Mat Total</th>
                            <th>Mat Markup</th>
                            <th>Mark Total</th>
                            <th>Lab Rate</th>
                            <th>Lab Total</th>
                            <th>Transport Rate</th>
                            <th>Transport Total</th>
                            <th>H&S Rate</th>
                            <th>H&S Total</th>
                            <th>Overhead Rate</th>
                            <th>Overhead Total</th>
                            <th>Specialist Rate</th>
                            <th>Specialist Total</th>
                            <th>Specialist Markup</th>
                            <th>Specialist Mark Total</th>
                            <th>Other Rate</th>
                            <th>Other Total</th>
                """%(jcno,dt,jcno)
        temphtml1 = ""
        html2 = ""
        for scp in budgetlist:
            temphtml2 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['item'],scp['description'],scp['unit'],scp['qty'],
                            scp['rate_material'],
                            int(scp['rate_material']*scp['qty']),
                            scp['rate_markup'],
                            scp['rate_markup']*scp['qty'],
                            scp['rate_labour'],
                            scp['rate_labour']*scp['qty'],
                            scp['rate_transport'],
                            scp['rate_transport']*scp['qty'],
                            scp['rate_healthsafety'],
                            scp['rate_healthsafety']*scp['qty'],
                            scp['rate_overheads'],
                            scp['rate_overheads']*scp['qty'],
                            scp['rate_specialist'],
                            scp['rate_specialist']*scp['qty'],
                            scp['rate_markup_specialist'],
                            scp['rate_markup_specialist']*scp['qty'],
                            scp['rate_other'],
                            scp['rate_other']*scp['qty'],
                            
                            )
            html2 = html2 + temphtml2

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxgetcontractbudgetitems(self,*arg,**named):
        try:
            if not arg[0]:
                jcno = 500 
            else:
                jcno = arg[0] 
        except:
            jcno = 500 
        jcno = str(jcno)
        budgetlist = []
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.budget_jno==jcno). \
                filter(JistContractBudget.active==True). \
                order_by(asc(JistContractBudget.id)). \
                all()
        for k in budgetdata:
            budgetlist.append({'id':k.id,
                                'item':k.budget_item,
                                'description':k.budget_description,
                                'unit':k.budget_unit,
                                'qty':k.budget_qty,
                                'rate':k.price_rate,
                                'rate_material':k.rate_material,
                                'rate_markup':k.rate_markup,
                                'rate_labour':k.rate_labour,
                                'rate_transport':k.rate_transport,
                                'rate_healthsafety':k.rate_healthsafety,
                                'rate_overheads':k.rate_overheads,
                                'rate_specialist':k.rate_specialist,
                                'rate_markup_specialist':k.rate_markup_specialist,
                                'rate_other':k.rate_other,
                                
                                })

        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """ 

               <h4 class="effect6">
               <span class='spanleft'>Budgets for JCNo: %s </span>
                <span class='spanright'>
                               <div id="img_add_budget">
                               <img id="img_toggle_budget_add"
                               src="/images/add.png"></img>
                               </div>
               </span>
               </h4>
                    <br/>
                    <table id="cont_main_budget">
                    <th>ID</th><th>Item</th><th>Description</th><th>Unit</th><th>Qty</th><th>Edit</th><th>Delete</th>
                """%jcno
        for scp in budgetlist:
            temphtml1 = """
                    <tr>
                    <td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td>
                                <td width="35px" ><img id="toggle_item_add"
                                src="/images/Edit-16.png"></img>
                                </td>
                                <td width="35px" ><img id="toggle_item_add"
                                src="/images/trash-16.png"></img>
                                </td>
                    </tr>

                    """%(scp['id'],scp['item'],scp['description'],scp['unit'],scp['qty'])
            html1 = html1 + temphtml1
        html1 =html1 + " </table>"+"<div id='cont_budgets_seperated'></div>"
        return html1

    @expose()
    def ajaxgetcontractbudgetseperated(self,*arg,**named):
        try:
            if not arg[0]:
                budgetid = 500 
            else:
                budgetid = arg[0] 
        except:
            budgetid = 500 
        budgetid = str(budgetid)
        """
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')
        """
        budgetlist = []
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.id==budgetid). \
                one()
        k = budgetdata
        budgetlist.append({'id':k.id,
                            'item':k.budget_item,
                            'description':k.budget_description,
                            'unit':k.budget_unit,
                            'qty':k.budget_qty,
                            'price_rate':k.price_rate,
                            'price_total':k.price_total,
                            'rate_material_percent':k.rate_material_percent,
                            'rate_material':k.rate_material,
                            'rate_markup_percent':k.rate_markup_percent,
                            'rate_markup':k.rate_markup,
                            'rate_labour_percent':k.rate_labour_percent,
                            'rate_labour':k.rate_labour,
                            'rate_transport_percent':k.rate_transport_percent,
                            'rate_transport':k.rate_transport,
                            'rate_healthsafety_percent':k.rate_healthsafety_percent,
                            'rate_healthsafety':k.rate_healthsafety,
                            'rate_overheads_percent':k.rate_overheads_percent,
                            'rate_overheads':k.rate_overheads,
                            'rate_specialist_percent':k.rate_specialist_percent,
                            'rate_specialist':k.rate_specialist,
                            'rate_markup_specialist_percent':k.rate_markup_specialist_percent,
                            'rate_markup_specialist':k.rate_markup_specialist,
                            'rate_other_percent':k.rate_other_percent,
                            'rate_other':k.rate_other,
                            
                            })

        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """ <form id="cont_main_budget_seperated">
                    <p id="contractheader">ID: %s - %s</p>
                        <fieldset>
                """%(budgetdata.id,budgetdata.budget_description)
        for scp in budgetlist:
            temphtml1 = """
                   <label for="%s">%s</label>
                    <input type="text" id="%s" value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  ='item1' value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s" name="%s" class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s" name="%s"  class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s" name="%s"  class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s" name="%s"  class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s"  name="%s" class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s"  name="%s" class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s"  name="%s" class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s"  name="%s" class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label><br/>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    %s
                    <input type="text" id="%s" value="%s"  name="%s" class="ui-widget-content"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text"  value="%s" class="ui-widget-content" disabled="true"></input>
                    <br/>
                   <label for="%s">%s</label>
                    <input type="text"  id="%s" class="ui-widget-content" disabled="true"></input>
                    <input type="text" id="%s"  class="ui-widget-content" disabled="true"></input>
                    <br/>
                    <button id="button_edit_budget" >Save Budget</button>
                    """%(
    "cont_total_budget","Total Budget","cont_total_budget",
        scp['price_rate'],scp['qty'],Decimal(float(scp['price_rate']*scp['qty'])),
    "cont_material_budget","Material Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_material_budget",scp['rate_material_percent']),"cont_material_budget",scp['rate_material'],"cont_material_budget",scp['qty'],scp['rate_material']*scp['qty'],
    "cont_matmarkup_budget","Material Markup Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_matmarkup_budget",scp['rate_markup_percent']),"cont_matmarkup_budget",scp['rate_markup'],"cont_matmarkup_budget",scp['qty'],scp['rate_markup']*scp['qty'],
    "cont_labour_budget","Labour Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_labour_budget",scp['rate_labour_percent']),"cont_labour_budget",scp['rate_labour'],"cont_labour_budget",scp['qty'],scp['rate_labour']*scp['qty'],
    "cont_transport_budget","Transport Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_transport_budget",scp['rate_transport_percent']),"cont_transport_budget",scp['rate_transport'],"cont_transport_budget",scp['qty'],scp['rate_transport']*scp['qty'],
    "cont_healthsafety","Health and Safety Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_healthsafety_budget",scp['rate_healthsafety_percent']),"cont_healthsafety",scp['rate_healthsafety'],"cont_healthsafety",scp['qty'],scp['rate_healthsafety']*scp['qty'],
    "cont_overheads","Overheads Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_overheads_budget",scp['rate_overheads_percent']),"cont_overheads",scp['rate_overheads'],"cont_overheads",scp['qty'],scp['rate_overheads']*scp['qty'],
    "cont_specialist","Specialist Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_specialist_budget",scp['rate_specialist_percent']),"cont_specialist",scp['rate_specialist'],"cont_specialist",scp['qty'],scp['rate_specialist']*scp['qty'],
    "cont_specialist_markup","Specialist Budget Markup",
        scp['price_rate'],self.producehtmlselectsPercent("sel_specialist_markup_budget",scp['rate_markup_specialist_percent']),"cont_specialist_markup",scp['rate_markup_specialist'],"cont_specialist_markup",scp['qty'],scp['rate_markup_specialist']*scp['qty'],
    "cont_other_budet","Other Budget",
        scp['price_rate'],self.producehtmlselectsPercent("sel_other_budget",scp['rate_other_percent']),"cont_other_budget",scp['rate_other'],"cont_other_budget",scp['qty'],scp['rate_other']*scp['qty'],
    "cont_check_budget_percent","Budget Check","cont_check_budget_percent","cont_check_budget_total"
                        )
            html1 = html1 + temphtml1
        html1 =html1 + " </fieldset></form>"
        return html1 
    
    def producehtmlselectsPercent(self,idname,selected_one):
        html2 =""" <select name="%s" id="%s">"""%(idname,idname)
        for k in range(101):
            if k == selected_one:
                html2temp = """
                                <option value="%s" selected>%s</option>
                        """%(k,k)
                html2 = html2 + html2temp
            else:
                html2temp = """
                                <option value="%s">%s</option>
                        """%(k,k)
                html2 = html2 + html2temp

        return html2 +"</select>"

    @expose()
    #@validate(ajax_form)
    def ajax_invoices_per_contract(self,jcno, **kw):
        invoices = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==jcno). \
                     order_by(desc(JistInvoicesList.id)). \
                     all()
        invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                      filter(JistInvoicesList.contract==jcno). \
                     value(func.sum(JistInvoicesList.value_excl))

        contract = DBS_ContractData.query(JistContracts).get(jcno)
        locale.setlocale(locale.LC_ALL, '')
        #print invoices_total
        #return
        if invoices_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
        #datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        #dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        invoice_text = """ 

               <h2 class="effect6">
               <span class='spanleft'>Invoices For Contract: %s - %s - %s - %s</span>
                <span class='spanright'>
               </span>
               </h2>

                            """%(contract.jno,contract.client,contract.site,contract.description)
        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/accountscont/export_invoice_contracts_pdf/%s'><p/> 
                        Export to PDF</a>
                   """%(jcno)
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
            #print k.contract
            totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            contractthis =  DBS_ContractData.query(JistContracts).get(int(k.contract))
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==int(k.contract)).one()
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
                            </tr>
                            """ % (k.id,k.invoiceno,
                                    k.invdate,
                                    k.client,
                                    totalexcl,
                                    k.contract,
                                    contractthis.site,
                                    user_name)
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose('jistdocstore.templates.management.invoicespoints')
    def invoicespoints(self,**kw):
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
        return dict(page='Point Invoices',
                    points = pointlist,
                    )

    @expose()
    #@validate(ajax_form)
    def ajax_invoices_per_point(self,usrid, **kw):
        if not usrid:
            usrid = '1'
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            if permis.permission_name=='productionmanage':
                logged = True
        if not logged: return "Only for People with the Production Manager Rights"
        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(usrid)). \
                order_by(desc(JistContracts.jno)). \
                all()
        user = User.by_user_id(int(usrid))
        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        invoices = []
        for wp in wip:
            invs = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==wp.jno). \
                         order_by(desc(JistInvoicesList.id)). \
                         all()
            invoices_total = DBS_JistInvoicing.query(JistInvoicesList). \
                          filter(JistInvoicesList.contract==wp.jno). \
                         value(func.sum(JistInvoicesList.value_excl))
            if invoices_total is None:
                totalexcl = 0.00
                invoices_total = 0.00
            else:
                totalexcl = format_decimal(invoices_total,format='#,##0.00;-#0.00',locale='en')
            for k in invs:
                invoices.append({"id":k.id,
                        "invoiceno":k.invoiceno,
                        "invdate":k.invdate,
                        "client":k.client,
                        "contract":k.contract,
                        "totalincl":k.value_incl,
                        })
                #print k.value_excl

        #locale.setlocale(locale.LC_ALL, '')
        invoice_text = """ 

               <h2 class="effect6">
               <span class='spanleft'>Invoices For User: %s </span>
                <span class='spanright'>
               </span>
               </h2>
                            """%(user.user_name)

        if invoices_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/accountscont/export_invoice_contracts_pdf/%s'><p/> 
                        Export to PDF</a>
                   """%("")
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

        pdfstuff = ''
        sitedata = "<div><table class='tabletabs'>"
        headerdata = """
                    <th>Invoice Number </th>
                    <th>Invoice Date</th>
                    <th>Client</th>
                    <th>Total Incl</th>
                    <th>JCNo</th>
                    <th>Site Name</th>
                    <th>Point Person</th>
                    <th>Total Paid</th>
                    """
        sitedata = invoice_text+pdfstuff+sitedata + headerdata
        for k in invoices:
            #print k["contract"]
            #print k.contract
            #totalexcl = format_decimal(k.value_excl,format='#,##0.00;-#0.00',locale='en')
            contractthis = DBS_ContractData.query(JistContracts).get(int(k["contract"]))
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==int(k["contract"])).one()
            paymentstotal = DBS_JistInvoicing.query(JistInvoicesPayments). \
                         filter(JistInvoicesPayments.invoiceid==k['id']). \
                         order_by(desc(JistInvoicesPayments.invoiceid)). \
                         value(func.sum(JistInvoicesPayments.amount))
            #if not paymentstotals:
            #    paymentstotals = 0
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            user_name = point.user_name
            if not paymentstotal:
                paymentstotal = 0
            paymentstotal = format_decimal(paymentstotal,format='#,##0.00;-#0.00',locale='en')
            invoicetotal = format_decimal(k["totalincl"],format='#,##0.00;-#0.00',locale='en')
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
                            <td align='right'>%s
                            </td>
                            </tr>
                            """ % (k["id"],k["invoiceno"],
                                    k["invdate"],
                                    k["client"],
                                    invoicetotal,
                                    k["contract"],
                                    contractthis.site,
                                    user_name,
                                    paymentstotal)
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def ajaxeditbudgetitem(self,uniq,budgetid,**kw):
        #print budgetid
        #for k, w in kw.iteritems():
        #    print k, w
        bdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.id==budgetid). \
                one()
        bdata.rate_material_percent = kw['sel_material_budget']
        bdata.rate_material = kw['cont_material_budget']
        bdata.rate_markup_percent = kw['sel_matmarkup_budget']
        bdata.rate_markup = kw['cont_matmarkup_budget']
        bdata.rate_labour_percent = kw['sel_labour_budget']
        bdata.rate_labour = kw['cont_labour_budget']
        bdata.rate_transport_percent = kw['sel_transport_budget']
        bdata.rate_transport = kw['cont_transport_budget']
        bdata.rate_healthsafety_percent = kw['sel_healthsafety_budget']
        bdata.rate_healthsafety = kw['cont_healthsafety']
        bdata.rate_overheads_percent = kw['sel_overheads_budget']
        bdata.rate_overheads = kw['cont_overheads']
        bdata.rate_specialist_percent = kw['sel_specialist_budget']
        bdata.rate_specialist = kw['cont_specialist']
        bdata.rate_markup_specialist_percent = kw['sel_specialist_markup_budget']
        bdata.rate_markup_specialist = kw['cont_specialist_markup']
        bdata.rate_other_percent = kw['sel_other_budget']
        bdata.rate_other = kw['cont_other_budget']

        return 

    @expose()
    def ajaxeditbudgetactive(self,budgetid,state,**kw):
        bdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.id==budgetid). \
                one()
        bdata.active= int(state) 
        return 

    @expose()
    def ajaxeditbudgetdescription(self,uniq,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        bdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.active==True). \
                one()
        bdata.budget_item = kw['budgetitem']
        bdata.budget_description = kw['budgetdescription']
        bdata.budget_unit = kw['budgetunit']
        if kw['budgetqty']:
            bdata.budget_qty = kw['budgetqty']
        if kw['budgetprice']:
            bdata.price_rate = kw['budgetprice']
        if kw['budgettotal']:
            bdata.price_total = kw['budgettotal']
        return

    @expose()
    def ajaxnewbudgetcontract(self,uniq,jcno,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        if self.last_saved_budgetcontract == uniq:
            return
        newcontractbudget = JistContractBudget(budget_item = kw['newbudgetitem'],
                        budget_jno = jcno,
                        budget_description = kw['newbudgetdescription'],
                        budget_unit = kw['newbudgetunit'],
                        budget_qty = kw['newbudgetqty'],
                        price_rate = kw['newbudgetprice'],
                        price_total = kw['newbudgettotal']
                       )
        DBS_ContractData.add(newcontractbudget)
        DBS_ContractData.flush()
        self.last_saved_budgetcontract = uniq
        return

    @expose()
    def ajaxgetproductioncontractbudget(self,*arg,**named):
        try:
            if not arg[0]:
                jcno = 500 
            else:
                jcno = arg[0] 
        except:
            jcno = 500 
        jcno = str(jcno)
        """
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')
        """
        budgetlist = []
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.budget_jno==jcno). \
                filter(JistContractBudget.active==True). \
                order_by(asc(JistContractBudget.id)). \
                all()
        for k in budgetdata:
            budgetlist.append({'id':k.id,
                                'item':k.budget_item,
                                'description':k.budget_description,
                                'unit':k.budget_unit,
                                'qty':k.budget_qty,
                                'rate':k.price_rate,
                                'rate_material':k.rate_material,
                                'rate_markup':k.rate_markup,
                                'rate_labour':k.rate_labour,
                                'rate_transport':k.rate_transport,
                                'rate_healthsafety':k.rate_healthsafety,
                                'rate_overheads':k.rate_overheads,
                                'rate_specialist':k.rate_specialist,
                                'rate_markup_specialist':k.rate_markup_specialist,
                                'rate_other':k.rate_other,
                                
                                })

        thiscontract = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.jno==jcno). \
                one()
        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """

               <h4 class="effect6">
               <span class='spanleft'>Budget Items For JCNo: %s </span>
                <span class='spanright'>
                Site Name: %s
               </span>
               </h4>
                            <table id="production_budget_table" class='table_productionbudget'>
                            <th>ID</th>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th>Qty</th>
                """%(jcno,thiscontract.site)
        temphtml1 = ""
        html2 = ""
        for scp in budgetlist:
            temphtml1 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['id'],scp['item'],scp['description'],scp['unit'],scp['qty'],
                            )
            html2 = html2 + temphtml1

        html3 = """
                            </table>
                            <div id="production_budget_totals"></div>
                """
                            
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxgetbudget_bybudget_id(self,budgetid,**named):
        budgetlist = []
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.id==budgetid). \
                one()
        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.budgetid==budgetid). \
                     all()
        totalmatspent = 0
        for req in reqsitems:
            if req.poitemid:
                poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                        filter(JistBuyingOrderItems.id==req.poitemid). \
                        one()
                totexcl = poitems.totalexcl
                if not totexcl:
                    totexcl = 0
                totalmatspent = totalmatspent + float(totexcl)
        totalmatspent_format = format_decimal(totalmatspent,format='#,##0.00;-#0.00',locale='en')
        k = budgetdata
        budgetlist.append({'id':k.id,
                            'item':k.budget_item,
                            'description':k.budget_description,
                            'unit':k.budget_unit,
                            'qty':k.budget_qty,
                            'rate':k.price_rate,
                            'rate_material':k.rate_material,
                            'rate_markup':k.rate_markup,
                            'rate_labour':k.rate_labour,
                            'rate_transport':k.rate_transport,
                            'rate_healthsafety':k.rate_healthsafety,
                            'rate_overheads':k.rate_overheads,
                            'rate_specialist':k.rate_specialist,
                            'rate_markup_specialist':k.rate_markup_specialist,
                            'rate_other':k.rate_other,
                            
                            })

        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """
                            <span>Budget Description: %s</span>
                            <table id="req_item_budget_table_total" class='table_productionbudget_detail'>
                            <th>Budget</th>
                            <th>Unit</th>
                            <th>Qty</th>
                            <th>Rate</th>
                            <th>Total</th>
                            <th>Spent</th>
                            <th>Balance</th>
                """%budgetlist[0]['description']
        temphtml1 = ""
        html2 = """
            <tr>
                            <td align="left">Material</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
            </tr>
            <tr>
                            <td align="left">Labour</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
            </tr>
            <tr>
                            <td align="left">Transport</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
            </tr>
            <tr>
                            <td align="left">Health & Safety</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
            <tr>
                            <td align="left">Specialist Budget</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
            """%(
               budgetlist[0]['unit'],
               budgetlist[0]['qty'],
               budgetlist[0]['rate_material'],
               format_decimal(budgetlist[0]['rate_material']*budgetlist[0]['qty'],format='#,##0.00;-#0.00',locale='en'),
               totalmatspent_format,
               format_decimal(float(budgetlist[0]['rate_material']*budgetlist[0]['qty'])-totalmatspent,format='#,##0.00;-#0.00',locale='en'),
               budgetlist[0]['unit'],
               budgetlist[0]['qty'],
               budgetlist[0]['rate_labour'],
               format_decimal(budgetlist[0]['rate_labour']*budgetlist[0]['qty'],format='#,##0.00;-#0.00',locale='en'),
               budgetlist[0]['unit'],
               budgetlist[0]['qty'],
               budgetlist[0]['rate_transport'],
               format_decimal(budgetlist[0]['rate_transport']*budgetlist[0]['qty'],format='#,##0.00;-#0.00',locale='en'),
               budgetlist[0]['unit'],
               budgetlist[0]['qty'],
               budgetlist[0]['rate_healthsafety'],
               format_decimal(budgetlist[0]['rate_healthsafety']*budgetlist[0]['qty'],format='#,##0.00;-#0.00',locale='en'),
               budgetlist[0]['unit'],
               budgetlist[0]['qty'],
               budgetlist[0]['rate_specialist'],
               format_decimal(budgetlist[0]['rate_specialist']*budgetlist[0]['qty'],format='#,##0.00;-#0.00',locale='en')
                   )
        html3 = """
                            </table>
                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxgetbudget_byreq_id(self,jcno,reqitemid,**named):
        jcno = int(jcno)
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==reqitemid). \
                     one()
        budgetlist = []
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.id==reqsitem.budgetid). \
                one()
        k = budgetdata
        budgetlist.append({'id':k.id,
                            'item':k.budget_item,
                            'description':k.budget_description,
                            'unit':k.budget_unit,
                            'qty':k.budget_qty,
                            'rate':k.price_rate,
                            'rate_material':k.rate_material,
                            'rate_markup':k.rate_markup,
                            'rate_labour':k.rate_labour,
                            'rate_transport':k.rate_transport,
                            'rate_healthsafety':k.rate_healthsafety,
                            'rate_overheads':k.rate_overheads,
                            'rate_specialist':k.rate_specialist,
                            'rate_markup_specialist':k.rate_markup_specialist,
                            'rate_other':k.rate_other,
                            
                            })

        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """


               <h2 class="effect6">
               <span class='spanleft'>Budgets for JCNo: %s </span>
                <span class='spanright'>
               </span>
               </h2>

                        Budget Item Description: %s <br/> 
                        </a>
                        </p>
                            <table id="req_item_budget_table" class='table_estdata'>
                            <th>ID</th>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th>Qty</th>
                            <th>Mat Rate</th>
                            <th>Mat Total</th>
                """%(jcno,k.budget_description)
        temphtml1 = ""
        html2 = ""
        for scp in budgetlist:
            temphtml1 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['id'],scp['item'],scp['description'],scp['unit'],scp['qty'],
                            scp['rate_material'],
                            float(scp['rate_material']*scp['qty']),
                            )
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def get_all_payment_reqs_per_contract(self,jcno):
        #filter(JistPaymentReqs.payreq_payed==False). \
        paymentreqs_notpaid = DBS_JistInvoicing.query(JistPaymentReqs). \
                      filter(JistPaymentReqs.payreq_jcno==int(jcno)). \
                      filter(JistPaymentReqs.payreq_payed==False). \
                     all()
        paymentreqs_paid = DBS_JistInvoicing.query(JistPaymentReqs). \
                      filter(JistPaymentReqs.payreq_jcno==int(jcno)). \
                      filter(JistPaymentReqs.payreq_payed==True). \
                     all()
        payreqlist_notpaid = []
        payreqlist_paid = []
        for k in paymentreqs_notpaid:
            payreqlist_notpaid.append({'id':k.id,
                                'payreq_date':k.payreq_date,
                                'payreq_ponumber':k.payreq_ponumber,
                                'payreq_payee':k.payreq_payee,
                                'payreq_by':k.payreq_by,
                                'payreq_jcno':k.payreq_jcno,
                                'payreq_purchasereq_number':k.payreq_purchasereq_number    , 
                                'payreq_description':k.payreq_description    , 
                                'payreq_unit': k.payreq_unit          ,
                                'payreq_qty':k.payreq_qty            ,
                                'payreq_rate':k.payreq_rate           ,
                                'payreq_total_excl':k.payreq_total_excl     ,
                                'payreq_total_vat':k.payreq_total_vat      ,
                                'payreq_total_incl':k.payreq_total_incl    , 
                                'payreq_must_pay_date':k.payreq_must_pay_date ,
                                'payreq_promised_pay_date':k.payreq_promised_pay_date      ,
                                'payreq_payed':k.payreq_payed                  ,
                                'payreq_date_paid':k.payreq_date_paid              ,
                                'payreq_active':k.payreq_active               , 
                                'useridnew':k.useridnew                     ,
                                'dateadded':k.dateadded                     ,
                                'dateedited':k.dateedited                    ,
                                'useridedited':k.useridedited                  
                                
                                })

        for k in paymentreqs_paid:
            payreqlist_paid.append({'id':k.id,
                                'payreq_date':k.payreq_date,
                                'payreq_ponumber':k.payreq_ponumber,
                                'payreq_payee':k.payreq_payee,
                                'payreq_by':k.payreq_by,
                                'payreq_jcno':k.payreq_jcno,
                                'payreq_purchasereq_number':k.payreq_purchasereq_number    , 
                                'payreq_description':k.payreq_description    , 
                                'payreq_unit': k.payreq_unit          ,
                                'payreq_qty':k.payreq_qty            ,
                                'payreq_rate':k.payreq_rate           ,
                                'payreq_total_excl':k.payreq_total_excl     ,
                                'payreq_total_vat':k.payreq_total_vat      ,
                                'payreq_total_incl':k.payreq_total_incl    , 
                                'payreq_must_pay_date':k.payreq_must_pay_date ,
                                'payreq_promised_pay_date':k.payreq_promised_pay_date      ,
                                'payreq_payed':k.payreq_payed                  ,
                                'payreq_date_paid':k.payreq_date_paid              ,
                                'payreq_active':k.payreq_active               , 
                                'useridnew':k.useridnew                     ,
                                'dateadded':k.dateadded                     ,
                                'dateedited':k.dateedited                    ,
                                'useridedited':k.useridedited                  
                                
                                })

        dts = datetime.now()
        dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        ##### Start of the not paid section
        html1 = """

                        <p id="contractheader">
                        Payment Requisitions Pending for %s <br/>Last updated: %s 
                        <a
                        href="/labourcont/export_subcon_jcnoall_summary_pdf/%s"
                        style="float:right">
                        <img align="right" src="/images/pdficon.jpg"></img>
                        </a>
                        </p>
                            <table id="production_budget_table" class='table_estdata'>
                            <th>ID</th>
                            <th>Document Date</th>
                            <th>PO Number</th>
                            <th>Payee</th>
                            <th>Requested By</th>
                            <th>JCNo</th>
                            <th>PO Req</th>
                            <th>Description</th>
                            <th>Total Incl</th>
                            <th>Must Pay Date</th>
                            <th>Promised Pay Date</th>
                            <th>Paid</th>
                """%(jcno,dt,jcno)
        temphtml1 = ""
        html2 = ""
        for scp in payreqlist_notpaid:
            temphtml1 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['id'],scp['payreq_date'],scp['payreq_ponumber'],scp['payreq_payee'],scp['payreq_by'],
                            scp['payreq_jcno'],
                            scp['payreq_purchasereq_number'],
                            scp['payreq_description'],
                            scp['payreq_total_incl'],
                            scp['payreq_must_pay_date'],
                            scp['payreq_promised_pay_date'],
                            scp['payreq_payed'],
                            
                            )
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        htmlpending =  html1 + html2 + html3


        ##### Start of the paid section
        html1 = """

                        <p id="contractheader">
                        Payment Requisitions Paid for %s <br/>Last updated: %s 
                        <a
                        href="/labourcont/export_subcon_jcnoall_summary_pdf/%s"
                        style="float:right">
                        <img align="right" src="/images/pdficon.jpg"></img>
                        </a>
                        </p>
                            <table id="production_budget_table" class='table_estdata'>
                            <th>ID</th>
                            <th>Document Date</th>
                            <th>Purchase Order Number</th>
                            <th>Payee</th>
                            <th>Requisted By</th>
                            <th>JCNo</th>
                            <th>Purchase Req Number</th>
                            <th>Description</th>
                            <th>Total Incl</th>
                            <th>Paid</th>
                            <th>Date Paid</th>
                """%(jcno,dt,jcno)
        temphtml1 = ""
        html2 = ""
        for scp in payreqlist_paid:
            temphtml1 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['id'],scp['payreq_date'],scp['payreq_ponumber'],scp['payreq_payee'],scp['payreq_by'],
                            scp['payreq_jcno'],
                            scp['payreq_purchasereq_number'],
                            scp['payreq_description'],
                            scp['payreq_total_incl'],
                            scp['payreq_payed'],
                            scp['payreq_date_paid']
                            
                            )
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        htmlcompleted =  html1 + html2 + html3
        return htmlpending +"<p/>"+ htmlcompleted


    @expose()
    def ajax_contracts_wip_balances_per_point(self,usrid,**kw):
        dictsites = []
        #contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               #order_by(desc(JistContracts.jno)).all()
        contracts = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(usrid)). \
                order_by(desc(JistContracts.jno)). \
                all()
        thisuser = DBS_ContractData.query(User).filter(User.user_id==int(usrid)).one()
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

               <h2 class="effect6">
               <span class='spanleft'>WIP For :%s </span>
               </h2>
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
                """%(thisuser.user_name,grandtotalexclsum, grandvatsum, grandtotalinclsum)
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
    def ajaxgetbudget_contracts_progress(self,**named):
        contracts = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.completed=="False"). \
                filter(JistContracts.jno > 1000). \
               order_by(desc(JistContracts.jno)).all()
        locale.setlocale(locale.LC_ALL, '')
        budgetlist = []
        for thiscontract in contracts:
            budgetdata = DBS_ContractData.query(JistContractBudget). \
                    filter(JistContractBudget.budget_jno==thiscontract.jno). \
                    filter(JistContractBudget.active==True). \
                    order_by(asc(JistContractBudget.id)). \
                    all()
            for k in budgetdata:
                budgetlist.append({'id':k.id,
                                    'item':k.budget_item,
                                    'jcno':thiscontract.jno,
                                    'description':k.budget_description,
                                    'unit':k.budget_unit,
                                    'qty':k.budget_qty,
                                    'rate':k.price_rate,
                                    'rate_total':k.price_total,
                                    'rate_material':k.rate_material,
                                    'rate_markup':k.rate_markup,
                                    'rate_labour':k.rate_labour,
                                    'rate_transport':k.rate_transport,
                                    'rate_healthsafety':k.rate_healthsafety,
                                    'rate_overheads':k.rate_overheads,
                                    'rate_specialist':k.rate_specialist,
                                    'rate_markup_specialist':k.rate_markup_specialist,
                                    'rate_other':k.rate_other,
                                    
                                    })

        #dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """

               <h4 class="effect6">
               <span class='spanleft'>Budgets Items For Contracts In Progress: </span>
                <span class='spanright'>
               </span>
               </h4>
                            <table id="production_budget_table" class='table_budgetoveriew'>
                            <th>ID</th>
                            <th>JCNo</th>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th>Qty</th>
                            <th>Rate</th>
                            <th>Total</th>
                            <th></th>
                            <th>Material</th>
                            <th>Markup</th>
                            <th>Labour</th>
                            <th>Transport</th>
                            <th>H&S</th>
                            <th>Overheads</th>
                            <th>Specialist</th>
                            <th>Spec Markup</th>
                            <th>Other</th>
                """
        temphtml1 = ""
        html2 = ""
        for scp in budgetlist:
            temphtml1 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td width="30px">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['id'],scp['jcno'],scp['item'],scp['description'],scp['unit'],scp['qty'],scp['rate'],scp['rate_total'],'',
                         scp['rate_material']*scp['qty'],
                         scp['rate_markup']*scp['qty'],
                         scp['rate_labour']*scp['qty'],
                         scp['rate_transport']*scp['qty'],
                         scp['rate_healthsafety']*scp['qty'],
                         scp['rate_overheads']*scp['qty'],
                         scp['rate_specialist']*scp['qty'],
                         scp['rate_markup_specialist']*scp['qty'],
                         scp['rate_other']*scp['qty'],
                            )
            html2 = html2 + temphtml1

        html3 = """
                            </table>
                            <div id="production_budget_totals"></div>
                """
                            
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxget_contracts_progress_no_budget(self,**named):
        contracts = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.completed=="False"). \
                filter(JistContracts.jno > 1000). \
               order_by(desc(JistContracts.jno)).all()
        locale.setlocale(locale.LC_ALL, '')
        budgetlist = []
        for thiscontract in contracts:
            budgetdata = DBS_ContractData.query(JistContractBudget). \
                    filter(JistContractBudget.budget_jno==thiscontract.jno). \
                    filter(JistContractBudget.active==True). \
                    order_by(asc(JistContractBudget.id)). \
                    all()
            if not budgetdata:
                budgetlist.append({'id':None,
                                    'item':None,
                                    'jcno':thiscontract.jno,
                                    'description':None,
                                    'unit':None,
                                    'qty':0,
                                    'rate':0,
                                    'rate_total':0,
                                    'rate_material':0,
                                    'rate_markup':0,
                                    'rate_labour':0,
                                    'rate_transport':0,
                                    'rate_healthsafety':0,
                                    'rate_overheads':0,
                                    'rate_specialist':0,
                                    'rate_markup_specialist':0,
                                    'rate_other':0,
                                    
                                    })
        #dt = dts.strftime("%A, %d %B %Y %H:%M:%S")
        html1 = """
                        <p id='contractheader'>Contracts With No Budgets: <br/> 
                        </p>
                            <table id="production_budget_table" class='table_budgetoveriew'>
                            <th>ID</th>
                            <th>JCNo</th>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th>Qty</th>
                            <th>Rate</th>
                            <th>Total</th>
                            <th></th>
                            <th>Material</th>
                            <th>Markup</th>
                            <th>Labour</th>
                            <th>Transport</th>
                            <th>H&S</th>
                            <th>Overheads</th>
                            <th>Specialist</th>
                            <th>Spec Markup</th>
                            <th>Other</th>
                """
        temphtml1 = ""
        html2 = ""
        for scp in budgetlist:
            temphtml1 = """
            <tr>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="left">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td width="30px">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                            <td align="right">%s</td>
                    </tr>
                    """%(scp['id'],scp['jcno'],scp['item'],scp['description'],scp['unit'],scp['qty'],scp['rate'],scp['rate_total'],'',
                         scp['rate_material']*scp['qty'],
                         scp['rate_markup']*scp['qty'],
                         scp['rate_labour']*scp['qty'],
                         scp['rate_transport']*scp['qty'],
                         scp['rate_healthsafety']*scp['qty'],
                         scp['rate_overheads']*scp['qty'],
                         scp['rate_specialist']*scp['qty'],
                         scp['rate_markup_specialist']*scp['qty'],
                         scp['rate_other']*scp['qty'],
                            )
            html2 = html2 + temphtml1

        html3 = """
                            </table>
                            <div id="production_budget_totals"></div>
                """
                            
        html =  html1 + html2 + html3
        return html

    @expose()
    @expose('json')
    def get_point_contracts_json_daily_data(self,**kw):
        if 'userpoint' in kw:
            print "it was there"
        else:
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            user = User.by_user_id(usernow.user_id)
            userpermissions = user.permissions
        if 'usercurrent'in kw:
            print "User current was here"
        
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='productionmanage':
                logged = True
        if not logged: return "Only for People with the Production Manager Rights"
        #contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               #order_by(desc(JistContracts.jno)).all()
        contracts = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                order_by(desc(JistContracts.jno)). \
                all()
        #thisuser = DBS_ContractData.query(User).filter(User.user_id==int(user_id)).one()
        locale.setlocale(locale.LC_ALL, '')
        grandtotalexcl = 0
        dictsites = []
        dicttest = []
        planfirstdate = DBS_ContractData.query(JistContracts,JistContractStatus,JistContractPlanningDates). \
                filter(JistContracts.completed=='False'). \
                filter(JistContracts.jno==JistContractPlanningDates.jcno). \
                filter(JistContracts.jno==JistContractStatus.jno). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                filter(JistContractPlanningDates.planstartdate != None). \
                filter(JistContractPlanningDates.planstartdate != 'Null'). \
                filter(JistContractPlanningDates.planstartdate != '0000-00-00'). \
                value(func.min(JistContractPlanningDates.planstartdate))
                #all()
        planlastdate = DBS_ContractData.query(JistContracts,JistContractStatus,JistContractPlanningDates). \
                filter(JistContracts.completed=='False'). \
                filter(JistContracts.jno==JistContractPlanningDates.jcno). \
                filter(JistContracts.jno==JistContractStatus.jno). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                filter(JistContractPlanningDates.planenddate != None). \
                filter(JistContractPlanningDates.planenddate != 'Null'). \
                filter(JistContractPlanningDates.planenddate != '0000-00-00'). \
                value(func.max(JistContractPlanningDates.planenddate))

        for thisites in contracts:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==thisites.jno).one()
            status = {}
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==thisites.jno).one()
                planstartdate = conplandates.planstartdate.strftime("%d-%m-%y")
                planenddate = conplandates.planenddate.strftime("%d-%m-%y")
                dtplanstartdate = conplandates.planstartdate 
                dtplanenddate = conplandates.planenddate 
                #print planstartdate,planenddate
            except:
                conplandates = 'None'
                planstartdate = 'None' 
                planenddate = 'None' 
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
                         #'orderdate':thisites.orderdate,
            delta_1day = timedelta(days=1)
            daysbetween = planlastdate - planfirstdate
            dayofweek_start = planfirstdate.isoweekday()
            strdaysbetween = str(daysbetween).split(' ')[0]
            ganttlist = []
            firstdateloop = planfirstdate
            for i in range(int(strdaysbetween)+dayofweek_start):
                #print type(firstdateloop), type(planfirstdate), type(planlastdate)
                #print planstartdate, type(planenddate)
                #splitstartdate = planstartdate.split(',')
                #print type(dtplanstartdate), dtplanstartdate
                if dtplanstartdate <= firstdateloop <= dtplanenddate:
                    #print firstdateloop, planfirstdate, planlastdate
                    ganttlist.append('T')
                else:
                    ganttlist.append('F')
                firstdateloop += delta_1day
            dictsites.append({'jno':thisites.jno,
                          'orderno':thisites.orderno,
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
                         'planstart':planstartdate,
                         'planend':planenddate,
                         'ganttlist':ganttlist,
                         })
        return json.dumps(dictsites)

    @expose()
    @expose('json')
    def get_point_contracts_json_monthly_data(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='productionmanage':
                logged = True
        if not logged: return "Only for People with the Production Manager Rights"
        #contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               #order_by(desc(JistContracts.jno)).all()
        contracts = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                order_by(desc(JistContracts.jno)). \
                all()
        #thisuser = DBS_ContractData.query(User).filter(User.user_id==int(user_id)).one()
        locale.setlocale(locale.LC_ALL, '')
        grandtotalexcl = 0
        dictsites = []
        dicttest = []
        planfirstdate = DBS_ContractData.query(JistContracts,JistContractStatus,JistContractPlanningDates). \
                filter(JistContracts.completed=='False'). \
                filter(JistContracts.jno==JistContractPlanningDates.jcno). \
                filter(JistContracts.jno==JistContractStatus.jno). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                filter(JistContractPlanningDates.planstartdate != None). \
                filter(JistContractPlanningDates.planstartdate != 'Null'). \
                filter(JistContractPlanningDates.planstartdate != '0000-00-00'). \
                value(func.min(JistContractPlanningDates.planstartdate))
                #all()
        planlastdate = DBS_ContractData.query(JistContracts,JistContractStatus,JistContractPlanningDates). \
                filter(JistContracts.completed=='False'). \
                filter(JistContracts.jno==JistContractPlanningDates.jcno). \
                filter(JistContracts.jno==JistContractStatus.jno). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                filter(JistContractPlanningDates.planenddate != None). \
                filter(JistContractPlanningDates.planenddate != 'Null'). \
                filter(JistContractPlanningDates.planenddate != '0000-00-00'). \
                value(func.max(JistContractPlanningDates.planenddate))

        for thisites in contracts:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==thisites.jno).one()
            status = {}
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==thisites.jno).one()
                planstartdate = conplandates.planstartdate.strftime("%d-%m-%y")
                planenddate = conplandates.planenddate.strftime("%d-%m-%y")
                dtplanstartdate = conplandates.planstartdate 
                dtplanenddate = conplandates.planenddate 
                #print planstartdate,planenddate
            except:
                conplandates = 'None'
                planstartdate = 'None' 
                planenddate = 'None' 
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
                         #'orderdate':thisites.orderdate,
            delta_1day = timedelta(days=1)
            daysbetween = planlastdate - planfirstdate
            dayofweek_start = planfirstdate.isoweekday()
            strdaysbetween = str(daysbetween).split(' ')[0]
            ganttlist = []
            firstdateloop = planfirstdate
            for i in range(int(strdaysbetween)+dayofweek_start):
                #print type(firstdateloop), type(planfirstdate), type(planlastdate)
                #print planstartdate, type(planenddate)
                #splitstartdate = planstartdate.split(',')
                #print type(dtplanstartdate), dtplanstartdate
                if dtplanstartdate <= firstdateloop <= dtplanenddate:
                    #print firstdateloop, planfirstdate, planlastdate
                    ganttlist.append('T')
                else:
                    ganttlist.append('F')
                firstdateloop += delta_1day

            dictsites.append({'jno':thisites.jno,
                          'orderno':thisites.orderno,
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
                         'planstart':planstartdate,
                         'planend':planenddate,
                         'ganttlist':ganttlist,
                         })
        return json.dumps(dictsites)

    @expose()
    @expose('json')
    def get_point_contracts_json_dates_table(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='productionmanage':
                logged = True
        if not logged: return "Only for People with the Production Manager Rights"
        contracts = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                order_by(desc(JistContracts.jno)). \
                all()
        planfirstdate = DBS_ContractData.query(JistContracts,JistContractStatus,JistContractPlanningDates). \
                filter(JistContracts.completed=='False'). \
                filter(JistContracts.jno==JistContractPlanningDates.jcno). \
                filter(JistContracts.jno==JistContractStatus.jno). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                filter(JistContractPlanningDates.planstartdate != None). \
                filter(JistContractPlanningDates.planstartdate != 'Null'). \
                filter(JistContractPlanningDates.planstartdate != '0000-00-00'). \
                value(func.min(JistContractPlanningDates.planstartdate))
                #all()
        planlastdate = DBS_ContractData.query(JistContracts,JistContractStatus,JistContractPlanningDates). \
                filter(JistContracts.completed=='False'). \
                filter(JistContracts.jno==JistContractPlanningDates.jcno). \
                filter(JistContracts.jno==JistContractStatus.jno). \
                filter(JistContractStatus.pointperson==int(user.user_id)). \
                filter(JistContractPlanningDates.planenddate != None). \
                filter(JistContractPlanningDates.planenddate != 'Null'). \
                filter(JistContractPlanningDates.planenddate != '0000-00-00'). \
                value(func.max(JistContractPlanningDates.planenddate))
        datepack = []
        strplanfirstdate = planfirstdate.strftime("%d-%m-%y")
        strplanlastdate = planlastdate.strftime("%d-%m-%y")
        daysbetween = planlastdate - planfirstdate
        dayofweek_start = planfirstdate.isoweekday()
        strdaysbetween = str(daysbetween).split(' ')[0]
        #print planfirstdate, planlastdate
        #print type(daysbetween)
        print 'Days Between in days {0}'.format(daysbetween.days)
        #print dayofweek_start
        #print wip
        #dt = planfirstdate.strftime("%A, %d %B %Y %H:%M:%S")
        daylisttemp = []
        allmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dow = ["S", "M", "T", "W", "T", "F", "S"]
        for i in range(daysbetween.days/7+2):
            for day in dow:
                daylisttemp.append(day)
        daylist = daylisttemp[dayofweek_start:] 
        dateslist = []
        monthslist = []
        weekdaylist = []
        weeknoyrlist = []
        daynoyrlist = []
        delta_1day = timedelta(days=1)
        firstdateloop = planfirstdate
        for i in range(int(strdaysbetween)+7):
            dateslist.append(firstdateloop.strftime("%d"))
            monthslist.append(firstdateloop.strftime("%B %Y"))
            weekdaylist.append(firstdateloop.strftime("%w"))
            weeknoyrlist.append(firstdateloop.strftime("%W"))
            daynoyrlist.append(firstdateloop.strftime("%j"))
            #dt = dts.strftime("%A, %d %B %Y %H:%M:%S"))
            firstdateloop += delta_1day
        print 'Start Date {0}'.format(strplanfirstdate)
        print 'Last Date {0}'.format(strplanlastdate)
        print 'Day of Week {0}'.format(dayofweek_start)
        print 'Day List', daylist
        print 'Dates List', dateslist
        print 'Months List', monthslist

        #print "Current year: ", datetime.date.today().strftime("%Y")
        #print "Month of year: ", datetime.date.today().strftime("%B")
        #print "Week number of the year: ", datetime.date.today().strftime("%W")
        #print "Weekday of the week: ", datetime.date.today().strftime("%w")
        #print "Day of year: ", datetime.date.today().strftime("%j")
        #print "Day of the month : ", datetime.date.today().strftime("%d")
        #print "Day of week: ", datetime.date.today().strftime("%A")


        if strdaysbetween < 60:
            pass
        elif strdaysbetween < 90:
            pass
        else:
            pass

        datepack.append({'totaldays': strdaysbetween,
                         'dayslist': daylist,
                         'dateslist':dateslist,
                         'monthslist':monthslist,
                         'weekyrlist':weeknoyrlist,
                         'weekdaylist':weekdaylist,
                         'dayyrlist':daynoyrlist,
                        }) 
        #thisuser = DBS_ContractData.query(User).filter(User.user_id==int(user_id)).one()
        return json.dumps(datepack)

    @expose()
    @expose('json')
    def get_contracts_wip_balances_all_point_json(self,**kw):
        dictsites = []
        #contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               #order_by(desc(JistContracts.jno)).all()
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
        point_export_list = [] 
        #for point in pointlist:
            #contractslist = DBS_ContractData.query(JistContracts,JistContractStatus). \
                    #filter(JistContracts.completed=='False'). \
                    #filter(JistContractStatus.pointperson==point['user_id']). \
                    #all()
            #contracts_totals = 0
            #for cont in contractslist:
                #contractsvalue = DBS_ContractData.query( JistContractOrderItems). \
                    #filter(JistContractOrderItems.jno==cont.jno). \
                    #value(func.sum(JistContractOrderItems.total))
                #contracts_totals = contracts_totals + contractsvalue
            #print contracts_total
            #if contracts_totals:
                #contracts_total_final = format_decimal(contracts_totals,format='#,##0.00;-#0.00',locale='en')

            #print contracts_totals_final
            #point_contract_list = DBS_ContractData.query(JistContracts, JistContractStatus). \
                    #filter(JistContracts.completed=='False'). \
                    #filter(JistContractStatus.pointperson==point['user_id']). \
                    #all()
            #total_invoices = 0
            #for cont in point_contract_list:
                #invoices_total_excl = DBS_JistInvoicing.query(JistInvoicesList). \
                              #filter(JistInvoicesList.contract==cont.jno). \
                             #value(func.sum(JistInvoicesList.value_excl))
                #if invoices_total_excl:
                    #total_invoices = total_invoices + invoices_total_excl
                #print total_invoices

        
        #thisuser = DBS_ContractData.query(User).filter(User.user_id==int(usrid)).one()
        #locale.setlocale(locale.LC_ALL, '')
        #grandtotalexcl = 0
        #grandtotalexclsum = format_decimal(grandtotalexcl,format='#,##0.00;-#0.00',locale='en')
        #grandvat = float(grandtotalexcl) * VAT_RATE
        #grandincl = float(grandvat) + float(grandtotalexcl)
        #grandtotalinclsum = format_decimal(Decimal(grandincl),format='#,##0.00;-#0.00',locale='en')
        #grandvatsum = format_decimal(grandvat,format='#,##0.00;-#0.00',locale='en')

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
                            #scp["description"],scp["pointperson"],scp["status"],
                            #scp["totalexcl_contractvalue"],scp["totalexcl_invoices"],scp["totalexcl_diff"],scp["totalincl_diff"])
            #html2 = html2 + temphtml1
        #return json.dumps({'pointlist':returnlist})
        return json.dumps({'data':[100,200,400,400],
                          'labels': ['BoBGT','Lucy','Gary','Hoolio'],
                          'tooltips': ['Bob did well','Lucy had her best result','Gary - not so good','Hoolio had a good start']
                         })
