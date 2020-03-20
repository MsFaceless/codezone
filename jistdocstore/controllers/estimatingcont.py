# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group
from tg.decorators import paginate
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

#from tw.jquery import AjaxForm
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
from jistdocstore.lib.jist3yrbuildingreportlab import * 
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import FileStoreProduction
#from jistdocstore.model import DBS_JistEstimating, metadata6
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
import random
from tg import session
#from tw.jquery import TreeView

from babel.numbers import format_currency, format_number, format_decimal
from decimal import Decimal
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')

__all__ = ['EstimatingController']


class EstimatingController(BaseController):
    """Sample controller-wide authorization"""
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))
    def __init__(self):
        session["session_site"] = [] 
        session["session_scopeitem"] = [] 
        session.save()
        self.last_saved_site_rnd = 0
        self.last_saved_scope_rnd = 0
        self.last_saved_bqitem_rnd = 0
        self.last_saved_quoteno = 0
        self.last_saved_scopelist = "" 
        self.last_saved_editscope = "" 
        self.last_save_scopeiddeleted = 0
        self.building_3yr_tender_number = "445Q"
        self.last_saved_scopecontract = 0

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def index(self):
        redirect('estimatingcont/menu')

    @expose('jistdocstore.templates.estimating.estimatingindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Estimating: Main Menu') 

