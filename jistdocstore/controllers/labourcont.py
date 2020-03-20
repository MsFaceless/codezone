# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, has_any_permission
from tg.decorators import paginate
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from jistdocstore.lib.base import BaseController
#from jistdocstore.lib.jistdocstorereportlab import *
from jistdocstore.lib.jist_labour_reportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.lib.jistfileuploader import qqFileUploader
from jistdocstore.model.userfile import FileStoreProduction
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
import random
from babel.numbers import format_currency, format_number, format_decimal
import json
from PIL import Image
from PIL.ExifTags import TAGS
import base64
from reportlab.platypus import BaseDocTemplate, Frame, Paragraph, NextPageTemplate, PageBreak, PageTemplate, Image
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
images_dir = os.path.join(public_dirname, 'images')
labour_picdir = os.path.join(images_dir, 'labourpics')
staff_picdir = os.path.join(images_dir, 'staffpics')
subcon_picdir = os.path.join(images_dir, 'subconpics')

__all__ = ['LabourController']

class LabourController(BaseController):
    """Sample controller-wide authorization"""
    has_permission = has_any_permission('manage','productionmanage','labour', msg=l_('Only for people with the "labour" permission'))
    
    #@identity.require(identity.not_anonymous())
    @expose()
    def index(self):
        redirect('labourcont/menu')

    @expose('jistdocstore.templates.labour.labourindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Labour: Main Menu') 

    @expose('jistdocstore.templates.labour.showlabourdivisionsall')
    def showlabourdivisionsall(self,**named):
        tmpl_context.widget = spx_divisions_labour_list
        #request.identity.not_anonymous() # User is logged in
        #k = request.identity.current.user # Logged in user object
        #print k
        value = labour_divisions_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View All Labour Divisions',
                    wip = items,
                    selfname = 'showlabourdivisionsall',
                    thiscurrentPage=currentPage,
                    count=count)

    @expose('jistdocstore.templates.labour.divisionnew')
    def division_new(self,**named):
        tmpl_context.form = add_new_labour_division_form
        return dict(page='New Direct Labour Division Form',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    action='/labourcont/savenewdivision')

    @expose()
    def savenewdivision(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = JistLabourDivisions()
        u.division_name = kw['division_name']
        u.division_leader = kw['division_leader']
        u.active = True
        u.useridnew = usernow.user_id
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        u.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(u)
        DBS_JistLabour.flush()
        emp = "LABDIV"+str(int(u.id)+999)
        editdiv = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==u.id). \
                one()
        editdiv.division_code =emp
        redirect("/labourcont/showlabourdivisionsall")

    @expose('jistdocstore.templates.labour.editdivisions')
    def editdivisions(self,*arg,**named):
        val = labour_division_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = labour_division_list_form 
        return dict(page='Edit Labour Divisions',
                   action='/labourcont/saveeditdivisions/'+str(arg[0]),
                   userid = str(arg[0]),
                   value=val
                   )

    @expose()
    def saveeditdivisions(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        div = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==arg[0]). \
                one()
        #for k, w in enumerate(kw):
        #    print k, w, kw[w]
        #return
        div.division_name = kw['division_name']
        div.division_leader = kw['division_leader']
        div.useridnew = usernow.user_id
        div.useridedited = usernow.user_id
        div.dateedited = datetime.date(datetime.now()) 
        div.dateadded = datetime.date(datetime.now()) 
        if type(kw['active'])==list:
            div.active = 1
        elif type(kw['active'])==unicode:
            div.active = 0
        else:
            pass
        flash("Division successfully edited.")
        redirect("/labourcont/showlabourdivisionsall")
    
    @expose('jistdocstore.templates.labour.showlabourall')
    def showlabourall(self,**named):
        tmpl_context.widget = spx_labour_list
        value = labour_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View All Labour',
                    wip = items,
                    thiscurrentPage=currentPage,
                    selfname = 'showlabourall',
                    pdfstring = "export_labour_list_all_pdf",
                    count=count)

    @expose('jistdocstore.templates.labour.showactivelabourall')
    def showactivelabourall(self,**named):
        tmpl_context.widget = spx_active_labour_list
        value = labour_active_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View All Active Labour',
                    wip = items,
                    thiscurrentPage=currentPage,
                    pageinfo = named,
                    selfname = 'showactivelabourall',
                    pdfstring = "export_labour_list_active_pdf",
                    count=count)

    @expose('jistdocstore.templates.labour.editlabour')
    def editlabour(self,*arg,**named):
        val = labour_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = labour_list_form 
        return dict(page='edit labour',
                   action='/labourcont/saveeditlabour/'+str(arg[0]),
                   userid = str(arg[0]),
                   value=val
                   )

    @expose('jistdocstore.templates.labour.labournew')
    def labour_new(self,**named):
        tmpl_context.form = add_new_labour_form
        return dict(page='New Labour Form',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    action='/labourcont/savenewlabour')


    @expose('jistdocstore.templates.labour.showpaymentruns')
    def showlabourpaymentruns(self,**named):
        tmpl_context.widget = spx_payment_runs_labour_list
        value = payment_runs_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View Labour Payment Runs',
                    wip = items,
                    thiscurrentPage=currentPage,
                    pdfstring = "export_labour_payment_runs_pdf",
                    count=count)

    @expose('jistdocstore.templates.labour.paymentrunnew')
    def paymentrun_new(self,**named):
        tmpl_context.form = add_new_payment_run_form
        return dict(page='New Payment Run Labour',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    action='/labourcont/savenewlabourpayment')

    @expose('jistdocstore.templates.labour.editlabourpaymentrun')
    def editlabourpaymentrun(self,*arg,**named):
        val = payment_run_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = payment_run_list_form 
        return dict(page='Edit Payment Run Labour',
                   action='/labourcont/saveeditlabourpaymentlist/'+str(arg[0]),
                   userid = str(arg[0]),
                   value=val
                   )

    @expose()
    def savenewlabourpayment(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newlist = JistLabourPaymentRunsList()
        newlist.payment_date = kw['payment_date']
        newlist.start_date = kw['start_date']
        newlist.end_date = kw['end_date']
        newlist.active = 1 
        newlist.useridnew = usernow.user_id
        newlist.useridedited = usernow.user_id
        newlist.dateedited = datetime.date(datetime.now()) 
        newlist.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(newlist)
        DBS_JistLabour.flush()
        editpayment = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==newlist.id). \
                one()
        emp = int(newlist.id)
        editpayment.payment_number =emp
        #start of the labour data writing to dbase
        divall = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.active==True). \
                all()
        for div in divall:
            labtemp = DBS_JistLabour.query(JistLabourList). \
                    filter(JistLabourList.active==True). \
                    filter(JistLabourList.division==div.id). \
                    all()
            for lab in labtemp:
                #print lab.id, lab.emp_number
                #break
                #return
                labdata = JistLabourPaymentRunsData() 
                var_hours_normal = 0 
                var_hours_normal = 0 
                var_hours_over_time =  0
                var_hours_over_time = 0
                var_hours_sunday_time =  0
                var_hours_sunday_time = 0
                var_paye =  0
                var_paye = 0 
                var_staff_loans =  0
                var_staff_loans = 0 
                labdata.empl_id = lab.id
                labdata.div_id = div.id
                labdata.paylist_id = newlist.id
                labdata.rate_per_day = lab.rate_per_day
                labdata.rate_per_hour = float(lab.rate_per_day)/8
                var_rate_per_day = lab.rate_per_day 
                #HourRate = var_rate_per_day / 8
                NTRate = float(var_rate_per_day) / 8
                OTRate = NTRate * 1.5
                SunRate = NTRate * 2
                AmountNT = NTRate * float(var_hours_normal)
                AmountUIF = AmountNT * 0.01
                AmountOT = OTRate * float(var_hours_over_time)
                AmountSun = SunRate * float(var_hours_sunday_time)
                GrossTotal = AmountNT + AmountOT + AmountSun
                NettTotal = GrossTotal - float(var_paye) -float(AmountUIF) - float(var_staff_loans)
                #to get the totals
                labdata.hours_normal = var_hours_normal
                labdata.hours_over_time = var_hours_over_time
                labdata.hours_sunday_time = var_hours_sunday_time 
                labdata.amount_normal_time = AmountNT
                labdata.amount_over_time = AmountOT
                labdata.amount_sunday_time = AmountSun
                labdata.paye = var_paye 
                labdata.uif = AmountUIF 
                labdata.staff_loans = var_staff_loans 
                labdata.amount_gross_total = GrossTotal
                labdata.amount_net_total = NettTotal 
                labdata.useridnew = usernow.user_id
                labdata.useridedited = usernow.user_id
                labdata.dateedited = datetime.date(datetime.now()) 
                DBS_JistLabour.add(labdata)
                DBS_JistLabour.flush()
        runtotal = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==newlist.id). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        newlist.total_gross = runtotal

        redirect("/labourcont/showlabourpaymentruns")

    @expose('jistdocstore.templates.labour.showpaymentrunsdata')
    def showlabourpaymentdata(self,*arg,**named):
        tmpl_context.widget = labour_division_box 
        try:
            if not arg[1]:
                init_value = 1
            else:
                init_value = arg[1]
        except:
            init_value = 1
        labourdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==arg[0]). \
                filter(JistLabourPaymentRunsData.div_id==init_value). \
                order_by(asc(JistLabourPaymentRunsData.empl_id)). \
                all()
        emps = DBS_JistLabour.query(JistLabourList). \
                all()
        p1total = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==arg[0]). \
                filter(JistLabourPaymentRunsData.div_id==init_value). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        #print p1total
        paymentrun = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==arg[0]). \
                one()
        divisiondata = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==init_value). \
                one()
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        for m in emps:
            employees.append([m.id,m.last_name+' ' +m.first_name])
        #print p1
        #print employees[2]
        #for k in p1:
        #    print k.empl_id
        count = len(labourdata) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            labourdata, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print items
        return dict(page='Payments Labour Data',
                    wip = items,
                    thiscurrentPage=currentPage,
                    init_value = init_value,
                    employees = employees,
                    paymentrun = paymentrun,
                    divisiondata = divisiondata,
                    action = '/labourcont/getdivisionsdata/'+arg[0],
                    runid= arg[0],
                    totalexcl = p1total,
                    pageinfo = named,
                    pdfstring =  "export_labour_payment_data_pdf/"+arg[0]+"/"+str(divisiondata.id),
                    count=count)

    @expose()
    def saveeditlabourpaymentlist(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==arg[0]). \
                one()
        u.payment_date = kw['payment_date']
        u.start_date = kw['start_date']
        u.end_date = kw['end_date']
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        if type(kw['active'])==list:
            u.active = 1
        elif type(kw['active'])==unicode:
            u.active = 0
        else:
            pass
        flash("Payment successfully edited.")
        redirect("/labourcont/showlabourpaymentruns")

    @expose()
    def getdivisionsdata(self,*arg,**kw):
        if not kw['division_name']:
            point = 1
        else:
            point = kw['division_name']
        redirect('/labourcont/showlabourpaymentdata/'+arg[0]+'/'+point)

    @expose('jistdocstore.templates.labour.editlabourpaymentdata')
    def editlabourpaymentdata(self,*arg,**named):
        val = payment_data_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = payment_data_list_form 
        emps = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==arg[1]). \
                one()
        #p1total = DBS_JistLabour.query(JistLabourPaymentRunsData). \
        #        filter(JistLabourPaymentRunsData.empl_id==arg[0]). \
        #        value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        #for x in paymentruns:
        #    #print x.id, x.start_date
        #    #print type(x)
        labdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.id==arg[0]). \
                one()
        lablist = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==labdata.paylist_id). \
                one()
        divisiondata = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==emps.division). \
                one()

        return dict(page='Edit Payment Data Labour',
                   action='/labourcont/saveeditlabourpaymentdata/'+str(arg[0])+'/'+str(arg[2])+'/'+str(arg[3])+'/'+str(arg[4]),
                   userid = str(arg[0]),
                   employee = emps,
                   lablist = lablist,
                   labdata = labdata,
                   division = divisiondata,
                   value=val,
                   )

    @expose()
    def saveeditlabourpaymentdata(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        labdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.id==arg[0]). \
                one()
        #print arg[0]
        #return
        if kw['hours_normal']:
            var_hours_normal = kw['hours_normal']
        else:
            var_hours_normal = 0 
        if kw['hours_over_time']:
            var_hours_over_time = kw['hours_over_time']
        else:
            var_hours_over_time = 0
        if kw['hours_sunday_time']:
            var_hours_sunday_time = kw['hours_sunday_time']
        else:
            var_hours_sunday_time = 0
        if kw['paye']:
            var_paye = kw['paye']
        else:
            var_paye = 0 
        if kw['staff_loans']:
            var_staff_loans = kw['staff_loans']
        else:
            var_staff_loans = 0 
        var_rate_per_day = labdata.rate_per_day 
        #HourRate = var_rate_per_day / 8
        NTRate = float(var_rate_per_day) / 8
        OTRate = NTRate * 1.5
        SunRate = NTRate * 2
        AmountNT = NTRate * float(var_hours_normal)
        AmountUIF = AmountNT * 0.01
        AmountOT = OTRate * float(var_hours_over_time)
        AmountSun = SunRate * float(var_hours_sunday_time)
        GrossTotal = AmountNT + AmountOT + AmountSun
        NettTotal = GrossTotal - float(var_paye) -float(AmountUIF) - float(var_staff_loans)
        #to get the totals
        labdata.hours_normal = var_hours_normal
        labdata.hours_over_time = var_hours_over_time
        labdata.hours_sunday_time = var_hours_sunday_time 
        labdata.amount_normal_time = AmountNT
        labdata.amount_over_time = AmountOT
        labdata.amount_sunday_time = AmountSun
        labdata.paye = var_paye 
        labdata.uif = AmountUIF 
        labdata.staff_loans = var_staff_loans 
        labdata.amount_gross_total = GrossTotal
        labdata.amount_net_total = NettTotal 
        labdata.useridedited = usernow.user_id
        labdata.dateedited = datetime.date(datetime.now()) 

        runtotal = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==labdata.paylist_id). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        listrun = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==labdata.paylist_id). \
                one()
        if runtotal:
            listrun.total_gross = runtotal
        else:
            listrun.total_gross = 0 

        flash("Payment Data successfully edited.")
        redirect("/labourcont/showlabourpaymentdata/"+arg[1]+'/'+arg[2]+"?page="+arg[3])

    @expose('jistdocstore.templates.labour.showlabouronepaymentdata')
    def showlabouronepaymentdata(self,*arg,**named):
        try:
            if not arg[1]:
                init_value = 1
            else:
                init_value = arg[1]
        except:
            init_value = 1
        paymentruns = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                join(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.empl_id==arg[0]). \
                filter(JistLabourPaymentRunsList.active==True). \
                    order_by(desc(JistLabourPaymentRunsList.payment_date)). \
                all()
        labourdata = []
        for x in paymentruns:
            labdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                    filter(JistLabourPaymentRunsData.empl_id==arg[0]). \
                    filter(JistLabourPaymentRunsData.paylist_id==x.id). \
                    order_by(desc(JistLabourPaymentRunsData.id)). \
                    all()
            labourdata.append([labdata,x.id,x.payment_date,x.start_date,x.end_date])
        emps = DBS_JistLabour.query(JistLabourList). \
                all()
        p1total = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.empl_id==arg[0]). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        divisiondata = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==init_value). \
                one()
        thislabourer = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==arg[0]). \
                one()

        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        for m in emps:
            employees.append([m.id,m.last_name+' ' +m.first_name])
            #print m.id,m.last_name
        count = len(labourdata) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            labourdata, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print items
        return dict(page='Payment History Individual Person',
                    wip = items,
                    thiscurrentPage=currentPage,
                    init_value = init_value,
                    employees = employees,
                    thislabour = thislabourer, 
                    paymentrun = paymentruns,
                    divisiondata = divisiondata,
                    action = '/labourcont/getdivisionsdata/'+arg[0],
                    runid= arg[0],
                    totalexcl = p1total,
                    pageinfo = named,
                    count=count)

    @expose('jistdocstore.templates.labour.editlabourpaymentdata')
    def editlabouronepaymentdata(self,*arg,**named):
        val = payment_data_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = payment_data_list_form 
        emps = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==arg[1]). \
                one()
        #p1total = DBS_JistLabour.query(JistLabourPaymentRunsData). \
        #        filter(JistLabourPaymentRunsData.empl_id==arg[0]). \
        #        value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        #for x in paymentruns:
        #    #print x.id, x.start_date
        #    #print type(x)
        labdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.id==arg[0]). \
                one()
        lablist = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==labdata.paylist_id). \
                one()
        divisiondata = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==emps.division). \
                one()

        return dict(page='Edit Payment Data Labour',
                   action='/labourcont/saveeditlabouronepaymentdata/'+str(arg[0])+'/'+str(arg[1])+'/'+str(arg[2])+'/'+str(arg[3]),
                   userid = str(arg[0]),
                   employee = emps,
                   lablist = lablist,
                   labdata = labdata,
                   division = divisiondata,
                   value=val,
                   )

    @expose()
    def saveeditlabouronepaymentdata(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        labdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.id==arg[0]). \
                one()
        #print arg[0]
        #return
        if kw['hours_normal']:
            var_hours_normal = kw['hours_normal']
        else:
            var_hours_normal = 0 
        if kw['hours_over_time']:
            var_hours_over_time = kw['hours_over_time']
        else:
            var_hours_over_time = 0
        if kw['hours_sunday_time']:
            var_hours_sunday_time = kw['hours_sunday_time']
        else:
            var_hours_sunday_time = 0
        if kw['paye']:
            var_paye = kw['paye']
        else:
            var_paye = 0 
        if kw['staff_loans']:
            var_staff_loans = kw['staff_loans']
        else:
            var_staff_loans = 0 
        var_rate_per_day = labdata.rate_per_day 
        #HourRate = var_rate_per_day / 8
        NTRate = float(var_rate_per_day) / 8
        OTRate = NTRate * 1.5
        SunRate = NTRate * 2
        AmountNT = NTRate * float(var_hours_normal)
        AmountUIF = AmountNT * 0.01
        AmountOT = OTRate * float(var_hours_over_time)
        AmountSun = SunRate * float(var_hours_sunday_time)
        GrossTotal = AmountNT + AmountOT + AmountSun
        NettTotal = GrossTotal - float(var_paye) -float(AmountUIF) - float(var_staff_loans)
        #to get the totals
        labdata.hours_normal = var_hours_normal
        labdata.hours_over_time = var_hours_over_time
        labdata.hours_sunday_time = var_hours_sunday_time 
        labdata.amount_normal_time = AmountNT
        labdata.amount_over_time = AmountOT
        labdata.amount_sunday_time = AmountSun
        labdata.paye = var_paye 
        labdata.uif = AmountUIF 
        labdata.staff_loans = var_staff_loans 
        labdata.amount_gross_total = GrossTotal
        labdata.amount_net_total = NettTotal 
        labdata.useridedited = usernow.user_id
        labdata.dateedited = datetime.date(datetime.now()) 

        flash("Payment Data successfully edited.")
        redirect("/labourcont/showlabouronepaymentdata/"+arg[1]+"?page="+arg[3])

    @expose('jistdocstore.templates.labour.showdivsummariespaymentrun')
    def showdivsummariespaymentrun(self,*arg,**named):
        paymentruns = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==arg[0]). \
                one()
        divall = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.active==True). \
                all()
        divisionout = []
        for div in divall:
            divtotal = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                    filter(JistLabourPaymentRunsData.paylist_id==paymentruns.id). \
                    filter(JistLabourPaymentRunsData.div_id==div.id). \
                    value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
            divisionout.append({'name':div.division_name,'total':divtotal})
        alltotal = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==paymentruns.id). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        return dict(page='Payment Summary All Divisions',
                    paymentrun = paymentruns,
                    pdfstring = "export_labour_division_summaries_all_pdf/"+arg[0],
                    divisiondata = divisionout,
                    grosstotal = alltotal
                    )

    @expose()
    def export_labour_list_all_pdf(self):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        lblist = DBS_JistLabour.query(JistLabourList). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         })
        userdata.append([datetime.date(datetime.now()),
                        "Labour List All",
                        ""
                        ])
        headers =["ID","Empl. Number","Last Name","First Name","ID Number","Date Started","Rate Per Day"]
        headerwidths=[50,80,100,100,80,80,80]
        pdffile.CreatePDFLabourList(userdata,lablist,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_labour_list_active_pdf(self):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.active==True). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         })
        userdata.append([datetime.date(datetime.now()),
                        "Labour List Active",
                        ""
                        ])
        headers =["ID","Empl. Number","Last Name","First Name","ID Number","Date Started","Rate Per Day"]
        headerwidths=[50,80,100,100,80,80,80]
        pdffile.CreatePDFLabourList(userdata,lablist,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_labour_payment_runs_pdf(self):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        lblist = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.active==True). \
                order_by(desc(JistLabourPaymentRunsList.id)). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({
                         'payment_date':k.payment_date,
                         'start_date':k.start_date,
                         'end_date':k.end_date,
                         'total_gross':k.total_gross,
                         })
        userdata.append([datetime.date(datetime.now()),
                        "Payment Run List",
                        ""
                        ])
        headers =["Payment Date","Start Date","End Date","Total Gross"]
        headerwidths=[100,100,100,100]
        pdffile.CreatePDFPaymentList(userdata,lablist,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_labour_division_summaries_all_pdf(self,paymentrun_id):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        paymentruns = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==paymentrun_id). \
                one()
        divall = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.active==True). \
                all()
        divisionout = []
        for div in divall:
            divtotal = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                    filter(JistLabourPaymentRunsData.paylist_id==paymentruns.id). \
                    filter(JistLabourPaymentRunsData.div_id==div.id). \
                    value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
            if not div.division_leader:
                usernow = User.by_user_id(1)
            else:
                usernow = User.by_user_id(div.division_leader)

            divisionout.append({'name':div.division_name,
                                'division_leader':usernow.user_name,
                                'total':divtotal})
        alltotal = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==paymentruns.id). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        userdata.append([datetime.date(datetime.now()),
                        "Payment Summary All Labour Divisions",
                        alltotal,
                        paymentruns.payment_date,
                        paymentruns.start_date,
                        paymentruns.end_date,
                        ])
        #for k in divisionout:
        #    print k
        headers =["Division Name","Division Leader","Total"]
        headerwidths=[200,200,100]
        pdffile.CreatePDFDivisionSummariesAll(userdata,divisionout,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_labour_payment_data_pdf(self,*arg):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        labourdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==arg[0]). \
                filter(JistLabourPaymentRunsData.div_id==arg[1]). \
                order_by(asc(JistLabourPaymentRunsData.empl_id)). \
                all()
        emps = DBS_JistLabour.query(JistLabourList). \
                all()
        p1total = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==arg[0]). \
                filter(JistLabourPaymentRunsData.div_id==arg[1]). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        #print p1total
        paymentrun = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                filter(JistLabourPaymentRunsList.id==arg[0]). \
                one()
        divisiondata = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==arg[1]). \
                one()
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        for m in emps:
            employees.append([m.id,m.last_name+' ' +m.first_name])
        lablist = []
        for k in labourdata:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({
                          'employee':employees[k.empl_id-1][1],
                          'rate_per_day':k.rate_per_day,
                          'hours_normal':k.hours_normal,
                          'amount_normal_time':k.amount_normal_time,
                          'hours_over_time':k.hours_over_time,
                          'amount_over_time':k.amount_over_time,
                          'hours_sunday_time':k.hours_sunday_time,
                          'amount_sunday_time':k.amount_sunday_time,
                          'amount_gross_total':k.amount_gross_total,
                          'uif':k.uif,
                          'paye':k.paye,
                          'staff_loans':k.staff_loans,
                          'amount_net_total':k.amount_net_total,

                         })
        userdata.append([datetime.date(datetime.now()),
                        "Payment Run Records",
                        divisiondata.division_name,
                        paymentrun.id,
                        paymentrun.start_date,
                        paymentrun.end_date,
                        paymentrun.payment_date,
                        totalexcl,
                        ""
                        ])
        headers =["Employee","Rate","NT",
                "Rand NT","OT","Rand OT","Sun T",
                "Rand ST","Gross","UIF",
                "Paye","Loans","Nett"]
        headerwidths=[150,50,50,
                      50,50,50,50,
                      50,50,50,
                      50,50,50
                    ]
        pdffile.CreatePDFLabourPaymentData(userdata,lablist,headers,headerwidths)
        #for m in lablist:
        #    print m
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def savelabourpic(self,user_id,*arg,**kw):
        del kw['sprox_id']
        #for k, w in enumerate(kw):
        #    print k, w, kw[w]
        #print user_id
        #print "User id was printed"
        #username = request.identity['repoze.who.userid']
        #usernow = User.by_user_name(username)
        filename = kw['filename']
        #Check File Size
        #uploadsize = os.path.getsize(filename.value)
        uploadsize = len(filename.value)
        ##print "Upload Size = %s"%(uploadsize/1024)
        if uploadsize == 0 or uploadsize/1024 > 1024*5:
            flash(_('File to big or nothing loaded. Max Size 5MB...'), 'warning')
            redirect("/secc/uploadpic/"+user_id)
        pic_path = os.path.join(labour_picdir, "lab_" + str(user_id)+'.png')
        f = file(pic_path, "w")
        f.write(kw['filename'].value)
        f.close()
        self.getthumbnail(pic_path,pic_path)
        #edituser = DBS_ContractData.query(User). \
        #        filter(User.user_id==kw['user_id']). \
        #        one()
        #for k, w in enumerate(kw):
        #    print k, w, kw[w]
        #<img src="/images/labourpics/labour_%s.png"
            #align="center"/>
        #</td>
        redirect("/secc/showusers")

    def getthumbnail(self, inpath, outpath):
        retcode = subprocess.call(['convert',inpath,'-resize','50!x50!',outpath])


    ########################################################################
    ###############Subcons##################################################
    ########################################################################
        
    @expose('jistdocstore.templates.labour.showsubcondivisionsall')
    def showsubcondivisionsall(self,**named):
        tmpl_context.widget = spx_divisions_subcon_list
        value = subcon_divisions_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='All Subcon Divisions',
                    wip = items,
                    thiscurrentPage=currentPage,
                    selfname = 'showsubcondivisionsall',
                    count=count)

    @expose('jistdocstore.templates.labour.divisionnew')
    def division_subcon_new(self,**named):
        tmpl_context.form = add_new_subcon_division_form
        return dict(page='New Subcontractor Division Form',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    action='/labourcont/savenewsubcondivision')

    @expose()
    def savenewsubcondivision(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = JistSubconDivisions()
        u.division_name = kw['division_name']
        u.division_leader = kw['division_leader']
        u.active = True
        u.useridnew = usernow.user_id
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        u.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(u)
        DBS_JistLabour.flush()
        emp = "SUBDIV"+str(int(u.id)+999)
        editdiv = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==u.id). \
                one()
        editdiv.division_code =emp
        redirect("/labourcont/showsubcondivisionsall")

    @expose('jistdocstore.templates.labour.editsubcondivisions')
    def editsubcondivisions(self,*arg,**named):
        val = subcon_division_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = subcon_division_list_form 
        return dict(page='Edit Subcon Divisions',
                   action='/labourcont/saveeditsubcondivisions/'+str(arg[0]),
                   userid = str(arg[0]),
                   value=val
                   )

    @expose()
    def saveeditsubcondivisions(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        div = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==arg[0]). \
                one()
        #for k, w in enumerate(kw):
        #    print k, w, kw[w]
        #return
        div.division_name = kw['division_name']
        div.division_leader = kw['division_leader']
        div.useridnew = usernow.user_id
        div.useridedited = usernow.user_id
        div.dateedited = datetime.date(datetime.now()) 
        div.dateadded = datetime.date(datetime.now()) 
        if type(kw['active'])==list:
            div.active = 1
        elif type(kw['active'])==unicode:
            div.active = 0
        else:
            pass
        flash("Division successfully edited.")
        redirect("/labourcont/showsubcondivisionsall")

    @expose('jistdocstore.templates.labour.showsubconall')
    def showsubconall(self,**named):
        tmpl_context.widget = spx_active_subcon_list
        value = subcon_filler.get_value(values={},offset=0,order_by='id',desc=True)
        #for v in value:
        #    print v
        currentPage = ''
        count = 1
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View All Subcon',
                    wip = items,
                    thiscurrentPage=currentPage,
                    selfname = 'showsubconall',
                    pdfstring = "export_subcon_list_all_pdf",
                    count=count)

    @expose('jistdocstore.templates.labour.showactivesubconall')
    def showactivesubconall(self,**named):
        tmpl_context.widget = spx_active_subcon_list
        value = subcon_active_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View All Active Subcon',
                    wip = items,
                    thiscurrentPage=currentPage,
                    pageinfo = named,
                    selfname = 'showactivesubconall',
                    pdfstring = "/export_subcon_list_active_pdf",
                    count=count)

    @expose('jistdocstore.templates.labour.editsubcon')
    def editsubcon(self,*arg,**named):
        val = subcon_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = subcon_list_form 
        return dict(page='Edit Subcon',
                   action='/labourcont/saveeditsubcon/'+str(arg[0]),
                   userid = str(arg[0]),
                   value=val
                   )

    @expose()
    #@validate(edit_supplier_form,edit_supplier)
    def saveeditsubcon(self,*arg,**kw):
        #print arg
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        editsubcon = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==arg[0]). \
                one()
        #for k, w in enumerate(kw):
        #    print k, w, kw[w]
        editsubcon.trading_name = kw['trading_name']
        editsubcon.vat_number = kw['vat_number']
        editsubcon.last_name = kw['last_name']
        editsubcon.first_name = kw['first_name']
        editsubcon.id_number = kw['id_number']
        editsubcon.date_started = kw['date_started']
        editsubcon.rate_per_day = kw['rate_per_day']
        editsubcon.division = kw['division']
        editsubcon.bank = kw['bank']
        editsubcon.bank_code = kw['branch_code']
        editsubcon.account_number = kw['account_number']
        editsubcon.address1 = kw['address1']
        editsubcon.address2 = kw['address2']
        editsubcon.tel_number_home = kw['tel_number_home']
        editsubcon.next_of_kin_name = kw['next_of_kin_name']
        editsubcon.next_of_kin_tel = kw['next_of_kin_tel']
        editsubcon.useridedited = usernow.user_id
        editsubcon.dateedited = datetime.date(datetime.now()) 
        if type(kw['active'])==list:
            editsubcon.active = 1
        elif type(kw['active'])==unicode:
            editsubcon.active = 0
        else:
            pass
        flash("Subcon successfully edited.")
        redirect("/labourcont/showsubconall")

    @expose('jistdocstore.templates.labour.subconnew')
    def subcon_new(self,**named):
        tmpl_context.form = add_new_subcon_form
        return dict(page='New Subcon Form',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    selfname = 'subcon_new',
                    action='/labourcont/savenewsubcon')

    @expose()
    #@validate(add_new_user,user_new)
    def savenewsubcon(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = JistSubconList()
        u.trading_name = kw['trading_name']
        u.vat_number = kw['vat_number']
        u.last_name = kw['last_name']
        u.first_name = kw['first_name']
        u.id_number = kw['id_number']
        u.date_started = kw['date_started']
        u.rate_per_day = kw['rate_per_day']
        u.division = kw['division']
        u.bank = kw['bank']
        u.bank_code = kw['branch_code']
        u.account_number = kw['account_number']
        u.address1 = kw['address1']
        u.address2 = kw['address2']
        u.tel_number_home = kw['tel_number_home']
        u.next_of_kin_name = kw['next_of_kin_name']
        u.next_of_kin_tel = kw['next_of_kin_tel']
        u.active = True
        u.useridnew = usernow.user_id
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        u.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(u)
        DBS_JistLabour.flush()
        redirect("/labourcont/showactivesubconall")

    @expose('jistdocstore.templates.labour.showsubconpaymentruns')
    def showsubconpaymentruns(self,**named):
        tmpl_context.widget = spx_payment_runs_subcon_list
        value = subconpayment_runs_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='View Subcon Payment Runs',
                    wip = items,
                    thiscurrentPage=currentPage,
                    pdfstring = "/export_subcon_payment_runs_pdf",
                    count=count)

    @expose('jistdocstore.templates.labour.paymentrunsubconnew')
    def paymentrunsubcon_new(self,**named):
        tmpl_context.form = subconadd_new_payment_run_form
        return dict(page='New Payment Run Subcon',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    action='/labourcont/savenewsubconpayment')

    @expose()
    def savenewsubconpayment(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newlist = JistSubconPaymentRunsList()
        newlist.payment_date = kw['payment_date']
        newlist.start_date = kw['start_date']
        newlist.end_date = kw['end_date']
        newlist.active = 1 
        newlist.useridnew = usernow.user_id
        newlist.useridedited = usernow.user_id
        newlist.dateedited = datetime.date(datetime.now()) 
        newlist.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(newlist)
        DBS_JistLabour.flush()
        editpayment = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==newlist.id). \
                one()
        emp = int(newlist.id)
        editpayment.payment_number =emp
        #start of the subcon data writing to dbase
        divall = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.active==True). \
                all()
        for div in divall:
            labtemp = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.active==True). \
                    filter(JistSubconList.division==div.id). \
                    all()
            for lab in labtemp:
                #print lab.id, lab.emp_number
                #break
                #return
                labdata = JistSubconPaymentRunsData() 
                var_qty = 0 
                var_price = 0 
                var_total =  0
                labdata.paylist_id = newlist.id 
                labdata.sub_id = lab.id 
                labdata.div_id = div.id 
                labdata.jcno = 1000 
                labdata.items = "Item 1" 
                labdata.description = "Description" 
                labdata.unit = "Each" 
                labdata.qty = var_qty 
                labdata.price = var_price 
                labdata.total_excl = var_total 
                labdata.useridnew = usernow.user_id
                labdata.useridedited = usernow.user_id
                labdata.dateedited = datetime.date(datetime.now()) 
                DBS_JistLabour.add(labdata)
                DBS_JistLabour.flush()
        runtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==newlist.id). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        newlist.total_gross = runtotal

        redirect("/labourcont/showsubconpaymentruns")


    @expose('jistdocstore.templates.labour.editsubconpaymentrun')
    def editsubconpaymentrun(self,*arg,**named):
        val = subconpayment_run_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = subconpayment_run_list_form 
        return dict(page='Edit Payment Run Subcon',
                   action='/labourcont/saveeditsubconpaymentlist/'+str(arg[0]),
                   userid = str(arg[0]),
                   value=val
                   )


    @expose('jistdocstore.templates.labour.subconpaymentdatanew')
    def subconpaymentdata_new(self,*arg,**named):
        #arg[0] = paymentrun.id
        #arg[1] = subid
        #arg[2] = division.id
        #arg[3] = currentpage 
        #href="/labourcont/subconpaymentdata_new/${paymentrun.payment_number}/${employee.id}/${division.id}/${thiscurrentPage.page}">
        tmpl_context.form = add_new_subcon_payment_data_form
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==arg[1]). \
                one()
        paymentrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==arg[0]). \
                one()
        divisiondata = division = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()
        return dict(page='New Subcon Claim',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named,
                    employee = emps,
                    division = divisiondata,
                    paymentrun = paymentrun,
                    selfname = 'subconpaymentdata_new',
                    action='/labourcont/savenewsubconpaymentdata/'+arg[0]+'/'+arg[1]+'/'+arg[2]+'/'+arg[3])

    @expose()
    def savenewsubconpaymentdata(self,*arg,**kw):
        del kw['sprox_id']
        #arg[0] = paymentrun.id
        #arg[1] = subid
        #arg[2] = division.id
        #arg[3] = currentpage 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        labdata = JistSubconPaymentRunsData() 
        if kw['qty']:
            var_qty = kw['qty'] 
        else:
            var_qty = 0
        if kw['price']:
            var_price = kw['price'] 
        else:
            var_price = 0 
        var_total =  0
        labdata.paylist_id = arg[0] 
        labdata.sub_id = arg[1] 
        labdata.div_id = arg[2] 
        labdata.jcno = kw['jcno'] 
        labdata.item = kw['item'] 
        labdata.description = kw['description'] 
        labdata.unit = kw['unit'] 
        labdata.qty = var_qty 
        labdata.price = var_price 
        var_total = float(var_qty)* float(var_price)
        labdata.total_excl = var_total 
        labdata.useridnew = usernow.user_id
        labdata.useridedited = usernow.user_id
        labdata.dateedited = datetime.date(datetime.now()) 
        labdata.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(labdata)
        DBS_JistLabour.flush()
        runtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==labdata.paylist_id). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        listrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==labdata.paylist_id). \
                one()
        if runtotal:
            listrun.total_gross = runtotal
        else:
            listrun.total_gross = 0 

        #href="/labourcont/subconpaymentdata_new/${paymentrun.payment_number}/${employee.id}/${division.id}/${thiscurrentPage.page}">
        redirect("/labourcont/showsubconpaymentdata/"+arg[0]+"/"+arg[1]+"/"+arg[3])

    @expose('jistdocstore.templates.labour.showsubconpaymentrunsdata')
    def showsubconpaymentdata(self,*arg,**named):
        tmpl_context.widget = subcon_list_box 
        #tmpl_context.widget = subcon_division_box 
        try:
            if not arg[1]:
                init_value = 1
            else:
                init_value = arg[1]
        except:
            init_value = 1
        #for k in arg:
        #    print k
        #return
        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==arg[0]). \
                filter(JistSubconPaymentRunsData.sub_id==init_value). \
                order_by(asc(JistSubconPaymentRunsData.sub_id)). \
                all()
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==init_value). \
                one()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==arg[0]). \
                filter(JistSubconPaymentRunsData.sub_id==init_value). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        paymentrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==arg[0]). \
                one()
        division = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()
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
        #print items
        return dict(page='Payment Run Data Per Subcontractor',
                    wip = items,
                    thiscurrentPage=currentPage,
                    init_value = init_value,
                    employee = emps,
                    paymentrun = paymentrun,
                    division = division,
                    action = '/labourcont/getsubtradingasdata/'+arg[0],
                    runid= arg[0],
                    totalexcl = p1total,
                    selfname = "showsubconpaymentdata",
                    pageinfo = named,
                    pdfstring = "/export_subcon_payment_data_pdf/"+arg[0]+"/"+str(init_value),
                    count=count)

    @expose()
    def getsubtradingasdata(self,*arg,**kw):
        if not kw['trading_name']:
            point = 1
        else:
            point = kw['trading_name']
        redirect('/labourcont/showsubconpaymentdata/'+arg[0]+'/'+point)

    @expose()
    def saveeditsubconpaymentlist(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==arg[0]). \
                one()
        u.payment_date = kw['payment_date']
        u.start_date = kw['start_date']
        u.end_date = kw['end_date']
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        if type(kw['active'])==list:
            u.active = 1
        elif type(kw['active'])==unicode:
            u.active = 0
        else:
            pass
        flash("Payment successfully edited.")
        redirect("/labourcont/showsubconpaymentruns")

    @expose()
    def getsubdata(self,*arg,**kw):
        if not kw['division_name']:
            point = 1
        else:
            point = kw['division_name']
        redirect('/labourcont/showsubconpaymentdata/'+arg[0]+'/'+point)

    @expose('jistdocstore.templates.labour.editsubconpaymentdata')
    def editsubconpaymentdata(self,*arg,**named):
        #arg[0] = paylist_id or paymentrun.id
        #arg[1] = subid 
        #arg[2] = payment_number 
        #arg[3] = division.id 
        #arg[4] = currentpage 
        val = subconpayment_data_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = subconpayment_data_list_form 
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==arg[1]). \
                one()
        labdata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.id==arg[0]). \
                one()
        lablist = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==labdata.paylist_id). \
                one()
        divisiondata = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()
        paymentrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==labdata.paylist_id). \
                one()

        return dict(page='Edit Payment Data Subcon',
                   action='/labourcont/saveeditsubconpaymentdata/'+str(arg[0])+'/'+str(arg[1])+'/'+str(arg[2])+'/'+str(arg[3])+'/'+str(arg[4]),
                   userid = str(arg[0]),
                   employee = emps,
                   lablist = lablist,
                   labdata = labdata,
                   division = divisiondata,
                   paymentrun = paymentrun,
                   value=val,
                   )

    @expose()
    def saveeditsubconpaymentdata(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        labdata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.id==arg[0]). \
                one()
        #for k,w in kw.iteritems():
        #    print k,w
        #return
        if kw['qty']:
            var_qty = kw['qty'] 
        else:
            var_qty = 0
        if kw['price']:
            var_price = kw['price'] 
        else:
            var_price = 0 
        var_total =  0
        labdata.jcno = kw['jcno'] 
        labdata.item = kw['item'] 
        labdata.description = kw['description'] 
        labdata.unit = kw['unit'] 
        labdata.qty = var_qty 
        labdata.price = var_price 
        var_total = float(var_qty)* float(var_price)
        labdata.total_excl = var_total 
        labdata.useridnew = usernow.user_id
        labdata.useridedited = usernow.user_id
        labdata.dateedited = datetime.date(datetime.now()) 
        DBS_JistLabour.add(labdata)
        DBS_JistLabour.flush()

        #runtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
        #    filter(JistSubconPaymentRunsData.paylist_id==labdata.paylist_id). \
        #    value(func.sum(JistSubconPaymentRunsData.total_excl))
        #newlist.total_gross = runtotal

        labdata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
            filter(JistSubconPaymentRunsData.id==arg[0]). \
            one()
        labdata.useridedited = usernow.user_id
        labdata.dateedited = datetime.date(datetime.now()) 

        runtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==labdata.paylist_id). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        listrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==labdata.paylist_id). \
                one()
        if runtotal:
            listrun.total_gross = runtotal
        else:
            listrun.total_gross = 0 
        #arg[0] = paymentdata_id
        #arg[1] = subid 
        #arg[2] = payment_number 
        #arg[3] = division.id 
        #arg[4] = currentpage 
        flash("Payment Data successfully edited.")
        redirect("/labourcont/showsubconpaymentdata/"+arg[2]+'/'+arg[1]+"?page="+arg[3])

    @expose('jistdocstore.templates.labour.showsubcononepaymentdata')
    def showsubcononepaymentdata(self,*arg,**named):
        try:
            if not arg[1]:
                init_value = 1
            else:
                init_value = arg[1]
        except:
            init_value = 1
        paymentruns = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                join(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.id==arg[0]). \
                filter(JistSubconPaymentRunsList.active==True). \
                    order_by(desc(JistSubconPaymentRunsList.payment_date)). \
                all()
        subcondata = []
        for x in paymentruns:
            labdata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                    filter(JistSubconPaymentRunsData.id==arg[0]). \
                    filter(JistSubconPaymentRunsData.paylist_id==x.id). \
                    order_by(desc(JistSubconPaymentRunsData.id)). \
                    all()
            subcondata.append([labdata,x.id,x.payment_date,x.start_date,x.end_date])
        emps = DBS_JistLabour.query(JistSubconList). \
                all()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.id==arg[0]). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        divisiondata = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==init_value). \
                one()
        thissubconer = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==arg[0]). \
                one()

        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        for m in emps:
            employees.append([m.id,m.last_name+' ' +m.first_name])
            #print m.id,m.last_name
        count = len(subcondata) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            subcondata, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print items
        return dict(page='Payment History Individual Subcon',
                    wip = items,
                    thiscurrentPage=currentPage,
                    init_value = init_value,
                    employees = employees,
                    thissubcon = thissubconer, 
                    paymentrun = paymentruns,
                    divisiondata = divisiondata,
                    action = '/labourcont/getsubdata/'+arg[0],
                    runid= arg[0],
                    totalexcl = p1total,
                    pageinfo = named,
                    count=count)

    @expose('jistdocstore.templates.labour.editsubcononepaymentdata')
    def editsubcononepaymentdata(self,*arg,**named):
        val = subconpayment_data_list_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = subconpayment_data_list_form 
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==arg[1]). \
                one()
        labdata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.id==arg[0]). \
                one()
        lablist = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==labdata.paylist_id). \
                one()
        divisiondata = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()

        return dict(page='Edit Payment Data Subcon',
                   action='/labourcont/saveeditsubcononepaymentdata/'+str(arg[0])+'/'+str(arg[1])+'/'+str(arg[2])+'/'+str(arg[3]),
                   userid = str(arg[0]),
                   employee = emps,
                   lablist = lablist,
                   labdata = labdata,
                   division = divisiondata,
                   value=val,
                   )

    @expose()
    def saveeditsubcononepaymentdata(self,*arg,**kw):
        del kw['sprox_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #print arg[0]
        #return
        if kw['hours_normal']:
            var_hours_normal = kw['hours_normal']
        else:
            var_hours_normal = 0 
        if kw['hours_over_time']:
            var_hours_over_time = kw['hours_over_time']
        else:
            var_hours_over_time = 0
        if kw['hours_sunday_time']:
            var_hours_sunday_time = kw['hours_sunday_time']
        else:
            var_hours_sunday_time = 0
        if kw['paye']:
            var_paye = kw['paye']
        else:
            var_paye = 0 
        if kw['staff_loans']:
            var_staff_loans = kw['staff_loans']
        else:
            var_staff_loans = 0 
        var_rate_per_day = labdata.rate_per_day 
        #HourRate = var_rate_per_day / 8
        NTRate = float(var_rate_per_day) / 8
        OTRate = NTRate * 1.5
        SunRate = NTRate * 2
        AmountNT = NTRate * float(var_hours_normal)
        AmountUIF = AmountNT * 0.01
        AmountOT = OTRate * float(var_hours_over_time)
        AmountSun = SunRate * float(var_hours_sunday_time)
        GrossTotal = AmountNT + AmountOT + AmountSun
        NettTotal = GrossTotal - float(var_paye) -float(AmountUIF) - float(var_staff_loans)
        #to get the totals
        labdata.hours_normal = var_hours_normal
        labdata.hours_over_time = var_hours_over_time
        labdata.hours_sunday_time = var_hours_sunday_time 
        labdata.amount_normal_time = AmountNT
        labdata.amount_over_time = AmountOT
        labdata.amount_sunday_time = AmountSun
        labdata.paye = var_paye 
        labdata.uif = AmountUIF 
        labdata.staff_loans = var_staff_loans 
        labdata.amount_gross_total = GrossTotal
        labdata.amount_net_total = NettTotal 
        labdata.useridedited = usernow.user_id
        labdata.dateedited = datetime.date(datetime.now()) 

        flash("Payment Data successfully edited.")
        redirect("/labourcont/showsubcononepaymentdata/"+arg[1]+"?page="+arg[3])

    @expose('jistdocstore.templates.labour.showdivsubconsummariespaymentrun')
    def showdivsubconsummariespaymentrun(self,*arg,**named):
        paymentruns = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==arg[0]). \
                one()
        divall = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.active==True). \
                all()
        divisionout = []
        for div in divall:
            divtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                    filter(JistSubconPaymentRunsData.paylist_id==paymentruns.id). \
                    filter(JistSubconPaymentRunsData.div_id==div.id). \
                    value(func.sum(JistSubconPaymentRunsData.amount_gross_total))
            divisionout.append({'name':div.division_name,'total':divtotal})
        alltotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==paymentruns.id). \
                value(func.sum(JistSubconPaymentRunsData.amount_gross_total))
        return dict(page='Payment Summary All Divisions',
                    paymentrun = paymentruns,
                    pdfstring = "export_subcon_division_summaries_all_pdf/"+arg[0],
                    divisiondata = divisionout,
                    grosstotal = alltotal
                    )

    @expose('jistdocstore.templates.labour.showsubcononejcnosummary')
    def showsubcononejcnosummary(self,*arg,**named):
        tmpl_context.widget = subcon_jcno_list_box 
        try:
            if not arg[0]:
                sub_id = 1
            else:
                sub_id = arg[0] 

            if not arg[1]:
                jcno = 500 
            else:
                jcno = arg[1] 
        except:
            sub_id = 1
            jcno = 500 
        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                join(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.active==True). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                filter(JistSubconPaymentRunsData.sub_id==sub_id). \
                order_by(asc(JistSubconPaymentRunsData.sub_id)). \
                all()
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==sub_id). \
                one()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                filter(JistSubconPaymentRunsData.sub_id==sub_id). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        paymentrun = []
        for k in subcondata:
            payrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                    filter(JistSubconPaymentRunsList.id==k.paylist_id). \
                    one()
            paymentrun.append({'pay_date':payrun.payment_date,
                               'payment_number':payrun.id,
                               'subcon':emps.trading_name
                               })

        division = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        #for m in emps:
        #employees.append([emps.id,emps.last_name+' ' +emps.first_name])
        #print p1
        #print employees[2]
        #for k in p1:
        #    print k.empl_id
        count = len(subcondata) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            subcondata, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print items
        return dict(page='Single Subcon Contract Payments',
                    wip = items,
                    thiscurrentPage=currentPage,
                    employee = emps,
                    paymentrun = paymentrun,
                    init_value = sub_id,
                    selfname = 'showsubcononejcnosummary',
                    division = division,
                    action = '/labourcont/getsubjcnodata/',
                    runid= sub_id,
                    totalexcl = p1total,
                    jcno = jcno,
                    #pageinfo = named,
                    pdfstring ="export_subcon_jcno_summary_pdf/"+sub_id+"/"+jcno,
                    #count=count
                    )

    @expose('jistdocstore.templates.labour.showsubcondivsummariespaymentrun')
    def showsubsummariespaymentrun(self,*arg,**named):
        paymentruns = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==arg[0]). \
                one()
        suball = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()
        subout = []
        for sub in suball:
            subtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                    filter(JistSubconPaymentRunsData.paylist_id==paymentruns.id). \
                    filter(JistSubconPaymentRunsData.sub_id==sub.id). \
                    value(func.sum(JistSubconPaymentRunsData.total_excl))
            subout.append({'name':sub.trading_name,'total':subtotal})
        alltotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==paymentruns.id). \
                    value(func.sum(JistSubconPaymentRunsData.total_excl))
        return dict(page='Payment Run All Subcontractors ',
                    paymentrun = paymentruns,
                    pdfstring = "export_subcon_payment_summaries_all_pdf/"+arg[0],
                    divisiondata = subout,
                    grosstotal = alltotal
                    )

    @expose()
    def getsubjcnodata(self,*arg,**kw):
        if not kw['jcno']:
            jcno = 1 
        else:
            jcno = kw['jcno']
        if not kw['sub_id']:
            subid = 1 
        else:
            subid = kw['sub_id']
        redirect('/labourcont/showsubcononejcnosummary/'+subid+'/'+jcno)

    @expose('jistdocstore.templates.labour.showsubconalljcnosummary')
    def showsubconalljcnosummary(self,*arg,**named):
        tmpl_context.widget = jcno_list_box 
        try:
            if not arg[0]:
                jcno = 500 
            else:
                jcno = arg[0] 
        except:
            jcno = 500 
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
        return dict(page='All Subcontractors Contract Payments',
                    wip = items,
                    thiscurrentPage=currentPage,
                    employee = emps,
                    paymentrun = paymentrun,
                    init_value = 1,
                    selfname = 'showsubconalljcnosummary',
                    #division = division,
                    action = '/labourcont/getjcnodata/',
                    runid= 1,
                    totalexcl = p1total,
                    jcno = jcno,
                    #pageinfo = named,
                    pdfstring ="export_subcon_jcnoall_summary_pdf/"+jcno,
                    #count=count
                    )

    @expose()
    def getjcnodata(self,*arg,**kw):
        if not kw['jcno']:
            jcno = 500 
        else:
            jcno = kw['jcno']
        redirect('/labourcont/showsubconalljcnosummary/'+jcno)

    @expose()
    def export_subcon_list_active_pdf(self):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        lblist = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'trading_name':k.trading_name,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'vat_number':k.vat_number,
                         })
        userdata.append([datetime.date(datetime.now()),
                        "Subcon List Active",
                        ""
                        ])
        headers =["ID","Trading Name","Last Name","First Name",
                    "ID Number","Date Started","Vat Number"]
        headerwidths=[50,180,100,100,80,80,100]
        pdffile.CreatePDFSubconList(userdata,lablist,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_subcon_payment_runs_pdf(self):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        lblist = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.active==True). \
                order_by(desc(JistSubconPaymentRunsList.id)). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({
                         'payment_date':k.payment_date,
                         'start_date':k.start_date,
                         'end_date':k.end_date,
                         'total_gross':k.total_gross,
                         })
        userdata.append([datetime.date(datetime.now()),
                        "Payment Run List",
                        ""
                        ])
        headers =["Payment Date","Start Date","End Date","Total Gross"]
        headerwidths=[100,100,100,100]
        pdffile.CreatePDFPaymentList(userdata,lablist,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_subcon_payment_data_pdf(self,*arg):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        init_value = arg[1]
        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==arg[0]). \
                filter(JistSubconPaymentRunsData.sub_id==init_value). \
                order_by(asc(JistSubconPaymentRunsData.sub_id)). \
                all()
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==init_value). \
                one()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==arg[0]). \
                filter(JistSubconPaymentRunsData.sub_id==init_value). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        paymentrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==arg[0]). \
                one()
        division = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        lablist = []
        for k in subcondata:
            lablist.append({
                          'trading_name':emps.trading_name,
                          'jcno':k.jcno,
                          'item':k.item,
                          'description':k.description,
                          'unit':k.unit,
                          'qty':k.qty,
                          'price':k.price,
                          'total':k.total_excl,

                         })
        userdata.append([datetime.date(datetime.now()),
                        "Subcon Payment Run Records",
                        emps.trading_name,
                        paymentrun.id,
                        paymentrun.start_date,
                        paymentrun.end_date,
                        paymentrun.payment_date,
                        totalexcl,
                        ""
                        ])
        headers =["Trading Name","JCNo","Item",
                "Description","Unit","Qty","Price",
                "Total",]
        headerwidths=[150,50,50,
                     150,50,50,50,
                      80,
                      ]
        pdffile.CreatePDFSubconPaymentData(userdata,lablist,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_subcon_jcno_summary_pdf(self,sub_id,jcno):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                join(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.active==True). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                filter(JistSubconPaymentRunsData.sub_id==sub_id). \
                order_by(asc(JistSubconPaymentRunsData.sub_id)). \
                all()
        emps = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.id==sub_id). \
                one()
        p1total = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                filter(JistSubconPaymentRunsData.sub_id==sub_id). \
                value(func.sum(JistSubconPaymentRunsData.total_excl))
        #print p1total
        paymentrun = []
        for k in subcondata:
            payrun = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                    filter(JistSubconPaymentRunsList.id==k.paylist_id). \
                    one()
            paymentrun.append({
                          'pay_run':str(payrun.id),
                          'pay_date':payrun.payment_date,
                          'trading_name':emps.trading_name,
                          'jcno':k.jcno,
                          'item':k.item,
                          'description':k.description,
                          'unit':k.unit,
                          'qty':k.qty,
                          'price':k.price,
                          'total':k.total_excl,
                               })
        division = DBS_JistLabour.query(JistSubconDivisions). \
                filter(JistSubconDivisions.id==emps.division). \
                one()
        contract = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.jno==jcno). \
                one()
        contractname = str(contract.jno) + '- ' + contract.site+ '- ' + contract.description

        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')
        userdata.append([datetime.date(datetime.now()),
                        "Subcon vs Contract Payment Records",
                        emps.trading_name,
                        contractname,
                        "Any",
                        "Any",
                        "Any",
                        totalexcl,
                        "",
                        ])
        headers =["Pay Run","Pay Date","Trading Name","JCNo","Item",
                "Description","Unit","Qty","Price",
                "Total",]
        headerwidths=[50,80,150,50,50,
                     150,50,50,50,
                      80,
                      ]
        pdffile.CreatePDFSubconJCNoOnePaymentData(userdata,paymentrun,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_subcon_jcnoall_summary_pdf(self,jcno):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        subcondata = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                join(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsData.jcno==jcno). \
                filter(JistSubconPaymentRunsList.active==True). \
                order_by(asc(JistSubconPaymentRunsData.paylist_id)). \
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
            emps = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.id==k.sub_id). \
                    one()
            paymentrun.append({
                          'pay_run':str(payrun.id),
                          'pay_date':payrun.payment_date,
                          'trading_name':emps.trading_name,
                          'jcno':k.jcno,
                          'item':k.item,
                          'description':k.description,
                          'unit':k.unit,
                          'qty':k.qty,
                          'price':k.price,
                          'total':k.total_excl,
                               })

        contract = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.jno==jcno). \
                one()
        contractname = str(contract.jno) + '- ' + contract.site+ '- ' + contract.description
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        userdata.append([datetime.date(datetime.now()),
                        "Contract vs All Subcon Payment Records",
                        contractname,
                        "All",
                        "Any",
                        "Any",
                        "Any",
                        totalexcl,
                        "",
                        ])
        headers =["Pay Run","Pay Date","Trading Name","JCNo","Item",
                "Description","Unit","Qty","Price",
                "Total",]
        headerwidths=[50,80,150,50,50,
                     150,50,50,50,
                      80,
                      ]
        pdffile.CreatePDFSubconJCNoAllPaymentData(userdata,paymentrun,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_subcon_payment_summaries_all_pdf(self,paymentrun_id):
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDF(filename)
        wip1 = []
        userdata = []
        paymentruns = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                filter(JistSubconPaymentRunsList.id==paymentrun_id). \
                one()
        suball = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()
        subout = []
        for sub in suball:
            subtotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                    filter(JistSubconPaymentRunsData.paylist_id==paymentruns.id). \
                    filter(JistSubconPaymentRunsData.sub_id==sub.id). \
                    value(func.sum(JistSubconPaymentRunsData.total_excl))
            div = DBS_JistLabour.query(JistSubconDivisions). \
                    filter(JistSubconDivisions.id==sub.division). \
                    one()
            if not div.division_leader:
                usernow = User.by_user_id(1)
            else:
                usernow = User.by_user_id(div.division_leader)

            subout.append({'name':sub.trading_name,
                            'division_leader':usernow.user_name,
                            'total':subtotal
                          })
        alltotal = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==paymentruns.id). \
                    value(func.sum(JistSubconPaymentRunsData.total_excl))
        userdata.append([datetime.date(datetime.now()),
                        "Payment Summary All Subcons",
                        alltotal,
                        paymentruns.payment_date,
                        paymentruns.start_date,
                        paymentruns.end_date,
                        ])
        headers =["Subcon Name","Division Leader","Total"]
        headerwidths=[300,300,100]
        pdffile.CreatePDFDivisionSummariesAll(userdata,subout,headers,headerwidths)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent


    ################################################################################
    ####################START OF THE ASYNC LABOUR###################################
    ################################################################################
    ################################################################################

    @expose('jistdocstore.templates.labour.labour_employees_console')
    def labour_employees_console(self,**named):
        return dict(page='Labour Employee Console',
                    wip = '',
                    )

    @expose('jistdocstore.templates.labour.labour_teams_console')
    def labour_teams_console(self,**named):
        return dict(page='Labour Teams Console',
                    wip = '',
                    )

    @expose('jistdocstore.templates.labour.labour_teams_schedule_console')
    def labour_teams_schedule_console(self,**named):
        return dict(page='Labour Teams Schedule Console',
                    wip = '',
                    )


    @expose()
    def export_labour_list_active_html_old(self):
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.active==True). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         'active':k.active,
                         'addpic':"""<input type='file' id='id_add_pic' name='id_add_pic'>"""
                         })
        headers =["ID","Empl. Number","Last Name","First Name","ID Number","Date Started","Active","Add Pic"]
        #(lab['id'],lab['emp_number'],lab['last_name'],lab['first_name'],lab['id_number'],lab['date_started'],lab['active'])
        headerwidths=[50,80,200,200,80,80,80,80]
        dictlist = ['id','emp_number','last_name','first_name','id_number','date_started','active','addpic']
        tdclassnames=['','','','','','','','','','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="active_labour_tbl")
        #header = """<h4 class="modal-content"> Labour Categories<span class='spanright'> {0} categories </span></h4>""".format(len(outputlist))
        #htmltbl = self.build_labour_html_table(headers,headerwidths,lablist)
        return htmltbl

    @expose()
    def export_labour_categories_active_html(self):
        wip1 = []
        labcatog = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        outputlist = []
        for k in labcatog:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'id':k.id,
                         'catname':k.category_name,
                         'active':k.active,
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                         })
        headers =["ID","Category Name","Edit","Open"]
        headerwidths=[50,'',30,30,200,80,80,80]
        dictlist = ['id','catname','edit','open']
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_categories_list")
        header = """<h4 class="modal-content"> Labour Categories<span class='spanright'> {0} categories </span></h4>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_labour_list_active_html(self):
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.active==True). \
                all()
        outputlist = []
        for k in lblist:
            pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(k.id))
            if not os.path.exists(pic_path):  
                labourpic = """ <img  id="labpic" title="{0}" src="/images/labourpics/{1}.png"></img>""".format(k.first_name + ' ' + k.last_name,"user_lab_none")
            else:
                labourpic = """ <img  id="labpic" title="{0}" src="/images/labourpics/labour_{1}.png"></img>""".format(k.first_name + ' ' + k.last_name,k.id)
            outputlist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         'active':k.active,
                         'staffpic':labourpic
                         })
        headers =["ID","Last Name","First Name","Pic"]
        headerwidths=[50,80,'',80,80,80,80]
        dictlist = ['id','last_name','first_name','staffpic']
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_labourlist")
        header = """<h4 class="modal-content"> Labour Force<span class='spanright'> {0} people </span></h4>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_subcon_list_active_html(self):
        wip1 = []
        lblist = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()
        outputlist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'id':k.id,
                         'trading_name':k.trading_name,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         })
        headers =["ID","Trading Name","Last Name","First Name"]
        headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['id','trading_name','last_name','first_name']
        headerwidths=[30,'',80,80,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_subconlist")
        header = """<h4 class="modal-content"> Subcons<span class='spanright'> {0} teams </span></h4>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_staff_list_active_html(self):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            #for permis in userpermissions:
                #print permis.permission_name
                #print permis
                #for m in permis:
                    #print m
                #if 'production' in permis:
                    #print "its found"
            if 'productionmanage' not in permissionlist:
                productionlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })
        outputlist = []
        for k in productionlist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'user_id':k['user_id'],
                         'user_name':k['user_name'],
                         'staffpic':""" <img  id="req_by_user_all" title="{0}" src="/images/staffpics/{1}.png"></img>""".format(k['user_name'],k['user_id'])
                         })
        headers =["ID","User Name","Pic"]
        #headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['user_id','user_name','staffpic']
        headerwidths=[30,'',30,30,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_supportlist")
        header = """<h4 class="modal-content"> Support Staff<span class='spanright'> {0} people </span></h4>""".format(len(outputlist)-1)
        return header + htmltbl

    @expose()
    def export_point_list_active_html(self):
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
        outputlist = []
        for k in pointlist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({
                         'user_id':k['user_id'],
                         'user_name':k['user_name'],
                         'staffpic':""" <img  id="req_by_user_all" title="{0}" src="/images/staffpics/{1}.png"></img>""".format(k['user_name'],k['user_id'])
                         })
        headers =["ID","User Name",'Pic']
        dictlist = ['user_id','user_name','staffpic']
        headerwidths=[30,'',30,80,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_pointlist")
        header = """<h4 class="modal-content"> Point List<span class='spanright'> {0} people </span></h4>""".format(len(outputlist)-1)
        return header + htmltbl

    @expose()
    def export_team_labour_list_active_html(self):
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.active==True). \
                all()
        outputlist = []
        for k in lblist:
            pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(k.id))
            if not os.path.exists(pic_path):  
                labourpic = """ <img  id="labpic" title="{0}" src="/images/labourpics/{1}.png"></img>""".format(k.first_name + ' ' + k.last_name,"user_lab_none")
            else:
                labourpic = """ <img  id="labpic" title="{0}" src="/images/labourpics/labour_{1}.png"></img>""".format(k.first_name + ' ' + k.last_name,k.id)
            outputlist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         'active':k.active,
                         'staffpic':labourpic
                         })
        headers =["ID","Last Name","First Name","Pic"]
        headerwidths=[50,80,'',30,80,80,80]
        dictlist = ['id','last_name','first_name','staffpic']
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_labourlist")
        header = """<h4 class="modal-content"> Labour Force<span class='spanright'> {0} people </span></h4>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_team_subcon_list_active_html(self):
        wip1 = []
        lblist = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()
        outputlist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'id':k.id,
                         'trading_name':k.trading_name,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         })
        headers =["ID","Trading Name","Last Name","First Name"]
        headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['id','trading_name','last_name','first_name']
        headerwidths=[30,'',80,80,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_subconlist")
        header = """<h4 class="modal-content"> Subcons<span class='spanright'> {0} teams </span></h4>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_team_staff_list_active_html(self):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            if 'productionmanage' not in permissionlist:
                productionlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })
        outputlist = []
        for k in productionlist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'user_id':k['user_id'],
                         'user_name':k['user_name'],
                         'staffpic':""" <img  id="req_by_user_all" title="{0}" src="/images/staffpics/{1}.png"></img>""".format(k['user_name'],k['user_id'])
                         })
        headers =["ID","User Name","Pic"]
        #headerwidths=[50,200,200,200,80,80,80]
        #htmltbl = self.build_labour_html_table(headers,headerwidths,lablist)
        dictlist = ['user_id','user_name','staffpic']
        headerwidths=[30,'',30,30,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_supportlist")
        header = """<h4 class="modal-content"> Support Staff<span class='spanright'> {0} people </span></h4>""".format(len(outputlist)-1)
        return header + htmltbl

    @expose()
    def export_team_point_list_active_html(self): 
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
        outputlist = []
        for k in pointlist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({
                         'user_id':k['user_id'],
                         'user_name':k['user_name'],
                         'staffpic':""" <img  id="req_by_user_all" title="{0}" src="/images/staffpics/{1}.png"></img>""".format(k['user_name'],k['user_id'])
                         })
        headers =["ID","User Name",'Pic']
        #htmltbl = self.build_labour_html_table(headers,headerwidths,lablist)
        dictlist = ['user_id','user_name','staffpic']
        headerwidths=[30,'',30,80,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_pointlist")
        header = """<h4 class="modal-content"> Point List<span class='spanright'> {0} people </span></h4>""".format(len(outputlist)-1)
        return header + htmltbl


    @expose()
    def export_labour_divisions_active_html(self):
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.active==True). \
                all()
        outputlist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'id':k.id,
                         'div_code':k.division_code,
                         'div_name':k.division_name,
                         'div_leader':k.division_leader,
                         'active':k.active,
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                         })
        headers =["ID","Division Name","Edit","Open"]
        headerwidths=[50,'',30,30,80,80]
        dictlist = ['id','div_name','edit','open']
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_division_list")
        header = """<h4 class="modal-content"> Divisions<span class='spanright'> {0} divisions </span></h4>""".format(len(outputlist))
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_division_add">Add Division</button><p/>"""
        return header+btnadddivision+ htmltbl

    @expose()
    def get_table_data_labour_divisions(self,**kw):
        divid = kw['itemid']
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==divid). \
                one()
        labdivision_all = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.division==divid). \
                filter(JistLabourList.active==True). \
                all()
        outputlist = []
        for k in labdivision_all:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({'id':k.id,
                         'div_code':k.division,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'active':k.active,
                           'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                         })
        headers =["ID","Last Name","First Name","Move","Job"]
        headerwidths=[50,'','',30,30,30]
        dictlist = ['id','last_name','first_name','move','job']
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_labour_division_list")

        header = """<h4 class="modal-content"> {1} - Labour<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.division_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_point_divisions(self,**kw):
        divid = kw['itemid']
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
        outputlist = []
        lblist = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==divid). \
                one()
        labdivision_all = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.division==divid). \
                filter(JistLabourList.active==True). \
                all()
        for k in pointlist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            try:
                staffdivision_link = DBS_JistLabour.query(JistPointDivisionLink). \
                        filter(JistPointDivisionLink.user_id==k['user_id']). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistPointDivisionLink()
                link.user_id = k['user_id']
                link.lab_division_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        staffdivisions_list = DBS_JistLabour.query(JistPointDivisionLink). \
                filter(JistPointDivisionLink.lab_division_id==divid). \
                all()
        for k in staffdivisions_list:
            activeuser = DBS_ContractData.query(User).filter(User.user_id==k.user_id).one()
            outputlist.append({
                         'user_id':activeuser.user_id,
                         'user_name':activeuser.user_name,
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format('something'),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                         })
        headers =["ID","User Name","Move","Job"]
        headerwidths=[50,'',30,30,80,80]
        dictlist = ['user_id','user_name','move','job']
        tdclassnames=['','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_point_division_list")
        header = """<h4 class="modal-content"> {1} - Point<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.division_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_subcon_divisions(self,**kw):
        divid = kw['itemid']
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []

        outputlist = []
        lblist = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==divid). \
                one()
        subconall = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()

        for k in subconall:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            try:
                staffdivision_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                        filter(JistSubconDivisionLink.user_id==k.id). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistSubconDivisionLink()
                link.user_id = k.id
                link.lab_division_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        staffdivisions_list = DBS_JistLabour.query(JistSubconDivisionLink). \
                filter(JistSubconDivisionLink.lab_division_id==divid). \
                all()
        for k in staffdivisions_list:
            subconone = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.id==k.user_id). \
                    one()
            if subconone.active:
                outputlist.append({
                             'user_id':subconone.id,
                             'user_name':subconone.trading_name,
                               'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                               'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                               'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                               'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                               'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                               'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format('something'),
                               'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                             })
        headers =["ID","Trading Name","Move","Job"]
        headerwidths=[50,'',30,30,80,80]
        dictlist = ['user_id','user_name','move','job']
        tdclassnames=['','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_subcon_division_list")
        header = """<h4 class="modal-content"> {1} - Subcons<span class='spanright'> {0} teams </span></h4>""".format(len(outputlist),lblist.division_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_staff_divisions(self,**kw):
        divid = kw['itemid']
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            #if 'production' in permissionlist:
            if 'productionmanage' not in permissionlist:
                productionlist.append({'user_id': point.user_id,
                                  'user_name': point.user_name,
                                  'display_name': point.display_name
                                  })
        lblist = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==divid). \
                one()
        labdivision_all = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.division==divid). \
                filter(JistLabourList.active==True). \
                all()
        outputlist = []
        for k in productionlist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            try:
                staffdivision_link = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==k['user_id']). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistStaffDivisionLink()
                link.user_id = k['user_id']
                link.lab_division_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        staffdivisions_list = DBS_JistLabour.query(JistStaffDivisionLink). \
                filter(JistStaffDivisionLink.lab_division_id==divid). \
                all()
        for k in staffdivisions_list:
            activeuser = DBS_ContractData.query(User).filter(User.user_id==k.user_id).one()
            if activeuser.active_status:
                outputlist.append({
                             'user_id':activeuser.user_id,
                             'user_name':activeuser.user_name,
                               'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                               'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                               'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                               'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                               'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                               'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format('something'),
                               'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                             })
        headers =["ID","User Name","Move","Job"]
        headerwidths=[50,'',30,30,30,80]
        dictlist = ['user_id','user_name','move','job']
        tdclassnames=['','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_staff_division_list")
        header = """<h4 class="modal-content"> {1} - Support Staff<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.division_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_labour_categories(self,**kw):
        categoryid = kw['itemid']
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.id==categoryid). \
                one()
        labdivision_all = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.active==True). \
                all()
        outputlist = []
        for k in labdivision_all:
            try:
                labcategory_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                        filter(JistLabourCategoryLink.user_id==k.id). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistLabourCategoryLink()
                link.user_id = k.id
                link.lab_category_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        labcategory_list = DBS_JistLabour.query(JistLabourCategoryLink). \
                filter(JistLabourCategoryLink.lab_category_id==categoryid). \
                all()
        for k in labcategory_list:
            thisuser = DBS_JistLabour.query(JistLabourList). \
                    filter(JistLabourList.id==k.user_id).one()
            outputlist.append({'id':k.user_id,
                         'last_name':thisuser.last_name,
                         'first_name':thisuser.first_name,
                         'active':thisuser.active,
                           'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.user_id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                           'spacer':'',
                         })
        headers =["ID","Last Name","First Name","Move",""]
        headerwidths=[50,'','',30,30,5]
        dictlist = ['id','last_name','first_name','move','spacer']
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_labour_category_list")
        header = """<h4 class="modal-content"> {1} - Labour<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.category_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_point_categories(self,**kw):
        categoryid = kw['itemid']
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
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.id==categoryid). \
                one()
        #labdivision_all = DBS_JistLabour.query(JistLabourList). \
                #filter(JistLabourList.active==True). \
                #all()
        outputlist = []
        for k in pointlist:
            try:
                labcategory_link = DBS_JistLabour.query(JistPointCategoryLink). \
                        filter(JistPointCategoryLink.user_id==k['user_id']). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistPointCategoryLink()
                link.user_id = k['user_id']
                link.lab_category_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        labcategory_list = DBS_JistLabour.query(JistPointCategoryLink). \
                filter(JistPointCategoryLink.lab_category_id==categoryid). \
                all()
        for k in labcategory_list:
            #thisuser = DBS_JistLabour.query(JistLabourList). \
                    #filter(JistLabourList.id==k.user_id).one()
            thisuser = DBS_ContractData.query(User).filter(User.user_id==k.user_id).one()
            outputlist.append({'id':k.user_id,
                         'last_name':thisuser.user_name,
                         'first_name':thisuser.display_name,
                         'active':'',
                           'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                           'spacer':'',
                         })
        headers =["ID","User Name","Move",""]
        headerwidths=[50,'',30,30,5]
        dictlist = ['id','last_name','move','spacer']
        tdclassnames=['','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_point_category_list")
        header = """<h4 class="modal-content"> {1} - Point<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.category_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_staff_categories(self,**kw):
        categoryid = kw['itemid']
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            #if 'production' in permissionlist:
            if 'productionmanage' not in permissionlist:
                productionlist.append({'user_id': point.user_id,
                                  'user_name': point.user_name,
                                  'display_name': point.display_name
                                  })
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.id==categoryid). \
                one()
        #labdivision_all = DBS_JistLabour.query(JistLabourList). \
                #filter(JistLabourList.active==True). \
                #all()
        outputlist = []
        for k in productionlist:
            try:
                labcategory_link = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==k['user_id']). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistStaffCategoryLink()
                link.user_id = k['user_id']
                link.lab_category_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        labcategory_list = DBS_JistLabour.query(JistStaffCategoryLink). \
                filter(JistStaffCategoryLink.lab_category_id==categoryid). \
                all()
        for k in labcategory_list:
            #thisuser = DBS_JistLabour.query(JistLabourList). \
                    #filter(JistLabourList.id==k.user_id).one()
            thisuser = DBS_ContractData.query(User).filter(User.user_id==k.user_id).one()
            outputlist.append({'id':k.user_id,
                         'last_name':thisuser.user_name,
                         'first_name':thisuser.display_name,
                         'active':'',
                           'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                           'spacer':'',
                         })
        headers =["ID","User Name","Move",""]
        headerwidths=[50,'',30,30,5]
        dictlist = ['id','last_name','move','spacer']
        tdclassnames=['','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_staff_category_list")
        header = """<h4 class="modal-content"> {1} - Support Staff<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.category_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_table_data_subcon_categories(self,**kw):
        categoryid = kw['itemid']
        wip1 = []
        lblist = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.id==categoryid). \
                one()
        labdivision_all = DBS_JistLabour.query(JistSubconList). \
                filter(JistSubconList.active==True). \
                all()
        outputlist = []
        for k in labdivision_all:
            try:
                labcategory_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                        filter(JistSubconCategoryLink.user_id==k.id). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistSubconCategoryLink()
                link.user_id = k.id
                link.lab_category_id = 1
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
        labcategory_list = DBS_JistLabour.query(JistSubconCategoryLink). \
                filter(JistSubconCategoryLink.lab_category_id==categoryid). \
                all()
        for k in labcategory_list:
            thisuser = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.id==k.user_id).one()
            outputlist.append({'id':k.user_id,
                         'last_name':thisuser.trading_name,
                         'first_name':thisuser.first_name,
                         'active':thisuser.active,
                           'move':"<img id='move_division_labour_item' src='/images/arrow-up-2.png'></img>",
                           'add':"<img id='add_labour_item' src='/images/shopping_basket_add_32.png'></img>",
                           'edit':"<img id='delete_labour_item' src='/images/edit-4.png'></img>",
                           'job':"<img id='labour_category' src='/images/user_mapping_48.png'></img>",
                           'trash':"<img id='delete_labour_item' src='/images/trash.png'></img>",
                           'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_labour_item' src='/images/pdficon.jpg'></img></a>".format(k.user_id),
                           'open':"<img id='open_labour_item' src='/images/project-open.png'></img>",
                           'spacer':'',
                         })
        headers =["ID","Trading Name","Move",""]
        headerwidths=[50,'',30,30,5]
        dictlist = ['id','last_name','move','spacer']
        tdclassnames=['','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_subcon_category_list")
        header = """<h4 class="modal-content"> {1} - Subcons<span class='spanright'> {0} people </span></h4>""".format(len(outputlist),lblist.category_name)
        btnadddivision = """<button class="ui-widget ui-widget-content ui-state-default" id="button_member_add_division">Add Member</button><p/>"""
        return header+ htmltbl

    @expose()
    def get_dialog_change_labour_division(self,**kw):
        labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        html1 = """
        <div id="dialog_division_change" title="Division Change">
            <form id="dialog_division_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>

                """.format(labour_id)
        html3 = """
                    <label for="">Move To Division</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in divisionlistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.division_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_labour_division(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==user_id). \
                one()
        lablist_one.division=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_labour_category(self,**kw):
        labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        categorylistall = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        html1 = """
        <div id="dialog_category_change" title="Category Change">
            <form id="dialog_category_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>
                """.format(labour_id)
        html3 = """
                    <label for="">Choose Category</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in categorylistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.category_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_labour_category(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistLabourCategoryLink). \
                filter(JistLabourCategoryLink.user_id==user_id). \
                one()
        lablist_one.lab_category_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_point_category(self,**kw):
        labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        categorylistall = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        html1 = """
        <div id="dialog_category_change" title="Category Change">
            <form id="dialog_category_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>
                """.format(labour_id)
        html3 = """
                    <label for="">Choose Category</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in categorylistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.category_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_point_category(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistPointCategoryLink). \
                filter(JistPointCategoryLink.user_id==user_id). \
                one()
        lablist_one.lab_category_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_staff_category(self,**kw):
        labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        categorylistall = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        html1 = """
        <div id="dialog_category_change" title="Category Change">
            <form id="dialog_category_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>
                """.format(labour_id)
        html3 = """
                    <label for="">Choose Category</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in categorylistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.category_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_staff_category(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistStaffCategoryLink). \
                filter(JistStaffCategoryLink.user_id==user_id). \
                one()
        lablist_one.lab_category_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_subcon_category(self,**kw):
        labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        categorylistall = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        html1 = """
        <div id="dialog_category_change" title="Category Change">
            <form id="dialog_category_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>
                """.format(labour_id)
        html3 = """
                    <label for="">Choose Category</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in categorylistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.category_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_subcon_category(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistSubconCategoryLink). \
                filter(JistSubconCategoryLink.user_id==user_id). \
                one()
        lablist_one.lab_category_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_staff_division(self,**kw):
        #labour_id = kw['labour_id']
        staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        html1 = """
        <div id="dialog_division_change" title="Division Change">
            <form id="dialog_division_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>

                """.format(staff_id)
        html3 = """
                    <label for="">Move To Division</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in divisionlistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.division_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_staff_division(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistStaffDivisionLink). \
                filter(JistStaffDivisionLink.user_id==user_id). \
                one()
        lablist_one.lab_division_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_point_division(self,**kw):
        #labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        html1 = """
        <div id="dialog_division_change" title="Division Change">
            <form id="dialog_division_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>

                """.format(point_id)
        html3 = """
                    <label for="">Move To Division</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in divisionlistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.division_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_point_division(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistPointDivisionLink). \
                filter(JistPointDivisionLink.user_id==user_id). \
                one()
        lablist_one.lab_division_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_subcon_division(self,**kw):
        #labour_id = kw['labour_id']
        #staff_id = kw['staff_id']
        subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        html1 = """
        <div id="dialog_division_change" title="Division Change">
            <form id="dialog_division_change_frm">
                <fieldset>
                    <label for="">For ID</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <br/>

                """.format(subcon_id)
        html3 = """
                    <label for="">Move To Division</label><br/>
                    <select id='div_to' name='div_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in divisionlistall: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.division_name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1 + html3 + html4

    @expose()
    def save_dialog_change_subcon_division(self,**kw):
        user_id = kw['from_id']
        divid = kw['div_to']
        lablist_one = DBS_JistLabour.query(JistSubconDivisionLink). \
                filter(JistSubconDivisionLink.user_id==user_id). \
                one()
        lablist_one.lab_division_id=divid
        DBS_JistLabour.flush()

    @expose()
    def get_dialog_change_division_name(self,**kw):
        divisionid = kw['division_id']
        #staff_id = kw['staff_id']
        #subcon_id = kw['subcon_id']
        #point_id = kw['point_id']
        division = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.id == divisionid).one()
        html1 = """
        <div id="dialog_division_change" title="Division Change">
            <form id="dialog_division_change_frm">
                <fieldset>
                    <label for="">Division Name</label><br/>
                    <input type='text' value={0} id='from_id' name='from_id' class="text ui-widget-content ui-corner-all" >
                    <label for="">Division Name</label><br/>
                    <input type='text' value='{1}' id='name' name='name' class="text ui-widget-content ui-corner-all" >
                    <br/>

                """.format(division.id,division.division_name)
        html4 = """
                </fieldset>
                </form>
               </div>
                """
        return html1  + html4

    @expose()
    def save_dialog_change_division_name(self,**kw):
        division_id = kw['from_id']
        division_name = kw['name']
        lablist_one = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==division_id). \
                one()
        lablist_one.division_name = division_name
        DBS_JistLabour.flush()

    @expose()
    def get_labour_division_people_html(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        endtoday = datetime.date(datetime.now()) - timedelta(weeks=10)
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(endtoday,sttimestart)
        #lblist = DBS_JistLabour.query(JistLabourDivisions). \
                #filter(JistLabourDivisions.id==divid). \
                #one()
        divisions_all = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.active==True). \
                all()
        #Create html accordion 
        header = """<h4 class="modal-content">Divisions View<span class='spanright'>  </span></h4>"""
        html1 = header + """<div id="labour_divisions_people_accordion">"""
        html2 = ''
        htmltemp = ''
        man_stages_list = []
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        #for k in staffdivisions_list:
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            if 'productionmanage' not in permissionlist:
                productionlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })
        for divis in divisions_all:
            lab_all_division = DBS_JistLabour.query(JistLabourList). \
                    filter(JistLabourList.division==divis.id). \
                    filter(JistLabourList.active==True). \
                    all()
            subcon_all_division = DBS_JistLabour.query(JistSubconDivisionLink). \
                    filter(JistSubconDivisionLink.lab_division_id==divis.id). \
                    all()
            staff_all_division = DBS_JistLabour.query(JistStaffDivisionLink). \
                    filter(JistStaffDivisionLink.lab_division_id==divis.id). \
                    all()
            sum_lab = len(lab_all_division)
            sum_subcon = len(subcon_all_division)
            sum_staff = len(staff_all_division)
            division_sum = sum_lab + sum_subcon + sum_staff
            htmltemp = """
                        <div class='accord_header'>
                        <h3>{0}<span class='accord_qty'>{1} people</span></h3>
                            <div>
                       """.format(
                              divis.division_name ,
                              division_sum
                               )
            htmlfaces = ''
            for lab in productionlist:
                staffdivision = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==lab['user_id']). \
                        one()
                staffcategory = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==lab['user_id']). \
                        one()
                if staffdivision.lab_division_id == divis.id:
                    pic_path = os.path.join(staff_picdir, "{0}.png".format(lab['user_id']))
                    category_this = DBS_JistLabour.query(JistLabourCategories). \
                            filter(JistLabourCategories.id==staffcategory.lab_category_id). \
                            one()
                    if not os.path.exists(pic_path):  
                        staffpic = """
                                    <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                            <li class="ui-widget-content ui-corner-tr">
                                            <h6 class="ui-widget-header">{0}</h6>
                                            <img class="div_staff_pic"  id="staffpic" title="{0}" src="/images/staffpics/{1}.png"></img>
                                            <h6 class="ui-widget-header">{2}</h6>
                                            </li>
                                    </ul>
                        """.format(lab['user_name'],"user_lab_none",category_this.category_name)
                    else:
                        staffpic = """ 
                                    <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                            <li class="ui-widget-content ui-corner-tr">
                                            <h6 class="ui-widget-header">{0}</h6>
                                            <img  class="div_staff_pic"  id="staffpic" title="{0}" src="/images/staffpics/{1}.png"></img>
                                            <h6 class="ui-widget-header">{2}</h6>
                                            </li>
                                    </ul>
                        """.format(lab['user_name'],lab['user_id'],category_this.category_name)
                    htmlfaces =  htmlfaces + staffpic 
            for lab in lab_all_division: 
                #print lab.first_name
                pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(lab.id))
                divisions_this = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==lab.division). \
                        one()
                category_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                        filter(JistLabourCategoryLink.user_id==lab.id). \
                        one()
                category_this = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category_link.lab_category_id). \
                        one()
                if not os.path.exists(pic_path):  
                    labourpic = """ 
                                    <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                            <li class="ui-widget-content ui-corner-tr">
                                            <h6 class="ui-widget-header">{0}</h6>
                                            <img   class="div_lab_pic" id="labpic" title="{0}" src="/images/labourpics/{1}.png"></img>
                                            <h6 class="ui-widget-header">{2}</h6>
                                            </li>
                                    </ul>
                                """.format(lab.first_name +' '+ lab.last_name,"user_lab_none",category_this.category_name)
                else:
                    labourpic = """ 

                                    <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                            <li class="ui-widget-content ui-corner-tr">
                                            <h6 class="ui-widget-header">{0}</h6>
                                            <img   class="div_lab_pic" id="labpic" title="{0}" src="/images/labourpics/labour_{1}.png"></img>
                                            <h6 class="ui-widget-header">{2}</h6>
                                            </li>
                                    </ul>
                                """.format(lab.first_name +' '+ lab.last_name,lab.id,category_this.category_name)
                htmlfaces =  htmlfaces + labourpic 
            for lab in subcon_all_division: 
                pic_path = os.path.join(labour_picdir, "subcon_{0}.png".format(lab.user_id))
                subconone = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==lab.user_id).one()
                if subconone.active == True:
                    category_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                            filter(JistSubconCategoryLink.user_id==subconone.id). \
                            one()
                    category_this = DBS_JistLabour.query(JistLabourCategories). \
                            filter(JistLabourCategories.id==category_link.lab_category_id). \
                            one()
                    if not os.path.exists(pic_path):  
                        labourpic = """ 
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                        <img  class="div_subcon_pic"  id="labpic" title="{0}" src="/images/subconpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                        
                                    """.format(subconone.trading_name,"user_subcon_none",category_this.category_name)
                    else:
                        labourpic = """ 
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                        <img  class="div_subcon_pic" id="labpic" title="{0}" src="/images/subconpics/subcon_{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>

                                    """.format(subconone.trading_name,lab.subconone.id,category_this.category_name)
                    htmlfaces =  htmlfaces + labourpic 

            htmllast = """

                            </div>
                        </div>
                       """

            html2 = html2 + htmltemp + htmlfaces + htmllast
        html3 = "</div>"
        htmlitems = ''
        htmldetails = ''
        return  html1 + html2 + html3 

    @expose()
    def get_labour_categories_people_html(self,**kw):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        categorieslist = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        #labdivision_all = DBS_JistLabour.query(JistLabourList). \
                #filter(JistLabourList.active==True). \
                #all()
        header = """<h4 class="modal-content">Categories View<span class='spanright'>  </span></h4>"""
        htmlstaff1 = header + """<div id="labour_categories_people_accordion">"""
        html2 = ''
        htmltemp = ''
        for category in categorieslist:
            staff_all_categories = DBS_JistLabour.query(JistStaffCategoryLink). \
                    filter(JistStaffCategoryLink.lab_category_id==category.id). \
                    all()
            labour_all_categories = DBS_JistLabour.query(JistLabourCategoryLink). \
                    filter(JistLabourCategoryLink.lab_category_id==category.id). \
                    all()
            subcon_all_categories = DBS_JistLabour.query(JistSubconCategoryLink). \
                    filter(JistSubconCategoryLink.lab_category_id==category.id). \
                    all()
            if len(staff_all_categories) > 0:
                category_sum = len(staff_all_categories)
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category.id). \
                        one()
                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0} [Staff]<span class='accord_qty'>{1} people</span></h3>
                                <div>
                           """.format(
                                  categoryone.category_name ,
                                  category_sum 
                                   )
                htmlfaces = ''
                for staff_cat in staff_all_categories:
                    thisuser = DBS_ContractData.query(User).filter(User.user_id==staff_cat.user_id).one()
                    if thisuser.active_status:
                        pic_path = os.path.join(staff_picdir, "{0}.png".format(thisuser.user_id))
                        if not os.path.exists(pic_path):  
                            staffpic = """
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img class="div_staff_pic"  id="staffpic" title="{0}" src="/images/staffpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.user_name,"user_lab_none",categoryone.category_name)
                        else:
                            staffpic = """ 
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_staff_pic"  id="staffpic" title="{0}" src="/images/staffpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.user_name,thisuser.user_id,categoryone.category_name)
                        htmlfaces =  htmlfaces + staffpic 
                htmllast = """

                                </div>
                            </div>
                       """
                html2 = html2 + htmltemp + htmlfaces + htmllast
            if len(labour_all_categories) > 0:
                category_sum = len(labour_all_categories)
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category.id). \
                        one()
                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0} [Labour]<span class='accord_qty'>{1} people</span></h3>
                                <div>
                           """.format(
                                  categoryone.category_name ,
                                  category_sum 
                                   )
                htmlfaces = ''
                for staff_cat in labour_all_categories:
                    thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staff_cat.user_id).one()
                    division_this = DBS_JistLabour.query(JistLabourDivisions). \
                            filter(JistLabourDivisions.id==thisuser.division). \
                            one()
                    if thisuser.active:
                        pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(thisuser.id))
                        if not os.path.exists(pic_path):  
                            staffpic = """
                                        
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix ui-draggable">
                                                <li  class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img class="div_lab_pic"  id="labpic" title="{0}" src="/images/labourpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.first_name,"user_lab_none",division_this.division_name)
                        else:
                            staffpic = """ 
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix ui-draggable">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_lab_pic"  id="labpic" title="{0}" src="/images/labourpics/labour_{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.first_name,thisuser.id,division_this.division_name)
                        htmlfaces =  htmlfaces + staffpic 
                htmllast = """

                                </div>
                            </div>
                       """


                html2 = html2 + htmltemp + htmlfaces + htmllast
            if len(subcon_all_categories) > 0:
                category_sum = len(subcon_all_categories)
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category.id). \
                        one()
                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0} [Subcon]<span class='accord_qty'>{1} Team</span></h3>
                                <div>
                           """.format(
                                  categoryone.category_name ,
                                  category_sum 
                                   )
                htmlfaces = ''
                for staff_cat in subcon_all_categories:
                    thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staff_cat.user_id).one()
                    division_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                            filter(JistSubconDivisionLink.user_id==thisuser.id). \
                            one()
                    division_this = DBS_JistLabour.query(JistLabourDivisions). \
                            filter(JistLabourDivisions.id==division_link.lab_division_id). \
                            one()
                    if thisuser.active:
                        pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(thisuser.id))
                        if not os.path.exists(pic_path):  
                            staffpic = """
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img class="div_subcon_pic"  id="subconpic" title="{0}" src="/images/subconpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.trading_name,"user_subcon_none",division_this.division_name)
                        else:
                            staffpic = """ 
                                        <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_subcon_pic"  id="subconpic" title="{0}" src="/images/subconpics/subcon_{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.trading_name,thisuser.id,division_this.division_name)
                        htmlfaces =  htmlfaces + staffpic 
                htmllast = """

                                </div>
                            </div>
                       """


                html2 = html2 + htmltemp + htmlfaces + htmllast
        htmllastdiv = "</div>"
        htmlitems = ''
        htmldetails = ''
        return  htmlstaff1 + html2 + htmllastdiv 

    @expose()
    def get_contact_details_by_division_people_html(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        endtoday = datetime.date(datetime.now()) - timedelta(weeks=10)
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(endtoday,sttimestart)
        #lblist = DBS_JistLabour.query(JistLabourDivisions). \
                #filter(JistLabourDivisions.id==divid). \
                #one()
        divisions_all = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.active==True). \
                all()
        #Create html accordion 
        html1 = """<div id="labour_divisions_people_accordion">"""
        html2 = ''
        htmltemp = ''
        man_stages_list = []
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        allsumpeople = 0
        #for k in staffdivisions_list:
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            #if 'productionmanage' not in permissionlist:
            if 'productionmanage' in permissionlist:
                pointlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })
            if 'productionmanage' not in permissionlist:
                productionlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })
        for divis in divisions_all:
            point_all_division = DBS_JistLabour.query(JistPointDivisionLink). \
                    filter(JistPointDivisionLink.lab_division_id==divis.id). \
                    all()
            lab_all_division = DBS_JistLabour.query(JistLabourList). \
                    filter(JistLabourList.division==divis.id). \
                    filter(JistLabourList.active==True). \
                    all()
            subcon_all_division = DBS_JistLabour.query(JistSubconDivisionLink). \
                    filter(JistSubconDivisionLink.lab_division_id==divis.id). \
                    all()
            staff_all_division = DBS_JistLabour.query(JistStaffDivisionLink). \
                    filter(JistStaffDivisionLink.lab_division_id==divis.id). \
                    all()
            sum_point = len(point_all_division)
            sum_lab = len(lab_all_division)
            sum_subcon = len(subcon_all_division)
            sum_staff = len(staff_all_division)
            division_sum = sum_point + sum_lab + sum_subcon + sum_staff
            allsumpeople = allsumpeople + division_sum
            htmltemp = """
                        <div class='accord_header'>
                        <h3>{0}<span class='accord_qty'>{1} people</span></h3>
                            <div>
                       """.format(
                              divis.division_name ,
                              division_sum
                               )
            htmlfaces = ''
            for lab in pointlist:
                staffdivision = DBS_JistLabour.query(JistPointDivisionLink). \
                        filter(JistPointDivisionLink.user_id==int(lab['user_id'])). \
                        one()
                staffcategory = DBS_JistLabour.query(JistPointCategoryLink). \
                        filter(JistPointCategoryLink.user_id==lab['user_id']). \
                        one()
                if staffdivision.lab_division_id == divis.id:
                    pic_path = os.path.join(staff_picdir, "{0}.png".format(lab['user_id']))
                    category_this = DBS_JistLabour.query(JistLabourCategories). \
                            filter(JistLabourCategories.id==staffcategory.lab_category_id). \
                            one()
                    staffpic = self.get_labour_picture_html('staff',lab['user_id'],lab['user_name'],divis.division_name,category_this.category_name)
                    htmlfaces =  htmlfaces + staffpic 
            for lab in productionlist:
                staffdivision = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==int(lab['user_id'])). \
                        one()
                staffcategory = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==lab['user_id']). \
                        one()
                if staffdivision.lab_division_id == divis.id:
                    pic_path = os.path.join(staff_picdir, "{0}.png".format(lab['user_id']))
                    category_this = DBS_JistLabour.query(JistLabourCategories). \
                            filter(JistLabourCategories.id==staffcategory.lab_category_id). \
                            one()
                    staffpic = self.get_labour_picture_html('staff',lab['user_id'],lab['user_name'],divis.division_name,category_this.category_name)
                    htmlfaces =  htmlfaces + staffpic 
            for lab in lab_all_division: 
                #print lab.first_name
                pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(lab.id))
                divisions_this = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==lab.division). \
                        one()
                category_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                        filter(JistLabourCategoryLink.user_id==lab.id). \
                        one()
                category_this = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category_link.lab_category_id). \
                        one()
                staffpic = self.get_labour_picture_html('labour',lab.id,lab.first_name +' ' + lab.last_name,divisions_this.division_name,category_this.category_name)
                htmlfaces =  htmlfaces + staffpic 
            for lab in subcon_all_division: 
                pic_path = os.path.join(labour_picdir, "subcon_{0}.png".format(lab.user_id))
                subconone = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==lab.user_id).one()
                if subconone.active == True:
                    category_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                            filter(JistSubconCategoryLink.user_id==subconone.id). \
                            one()
                    category_this = DBS_JistLabour.query(JistLabourCategories). \
                            filter(JistLabourCategories.id==category_link.lab_category_id). \
                            one()
                    staffpic = self.get_labour_picture_html('subcon',subconone.id,subconone.trading_name,divis.division_name,category_this.category_name)
                    htmlfaces =  htmlfaces + staffpic 
            htmllast = """
                            </div>
                        </div>
                       """

            html2 = html2 + htmltemp + htmlfaces + htmllast
            #html2 = html2  + htmlfaces + htmllast
        html3 = "</div>"
        header = """<h4 class="modal-content">Contact Details By Division<span class='spanright'>{0} people</span></h4>""".format(allsumpeople)
        htmlitems = ''
        htmldetails = ''
        return  header + html1 + html2 + html3 

    @expose()
    def get_contact_data_by_person_id(self,**kw):
        staffid = kw['staffid']
        groupid = kw['groupid']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        if groupid == 'staff':
            try:
                contactdata = DBS_JistLabour.query(JistEmployeeContactList). \
                        filter(JistEmployeeContactList.staff_id==staffid). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistEmployeeContactList()
                link.staff_id = staffid
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
            contactdata = DBS_JistLabour.query(JistEmployeeContactList). \
                    filter(JistEmployeeContactList.staff_id==staffid). \
                    one()
            try:
                #See if id is a point
                staff_category = DBS_JistLabour.query(JistPointCategoryLink). \
                        filter(JistPointCategoryLink.user_id==staffid). \
                        one()
                category_this = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==staff_category.lab_category_id). \
                        one()
                pointdivision_link = DBS_JistLabour.query(JistPointDivisionLink). \
                        filter(JistPointDivisionLink.user_id==staffid). \
                        one()
                division_one = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==pointdivision_link.lab_division_id). \
                        one()
            except:
                #else its a normal staff
                staff_category = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==staffid). \
                        one()
                category_this = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==staff_category.lab_category_id). \
                        one()
                pointdivision_link = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==staffid). \
                        one()
                division_one = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==pointdivision_link.lab_division_id). \
                        one()
            thisuser = DBS_ContractData.query(User).filter(User.user_id==staffid).one()
            staffpic = self.get_labour_picture_html('staff',thisuser.user_id,thisuser.user_name,division_one.division_name,category_this.category_name)
        elif groupid == 'labour':
            try:
                contactdata = DBS_JistLabour.query(JistEmployeeContactList). \
                        filter(JistEmployeeContactList.lab_id==staffid). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistEmployeeContactList()
                link.lab_id = staffid
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
            contactdata = DBS_JistLabour.query(JistEmployeeContactList). \
                    filter(JistEmployeeContactList.lab_id==staffid). \
                    one()
            thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staffid).one()
            staff_category = DBS_JistLabour.query(JistLabourCategoryLink). \
                    filter(JistLabourCategoryLink.user_id==staffid). \
                    one()
            category_this = DBS_JistLabour.query(JistLabourCategories). \
                    filter(JistLabourCategories.id==staff_category.lab_category_id). \
                    one()
            #pointdivision_link = DBS_JistLabour.query(JistLabourList). \
                    #filter(JistLabourList.division==staffid). \
                    #one()
            division_one = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.id==thisuser.division). \
                    one()

            staffpic = self.get_labour_picture_html('labour',thisuser.id,thisuser.first_name+' '+thisuser.last_name,division_one.division_name,category_this.category_name)
        elif groupid == 'subcon':
            try:
                contactdata = DBS_JistLabour.query(JistEmployeeContactList). \
                        filter(JistEmployeeContactList.subcon_id==staffid). \
                        one()
            except:
                #Create the record
                username = request.identity['repoze.who.userid']
                usernow = User.by_user_name(username)
                link = JistEmployeeContactList()
                link.subcon_id = staffid
                link.useridnew = usernow.user_id
                link.useridedited = usernow.user_id
                link.dateedited = datetime.date(datetime.now()) 
                link.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(link)
                DBS_JistLabour.flush()
            contactdata = DBS_JistLabour.query(JistEmployeeContactList). \
                    filter(JistEmployeeContactList.subcon_id==staffid). \
                    one()
            thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staffid).one()
            staff_category = DBS_JistLabour.query(JistSubconCategoryLink). \
                    filter(JistSubconCategoryLink.user_id==staffid). \
                    one()
            category_this = DBS_JistLabour.query(JistLabourCategories). \
                    filter(JistLabourCategories.id==staff_category.lab_category_id). \
                    one()
            pointdivision_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                    filter(JistSubconDivisionLink.user_id==staffid). \
                    one()
            division_one = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.id==pointdivision_link.lab_division_id). \
                    one()

            staffpic = self.get_labour_picture_html('subcon',thisuser.id,thisuser.trading_name,division_one.division_name,category_this.category_name)

        html1 = """
                    <form id="employee_contact_data_frm">
                            {9}
                        <fieldset>
                            <label for="">Contact ID</label><br/>
                            <input value="{0}" name="staffid" id="staffid" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Office</label><br/>
                            <input value="{1}" name="office" id="office" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Office Tel</label><br/>
                            <input value="{2}" name="office_tel" id="office_tel" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Office Extention</label><br/>
                            <input value="{3}" name="office_ext" id="office_ext" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Mobile 1</label><br/>
                            <input value="{4}" name="mobile1" id="mobile1" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Mobile 2</label><br/>
                            <input value="{5}" name="mobile2" id="mobile2" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Mobile 3</label><br/>
                            <input value="{6}" name="mobile3" id="mobile3" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Email</label><br/>
                            <input value="{7}" name="email" id="email" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Sip</label><br/>
                            <input value="{8}" name="sip" id="sip" class="text ui-widget-content ui-corner-all" /><br/>
                            <p/>
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_edit_save_contact">Submit Changes</button>
                        </fieldset>
                    </form>
                <button class="ui-widget ui-widget-content ui-state-default" id="button_edit_contact">Edit Contact Details</button>
                """.format(contactdata.id,contactdata.office,contactdata.office_tel,
                        contactdata.office_ext,contactdata.mobile_tel1,contactdata.mobile_tel2,contactdata.mobile_tel3,
                        contactdata.email,contactdata.sip,staffpic)
        return html1 

    @expose()
    def save_contact_data_by_person_id(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        staffid = kw['staffid']
        office = kw['office']
        office_tel = kw['office_tel']
        office_ext = kw['office_ext']
        mobile1 = kw['mobile1']
        mobile2 = kw['mobile2']
        mobile3 = kw['mobile3']
        email = kw['email']
        sip = kw['sip']
        data = DBS_JistLabour.query(JistEmployeeContactList). \
                filter(JistEmployeeContactList.id==staffid). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        data.office = office
        data.office_tel = office_tel
        data.office_ext = office_ext
        data.mobile_tel1 = mobile1
        data.mobile_tel2 = mobile2
        data.mobile_tel3 = mobile3
        data.email = email 
        data.sip = sip
        data.useridedited = usernow.user_id
        data.dateedited = datetime.date(datetime.now()) 
        DBS_JistLabour.flush()


    @expose()
    def get_dialog_add_division(self,**kw):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        pointlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            user = User.by_user_id(point.user_id)
            userpermissions = user.permissions
            permissionlist = [permis.permission_name for permis in userpermissions]
            if 'productionmanage' in permissionlist:
                pointlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })
        html1 = """
                <div id="dialog_add_division_item" title="Add Division">
                    <form id="dialog_add_division_item_frm">
                        <fieldset>
                            <label for="">Division Name</label>
                            <input type="text" name="divisionname" id="divisionname" class="text ui-widget-content ui-corner-all" /><br/>
               """
        html2 = """
                """
        html3 = """
                    <label for="">Person In Charge</label>
                      <select id="point_person" class="text ui-widget-content ui-corner-all">
                """
        for point in pointlist:
            html3temp = """
                        <option value="%s">%s</option>

                          """%(point['user_id'],point['user_name'])
            html3 = html3 + html3temp
        
        html4 = """
                    </select>
                    </fieldset>
                    </form>
                </div>
                """
        return html1 + html2 + html4

    @expose()
    def get_dialog_edit_division(self,**kw):
        itemid = kw['item_id']
        html1 = """
                <div id="dialog_edit_division_item" title="Edit Division">
                    <form id="dialog_edit_division_item_frm">
                        <fieldset>
                            <label for="">Division Name</label>
                            <input type="text" name="divisionname" id="divisionname" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">List ID</label>
                            <input type="text" value={0} name="listid" id="listid" class="text ui-widget-content ui-corner-all" /><br/>
                        </fieldset>
                    </form>
                </div>
                """.format(itemid)
        return html1

    @expose()
    def savenewdivision(self,**kw):
        #for k,w in kw.iteritems():
            #print k,w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = JistLabourDivisions()
        u.division_name = kw['divisionname']
        u.division_leader = 1 
        u.active = True
        u.useridnew = usernow.user_id
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        u.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(u)
        DBS_JistLabour.flush()

    @expose()
    def get_labour_teams_choice_box(self,**kw):
        allteamslist= DBS_JistLabour.query(JistLabourTeamsList). \
                all()
        html2 = """
                  <select id='edit_labour_teams' name='edit_labour_teams' class="text ui-widget-content ui-corner-all" >
                  <option value="">Select one...</option>
                """
        for m in allteamslist: 
            html2temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.team_name)
            html2 = html2 + html2temp
        html2 = html2 + "</select>"

        html = """
            <fieldset>
            <button class="ui-widget ui-widget-content ui-state-default" id="button_create_new_team">Create New Team</button>
            <label for="edit_teamname">Edit This Team</label>
            {0}
            <button class="ui-widget ui-widget-content ui-state-default" id="button_team_reset">Reset</button>
            </fieldset>

               """.format(html2)

        return html

    @expose()
    def get_edit_labour_current_team(self,**kw):
        if kw['teamid'] == '': return
        team= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id==kw['teamid']).one()
        teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                order_by(desc(JistFleetList.id)). \
                all()
        editfleet_form2 = """ <select id="edit_team_vehicle_id"  class="text ui-widget-content ui-corner-all">
                        <option value="">Select one...</option>
                        """
        for fleet in fleetlist: 
            if fleet.id == team.team_vehicle_id:
                editfleet_temp = """
                              <option value="%s" selected="selected">%s</option>
                          """%(fleet.id, fleet.registration_number)
                editfleet_form2 = editfleet_form2 + editfleet_temp

            else:
                editfleet_temp = """
                              <option value="%s">%s</option>
                          """%(fleet.id, fleet.registration_number)
                editfleet_form2 = editfleet_form2 + editfleet_temp
        htmltemp = """
                    <div class='accord_header'>
                    <h3>{0}<span class='accord_qty'>{1} people</span></h3>
                        <div>
                   """.format(team.team_name,sumteams)
        htmlfaces = """
                       <label>Team ID</label> <input type="text" name="edit_team_id" value="{1}" id="edit_team_id" class="text ui-widget-content ui-corner-all" /><br/>
                       <label>Team Name</label><input type="text" name="edit_team_name" value="{0}" id="edit_team_name" class="text ui-widget-content ui-corner-all" /><br/>
                       <label>Team Description</label><input type="text" name="edit_team_description" value="{2}" id="edit_team_description" class="text ui-widget-content ui-corner-all" /><br/>
                       <label>Team Vehicle</label>{3} </select><br/>
                    """.format(team.team_name,team.id,team.team_description,editfleet_form2)
        for staff_mem in teamliststaff:
            thisuser = DBS_ContractData.query(User).filter(User.user_id==staff_mem.team_staff_member_id).one()
            if thisuser.active_status:
                staffdivision_link = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==thisuser.user_id). \
                        one()
                staffcategory_link = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==thisuser.user_id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==staffcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==staffdivision_link.lab_division_id). \
                        one()
                staffpic = self.get_labour_picture_html('staff',thisuser.user_id,thisuser.user_name,divisionone.division_name,categoryone.category_name)
                htmlfaces =  htmlfaces + staffpic 
        for staff_mem in teamlistlabour:
            thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staff_mem.team_lab_member_id).one()
            if thisuser.active:
                labcategory_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                        filter(JistLabourCategoryLink.user_id==thisuser.id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==labcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==thisuser.division). \
                        one()
                staffpic = self.get_labour_picture_html('labour',thisuser.id,thisuser.first_name+' '+thisuser.last_name,divisionone.division_name,categoryone.category_name)
                htmlfaces =  htmlfaces + staffpic 
        for staff_mem in teamlistsubcon:
            thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staff_mem.team_subcon_member_id).one()
            if thisuser.active:
                subcondivision_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                        filter(JistSubconDivisionLink.user_id==thisuser.id). \
                        one()
                subconcategory_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                        filter(JistSubconCategoryLink.user_id==thisuser.id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==subconcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==subcondivision_link.lab_division_id). \
                        one()
                staffpic = self.get_labour_picture_html('subcon',thisuser.id,thisuser.trading_name,divisionone.division_name,categoryone.category_name)
                htmlfaces =  htmlfaces + staffpic 
        return htmlfaces

    @expose()
    def saveeditlabour_team(self,**kw):
        #for k,w in kw.iteritems():
            #print k, w
        #return
        teamdescription = kw['teamdescription']
        teamfleetid = kw['teamfleetid']
        teamname = kw["teamname"]
        teamid = kw["teamid"]
        thisdata = json.loads(kw['teamdata'])
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisteam = DBS_JistLabour.query(JistLabourTeamsList).filter(JistLabourTeamsList.id==teamid).one()
        thisteam.team_name = teamname
        thisteam.team_description = teamdescription 
        if teamfleetid != '':
            thisteam.team_vehicle_id =  teamfleetid 
        else:
            thisteam.team_vehicle_id = None 
        thisteammembers = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.id==teamid).all()
        for item in thisdata:
            #print item['jistUserid'],item['jistLabourgroup']
            if item['jistLabourgroup'] == 'labour': 
                try:
                    thisteammember = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.team_lab_member_id == item['jistUserid']).one()
                except:
                    newmem = JistLabourTeamsMembers()
                    newmem.team_id = teamid 
                    newmem.team_lab_member_id = item['jistUserid'] 
                    newmem.useridnew = usernow.user_id
                    DBS_JistLabour.add(newmem)
                    DBS_JistLabour.flush()
            elif item['jistLabourgroup'] == 'staff':
                try:
                    thisteammember = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.team_staff_member_id == item['jistUserid']).one()
                except:
                    newmem = JistLabourTeamsMembers()
                    newmem.team_id = teamid 
                    newmem.team_staff_member_id = item['jistUserid'] 
                    newmem.useridnew = usernow.user_id
                    DBS_JistLabour.add(newmem)
                    DBS_JistLabour.flush()
            elif item['jistLabourgroup'] == 'subcon':
                try:
                    thisteammember = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.team_subcon_member_id == item['jistUserid']).one()
                except:
                    newmem = JistLabourTeamsMembers()
                    newmem.team_id = teamid 
                    newmem.team_subcon_member_id = item['jistUserid'] 
                    newmem.useridnew = usernow.user_id
                    DBS_JistLabour.add(newmem)
                    DBS_JistLabour.flush()
            else:
                pass
        return

    @expose()
    def delete_labour_from_team(self,**kw):
        #for k,w in kw.iteritems():
            #print k
        item = json.loads(kw['teamdata'])
        #for item in thisdata:
            #print item['jistUserid'],item['jistLabourgroup']
        if item['jistLabourgroup'] == 'labour': 
            try:
                thisteammember = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.team_lab_member_id == item['jistUserid']).one()
                DBS_JistLabour.delete(thisteammember)
            except:
                pass
        elif item['jistLabourgroup'] == 'staff':
            try:
                thisteammember = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.team_staff_member_id == item['jistUserid']).one()
                DBS_JistLabour.delete(thisteammember)
            except:
                pass
        elif item['jistLabourgroup'] == 'subcon':
            try:
                thisteammember = DBS_JistLabour.query(JistLabourTeamsMembers).filter(JistLabourTeamsMembers.team_subcon_member_id == item['jistUserid']).one()
                DBS_JistLabour.delete(thisteammember)
            except:
                pass
        else:
            pass

        return

    @expose()
    def savenewlabour_team(self,**kw):
        #for k,w in kw.iteritems():
            #print k
        teamname= kw['teamname']
        thisdata = json.loads(kw['teamdata'])
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newteam = JistLabourTeamsList()
        newteam.team_name = teamname
        newteam.useridnew = usernow.user_id
        DBS_JistLabour.add(newteam)
        DBS_JistLabour.flush()
        for item in thisdata:
            #print item['jistUserid'],item['jistLabourgroup']
            if item['jistLabourgroup'] == 'labour': 
                newmem = JistLabourTeamsMembers()
                newmem.team_id = newteam.id 
                newmem.team_lab_member_id = item['jistUserid'] 
                newmem.useridnew = usernow.user_id
                DBS_JistLabour.add(newmem)
                DBS_JistLabour.flush()
            elif item['jistLabourgroup'] == 'staff':
                newmem = JistLabourTeamsMembers()
                newmem.team_id = newteam.id 
                newmem.team_staff_member_id = item['jistUserid'] 
                newmem.useridnew = usernow.user_id
                DBS_JistLabour.add(newmem)
                DBS_JistLabour.flush()
            elif item['jistLabourgroup'] == 'subcon':
                newmem = JistLabourTeamsMembers()
                newmem.team_id = newteam.id 
                newmem.team_subcon_member_id = item['jistUserid'] 
                newmem.useridnew = usernow.user_id
                DBS_JistLabour.add(newmem)
                DBS_JistLabour.flush()
            else:
                pass

        return

    def build_labour_html_table(self,headers,headerwidths,lablist):
        htmltbl = """
                    <table id = "active_labour_tbl">

                   """
        for i,head in enumerate(headers):
            htmltemp1 = """
                    <th width=%s>%s</th>
                        """%(headerwidths[i],head)
            htmltbl = htmltbl + htmltemp1
        for lab in lablist:
            htmltemp1 = """
                    <tr>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    <td>%s</td>
                    </tr>
                        """%(lab['id'],lab['emp_number'],lab['last_name'],
                                lab['first_name'],lab['id_number'],
                                lab['date_started'],lab['active']
                                )

            htmltbl = htmltbl + htmltemp1
        htmltbl = htmltbl + "</table>"
        return htmltbl 

    @expose()
    def search_labour_by_idno(self,**kw):
        phrase = ''
        for k,w in kw.iteritems():
            #print k,w
            phrase = k
        searchphrase = "%"+phrase+"%"
        #filter(JistBuyingOrderItems.description.like(str(searchphrase))). \
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id_number.like(str(searchphrase))). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         'active':k.active,
                         })
        headers =["ID","Empl. Number","Last Name","First Name","ID Number","Date Started","Active"]
        headerwidths=[50,80,200,200,80,80,80]
        htmltbl = self.build_labour_html_table(headers,headerwidths,lablist)
        return htmltbl

    @expose()
    def search_labour_by_first_name(self,**kw):
        phrase = ''
        for k,w in kw.iteritems():
            #print k,w
            phrase = k
        searchphrase = "%"+phrase+"%"
        #filter(JistBuyingOrderItems.description.like(str(searchphrase))). \
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.first_name.like(str(searchphrase))). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         'active':k.active,
                         })
        headers =["ID","Empl. Number","Last Name","First Name","ID Number","Date Started","Active"]
        headerwidths=[50,80,200,200,80,80,80]
        htmltbl = self.build_labour_html_table(headers,headerwidths,lablist)
        return htmltbl

    @expose()
    def search_labour_by_last_name(self,**kw):
        phrase = ''
        for k,w in kw.iteritems():
            #print k,w
            phrase = k
        searchphrase = "%"+phrase+"%"
        #filter(JistBuyingOrderItems.description.like(str(searchphrase))). \
        lblist = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.last_name.like(str(searchphrase))). \
                all()
        lablist = []
        for k in lblist:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            lablist.append({'id':k.id,
                         'emp_number':k.emp_number,
                         'last_name':k.last_name,
                         'first_name':k.first_name,
                         'id_number':k.id_number,
                         'date_started':k.date_started,
                         'rate_per_day':k.rate_per_day,
                         'active':k.active,
                         })
        headers =["ID","Empl. Number","Last Name","First Name","ID Number","Date Started","Active"]
        headerwidths=[50,80,200,200,80,80,80]
        htmltbl = self.build_labour_html_table(headers,headerwidths,lablist)
        return htmltbl

    @expose()
    def get_labour_by_edit_id(self,labid,**kw):
        lab = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id == labid). \
                one()
        activehtmltext = ''
        if lab.active:
            activehtmltext = """
                          <select " id="labour_active" name="labour_active" >
                            <option value="0"">False</option>
                            <option value="1" selected="selected">True</option>
                          </select><br/>


                          """
        else:
            activehtmltext = """
                          <select " id="labour_active" name="labour_active" >
                            <option value="0" selected="selected">False</option>
                            <option value="1">True</option>
                          </select><br/>

                          """
        thisdiv = lab.division
        divisions_all = DBS_JistLabour.query(JistLabourDivisions). \
                        all()
        htmldivision = ''
        html1 ="""<select id="labour_divisions" name="labour_divisions" >"""
        htmldivision = htmldivision + html1
        for i, div in enumerate(divisions_all):
            if i+1 == thisdiv:
                html2 = """<option value="%s" selected="selected">%s</option>"""%(div.id,div.division_name)
            else:
                html2 = """<option value="%s">%s</option>"""%(div.id,div.division_name)
            htmldivision = htmldivision + html2

        html3 ="""</select>"""
        htmldivision = htmldivision + html3


        htmltbl = """
                    <fieldset>
                    <legend>Edit Employee Details</legend>
                    <form id="edit_employee_form">
                        <label for="">Employee Picture</label>
                        <input type="file" name="edit_employee_pic" id="edit_employee_pic" class="text ui-widget-content ui-corner-all" /><br/>
                        <br/>
                        <label for="">Employee Id</label>
                        <input type="text" value="%s" name="edit_employee_id" id="edit_employee_id" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Emp_number</label>
                        <input type="text" value="%s" name="edit_employee_emp_number" id="edit_employee_emp_number" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee First Name</label>
                        <input type="text" value="%s" name="edit_employee_first_name" id="edit_employee_first_name" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Last Name</label>
                        <input type="text" value="%s" name="edit_employee_last_name" id="edit_employee_last_name" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee ID Number</label>
                        <input type="text" value="%s" name="edit_employee_id_number" id="edit_employee_id_number" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Date Started</label>
                        <input type="text" value=%s name="edit_employee_date_started" id="edit_employee_date_started" class="ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Rate Per Day</label>
                        <input type="text" value="%s" name="edit_employee_rate_per_day" id="edit_employee_rate_per_day" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Division</label>
                        %s<br/>
                        <label for="">Employee Bank</label>
                        <input type="text" value="%s" name="edit_employee_bank" id="edit_employee_bank" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Bank Branch Code</label>
                        <input type="text" value="%s" name="edit_employee_branch_code" id="edit_employee_branch_code" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Bank Account Number</label>
                        <input type="text" value="%s" name="edit_employee_account_number" id="edit_employee_account_number" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Address 1</label>
                        <input type="text" value="%s" name="edit_employee_address1" id="edit_employee_address1" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Address 2</label>
                        <input type="text" value="%s" name="edit_employee_address2" id="edit_employee_address2" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Tel Home</label>
                        <input type="text" value="%s" name="edit_employee_tel_number_home" id="edit_employee_tel_number_home" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Next Of Kin Name</label>
                        <input type="text" value="%s" name="edit_employee_next_of_kin_name" id="edit_employee_next_of_kin_name" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Next Of Kin Tel</label>
                        <input type="text" value="%s" name="edit_employee_next_of_kin_tel" id="edit_employee_next_of_kin_tel" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Active</label>
                        %s

                        <button class="ui-widget ui-widget-content ui-state-default" id="button_employee_edit">Edit Employee</button>
                    </form>
                    </fieldset>
                
                    """%(lab.id,lab.emp_number,lab.first_name,lab.last_name,lab.id_number,lab.date_started,lab.rate_per_day,
                            htmldivision,lab.bank,lab.branch_code,lab.account_number,lab.address1,lab.address2,lab.tel_number_home,
                            lab.next_of_kin_name,lab.next_of_kin_tel,activehtmltext
                            )

        return htmltbl 

    @expose()
    def get_new_labour_form(self,**kw):
        activehtmltext = """
                      <select id="labour_active_new" name="labour_active_new" >
                        <option value="0"">False</option>
                        <option value="1" selected="selected">True</option>
                      </select><br/>
                      """

        divisions_all = DBS_JistLabour.query(JistLabourDivisions). \
                        all()
        htmldivision = ''
        html1 ="""<select id="labour_divisions_new" name="labour_divisions_new" >"""
        htmldivision = htmldivision + html1
        for i, div in enumerate(divisions_all):
            html2 = """<option value="%s">%s</option>"""%(div.id,div.division_name)
            htmldivision = htmldivision + html2

        html3 ="""</select>"""
        htmldivision = htmldivision + html3
        htmltbl = """
                    <form id="new_employee_form">
                    <fieldset>
                    <legend>New Employee </legend>
                        <label for="">Employee First Name</label>
                        <input type="text" name="new_employee_first_name" id="new_employee_first_name" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Last Name</label>
                        <input type="text" name="new_employee_last_name" id="new_employee_last_name" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee ID Number</label>
                        <input type="text" name="new_employee_id_number" id="new_employee_id_number" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Date Started</label>
                        <input type="text" name="new_employee_date_started" id="new_employee_date_started" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Rate Per Day</label>
                        <input type="text" name="new_employee_rate_per_day" id="new_employee_rate_per_day" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Division</label>
                        %s<br/>
                        <label for="">Employee Bank</label>
                        <input type="text" name="new_employee_bank" id="new_employee_bank" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Bank Branch Code</label>
                        <input type="text" name="new_employee_branch_code" id="new_employee_branch_code" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Bank Account Number</label>
                        <input type="text" name="new_employee_account_number" id="new_employee_account_number" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Address 1</label>
                        <input type="text" name="new_employee_address1" id="new_employee_address1" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Address 2</label>
                        <input type="text" name="new_employee_address2" id="new_employee_address2" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Tel Home</label>
                        <input type="text" name="new_employee_tel_number_home" id="new_employee_tel_number_home" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Next Of Kin Name</label>
                        <input type="text" name="new_employee_next_of_kin_name" id="new_employee_next_of_kin_name" class="text ui-widget-content ui-corner-all" /><br/>
                        <label for="">Employee Next Of Kin Tel</label>
                        <input type="text"  id="new_employee_next_of_kin_tel" name="new_employee_next_of_kin_tel" class="text ui-widget-content ui-corner-all" /><br/>

                        <button class="ui-widget ui-widget-content ui-state-default" id="button_save_employee_new">New Employee</button>
                    </fieldset>
                    </form>
                    """%htmldivision
        return htmltbl 

    @expose()
    def saveeditlabour(self,**kw):
        #for k,w in kw.iteritems():
            #print k,w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        editlabour = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==kw['edit_employee_id']). \
                one()
        #for k, w in enumerate(kw):
        #    print k, w, kw[w]
        editlabour.last_name = kw['edit_employee_last_name']
        editlabour.first_name = kw['edit_employee_first_name']
        editlabour.id_number = kw['edit_employee_id_number']
        editlabour.date_started = kw['edit_employee_date_started']
        editlabour.rate_per_day = kw['edit_employee_rate_per_day']
        editlabour.division = kw['labour_divisions']
        editlabour.bank = kw['edit_employee_bank']
        editlabour.bank_code = kw['edit_employee_branch_code']
        editlabour.account_number = kw['edit_employee_account_number']
        editlabour.address1 = kw['edit_employee_address1']
        editlabour.address2 = kw['edit_employee_address2']
        editlabour.tel_number_home = kw['edit_employee_tel_number_home']
        editlabour.next_of_kin_name = kw['edit_employee_next_of_kin_name']
        editlabour.next_of_kin_tel = kw['edit_employee_next_of_kin_tel']
        editlabour.active=kw['labour_active']

    @expose()
    def savenewlabour(self,*arg,**kw):
        #for k,w in kw.iteritems():
            #print k,w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        u = JistLabourList()
        u.last_name = kw['new_employee_last_name']
        u.first_name = kw['new_employee_first_name']
        u.id_number = kw['new_employee_id_number']
        u.date_started = kw['new_employee_date_started']
        u.rate_per_day = kw['new_employee_rate_per_day']
        u.division = kw['labour_divisions_new']
        u.bank = kw['new_employee_bank']
        u.bank_code = kw['new_employee_branch_code']
        u.account_number = kw['new_employee_account_number']
        u.address1 = kw['new_employee_address1']
        u.address2 = kw['new_employee_address2']
        u.tel_number_home = kw['new_employee_tel_number_home']
        u.next_of_kin_name = kw['new_employee_next_of_kin_name']
        u.next_of_kin_tel = kw['new_employee_next_of_kin_tel']
        u.active = True
        u.useridnew = usernow.user_id
        u.useridedited = usernow.user_id
        u.dateedited = datetime.date(datetime.now()) 
        u.dateadded = datetime.date(datetime.now()) 
        DBS_JistLabour.add(u)
        DBS_JistLabour.flush()
        emp = "EMP"+str(int(u.id)+999)
        editlabour = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==u.id). \
                one()
        editlabour.emp_number =emp

    @expose()
    def get_dialog_add_labourpic(self,**kw):
        html1 = """
                <div id="dialog_labour_pic" title="Add Labour Picture">
                    <form id="dialog_labour_pic_frm">
                        <fieldset>
                            <label for="">Labour ID</label>
                            <input type="text" value='{0}' name="userid" id="userid" class="text ui-widget-content ui-corner-all" /><br/>
                        <div id="jquery-fine-uploader" style="display: block">
                        </div>
                        <br/>
                        <button id="triggerUpload" style="display: block" class="ui-state-default ui-corner-all">
                             Upload now
                        </button>

               """.format(kw['userid'])
        html2 = """
                """
        
        html4 = """
                    </fieldset>
                    </form>
                <canvas id='canvas_labpic' width='200px' height='200px'></canvas>
                </div>
                """
        return html1 + html2 + html4

    @expose()
    def save_dialog_labourpic(self,*arg,**kw):
        #for k,w in kw.iteritems():
            #print k,w
        #return
        userid = kw['userid']
        uploader = qqFileUploader(userid,kw,labour_picdir, [".png"], 2147483648)
        uploadname = uploader.handleLabourPicUpload()
        target = os.path.join(labour_picdir, uploadname)
        self.getthumbnail(target,target)
        return json.dumps({"success": True})

    def convert_base64(self,imagepth):
        f = open(imagepth)
        data = f.read()
        f.close()

        string = base64.b64encode(data)
        #convert = base64.b64decode(string)
        return string

    @expose()
    def get_dialog_edit_division(self,**kw):
        itemid = kw['item_id']
        html1 = """
                <div id="dialog_edit_division_item" title="Edit Division">
                    <form id="dialog_edit_division_item_frm">
                        <fieldset>
                            <label for="">Division Name</label>
                            <input type="text" name="divisionname" id="divisionname" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">List ID</label>
                            <input type="text" value={0} name="listid" id="listid" class="text ui-widget-content ui-corner-all" /><br/>
                        </fieldset>
                    </form>
                </div>
                """.format(itemid)
        return html1

    @expose()
    def get_labour_history_by_id(self,labid,**kw):
        init_value = 1
        paymentruns = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                join(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.empl_id==labid). \
                filter(JistLabourPaymentRunsList.active==True). \
                    order_by(desc(JistLabourPaymentRunsList.payment_date)). \
                all()
        labourdata = []
        for x in paymentruns:
            labdata = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                    filter(JistLabourPaymentRunsData.empl_id==labid). \
                    filter(JistLabourPaymentRunsData.paylist_id==x.id). \
                    order_by(desc(JistLabourPaymentRunsData.id)). \
                    all()
            labourdata.append([labdata,x.id,x.payment_date,x.start_date,x.end_date])
        emps = DBS_JistLabour.query(JistLabourList). \
                all()
        p1total = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.empl_id==labid). \
                value(func.sum(JistLabourPaymentRunsData.amount_gross_total))
        divisiondata = DBS_JistLabour.query(JistLabourDivisions). \
                filter(JistLabourDivisions.id==init_value). \
                one()
        thislabourer = DBS_JistLabour.query(JistLabourList). \
                filter(JistLabourList.id==labid). \
                one()

        #print labourdata
        for lab in labourdata:
            #print lab[0].paylist_id
            for la in lab[0]:
                print la.paylist_id
                #print la['paylist_id']
        #return
        totalexcl = 0.00
        if p1total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(p1total,format='#,##0.00;-#0.00',locale='en')

        employees = []
        for m in emps:
            employees.append([m.id,m.last_name+' ' +m.first_name])
            #print m.id,m.last_name

        headers =["ID","Payment Date","Rate Per Day","NT","NT Amount","OT","OT Amount"]
        headerwidths=[50,80,200,200,80,80,80]
        htmltbl = """
                    <table id = "active_labour_history_tbl">

                   """
        for i,head in enumerate(headers):
            htmltemp1 = """
                    <th width=%s>%s</th>
                        """%(headerwidths[i],head)
            htmltbl = htmltbl + htmltemp1
        for lablst in labourdata:
            for lab in lablst[0]:
                htmltemp1 = """
                        <tr>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        <td>%s</td>
                        </tr>
                            """%(lab.id,lablst[2],lab.rate_per_day,lab.hours_normal,lab.amount_normal_time,lab.hours_over_time,lab.amount_over_time)


                htmltbl = htmltbl + htmltemp1
        htmltbl = htmltbl + "</table>"
        return htmltbl 

    def build_labour_html_table_new(self,dictlist,headers,headerwidths,outputlist,tdclassnames,tblname):
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

    def getthumbnail(self, inpath, outpath):
        retcode = subprocess.call(['convert',inpath,'-resize','50!x50!',outpath])

    @expose()
    def get_labour_teams_picture_by_division_html(self,**kw):
        allteamslist= DBS_JistLabour.query(JistLabourTeamsList). \
                all()
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        #teamstaffids = [k.team_staff_member_id for k in teamliststaff] 
        #teamlabourids = [k.team_lab_member_id for k in teamlistlabour] 
        #teamsubconids = [k.team_subcon_member_id for k in teamlistsubcon] 
        html2 = ''
        htmltemp = ''
        header = """<h4 class="modal-content">All Labour Teams<span class='spanright'>  </span></h4>"""
        htmlstaff1 = header + """<div id="labour_teams_accordion">"""
        html2 = ''
        htmltemp = ''
        for division in divisionlistall:
            for team in allteamslist:
                userimg, sumteams, divisionid = self.get_labour_leader_team_pic_html(team)
                if divisionid == division.id:
                    htmltemp = """
                                <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                        <li class="ui-widget-content ui-corner-tr">
                                        <h6 class="ui-widget-header">{0}</h6>
                                        {2}
                                        <h6 class="ui-widget-header">{3}</h6>
                                        </li>
                                </ul>
                               """.format(team.team_name,sumteams,userimg,division.division_name)
                    html2 =  html2 + htmltemp  
        return html2

    @expose()
    def get_labour_teams_picture_by_division_html_old(self,**kw):
        allteamslist= DBS_JistLabour.query(JistLabourTeamsList). \
                all()
        divisionlistall = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.active == True).all()
        #teamstaffids = [k.team_staff_member_id for k in teamliststaff] 
        #teamlabourids = [k.team_lab_member_id for k in teamlistlabour] 
        #teamsubconids = [k.team_subcon_member_id for k in teamlistsubcon] 
        html2 = ''
        htmltemp = ''
        header = """<h4 class="modal-content">All Labour Teams<span class='spanright'>  </span></h4>"""
        htmlstaff1 = header + """<div id="labour_teams_accordion">"""
        html2 = ''
        htmltemp = ''
        for division in divisionlistall:
            for team in allteamslist:
                userimg, sumteams, divisionid = self.get_labour_leader_team_pic_html(team)
                if divisionid == division.id:
                    htmltemp = """
                                <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                        <li class="ui-widget-content ui-corner-tr">
                                        <h6 class="ui-widget-header">{0}</h6>
                                        {2}
                                        <h6 class="ui-widget-header">{3}</h6>
                                        </li>
                                </ul>
                               """.format(team.team_name,sumteams,userimg,division.division_name)
                    html2 =  html2 + htmltemp  
        return html2

    def get_labour_leader_team_pic_html(self,team,**kw):
        teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
        teamliststafffirst= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id). \
                order_by(asc(JistLabourTeamsMembers.id)).first()
        teamlistlabourfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id). \
                order_by(asc(JistLabourTeamsMembers.id)).first()
        teamlistsubconfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id). \
                order_by(asc(JistLabourTeamsMembers.id)).first()
        userimg = None
        notuserfound = True
        thisuserdivisionid = None
        while notuserfound:
            if teamliststafffirst and notuserfound:
                #print "Staff First {0}".format(teamliststafffirst.team_staff_member_id)
                pic_path = os.path.join(staff_picdir, "{0}.png".format(teamliststafffirst.team_staff_member_id))
                staff_division = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==teamliststafffirst.team_staff_member_id). \
                        one()
                thisuserdivisionid = staff_division.lab_division_id
                if not os.path.exists(pic_path):  
                    userimg = """
                                <img myid="{1}" class="div_leader_accord_team_pic"  id="leader_staffpic" src="/images/staffpics/1.png"></img>
                              """.format(teamliststafffirst.team_staff_member_id,team.id)
                else:
                    userimg = """
                                <img myid="{1}" class="div_leader_accord_team_pic"  id="leader_staffpic" src="/images/staffpics/{0}.png"></img>
                              """.format(teamliststafffirst.team_staff_member_id,team.id)
                notuserfound = False
            elif teamlistlabourfirst and notuserfound:
                #print "Labour First {0}".format(teamlistlabourfirst.team_lab_member_id)
                this_user = DBS_JistLabour.query(JistLabourList). \
                        filter(JistLabourList.id==teamlistlabourfirst.team_lab_member_id). \
                        one()
                thisuserdivisionid = this_user.division
                pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(teamlistlabourfirst.team_lab_member_id))
                if not os.path.exists(pic_path):  
                    userimg = """
                                <img myid="{1}" class="div_leader_accord_team_pic"  id="leader_labourpic" src="/images/labourpics/user_lab_none.png"></img>
                              """.format(teamlistlabourfirst.team_lab_member_id,team.id)
                else:
                    userimg = """
                                <img myid="{1}" class="div_leader_accord_team_pic"  id="leader_labourpic" src="/images/labourpics/labour_{0}.png"></img>
                              """.format(teamlistlabourfirst.team_lab_member_id,team.id)
                notuserfound = False
            elif teamlistsubconfirst and notuserfound:
                #print "Subcon First {0}".format(teamlistsubconfirst.team_subcon_member_id)
                subcon_division = DBS_JistLabour.query(JistSubconDivisionLink). \
                        filter(JistSubconDivisionLink.user_id==teamlistsubconfirst.team_subcon_member_id). \
                        one()
                thisuserdivisionid = subcon_division.lab_division_id
                pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(teamlistsubconfirst.team_subcon_member_id))
                if not os.path.exists(pic_path):  
                    userimg = """
                                <img myid="{1}" class="div_leader_accord_team_pic"  id="leader_subconpic" src="/images/subconpics/user_subcon_none.png"></img>
                              """.format(teamlistsubconfirst.team_subcon_member_id,team.id)
                else:
                    userimg = """
                                <img myid="{1}" class="div_leader_accord_team_pic"  id="leader_subconpic" src="/images/subconpics/subcon_{0}.png"></img>
                              """.format(teamlistsubconfirst.team_subcon_member_id,team.id)
                notuserfound = False
            else:
                notuserfound = False
        return userimg, sumteams, thisuserdivisionid

    def get_labour_leader_team_pic_path(self,teamid,**kw):
        teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == teamid).all()
        teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == teamid).all()
        teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == teamid).all()
        sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
        teamliststafffirst= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == teamid). \
                order_by(asc(JistLabourTeamsMembers.id)).first()
        teamlistlabourfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == teamid). \
                order_by(asc(JistLabourTeamsMembers.id)).first()
        teamlistsubconfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == teamid). \
                order_by(asc(JistLabourTeamsMembers.id)).first()
        userimg = None
        notuserfound = True
        thisuserdivisionid = None
        while notuserfound:
            if teamliststafffirst and notuserfound:
                #print "Staff First {0}".format(teamliststafffirst.team_staff_member_id)
                pic_path = os.path.join(staff_picdir, "{0}.png".format(teamliststafffirst.team_staff_member_id))
                staff_division = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==teamliststafffirst.team_staff_member_id). \
                        one()
                thisuserdivisionid = staff_division.lab_division_id
                if not os.path.exists(pic_path):  
                    userimg = """images/staffpics/1.png""".format(teamliststafffirst.team_staff_member_id,teamid)
                else:
                    userimg = """images/staffpics/{0}.png""".format(teamliststafffirst.team_staff_member_id,teamid)
                notuserfound = False
            elif teamlistlabourfirst and notuserfound:
                #print "Labour First {0}".format(teamlistlabourfirst.team_lab_member_id)
                this_user = DBS_JistLabour.query(JistLabourList). \
                        filter(JistLabourList.id==teamlistlabourfirst.team_lab_member_id). \
                        one()
                thisuserdivisionid = this_user.division
                pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(teamlistlabourfirst.team_lab_member_id))
                if not os.path.exists(pic_path):  
                    userimg = """images/labourpics/user_lab_none.png""".format(teamlistlabourfirst.team_lab_member_id,teamid)
                else:
                    userimg = """images/labourpics/labour_{0}.png""".format(teamlistlabourfirst.team_lab_member_id,teamid)
                notuserfound = False
            elif teamlistsubconfirst and notuserfound:
                #print "Subcon First {0}".format(teamlistsubconfirst.team_subcon_member_id)
                subcon_division = DBS_JistLabour.query(JistSubconDivisionLink). \
                        filter(JistSubconDivisionLink.user_id==teamlistsubconfirst.team_subcon_member_id). \
                        one()
                thisuserdivisionid = subcon_division.lab_division_id
                pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(teamlistsubconfirst.team_subcon_member_id))
                if not os.path.exists(pic_path):  
                    userimg = """images/subconpics/user_subcon_none.png""".format(teamlistsubconfirst.team_subcon_member_id,teamid)
                else:
                    userimg = """images/subconpics/subcon_{0}.png""".format(teamlistsubconfirst.team_subcon_member_id,teamid)
                notuserfound = False
            else:
                notuserfound = False
        return userimg

    @expose()
    def get_labour_categories_people_for_teams_html(self,**kw):
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        categorieslist = DBS_JistLabour.query(JistLabourCategories). \
                filter(JistLabourCategories.active==True). \
                all()
        #labdivision_all = DBS_JistLabour.query(JistLabourList). \
                #filter(JistLabourList.active==True). \
                #all()
        header = """<h4 class="modal-content">Available Labour<span class='spanright'>  </span></h4>"""
        #htmlstaff1 = header + """<div id="labour_categories_people_accordion">"""
        html2 = ''
        htmltemp = ''
        for category in categorieslist:
            staff_all_categories = DBS_JistLabour.query(JistStaffCategoryLink). \
                    filter(JistStaffCategoryLink.lab_category_id==category.id). \
                    all()
            labour_all_categories = DBS_JistLabour.query(JistLabourCategoryLink). \
                    filter(JistLabourCategoryLink.lab_category_id==category.id). \
                    all()
            subcon_all_categories = DBS_JistLabour.query(JistSubconCategoryLink). \
                    filter(JistSubconCategoryLink.lab_category_id==category.id). \
                    all()
            teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                    filter(JistLabourTeamsMembers.team_staff_member_id != None).all()
            teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                    filter(JistLabourTeamsMembers.team_lab_member_id != None).all()
            teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                    filter(JistLabourTeamsMembers.team_subcon_member_id != None).all()
            #for k in teamlistlabour:
                #print k
            teamstaff = [k.team_staff_member_id for k in teamliststaff] 
            teamlabour = [k.team_lab_member_id for k in teamlistlabour] 
            teamsubcon = [k.team_subcon_member_id for k in teamlistsubcon] 
            if len(staff_all_categories) > 0:
                category_sum = len(staff_all_categories)
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category.id). \
                        one()
                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0} [Staff]<span class='accord_qty'>{1} people</span></h3>
                                <div>
                           """.format(
                                  categoryone.category_name ,
                                  category_sum 
                                   )
                htmlfaces = ''
                for staff_cat in staff_all_categories:
                    thisuser = DBS_ContractData.query(User).filter(User.user_id==staff_cat.user_id).one()
                    if thisuser.active_status:
                        if thisuser.user_id in teamstaff:  continue
                        pic_path = os.path.join(staff_picdir, "{0}.png".format(thisuser.user_id))
                        if not os.path.exists(pic_path):  
                            staffpic = """
                                        <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_staff_mem_pic"  id="staffpic" data-jist-userid="{3}" data-jist-labourgroup="staff" title="{0}" src="/images/staffpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.user_name,"user_lab_none",categoryone.category_name,thisuser.user_id)
                        else:
                            staffpic = """ 
                                        <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_staff_mem_pic"  id="staffpic" data-jist-userid="{1}" data-jist-labourgroup="staff" title="{0}" src="/images/staffpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.user_name,thisuser.user_id,categoryone.category_name)
                        htmlfaces =  htmlfaces + staffpic 
                htmllast = """

                                </div>
                            </div>
                       """
                html2 =  html2  + htmlfaces 
            if len(labour_all_categories) > 0:
                category_sum = len(labour_all_categories)
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category.id). \
                        one()
                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0} [Labour]<span class='accord_qty'>{1} people</span></h3>
                                <div>
                           """.format(
                                  categoryone.category_name ,
                                  category_sum 
                                   )
                htmlfaces = ''
                for staff_cat in labour_all_categories:
                    thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staff_cat.user_id).one()
                    division_this = DBS_JistLabour.query(JistLabourDivisions). \
                            filter(JistLabourDivisions.id==thisuser.division). \
                            one()
                    if thisuser.active:
                        if thisuser.id in teamlabour: continue 
                        pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(thisuser.id))
                        if not os.path.exists(pic_path):  
                            staffpic = """
                                        
                                        <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix ui-draggable">
                                                <li  class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_lab_mem_pic"  id="labpic" data-jist-userid="{6}"  data-jist-labourgroup="labour" title="{0}" src="/images/labourpics/{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                <h6 class="ui-widget-header">{3}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.first_name+' '+thisuser.last_name,
                                        "user_lab_none",
                                        division_this.division_name,
                                        categoryone.category_name,
                                        categoryone.category_name,
                                        division_this.id,
                                        thisuser.id
                                        )
                        else:
                            staffpic = """ 
                                        <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix ui-draggable">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_lab_mem_pic"  id="labpic" data-jist-userid="{1}" data-jist-labourgroup="labour" title="{0}" src="/images/labourpics/labour_{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                <h6 class="ui-widget-header">{3}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.first_name+' '+thisuser.last_name,
                                        thisuser.id,
                                        division_this.division_name,
                                        categoryone.category_name,
                                        division_this.id
                                        )
                        htmlfaces =  htmlfaces + staffpic 
                htmllast = """

                                </div>
                            </div>
                       """


                html2 = html2 + htmlfaces 
            if len(subcon_all_categories) > 0:
                category_sum = len(subcon_all_categories)
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==category.id). \
                        one()
                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0} [Subcon]<span class='accord_qty'>{1} Team</span></h3>
                                <div>
                           """.format(
                                  categoryone.category_name ,
                                  category_sum 
                                   )
                htmlfaces = ''
                for staff_cat in subcon_all_categories:
                    thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staff_cat.user_id).one()
                    division_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                            filter(JistSubconDivisionLink.user_id==thisuser.id). \
                            one()
                    division_this = DBS_JistLabour.query(JistLabourDivisions). \
                            filter(JistLabourDivisions.id==division_link.lab_division_id). \
                            one()
                    if thisuser.active:
                        if thisuser.id in teamsubcon: continue 
                        pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(thisuser.id))
                        if not os.path.exists(pic_path):  
                            staffpic = """
                                        <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_subcon_mem_pic"  id="subconpic" data-jist-userid="{1}" data-jist-labourgroup="subcon" title="{0}" src="/images/subconpics/{2}.png"></img>
                                                <h6 class="ui-widget-header">{3}</h6>
                                                <h6 class="ui-widget-header">{4}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.trading_name,thisuser.id,"user_subcon_none",division_this.division_name,categoryone.category_name)
                        else:
                            staffpic = """ 
                                        <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                                <li class="ui-widget-content ui-corner-tr">
                                                <h6 class="ui-widget-header">{0}</h6>
                                                <img  class="div_subcon_mem_pic"  id="subconpic" data-jist-userid="{1}" data-jist-labourgroup="subcon" title="{0}" src="/images/subconpics/subcon_{1}.png"></img>
                                                <h6 class="ui-widget-header">{2}</h6>
                                                <h6 class="ui-widget-header">{3}</h6>
                                                </li>
                                        </ul>
                            """.format(thisuser.trading_name,thisuser.id,division_this.division_name,categoryone.category_name)
                        htmlfaces =  htmlfaces + staffpic 
                htmllast = """

                                </div>
                            </div>
                       """


                html2 = html2 + htmlfaces + htmllast 
        htmllastdiv = "</div>"
        htmlitems = ''
        htmldetails = ''
        return  header + html2 + htmllastdiv 

    @expose()
    def savenewlabour_team(self,**kw):
        teamname= kw['teamname']
        thisdata = json.loads(kw['teamdata'])
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newteam = JistLabourTeamsList()
        newteam.team_name = teamname
        newteam.useridnew = usernow.user_id
        DBS_JistLabour.add(newteam)
        DBS_JistLabour.flush()
        for item in thisdata:
            #print item['jistUserid'],item['jistLabourgroup']
            if item['jistLabourgroup'] == 'labour': 
                newmem = JistLabourTeamsMembers()
                newmem.team_id = newteam.id 
                newmem.team_lab_member_id = item['jistUserid'] 
                newmem.useridnew = usernow.user_id
                DBS_JistLabour.add(newmem)
                DBS_JistLabour.flush()
            elif item['jistLabourgroup'] == 'staff':
                newmem = JistLabourTeamsMembers()
                newmem.team_id = newteam.id 
                newmem.team_staff_member_id = item['jistUserid'] 
                newmem.useridnew = usernow.user_id
                DBS_JistLabour.add(newmem)
                DBS_JistLabour.flush()
            elif item['jistLabourgroup'] == 'subcon':
                newmem = JistLabourTeamsMembers()
                newmem.team_id = newteam.id 
                newmem.team_subcon_member_id = item['jistUserid'] 
                newmem.useridnew = usernow.user_id
                DBS_JistLabour.add(newmem)
                DBS_JistLabour.flush()
            else:
                pass

        return

    @expose()
    def get_labour_teams_accordion_html(self,**kw):
        allteamslist= DBS_JistLabour.query(JistLabourTeamsList). \
                all()
        #teamstaffids = [k.team_staff_member_id for k in teamliststaff] 
        #teamlabourids = [k.team_lab_member_id for k in teamlistlabour] 
        #teamsubconids = [k.team_subcon_member_id for k in teamlistsubcon] 

        html2 = ''
        htmltemp = ''
        header = """<h4 class="modal-content">All Labour Teams<span class='spanright'>  </span></h4>"""
        htmlstaff1 = header + """<div id="labour_teams_accordion">"""
        html2 = ''
        htmltemp = ''
        if len(allteamslist) > 0:
            for team in allteamslist:
                teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id).all()
                teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id).all()
                teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id).all()
                sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
                teamliststafffirst= DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id). \
                        order_by(asc(JistLabourTeamsMembers.id)).first()
                teamlistlabourfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id). \
                        order_by(asc(JistLabourTeamsMembers.id)).first()
                teamlistsubconfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id). \
                        order_by(asc(JistLabourTeamsMembers.id)).first()
                userimg = None
                notuserfound = True
                while notuserfound:
                    if teamliststafffirst and notuserfound:
                        #print "Staff First {0}".format(teamliststafffirst.team_staff_member_id)
                        pic_path = os.path.join(staff_picdir, "{0}.png".format(teamliststafffirst.team_staff_member_id))
                        if not os.path.exists(pic_path):  
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_staffpic" src="/images/staffpics/1.png"></img>
                                      """.format(teamliststafffirst.team_staff_member_id)

                        else:
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_staffpic" src="/images/staffpics/{0}.png"></img>
                                      """.format(teamliststafffirst.team_staff_member_id)
                        notuserfound = False
                    elif teamlistlabourfirst and notuserfound:
                        #print "Labour First {0}".format(teamlistlabourfirst.team_lab_member_id)
                        pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(teamlistlabourfirst.team_lab_member_id))
                        if not os.path.exists(pic_path):  
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_labourpic" src="/images/labourpics/user_lab_none.png"></img>
                                      """.format(teamlistlabourfirst.team_lab_member_id)

                        else:
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_labourpic" src="/images/labourpics/labour_{0}.png"></img>
                                      """.format(teamlistlabourfirst.team_lab_member_id)
                        notuserfound = False
                    elif teamlistsubconfirst and notuserfound:
                        #print "Subcon First {0}".format(teamlistsubconfirst.team_subcon_member_id)
                        pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(teamlistsubconfirst.team_subcon_member_id))
                        if not os.path.exists(pic_path):  
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_subconpic" src="/images/subconpics/user_subcon_none.png"></img>
                                      """.format(teamlistsubconfirst.team_subcon_member_id)

                        else:
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_subconpic" src="/images/subconpics/subcon_{0}.png"></img>
                                      """.format(teamlistsubconfirst.team_subcon_member_id)
                        notuserfound = False
                    else:
                        notuserfound = False

                htmltemp = """
                            <div class='accord_header'>
                            <h3>{0}<span class='accord_qty'>{1} people{2}</span></h3>
                                <div>
                           """.format(team.team_name,sumteams,userimg)
                htmlfaces = ''
                for staff_mem in teamliststaff:
                    if staff_mem.team_staff_member_id == 0: continue
                    thisuser = DBS_ContractData.query(User).filter(User.user_id==staff_mem.team_staff_member_id).one()
                    if thisuser.active_status:
                        staffdivision_link = DBS_JistLabour.query(JistStaffDivisionLink). \
                                filter(JistStaffDivisionLink.user_id==thisuser.user_id). \
                                one()
                        staffcategory_link = DBS_JistLabour.query(JistStaffCategoryLink). \
                                filter(JistStaffCategoryLink.user_id==thisuser.user_id). \
                                one()
                        categoryone = DBS_JistLabour.query(JistLabourCategories). \
                                filter(JistLabourCategories.id==staffcategory_link.lab_category_id). \
                                one()
                        divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                                filter(JistLabourDivisions.id==staffdivision_link.lab_division_id). \
                                one()
                        staffpic = self.get_labour_picture_html('staff',thisuser.user_id,thisuser.user_name,divisionone.division_name,categoryone.category_name)
                        htmlfaces =  htmlfaces + staffpic 
                for staff_mem in teamlistlabour:
                    if staff_mem.team_lab_member_id == 0: continue
                    thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staff_mem.team_lab_member_id).one()
                    if thisuser.active:
                        labcategory_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                                filter(JistLabourCategoryLink.user_id==thisuser.id). \
                                one()
                        categoryone = DBS_JistLabour.query(JistLabourCategories). \
                                filter(JistLabourCategories.id==labcategory_link.lab_category_id). \
                                one()
                        divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                                filter(JistLabourDivisions.id==thisuser.division). \
                                one()
                        staffpic = self.get_labour_picture_html('labour',thisuser.id,thisuser.first_name+' '+thisuser.last_name,divisionone.division_name,categoryone.category_name)
                        htmlfaces =  htmlfaces + staffpic 
                for staff_mem in teamlistsubcon:
                    thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staff_mem.team_subcon_member_id).one()
                    if staff_mem.team_subcon_member_id == 0: continue
                    if thisuser.active:
                        subcondivision_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                                filter(JistSubconDivisionLink.user_id==thisuser.id). \
                                one()
                        subconcategory_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                                filter(JistSubconCategoryLink.user_id==thisuser.id). \
                                one()
                        categoryone = DBS_JistLabour.query(JistLabourCategories). \
                                filter(JistLabourCategories.id==subconcategory_link.lab_category_id). \
                                one()
                        divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                                filter(JistLabourDivisions.id==subcondivision_link.lab_division_id). \
                                one()
                        staffpic = self.get_labour_picture_html('subcon',thisuser.id,thisuser.trading_name,divisionone.division_name,categoryone.category_name)
                        htmlfaces =  htmlfaces + staffpic 

                htmllast = """
                                </div>
                            </div>
                       """

                html2 =  html2 + htmltemp + htmlfaces + htmllast 
        htmllastdiv = "</div>"
        return htmlstaff1 + html2 + htmllastdiv

    def get_labour_picture_html(self,labgroup,userid,username,division_name,category_name):
        if labgroup == 'staff':
            pic_path = os.path.join(staff_picdir, "{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                            <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                    <li class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    <img  class="div_staff_pic"  id="staffpic" data-jist-userid="{1}" data-jist-labourgroup="staff" title="{0}" src="/images/staffpics/{1}.png"></img>
                                    <h6 class="ui-widget-header">{2}</h6>
                                    <h6 class="ui-widget-header">{2}</h6>
                                    </li>
                            </ul>
                """.format(username,userid,"1",category_name,division_name)
            else:
                staffpic = """ 
                            <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                    <li class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    <img  class="div_staff_pic"  id="staffpic" data-jist-userid="{1}" data-jist-labourgroup="staff" title="{0}" src="/images/staffpics/{1}.png"></img>
                                    <h6 class="ui-widget-header">{2}</h6>
                                    <h6 class="ui-widget-header">{3}</h6>
                                    </li>
                            </ul>
                """.format(username,userid,category_name,division_name)
        elif labgroup == 'labour':
            pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                            <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix ui-draggable">
                                    <li  class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    <img class="div_lab_pic"  id="labpic" data-jist-userid="{1}" data-jist-labourgroup="labour" title="{0}" src="/images/labourpics/{2}.png"></img>
                                    <h6 class="ui-widget-header">{4}</h6>
                                    <h6 class="ui-widget-header">{3}</h6>
                                    </li>
                            </ul>
                """.format(username,userid,"user_lab_none",category_name,division_name)
            else:
                staffpic = """ 
                            <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix ui-draggable">
                                    <li class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    <img  class="div_lab_pic"  id="labpic" data-jist-userid="{1}" data-jist-labourgroup="labour" title="{0}" src="/images/labourpics/labour_{1}.png"></img>
                                    <h6 class="ui-widget-header">{2}</h6>
                                    <h6 class="ui-widget-header">{3}</h6>
                                    </li>
                            </ul>
                """.format(username,userid,category_name,division_name)

        elif labgroup == 'subcon':
            pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                            <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                    <li class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    <img class="div_subcon_pic"  id="subconpic" data-jist-userid="{1}" data-jist-labourgroup="subcon" title="{0}" src="/images/subconpics/{2}.png"></img>
                                    <h6 class="ui-widget-header">{3}</h6>
                                    <h6 class="ui-widget-header">{4}</h6>
                                    </li>
                            </ul>
                """.format(username,userid,"user_subcon_none",division_name,category_name)
            else:
                staffpic = """ 
                            <ul id="gallery_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                    <li class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    <img  class="div_subcon_pic"  id="subconpic" data-jist-userid="{1}" data-jist-labourgroup="subcon" title="{0}" src="/images/subconpics/subcon_{1}.png"></img>
                                    <h6 class="ui-widget-header">{2}</h6>
                                    <h6 class="ui-widget-header">{3}</h6>
                                    </li>
                            </ul>
                """.format(username,userid,division_name,category_name)
        return staffpic

    def get_labour_picture_png(self,labgroup,userid,username,division_name,category_name):
        if labgroup == 'staff':
            pic_path = os.path.join(staff_picdir, "{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                                    <img  class="div_staff_pic"  id="staffpic" data-jist-userid="{1}" data-jist-labourgroup="staff" title="{0}" src="/images/staffpics/{1}.png"></img>
                """.format(username,userid,"1",category_name,division_name)
            else:
                staffpic = """ 
                                    <img  class="div_staff_pic"  id="staffpic" data-jist-userid="{1}" data-jist-labourgroup="staff" title="{0}" src="/images/staffpics/{1}.png"></img>
                """.format(username,userid,category_name,division_name)
        elif labgroup == 'labour':
            pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                                    <img class="div_lab_pic"  id="labpic" data-jist-userid="{1}" data-jist-labourgroup="labour" title="{0}" src="/images/labourpics/{2}.png"></img>
                """.format(username,userid,"user_lab_none",category_name,division_name)
            else:
                staffpic = """ 
                                    <img  class="div_lab_pic"  id="labpic" data-jist-userid="{1}" data-jist-labourgroup="labour" title="{0}" src="/images/labourpics/labour_{1}.png"></img>
                """.format(username,userid,category_name,division_name)

        elif labgroup == 'subcon':
            pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                                    <img class="div_subcon_pic"  id="subconpic" data-jist-userid="{1}" data-jist-labourgroup="subcon" title="{0}" src="/images/subconpics/{2}.png"></img>
                """.format(username,userid,"user_subcon_none",division_name,category_name)
            else:
                staffpic = """ 
                                    <img  class="div_subcon_pic"  id="subconpic" data-jist-userid="{1}" data-jist-labourgroup="subcon" title="{0}" src="/images/subconpics/subcon_{1}.png"></img>
                """.format(username,userid,division_name,category_name)
        return staffpic

    def get_labour_picture_src(self,labgroup,userid,username,division_name,category_name):
        if labgroup == 'staff':
            pic_path = os.path.join(staff_picdir, "{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                                     src="/images/staffpics/{1}.png"
                """.format(username,userid,"1",category_name,division_name)
            else:
                staffpic = """ 
                                     src="/images/staffpics/{1}.png"
                """.format(username,userid,category_name,division_name)
        elif labgroup == 'labour':
            pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                                    src="/images/labourpics/{2}.png"
                """.format(username,userid,"user_lab_none",category_name,division_name)
            else:
                staffpic = """ 
                                    src="/images/labourpics/labour_{1}.png"
                """.format(username,userid,category_name,division_name)

        elif labgroup == 'subcon':
            pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """
                                     src="/images/subconpics/{2}.png"
                """.format(username,userid,"user_subcon_none",division_name,category_name)
            else:
                staffpic = """ 
                                     src="/images/subconpics/subcon_{1}.png"
                """.format(username,userid,division_name,category_name)
        return staffpic

    def get_labour_picture_path(self,labgroup,userid,username,division_name,category_name):
        if labgroup == 'staff':
            pic_path = os.path.join(staff_picdir, "{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """images/staffpics/{1}.png""".format(username,userid,"1",category_name,division_name)
            else:
                staffpic = """images/staffpics/{1}.png""".format(username,userid,category_name,division_name)
        elif labgroup == 'labour':
            pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """images/labourpics/{2}.png""".format(username,userid,"user_lab_none",category_name,division_name)
            else:
                staffpic = """images/labourpics/labour_{1}.png""".format(username,userid,category_name,division_name)

        elif labgroup == 'subcon':
            pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(userid))
            if not os.path.exists(pic_path):  
                staffpic = """images/subconpics/{2}.png""".format(username,userid,"user_subcon_none",division_name,category_name)
            else:
                staffpic = """images/subconpics/subcon_{1}.png""".format(username,userid,division_name,category_name)
        return staffpic

    @expose()
    def get_labour_teams_picture_html(self,**kw):
        allteamslist= DBS_JistLabour.query(JistLabourTeamsList). \
                all()
        #teamstaffids = [k.team_staff_member_id for k in teamliststaff] 
        #teamlabourids = [k.team_lab_member_id for k in teamlistlabour] 
        #teamsubconids = [k.team_subcon_member_id for k in teamlistsubcon] 
        html2 = ''
        htmltemp = ''
        header = """<h4 class="modal-content">All Labour Teams<span class='spanright'>  </span></h4>"""
        htmlstaff1 = header + """<div id="labour_teams_accordion">"""
        html2 = ''
        htmltemp = ''
        if len(allteamslist) > 0:
            for team in allteamslist:
                teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id).all()
                teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id).all()
                teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id).all()
                sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
                teamliststafffirst= DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id). \
                        order_by(asc(JistLabourTeamsMembers.id)).first()
                teamlistlabourfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id). \
                        order_by(asc(JistLabourTeamsMembers.id)).first()
                teamlistsubconfirst = DBS_JistLabour.query(JistLabourTeamsMembers). \
                        filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                        filter(JistLabourTeamsMembers.team_id == team.id). \
                        order_by(asc(JistLabourTeamsMembers.id)).first()
                userimg = None
                notuserfound = True
                while notuserfound:
                    if teamliststafffirst and notuserfound:
                        #print "Staff First {0}".format(teamliststafffirst.team_staff_member_id)
                        pic_path = os.path.join(staff_picdir, "{0}.png".format(teamliststafffirst.team_staff_member_id))
                        staff_division = DBS_JistLabour.query(JistStaffDivisionLink). \
                                filter(JistStaffDivisionLink.user_id==teamliststafffirst.team_staff_member_id). \
                                one()
                        thisuserdivisionid = staff_division.lab_division_id
                        if not os.path.exists(pic_path):  
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_staffpic" src="/images/staffpics/1.png"></img>
                                      """.format(teamliststafffirst.team_staff_member_id)
                        else:
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_staffpic" src="/images/staffpics/{0}.png"></img>
                                      """.format(teamliststafffirst.team_staff_member_id)
                        notuserfound = False
                    elif teamlistlabourfirst and notuserfound:
                        #print "Labour First {0}".format(teamlistlabourfirst.team_lab_member_id)
                        this_user = DBS_JistLabour.query(JistLabourList). \
                                filter(JistLabourList.id==teamlistlabourfirst.team_lab_member_id). \
                                one()
                        thisuserdivisionid = this_user.division
                        pic_path = os.path.join(labour_picdir, "labour_{0}.png".format(teamlistlabourfirst.team_lab_member_id))
                        if not os.path.exists(pic_path):  
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_labourpic" src="/images/labourpics/user_lab_none.png"></img>
                                      """.format(teamlistlabourfirst.team_lab_member_id)
                        else:
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_labourpic" src="/images/labourpics/labour_{0}.png"></img>
                                      """.format(teamlistlabourfirst.team_lab_member_id)
                        notuserfound = False
                    elif teamlistsubconfirst and notuserfound:
                        #print "Subcon First {0}".format(teamlistsubconfirst.team_subcon_member_id)
                        subcon_division = DBS_JistLabour.query(JistSubconDivisionLink). \
                                filter(JistSubconDivisionLink.user_id==teamlistsubconfirst.team_subcon_member_id). \
                                one()
                        thisuserdivisionid = subcon_division.lab_division_id
                        pic_path = os.path.join(subcon_picdir, "subcon_{0}.png".format(teamlistsubconfirst.team_subcon_member_id))
                        if not os.path.exists(pic_path):  
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_subconpic" src="/images/subconpics/user_subcon_none.png"></img>
                                      """.format(teamlistsubconfirst.team_subcon_member_id)
                        else:
                            userimg = """
                                        <img  class="div_leader_accord_team_pic"  id="leader_subconpic" src="/images/subconpics/subcon_{0}.png"></img>
                                      """.format(teamlistsubconfirst.team_subcon_member_id)
                        notuserfound = False
                    else:
                        notuserfound = False
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==thisuserdivisionid). \
                        one()
                htmltemp = """
                            <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                    <li class="ui-widget-content ui-corner-tr">
                                    <h6 class="ui-widget-header">{0}</h6>
                                    {2}
                                    <h6 class="ui-widget-header">{3}</h6>
                                    </li>
                            </ul>
                           """.format(team.team_name,sumteams,userimg,divisionone.division_name)
                htmllast = """
                                </div>
                            </div>
                       """

                #html2 =  html2 + htmltemp + htmlfaces + htmllast 
                html2 =  html2 + htmltemp  
        htmllastdiv = "</div>"
        #return htmlstaff1 + html2 + htmllastdiv
        return html2

    @expose()
    def get_labour_team_people_html(self,**kw):
        if kw['teamid'] == '': return
        team= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id==kw['teamid']).one()
        teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                order_by(desc(JistFleetList.id)). \
                all()
        editfleet_form2 = """ <select id="edit_team_vehicle_id"  class="text ui-widget-content ui-corner-all">
                        <option value="">Select one...</option>
                        """
        for fleet in fleetlist: 
            if fleet.id == team.team_vehicle_id:
                editfleet_temp = """
                              <option value="%s" selected="selected">%s</option>
                          """%(fleet.id, fleet.registration_number)
                editfleet_form2 = editfleet_form2 + editfleet_temp

            else:
                editfleet_temp = """
                              <option value="%s">%s</option>
                          """%(fleet.id, fleet.registration_number)
                editfleet_form2 = editfleet_form2 + editfleet_temp
        htmltemp = """
                    <div class='accord_header'>
                    <h3>{0}<span class='accord_qty'>{1} people</span></h3>
                        <div>
                   """.format(team.team_name,sumteams)
        htmlfaces = """
                       <label>Team Name</label><input type="text" name="edit_team_name" value="{0}" id="edit_team_name" class="text ui-widget-content ui-corner-all" /><br/>
                    """.format(team.team_name,team.id,team.team_description,editfleet_form2)
        for staff_mem in teamliststaff:
            thisuser = DBS_ContractData.query(User).filter(User.user_id==staff_mem.team_staff_member_id).one()
            if thisuser.active_status:
                staffdivision_link = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==thisuser.user_id). \
                        one()
                staffcategory_link = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==thisuser.user_id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==staffcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==staffdivision_link.lab_division_id). \
                        one()
                staffpic = self.get_labour_picture_html('staff',thisuser.user_id,thisuser.user_name,divisionone.division_name,categoryone.category_name)
                htmlfaces =  htmlfaces + staffpic 
        for staff_mem in teamlistlabour:
            thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staff_mem.team_lab_member_id).one()
            if thisuser.active:
                labcategory_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                        filter(JistLabourCategoryLink.user_id==thisuser.id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==labcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==thisuser.division). \
                        one()
                staffpic = self.get_labour_picture_html('labour',thisuser.id,thisuser.first_name+' '+thisuser.last_name,divisionone.division_name,categoryone.category_name)
                htmlfaces =  htmlfaces + staffpic 
        for staff_mem in teamlistsubcon:
            thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staff_mem.team_subcon_member_id).one()
            if thisuser.active:
                subcondivision_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                        filter(JistSubconDivisionLink.user_id==thisuser.id). \
                        one()
                subconcategory_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                        filter(JistSubconCategoryLink.user_id==thisuser.id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==subconcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==subcondivision_link.lab_division_id). \
                        one()
                staffpic = self.get_labour_picture_html('subcon',thisuser.id,thisuser.trading_name,divisionone.division_name,categoryone.category_name)
                htmlfaces =  htmlfaces + staffpic 
        return htmlfaces

    def get_labour_team_people_path(self,teamid,**kw):
        team= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id==teamid).one()
        teamliststaff= DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_staff_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistlabour = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_lab_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        teamlistsubcon = DBS_JistLabour.query(JistLabourTeamsMembers). \
                filter(JistLabourTeamsMembers.team_subcon_member_id != None). \
                filter(JistLabourTeamsMembers.team_id == team.id).all()
        sumteams = len(teamliststaff) + len(teamlistlabour) + len(teamlistsubcon)
        fleetlist = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                order_by(desc(JistFleetList.id)). \
                all()
        editfleet_form2 = """ <select id="edit_team_vehicle_id"  class="text ui-widget-content ui-corner-all">
                        <option value="">Select one...</option>
                        """
        for fleet in fleetlist: 
            if fleet.id == team.team_vehicle_id:
                editfleet_temp = """
                              <option value="%s" selected="selected">%s</option>
                          """%(fleet.id, fleet.registration_number)
                editfleet_form2 = editfleet_form2 + editfleet_temp

            else:
                editfleet_temp = """
                              <option value="%s">%s</option>
                          """%(fleet.id, fleet.registration_number)
                editfleet_form2 = editfleet_form2 + editfleet_temp
        htmltemp = """
                    <div class='accord_header'>
                    <h3>{0}<span class='accord_qty'>{1} people</span></h3>
                        <div>
                   """.format(team.team_name,sumteams)
        htmlfaces = """
                       <label>Team Name</label><input type="text" name="edit_team_name" value="{0}" id="edit_team_name" class="text ui-widget-content ui-corner-all" /><br/>
                    """.format(team.team_name,team.id,team.team_description,editfleet_form2)
        htmlfaces = []
        for staff_mem in teamliststaff:
            thisuser = DBS_ContractData.query(User).filter(User.user_id==staff_mem.team_staff_member_id).one()
            if thisuser.active_status:
                staffdivision_link = DBS_JistLabour.query(JistStaffDivisionLink). \
                        filter(JistStaffDivisionLink.user_id==thisuser.user_id). \
                        one()
                staffcategory_link = DBS_JistLabour.query(JistStaffCategoryLink). \
                        filter(JistStaffCategoryLink.user_id==thisuser.user_id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==staffcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==staffdivision_link.lab_division_id). \
                        one()
                staffpic = self.get_labour_picture_path('staff',thisuser.user_id,thisuser.user_name,divisionone.division_name,categoryone.category_name)
                #htmlfaces =  htmlfaces + staffpic 
                htmlfaces.append({'staffpic':staffpic,'username':thisuser.user_name,'division':divisionone.division_name,'category':categoryone.category_name})
        for staff_mem in teamlistlabour:
            thisuser = DBS_JistLabour.query(JistLabourList).filter(JistLabourList.id==staff_mem.team_lab_member_id).one()
            if thisuser.active:
                labcategory_link = DBS_JistLabour.query(JistLabourCategoryLink). \
                        filter(JistLabourCategoryLink.user_id==thisuser.id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==labcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==thisuser.division). \
                        one()
                staffpic = self.get_labour_picture_path('labour',thisuser.id,thisuser.first_name+' '+thisuser.last_name,divisionone.division_name,categoryone.category_name)
                #htmlfaces =  htmlfaces + staffpic 
                htmlfaces.append({'staffpic':staffpic,'username':thisuser.first_name+' '+thisuser.last_name,'division':divisionone.division_name,'category':categoryone.category_name})
        for staff_mem in teamlistsubcon:
            thisuser = DBS_JistLabour.query(JistSubconList).filter(JistSubconList.id==staff_mem.team_subcon_member_id).one()
            if thisuser.active:
                subcondivision_link = DBS_JistLabour.query(JistSubconDivisionLink). \
                        filter(JistSubconDivisionLink.user_id==thisuser.id). \
                        one()
                subconcategory_link = DBS_JistLabour.query(JistSubconCategoryLink). \
                        filter(JistSubconCategoryLink.user_id==thisuser.id). \
                        one()
                categoryone = DBS_JistLabour.query(JistLabourCategories). \
                        filter(JistLabourCategories.id==subconcategory_link.lab_category_id). \
                        one()
                divisionone = DBS_JistLabour.query(JistLabourDivisions). \
                        filter(JistLabourDivisions.id==subcondivision_link.lab_division_id). \
                        one()
                staffpic = self.get_labour_picture_path('subcon',thisuser.id,thisuser.trading_name,divisionone.division_name,categoryone.category_name)
                #htmlfaces =  htmlfaces + staffpic 
                htmlfaces.append({'staffpic':staffpic,'username':thisuser.trading_name,'division':divisionone.division_name,'category':categoryone.category_name})
        return htmlfaces

    @expose()
    def get_labour_team_schedule_form(self,**kw):
        teamid = kw['teamid']
        html3 = """
                    <select id='days_count' name='days_count' class="text ui-widget-content ui-corner-all" >
                """
        for m in range(31): 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m,m)
            html3 = html3 + html3temp
        html3 = html3 + "</select>"
        jcnobox = self.produce_jcno_listbox()
        team= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id==teamid).one()
        html1 = """
                        <fieldset>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_toggle_team_faces">Toggle Team Faces</button>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_toggle_contract_tasks">Toggle Contract Tasks</button>
                        <p/>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_unschedule_date">Unschedule Date</button>
                        <button class="ui-widget ui-widget-content ui-state-default" id="button_toggle_printing">Toggle Printing Menu</button>
                        </fieldset>
                    <form id="team_schedule_frm">
                        <fieldset>
                            <!--label for="">Team ID</label-->
                            <input type="text" value="{2}" name="teamid" id="teamid" class="text ui-widget-content ui-corner-all" />
                            <label for="">Team Name</label>
                            <input type="text" value="{3}" name="teamname" id="teamname" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">JCNO</label>
                            {1}
                            <br/>
                            <label for="">Start Date</label>
                            <input type="text" name="startdate" id="startdate" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for=""> Task Name</label>
                            <input type="text"  name="taskname" id="taskname" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">No Of Days</label>
                            {0}<br/>
                            <button class="ui-widget ui-widget-content ui-state-default" id="button_schedule_team">Schedule Team</button>
                        </fieldset>
                    </form>
                """.format(html3,jcnobox,teamid,team.team_name)
        return html1

    @expose()
    def get_labour_printing_form(self,**kw):
        teamid = kw['teamid']
        jcno = kw['contractid']
        team= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id==teamid).one()
        html1 = """
                        <fieldset>
                """
        html2 = """    <a href='/labourcont/export_schedule_labour_for_teams_dates_pdf/{0}'><img id='print_labour_schedule' src='/images/pdficon.jpg'>PDF Team Schedule</img></a>
                       <p/>
                           <a href='/labourcont/export_team_faces_pdf/{0}'><img id='print_team_faces' src='/images/pdficon.jpg'>PDF Team Faces</img></a>
                       <p/>
                """.format(teamid,team.team_name)
        htmlclose ="""</fieldset>"""

        if jcno != 'None':
            html3 = """  
                           <a href='/labourcont/export_contract_schedule_pdf/{0}'><img id='print_contract_schedule' src='/images/pdficon.jpg'>PDF Teams Scheduled per Contract</img></a>
                       <p/>
                           <a href='/labourcont/export_contract_tasks_pdf/{0}'><img id='print_contract_tasks' src='/images/pdficon.jpg'>PDF Contract Tasks</img></a>
                       <p/>
                           <a href='/contractscont/exportcontract_scopepdf/{0}'><img id='print_contract_directions' src='/images/pdficon.jpg'>PDF Contract Scope</img></a>
                       <p/>
                    """.format(jcno,team.team_name)
            try:
                thisites = DBS_ContractData.query(JistContracts). \
                            filter(JistContracts.jno==jcno). \
                            one()
                location = DBS_ContractData.query(JistLocationList). \
                        filter(JistLocationList.id==int(thisites.locationid)). \
                        one()
                streetviewpics = "<a href='/productioncont/export_google_street_view?lat=%s&lng=%s'><img src='/images/pdficon.jpg'>PDF Google Streetview</img></a>"%(location.lat,location.lng)
                mapdirections = "<a href='/productioncont/export_google_maps?lat={1}&lng={2}&site={3}&jcno={4}'><img src='/images/pdficon.jpg'>PDF Google Maps</img></a>".format(location.id, location.lat,location.lng, thisites.site, thisites.jno)
                trashpic = "<img value='%s' class='location_trash' src='/images/trash.png' alt=''/>"%(location.id)
                add_lat = location.lat
                add_lng = location.lng
                html4 = """
                        {0}
                        <p/>
                        {1}
                        """.format(streetviewpics,mapdirections)
                return html1 + html2 + html3 + html4 + htmlclose
            except:
                pass
                

            return html1 + html2 + html3 + htmlclose
        else:
            return html1 + html2 + htmlclose


    def produce_jcno_listbox(self):
        pointlist = []
        productionlist = []
        accountslist = []
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
                    order_by(desc(JistContracts.jno)).all()

        for thisites in contracts:
            #username = request.identity['repoze.who.userid']
            #usernow = User.by_user_name(username)
            #thisuseridnew = usernow.user_id
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
                         'loclat':location.lat,
                         'loclng':location.lng,
                         })
        html2 = """<select id='jcno_listbox' name='jcno_listbox'>
                   <option value='Select a Contract'></option> 
        """
        for scp in dictsites:
            html2temp = """
                        <option value='%s'>%s-%s-%s-%s-%s</option>
                        """%(scp["jno"],scp["jno"],scp["client"],scp["site"],scp["description"],scp['pointperson'])
            html2 = html2 + html2temp
        html2 = html2 + "</select>"
        return html2

    @expose()
    def check_schedule_team(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        jcno = kw['jcno_listbox']
        #Dayscount needs to be less one to user one day as dayscount is added to datetime
        dayscount = int(kw['days_count']) - 1
        startdate = kw['startdate']
        teamid = kw['teamid']
        enddate = None
        year =startdate.split('-')[0]
        month =startdate.split('-')[1]
        day =startdate.split('-')[2]
        thisday = date(int(year),int(month),int(day))
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        tempenddate = datetime.combine(thisday,sttimeend)
        tempstartdate = datetime.combine(thisday,sttimestart)
        end_inclweekends_date = datetime.date(tempenddate) + timedelta(days=int(dayscount))
        temp_end_businness_date = self.getNthBusinessDay(tempenddate,int(dayscount))
        temp_end_businness_date_incl_sat = self.getNthBusinessDay_Incl_Sat(tempenddate,int(dayscount))
        end_businness_date_incl_sat = datetime.date(temp_end_businness_date_incl_sat)
        end_businness_date = datetime.date(temp_end_businness_date)
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                all()
        list_all_records = [rec.schedule_date for rec in all_records]
        for dt in self.get_daterange(tempstartdate,temp_end_businness_date): 
            if datetime.date(dt) in list_all_records:
                return json.dumps({"response": 'fail',"date":str(datetime.date(dt))})
        return json.dumps({"response": 'success'})

    @expose()
    def schedule_team(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        jcno = kw['jcno_listbox']
        #Dayscount needs to be less one to user one day as dayscount is added to datetime
        dayscount = int(kw['days_count']) - 1
        startdate = kw['startdate']
        teamid = kw['teamid']
        taskname = kw['taskname']
        enddate = None
        year =startdate.split('-')[0]
        month =startdate.split('-')[1]
        day =startdate.split('-')[2]
        thisday = date(int(year),int(month),int(day))
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        tempenddate = datetime.combine(thisday,sttimeend)
        tempstartdate = datetime.combine(thisday,sttimestart)
        end_inclweekends_date = datetime.date(tempenddate) + timedelta(days=int(dayscount))
        temp_end_businness_date = self.getNthBusinessDay(tempenddate,int(dayscount))
        temp_end_businness_date_incl_sat = self.getNthBusinessDay_Incl_Sat(tempenddate,int(dayscount))
        end_businness_date_incl_sat = datetime.date(temp_end_businness_date_incl_sat)
        end_businness_date = datetime.date(temp_end_businness_date)
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        for dt in self.get_daterange(tempstartdate,temp_end_businness_date): 
            #Add code to check if date and team for already exist
            if datetime.date(dt).weekday() < 5:
                u = JistLabourTeamsSchedule()
                u.schedule_date = datetime.date(dt) 
                u.team_id = teamid 
                u.task_name = taskname 
                u.jcno = jcno 
                u.work_percent = 100 
                u.useridnew = usernow.user_id
                u.dateadded = datetime.date(datetime.now()) 
                DBS_JistLabour.add(u)
        DBS_JistLabour.flush()
        
    def getNthBusinessDay(self,startDate, businessDaysInBetween):
        currentDate = startDate
        daysToAdd = businessDaysInBetween
        while daysToAdd > 0:
            currentDate += timedelta(days=1)
            day = currentDate.weekday()
            if day < 5:
                daysToAdd -= 1
        return currentDate 

    def getNthBusinessDay_Incl_Sat(self,startDate, businessDaysInBetween):
        currentDate = startDate
        daysToAdd = businessDaysInBetween
        while daysToAdd > 0:
            currentDate += timedelta(days=1)
            day = currentDate.weekday()
            if day < 5:
                daysToAdd -= 1
        return currentDate 

    def get_daterange(self, start_date, end_date ):
        if start_date <= end_date:
            for n in range( ( end_date - start_date ).days + 1 ):
                yield start_date + timedelta(days= n )
        else:
            for n in range( ( start_date - end_date ).days + 1 ):
                yield start_date - timedelta(days= n )

    @expose()
    def export_schedule_labour_list_scheduled_by_date(self,**kw):
        thisdate = kw['thisdate']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.schedule_date==thisdate). \
                all()
        outputlist = []
        for schedule  in schedules:
            team= DBS_JistLabour.query(JistLabourTeamsList). \
                          filter(JistLabourTeamsList.id==schedule.team_id).one()
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==int(schedule.jcno)). \
                    one()
            userimg, sumteams, divisionid = self.get_labour_leader_team_pic_html(team)
            html2 = ''
            htmltemp = """
                        <ul id="gallery_team_labour_scheduled" class="gallery ui-helper-reset ui-helper-clearfix">
                                <li class="ui-widget-content ui-corner-tr">
                                <h7 class="ui-widget-header">{0}</h7>
                                {2}
                                </li>
                        </ul>
                       """.format(team.team_name,sumteams,userimg,)
            html2 =  html2 + htmltemp  

            outputlist.append({
                          'id':schedule.id,
                          'jcno':schedule.jcno,
                          'date':schedule.schedule_date,
                          'task':schedule.task_name,
                          'site':contract.site,
                          'description':contract.description,
                         'staffpic':""" <img  id="req_by_user" title="{0}" src="/images/staffpics/{0}.png"></img>""".format(schedule.useridnew),
                         'teampic':html2
                         })
        headers =["ID","Date","JCNo","Site","Description","Task","Team","Booked By"]
        #headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['id','date','jcno','site','description','task','teampic','staffpic']
        headerwidths=[30,80,30,'','','',180,30,30,30,30,30]
        tdclassnames=['','','','','','','','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_teamschedule_list")
        header = """<h5 class="modal-content"> All Scheduled Teams for: {1} <span class='spanright'> {0} teams </span></h5>""".format(len(outputlist),thisdate)
        return header + htmltbl

    @expose()
    def export_schedule_labour_list_nonscheduled_by_date(self,**kw):
        thisdate = kw['thisdate']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.schedule_date==thisdate). \
                all()

        teams= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id).all()
        teamlist = [team.id for team in teams]
        schedulelist = [schedule.team_id for schedule in schedules]
        html2 = ''
        teamcount = 0
        for team  in teams:
            if team.id not in schedulelist:
                teamcount += 1
                userimg, sumteams, divisionid = self.get_labour_leader_team_pic_html(team)
                if divisionid:
                    division = DBS_JistLabour.query(JistLabourDivisions). \
                                filter(JistLabourDivisions.id == int(divisionid)).one()
                    htmltemp = """
                                <ul id="gallery_team_labour" class="gallery ui-helper-reset ui-helper-clearfix">
                                        <li class="ui-widget-content ui-corner-tr">
                                        <h6 class="ui-widget-header">{0}</h6>
                                        {2}
                                        <h6 class="ui-widget-header">{3}</h6>
                                        </li>
                                </ul>
                               """.format(team.team_name,sumteams,userimg,division.division_name)
                    html2 =  html2 + htmltemp  

        header = """<h5 class="modal-content"> Teams Not Scheduled For: {1} <span class='spanright'> {0} teams </span></h5>""".format(teamcount,thisdate)
        return header + html2

    @expose()
    def export_schedule_list_for_team_html(self,**kw):
        teamid = kw['teamid']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                all()
        outputlist = []
        for schedule  in schedules:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            outputlist.append({
                          'id':schedule.id,
                          'jcno':schedule.jcno,
                          'date':schedule.schedule_date,
                         'staffpic':""" <img  id="req_by_user" title="{0}" src="/images/staffpics/{0}.png"></img>""".format(schedule.useridnew)
                         })
        headers =["ID","Date","JCNo","Booked By"]
        #headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['id','date','jcno','staffpic']
        headerwidths=[30,'80',30,50,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_teamschedule_list")
        header = """<h5 class="modal-content"> Team Schedule <span class='spanright'> {0} days </span></h5>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_schedule_list_for_contract_html(self,**kw):
        jcno = kw['contractid']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        outputlist = []
        for schedule  in schedules:
            team= DBS_JistLabour.query(JistLabourTeamsList). \
                          filter(JistLabourTeamsList.id==schedule.team_id).one()
            userimg, sumteams, divisionid = self.get_labour_leader_team_pic_html(team)
            html2 = ''
            htmltemp = """
                        <ul id="gallery_team_labour_small" class="gallery ui-helper-reset ui-helper-clearfix">
                                <li class="ui-widget-content ui-corner-tr">
                                <h7 class="ui-widget-header">{0}</h7>
                                {2}
                                </li>
                        </ul>
                       """.format(team.team_name,sumteams,userimg,)
            html2 =  html2 + htmltemp  

            outputlist.append({
                          'id':schedule.id,
                          'jcno':schedule.jcno,
                          'date':schedule.schedule_date,
                         'staffpic':""" <img  id="req_by_user" title="{0}" src="/images/staffpics/{0}.png"></img>""".format(schedule.useridnew),
                         'teampic':html2
                         })
        headers =["ID","Date","JCNo","Booked By","Team"]
        #headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['id','date','jcno','staffpic','teampic']
        headerwidths=[30,80,30,50,50,10,10,30,30,30,30,30]
        tdclassnames=['','','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_teamschedule_list")
        header = """<h5 class="modal-content"> Contract Schedule <span class='spanright'> {0} days </span></h5>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    def export_schedule_contract_tasks_html(self,**kw):
        jcno = kw['contractid']
        schedules = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.team_id)). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        outputlist = []
        for team in schedules:
            planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.min(JistLabourTeamsSchedule.schedule_date))
            planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.max(JistLabourTeamsSchedule.schedule_date))
            thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                    filter(JistLabourTeamsList.id==team[0]). \
                    one()
            all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            all_tasks = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.task_name)). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            list_all_records = [rec.schedule_date for rec in all_records]
            #daysbetween = planlastdate - planfirstdate
            #all_days_between = dt_allenddate - dt_allstartdate
            #dayofweek_start = planfirstdate.isoweekday()
            #strdaysbetween = str(daysbetween).split(' ')[0]
            #firstdateloop = planfirstdate
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==int(jcno)). \
                    one()
            dtplanstartdate = planfirstdate
            dtplanenddate = planlastdate
            ganttlist = []
            for task in all_tasks:
                thisrecordmax = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                        filter(JistLabourTeamsSchedule.task_name==task[0]). \
                        filter(JistLabourTeamsSchedule.team_id==team[0]). \
                        filter(JistLabourTeamsSchedule.jcno==jcno). \
                        value(func.max(JistLabourTeamsSchedule.schedule_date))
                thisrecordmin = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                        filter(JistLabourTeamsSchedule.task_name==task[0]). \
                        filter(JistLabourTeamsSchedule.team_id==team[0]). \
                        filter(JistLabourTeamsSchedule.jcno==jcno). \
                        value(func.min(JistLabourTeamsSchedule.schedule_date))
                schedule_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                        filter(JistLabourTeamsSchedule.task_name==task[0]). \
                        filter(JistLabourTeamsSchedule.team_id==team[0]). \
                        filter(JistLabourTeamsSchedule.jcno==jcno). \
                        all()
                outputlist.append({'jno':contract.jno,
                              'orderno':contract.orderno,
                             'client':contract.client,
                             'description':contract.description,
                             'site':contract.site,
                             'contact':contract.contact,
                             'tel':contract.tel,
                             'fax':contract.fax,
                             'cell':contract.cell,
                             'workcategory':contract.workcategory,
                             'cidbcategory':contract.cidbcategory,
                             'cidbrating':contract.cidbrating,
                             'groupjno':contract.groupjno,
                             'completed':contract.completed,
                             'planstart':str(thisrecordmin),
                             'planend':str(thisrecordmax),
                             'ganttlist':ganttlist,
                             'teamname':thisteam.team_name,
                             'taskname':task[0],
                             'staffpic':""" <img  id="req_by_user" title="{0}" src="/images/staffpics/{0}.png"></img>""".format(schedule_records[0].useridnew)
                             })
        headers =["JCNo","Team Name","Task Name","Start Date","End Date","Booked By"]
        #headerwidths=[50,200,200,200,80,80,80]
        dictlist = ['jno','teamname','taskname','planstart','planend','staffpic']
        headerwidths=[30,100,'',80,80,80,10,30,30,30,30,30]
        tdclassnames=['','','','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_labour_html_table_new(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_teamschedule_list")
        header = """<h5 class="modal-content"> Contract Tasks <span class='spanright'> {0} tasks </span></h5>""".format(len(outputlist))
        return header + htmltbl

    @expose()
    @expose('json')
    def get_schedule_labour_for_contracts_dates_json(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        jcno = kw['contractid']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                value(func.min(JistLabourTeamsSchedule.schedule_date))
        planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                value(func.max(JistLabourTeamsSchedule.schedule_date))

        outputlist = []
        """
        for schedule  in schedules:
            team= DBS_JistLabour.query(JistLabourTeamsList). \
                          filter(JistLabourTeamsList.id==schedule.team_id).one()
            schedule.schedule_date
            outputlist.append({
                          'id':schedule.id,
                          'jcno':schedule.jcno,
                          'date':schedule.schedule_date,
                         })

        """
        if not planfirstdate: return outputlist.append({'result':'Not Sheduled'})
        datepack = []
        strplanfirstdate = planfirstdate.strftime("%Y-%m-%d")
        strplanlastdate = planlastdate.strftime("%Y-%m-%d")
        daysbetween = planlastdate - planfirstdate
        dayofweek_start = planfirstdate.isoweekday()
        strdaysbetween = str(daysbetween).split(' ')[0]
        #print planfirstdate, planlastdate
        #print type(daysbetween)
        #print 'Days Between in days {0}'.format(daysbetween.days)
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
        for i in range(daysbetween.days+7):
            dateslist.append(firstdateloop.strftime("%d"))
            monthslist.append(firstdateloop.strftime("%B %Y"))
            weekdaylist.append(firstdateloop.strftime("%w"))
            weeknoyrlist.append(firstdateloop.strftime("%W"))
            daynoyrlist.append(firstdateloop.strftime("%j"))
            #dt = dts.strftime("%A, %d %B %Y %H:%M:%S"))
            firstdateloop += delta_1day
        #print 'Start Date {0}'.format(strplanfirstdate)
        #print 'Last Date {0}'.format(strplanlastdate)
        #print 'Day of Week {0}'.format(dayofweek_start)
        #print 'Day List', daylist
        #print 'Dates List', dateslist
        #print 'Months List', monthslist

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
                         'startdate':strplanfirstdate,
                         'enddate':strplanlastdate
                        }) 
        return json.dumps(datepack)

    @expose()
    @expose('json')
    def get_labour_schedule_contracts_json_daily_data(self,**kw):
        jcno = kw['contractid']
        teamid = kw['teamid']
        allstartdate = kw['allstart']
        allenddate = kw['allend']
        schedules = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.team_id)). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        dictsites = []
        for team in schedules:
            planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.min(JistLabourTeamsSchedule.schedule_date))
            planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.max(JistLabourTeamsSchedule.schedule_date))
            thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                    filter(JistLabourTeamsList.id==team[0]). \
                    one()
            all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            all_tasks = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.task_name)). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()

            list_all_records = [rec.schedule_date for rec in all_records]
            dt_allstartdate = datetime.strptime(allstartdate,"%Y-%m-%d")
            dt_allenddate = datetime.strptime(allenddate,"%Y-%m-%d")
            #print dt_allstartdate, dt_allenddate
            #print 'Days Between in days {0}'.format(daysbetween.days)
            daysbetween = planlastdate - planfirstdate
            all_days_between = dt_allenddate - dt_allstartdate
            dayofweek_start = planfirstdate.isoweekday()
            strdaysbetween = str(daysbetween).split(' ')[0]
            firstdateloop = planfirstdate
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==int(jcno)). \
                    one()
            dtplanstartdate = planfirstdate
            dtplanenddate = planlastdate
            ganttlist = []
            for dt in self.get_daterange(dt_allstartdate,dt_allenddate): 
                #if dtplanstartdate <= datetime.date(dt) <= dtplanenddate:
                if datetime.date(dt) in list_all_records:
                    ganttlist.append('T')
                else:
                    ganttlist.append('F')
            taskname = ''
            if len(all_tasks) > 1:
                taskname = str(len(all_tasks)) + " Tasks"
            else:
                taskname = all_tasks[0]
            dictsites.append({'jno':contract.jno,
                          'orderno':contract.orderno,
                         'client':contract.client,
                         'description':contract.description,
                         'site':contract.site,
                         'contact':contract.contact,
                         'tel':contract.tel,
                         'fax':contract.fax,
                         'cell':contract.cell,
                         'workcategory':contract.workcategory,
                         'cidbcategory':contract.cidbcategory,
                         'cidbrating':contract.cidbrating,
                         'groupjno':contract.groupjno,
                         'completed':contract.completed,
                         'planstart':str(planfirstdate),
                         'planend':str(planlastdate),
                         'ganttlist':ganttlist,
                         'allplanstart':str(allstartdate),
                         'allplanend':str(allenddate),
                         'teamname':thisteam.team_name,
                         'taskname':taskname,
                         })
        return json.dumps(dictsites)

    @expose()
    @expose('json')
    def get_schedule_labour_for_teams_dates_json(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        #jcno = kw['contractid']
        teamid = kw['teamid']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                all()
        planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                value(func.min(JistLabourTeamsSchedule.schedule_date))
        planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                value(func.max(JistLabourTeamsSchedule.schedule_date))
        outputlist = []
        datepack = []
        if not planfirstdate: return
        #Only get the last 15 days of records
        datetoday = datetime.date(datetime.now())
        dayspass = datetoday - planfirstdate
        if dayspass.days > 30:
            planfirstdate = datetoday - timedelta(days=15)

        strplanfirstdate = planfirstdate.strftime("%Y-%m-%d")
        strplanlastdate = planlastdate.strftime("%Y-%m-%d")
        daysbetween = planlastdate - planfirstdate
        dayofweek_start = planfirstdate.isoweekday()
        strdaysbetween = str(daysbetween).split(' ')[0]
        #print planfirstdate, planlastdate
        #print type(daysbetween)
        #print 'Days Between in days {0}'.format(daysbetween.days)
        #print dayofweek_start
        #print wip
        #dt = planfirstdate.strftime("%A, %d %B %Y %H:%M:%S")
        daylisttemp = []
        allmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dow = ["S", "M", "T", "W", "T", "F", "S"]
        weeks = daysbetween.days / 7 + 3
        print weeks
        for i in range(weeks):
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
        for i in range(daysbetween.days+14):
            dateslist.append(firstdateloop.strftime("%d"))
            monthslist.append(firstdateloop.strftime("%B %Y"))
            weekdaylist.append(firstdateloop.strftime("%w"))
            weeknoyrlist.append(firstdateloop.strftime("%W"))
            daynoyrlist.append(firstdateloop.strftime("%j"))
            #dt = dts.strftime("%A, %d %B %Y %H:%M:%S"))
            firstdateloop += delta_1day
        #print 'Start Date {0}'.format(strplanfirstdate)
        #print 'Last Date {0}'.format(strplanlastdate)
        #print 'Day of Week {0}'.format(dayofweek_start)
        #print 'Day List', daylist
        #print 'Dates List', dateslist
        #print 'Months List', monthslist

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
                         'startdate':strplanfirstdate,
                         'enddate':strplanlastdate
                        }) 
        return json.dumps(datepack)

    @expose()
    @expose('json')
    def get_labour_schedule_teams_json_daily_data(self,**kw):
        teamid = kw['teamid']
        allstartdate = kw['allstart']
        allenddate = kw['allend']
        schedules = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.jcno)). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                filter(JistLabourTeamsSchedule.schedule_date>=allstartdate). \
                all()
        dictsites = []
        for schedule in schedules:
            #if schedule[0] == 0: continue
            planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==teamid). \
                    filter(JistLabourTeamsSchedule.jcno==schedule[0]). \
                    value(func.min(JistLabourTeamsSchedule.schedule_date))
            planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==teamid). \
                    filter(JistLabourTeamsSchedule.jcno==schedule[0]). \
                    value(func.max(JistLabourTeamsSchedule.schedule_date))
            thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                    filter(JistLabourTeamsList.id==teamid). \
                    one()
            all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==teamid). \
                    filter(JistLabourTeamsSchedule.jcno==schedule[0]). \
                    all()
            list_all_records = [rec.schedule_date for rec in all_records]
            dt_allstartdate = datetime.strptime(allstartdate,"%Y-%m-%d")
            dt_allenddate = datetime.strptime(allenddate,"%Y-%m-%d")
            #print dt_allstartdate, dt_allenddate
            #print 'Days Between in days {0}'.format(daysbetween.days)
            daysbetween = planlastdate - planfirstdate
            all_days_between = dt_allenddate - dt_allstartdate
            dayofweek_start = planfirstdate.isoweekday()
            strdaysbetween = str(daysbetween).split(' ')[0]
            firstdateloop = planfirstdate
            #print schedule
            #print schedule[0]
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==int(schedule[0])). \
                    one()
            dtplanstartdate = planfirstdate
            dtplanenddate = planlastdate
            ganttlist = []

            for dt in self.get_daterange(dt_allstartdate,dt_allenddate): 
                #if dtplanstartdate <= datetime.date(dt) <= dtplanenddate:
                if datetime.date(dt) in list_all_records:
                    ganttlist.append('T')
                else:
                    ganttlist.append('F')
            dictsites.append({'jno':contract.jno,
                          'orderno':contract.orderno,
                         'client':contract.client,
                         'description':contract.description,
                         'site':contract.site,
                         'contact':thisteam.team_name,
                         'tel':contract.tel,
                         'fax':contract.fax,
                         'cell':contract.cell,
                         'workcategory':contract.workcategory,
                         'cidbcategory':contract.cidbcategory,
                         'cidbrating':contract.cidbrating,
                         'groupjno':contract.groupjno,
                         'completed':contract.completed,
                         'planstart':str(planfirstdate),
                         'planend':str(planlastdate),
                         'allplanstart':str(allstartdate),
                         'allplanend':str(allenddate),
                         'ganttlist':ganttlist,
                         'teamname': thisteam.team_name
                         })
        return json.dumps(dictsites)

    @expose()
    def export_schedule_labour_for_teams_dates_pdf(self,teamid,**kw):
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #rnd = random.random()
        #print rnd
        #print listid
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Teams-Schedule-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        items = []
        datepack = self.get_date_pack_team_gantt_list(teamid) 

        totdays= datepack[0]['totaldays']
        dayslist = datepack[0]['dayslist']
        dateslist = datepack[0]['dateslist']
        monthslist = datepack[0]['monthslist']
        weekyrlist = datepack[0]['weekyrlist']
        weekdaylist=  datepack[0]['weekdaylist']
        dayyrlist=  datepack[0]['dayyrlist']
        allstartdate=  datepack[0]['startdate']
        allenddate=  datepack[0]['enddate']

        schedules = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.jcno)). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                filter(JistLabourTeamsSchedule.schedule_date>=allstartdate). \
                all()
        dictsites = []
        #staffpic = self.get_labour_leader_team_pic_html(teamid)
        leaderstaffpic = self.get_labour_leader_team_pic_path(teamid)
        leaderpic = os.path.join(public_dirname, leaderstaffpic)
        leaderface = Image(leaderpic)
        for schedule in schedules:
            #if schedule[0] == 0: continue
            planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==teamid). \
                    filter(JistLabourTeamsSchedule.jcno==schedule[0]). \
                    value(func.min(JistLabourTeamsSchedule.schedule_date))
            planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==teamid). \
                    filter(JistLabourTeamsSchedule.jcno==schedule[0]). \
                    value(func.max(JistLabourTeamsSchedule.schedule_date))
            thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                    filter(JistLabourTeamsList.id==teamid). \
                    one()
            all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==teamid). \
                    filter(JistLabourTeamsSchedule.jcno==schedule[0]). \
                    all()
            list_all_records = [rec.schedule_date for rec in all_records]
            dt_allstartdate = datetime.strptime(allstartdate,"%Y-%m-%d")
            dt_allenddate = datetime.strptime(allenddate,"%Y-%m-%d")
            #print dt_allstartdate, dt_allenddate
            #print 'Days Between in days {0}'.format(daysbetween.days)
            daysbetween = planlastdate - planfirstdate
            all_days_between = dt_allenddate - dt_allstartdate
            dayofweek_start = planfirstdate.isoweekday()
            strdaysbetween = str(daysbetween).split(' ')[0]
            firstdateloop = planfirstdate
            #print schedule
            #print schedule[0]
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==int(schedule[0])). \
                    one()
            dtplanstartdate = planfirstdate
            dtplanenddate = planlastdate
            ganttlist = []

            for dt in self.get_daterange(dt_allstartdate,dt_allenddate): 
                #if dtplanstartdate <= datetime.date(dt) <= dtplanenddate:
                if datetime.date(dt) in list_all_records:
                    ganttlist.append('T')
                else:
                    ganttlist.append('F')
            dictsites.append({'jno':contract.jno,
                          'orderno':contract.orderno,
                         'client':contract.client,
                         'description':contract.description,
                         'site':contract.site,
                         'contact':thisteam.team_name,
                         'tel':contract.tel,
                         'fax':contract.fax,
                         'cell':contract.cell,
                         'workcategory':contract.workcategory,
                         'cidbcategory':contract.cidbcategory,
                         'cidbrating':contract.cidbrating,
                         'groupjno':contract.groupjno,
                         'completed':contract.completed,
                         'planstart':str(planfirstdate),
                         'planend':str(planlastdate),
                         'allplanstart':str(allstartdate),
                         'allplanend':str(allenddate),
                         'ganttlist':ganttlist,
                         'teamname': thisteam.team_name,
                         'thisimage':leaderface 
                         })
        for x in dictsites:
            outputlist.append((
                             x['jno'],
                             Paragraph(checknullvalue(x['site']),pdffile.styleNormal),
                             Paragraph(checknullvalue(x['description']),pdffile.styleNormal),
                             Paragraph(checknullvalue(x['planstart']),pdffile.styleNormal),
                             Paragraph(checknullvalue(x['planend']),pdffile.styleNormal),
                              ))
        userdata = {
                'title1_header':'Labour:', 'title1':'Scheduled Team Work Sheet ',
                'title2_header':'Team Name', 'title2':thisteam.team_name,
                'title3_header':'Team Leader:', 'title3':'',
                'title4_header':'', 'title4':'',
                'datenow_header': "Date Printed:", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':"",
                'headerl3_header':'', 'headerl3':'',
                'headerl4_header':'', 'headerl4':' ',
                'id_header_header': "", 'id_header':'',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                'team_leader_img':leaderpic, 
                } 
        headers =["JCNo","Site Name","Description","To Start","To End"]
        headerwidths=[80,190,190,150,150,50,50,50,50,70,90,70,32,21]
        pdffile.CreatePDFLabourScheduleReport(userdata,datepack,outputlist,headers,headerwidths,11)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_team_faces_pdf(self,teamid,**kw):
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #rnd = random.random()
        #print rnd
        #print listid
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Team-Members-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        items = []
        allteam = self.get_labour_team_people_path(teamid)
        thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                      filter(JistLabourTeamsList.id==teamid).one()
        for x in allteam:
            teampic = os.path.join(public_dirname, x['staffpic'])
            memberface = Image(teampic)
            outputlist.append((
                             x['username'],
                             Paragraph(checknullvalue(x['division']),pdffile.styleNormal),
                             Paragraph(checknullvalue(x['category']),pdffile.styleNormal),
                             memberface
                              ))
        userdata = {
                'title1_header':'Labour:', 'title1':'Team Members ',
                'title2_header':'Team Name', 'title2':thisteam.team_name,
                'title3_header':'', 'title3':'',
                'title4_header':'', 'title4':'',
                'datenow_header': "Date Printed:", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':"",
                'headerl3_header':'', 'headerl3':'',
                'headerl4_header':'', 'headerl4':' ',
                'id_header_header': "", 'id_header':'',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["Member Name","Division","Labour Category","Member Pic"]
        headerwidths=[150,190,190,150,50,50,50,50,50,70,90,70,32,21]
        pdffile.CreatePDFGenericReport(userdata,outputlist,headers,headerwidths,7)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def export_contract_schedule_pdf(self,jcno,**kw):
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #rnd = random.random()
        #print rnd
        #print listid
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Contract-Teams-Scheduled-"+jcno+"-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        #jcno = kw['contractid']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                value(func.min(JistLabourTeamsSchedule.schedule_date))
        planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                value(func.max(JistLabourTeamsSchedule.schedule_date))

        outputlist = []
        #if not planfirstdate: return outputlist.append({'result':'Not Sheduled'})
        strplanfirstdate = planfirstdate.strftime("%Y-%m-%d")
        strplanlastdate = planlastdate.strftime("%Y-%m-%d")
        daysbetween = planlastdate - planfirstdate
        dayofweek_start = planfirstdate.isoweekday()
        strdaysbetween = str(daysbetween).split(' ')[0]
        #teamid = kw['teamid']
        #allstartdate = kw['allstart']
        #allenddate = kw['allend']
        schedules = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.team_id)). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        dictsites = []
        for team in schedules:
            planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.min(JistLabourTeamsSchedule.schedule_date))
            planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.max(JistLabourTeamsSchedule.schedule_date))
            thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                    filter(JistLabourTeamsList.id==team[0]). \
                    one()
            all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            all_tasks = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.task_name)). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            list_all_records = [rec.schedule_date for rec in all_records]
            #dt_allstartdate = datetime.strptime(allstartdate,"%Y-%m-%d")
            #dt_allenddate = datetime.strptime(allenddate,"%Y-%m-%d")
            #print dt_allstartdate, dt_allenddate
            #print 'Days Between in days {0}'.format(daysbetween.days)
            daysbetween = planlastdate - planfirstdate
            #all_days_between = dt_allenddate - dt_allstartdate
            #dayofweek_start = planfirstdate.isoweekday()
            #strdaysbetween = str(daysbetween).split(' ')[0]
            #firstdateloop = planfirstdate
            contract = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno==int(jcno)). \
                    one()
            dtplanstartdate = planfirstdate
            dtplanenddate = planlastdate
            ganttlist = []
            allstartdate = None
            allenddate = None
            #for dt in self.get_daterange(dt_allstartdate,dt_allenddate): 
                ##if dtplanstartdate <= datetime.date(dt) <= dtplanenddate:
                #if datetime.date(dt) in list_all_records:
                    #ganttlist.append('T')
                #else:
                    #ganttlist.append('F')
            taskname = ''
            if len(all_tasks) > 1:
                taskname = str(len(all_tasks)) + " Tasks"
            else:
                taskname = all_tasks[0]
            dictsites.append({'jno':contract.jno,
                          'orderno':contract.orderno,
                         'client':contract.client,
                         'description':contract.description,
                         'site':contract.site,
                         'contact':contract.contact,
                         'tel':contract.tel,
                         'fax':contract.fax,
                         'cell':contract.cell,
                         'workcategory':contract.workcategory,
                         'cidbcategory':contract.cidbcategory,
                         'cidbrating':contract.cidbrating,
                         'groupjno':contract.groupjno,
                         'completed':contract.completed,
                         'planstart':str(planfirstdate),
                         'planend':str(planlastdate),
                         'ganttlist':ganttlist,
                         'allplanstart':str(allstartdate),
                         'allplanend':str(allenddate),
                         'teamname':thisteam.team_name,
                         'taskname':taskname,
                         })
            outputlist.append((
                             Paragraph(checknullvalue(thisteam.team_name),pdffile.styleNormal),
                             Paragraph(checknullvalue(contract.description),pdffile.styleNormal),
                             Paragraph(checknullvalue(taskname[0]),pdffile.styleNormal),
                             Paragraph(checknullvalue(str(planfirstdate)),pdffile.styleNormal),
                             Paragraph(checknullvalue(str(planlastdate)),pdffile.styleNormal),
                              ))
        userdata = {
                'title1_header':'Labour:', 'title1':'Teams Scheduled for Contract ',
                'title2_header':'Contract', 'title2':contract.site,
                'title3_header':'JCNo', 'title3':str(contract.jno),
                'title4_header':'', 'title4':'',
                'datenow_header': "Date Printed:", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':"",
                'headerl3_header':'', 'headerl3':'',
                'headerl4_header':'', 'headerl4':' ',
                'id_header_header': "", 'id_header':'',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["Team Name","Site Description","Task Name","Start Date","End Date"]
        headerwidths=[140,140,'250',80,80,80,10,30,30,30,30,30]
        dictlist = ['jno','teamname','taskname','planstart','planend','staffpic']
        pdffile.CreatePDFGenericReport(userdata,outputlist,headers,headerwidths,11)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent


    @expose()
    def export_contract_tasks_pdf(self,jcno):
        #jcno = kw['contractid']
        import random
        #for k, w in kw.iteritems():
            #print k, w
        #rnd = random.random()
        #print rnd
        #print listid
        #return
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        #fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        datename = str(datetime.now()).split(' ')[0]
        #filename = os.path.join(pdf_dirname, str(fname))
        #pdffile = CreatePDF(filename)
        fname = "Contract-Tasks-"+jcno+"-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        schedules = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.team_id)). \
                filter(JistLabourTeamsSchedule.jcno==jcno). \
                all()
        contract = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.jno==int(jcno)). \
                one()
        outputlist = []
        for team in schedules:
            planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.min(JistLabourTeamsSchedule.schedule_date))
            planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    value(func.max(JistLabourTeamsSchedule.schedule_date))
            thisteam= DBS_JistLabour.query(JistLabourTeamsList). \
                    filter(JistLabourTeamsList.id==team[0]). \
                    one()
            all_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            all_tasks = DBS_JistLabour.query(func.distinct(JistLabourTeamsSchedule.task_name)). \
                    filter(JistLabourTeamsSchedule.team_id==team[0]). \
                    filter(JistLabourTeamsSchedule.jcno==jcno). \
                    all()
            list_all_records = [rec.schedule_date for rec in all_records]
            #daysbetween = planlastdate - planfirstdate
            #all_days_between = dt_allenddate - dt_allstartdate
            #dayofweek_start = planfirstdate.isoweekday()
            #strdaysbetween = str(daysbetween).split(' ')[0]
            #firstdateloop = planfirstdate
            dtplanstartdate = planfirstdate
            dtplanenddate = planlastdate
            ganttlist = []
            for task in all_tasks:
                thisrecordmax = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                        filter(JistLabourTeamsSchedule.task_name==task[0]). \
                        filter(JistLabourTeamsSchedule.team_id==team[0]). \
                        filter(JistLabourTeamsSchedule.jcno==jcno). \
                        value(func.max(JistLabourTeamsSchedule.schedule_date))
                thisrecordmin = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                        filter(JistLabourTeamsSchedule.task_name==task[0]). \
                        filter(JistLabourTeamsSchedule.team_id==team[0]). \
                        filter(JistLabourTeamsSchedule.jcno==jcno). \
                        value(func.min(JistLabourTeamsSchedule.schedule_date))
                schedule_records = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                        filter(JistLabourTeamsSchedule.task_name==task[0]). \
                        filter(JistLabourTeamsSchedule.team_id==team[0]). \
                        filter(JistLabourTeamsSchedule.jcno==jcno). \
                        all()
                thisstaff= DBS_ContractData.query(User). \
                        filter(User.user_id==schedule_records[0].useridnew). \
                        one()
                outputlist.append((
                                 contract.jno,
                                 Paragraph(checknullvalue(thisteam.team_name),pdffile.styleNormal),
                                 Paragraph(checknullvalue(task[0]),pdffile.styleNormal),
                                 Paragraph(checknullvalue(str(thisrecordmin)),pdffile.styleNormal),
                                 Paragraph(checknullvalue(str(thisrecordmax)),pdffile.styleNormal),
                                 Paragraph(checknullvalue(thisstaff.user_name),pdffile.styleNormal),
                                  ))
        userdata = {
                'title1_header':'Labour:', 'title1':'Contract Tasks ',
                'title2_header':'Contract', 'title2':contract.site,
                'title3_header':'JCNo', 'title3':str(contract.jno),
                'title4_header':'', 'title4':'',
                'datenow_header': "Date Printed:", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'', 'headerl2':"",
                'headerl3_header':'', 'headerl3':'',
                'headerl4_header':'', 'headerl4':' ',
                'id_header_header': "", 'id_header':'',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["JCNo","Team Name","Task Name","Start Date","End Date","Booked By"]
        headerwidths=[40,100,'250',80,80,80,10,30,30,30,30,30]
        dictlist = ['jno','teamname','taskname','planstart','planend','staffpic']
        pdffile.CreatePDFGenericReport(userdata,outputlist,headers,headerwidths,11)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def get_dialog_unschedule_date_team(self,**kw):
        html1 = """
                    <form id="dialog_unschedule_team_date_frm">
                        <fieldset>
                            <label for="">Date</label>
                            <input type="text" name="un_date" id="un_date" class="text ui-widget-content ui-corner-all" /><br/>
               """
        html4 = """
                    </fieldset>
                    </form>
                """
        return html1 + html4

    @expose()
    def delete_labour_schedule_date(self,**kw):
        thisdate = kw['thisdate']
        teamid = kw['teamid']
        schedule = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                filter(JistLabourTeamsSchedule.schedule_date==thisdate). \
                one()
        DBS_JistLabour.delete(schedule)
        DBS_JistLabour.flush()

    @expose()
    def get_labour_schedule_contract_gantt_div(self,**kw):
        return """ 
                <canvas id='jist_contract_gantt_canvas'></canvas> 
                """

    @expose()
    def get_labour_schedule_team_gantt_div(self,**kw):
        return """ 
                <canvas id='jist_team_gantt_canvas'></canvas> 
                """
    def get_date_pack_team_gantt_list(self,teamid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        ##jcno = kw['contractid']
        #teamid = kw['teamid']
        schedules = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                all()
        planfirstdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                value(func.min(JistLabourTeamsSchedule.schedule_date))
        planlastdate = DBS_JistLabour.query(JistLabourTeamsSchedule). \
                filter(JistLabourTeamsSchedule.team_id==teamid). \
                value(func.max(JistLabourTeamsSchedule.schedule_date))
        outputlist = []
        datepack = []
        if not planfirstdate: return
        #Only get the last 15 days of records
        datetoday = datetime.date(datetime.now())
        dayspass = datetoday - planfirstdate
        if dayspass.days > 30:
            planfirstdate = datetoday - timedelta(days=15)

        strplanfirstdate = planfirstdate.strftime("%Y-%m-%d")
        strplanlastdate = planlastdate.strftime("%Y-%m-%d")
        daysbetween = planlastdate - planfirstdate
        dayofweek_start = planfirstdate.isoweekday()
        strdaysbetween = str(daysbetween).split(' ')[0]
        #print planfirstdate, planlastdate
        #print type(daysbetween)
        #print 'Days Between in days {0}'.format(daysbetween.days)
        #print dayofweek_start
        #print wip
        #dt = planfirstdate.strftime("%A, %d %B %Y %H:%M:%S")
        daylisttemp = []
        allmonths = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
        dow = ["S", "M", "T", "W", "T", "F", "S"]
        weeks = daysbetween.days / 7 + 3
        for i in range(weeks):
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
        for i in range(daysbetween.days+14):
            dateslist.append(firstdateloop.strftime("%d"))
            monthslist.append(firstdateloop.strftime("%B %Y"))
            weekdaylist.append(firstdateloop.strftime("%w"))
            weeknoyrlist.append(firstdateloop.strftime("%W"))
            daynoyrlist.append(firstdateloop.strftime("%j"))
            #dt = dts.strftime("%A, %d %B %Y %H:%M:%S"))
            firstdateloop += delta_1day
        #print 'Start Date {0}'.format(strplanfirstdate)
        #print 'Last Date {0}'.format(strplanlastdate)
        #print 'Day of Week {0}'.format(dayofweek_start)
        #print 'Day List', daylist
        #print 'Dates List', dateslist
        #print 'Months List', monthslist

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
                         'startdate':strplanfirstdate,
                         'enddate':strplanlastdate
                        }) 
        return datepack


def isnumeric(value):
    return str(value).replace(".", "").replace("-", "").isdigit()

def checknullvalue(value):
    if value:
        return str(value)
    else:
        return 'undefined'

