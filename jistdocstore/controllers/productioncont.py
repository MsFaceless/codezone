# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
from tg.decorators import paginate
import math
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
#from tw.extjs import ItemSelector
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
import jistdocstore.lib.jist_google_reportlab as ReportLabGoogle 
#from jistdocstore.model import DBSession, metadata
from formencode import validators
#from tw.jquery import FlotWidget
#from tw.forms.fields import TextField, TextArea, CheckBox
#from tw.jquery import AjaxForm
#from tw.api import WidgetsList
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import FileStoreProduction
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
import shutil
import string
import re
import json
#import simplejson, urllib
from pkg_resources import resource_filename
from babel.numbers import format_currency, format_number, format_decimal
from jistdocstore.lib.jistfileuploader import qqFileUploader
from PIL import Image
from PIL.ExifTags import TAGS
#from ming import create_datastore
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
UPLOAD_DIRECTORY = os.path.join(public_dirname ,"production_pictures/")
current_filestore_contract_id = 0 
GoogleKeyAPI = '&key=AIzaSyAq-Ji88xFVYLxTGIPfKnTV_P8VKdjpo2I'
GoogleKeyAPIClean = 'key=AIzaSyAq-Ji88xFVYLxTGIPfKnTV_P8VKdjpo2I'
JistLat = '-33.973064746048856'
JistLng = '18.695168495178223'
__all__ = ['ProductionController']