#*********************************************************************
#*********Start of 2yr Building Tender 2010-2012**********************
#*********************************************************************
    @require(in_any_group("managers","estimates"))
    @expose('jistdocstore.templates.estimating.estimate_search')
    def search_estimate(self,**named):
        """Handle the 'sitesearch' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=SiteNameSearch(),
                    target="output",
                    action="do_search_estimate")

        tmpl_context.form = ajax_form 

        return dict(page='estimatesearch',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_estimate(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        sitename = "%(site_name)s" % kw
        searchphrase = "%"+sitename+"%"
        contract = DBS_JistEstimating.query(JistEstimating2yrSites).filter(JistEstimating2yrSites.name.like(searchphrase)). \
                                           filter(JistEstimating2yrSites.active=="Y"). \
                                           order_by(desc(JistEstimating2yrSites.id)).all()
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>Site Id</th>
                    <th>Date</th>
                    <th>Site Name </th>
                    <th>Description </th>
                    <th>WO Number</th>
                    <th>Supervisor</th>
                    """
        sitedata = sitedata + headerdata
        for k in contract:
            #status = DBS_ContractData.query(JistContractStatus). \
            #        filter(JistContractStatus.jno==k.jno).one()
            sitedatatemp = """<tr><td><a href='/productioncont/get_one/%s'>%s</a>
                            </td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><p/></tr>
                            """ % (k.id,k.id,k.date,k.name,
                                   k.description,k.wonumber,k.supervisor)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @require(in_any_group("managers","estimates"))
    @expose('jistdocstore.templates.estimating.estimate_search')
    def search_estimate_contracts(self,**named):
        """Handle the 'sitesearch' page."""

        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=EstimateJCNoSearch(),
                    target="output",
                    action="do_search_estimate_contracts")

        tmpl_context.form = ajax_form 

        return dict(page='estimatesearch',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_estimate_contracts(self, **kw):
        quotes = DBS_JistEstimating.query(JistEstimating2yrQuotes). \
                                           filter(JistEstimating2yrQuotes.jcno<>"None"). \
                                           order_by(desc(JistEstimating2yrQuotes.id)).all()
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>Quote No</th>
                    <th>Quote Date</th>
                    <th>Est Site Name </th>
                    <th>JCNo </th>
                    <th></th>
                    <th></th>
                    """
        sitedata = sitedata + headerdata
        for k in quotes:
            #status = DBS_ContractData.query(JistContractStatus). \
            #        filter(JistContractStatus.jno==k.jno).one()
            estcontract = DBS_JistEstimating.query(JistEstimating2yrSites). \
                                               filter(JistEstimating2yrSites.id==k.idsite). \
                                               one()
            #jcnocontract = DBS_ContractData.query(JistContracts). \
            #                                   filter(JistContracts.jno==k.jcno). \
            #                                   one()
            sitedatatemp = """<tr><td><a href='/productioncont/get_one/%s'>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td></td><p/></tr>
                            """ %(k.id,k.id,
                                    k.date,
                                    estcontract.name,
                                    k.jcno,
                                    #jcnocontract.site
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose('jistdocstore.templates.estimating.estimate_all_contracts')
    def search_estimates_contracts_test(self, **kw):
        quotes = DBS_JistEstimating.query(JistEstimating2yrQuotes). \
                                           filter(JistEstimating2yrQuotes.jcno<>"None"). \
                                           order_by(desc(JistEstimating2yrQuotes.id)).all()
        wip1 = Est_contracts_filler.get_value(values={},offset=0,order_by='id',desc=True)
        """
        wip1 = []
        for k in quotes:
            estcontract = DBS_JistEstimating.query(JistEstimating2yrSites). \
                                               filter(JistEstimating2yrSites.id==k.idsite). \
                                               one()
            wip1.append({
                         'id':k.id,
                         'date':k.date,
                         'contract':estcontract.name,
                         'jno':k.jcno,
                         })

        """
        tmpl_context.form = spx_est_contracts_table 
        count = len(wip1) 
        page =int( kw.get( 'page', '1' ))
        currentPage = paginate.Page(
            wip1, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print items
        return dict(page='All Estimates vs Contract',
                    wip = items,
                    thiscurrentPage=currentPage,
                    value=kw,
                    selfname = 'search_estimates_contracts_test',
                    value2=kw)

    @expose('jistdocstore.templates.estimating.estimate_all_contracts')
    def search_estimates_contracts_all(self,statusidcode=0,**kw):
        quotes = DBS_JistEstimating.query(JistEstimating2yrQuotes). \
                                           filter(JistEstimating2yrQuotes.jcno<>"None"). \
                                           filter(JistEstimating2yrQuotes.date>"2011-06-01"). \
                                           order_by(desc(JistEstimating2yrQuotes.id)).all()
        wip1 = []
        if statusidcode !=0:
            thisstatcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusidcode).one()
            thestatcode = thisstatcode.status
        else:
            thestatcode = "Nothing"
        for k in quotes:
            estsite = DBS_JistEstimating.query(JistEstimating2yrSites). \
                                               filter(JistEstimating2yrSites.id==k.idsite). \
                                               one()
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==k.jcno). \
                    one()

            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.jcno).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            status = {}
            plandates = {}
            timeframe = {}
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==k.jcno).one()
                thestartdate = str(conplandates.planstartdate).split(' ')[0]
                theenddate = str(conplandates.planenddate).split(" ")[0]
                plandates = {'planstart':thestartdate,
                             'planend':theenddate
                             }
            except:
                plandates = {'planstart':'None',
                             'planend':'None'
                             }

            timeframe = {'orderdate':contract.orderdate,
                     'sitehandover':statusall.sitehandoverdate,
                     'startdate':statusall.actualstartdate,
                     'firstdel':statusall.firstdeldate,
                     'finalcompl':statusall.finalcompldate,
                     'lasttoedit':statusall.useridedited,
                     'timeedit':statusall.dateedited,
                     }
            try:
                agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
                status = {'statuscode':statcode.status,
                          'pointperson':point.user_name,
                          'codeid':statcode.id,
                          'siteagent':agent.user_name}
            except:
                agent = DBS_ContractData.query(User).filter(User.user_id==1).one()
                status = {'statuscode':statcode.status,
                          'pointperson':point.user_name,
                          'codeid':statcode.id,
                          'siteagent':agent.user_name}
            wip1.append({
                         'quoteid':k.id,
                         'quotedate':k.date,
                         'wonumber':estsite.wonumber,
                         'estsite':estsite.name,
                         'jcno':k.jcno,
                         'ordernumber':contract.orderno,
                         'orderdate':contract.orderdate,
                         'pointperson':status['pointperson'],
                         'siteagent':status['siteagent'],
                         'status':status['statuscode'],
                         'active':contract.completed,
                         'planstart':plandates['planstart'],
                         'planend':plandates['planend'],
                         'statuscodeid':status['codeid'],
                         })
        wip2 = []
        for w in wip1:
            if w['active'] == 'False':
                if int(str(w['statuscodeid'])) <= int(str(statusidcode)):
                    wip2.append(w['statuscodeid'])
        tmpl_context.widget = contract_status_chooser 

        result = self.multikeysort(wip2, ['-orderdate', 'pointperson', 'status'])
        count = len(result) 
        page =int( kw.get( 'page', '1' ))
        currentPage = paginate.Page(
            result, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='All ESS 2 yr Building Estimates vs Contracts',
                    wip = items,
                    thiscurrentPage=currentPage,
                    value=statusidcode,
                    selfname = 'search_estimates_contracts_all',
                    action = '/estimatingcont/getstatusitems',
                    pdfstring = "/estimatingcont/export_ess_contracts_pdf/"+str(statusidcode),
                    statusidcode=statusidcode,
                    viewinfo = thestatcode
                    )

    def multikeysort(self,items, columns):
        from operator import itemgetter
        comparers = [ ((itemgetter(col[1:].strip()), -1) if col.startswith('-') else (itemgetter(col.strip()), 1)) for col in columns]
        def comparer(left, right):
            for fn, mult in comparers:
                result = cmp(fn(left), fn(right))
                if result:
                    return mult * result
            else:
                return 0
        return sorted(items, cmp=comparer)

    @expose()
    def getstatusitems(self,*args,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        if not kw['statuscode']:
            point = 0
        else:
            point = kw['statuscode']
        redirect('/estimatingcont/search_estimates_contracts_all/'+point)

    @expose()
    def export_ess_contracts_pdf(self,statusidcode):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA3(filename)
        wip1 = []
        userdata = []

        quotes = DBS_JistEstimating.query(JistEstimating2yrQuotes). \
                                           filter(JistEstimating2yrQuotes.jcno<>"None"). \
                                           filter(JistEstimating2yrQuotes.date>"2011-06-01"). \
                                           order_by(desc(JistEstimating2yrQuotes.id)).all()
        wip1 = []
        if statusidcode !=0:
            thisstatcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusidcode).one()
            thestatcode = thisstatcode.status
        else:
            thestatcode = "Nothing"

        for k in quotes:
            estsite = DBS_JistEstimating.query(JistEstimating2yrSites). \
                                               filter(JistEstimating2yrSites.id==k.idsite). \
                                               one()
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==k.jcno). \
                    one()

            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==k.jcno).one()
            point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            status = {}
            plandates = {}
            timeframe = {}
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==k.jcno).one()
                thestartdate = str(conplandates.planstartdate).split(' ')[0]
                theenddate = str(conplandates.planenddate).split(" ")[0]
                plandates = {'planstart':thestartdate,
                             'planend':theenddate
                             }
            except:
                plandates = {'planstart':'None',
                             'planend':'None'
                             }

            timeframe = {'orderdate':contract.orderdate,
                     'sitehandover':statusall.sitehandoverdate,
                     'startdate':statusall.actualstartdate,
                     'firstdel':statusall.firstdeldate,
                     'finalcompl':statusall.finalcompldate,
                     'lasttoedit':statusall.useridedited,
                     'timeedit':statusall.dateedited,
                     }
            try:
                agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
                status = {'statuscode':statcode.status,
                          'pointperson':point.user_name,
                          'codeid':statcode.id,
                          'siteagent':agent.user_name}
            except:
                agent = DBS_ContractData.query(User).filter(User.user_id==1).one()
                status = {'statuscode':statcode.status,
                          'pointperson':point.user_name,
                          'codeid':statcode.id,
                          'siteagent':agent.user_name}
            wip1.append({
                         'quoteid':k.id,
                         'quotedate':k.date,
                         'wonumber':estsite.wonumber,
                         'estsite':estsite.name,
                         'jcno':k.jcno,
                         'ordernumber':contract.orderno,
                         'orderdate':contract.orderdate,
                         'pointperson':status['pointperson'],
                         'siteagent':status['siteagent'],
                         'status':status['statuscode'],
                         'active':contract.completed,
                         'planstart':plandates['planstart'],
                         'planend':plandates['planend'],
                         'statuscodeid':status['codeid'],
                         })
        #print wip1 
        wip2 = []
        for w in wip1:
            if w['active'] == 'False':
                if int(str(w['statuscodeid'])) <= int(str(statusidcode)):
                    wip2.append(w)
        result = self.multikeysort(wip2, ['-orderdate', 'pointperson', 'status'])

        userdata.append([datetime.date(datetime.now()),
                        "All ESS Contracts vs Quotes",
                        "Status: Equal or Less Than %s"%(thestatcode)
                        ])
        headers =["QuoteID","Quote Date","WO-Number","Est Site Name","JCNo","PO Number",  
                  "Order Date","Point","Siteagent","Status","Plan Start","Plan End"]
        headerwidths=[60,80,80,150,60,80,80,80,80,80,80,80]
        pdffile.CreatePDFESSContractsQuotes(userdata,result,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

#*********************************************************************
#*********Start of 3yr Building Tender 2012-2015**********************
#*********************************************************************

    @require(in_any_group("managers","estimates"))
    @expose('jistdocstore.templates.estimating.estimate_3yr_boq')
    def show_3yr_boq(self,**named):
        schedules = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSchedules).all()

        statuscodes = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingStatusCodes).all()
        return dict(page='Building Tender 3yr ESS Bill Of Quantities',
                    wip = schedules,
                    currentPage=1,
                    statuscodes=statuscodes,
                    value=named,
                    value2=named)

    @expose()
    def ajax3yrheadings(self,jno,**kw):
        if jno:
            headings =  DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingHeadings). \
                        filter(JistEstimating3yrBuildingHeadings.idschedule==int(jno)).all()
            schedule = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSchedules). \
                        filter(JistEstimating3yrBuildingSchedules.id==int(jno)).one()
            html1 = """
                            <H4>Bill Headings</H4>
                                %s
                                <table class='table_estdata'>
                                <th>Heading</th>
                                <th>Show Sub Headings</th>
                    """%schedule.description
            temphtml1 = ""
            html2 = ""
            for scp in headings:
                temphtml1 = """
                        <tr>
                        <td >
                        %s
                        </td>
                        <td width='25px'>
                            <img src="/images/project-open.png"
                            onclick="loadXMLSubHeaders(%s)">
                            </img>
                        </td>
                        </tr>
                        """%(scp.description,scp.id)
                html2 = html2 + temphtml1

            html3 = """
                                </table>

                    """
            html =  html1 + html2 + html3
            return html
            
    @expose()
    def ajax3yrsubheadings(self,jno,**kw):
        if jno:
            subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
                        filter(JistEstimating3yrBuildingSubHeadings.idheading==int(jno)).all()
            headings =  DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingHeadings). \
                        filter(JistEstimating3yrBuildingHeadings.id==int(jno)).one()
            html1 = """
                            <H4>Bill Sub Headings</H4>
                                %s
                                <table class='table_estdata'>
                                <th>Sub Heading</th>
                                <th>Show Items</th>
                    """%headings.description
            temphtml1 = ""
            html2 = ""
            for scp in subheadings:
                temphtml1 = """
                        <tr>
                        <td >
                        %s
                        </td>
                        <td width='25px'>
                            <img src="/images/project-open.png"
                            onclick="loadXMLItems(%s)">
                            </img>
                        </td>
                        </tr>
                        """%(scp.description,scp.id)
                html2 = html2 + temphtml1

            html3 = """
                                </table>

                    """
            html =  html1 + html2 + html3
            return html

    @expose()
    def ajax3yritems(self,jno,scopeid='',**kw):
        try:
            if jno:
                items =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingItems). \
                            filter(JistEstimating3yrBuildingItems.idsubheading==jno).all()
                subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
                            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
                html1 = """
                                <H4>Bill Items</H4>
                                    %s
                                    <table class='table_estdata'>
                                    <th>Item ID</th>
                                    <th>Description</th>
                                    <th>Unit</th>
                                    <th>Price</th>
                                    <th>Add To Scope</th>
                        """%subheadings.description
                temphtml1 = ""
                #for m in session['session_scopeitem']:
                #    print m[0].id
                if not scopeid == '':
                    sitescope = scopeid
                    html2 = ""
                    for scp in items:
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
                                <td width='25px'>
                                    <img src="/images/project-open.png"
                                    onclick="loadXMLSiteBQItem(%s,%s)">
                                    </img>
                                </td>
                                </tr>
                                """%(scp.itemno,scp.description,scp.units,scp.price,scp.id,sitescope)
                        html2 = html2 + temphtml1
                else:
                    html2 = """
                            <tr>
                            <td colspan='5'>
                            Please Choose a site and a scope item first !!!
                            </td>
                            </tr>
                            """

                html3 = """
                                    </table>

                        """
                html =  html1 + html2 + html3
                return html
        except:
            html1 = """
                                <H4>Bill Items</H4>
                                    <table class='table_estdata'>
                                    <th>Error</th>
                        """
            html2 = """
                        <tr>
                        <td>
                        Please Choose a site and a scope item first !!!
                        </td>
                        </tr>
                        """
            html3 = """
                                    </table>

                        """
            html =  html1 + html2 + html3

            return html

    @expose()
    def ajax3yrsites(self,statuscode,**kw):
        dictsites = []
        sites =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.active=='Y'). \
                            order_by(desc(JistEstimating3yrBuildingSites.id)).all()
        statusitem=DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingStatusCodes). \
                    filter(JistEstimating3yrBuildingStatusCodes.id==int(statuscode)). \
                            one()
        statusdata=DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingStatusData). \
                    filter(JistEstimating3yrBuildingStatusData.statuscode==str(statuscode)). \
                            order_by(desc(JistEstimating3yrBuildingStatusData.id)).all()
        for k in statusdata:
            #print k.idsite
            thisites =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.id==k.idsite). \
                        one()
            dictsites.append({'id':thisites.id,
                          'name':thisites.name,
                         'area':thisites.area,
                         'description':thisites.description,
                         'date':thisites.date,
                         'wonumber':thisites.wonumber,
                         'supervisor':thisites.supervisor,
                         'visit_by':thisites.visit_by,
                         })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """
                            Sites Sorted By: %s
                            <table class='table_estdata'>
                            <th>ID</th>
                            <th>Site Name</th>
                            <th>Area</th>
                            <th>Description</th>
                            <th>Open SOW</th>
                            <th>Edit Site</th>
                """%statusitem.status
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
                        <td width='25px'>
                            <img src="/images/project-open.png"
                            onclick="loadXMLSOW(%s)">
                            </img>
                        </td>
                        <td width='25px'>
                            <img src="/images/edit_qty.png"
                            onclick="openestsite(%s,'%s','%s','%s','%s','%s','%s')">
                            </img>

                        </td>
                    </tr>
                    """%(scp["id"],scp["name"],scp["area"],scp["description"],scp["id"],
                            scp["id"],scp['name'],scp["date"],scp["description"],scp["wonumber"],scp["supervisor"],scp["area"])
            html2 = html2 + temphtml1
        #,%s,%s,%s,%s
        #,scp["description"],scp["wonumber"],scp["supervisor"],scp["area"]
        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @require(in_any_group("managers","estimates"))
    @expose('jistdocstore.templates.estimating.estimate_3yr_sites')
    def show_3yr_sites(self,**named):
        schedules = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSchedules).all()
        statuscodes = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingStatusCodes).all()
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        #statusdata = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingStatusCodes).all()
        #sitetree = TreeView(treeDiv='navTree')
        #tmpl_context.tree = sitetree 
        #tmpl_context.tree = sitetree 
        return dict(page='Building Tender 3yr ESS Sites',
                    wip = schedules,
                    statuscodes=statuscodes,
                    contracts = contracts,
                    currentPage=1,
                    value=named,
                    value2=named)
  
    @expose()
    def ajax3yrsitesow(self,jno,**kw):
        scopeofwork =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.idsite==jno).all()
        site =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.id==jno). \
                            one()
        session["session_site"] = [] 
        session.save()
        session["session_site"] = [site] 
        session.save()
        #print jno
        #print site.id
                            #order_by(desc(JistEstimating3yrBuildingSiteSOW.id)).all()
        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        #for s in scopeofwork:
        #    print s.id
        html1 = """
                            <H4>Scope of Works</H4>
                            %s
                            <table class='table_estdata'>
                            <th>ID</th>
                            <th>Scope</th>
                            <th>Unit</th>
                            <th>Quantity</th>
                            <th>Open Items</th>
                            <th>Edit Scope</th>
                """%('Site ID: ' +str(site.id) +'-'+ site.name)
        temphtml1 = ""
        html2 = ""

        for scp in scopeofwork:
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
                        <td width='25px'>
                            <img src="/images/project-open.png"
                            onclick="loadXMLBQItems(%s)">
                            </img>
                        </td>
                    <td width='25px'>
                            <img src="/images/edit_qty.png"
                            onclick="openeditscope('%s','%s','%s','%s','%s')" return="false">
                            </img>
                    </td>
                    </tr>

                    """%(scp.id,scp.scope,scp.unit,scp.quantity,scp.id,scp.id,scp.scope,scp.unit,scp.quantity,scp.id)
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax3yrstatuschange(self,statcode,jno,**kw):
        #for m in session['session_site']:
        #    jno = m.id
        scopeofwork =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.idsite==jno).all()
        site =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.id==int(jno)). \
                            one()
        contractstatus = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingStatusData). \
                            filter(JistEstimating3yrBuildingStatusData.idsite==jno).one()
        statuscode = contractstatus.statuscode
        if statcode:
            contractstatus.statuscode = str(statcode)
            DBS_Jist3yrBuilding.flush()
            
        #return html
        return 

    @expose()
    def ajax3yrscopeitems(self,scopeid,jcno,**kw):
        scopesitebqitems=DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSOWBQItems). \
                            filter(JistEstimating3yrBuildingSOWBQItems.idscope==scopeid).all()
        sitescope = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.id==scopeid).one()
        #for m in session['session_site']:
        #    jno = m.id
        #    sitename = m.name
        #session["session_scopeitem"].insert(0,[sitescope]) 
        #session.save()
        site =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.id==int(jcno)). \
                            one()
        html1 = """
                            <H4>Scoped Items</H4>
                            %s</br>
                            %s 

                            <table class='table_estdata'>
                            <th>ID</th>
                            <th>Scopeid</th>
                            <th>Description</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                            <th>Edit Qty</th>
                            <th>Remove Item</th>
                """%('Site ID: ' +str(jcno) +' - '+ site.name, 'Scope ID: '+str(sitescope.id) +' - '+ sitescope.scope)
        html2 = ""
        #onclick="loadXMLBQItems(%s)">
        for scp in scopesitebqitems:
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
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                    <td width='25px'>
                            <img src="/images/edit_qty.png"
                            onclick="openbqqty(%s,%s,%s)" return="false">
                            </img>
                    </td>
                    <td width='25px'>
                            <img src="/images/delete.png"
                            onclick="deleteitemscope(%s)" return="false">
                            </img>
                    </td>
                    </tr>
                    """%(scp.id,scp.idscope,scp.description,scp.quantity,scp.price,scp.total,scp.id,scp.quantity,scp.price,scp.id)
            html2 = html2 + temphtml1

        if html2 == "":
            html2 = """

                        <tr>
                        <td >
                            No Records
                            </td>
                        </tr>

                        """

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax3yrremoveitemscope(self,uniqid,scopeitemid,**kw):
        if uniqid == self.last_save_scopeiddeleted:
            return
        scopesitebqitems=DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSOWBQItems). \
                            filter(JistEstimating3yrBuildingSOWBQItems.id==scopeitemid).one()
        #sitescope = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
        #                    filter(JistEstimating3yrBuildingSiteSOW.id==scopeid).one()
        
        #DBS_Jist3yrBuilding.delete(sitescope)
        DBS_Jist3yrBuilding.delete(scopesitebqitems)
        self.last_save_scopeiddeleted = uniqid
        return

    @expose()
    def ajax3yrnewsite(self,name,description='',
                            area='',wonumber='',supervisor='',
                            date=datetime.date(datetime.now()),
                            **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        if self.last_saved_site_rnd == name:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_site = JistEstimating3yrBuildingSites(name = name,
                                       description=description,
                                       wonumber = wonumber,
                                       supervisor = supervisor,
                                       date = date,
                                       area = area,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrBuilding.add(new_site)
        DBS_Jist3yrBuilding.flush()
        newstatus = JistEstimating3yrBuildingStatusData(idsite=new_site.id,
                                        statuscode=1,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        self.last_saved_site_rnd = name 
        DBS_Jist3yrBuilding.add(newstatus)
        DBS_Jist3yrBuilding.flush()

    @expose()
    def ajax3yreditsite(self,siteid,sitedate,sitename,
                        sitedescription,sitewonumber,
                        sitesupervisor,sitearea,
                            **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        thissite =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                            filter(JistEstimating3yrBuildingSites.id==siteid).one()
        thissite.name = sitename
        thissite.description=sitedescription
        thissite.wonumber = sitewonumber
        thissite.supervisor = sitesupervisor
        thissite.date = sitedate
        thissite.area = sitearea
        thissite.useridedited=useridcreated
        thissite.dateedited = datetime.date(datetime.now())
        thissite.timeedited =datetime.time(datetime.now())
        DBS_Jist3yrBuilding.flush()

    @expose()
    def ajax3yraddbqitem_tosite(self,jcno,bqitemid,scopeid,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        if self.last_saved_bqitem_rnd == bqitemid:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        #for m in session['session_site']:
        #jno = session['session_site'][0].id
        #sitescope = session['session_scopeitem'][0][0].id
        #print jno,sitescope,bqitem
        if bqitemid:
            bqitem =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingItems). \
                            filter(JistEstimating3yrBuildingItems.id==bqitemid).one()
            newscopebqitem = JistEstimating3yrBuildingSOWBQItems(id3yritem=bqitem.id,
                            idscope = scopeid,
                            description = bqitem.description,
                            units = bqitem.units,
                            quantity = 0,
                            price = bqitem.price,
                            total = 0,
                           useridnew=useridcreated,
                           useridedited=useridcreated,
                           dateadded = datetime.date(datetime.now()),
                           dateedited = datetime.date(datetime.now()),
                           timeedited =datetime.time(datetime.now()),
                           )
            DBS_Jist3yrBuilding.add(newscopebqitem)
            DBS_Jist3yrBuilding.flush()
            self.last_saved_bqitem_rnd = bqitemid 

        return "" 

    @expose()
    def ajax3yrnewscope(self,name,jcno,unit='',
                            qty='',
                            **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        if self.last_saved_scope_rnd == name:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        #jno = session['session_site'][0].id
        new_scope = JistEstimating3yrBuildingSiteSOW(idsite = jcno,
                                       scope=name,
                                       unit = unit,
                                       quantity = qty,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrBuilding.add(new_scope)
        DBS_Jist3yrBuilding.flush()
        self.last_saved_scope_rnd = name 

    @expose()
    def ajax3yreditscope(self,scopename,jcno,unit='',
                            qty='',thisid=0,
                            **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        if self.last_saved_editscope == scopename:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        meid = int(thisid)
        scopeofwork =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.id==meid).one()
        scopeofwork.scope=str(scopename)
        scopeofwork.unit = unit
        scopeofwork.quantity = qty
        scopeofwork.useridedited=useridcreated
        scopeofwork.dateedited=datetime.date(datetime.now())
        DBS_Jist3yrBuilding.flush()
        self.last_saved_editscope = scopename 
        
    @expose()
    def ajax3yrnewquotescope(self,jno,**kw):
        scopeofwork =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.idsite==jno). \
                            order_by(asc(JistEstimating3yrBuildingSiteSOW.id)).all()
        site =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.id==int(jno)). \
                            one()
        html1 = """
                            <H4>New Quote</H4>
                            %s
                    <form>
                <fieldset>
                """%('Site ID: ' +str(site.id) +'-'+ site.name)
        temphtml1 = ""
        html2 = ""
        for scp in scopeofwork:
            temphtml1 = """
                            <input type="checkbox" name="chkboxscopequote" value="%s"
                            checked="true">
                              %s
                            <br>

                    """%(scp.id,(str(scp.id) +' - ' + scp.scope))
            html2 = html2 + temphtml1

        html3 = """
                <input type="button" value="Create New Quote"
                onclick="javascript:scopecheck();" return="false"">
                </fieldset>
                </form>
                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax3yredit_bqqty(self,qty,siteid,scopeid,bqitemid,bqprice,
                            **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        #print qty, siteid,scopeid,bqitemid 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        bqitems =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSOWBQItems). \
                    filter(JistEstimating3yrBuildingSOWBQItems.id==bqitemid).one()
        if isnumeric(qty): 
            if isnumeric(bqprice):
                bqitems.price=Decimal(bqprice)
            total  = Decimal(qty) * bqitems.price 
            #rate = Decimal(Decimal(str(totalscopedata[0][0]))/Decimal(str(totalqty)))
            bqitems.quantity = qty
            bqitems.total = total
            DBS_Jist3yrBuilding.flush()
        return ''

    @expose()
    def ajax3yraddnewquote(self,jcno,scopearray,
                            **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        #print qty, siteid,scopeid,bqitemid 
        #print self.last_saved_scopelist
        #print type(scopearray)
        if self.last_saved_scopelist == scopearray:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        #scopes = scopearray.split()
        #print scopes, type(scopes)
        new_quote = JistEstimating3yrBuildingQuotes(
                                       idsite = jcno,
                                       estdate = datetime.date(datetime.now()),
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.date(datetime.now()),
                                       dateedited = datetime.date(datetime.now()),
                                       timeedited =datetime.time(datetime.now()),
                                       )
        DBS_Jist3yrBuilding.add(new_quote)
        DBS_Jist3yrBuilding.flush()
        for scp in scopearray.split(','):
            new_quote_scope = JistEstimating3yrBuildingQuoteScope(
                                           idquote = new_quote.id,
                                           idscope = scp,
                                           useridnew=useridcreated,
                                           useridedited=useridcreated,
                                           dateadded = datetime.date(datetime.now()),
                                           dateedited = datetime.date(datetime.now()),
                                           timeedited =datetime.time(datetime.now()),
                                           )
            DBS_Jist3yrBuilding.add(new_quote_scope)
            DBS_Jist3yrBuilding.flush()
            #Get the bqitems for this scope
            scp_recd = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                        filter(JistEstimating3yrBuildingSiteSOW.id==scp).one()
            scp_items = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSOWBQItems). \
                        filter(JistEstimating3yrBuildingSOWBQItems.idscope==scp).all()
            for item in scp_items:
                new_quote_bqitem = JistEstimating3yrBuildingQuoteBQItems(
                                               idquote = new_quote.id,
                                               idbqitem = item.id,
                                               idscope = new_quote_scope.idscope,
                                               description = item.description,
                                               units = item.units,
                                               quantity = item.quantity,
                                               price = item.price,
                                               total = item.total,
                                               useridnew=useridcreated,
                                               useridedited=useridcreated,
                                               dateadded = datetime.date(datetime.now()),
                                               dateedited = datetime.date(datetime.now()),
                                               timeedited =datetime.time(datetime.now()),
                                               )
                DBS_Jist3yrBuilding.add(new_quote_bqitem)
                DBS_Jist3yrBuilding.flush()
        self.last_saved_scopelist = scopearray
        return ''

    @expose()
    def ajax3yrquotespercontract(self,jno,**kw):
        site =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                    filter(JistEstimating3yrBuildingSites.id==jno). \
                            one()
        quotes =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuotes). \
                            filter(JistEstimating3yrBuildingQuotes.idsite==jno). \
                       order_by(desc(JistEstimating3yrBuildingQuotes.id)).all()
        html1 = """
                            <H4>All Quotes</H4>
                            %s
                            <table class='table_estdata'>
                            <th>Quote Number</th>
                            <th>Quote Date</th>
                            <th>View</th>
                            <th>Get Scope </th>
                            <th>Get Rates</th>
                """%('Site ID: ' +str(site.id) +'-'+ site.name)
        temphtml1 = ""
        html2 = ""
        for scp in quotes:
            temphtml1 = """
                    <tr>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                        <td width='25px'>
                            <img src="/images/project-open.png"
                            onclick="LoadXMLQuoteScopesShow(%s)">
                            </img>
                        </td>
                        <td width='25px'>
                            <a href="/estimatingcont/export_3yr_quote_to_pdf/%s"> 
                            <img src="/images/pdficon.jpg">
                            </img>
                            </a>
                        </td>
                    <td width='25px' >
                            <a
                            href="/estimatingcont/export_3yr_quote_to_pdf/%s/ratesonly"> 
                            <img src="/images/pdficon.jpg">
                            </img>
                            </a>
                    </td>
                    <td >
                    </td>
                    </tr>

                    """%(scp.id,scp.estdate,scp.id,scp.id,scp.id)
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax3yrquotescopeshow(self,quoteno,**kw):
        quote =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuotes). \
                            filter(JistEstimating3yrBuildingQuotes.id==quoteno). \
                       order_by(desc(JistEstimating3yrBuildingQuotes.id)).all()
        quotescopes = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteScope). \
                            filter(JistEstimating3yrBuildingQuoteScope.idquote==quoteno). \
                       order_by(desc(JistEstimating3yrBuildingQuoteScope.idscope)).all()
        #for scp in quotescopes:
        #    print scp
            
        html1 = """
                            <H4>Quote Scope of Work</H4>
                            %s
                            <div id="div_add_to_contract">
                            <button id="button_add_quote_to_contract"
                            onclick="loadQuoteToScopeOfWorks(%s)">
                            Add Quote to Scope Of Works For Contract
                            </button>
                            </div>
                            <table class='table_estdata'>
                            <th></th>
                            <th></th>
                            <th></th>
                
                """%('Quote ID: ' +str(quoteno),quoteno)
        temphtml1 = ""
        html2 = ""
        for scp in quotescopes:
            scopeofwork =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.id==scp.idscope).one()
            temphtml1 = """
                    <tr>
                    <td >
                    %s
                    </td>
                    <td >
                    %s
                    </td>
                        <td width='25px'>
                            <img src="/images/project-open.png"
                            onclick="LoadXMLQuoteScopesItemsShow(%s,%s)">
                            </img>
                        </td>
                    </tr>

                    """%(scp.id,scopeofwork.scope,scp.idquote,scp.idscope)
            html2 = html2 + temphtml1

        html3 = """
                            </table>
                            

                """
        html =  html1 + html2 + html3 

        return html

    @expose()
    def ajax3yrquotescopeitemsshow(self,quoteno,scopeid,**kw):
        quote =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuotes). \
                            filter(JistEstimating3yrBuildingQuotes.id==quoteno). \
                       order_by(asc(JistEstimating3yrBuildingQuotes.id)).all()
        quotebqitems = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteBQItems). \
                            filter(JistEstimating3yrBuildingQuoteBQItems.idscope==scopeid). \
                            filter(JistEstimating3yrBuildingQuoteBQItems.idquote==quoteno). \
                       order_by(asc(JistEstimating3yrBuildingQuoteBQItems.id)).all()
            
        html1 = """
                            <H4>Quote Scope Items</H4>
                            %s<br/>
                            %s
                            <table class='table_estdata'>
                            <th>Description</th>
                            <th>Units</th>
                            <th>Quantity</th>
                            <th>Price</th>
                            <th>Total</th>
                """%('Quote ID: '+quoteno,'Scope ID: '+scopeid )
        temphtml1 = ""
        html2 = ""
        for scp in quotebqitems:
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
                    <td>
                    %s
                    </td>
                    <td>
                    %s
                    </td>
                    </tr>

                    """%(scp.description,scp.units,scp.quantity,scp.price,scp.total)
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajax3yrquoteScopeAttachContract(self,uniqid,jcno,quoteno,**kw):
        if self.last_saved_scopecontract == uniqid:
            return
        quote =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuotes). \
                            filter(JistEstimating3yrBuildingQuotes.id==int(quoteno)). \
                            one()
        quotescopes = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteScope). \
                            filter(JistEstimating3yrBuildingQuoteScope.idquote==quoteno). \
                       order_by(desc(JistEstimating3yrBuildingQuoteScope.idscope)).all()
        datanew = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        for qscope in quotescopes:
            scopeofwork = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                                filter(JistEstimating3yrBuildingSiteSOW.id==qscope.idscope). \
                                one()
            scopeofworktotal = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSOWBQItems). \
                                filter(JistEstimating3yrBuildingSOWBQItems.idscope==qscope.idscope). \
                                value(func.sum(JistEstimating3yrBuildingSOWBQItems.total))
            if scopeofworktotal is None:
                scopeofworktotal = 0.00
            #else:
            #scopeofworktotal = format_decimal(scopeofworktotal,format='#,##0.00;-#0.00',locale='en')
            datanew.append({
                            'jcno':jcno,
                            'quoteno':quoteno,
                            'scopeid':scopeofwork.id,
                            'scopedescription':scopeofwork.scope,
                            'scopeunit':scopeofwork.unit,
                            'scopeqty':scopeofwork.quantity,
                            'scopetotal':scopeofworktotal
                            })
        for data in datanew:
            #print data
            #print float(data['scopetotal'])
            #print float(data['scopeqty'])
            thisprice = float(data['scopetotal'])/float(data['scopeqty'])
            newcontractscope = JistContractScope(jno=data['jcno'],
                                         quoteno=data['quoteno'],
                                         description=data['scopedescription'],
                                         unit=data['scopeunit'],
                                         qty=data['scopeqty'],
                                         price=thisprice,
                                         total=data['scopetotal'],
                                         dateadded = datetime.now(),
                                         dateedited = datetime.now(),
                                         useridnew=useridcreated,
                                         useridedited=useridcreated
                                       )
            
            newcontractscope
            DBS_ContractData.add(newcontractscope)
            DBS_ContractData.flush()
        self.last_saved_scopecontract = uniqid
        return

    @expose()
    def export_3yr_quote_to_pdf(self,quoteno,flag="scopeonly"):
        import random
        locale.setlocale(locale.LC_ALL, '')
        totalbal = 0
        totalbalance = 0
        quote =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuotes). \
                            filter(JistEstimating3yrBuildingQuotes.id==quoteno). \
                       one()
        quotescopes = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteScope). \
                            filter(JistEstimating3yrBuildingQuoteScope.idquote==quoteno). \
                       order_by(desc(JistEstimating3yrBuildingQuoteScope.idscope)).all()
        this_site = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSites). \
                            filter(JistEstimating3yrBuildingSites.id==quote.idsite). \
                            one()
        rnd1 = random.random()
        rnd1 = str(rnd1).split('.')[1]
        tmpname ="QuoteSOW"+'-'+self.building_3yr_tender_number+'-'+str(this_site.id)+'-' 
        fnamesow = tmpname+'-'+str(datetime.now()).split(' ')[0] + rnd1 +'.pdf'
        filenamesow = os.path.join(pdf_dirname, str(fnamesow))
        rnd2 = random.random()
        rnd2 = str(rnd2).split('.')[1]
        tmpname2 ="QuoteRates"+'-'+self.building_3yr_tender_number+'-'+str(this_site.id)+'-' 
        fnamerates = tmpname2+'-'+str(datetime.now()).split(' ')[0] + rnd2 +'.pdf'
        filenamerates = os.path.join(pdf_dirname, str(fnamerates))
        pdffile1 = CreateEstimating3yrPDF(filenamesow)
        pdffile2 = CreateEstimating3yrPDF(filenamerates)
        wip1 = []
        userdata = []
        datascopes = []
        for k in quotescopes:
            onescope =DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSiteSOW). \
                            filter(JistEstimating3yrBuildingSiteSOW.id==k.idscope). \
                               one()
            datascopes.append({'scopeid':k.idscope,
                               'quoteid':k.idquote,
                               'scopename':onescope.scope,
                               'scopeunit':onescope.unit,
                               'scopeqty':onescope.quantity,
                               'scopetotal':0,
                               'itemdict':[]
                             })
        qtotalexcl = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteBQItems). \
                    filter(JistEstimating3yrBuildingQuoteBQItems.idquote==quoteno). \
                     value(func.sum(JistEstimating3yrBuildingQuoteBQItems.total))
        if qtotalexcl is None:
            qtotalexcl = 0.00
        quotetotalexcl = format_decimal(qtotalexcl,format='#,##0.00;-#0.00',locale='en')
        for s in datascopes:
            quotebqitems = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteBQItems). \
                                filter(JistEstimating3yrBuildingQuoteBQItems.idquote==quoteno). \
                                filter(JistEstimating3yrBuildingQuoteBQItems.idscope==s['scopeid']). \
                           order_by(desc(JistEstimating3yrBuildingQuoteBQItems.id)).all()

            quotescopetotal = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingQuoteBQItems). \
                        filter(JistEstimating3yrBuildingQuoteBQItems.idquote==quoteno). \
                        filter(JistEstimating3yrBuildingQuoteBQItems.idscope==s['scopeid']). \
                        value(func.sum(JistEstimating3yrBuildingQuoteBQItems.total))
            if quotescopetotal is None:
                scopetotalexcl = 0.00
            else:
                scopetotalexcl = format_decimal(quotescopetotal,format='#,##0.00;-#0.00',locale='en')
            s['scopetotal'] = scopetotalexcl 
            for k in quotebqitems:
                bqitem = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSOWBQItems). \
                        filter(JistEstimating3yrBuildingSOWBQItems.id==k.idbqitem).one() 
                item =  DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingItems). \
                        filter(JistEstimating3yrBuildingItems.id==bqitem.id3yritem).one() 
                subheading = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
                        filter(JistEstimating3yrBuildingSubHeadings.id==item.idsubheading).one()
                heading = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingHeadings). \
                        filter(JistEstimating3yrBuildingHeadings.id==subheading.idheading).one()
                schedule = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSchedules). \
                        filter(JistEstimating3yrBuildingSchedules.id==heading.idschedule).one()
                s['itemdict'].append({
                        'units' : k.units,
                        'quantity' : k.quantity,
                        'itemdescription' : k.description,
                        'itemid' : item.itemno,
                        'itemprice' : k.price,
                        'itemtotal' : k.total,
                        'subheading' : subheading.description, 
                        'heading' : heading.description, 
                        'schedule' : schedule.description, 
                        'scheduleid' : schedule.id,
                })
        _sitetempid = '%0.3d' %int(this_site.id)
        _siteid =  self.building_3yr_tender_number +" - "+ str(_sitetempid)
        userdata.append({
            'quotedate':quote.estdate,
            'sitename':this_site.name,
            'siteid':_siteid,
            'quoteid':quote.id,
            'wonumber':this_site.wonumber,
            'area':this_site.area,
            'supervisor':this_site.supervisor,
                        })
        headers_scopes =["Scope ID","Scope Description","Scope Unit","Scope Qty","Scope Total Excl"]
        headerwidths_scopes=[70,300,80,100,100]
        headers_rates =["Scope ID","Schedule","Heading","Sub Heading","Item ID","Item Description","Units","Quantity","Price","Total Excl"]
        headerwidths_rates=[40,100,100,150,40,150,50,50,50,60]
        if flag == "scopeonly":
            pdffile1.CreatePDF3yrEstimatingScope(userdata,datascopes,headers_scopes,headerwidths_scopes,quotetotalexcl)
            response.headers["Content-Type"] = 'application/pdf'
            response.headers["Content-Disposition"] = 'attachment;filename="'+fnamesow+'"'
            filecontent = file(filenamesow, "r")
        elif flag == "ratesonly":
            pdffile2.CreatePDF3yrEstimatingRates(userdata,datascopes,headers_rates,headerwidths_rates,quotetotalexcl)
            response.headers["Content-Type"] = 'application/pdf'
            response.headers["Content-Disposition"] ='attachment;filename="'+fnamerates+'"'
            filecontent = file(filenamerates, "r")
        return  filecontent


def isnumeric(value):
    return str(value).replace(".", "").replace("-", "").isdigit()