class ProductionController(BaseController):
    """Sample controller-wide authorization"""
    
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_(''))

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def index(self):
        redirect('productioncont/menu')

    @expose('jistdocstore.templates.production.productionindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Production: Main Menu') 
    
    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.wip')
    def wip(self,**named):
        """Handle the 'wip' page."""
        tmpl_context.widget = spx_contracts_table 
        value = contracts_filler.get_value(values={},offset=0,order_by='jno',desc=True)
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

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.get_one_contract')
    def get_one(self, jno_id,**named):
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jno_id).one()
        lasteditedperson = DBS_ContractData.query(User).filter(User.user_id==statusall.useridedited).one()
        point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
        statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
        try:
            conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
        except:
            conplandates = None

        timeframe = {'orderdate':contract.orderdate,
                 'sitehandover':statusall.sitehandoverdate,
                 'startdate':statusall.actualstartdate,
                 'firstdel':statusall.firstdeldate,
                 'finalcompl':statusall.finalcompldate,
                 'lasttoedit':statusall.useridedited,
                 'timeedit':statusall.dateedited}
        try:
            agent = DBS_ContractData.query(User).filter(User.user_id==statusall.siteagent).one()
            status = {'statuscode':statcode.status,
                      'pointperson':statusall.pointperson,
                      'siteagent':statusall.siteagent}
        except:
            status = {'statuscode':statcode.status,
                      'pointperson':statusall.pointperson,
                      'siteagent':'1'}
        #print conplandates.planstartdate

        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.jcno==jno_id). \
                order_by(asc(JistSubconPaymentRunsData.paylist_id)). \
                all()
        emps = DBS_JistLabour.query(JistSubconList). \
                all()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.jcno==jno_id). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        #print p1total
        paymentrun = []
        for k in subcondata:
            payrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                    filter(JistSubconPaymentRunsList.id==k.paylist_id). \
                    one()
            emps = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.id==k.sub_id). \
                    one()
            paymentrun.append({'pay_date':payrun.payment_date,'payment_number':payrun.id,'subcon':emps.trading_name})

        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        count = len(subcondata) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            subcondata, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page = "Viewing JCNo:",
                    cont=contract,
                    scp=scope,
                    stus=status,
                    plandates=conplandates,
                    wip = items,
                    thiscurrentPage=currentPage,
                    #employee = emps,
                    paymentrun = paymentrun,
                    init_value = 1,
                    selfname = 'get_one',
                    runid= 1,
                    totalexcl = p1total,
                    jcno = jno_id,
                    pdfstring ="/export_subcon_jcnoall_summary_pdf/"+jno_id,
                    timef=timeframe,
                    point=statusall.pointperson
                    )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.newcontract')
    def newcontract(self, **kw):
        """Handle the 'new contract' page."""
        tmpl_context.widget = add_new_contract_form
        return dict(newcontract=kw)

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.newsitediaryentry')
    def newsitediary(self,jno_id,**kw):
        """Handle the new sitediary page."""
        tmpl_context.widget = add_new_sitediary_form
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        return dict(page="newsitediary",
                newsitediary=kw,
                cont= contract
                    )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.sitediarymain')
    def sitediarymain(self,jno_id,**named):
        """Handle the sitediarymain page."""
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        contracttsksreplies = DBS_ContractData.query(SiteDiaryContracts). \
                   filter(SiteDiaryContracts.jcno==jno_id). \
                   order_by(desc(SiteDiaryContracts.datecreated)).all()
        contractcount = len(contracttsksreplies) 
        page =int( named.get( 'page', '1' ))
        contract_currentPage = paginate.Page(
            contracttsksreplies, page, item_count=contractcount,
            items_per_page=5,
        )
        sitediaryitems = contract_currentPage.items
        #tmpl_context.widget = add_new_sitediary_form
        return dict(page='sitediarymain',
                   cont = contract,
                   contractsitediary= sitediaryitems,
                   currentPage=contract_currentPage,
                   jno = jno_id,
                   count = contractcount
                    )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    #@validate(ajax_form)
    @expose('jistdocstore.templates.production.searchcontract')
    def searchcontract(self,**named):
        """Handle the 'sitesearch' page."""
        #tmpl_context.widget = TextField() 
        from_data = [["AL","Alabama"], ["AK","Alaska"], ["AZ","Arizona"], ["AR","Arkansas"], ["CA","California"],["WY","Wyoming"]]
        to_data = []
        item_selector = ItemSelector(divID='item_selector_div',
                                 width=850,
                                 url='/productioncont/dummysave',
                                 fieldLabel='States',
                                 labelWidth=40,
                                 fromData=from_data,
                                 toData=to_data,
                                 msWidth=400,
                                 msHeight=400,
                                 dataFields=['code','desc'],
                                 valueField='code',
                                 displayField='desc',
                                 fromLegend='Available',
                                 toLegend='Selected',
                                 submitText='Save',
                                 resetText='Reset')
        #tmpl_context.widget = item_selector 

        flot = FlotWidget(id='flotSample', width='320px',height='160px',
            label='Simple Flot Example')
        #tmpl_context.flot = flot
        d1 = [(0.5*i, math.sin(0.5*i)) for i in range(0,28)]
        d2 = [(0, 3), (4, 8), (8, 5), (9, 13)]
        # a None value signifies separate line segments
        d3 = [(0, 12), (7, 12), None, (7, 2.5), (12, 2.5)]
        #ajax_form = AjaxForm(id="myAjaxFormSearch",
        #            fields=CommentFields(),
        #            target="output",
        #            action="do_search")

        tmpl_context.form = site_ajax_form 
        #tmpl_context.form = item_selector 
        #value = contracts_filler.get_value(values={},offset=0,order_by='jno',desc=True)
        #from tg.decorators import paginate
        #count = len(value) 
        #page =int( named.get( 'page', '1' ))
        #currentPage = paginate.Page(
        #    value, page, item_count=count,
        #    items_per_page=15,
        #)
        #items = currentPage.items

        return dict(page='sitesearch',
                    wip = '',
                    currentPage=1,
                    count=1,
                    data=[d1, d2, d3],
                    value=named)

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.searchcontract_description')
    def searchcontract_description(self,**named):
        """Handle the 'sitesearch' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=DescriptionSearch(),
                    target="output",
                    action="do_search_description")

        tmpl_context.form = ajax_form 
        #value = contracts_filler.get_value(values={},offset=0,order_by='jno',desc=True)
        #from tg.decorators import paginate
        #count = len(value) 
        #page =int( named.get( 'page', '1' ))
        #currentPage = paginate.Page(
        #    value, page, item_count=count,
        #    items_per_page=15,
        #)
        #items = currentPage.items

        return dict(page='sitesearch',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(site_ajax_form)
    def do_search(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        sitename = "%(site_search)s" % kw
        searchphrase = "%"+sitename+"%"
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.site.like(searchphrase)). \
                                           filter(JistContracts.completed=="False"). \
                                           order_by(desc(JistContracts.jno)).all()
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>JCNo</th>
                    <th>Client </th>
                    <th>Site </th>
                    <th>Description</th>
                    <th>Point</th>
                    <th>Site Agent</th>
                    <th>Completed</th>
                    """
        sitedata = sitedata + headerdata
        for k in contract:
            status = DBS_ContractData.query(JistContractStatus). \
                    filter(JistContractStatus.jno==k.jno).one()
            point = User.by_user_id(status.pointperson)
            siteagent = User.by_user_id(status.siteagent)
            if not siteagent: 
                thissiteagent = "Nobody"
            else:
                thissiteagent = siteagent.user_name
            sitedatatemp = """<tr><td><a href='/productioncont/get_one/%s'>%s</a></td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <td>%s</td>
                                  <p/>
                                  </tr>
                            """ % (k.jno,
                                    k.jno,
                                    k.client,
                                    k.site,
                                   k.description,
                                   point.user_name,
                                   thissiteagent,
                                   k.completed)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    #@validate(ajax_form)
    def do_search_description(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        sitename = "%(contract_description_search)s" % kw
        searchphrase = "%"+sitename+"%"
        contract = DBS_ContractData.query(JistContracts). \
                        filter(JistContracts.description.like(searchphrase)). \
                        filter(JistContracts.completed=="False"). \
                        order_by(desc(JistContracts.jno)).all()
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>JCNo</th>
                    <th>Client </th>
                    <th>Site </th>
                    <th>Description</th>
                    <th>Completed</th>
                    """
        sitedata = sitedata + headerdata
        for k in contract:
            status = DBS_ContractData.query(JistContractStatus). \
                    filter(JistContractStatus.jno==k.jno).one()
            sitedatatemp = """<tr><td><a href='/productioncont/get_one/%s'>%s</a></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><p/></tr>
                            """ % (k.jno,k.jno,k.client,k.site,
                                   k.description,k.completed)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def dummysave(self,**kw):
        redirect("/productioncont/menu")
        return 

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.update_status')
    def update_status(self,jno_id,**kw):
        """Handle the 'status update contract' page."""
        #print jno_id
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        status = DBS_ContractData.query(JistContractStatus). \
                filter(JistContractStatus.jno==jno_id).one()
        cont = contract
        val = status_changer_filler.get_value(values={
            'jno':int(jno_id),'id':int(jno_id),'statuscode':str(status.statuscode)
            })
        #for k,w in val.iteritems():
        #    print k,w
        tmpl_context.widget = status_contract_form 
        return dict(cont=contract,status_update=val,came_from=url('/productioncont/update_status/'+jno_id))

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def savestatus(self,*args,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        status = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==kw['id']).one()
        #print args
        #print status.point.user_id
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        status.pointperson = kw['pointperson']
        status.siteagent = kw['siteagent']
        status.statuscode = kw['statuscode']
        status.sitehandoverdate = kw['sitehandoverdate']
        status.actualstartdate = kw['actualstartdate']
        status.firstdeldate = kw['firstdeldate']
        status.finalcompldate = kw['finalcompldate']
        status.useridedited = usernow.user_id
        status.dateedited = datetime.date(datetime.now())
        DBS_ContractData.flush()
        flash('Contract Status saved !!!!')
        redirect('/productioncont/get_one/'+kw['id'])

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.productionpages')
    def productionpages(self,**named):
        """Handle the 'productionpages'."""
        return dict(page='productionpages')

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.sitediarymain')
    def sitediarymain(self,jno_id,**named):
        """Handle the sitediarymain page."""
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        contracttsksreplies = DBS_ContractData.query(SiteDiaryContracts). \
                   filter(SiteDiaryContracts.jcno==jno_id). \
                   order_by(desc(SiteDiaryContracts.datecreated)).all()
        contractcount = len(contracttsksreplies) 
        page =int( named.get( 'page', '1' ))
        contract_currentPage = paginate.Page(
            contracttsksreplies, page, item_count=contractcount,
            items_per_page=5,
        )
        sitediaryitems = contract_currentPage.items

        tmpl_context.widget = add_new_sitediary_form
        return dict(page='sitediarymain',
                   cont = contract,
                   contractsitediary= sitediaryitems,
                   currentPage=contract_currentPage,
                   jno = jno_id,
                   count = contractcount
                    )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    #@expose('jistdocstore.templates.production.fileupload_form')
    def uploadpic(self,jno_id,**kw):
        """Handle the uploads-page."""
        #contract = DBS_ContractData.query(JistContracts).get(jno_id)
        #current_files = DBS_JistFileStore.query(FileStoreProduction).all()
        #tmpl_context.widget = add_file_to_contract 
        #jno = {'jcno':contract.jno}
        #print jno
        return dict(jno=jno,cont=contract,value=kw,user_names=DBS_ContractData.query(User).all())
    
    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.upload')
    def uploadpic(self,jno_id,**kw):
        """Handle the uploads-page."""
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        file_under_options = DBS_JistFileStore.query(PictureCategory).distinct()
        #for i in file_under_options:
        #    print i
        value = dict(jcno=contract.jno)
        tmpl_context.widget = add_file_to_contract 
        return dict(fileunderoptions=file_under_options,
                cont=contract,
                value=value,
                user_names=DBS_ContractData.query(User).filter(User.active_status=='True').all()
                )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.view_files')
    def view_files(self,jno_id,**kw):
        """Handle the uploads-page."""
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        current_files = DBS_JistFileStore.query(FileStoreProduction). \
                            filter(FileStoreProduction.jcno==jno_id). \
                            order_by(desc(FileStoreProduction.id)).all()
        tmp_files = current_files
        tmpl_context.widget = spx_contract_file_list 
        val = contracts_file_filler.get_value(values={'jno':int(jno_id)},offset=0,order_by='jno',desc=False)
        htmlstuff = {'jno':str(jno_id),'picid':str('4')}
        filecount = len(current_files) 
        page =int(kw.get( 'page', '1' ))
        contract_currentPage = paginate.Page(
            current_files, page, item_count=filecount,
            items_per_page=5,
        )
        fileitems = contract_currentPage.items
        return dict(
                cont=contract,
                value = val,
                current_files=fileitems,
                currentPage=contract_currentPage,
                htmlstuff = htmlstuff
                )

    @expose('jistdocstore.templates.production.planning_dates')
    def contract_plan_dates(self,jno_id,**kw):
        contract = DBS_ContractData.query(JistContracts).get(jno_id)
        contractdates = None
        try:
            contractdates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
            if contractdates:
                val = plandates_changer_filler.get_value(values={'id':contractdates.id,'jcno':jno_id})
                #for k,w in val.iteritems():
                tmpl_context.widget = plandates_contract_form 
        except:
            jcno = jno_id 
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            useridcreated = usernow.user_id
            new_contractdates = JistContractPlanningDates(jcno = jcno,
                                           useridnew = str(useridcreated),
                                           #dateadded = datetime.now(),
                                           #dateedited = datetime.now(),
                                           useridedited = useridcreated
                                           )
            DBS_ContractData.add(new_contractdates)
            DBS_ContractData.flush()
            contractdates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
            if contractdates:
                val = plandates_changer_filler.get_value(values={'id':contractdates.id,'jcno':jno_id})
                #for k,w in val.iteritems():
                tmpl_context.widget = plandates_contract_form 

        return   dict(cont=contract,
                      plan_dates=val,
                      came_from=url('/productioncont/contract_plan_dates/'+jno_id))

    @expose()
    def savecontractplanningdates(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        jcno = kw['jcno'] 
        cdates = DBS_ContractData.query(JistContractPlanningDates). \
                    filter(JistContractPlanningDates.jcno==jcno).one()
        cdates.planstartdate = kw['planstartdate']
        cdates.planenddate = kw['planenddate']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        cdates.useridnew = str(useridcreated)
        cdates.useridedited = str(useridcreated)
        DBS_ContractData.flush()
        redirect("/productioncont/get_one/"+jcno)

    @expose()
    #@validate(add_file_to_contract,error_handler=uploadpic())
    def savefile(self,*arg,**kw):
        jno = kw['jcno']
        filename = kw['filename']
        takenbyname = kw['takenby']
        takenby = kw['takenby'] 
        datetaken = kw['datetaken']
        fileunder = kw['fileunder']
        description = kw['description']
        filename = kw['filename']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #see to create the jno folder
        #try:
        jno_path = os.path.join(pics_dirname, str(jno))
        #Check File Size
        #uploadsize = os.path.getsize(filename.value)
        uploadsize = len(filename.value)
        ##print "Upload Size = %s"%(uploadsize/1024)
        if uploadsize == 0 or uploadsize/1024 > 1024*5:
            flash(_('File to big or nothing loaded. Max Size 5MB...'), 'warning')
            redirect("/productioncont/view_files/"+jno)
        new_file = FileStoreProduction(filename=filename.filename,
                                       jcno = jno,
                                       takenby=takenby,
                                       description=description,
                                       fileunder=fileunder,
                                       datetaken=datetaken,
                                       useridcreated=usernow.user_id
                                       )
        DBS_JistFileStore.add(new_file)
        DBS_JistFileStore.flush()
        #except:
        #flash(_('File Upload Failed'), 'warning')
        #redirect("/productioncont/view_files/"+kw['jcno'])
        try:
            os.makedirs(jno_path)
        except OSError:
            #ignore if the folder already exists
            pass
        #write the file to the jno directory
        pic_path = os.path.join(jno_path, str(new_file.id))
        try:
            os.makedirs(pic_path)
        except OSError:
            #ignore if the folder already exists
            pass
        thispic_path = os.path.join(pic_path, new_file.filename)
        main_picpath = thispic_path
        #f = open(thispic_path, 'wb', 10000)
        f = file(thispic_path, "w")
        f.write(kw['filename'].value)
        f.close()

        uploadedfilename = new_file.filename
        basefilename = string.join(re.split("\.", uploadedfilename)[0:-1], ".")
        thumbnailname = basefilename  + ".gif"
        thumbnailpath = os.path.join(pic_path ,thumbnailname)
        new_file.thumbname = thumbnailname
        self.getthumbnail(main_picpath,thumbnailpath)
        self.writejcno(main_picpath,main_picpath)
        flash("File successfully saved.")
        redirect("/productioncont/view_files/"+jno)

    def getthumbnail(self, inpath, outpath):
        retcode = subprocess.call(['convert',inpath,'-resize','100x100',outpath])

    def writejcno(self, inpath, outpath):
        retcode = subprocess.call(['convert',inpath,'-annotate','(100,200)','This Number',outpath])

    @require(in_any_group("managers","production"))
    @expose('jistdocstore.templates.production.fileuploadconsole')
    def fileuploadconsole(self,**named):
        """Handle the 'fileupload new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()

        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id

        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()

        return dict(page='Picture Upload Console',
                    contracts = contracts,
                    users = activeusers,
                    myjistid = myid)

    @expose()
    #@expose('json')
    def uploadfile(self,*arg,**kw):
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
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        uploader = qqFileUploader(int(pictakenby),kw,None, [".jpg",".jpeg",".JPG",".JPEG", ".png", ".ico", ".*"], 2147483648)
        #print uploader.getName()
        big_file_path, thumb_path = uploader.handleUpload()
        #print big_file_path, thumb_path
        big_file_base = os.path.basename(big_file_path) 
        thumb_file_base = os.path.basename(thumb_path) 
        usersharetable = []
        new_file = FileStoreProduction(filename=big_file_base,
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
        DBS_JistFileStore.add(new_file)
        DBS_JistFileStore.flush()
        return json.dumps({"success": True})

    @expose()
    #@expose('json')
    def myuploads(self,*arg,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        datestart = kw['startdate']
        dateend = kw['enddate']
        if not datestart:
            todaydate = datetime.date(datetime.now()) 
            datestart = datetime.date(datetime.now()) - timedelta(weeks=1)
            dateend = datetime.date(datetime.now()) 
        if not dateend:
            dateend = datetime.date(datetime.now()) 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myuploadlist_byid = DBS_JistFileStore.query(FileStoreProduction).filter_by(takenby=usernow.user_id).all()
        myuploadlist_date = DBS_JistFileStore.query(FileStoreProduction.datetaken). \
                    filter(FileStoreProduction.takenby==usernow.user_id). \
                    filter(FileStoreProduction.datetaken>=datestart). \
                    filter(FileStoreProduction.datetaken<=dateend). \
                    order_by(desc(FileStoreProduction.datetaken)). \
                    distinct()
        htmltemp = ''
        htmlout = """<h5 class="ui-widget-header">View Pictures Uploaded Between: %s and %s</h5>"""%(datestart,dateend)
        htmlclose = ''
        for upload in myuploadlist_date:
            #print upload[0]
            htmlheader = """
                        <div class="">
                        <h5 class="ui-widget-header">%s</h5>
                        """%(upload[0])
            myuploadlist_bydate = DBS_JistFileStore.query(FileStoreProduction). \
                    filter(FileStoreProduction.datetaken==str(upload[0])). \
                    order_by(desc(FileStoreProduction.datetaken)). \
                    all()
            htmlout =  htmlout + htmlheader 
            for thisupload in myuploadlist_bydate:
                #print thisupload.takenby, usernow.user_id
                if thisupload.takenby == usernow.user_id: 
                    #print thisupload.thumbname, thisupload.filename
                    userpath = os.path.join('/production_pictures', str(usernow.user_id))
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
        return htmlout + htmlclose

    @expose()
    #@expose('json')
    def uploads_shared_view(self,*arg,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        activeusersall = DBS_ContractData.query(User).filter(User.active_status==1).all()
        sharedpiclist = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.user_id==usernow.user_id).all()
        htmlmiddle = ''
        htmlhead =""" 
                    <div id ="staff_faces_available_div_shared" class = "staff_photo_carousel responsive">
                    <h3 class="ui-widget-header">Available Users</h3>
                            <ul id="staff_faces_available_carousel_shared">
                """
        for user in activeusersall:
            htmltemp = """
                                    <img  value="%s"
                                    src="/images/staffpics/%s.png" alt="%s" title="%s" width="80px" height="80px" />
                                    <br/>
                                    </img>
                         """%(user.user_id,user.user_id,user.user_name,user.user_name)
            htmlmiddle = htmlmiddle + htmltemp
        htmlend = """</ul></div><div id='my_upload_list_pics_shared'></div>"""
        htmlout = htmlhead + htmlmiddle + htmlend
        return htmlout

    @expose()
    #@expose('json')
    def uploads_shared_thumbs_per_user(self,sharerid,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        usersharer = User.by_user_id(int(sharerid))
        sharedpicrawlist = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.user_id==usernow.user_id). \
                filter(PictureSharing.sharer_id==int(sharerid)). \
                    order_by(asc(PictureSharing.sharer_id)). \
                all()
        htmlheader = """
                    <div class="">
                    <h5 class="ui-widget-header">Picture Uploads Taken By %s Shared With Me.</h5>
                    """%(usersharer.user_name)
        htmlout = ''
        for sharedpic in sharedpicrawlist[::-1]:
            thisupload = DBS_JistFileStore.query(FileStoreProduction). \
                    filter(FileStoreProduction.pic_id==sharedpic.pic_id). \
                    one()
            userpath = os.path.join('/production_pictures', str(thisupload.takenby))
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
                    
    @expose()
    #@expose('json')
    def uploads_thumbs_per_jcno(self,jcno,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        htmlheader = """
                    <div class="">
                    <h5 class="ui-widget-header">Picture Uploads For JCNo %s .</h5>
                    """%(jcno)
        htmlout = ''
        thisuploads = DBS_JistFileStore.query(FileStoreProduction). \
                filter(FileStoreProduction.jcno==int(jcno)). \
                all()
        for thisupload in thisuploads[::-1]:
            userpath = os.path.join('/production_pictures', str(thisupload.takenby))
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
                    
    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.jist_pic_viewer')
    def production_pic_viewer(self,**kw):
        fname = kw['fname']
        thisupload = DBS_JistFileStore.query(FileStoreProduction). \
                filter(FileStoreProduction.filename==fname). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #print myuploadlist_bydate
        userpath = os.path.join('/production_pictures', str(thisupload.takenby))
        #thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        #srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        userowner = User.by_user_id(thisupload.takenby)
        activeusersall = DBS_ContractData.query(User).filter(User.active_status==1).all()
        nobody = DBS_ContractData.query(User).filter(User.user_id==1).all()
        sharedusers = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.pic_id==thisupload.pic_id).all()
        if not sharedusers:
            sharedusers = DBS_ContractData.query(User).filter(User.user_id==1).all()
        activeusers = []
        #activeusers = [user for user in activeusersall for userid in sharedusers if user.user_id != userid.user_id]
        for usr in activeusersall:
            blnshared = False
            for share in sharedusers:
                if usr.user_id == share.user_id:
                    blnshared = True
                    break
            if not blnshared:
                activeusers.append(usr)
        return dict(page='JIST Picture Viewer',
                   srcpic=srcpic,
                   srcid=thisupload.pic_id,
                   thisupload=thisupload,
                   owner=userowner.user_name,
                   activeusers = activeusers,
                   sharedusers = sharedusers,
                   )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.jist_pic_viewer_shared')
    def production_pic_viewer_shared(self,**kw):
        fname = kw['fname']
        thisupload = DBS_JistFileStore.query(FileStoreProduction). \
                filter(FileStoreProduction.filename==fname). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #print myuploadlist_bydate
        userpath = os.path.join('/production_pictures', str(thisupload.takenby))
        #thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        #srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        userowner = User.by_user_id(thisupload.takenby)
        activeusersall = DBS_ContractData.query(User).filter(User.active_status==1).all()
        nobody = DBS_ContractData.query(User).filter(User.user_id==1).all()
        sharedusers = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.pic_id==thisupload.pic_id).all()
        activeusers = []
        for usr in activeusersall:
            blnshared = False
            for share in sharedusers:
                if usr.user_id == share.user_id:
                    blnshared = True
                    break
            if not blnshared:
                activeusers.append(usr)
                

        return dict(page='JIST Picture Viewer - Shared Pictures',
                   srcpic=srcpic,
                   srcid=thisupload.pic_id,
                   thisupload=thisupload,
                   owner=userowner.user_name,
                   activeusers = activeusers,
                   sharedusers = sharedusers,
                   )

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.production.jist_pic_viewer_jcno')
    def production_pic_viewer_jcno(self,**kw):
        fname = kw['fname']
        thisupload = DBS_JistFileStore.query(FileStoreProduction). \
                filter(FileStoreProduction.filename==fname). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #print myuploadlist_bydate
        userpath = os.path.join('/production_pictures', str(thisupload.takenby))
        #thumbpath = os.path.join(userpath, 'thumbs')
        bigpicpath = os.path.join(userpath, 'pics')
        #srcthumb = os.path.join(thumbpath, thisupload.thumbname)
        srcpic = os.path.join(bigpicpath, thisupload.filename)
        userowner = User.by_user_id(thisupload.takenby)
        activeusersall = DBS_ContractData.query(User).filter(User.active_status==1).all()
        nobody = DBS_ContractData.query(User).filter(User.user_id==1).all()
        sharedusers = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.pic_id==thisupload.pic_id).all()
        activeusers = []
        for usr in activeusersall:
            blnshared = False
            for share in sharedusers:
                if usr.user_id == share.user_id:
                    blnshared = True
                    break
            if not blnshared:
                activeusers.append(usr)
                

        return dict(page='JIST Picture Viewer - Pictures By Contract',
                   srcpic=srcpic,
                   srcid=thisupload.pic_id,
                   thisupload=thisupload,
                   owner=userowner.user_name,
                   activeusers = activeusers,
                   sharedusers = sharedusers,
                   )


    @expose()
    def addpicturesharing(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        userid = kw['userid']
        picid = kw['currentpicid']
        new_pic_sharing = PictureSharing(user_id = userid,
                                       pic_id=picid,
                                       sharer_id = usernow.user_id
                                       )
        DBS_JistFileStore.add(new_pic_sharing)
        DBS_JistFileStore.flush()

    @expose()
    def deletepicturesharing_from_sharer(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        userid = usernow.user_id 
        picid = kw['currentpicid']
        thispic = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.user_id == int(userid)). \
                filter(PictureSharing.pic_id == int(picid)). \
                one()
        DBS_JistFileStore.delete(thispic)
        DBS_JistFileStore.flush()

    @expose()
    def deletepicturesharing_from_owner(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #userid = usernow.user_id 
        picid = kw['currentpicid']
        userid = kw['userid']
        thispic = DBS_JistFileStore.query(PictureSharing). \
                filter(PictureSharing.user_id == int(userid)). \
                filter(PictureSharing.pic_id == int(picid)). \
                one()
        DBS_JistFileStore.delete(thispic)
        DBS_JistFileStore.flush()

    @expose()
    def rotate_pic(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        thisupload = DBS_JistFileStore.query(FileStoreProduction). \
                filter(FileStoreProduction.pic_id==kw["currentpicid"]). \
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


    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def savenewdiaryentry(self,jno_id,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        jcno = jno_id 
        entry = kw['entry']
        report_date = kw['report_date']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_sitediary = SiteDiaryContracts(jcno = jcno,
                                       entry=entry,
                                       report_date=report_date,
                                       owner=useridcreated
                                       )
        DBS_ContractData.add(new_sitediary)
        DBS_ContractData.flush()

        flash("Site Diary entry successfully saved.")

        redirect("/productioncont/sitediarymain/"+jcno)

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def view(self,jcno, fileid):
        try:
            userfile = DBS_JistFileStore.query(FileStoreProduction).filter_by(id=fileid).one()
        except:
            redirect("/productioncont/view_files/"+jcno)
        content_types = {
            'display': {'.png': 'image/jpeg', '.jpeg':'image/jpeg', 
                        '.jpg':'image/jpeg', '.gif':'image/jpeg', 
                        '.txt': 'text/plain','.JPG':'image/jpeg','.JPEG':'image/jpeg'
                        },
            'download': {'.pdf':'application/pdf', '.zip':'application/zip', '.rar':'application/x-rar-compressed'}
        }
        for file_type in content_types['display']:
            if userfile.filename.endswith(file_type):
                response.headers["Content-Type"] = content_types['display'][file_type]
                jno_path = os.path.join(pics_dirname, str(jcno))
                pic_path = os.path.join(jno_path,str(fileid))
                pic_name = os.path.join(pic_path,str(userfile.filename))
                filecontent = file(pic_name, "r")
                return filecontent
        for file_type in content_types['download']:
            if userfile.filename.endswith(file_type):
                response.headers["Content-Type"] = content_types['download'][file_type]
                response.headers["Content-Disposition"] = 'attachment; filename="'+userfile.filename+'"'
                jno_path = os.path.join(pics_dirname, str(jcno))
                pic_path = os.path.join(jno_path,str(fileid))
                pic_name = os.path.join(pic_path,str(userfile.filename))
                filecontent = file(pic_name, "r")
                return filecontent
            else:
                response.headers["Content-Type"] = content_types['download'][file_type]
                response.headers["Content-Disposition"] = 'attachment; filename="'+userfile.filename+'"'
                jno_path = os.path.join(pics_dirname, str(jcno))
                pic_path = os.path.join(jno_path,str(fileid))
                pic_name = os.path.join(pic_path,str(userfile.filename))
                filecontent = file(pic_name, "r")
                return filecontent

        if userfile.filename.find(".") == -1:
            response.headers["Content-Type"] = "text/plain"
            jno_path = os.path.join(pics_dirname, str(jcno))
            pic_path = os.path.join(jno_path,str(fileid))
            pic_name = os.path.join(pic_path,str(userfile.filename))
            filecontent = file(pic_name, "r")
            return filecontent

    @expose()
    def delete(self, fileid):
        try:
            userfile = DBSession.query(FileStoreProduction).filter_by(id=fileid).one()
        except:
            return redirect("/productioncont/")
        DBSession.delete(userfile)
        return redirect("/productioncont/")

    @expose()
    def ajaxgetmanagesiteagents(self,usrid='1',**kw):
        if not usrid:
            usrid = '1'
        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.siteagent==int(usrid)). \
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
            wip1.append({'jno':w.jno,
                         'client':w.client,
                         'site':w.site,
                         'description':w.description,
                         'status':statcode.status,
                         'pointperson':statusall.siteagent
                         })
        html1 = """

                        <p id="contractheader">
                        Site Agent Contracts for %s <br/>Last updated: %s 
                        <a href="/productioncont/exportsinglesiteagentpdf/%s">
                        <img src="/images/pdficon.jpg"></img>
                        </a>
                        </p>
                            <table class='table_estdata'>
                            <th>JCno</th>
                            <th>Client</th>
                            <th>Site</th>
                            <th>Description</th>
                            <th>Status</th>
                """%(user.user_name,dt,user.user_id)
        temphtml1 = ""
        html2 = ""
        for scp in wip1:
            temphtml1 = """
                    <tr>
                    <td >
                    <a href = "/productioncont/get_one/%s">
                    %s
                    </a>
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
                    """%(scp['jno'],scp['jno'],scp['client'],scp['site'],scp['description'],scp['status'])
            html2 = html2 + temphtml1

        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html
    
    @expose()
    def exportsinglesiteagentpdf(self,siteagent):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
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
                filter(JistContractStatus.siteagent==siteagent). \
                order_by(desc(JistContracts.jno)). \
                all()
        wip1 = []
        for w in wip:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==w.jno).one()
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==w.jno).one()
                planstart = datetime.date(conplandates.planstartdate)
                planend = datetime.date(conplandates.planenddate)
            except:
                planstart = '' 
                planend = ''

            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            wip1.append({'jno':w.jno,
                         'client':w.client,
                         'site':w.site,
                         'description':w.description,
                         'planstart':planstart,
                         'planend':planend,
                         'status':statcode.status,
                         'pointperson':statusall.siteagent
                         })
        
        count = len(wip1) 
        pointperson_name = User.by_user_id(siteagent).user_name
        userdata.append([datetime.date(datetime.now()),
                        "Site Agent Contracts For %s"%pointperson_name,
                        ""
                        ])
        headers =["JCNo","Client","Site","Description","Plan Start","Plan End","Status"]
        headerwidths=[40,120,200,200,60,60,80]
        pdffile.CreatePDFPointContracts(userdata,wip1,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def do_search_outofoffice_movements_per_person(self, **kw):
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
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        userid = usernow.user_id
        openorders = DBS_ContractData.query(JistOutOfOfficeNotices).filter(JistOutOfOfficeNotices.dateadded>=startdate). \
                                              filter(JistOutOfOfficeNotices.dateadded<=enddate). \
                                              filter(JistOutOfOfficeNotices.for_user==userid). \
                                              order_by(desc(JistOutOfOfficeNotices.dateadded)).  \
                                              all()
        datenow = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        supplier_text = "<H3 align='center'>Out Of Office Movements For %s</H3><p/>"%datenow
        table = "<table class='tabletabs'>"
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

    @expose('jistdocstore.templates.production.productioncalendar')
    def productioncalendar(self,**kw):
        thistime = datetime.now() 
        twoweek = []
        for i in range(30):
            thisnow = datetime.now() + timedelta(days=i-7)
            thisplus = datetime.date(datetime.now()) + timedelta(days=i-7)
            weekdayint = datetime.weekday(thisplus)
            weekdayname = thisplus.strftime('%A')
            twoweek.append({"weekdayint": weekdayint,
                            "weekdayname": weekdayname,
                            "date":thisplus,
                            "datetime":thisnow,
                            })
            #print weekdayname
            #print weekdayint
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
                    if permis.permission_name=='production':
                        pointlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name,
                                          'display_name':point.display_name
                                          })
        return dict(page='Production Calendar',
                    twoweek = twoweek,
                    points = pointlist,
                    )
    
    @expose('jistdocstore.templates.production.productioncalendar2')
    def productioncalendar_weekly(self,**kw):
        thistime = datetime.now() 
        twoweek = []
        for i in range(30):
            thisnow = datetime.now() + timedelta(days=i-7)
            thisplus = datetime.date(datetime.now()) + timedelta(days=i-7)
            weekdayint = datetime.weekday(thisplus)
            weekdayname = thisplus.strftime('%A')
            twoweek.append({"weekdayint": weekdayint,
                            "weekdayname": weekdayname,
                            "date":thisplus,
                            "datetime":thisnow,
                            })
            #print weekdayname
            #print weekdayint
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
                    if permis.permission_name=='production':
                        pointlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name,
                                          'display_name':point.display_name
                                          })

        return dict(page='Production Calendar',
                    twoweek = twoweek,
                    points = pointlist,
                    )

    @expose('jistdocstore.templates.production.production_openlayers')
    def production_openlayers(self,**kw):
        return dict(page='Production Open Layers',
                    #twoweek = twoweek,
                    #points = pointlist,
                    )

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
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(today,sttimestart)
        enddate = datetime.combine(today,sttimeend)
        openorders = DBS_ContractData.query(JistOutOfOfficeNotices).filter(JistOutOfOfficeNotices.dateadded>=startdate). \
                                              filter(JistOutOfOfficeNotices.dateadded<=enddate). \
                                              filter(JistOutOfOfficeNotices.for_user==thisuseridnew). \
                                              order_by(desc(JistOutOfOfficeNotices.dateadded)).  \
                                              all()
        datenow = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        supplier_text = "<H3 align='center'>My Out of Office Movements For %s</H3><p/>"%datenow
        table = "<table class='tabletabs'>"
        headerdata = """
                    <th>For User</th>
                    <th>Site </th>
                    <th>Other Destination</th>
                    <th>Purpose</th>
                    <th>Est Hr There</th>
                    <th>Time Start</th>
                    <th>Added By</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in openorders:
            tr = "<tr class='tablestandard'><td>"
            sitedatatemp = "<img src='/images/staffpics/%s.png'/></td>"%str(k.for_user)
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
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+"</p>"+tr+sitedatatemp+ \
                    fromperson+callback+callagain+nomsgs+ \
                    messg+returntel+trclose
        sitedata = sitedata+"</table>"
        return sitedata 

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
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        openorders = DBS_ContractData.query(JistReceptionTelephoneMessages). \
                                              filter(JistReceptionTelephoneMessages.to_user==thisuseridnew). \
                                              filter(JistReceptionTelephoneMessages.active==1). \
                                              order_by(desc(JistReceptionTelephoneMessages.dateadded)).  \
                                              all()
        datenow = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        supplier_text = "<H2 align='center'>My Active Telephone Messages </H2><p/>"
        table = "<table id='tbltelephonemsg_per_person' class='tabletabs'>"
        headerdata = """
                    <th>ID</th>
                    <th>To User</th>
                    <th>From Person </th>
                    <th>Message</th>
                    <th>Return Tel Number</th>
                    <th>Added By</th>
                    <th>Date Time Added</th>
                    <th>Deactivate</th>
                    """
        sitedata = supplier_text + table + headerdata
        for k in openorders:
            tr = """<tr class='tablestandard'><td>
                    %s</td><td>
                 """%k.id
            sitedatatemp = "<img src='/images/staffpics/%s.png' align=right/></td>"%str(k.to_user)
            fromperson =""" 
                            <td>%s</td>
                            """%(k.from_person)
            messg =""" 
                            <td>%s</td>
                            """%(k.message)
            returntel =""" 
                            <td width=80px>%s</td>
                            """%(k.return_tel)
            whoadded ="<td><img src='/images/staffpics/%s.png'/></td>"%str(k.useridnew)
            added =""" 
                            <td>%s</td>
                            """%(k.dateadded)
            trclose   ="""
                        <td><img id='deactivate_telephonemsg'src='/images/trash.png'/></td>
                        </tr>
                       """
            sitedata = sitedata+"</p>"+tr+sitedatatemp+ \
                    fromperson+ \
                    messg+returntel+whoadded+added+trclose
        sitedata = sitedata+"""</table> <img id="jisttabfooter" src="/images/jistfooter.png"/>"""
    
        return sitedata 

    @expose()
    def toggletelephonemsg_active(self,id,**kw):
        wip1 = DBS_ContractData.query(JistReceptionTelephoneMessages). \
                filter(JistReceptionTelephoneMessages.id==id). \
                one()
        if wip1.active == False:
            wip1.active = 1
        else:
            wip1.active = 0
        DBS_ContractData.flush()

    @expose()
    def getmyjistbioinfo(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        #telephonecallsum = DBS_ContractData.query(func.count(JistReceptionTelephoneMessages.id)). \
        #                                      filter(JistReceptionTelephoneMessages.to_user==thisuseridnew). \
        #                                      filter(JistReceptionTelephoneMessages.active==1)
        #                                      value(func.count(JistSubconPaymentRunsData.id))
        telephonecallsum = DBS_ContractData.query(JistReceptionTelephoneMessages). \
                                              filter(JistReceptionTelephoneMessages.to_user==thisuseridnew). \
                                              filter(JistReceptionTelephoneMessages.active==1). \
                                              value(func.count(JistReceptionTelephoneMessages.id))
        wipsum = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==int(thisuseridnew)). \
                value(func.count(JistContracts.jno))
        transportsum = DBS_JistFleetTransport.query(JistTransportList). \
                filter(JistTransportList.user_active == 1). \
                filter(JistTransportList.request_person == usernow.user_id). \
                value(func.count(JistTransportList.id))
        reqsitemssum = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.useridnew==int(thisuseridnew)). \
                     filter(JistBuyingPurchaseReqsItems.useractive==True). \
                     value(func.count(JistBuyingPurchaseReqsItems.id))
        activetelcalls = """
                         <div class='my_bio_info'>My Active Telephone
                         Calls:<span style="float:right; margin-right:10px"><strong>%s</strong></span></div>
                         """%str(telephonecallsum)
        activepointcontracts = """
                         <div class='my_bio_info'>My Active Point Contracts: <span style="float:right; margin-right:10px"><strong>%s</strong></span></div>
                         """%str(wipsum)
        activepurchasereqs = """
                         <div class='my_bio_info'>My Active Purchase Reqs: <span style="float:right; margin-right:10px"><strong>%s</strong></span></div>
                         """%str(reqsitemssum)
        activetransportreqs = """
                         <div class='my_bio_info'>My Active Transport Reqs: <span style="float:right; margin-right:10px"><strong>%s</strong></span></div>
                         """%str(transportsum)
        activerentals = """
                         <div class='my_bio_info'>My Active Rentals: <span style="float:right; margin-right:10px"><strong>%s</strong></span></div>
                         """%str('[Coming Soon]')
        activemeetings = """
                         <div class='my_bio_info'>My Scheduled Meetings: <span style="float:right; margin-right:10px"><strong>%s</strong></span></div>
                         """%str('[Coming Soon]')

        return activetelcalls + activepointcontracts + activepurchasereqs + activetransportreqs + activerentals+ activemeetings

    @expose('jistdocstore.templates.production.googlemaps')
    def googlemaps(self, **kw):
        return dict(page='Directions - Routes - Maps',
                    #twoweek = twoweek,
                    #points = pointlist,
                    )

    @expose()
    def export_pdf_div(self):
        html = """
                
                <a href='/productioncont/export_google_street_view/20'><img src="/images/pdficon.jpg"></img>Export To PDF</a>

                """
        return '' 

    @expose()
    def get_my_saved_locations(self,**kw):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        locationlist = DBS_ContractData.query(JistLocationList). \
                filter(JistLocationList.active==True). \
                filter(JistLocationList.useridnew==usernow.user_id). \
                order_by(desc(JistLocationList.id)). \
                all()
        outputlist = []
        for k in locationlist:
            screenview = "<img value='%s' class='location_screenview' src='/images/kview.png'/>"%(k.id)
            mapdirections = "<img value='%s' class='export_directions' src='/images/pdficon.jpg'></img>"%(k.id)
            streetviewpics = "<a href='/productioncont/export_google_street_view?lat=%s&lng=%s'><img src='/images/pdficon.jpg'></img></a>"%(k.lat,k.lng)
            trashpic = "<img value='%s' class='location_trash' src='/images/trash.png' alt=''/>"%(k.id)
            outputlist.append({
                         'id':k.id,
                         'lat':k.lat,
                         'lng':k.lng,
                         'description':k.description,
                         'active':k.active,
                         'screenview':screenview,
                         'streetview':streetviewpics,
                         'mapdirections':mapdirections,
                         'deactivate':trashpic
                         })
        headers =["ID","View","Description","Delete"]
        dictlist = ['id','screenview','description','deactivate']
        headerwidths=[50,35,'',35,'','',50,80,35,80,50,50,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','','','']
        htmltbl = self.build_google_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_my_locations")
        title = """
                <h5 class="ui-widget-shadow">My Places of Interest</h5>
                """
        return title + htmltbl

    @expose()
    @expose('json')
    def get_single_location(self,locationid,**kw):
        locationlist = DBS_ContractData.query(JistLocationList). \
                filter(JistLocationList.id==locationid). \
                one()
        listloc = locationlist.lat+','+locationlist.lng
        #return listloc
        return json.dumps({'lat':locationlist.lat,'lng':locationlist.lng})

    def build_google_html_table(self,dictlist,headers,headerwidths,outputlist,tdclassnames,tblname):
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
    def save_location(self,**kw):
        #for k , w in kw.iteritems():
            #print k, w
        lat = float(kw['dialog_lat'])
        lng = float(kw['dialog_lng'])
        format_lat = format_decimal(lat,format='#,##0.0000###############;-#0.0000###############',locale='en')
        format_lng = format_decimal(lng,format='#,##0.0000###############;-#0.0000###############',locale='en')
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        newlocation = JistLocationList()
        newlocation.lat = format_lat
        newlocation.lng = format_lng
        newlocation.description = kw['description_location']
        newlocation.useridnew = thisuseridnew
        newlocation.useridedited = thisuseridnew
        newlocation.active = 1 
        DBS_ContractData.add(newlocation)
        DBS_ContractData.flush()

    @expose()
    def deactivate_location(self,loc,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        location = DBS_ContractData.query(JistLocationList). \
                filter(JistLocationList.id==loc). \
                one()
        location.active = 0 
        DBS_ContractData.flush()
        return


    @expose()
    def export_google_street_view(self,**kw):
        #print "Got Here"
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        fname = "JIST-Google-Direction-Maps-"+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = ReportLabGoogle.CreatePDFA4(filename)
        contractdata = []
        wip1 = []
        lat = kw['lat']
        lng = kw['lng']
        #lat = '-33.973064746048856'
        #lng = '18.695168495178223'
        loc = lat +','+ lng
        size = '300x150'
        heading90 = '90'
        heading270 = '270'
        heading180 = '180'
        heading0 = '0'
        pitch = '0'
        sensor = 'false'
        param0 = '&heading='+heading0
        param90 = '&heading='+heading90
        param180 = '&heading='+heading180
        param270 = '&heading='+heading270
        GoogleKeyAPI = '&key=AIzaSyAq-Ji88xFVYLxTGIPfKnTV_P8VKdjpo2I'
        params = '&size='+size+'&location='+loc+'&pitch='+pitch+'&sensor='+sensor+GoogleKeyAPI
        streetpage = 'http://maps.googleapis.com/maps/api/streetview?'
        imgstring = streetpage + params + param0

        userdata = {
                'title1_header':'JIST Maps:', 'title1':'Location Map - Directions - Coordinates View ',
                'title2_header':'Latitude', 'title2':lat,
                'title3_header':'Longitude', 'title3':lng,
                'title4_header':'Provider', 'title4':'Google Maps',
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
                'image_path1':streetpage+params+param0, 
                'image_path2':streetpage+params+param90, 
                'image_path3':streetpage+params+param180, 
                'image_path4':streetpage+params+param270, 
                } 
        #filter(JistTransportScheduling.fleet_id==fleetid). \
        #dictlist = ['id','date_scheduled','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        #headerwidths=[40,60,90,90,90,90,100,90,50,50,40,40,40,40,50,32,32]
        #tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFGoogleStreetView(userdata)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_google_directions(self,**kw):
        #print "Got Here"
        #for k, w in kw.iteritems():
            #print k, w
        import random
        #import simplejson, urllib
        myroute = json.loads(kw['route'])
        #print myroute['duration']['text']
        #for keys in myroute.keys():
            #print keys
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        fname = "JIST-Google-Direction-Maps-"+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = ReportLabGoogle.CreatePDFA4(filename)
        contractdata = []
        wip1 = []
        lat = kw['lat']
        lng = kw['lng']
        center = 'center='+lat +','+ lng
        zoom16 = '&zoom=16'
        zoom15 = '&zoom=15'
        zoom14 = '&zoom=14'
        zoom13 = '&zoom=13'
        zoom12 = '&zoom=12'
        zoom09 = '&zoom=09'
        size = '&size=600x300'
        maptype = '&maptype=roadmap'
        sensor = '&sensor=false'
        markerto = '&markers=color:blue%%7Clabel:T%%7C' + lat+','+lng 
        params16 = center + zoom16 + size + sensor + GoogleKeyAPI 
        params15 = center + zoom15 + size + sensor + GoogleKeyAPI 
        params14 = center + zoom14 + size + sensor + GoogleKeyAPI 
        params13 = center + zoom13 + size + sensor + GoogleKeyAPI 
        params12 = center + zoom12 + size + sensor + GoogleKeyAPI 
        params09 = center + zoom09 + size + sensor + GoogleKeyAPI 
        mappage = 'http://maps.googleapis.com/maps/api/staticmap?'
        #mappage = 'http://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&sensor=false'
        #print mappage + params 
        outputlist = []
        for x in myroute['steps']:
            outputlist.append((
                             Paragraph(x['instructions'],pdffile.styleNormal),
                              ))
        #return
        mappage16 = mappage + params16 + markerto
        mappage15 = mappage + params15 + markerto
        mappage14 = mappage + params14 + markerto
        mappage13 = mappage + params13 + markerto
        mappage12 = mappage + params12 + markerto
        mappage09 = mappage + params09 + markerto
        #print outputlist
        driving_time = myroute['duration']['text']
        driving_km_all = myroute['distance']['text']
        startaddress = myroute['start_address']
        endaddress = myroute['end_address']
        try:
            location = DBS_ContractData.query(JistLocationList). \
                    filter(JistLocationList.lat==lat). \
                    filter(JistLocationList.lng.like(lng)). \
                    first()
                    #filter(JistLocationList.lat==lat). \
            locationstring = location.description
        except:
            locationstring = "Not Found" 
        userdata = {
                'title1_header':'JIST Maps:', 'title1':'Location Map - Directions - Coordinates View ',
                'title2_header':'Start Address', 'title2':startaddress,
                'title3_header':'End Address', 'title3':endaddress,
                'title4_header':'Location Description', 'title4':locationstring,
                'datenow_header': "Date Printed", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'Est Distance', 'headerl1':driving_km_all,
                'headerl2_header':'Est Time', 'headerl2':driving_time,
                'headerl3_header':'Printed By', 'headerl3':username,
                'id_header_header': "", 'id_header':'',
                'headerl4_header':'', 'headerl4':' ',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                'image_path1':mappage16, 
                'image_path2':mappage15, 
                'image_path3':mappage12, 
                'image_path4':mappage09, 
                'path_map':mappage09, 
                'directions_path':mappage09, 
                } 
        #filter(JistTransportScheduling.fleet_id==fleetid). \
        #dictlist = ['id','date_scheduled','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        headers =["Instruction","Duration","Distance"]
        headerwidths=[240,60,60,90,90,90,100,90,50,50,40,40,40,40,50,32,32]
        #tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFGoogleMap(userdata,outputlist,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_google_maps(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        import random
        #import simplejson, urllib
        #myroute = json.loads(kw['route'])
        #print myroute['duration']['text']
        #for keys in myroute.keys():
            #print keys
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        fname = "JIST-Google-Direction-Maps-"+ rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = ReportLabGoogle.CreatePDFA4(filename)
        contractdata = []
        wip1 = []
        lat = kw['lat']
        lng = kw['lng']
        jcno = kw['jcno']
        site = kw['site']
        center = 'center='+lat +','+ lng
        zoom16 = '&zoom=16'
        zoom15 = '&zoom=15'
        zoom14 = '&zoom=14'
        zoom13 = '&zoom=13'
        zoom12 = '&zoom=12'
        zoom09 = '&zoom=09'
        size = '&size=600x300'
        maptype = '&maptype=roadmap'
        sensor = '&sensor=false'
        markerto = '&markers=color:blue%%7Clabel:T%%7C' + lat+','+lng 
        params16 = center + zoom16 + size + sensor + GoogleKeyAPI 
        params15 = center + zoom15 + size + sensor + GoogleKeyAPI 
        params14 = center + zoom14 + size + sensor + GoogleKeyAPI 
        params13 = center + zoom13 + size + sensor + GoogleKeyAPI 
        params12 = center + zoom12 + size + sensor + GoogleKeyAPI 
        params09 = center + zoom09 + size + sensor + GoogleKeyAPI 
        mappage = 'http://maps.googleapis.com/maps/api/staticmap?'
        #mappage = 'http://maps.googleapis.com/maps/api/staticmap?center=Brooklyn+Bridge,New+York,NY&zoom=13&size=600x300&maptype=roadmap&sensor=false'
        #print mappage + params 
        outputlist = []
        #for x in myroute['steps']:
            #outputlist.append((
                             #Paragraph(x['instructions'],pdffile.styleNormal),
                              #))
        #return
        mappage16 = mappage + params16 + markerto
        mappage15 = mappage + params15 + markerto
        mappage14 = mappage + params14 + markerto
        mappage13 = mappage + params13 + markerto
        mappage12 = mappage + params12 + markerto
        mappage09 = mappage + params09 + markerto
        #print outputlist
        #driving_time = myroute['duration']['text']
        #driving_km_all = myroute['distance']['text']
        #startaddress = myroute['start_address']
        #endaddress = myroute['end_address']
        try:
            location = DBS_ContractData.query(JistLocationList). \
                    filter(JistLocationList.lat==lat). \
                    filter(JistLocationList.lng.like(lng)). \
                    first()
                    #filter(JistLocationList.lat==lat). \
            locationstring = location.description
        except:
            locationstring = "Not Found" 
        userdata = {
                'title1_header':'JIST Maps:', 'title1':'Site Location Map ',
                'title2_header':'Site', 'title2':site,
                'title3_header':'JCNo', 'title3':jcno,
                'title4_header':'Location Description', 'title4':locationstring,
                'datenow_header': "Date Printed", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':'',
                'headerl3_header':'', 'headerl3':'',
                'id_header_header': "", 'id_header':'',
                'headerl4_header':'', 'headerl4':' ',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                'image_path1':mappage16, 
                'image_path2':mappage15, 
                'image_path3':mappage12, 
                'image_path4':mappage09, 
                'path_map':mappage09, 
                'directions_path':mappage09, 
                } 
        #filter(JistTransportScheduling.fleet_id==fleetid). \
        #dictlist = ['id','date_scheduled','time_scheduled','from_place','from_area','to_place','to_area','special_inst','request_person','dateadded','scheduled',]
        headers =["Instruction","Duration","Distance"]
        headerwidths=[240,60,60,90,90,90,100,90,50,50,40,40,40,40,50,32,32]
        #tdclassnames=['','','','','','','','','','','','tdspacer','','','']
        #htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_all")
        pdffile.CreatePDFGoogleMapOnly(userdata,outputlist,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def get_dialog_saved_locations_directions(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id

        alllocations = DBS_ContractData.query(JistLocationList). \
                filter(JistLocationList.active==1). \
                filter(JistLocationList.useridnew==thisuseridnew). \
                order_by(desc(JistLocationList.id)). \
                all()
                #filter(JistLocationList.lat==lat). \

        html1 = """
                <div id="dialog_choose_locations" title="Get Directions Between Locations">
                    <form id="dialog_choose_locations_frm">
                        <fieldset>
                            <label for="">Location Start</label><br/>
                            <select id='location_start' name='location_start' class="text ui-widget-content ui-corner-all" >

                  """
        html2 = ''
        for m in alllocations: 
            html2temp = """
                          <option value="%s,%s,%s">%s</option>
                    """%(m.id,m.lat,m.lng,m.description)
            html2 = html2 + html2temp

        html3 = """</select><br/>
                    <label for="">Location End</label><br/>
                    <select id='location_end' name='location_end' class='text ui-widget-content ui-corner-all' >
        
                """
                            
        for m in alllocations: 
            html3temp = """
                          <option value="%s,%s,%s">%s</option>
                    """%(m.id,m.lat,m.lng,m.description)
            html3 = html3 + html3temp

        html4 = """
                        </select>
                        </fieldset>
                        </form>
               </div>
                """
        return html1 + html2 + html3 + html4    


    @require(in_any_group("managers","production"))
    @expose('jistdocstore.templates.production.contacts_console')
    def contacts_console(self,**named):
        """Handle the 'Contacts new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()

        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id

        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()

        return dict(page='Company Employee Contacts Console',
                    contracts = contracts,
                    users = activeusers,
                    myjistid = myid)

    @require(in_any_group("managers","production"))
    @expose('jistdocstore.templates.production.site_address_console')
    def site_address_console(self,**named):
        """Handle the 'Contacts new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()

        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        myid = usernow.user_id

        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()

        return dict(page='Site Address Console',
                    contracts = contracts,
                    users = activeusers,
                    myjistid = myid)

    @expose()
    def get_site_address_list_html(self,**kw):
        pointlist = []
        productionlist = []
        accountslist = []
        outputlist = []
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
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
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
                    filter(JistContracts.locationid!=None). \
                    order_by(desc(JistContracts.jno)).all()

        for thisites in contracts:
            try:
                location = DBS_ContractData.query(JistLocationList). \
                        filter(JistLocationList.id==int(thisites.locationid)). \
                        one()
                loclat = location.lat
                loclng = location.lng
            except:
                loclat = 0 
                loclng = 0 
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
            try:
                location = DBS_ContractData.query(JistLocationList). \
                        filter(JistLocationList.id==int(thisites.locationid)). \
                        one()
                screenview = "<img value='%s' class='location_screenview' src='/images/kview.png'/>"%(location.id)
                streetviewpics = "<a href='/productioncont/export_google_street_view?lat=%s&lng=%s'><img src='/images/pdficon.jpg'></img></a>"%(location.lat,location.lng)
                mapdirections = "<img value='{0}' class='export_site_directions' lat='{1}' lng='{2}' site='{3}' jcno='{4}' src='/images/kview.png'></img>".format(location.id, location.lat,
                                                                                                                                                            location.lng, thisites.site, thisites.jno)
                trashpic = "<img value='%s' class='location_trash' src='/images/trash.png' alt=''/>"%(location.id)
                add_lat = location.lat
                add_lng = location.lng

            except:
                streetviewpics = "None"
                mapdirections = "None"
                trashpic = "None"
                add_lat = 0  
                add_lng =  0 

            outputlist.append({'jno':thisites.jno,
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
                         'loclat':add_lat,
                         'loclng':add_lng,
                         'streetview':streetviewpics,
                         'mapdirections':mapdirections,
                         'deactivate':trashpic
                         })
        headers =["ID","Site","Description","Point","Directions"]
        dictlist = ['jno','site','description','pointperson','mapdirections']
        headerwidths=[50,235,'',130,'30','',50,80,35,80,50,50,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','','','','tdrightalign']
        htmltbl = self.build_google_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_sites_locations")
        header = """<h5 class="modal-content">Active Sites With Saved Locations <span class='spanright'> {0} locations </span></h5>""".format(len(outputlist))
        return header + htmltbl

    def build_contracts_html_table(self,dictlist,headers,headerwidths,outputlist,tdclassnames,tblname):
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

    def geocode(self,address,sensor, **geo_args):
        GEOCODE_BASE_URL = 'http://maps.googleapis.com/maps/api/geocode/json'
        geo_args.update({
            'address': address,
            'sensor': sensor,  
        })

        url = GEOCODE_BASE_URL + '?' + urllib.urlencode(geo_args)
        result = simplejson.load(urllib.urlopen(url))

        print simplejson.dumps([s['formatted_address'] for s in result['results']], indent=2)

    if __name__ == '__main__':
        geocode(address="San+Francisco",sensor="false")
