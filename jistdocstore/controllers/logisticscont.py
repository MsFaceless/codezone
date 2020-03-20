# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group
from tg.decorators import paginate

#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
#from tw.jquery import AjaxForm
#from tw.jquery import FlexiGrid
#from tw.extjs import ItemSelector
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
from datetime import datetime, time, date
import calendar
import locale
from tg import session
from babel.numbers import format_currency, format_number, format_decimal
public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
__all__ = ['LogisticsController']
#global current_purchase_req_id  
#global current_purchase_order_id  
#global current_shopping_items 
#global current_purchase_req_items  
class LogisticsController(BaseController):
    """Sample controller-wide authorization"""
    def __init__(self):
        self.current_purchase_req_id = 0  
        self.current_purchase_order_id   = 0
        self.current_purchase_req_items = [] 
        session["mysession"] = [] 
        session.save()
        self.newreqitemfields = ['req_jcno',
                             'req_budget_item',
                             'req_item',
                             'req_description',
                             'req_unit',
                             'req_qty',
                             ]
        #Async stuff
        self.last_saved_purchasereq_rnd = 0
        self.last_saved_purchasereq_id = 0
        self.last_saved_purchaseitem_rnd = 0
        self.last_saved_grv_item_rnd = 0
        self.last_saved_order_item_rnd = 0
        self.last_saved_purchasenote_rnd = 0 
        self.last_saved_shopping_prices_rnd = 0 
        self.last_saved_purchaseadd_trolley_rnd = 0 
        self.last_saved_purchase_order_rnd = 0

    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))

    def safe(self, input):
        input = string.replace(input, "'", "\'")
        input = string.replace(input, '"', '\"')
        input = string.replace(input, "'\'", "\\")
        input = string.replace(input, "%", "\%")
        input = string.replace(input, "_", "\_")
        #input = string.replace(input, ";", "\\;")
        return input

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def index(self):
        redirect('logisticscont/menu')

    @expose('jistdocstore.templates.logistics.logisticsindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        #if session.get("mysession",None):
        #    print session["mysession"]
        return dict(page='Logistics: Main Menu') 
    
    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.supplier_search')
    def search_supplier(self,**named):
        """Handle the 'sitesearch' page."""
        #ajax_form = AjaxForm(id="myAjaxForm",
                    #fields=SupplierNameSearch(),
                    #target="output",
                    #action="do_search_supplier")
        #tmpl_context.form = ajax_form 

        return dict(page='Search Supplier [Enter Phrase]',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.supplier_new')
    def supplier_new(self,**named):
        """Handle the 'sitesearch' page."""
        #tmpl_context.form = add_new_supplier_form 
        return dict(page='Supplier New',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @require(in_any_group("managers", "logistics"))
    @expose()
    def addsupplier(self,*args,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        #status = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==kw['id']).one()
        #print args
        supname = kw['supname']
        supacc = kw['supacc']
        supadd = kw['supadd']
        supcity = kw['supcity']
        supfax = kw['supfax']
        supphone = kw['supphone']
        supcontact = kw['supcontact']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        #testsupp = DBS_JistBuying.query(JistBuyingSupplierList).all()
        #for k in testsupp:
        #    print k.city
        new_supplier = JistBuyingSupplierList()
        new_supplier.suppliername = supname
        new_supplier.accnumber=str(supacc)
        new_supplier.address=str(supadd)
        new_supplier.city=str(supcity)
        new_supplier.fax=str(supfax)
        new_supplier.phone=str(supphone)
        new_supplier.contact=str(supcontact)
        new_supplier.active=True
        DBS_JistBuying.add(new_supplier)
        DBS_JistBuying.flush()
        #redirect('/logisticscont/search_supplier?'+ supname)

    @expose('jistdocstore.templates.logistics.showstoresall')
    def showstoresall(self,**named):
        locations = DBS_JistBuying.query(JistBuyingStoresLocation).all()
        return dict(page='View All Stores',
                    locations = locations,
                    selfname = 'showstoresall',
                    pdfstring = "export_stores_list_all_pdf",
                    count=0)

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.storelocation_new')
    def storelocation_new(self,**named):

        return dict(page='New Store and Location',
                    wip = '',
                    currentPage=1,
                    value=named,
                    action = '/logisticscont/addstorelocation',
                    value2=named)

    @require(in_any_group("managers", "logistics"))
    @expose()
    def addstorelocation(self,*args,**kw):
        name = kw['store_name']
        loc = kw['store_location']
        add1 = kw['store_address_1']
        add2 = kw['store_address_2']
        add3 = kw['store_address_3']
        person = kw['store_person_name']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridnew = usernow.user_id
        #return
        #testsupp = DBS_JistBuying.query(JistBuyingSupplierList).all()
        #for k in testsupp:
        #    print k.city
        new_store = JistBuyingStoresLocation()
        new_store.store_name = name
        new_store.store_location=loc
        new_store.store_address_1=add1
        new_store.store_address_2=add2
        new_store.store_address_3=add3
        new_store.store_person_name=person
        new_store.useridnew=useridnew
        new_store.active=True
        DBS_JistBuying.add(new_store)
        DBS_JistBuying.flush()

    @expose('jistdocstore.templates.logistics.editstores_location')
    def edit_stores_location(self,locid, **kw):
        storelocation = DBS_JistBuying.query(JistBuyingStoresLocation). \
                filter(JistBuyingStoresLocation.id==locid). \
                one()
        storelocation.store_name

        #print supplierone
        return dict(page='Edit Stores Location',
                    storelocation = storelocation,
                    )

    @expose()
    def saveeditstores(self,*arg,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        div = DBS_JistBuying.query(JistBuyingStoresLocation). \
                filter(JistBuyingStoresLocation.id==kw['store_id_edit']). \
                one()
        div.store_name= kw['store_name_edit']
        div.store_location = kw['store_location_edit'] #MySQL column has date format, change then uncomment
        div.store_address_1 = kw['store_address_1_edit']
        div.store_address_2 = kw['store_address_2_edit']
        div.store_address_3 = kw['store_address_3_edit']
        div.store_person_name = kw['store_person_name_edit']
        div.active = kw['storeactive']

    @expose()
    #@validate(ajax_form)
    def do_search_supplier(self,sitename, **kw):
        #sitename = "%(supplier_name)s" % kw
        searchphrase = "%"+sitename+"%"
        #print searchphrase
        #contract = DBS_ContractData.query(JistContracts).filter(JistContracts.site.like(searchphrase)). \
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.suppliername.like(searchphrase)). \
                        order_by(desc(JistBuyingSupplierList.id)).all()
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>ID</th>
                    <th>Supplier Name </th>
                    <th>Acc Number </th>
                    <th>Address</th>
                    <th>City</th>
                    <th>Fax</th>
                    <th>Phone</th>
                    <th>Contact</th>
                    <th>Active</th>
                    """
        sitedata = sitedata + headerdata
        for k in supplier:
            sitedatatemp = """<tr><td><a href='/logisticscont/edit_buying_supplier/%s'>%s</a>
                            </td><td>%s</td><td>%s</td><td>%s</td>
                            <td>%s</td><td>%s</td><td>%s</td>
                            <td>%s</td><td>%s</td><p/></tr>
                            """ % (k.id,k.id,k.suppliername,
                                    k.accnumber,k.address,
                                   k.city,k.fax,k.phone,k.contact,k.active)
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.grv_search')
    def search_grv(self,**named):
        """Handle the 'sitesearch' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=SupplierComboSearch(),
                    target="output",
                    action="do_search_open_orders_grv")

        tmpl_context.form = ajax_form 

        return dict(page='GRV - Open Orders',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_open_orders_grv_old(self, **kw):
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
        suppliercode = "%(supplier_name)s" % kw
        #contract = DBS_ContractData.query(JistContracts).filter(JistContracts.site.like(searchphrase)). \
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==int(suppliercode)). \
                      filter(JistBuyingOrderList.podate>=startdate). \
                      filter(JistBuyingOrderList.podate<=enddate). \
                     order_by(desc(JistBuyingOrderList.id)). \
                     all()
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==suppliercode). \
                      filter(JistBuyingOrderList.podate>=startdate). \
                      filter(JistBuyingOrderList.podate<=enddate). \
                     value(func.sum(JistBuyingOrderList.totalexcl))

        supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()
        #for k in supn:
        #    print k
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        #print openorders_total
        #return
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        supplier_text = "<H3 align='center'> Purchase Orders to %s for period from: %s to  %s</H3><p/>"%(suppliername,datestart,dateend)
        pdfstuff = ""
        #"""
        #if openorders_total:
        #    pdf1 = """<div class=sidebar_total_excl>
        #                Total Excl Vat: R %s
        #           """%("0.00")
        #    pdf2 = """
        #                <a
        #                href='/logisticscont/export_purchase_orders_pdf/%s/%s'><p/> 
        #                Export to PDF</a>
        #           """%(startdate,enddate)
        #    pdf3 = """
        #                </div>
        #                <p/>
        #            """
        #    pdfstuff = pdf1+pdf2+pdf3
        #else:
        #    pdf1 = """<div class=sidebar_total_excl>
        #                Total Excl Vat: R %s
        #           """%("0.00")
        #    pdf3 = """
        #                </div>
        #                <p/>
        #            """
        #    pdfstuff = pdf1+pdf3
        #"""
        sitedata = "<table class='tablestandard'>"
        headerdata = """
                    <th>Purchase Order Number </th>
                    <th>Purchase Date</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/logisticscont/grv_order_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.ponumber,
                                    k.podate
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.order_vs_grv_search')
    def search_open_orders_vs_grv_old(self,**named):
        """Handle the 'sitesearch' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=SupplierComboSearch(),
                    target="output",
                    action="do_search_open_orders_vs_grv")

        tmpl_context.form = ajax_form 

        return dict(page='Open Orders By Date & Supplier',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.grv_order_one')
    def grv_order_one(self,ordernumber,**named):
        order = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==ordernumber). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==order.suppliercode). \
                        one()

        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==ordernumber). \
                all()
        return dict(page='GRV Open Order: ' + order.ponumber,
                    poorder = order,
                    poitems = poitems,
                    currentPage=1,
                    supplier = supplier.suppliername,
                    value=named,
                    value2=named)

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.grv_item_one')
    def grv_item_one(self,itemid,poid,**named):
        tmpl_context.form = edit_grv_form 
        #tmpl_context.form = AddNewPurchaseGRV 
        order = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==poid). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==order.suppliercode). \
                        one()
        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.id==itemid). \
                one()
        grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                join(JistBuyingOrderItems). \
                filter(JistBuyingGRV.buyingitemid==poitems.id). \
                all()
        grvitemsqtytotal = DBS_JistBuying.query(JistBuyingGRV). \
                filter(JistBuyingGRV.buyingitemid==poitems.id). \
                value(func.sum(JistBuyingGRV.grvqty))
        if grvitemsqtytotal:
            grvbalance = int(poitems.quantity) - int(grvitemsqtytotal)
        else:
            grvitemsqtytotal = 0
            grvbalance = int(poitems.quantity) - int(grvitemsqtytotal)
        return dict(page='Open Order: '+ order.ponumber,
                    wip = '',
                    poorder = order,
                    poitems = poitems,
                    grvitems = grvitems,
                    grvitemqtytotal = grvitemsqtytotal,
                    grvbalance = grvbalance,
                    currentPage=1,
                    supplier = supplier.suppliername,
                    action="/logisticscont/do_get_grv_save/"+itemid+'/'+poid,
                    value2=named)

    @expose()
    #@validate(edit_grv_form)
    def do_get_grv_save(self,*arg, **kw):
        new_grv = JistBuyingGRV()
        new_grv.buyingitemid = arg[0]
        new_grv.grvdate = kw['Delivery_Date']
        new_grv.grvdelnum = kw['grvdelnum']
        new_grv.grvqty = kw['grvqty']
        new_grv.in_store = kw['In_Store']
        new_grv.active = 1 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        new_grv.useridnew = usernow.user_id
        DBS_JistBuying.add(new_grv)
        DBS_JistBuying.flush()
        redirect('/logisticscont/grv_item_one/'+arg[0]+'/'+arg[1])

    @expose()
    #@validate(ajax_form)
    def do_search_open_orders_vs_grv(self, **kw):
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
        suppliercode = "%(supplier_name)s" % kw
        #print suppliercode
        #contract = DBS_ContractData.query(JistContracts).filter(JistContracts.site.like(searchphrase)). \
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==int(suppliercode)). \
                      filter(JistBuyingOrderList.podate>=startdate). \
                      filter(JistBuyingOrderList.podate<=enddate). \
                     order_by(desc(JistBuyingOrderList.id)). \
                     all()
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==suppliercode). \
                      filter(JistBuyingOrderList.podate>=startdate). \
                      filter(JistBuyingOrderList.podate<=enddate). \
                     value(func.sum(JistBuyingOrderList.totalexcl))

        supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()
        #for k in supn:
        #    print k
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        #print openorders_total
        #return
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        supplier_text = "<H3 align='center'> Purchase Orders to %s for period from: %s to  %s</H3><p/>"%(suppliername,datestart,dateend)
        if openorders_total:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/logisticscont/export_purchase_orders_pdf/%s/%s'><p/> 
                        Export to PDF</a>
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
        sitedata = "<table class='tablestandard'>"
        headerdata = """
                    <th>Purchase Order Number </th>
                    <th>Purchase Date</th>
                    <th>Total Excl</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/logisticscont/purchase_order_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <td align='right'>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.ponumber,
                                    k.podate,totalexcl
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.requistion_search')
    def search_requisitions(self,**named):
        """Handle the 'sitesearch' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=SupplierComboSearch(),
                    target="output",
                    action="do_search_open_orders_grv")

        tmpl_context.form = ajax_form 

        return dict(page='requisitionsearch',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @require(in_any_group("managers","logistics","logistics_manager"))
    @expose('jistdocstore.templates.logistics.requisitionsopen')
    def purchase_requisition_open(self,**named):
        """Handle the 'sitesearch' page."""
        #contract = DBS_JistBuying.query(JistBuyingPurchaseReqsList).all() # \
        #            #filter(JistBuyingPurchaseReqsList.active==False).all()
        #username = request.identity['repoze.who.userid']
        ##for i in contract:
        ##    print i.jcno, i.prefered_supplier
        #usernow = User.by_user_name(username)
        tmpl_context.widget = spx_open_purchase_reqs 
        value = openpurchasereq_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print currentPage
        #print currentPage.page
        #print currentPage.previous_page
        #contracttsksreplies = DBS_ContractData.query(SiteDiaryContracts). \
        #           filter(SiteDiaryContracts.jcno==jno_id). \
        #           order_by(desc(SiteDiaryContracts.datecreated)).all()
        #contractcount = len(contracttsksreplies) 
        #page =int( named.get( 'page', '1' ))
        #contract_currentPage = paginate.Page(
        #    contracttsksreplies, page, item_count=contractcount,
        #    items_per_page=5,
        #)
        #sitediaryitems = contract_currentPage.items
        #tmpl_context.widget = add_new_sitediary_form
        return dict(page='Open Requisitions Buying Side',
                    wip = items,
                    thiscurrentPage=currentPage,
                    count=count
                    )


    @require(in_any_group("managers", "logistics"))
    #@validate(add_new_purchase_req,purchase_requisition_new)
    @expose()
    def addpurchasereq(self,*args,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newreq = JistBuyingPurchaseReqsList(
                jcno = kw['jcno'],
                prefered_supplier =kw['prefered_supplier'],
                must_have_date =kw['must_have_date'],
                useridnew = usernow.user_id
        )
        DBS_JistBuying.add(newreq)
        DBS_JistBuying.flush()
        self.current_purchase_req_id = newreq.id 
        #current_purchase_req_id = 5 
        #print "Current Purchase Req is %s"%str(current_purchase_req_id)
        redirect('/logisticscont/purchase_requisition_items_add/'+str(newreq.id))

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.logistics.requisition_items_add')
    def purchase_requisition_items_add(self,reqid=None,**named):
        """Handle the 'sitesearch' page."""
        #ajax_form = AjaxForm(id="myAjaxForm",
        #            fields=AddNewPurchaseReqItem(),
        #            target="output",
        #            action="do_add_req_items")

        #tmpl_context.form = ajax_form 
        tmpl_context.form = add_new_purchase_req_item 
        reqs = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.reqid==str(reqid)). \
                     order_by(asc(JistBuyingPurchaseReqsItems.id)). \
                     all()

        return dict(page='Add Purchase Requisition Items',
                    wip = '',
                    currentPage=1,
                    value=named,
                    reqs = reqs,
                    action='/logisticscont/do_add_req_items/'+reqid
                    )

    @expose()
    #@validate(ajax_form)
    #@validate(add_new_purchase_req_item,purchase_requisition_items_add)
    def do_add_req_items(self,reqid=None, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        #print current_purchase_req_id
        #print kw['item']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newreqitem = JistBuyingPurchaseReqsItems()
        newreqitem.reqid = reqid
        newreqitem.item = kw['item']
        newreqitem.description =kw['description']
        newreqitem.unit =kw['unit']
        newreqitem.quantity =kw['quantity']
        #newreqitem.price =kw['price']
        #newreqitem.total =kw['total']
        newreqitem.useridnew = usernow.user_id
        DBS_JistBuying.add(newreqitem)
        DBS_JistBuying.flush()
        reqs = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.reqid==str(reqid)). \
                     order_by(asc(JistBuyingPurchaseReqsItems.id)). \
                     all()
        #global current_purchase_req_items
        self.current_purchase_req_items = []
        for k in reqs:
            self.current_purchase_req_items.append([str(k.item),str(k.description),str(k.unit),str(k.quantity)])
        redirect('/logisticscont/purchase_requisition_items_add/'+str(reqid))

    @require(in_any_group("managers", "logistics"))
    @expose('jistdocstore.templates.logistics.requisition_one')
    def requisition_one(self,reqid):
        #username = request.identity['repoze.who.userid']
        reqone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                filter(JistBuyingPurchaseReqsList.id==reqid).one()
        userthen = User.by_user_id(reqone.useridnew)
        items = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                filter(JistBuyingPurchaseReqsItems.reqid==reqid).all()
        #global current_purchase_req_id  
        #current_purchase_req_id = newreq.id 
        return dict(page='Purchase Requisition',
                    cont = reqone,
                    currentPage=1,
                    username=userthen.user_name,
                    items=items
                    )

    @expose()
    def close_req_items(self,reqid):
        req = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.id==str(reqid)). \
                     one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        req.dateclosed = datetime.date(datetime.now())
        redirect('/logisticscont/mypurchasereqs')

    @require(in_any_group("managers", "buying_manager","accounts_manager"))
    @expose('jistdocstore.templates.logistics.requisition_buying_one')
    def requisition_buying_one(self,*arg,**named):
        if not arg[0] == "clearshoppingcart":
            reqone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                    filter(JistBuyingPurchaseReqsList.id==int(arg[0])).one()
            userthen = User.by_user_id(reqone.useridnew)
            items = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                    filter(JistBuyingPurchaseReqsItems.reqid==arg[0]).all()
        return dict(page='Purchase Requisition Buying Side',
                    cont = reqone,
                    currentPage=1,
                    username=userthen.user_name,
                    items=items,
                    value = arg[0],
                    action="/logisticscont/clearshoppingcart/"+arg[0],
                    current_shopping_items= session["mysession"],
                    came_from = "/logisticscont/requisition_buying_one/"+arg[0]
                    )

    @expose()
    def clearshoppingcart(self,*arg,**kw):
        session["mysession"] = []
        session.save()
        redirect('/logisticscont/requisition_buying_one/'+arg[0])

    @expose()
    def add_req_item_to_current_shopping_items(self,reqid,itemid,**kw):
        #global current_purchase_req_id  
        #current_purchase_req_id = newreq.id 
        #for k,w in enumerate(kw):
        #    print k,w
        items = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                filter(JistBuyingPurchaseReqsItems.id==itemid).one()
        #print current_purchase_req_id
        #print kw['item']
        #global current_shopping_items
        session["mysession"].append([items.id,items.item,items.description,items.unit,items.quantity])
        session.save()
        redirect('/logisticscont/requisition_buying_one/'+reqid)
        
    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.logistics.mypurchase_requisitions')
    def mypurchasereqs(self,**named):
        """Handle the 'mypurchasereq' page."""
        tmpl_context.widget = spx_purchase_reqs 
        value = mypurchasereq_filler.get_value(values={},offset=0,order_by='id',desc=True)
        count = len(value) 
        page =int( named.get( 'page', '1' ))
        currentPage = paginate.Page(
            value, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        #print currentPage
        #print currentPage.page
        #print currentPage.previous_page
        return dict(page='My Purchase Requisitions',
                    wip = items,
                    thiscurrentPage=currentPage,
                    count=count)

    @require(in_any_group("managers", "buying_manager","accounts_manager"))
    @expose('jistdocstore.templates.logistics.purchase_order_one')
    def purchase_order_one(self,orderid,**named):
        orderlist = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==orderid).one()
        orderitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==orderid).all()
        supptemp = DBS_JistBuying.query(JistBuyingSupplierList).filter(JistBuyingSupplierList.id==orderlist.suppliercode).one()
        #for k in orderitems:
        #    print k.description, k.total
        #return
        #userthen = User.by_user_id(reqone.useridnew)
        #items = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
        #        filter(JistBuyingPurchaseReqsItems.reqid==reqid).all()
        #global current_purchase_req_id  
        #current_purchase_req_id = newreq.id 
        return dict(page='Purchase Order One: ' + orderlist.ponumber,
                    cont = orderlist,
                    supplier = supptemp.suppliername,
                    poitems = orderitems,
                    poorder = orderlist,
                    currentPage=1,
                    #username=userthen.user_name,
                    items=orderitems,
                    current_shopping_items = session["mysession"]
                    )

    @require(in_any_group("managers", "buying_manager","accounts_manager"))
    @expose('jistdocstore.templates.logistics.purchaseorder_new')
    def purchase_order_new(self,**named):
        tmpl_context.form = add_new_purchase_order 
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=TrolleyOptions(),
                    target="output",
                    )
        tmpl_context.form = ajax_form 

        return dict(page='New Purchase Order',
                    wip = '',
                    currentPage=1,
                    value=named,
                    current_shopping_items= session["mysession"],
                    action = "/logisticscont/addpurchaseorder",
                    value2=named)

    @require(in_any_group("managers", "buying_manager","accounts_manager"))
    @expose('jistdocstore.templates.logistics.search_purchase_order')
    def search_purchase_order(self,**named):
        """Handle the 'myoutofoffice' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=SearchPurchaseOrderDate(),
                    target="output",
                    action="do_search_purchase_order")
        tmpl_context.form = ajax_form 
        #tmpl_context.form = add_new_reception_message

        return dict(page='Purchase Orders Search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    #@validate(ajax_form)
    def do_search_purchase_order(self, **kw):
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
        #orderlist = DBS_JistBuying.query(JistBuyingOrderList). \
        #        filter(JistBuyingOrderList.id==orderid).one()
        #orderitems = DBS_JistBuying.query(JistBuyingOrderItems). \
        #        filter(JistBuyingOrderItems.ponumber==orderid).all()
        purchase_orders = DBS_JistBuying.query(JistBuyingOrderList).filter(JistBuyingOrderList.podate>=startdate). \
                                              filter(JistBuyingOrderList.podate<=enddate). \
                                              order_by(desc(JistBuyingOrderList.id)).  \
                                              all()
        purchase_orders_sum = DBS_JistBuying.query(JistBuyingOrderList).filter(JistBuyingOrderList.podate>=startdate). \
                                              filter(JistBuyingOrderList.podate<=enddate). \
                         value(func.sum(JistBuyingOrderList.totalexcl))
        locale.setlocale(locale.LC_ALL, '')
        #print purchase_orders_sum
        #return
        if purchase_orders_sum is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(purchase_orders_sum,format='#,##0.00;-#0.00',locale='en')
        datestart = str(tup[0])+'-'+str(tup[1])+'-'+str(tup[2]) 
        dateend = str(endtup[0])+'-'+str(endtup[1])+'-'+str(endtup[2]) 
        supplier_text = "<H3 align='left'> Purchase Orders from: %s to  %s</H3><p/>"%(datestart,dateend)
        if purchase_orders_sum:
            pdf1 = """<div class=sidebar_total_excl>
                        Total Excl Vat: R %s
                   """%(totalexcl)
            pdf2 = """
                        <a
                        href='/logisticscont/export_purchase_orders_pdf/%s/%s'><p/> 
                        Export to PDF</a>
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

        table = "<table class='tablecontractdata'>"
        headerdata = """
                    <th>Date </th>
                    <th>PO Number </th>
                    <th>Supplier </th>
                    <th>Total Excl</th>
                    <th>Total Vat</th>
                    <th>Total Incl</th>
                    """
        sitedata = supplier_text +pdfstuff + table + headerdata 
        for k in purchase_orders:
            tr = "<tr class='tablestandard'>"
            #sitedatatemp = "<img src='/images/staffpics/%s.png'/></td>"%str(k.for_user)
            supptemp = DBS_JistBuying.query(JistBuyingSupplierList).filter(JistBuyingSupplierList.id==k.suppliercode).one()
            transdate =""" 
                            <td>%s</td>
                            """%(k.podate)
            ponumber =""" 
                            <td>
                        <a href='/logisticscont/purchase_order_one/%s'>
                        %s</a> 
                            </td>
                            """%(k.id,k.ponumber)
            fromperson =""" 
                            <td>%s</td>
                            """%(supptemp.suppliername)
            callback =""" 
                            <td align=right>%s</td>
                            """%(k.totalexcl)
            callagain =""" 
                            <td align=right>%s</td>
                            """%(k.totalvat)
            nomsgs =""" 
                            <td align=right>%s</td>
                            """%(k.totalincl)
            trclose   ="""
                        </tr>
                       """
            sitedata = sitedata+"</p>"+tr+transdate+ponumber+ \
                    fromperson+callback+callagain+nomsgs+ \
                    trclose
        sitedata = sitedata+"</table>"
        return sitedata 

    #@validate(add_new_purchase_order,error_handler=purchase_order_new)
    @expose()
    def addpurchaseorder(self,*args,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        #status = DBS_ContractData.querydd(JistContractStatus).filter(JistContractStatus.jno==kw['id']).one()
        #print args
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        neworder = JistBuyingOrderList()
        neworder.podate = kw['podate'],
        neworder.suppliercode = kw['suppliercode'],
        neworder.datecreated = datetime.now()
        neworder.useridnew = usernow.user_id
        #DBS_JistBuying.add(newreq)
        #DBS_JistBuying.flush()
        #global current_purchase_order_id  
        self.current_purchase_order_id = neworder.id 
        #redirect('/logisticscont/purchase_order_items_add')
        redirect('/logisticscont/get_thisorderitems_from_currentreq')

    @expose('jistdocstore.templates.logistics.edit_purchase_order_one')
    def edit_purchase_order_one(self,*arg,**named):
        val = edit_purchase_order_filler.get_value(values={'id':int(arg[0])})
        tmpl_context.form = edit_purchase_order 
        orderlist = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==arg[1]).one()
        orderitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.id==arg[0]).one()
        supptemp = DBS_JistBuying.query(JistBuyingSupplierList).filter(JistBuyingSupplierList.id==orderlist.suppliercode).one()
        return dict(page='Edit Purchase Order: '+arg[1],
                   action='/logisticscont/saveeditpurchase_order/'+str(arg[0])+'/'+str(arg[1]),
                   userid = str(arg[0]),
                   supplier = supptemp.suppliername,
                   poitems = orderitems,
                   poorder = orderlist,
                   value=val
                   )

    @expose()
    def saveeditpurchase_order(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        ot = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.id==arg[0]).one()
        ot.contract = kw['contract']
        ot.description = kw['description']
        ot.unit = kw['unit']
        #if kw['quantity']:
        if isnumeric(kw['quantity']):
            qty = kw['quantity']
        else:
            qty = 0
        if isnumeric(kw['priceexcl']):
            pricex = kw['priceexcl']
        else:
            pricex = 0
        ot.quantity = float(qty) 
        ot.priceexcl = float(pricex) 
        TotalExcl = float(qty) * float(pricex) 
        ot.totalexcl = TotalExcl
        ot.dateedited = datetime.now()
        ot.useridedited = usernow.user_id
        redirect("/logisticscont/purchase_order_one/" +str(arg[1]))

    @expose('jistdocstore.templates.logistics.search_po_description')
    def search_po_description(self,**named):
        """Handle the 'sitesearch' page."""
        ajax_form = AjaxForm(id="myAjaxForm",
                    fields=POItemSearch(),
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

        return dict(page='Description Item Search',
                    wip = '',
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def export_purchase_orders_pdf(self,startdate,enddate):
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
        purchase_orders = DBS_JistBuying.query(JistBuyingOrderList).filter(JistBuyingOrderList.podate>=startdate). \
                                              filter(JistBuyingOrderList.podate<=enddate). \
                                              order_by(desc(JistBuyingOrderList.podate)).  \
                                              all()
        purchase_orders_sum = DBS_JistBuying.query(JistBuyingOrderList).filter(JistBuyingOrderList.podate>=startdate). \
                                              filter(JistBuyingOrderList.podate<=enddate). \
                         value(func.sum(JistBuyingOrderList.totalexcl))
        locale.setlocale(locale.LC_ALL, '')
        if not purchase_orders_sum:
            totalexcl = 0
        totalexcl = format_decimal(purchase_orders_sum,format='#,##0.00;-#0.00',locale='en')
        for k in purchase_orders:
            #fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
            supptemp = DBS_JistBuying.query(JistBuyingSupplierList).filter(JistBuyingSupplierList.id==k.suppliercode).one()
            wip1.append({'podate':k.podate,
                         'ponumber':k.ponumber,
                         'suppliercode':supptemp.suppliername,
                         'totalexcl':k.totalexcl,
                         'totalvat':k.totalvat,
                         'totalincl':k.totalincl
                         })
        count = len(wip1) 
        #for k in wip1:
        #    print k
        #pointperson_name = User.by_user_id(point).user_name
        userdata.append([datetime.date(datetime.now()),
            "Purchase Orders From: %s to %s"%(startdate,enddate),
                        ""
                        ])
        headers =["Date","PO Number","Supplier","Total Excl","Total Vat","Total Incl"]
        headerwidths=[100,150,200,100,100,100]
        pdffile.CreatePDFPurchaseOrdersTime(userdata,wip1,headers,headerwidths,totalexcl)
        #return
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    #@validate(add_new_purchase_item,error_handler=purchase_order_items_add)
    @expose('jistdocstore.templates.logistics.purchase_order_items_add')
    #@validate(ajax_form)
    def get_thisorderitems_from_currentreq(self, **named):
        from_data = []
        for k in session["mysession"]:
            from_data.append([str(k[0]),str(k[2])])
        to_data = []
        item_selector = ItemSelector(divID='item_selector_div', width=850,
                                 url='/logisticscont/save_purchase_order_items_add',
                                 fieldLabel='',
                                 labelWidth=0,
                                 fromData=from_data,
                                 toData=to_data,
                                 msWidth=300,
                                 msHeight=300,
                                 dataFields=['code','desc','cons','cons'],
                                 valueField='code',
                                 displayField='desc',
                                 fromLegend='Available',
                                 toLegend='Selected',
                                 submitText='Save',
                                 resetText='Reset')
        tmpl_context.widget = item_selector 
        return dict(page='Add Purchase Order Items',
                    currentPage=1,
                    count=1,
                    value=named,
                    )

    @expose()
    def save_purchase_order_items_add(self,*arg,**kw):
        #for m in arg:
        #    print m
        #for k,w in enumerate(kw):
        #    print k,w
        #print "Got here"
        #print kw['itemselector']
        redirect('/logisticscont/get_thisorderitems_from_currentreq')


    @expose('jistdocstore.templates.logistics.purchase_order_items_add')
    def purchase_order_items_add(self,**named):
        """Handle the 'sitesearch' page."""
        #ajax_form = AjaxForm(id="myAjaxForm",
        #            fields=AddNewPurchaseOrderItem(),
        #            target="output",
        #            action="do_search_order_items")

        #tmpl_context.form = ajax_form 
        tmpl_context.form = add_new_purchase_item 

        return dict(page='Add Purchase Order Items',
                    wip = '',
                    currentPage=1,
                    value=named,
                    )

    @expose()
    #@validate(add_new_purchase_item,error_handler=purchase_order_items_add)
    #@validate(ajax_form)
    def do_search_order_items(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        #print current_purchase_req_id
        #print kw['item']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        redirect('/logisticscont/purchase_order_items_add')

#####################################################################################################
############New BuyingAsync##########################################################################
#####################################################################################################
    def getUserRightsLogistics(self,user_id,haspermission):
        user = User.by_user_id(point.user_id)
        userpermissions = user.permissions
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='productionmanage':
                pointlist.append({'user_id':point.user_id,
                                  'user_name':point.user_name,
                                  'display_name':point.display_name
                                  })

    @expose()
    def getPurchase_orders_for_jcno(self,jcno,**kw):
        ot = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.contract.like(jcno)). \
                order_by(desc(JistBuyingOrderItems.id)).all()
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>ID</th>
                    <th>Date </th>
                    <th>PO Number </th>
                    <th>Req ID</th>
                    <th>Contract</th>
                    <th>Supplier</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total Excl</th>
                    """
        sitedata = sitedata + headerdata
        for k in ot:
            sitedatatemp = """<tr><td><a href='/productioncont/get_one/%s'>%s</a></td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <p/></tr>
                            """ % (k.id,k.id,k.podate,k.ponumber,k.reqid,
                                   k.contract,k.suppliercode,k.description,
                                   k.unit,k.quantity,k.priceexcl,k.totalexcl)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.logistics.requisitionnew')
    def purchase_requisition_new(self,**named):
        """Handle the 'requistion new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        return dict(page='New Purchase Requisition',
                    wip = contracts,
                    suppliers = supplierlist,
                    newreqitemfields = self.newreqitemfields,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.logistics.supplier_edit')
    def edit_buying_supplier(self,suppid):
        supplierone = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.id==suppid). \
                one()
        #print supplierone
        return dict(page='Edit Existing Supplier',
                    supplier = supplierone,
                    )

    @expose()
    def save_edit_buying_supplier(self,**kw):
        #for k,w in kw.iteritems():
        #    print k,w
        #return
        suppone = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.id==kw["supplierid_edit"]). \
                one()
        suppone.suppliername = kw["suppliername_edit"]
        suppone.accnumber = kw["supplieraccno_edit"]
        suppone.address = kw["supplieraddress_edit"]
        suppone.city = kw["suppliercity_edit"]
        suppone.fax = kw["supplierfax_edit"]
        suppone.phone = kw["supplierphone_edit"]
        suppone.contact = kw["suppliercontact_edit"]
        suppone.active = kw["supplieractive_edit"]
        #redirect('/logisticscont/search_supplier')
        return

    @expose()
    def purchase_reqs_per_jcno(self,jcno):
        reqslist = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.jcno==jcno). \
                     filter(JistBuyingPurchaseReqsList.active==False). \
                     order_by(asc(JistBuyingPurchaseReqsList.id)). \
                     all()
        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.jcno==int(jcno)). \
                     filter(JistBuyingPurchaseReqsItems.active==True). \
                     order_by(desc(JistBuyingPurchaseReqsItems.id)). \
                     all()
        sitedata = """
                    

               <h2 class="effect6">
               <span class='spanleft'>All Requisitioned Items  for JCNo: %s </span>
                <span class='spanright'>
               </span>
               </h2>

                   <table id='purchase_req_contract_all_table' class='tablesinglepoint'>

                    
                   """%jcno
        headerdata = """
                    <th>ID</th>
                    <th>JCNo  </th>
                    <th>Req Number</th>
                    <th>BudgetID</th>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Req By</th>
                    <th>PO-No</th>
                    """
        sitedata = sitedata + headerdata
        for k in reqsitems:
            usernow = User.by_user_id(k.useridnew)
            sitedatatemp = """<tr>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <p/></tr>
                            """ % (k.id,k.jcno,k.reqid,
                                   k.budgetid,k.item,k.description,
                                   k.unit,k.quantity,usernow.display_name,k.poid)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def purchase_reqs_items_per_user(self,usrid):
        reqslist = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.useridnew==int(usrid)). \
                     filter(JistBuyingPurchaseReqsList.active==True). \
                     order_by(asc(JistBuyingPurchaseReqsList.id)). \
                     all()
        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.useridnew==int(usrid)). \
                     filter(JistBuyingPurchaseReqsItems.useractive==True). \
                     order_by(desc(JistBuyingPurchaseReqsItems.id)). \
                     all()
        userme = User.by_user_id(int(usrid))
        sitedata = """
               <h2 class="effect6">
               <span class='spanleft'>All Requisitioned Items  for User: %s </span>
                <span class='spanright'>
               </span>
               </h2>
                   <table id='purchase_req_user_all_table' class='tablesinglepoint'>
                   """%userme.user_name
        headerdata = """
                    <th>ID</th>
                    <th>JCNo  </th>
                    <th>Req No</th>
                    <th>Budget Description</th>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Req By</th>
                    <th>Notes</th>
                    <th>In Buying</th>
                    <th>PO Number</th>
                    <th>GRV Qty</th>
                    <th>Delete</th>
                    """
        sitedata = sitedata + headerdata
        for k in reqsitems:
            budgetname = ''
            usernow = User.by_user_id(k.useridnew)
            notes = DBS_JistBuying.query(JistBuyingPurchaseReqsNotes). \
                         filter(JistBuyingPurchaseReqsNotes.reqitemid==k.id). \
                         filter(JistBuyingPurchaseReqsNotes.active==True). \
                         order_by(desc(JistBuyingPurchaseReqsNotes.id)). \
                         all()
            notehtml = ''
            if notes:
                for note in notes:
                    if note.useridnew:
                        userthis = User.by_user_id(note.useridnew)
                        htmltemp = """%s: %s \n %s \n\r"""%(userthis.display_name,note.dateadded,note.note)
                        notehtml = notehtml + htmltemp 
            try:
                budgetitem = DBS_ContractData.query(JistContractBudget). \
                                filter(JistContractBudget.id==k.budgetid). \
                                one()
                budgetname = budgetitem.budget_description
            except:
                budgetname = ''
            if k.poid:
                grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                        join(JistBuyingOrderItems). \
                        filter(JistBuyingGRV.buyingitemid==k.poitemid). \
                        all()
                grvitemsqtytotal = DBS_JistBuying.query(JistBuyingGRV). \
                        filter(JistBuyingGRV.buyingitemid==k.poitemid). \
                        value(func.sum(JistBuyingGRV.grvqty))
                if grvitemsqtytotal:
                    grvbalance = Decimal(k.quantity) - Decimal(grvitemsqtytotal)
                else:
                    if k.quantity == '': k.quantity = 0
                    grvitemsqtytotal = 0
                    grvbalance = Decimal(k.quantity) - Decimal(grvitemsqtytotal)
            else:
                grvitemsqtytotal = 0

            sitedatatemp = """<tr>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td width='200px'>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td width='25px'>
                                        <img id="addtocontractscope"
                                        title="%s" src="/images/notes_32.png" >
                                        </img>
                                </td>
                                <td width='25px'>
                                %s
                                </td>
                                <td width='25px'>
                                %s
                                </td>
                                <td width='25px'>
                                %s
                                </td>
                                <td width='25px'>
                                        <img id="deleteitem"
                                        src="/images/trash.png" >
                                        </img>
                                </td>
                                <p/></tr>
                            """ % (k.id,k.jcno,k.reqid,
                                   budgetname,k.item,k.description,
                                   k.unit,k.quantity,usernow.display_name,notehtml,
                                   self.producehtml_inbuying(k.buyingactive),
                                   k.poid,grvitemsqtytotal)
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 
    
    def producehtml_inbuying(self,state):
        if state:
            html = """<img id="addtocontractscope"
            src="/images/dialog-yes.png" >
            </img>"""
        else:
            html = """<img id="addtocontractscope"
            src="/images/dialog-no.png" >
            </img>"""

        return html

    @expose()
    def ajaxDeactivateBuyingSideReq(self,uniqid,reqitemid):
        #print reqitemid
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==reqitemid). \
                     one()
        reqsitem.buyingactive = False
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        html = """Action: %s removed item from buying."""%(usernow.display_name)
        newnote = JistBuyingPurchaseReqsNotes()
        newnote.reqitemid = reqitemid 
        newnote.note = self.safe(html)
        newnote.useridnew = usernow.user_id
        newnote.dateadded = datetime.now()
        DBS_JistBuying.add(newnote)
        DBS_JistBuying.flush()
        return
        
    @expose()
    def ajaxToggleUserSideBuyingReq(self,reqitemid):
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==reqitemid). \
                     one()
        decisiontree = reqsitem.buyingactive
        reqsitem.buyingactive = not decisiontree 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        if decisiontree:
            #true
            html = """Action: %s removed item from buying."""%(usernow.display_name)
        else:
            #false
            html = """Action: %s moved item to buying."""%(usernow.display_name)

        newnote = JistBuyingPurchaseReqsNotes()
        newnote.reqitemid = reqitemid 
        newnote.note = self.safe(html)
        newnote.useridnew = usernow.user_id
        newnote.dateadded = datetime.now()
        DBS_JistBuying.add(newnote)
        DBS_JistBuying.flush()
        return

    @expose()
    def ajaxToggleUserActiveBuyingReq(self,reqitemid):
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==reqitemid). \
                     one()
        decisiontree = reqsitem.useractive
        reqsitem.useractive = not decisiontree 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        if decisiontree:
            #true
            html = """Action: %s deleted item ."""%(usernow.display_name)
        else:
            #false
            html = """Action: %s actived item."""%(usernow.display_name)
        newnote = JistBuyingPurchaseReqsNotes()
        newnote.reqitemid = reqitemid 
        newnote.note = self.safe(html)
        newnote.useridnew = usernow.user_id
        newnote.dateadded = datetime.now()
        DBS_JistBuying.add(newnote)
        DBS_JistBuying.flush()
        return
        
    @expose()
    def purchase_reqs_items_all_active(self):
        """
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='logisticsmanage':
                logged = True
        if not logged: return "Only for the Logistics Managers Eyes"
        """
        reqslist = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.active==True). \
                     order_by(asc(JistBuyingPurchaseReqsList.id)). \
                     all()
        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.buyingactive==True). \
                     order_by(desc(JistBuyingPurchaseReqsItems.id)). \
                     all()
        sitedata = """
                    
                    <p id="contractheader">
                    All Active Requisitioned Items  
                    </p>
                   <div id='purchase_req_contract_all_div'>
                   <table id='purchase_req_contract_all_table' class='tablesinglepoint'>
                   """
        headerdata = """
                    <th>ID</th>
                    <th>JCNo  </th>
                    <th>Must Have Date</th>
                    <th>Budget Description</th>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Req By</th>
                    <th>Active</th>
                    <th>Date Added</th>
                    <th ></th>
                    <th>Trolley</th>
                    <th>PO No</th>
                    <th>Notes</th>
                    <th>GRV</th>
                    """
        sitedata = sitedata + headerdata
        for k in reqsitems:
            budgetname = ''
            usernow = User.by_user_id(k.useridnew)
            try:
                budgetitem = DBS_ContractData.query(JistContractBudget). \
                                filter(JistContractBudget.id==k.budgetid). \
                                one()
                budgetname = budgetitem.budget_description
            except:
                budgetname = ''
            trolleyhtml = ''
            try:
                shoppingtrolley = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList).filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==k.id).one()
                #print shoppingtrolley.id                
                if shoppingtrolley.active:
                    trolleyhtml = """<img id="toggle_item_add" src="/images/shopping_basket_add_32.png"></img>"""
                else:
                    trolleyhtml = """<img id="toggle_item_delete" src="/images/shopping_basket_remove_32.png"></img>"""

            except:
                trolleyhtml = """<img id="toggle_item_delete" src="/images/shopping_basket_remove_32.png"></img>"""

            reqsone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                         filter(JistBuyingPurchaseReqsList.id==k.reqid). \
                         one()
            notes = DBS_JistBuying.query(JistBuyingPurchaseReqsNotes). \
                         filter(JistBuyingPurchaseReqsNotes.reqitemid==k.id). \
                         filter(JistBuyingPurchaseReqsNotes.active==True). \
                         order_by(desc(JistBuyingPurchaseReqsNotes.id)). \
                         all()
            notehtml = ''
            htmltemp = ''
            if notes:
                for note in notes:
                    if note.useridnew:
                        userthis = User.by_user_id(note.useridnew)
                        htmltemp = """%s: %s \n %s \n\r"""%(userthis.display_name,note.dateadded,note.note)
                        notehtml = notehtml + htmltemp +"<br/>" 
            sitedatatemp = """<tr>
                                <td>%s</td>
                                <td>%s</td>
                                <td width="70px">%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td width="25px" >
                                <img  id="req_by_user_all" title="%s" src="/images/staffpics/%s.png"></img>
                                </td>
                                <td width="25px"><img id="toggle_item_active"
                                src="/images/switch.png"></img>
                                </td>
                                <td width='80px'>%s</td>
                                <td class="tdspacer" width="35px">
                                </td>
                                <td width="25px" >
                                %s   
                                </td>
                                <td>
                                %s
                                </td>
                                <td width="25px" ><img id="toggle_item_add"
                                title="%s" src="/images/notes_32.png"></img>
                                </td>
                                <td width="25px" ><img id="grv_purchasereq_details"
                                src="/images/grv_32.png"></img>
                                </td>
                                <p/></tr>
                            """ % (k.id,k.jcno,reqsone.must_have_date,
                                   budgetname,k.item,k.description,
                                   k.unit,k.quantity,usernow.display_name,reqsone.useridnew,k.dateadded,trolleyhtml,k.poid,notehtml)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table></div>"
        return sitedata 

    @expose()
    def purchase_reqs_items_all_active_by_user(self,usridasked):
        """
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        user = User.by_user_id(usernow.user_id)
        userpermissions = user.permissions
        logged = False
        for permis in userpermissions:
            #print permis.permission_name
            if permis.permission_name=='logisticsmanage':
                logged = True
        if not logged: return "Only for the Logistics Managers Eyes"
        """
        reqslist = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.active==True). \
                     order_by(asc(JistBuyingPurchaseReqsList.id)). \
                     all()
        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.buyingactive==True). \
                     order_by(desc(JistBuyingPurchaseReqsItems.id)). \
                     all()
        sitedata = """
                    
                    <p id="contractheader">
                    All Active Requisitioned Items  
                    </p>
                   <table id='purchase_req_contract_all_table' class='tablesinglepoint'>
                   """
        headerdata = """
                    <th>ID</th>
                    <th>JCNo  </th>
                    <th>Must Have Date</th>
                    <th>Budget Description</th>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Req By</th>
                    <th>Active</th>
                    <th>Date Added</th>
                    <th ></th>
                    <th>Trolley</th>
                    <th>PO No</th>
                    <th>Notes</th>
                    <th>GRV</th>
                    """
        sitedata = sitedata + headerdata
        for k in reqsitems:
            budgetname = ''
            sitedatatemp = ''
            usernow = User.by_user_id(k.useridnew)
            #print k.useridnew, usridasked
            if k.useridnew == int(usridasked):
                #print k.useridnew, usridasked
                try:
                    budgetitem = DBS_ContractData.query(JistContractBudget). \
                                    filter(JistContractBudget.id==k.budgetid). \
                                    one()
                    budgetname = budgetitem.budget_description
                except:
                    budgetname = ''
                trolleyhtml = ''
                try:
                    shoppingtrolley = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList).filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==k.id).one()
                    #print shoppingtrolley.id                
                    if shoppingtrolley.active:
                        trolleyhtml = """<img id="toggle_item_add" src="/images/shopping_basket_add_32.png"></img>"""
                    else:
                        trolleyhtml = """<img id="toggle_item_delete" src="/images/shopping_basket_remove_32.png"></img>"""

                except:
                    trolleyhtml = """<img id="toggle_item_delete" src="/images/shopping_basket_remove_32.png"></img>"""

                reqsone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                             filter(JistBuyingPurchaseReqsList.id==k.reqid). \
                             one()
                sitedatatemp = """<tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td width="70px">%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td width="25px" >
                                    <img  id="req_by_user" title="%s" src="/images/staffpics/%s.png"></img>
                                    </td>
                                    <td width="25px"><img id="toggle_item_active"
                                    src="/images/switch.png"></img>
                                    </td>
                                    <td width='80px'>%s</td>
                                    <td class="tdspacer" width="35px">
                                    </td>
                                    <td width="25px" >
                                    %s   
                                    </td>
                                    <td>
                                    %s
                                    </td>
                                    <td width="25px" ><img id="toggle_item_add"
                                    src="/images/notes_32.png"></img>
                                    </td>
                                    <td width="25px" ><img id="grv_purchasereq_details"
                                    src="/images/grv_32.png"></img>
                                    </td>
                                    <p/></tr>
                                """ % (k.id,k.jcno,reqsone.must_have_date,
                                       budgetname,k.item,k.description,
                                       k.unit,k.quantity,usernow.display_name,reqsone.useridnew,k.dateadded,trolleyhtml,k.poid)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def purchase_reqs_trolley_all_active(self):
        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.active==True). \
                     order_by(desc(JistBuyingPurchaseReqsItemsShoppingList.id)). \
                     all()
        #reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
        #             filter(JistBuyingPurchaseReqsItems.buyingactive==True). \
        #             order_by(desc(JistBuyingPurchaseReqsItems.id)). \
        #             all()
        sitedata = """
                    <p id="contractheader">
                    All Active Shopping Trolley Items  
                    </p>
                    <div id="purchase_req_trolley_active_div">
                   <table id='purchase_req_trolley_all_table' class='tablesinglepoint'>
                   """
        headerdata = """
                    <th>ID</th>
                    <th>Item ID</th>
                    <th>JCNo  </th>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Req By</th>
                    <th>Date Added</th>
                    <th>Notes</th>
                    <th>Prices</th>
                    """
        sitedata = sitedata + headerdata
        for trolley in trolleylist:
            #usernow = User.by_user_id(trolley.useridnew)
            reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                         filter(JistBuyingPurchaseReqsItems.id==trolley.reqitemid). \
                         one()
            reqsone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                         filter(JistBuyingPurchaseReqsList.id==reqsitem.reqid). \
                         one()
            usernow = User.by_user_id(reqsone.useridnew)
            notes = DBS_JistBuying.query(JistBuyingPurchaseReqsNotes). \
                         filter(JistBuyingPurchaseReqsNotes.reqitemid==trolley.reqitemid). \
                         filter(JistBuyingPurchaseReqsNotes.active==True). \
                         order_by(desc(JistBuyingPurchaseReqsNotes.id)). \
                         all()
            notehtml = ''
            if notes:
                for note in notes:
                    if note.useridnew:
                        userthis = User.by_user_id(note.useridnew)
                        htmltemp = """%s: %s \n %s \n\r"""%(userthis.display_name,note.dateadded,note.note)
                        notehtml = notehtml + htmltemp + "</br>"
            if reqsitem.buyingactive:
                sitedatatemp = """<tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td width="25px" >
                                    <img  id="req_by_user" title="%s" src="/images/staffpics/%s.png"></img>
                                    </td>
                                    <td>%s</td>
                                    <td width="25px" ><img
                                    id="toggle_item_add" title="%s" src="/images/notes_32.png"></img>
                                    </td>
                                    <td width="25px" ><img id="toggle_shopping_prices"
                                    src="/images/prices_32.png"></img>
                                    </td>
                                    <p/></tr>
                                """ % (trolley.id,reqsitem.id,reqsitem.jcno,
                                       reqsitem.item,reqsitem.description,
                                       reqsitem.unit,reqsitem.quantity,usernow.user_name,reqsitem.useridnew,reqsitem.dateadded,notehtml)
                sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw

        sitedata = sitedata +"</table></div>"
        supp_prices = """<div id='active_shopping_req_prices_list'>
                        </div>
                      """
        return "<div id='active_shopping_trolley'></div>"+sitedata+supp_prices 

    @expose()
    def purchase_reqs_trolley_for_approval(self):
        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.active==True). \
                     order_by(desc(JistBuyingPurchaseReqsItemsShoppingList.id)). \
                     all()
        #reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
        #             filter(JistBuyingPurchaseReqsItems.buyingactive==True). \
        #             order_by(desc(JistBuyingPurchaseReqsItems.id)). \
        #             all()
        sitedata = """
                    <p id="contractheader">
                    Shopping Trolley For Approval  
                    </p>
                    <div id="purchase_req_trolley_approval_div">
                   <table id='purchase_req_trolley_for_approval' class='tablesinglepoint'>
                   """
        headerdata = """
                    <th>ID</th>
                    <th>Item ID</th>
                    <th>JCNo  </th>
                    <th>Must Have Date</th>
                    <th>Item</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Req By</th>
                    <th>Date Added</th>
                    <th>Notes</th>
                    <th>Budgets</th>
                    <th>Prices</th>
                    <th>De Activate</th>
                    """
        sitedata = sitedata + headerdata
        for trolley in trolleylist:
            reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                         filter(JistBuyingPurchaseReqsItems.id==trolley.reqitemid). \
                         one()
            shoppingpricescount = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                              filter(JistBuyingPurchaseReqsItemsShoppingPrices.shoppinglistid==trolley.reqitemid). \
                              value(func.count())
            reqsone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.id==reqsitem.reqid). \
                     one()
            usernow = User.by_user_id(reqsone.useridnew)
            notes = DBS_JistBuying.query(JistBuyingPurchaseReqsNotes). \
                         filter(JistBuyingPurchaseReqsNotes.reqitemid==trolley.reqitemid). \
                         filter(JistBuyingPurchaseReqsNotes.active==True). \
                         order_by(desc(JistBuyingPurchaseReqsNotes.id)). \
                         all()
            notehtml = ''
            if notes:
                for note in notes:
                    if note.useridnew:
                        userthis = User.by_user_id(note.useridnew)
                        htmltemp = """%s: %s \n %s \n\r"""%(userthis.display_name,note.dateadded,note.note)
                        notehtml = notehtml + htmltemp + "</br>"
            if reqsitem.buyingactive:
                sitedatatemp = """<tr>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td width="70px">%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td>%s</td>
                                    <td width="25px" ><img id="toggle_item_add"
                                    title="%s" src="/images/notes_32.png"></img>
                                    </td>
                                    <td width="25px" ><img id="toggle_shopping_prices"
                                    src="/images/emblem-money.png"></img>
                                    </td>
                                    <td>%s</td>
                                    <td width="25px" ><img
                                    id="toggle_shopping_active"
                                    src="/images/approve_not_32.png"></img>
                                    </td>
                                    <p/></tr>
                                """ % (trolley.id,reqsitem.id,reqsitem.jcno,reqsone.must_have_date,
                                       reqsitem.item,reqsitem.description,
                                       reqsitem.unit,reqsitem.quantity,usernow.display_name,reqsitem.dateadded,notehtml,shoppingpricescount)
                sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table></div>"
        supp_prices = """
                        <div id='active_shopping_req_prices_budget'>
                        </div>      
                        <div id='active_shopping_req_prices_list_approval'>
                        </div>
                        <div id='active_shopping_req_approval_compare'>
                        </div>
                        
                      """
        return "<div id='active_shopping_trolley_approval'>"+sitedata+"</div>"+supp_prices 

    @expose()
    def ajaxpurchase_reqs_get_quotation_prices(self,uniqid,itemid,**kw):
        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.id==int(itemid)). \
                     one()
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==trolleylist.reqitemid). \
                     one()
        reqsone = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.id==reqsitem.reqid). \
                     one()
        usernow = User.by_user_id(reqsone.useridnew)

        html = """
                        <form id="supp_shopping_quote_form">
                <fieldset>
                      <img  id="purchasereq_by_user" title="%s" src="/images/staffpics/%s.png" style="float:right"></img>
                      <input type="text" name="shoppinglist_id" id="shoppinglist_id" value = "%s" style="display:none" />
                      <input type="text" name="reqitem_id" id="reqitem_id"  value = "%s"  style="display:none" />
                      <label for="">Preferred Supplier</label><input type="text" name="" id="reqitem_prefered_supplier"  value = "%s" style="display:block" />
                      <label for="">Must Have Date</label><input type="text" name="" id="reqitem_must_have_date"  value = "%s" style="display:block" />
                      <br/>
                      <label for="supp_name_shopping">Supplier Name</label><br/>
                      <input type="text" name="supp_name_shopping" id="supp_name_shopping" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="supp_description">Description</label><br/>
                      <input type="text" name="supp_description_shopping" id="supp_description_shopping" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="supp_unit">Unit</label><br/>
                      <input type="text" name="supp_unit" id="supp_unit_shopping" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="supp_quantity">Quantity</label><br/>
                      <input type="text" name="supp_quantity" id="supp_quantity_shopping" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="supp_price">Price</label><br/>
                      <input type="text" name="supp_price" id="supp_price_shopping" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="supp_total">Total</label><br/>
                      <input type="text" name="supp_total" id="supp_total_shopping" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <button id="supp_shopping_price_submit_button" class="text ui-widget-content ui-corner-all" >Add Quotation</button>
                      <br/>

                </fieldset>
                        </form>

               """%(usernow.user_name,reqsone.useridnew,trolleylist.id,reqsitem.id,reqsone.prefered_supplier,reqsone.must_have_date)
        #shoppingtrolleys = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList).filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==itemid).one()
        #shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
        #        filter(JistBuyingPurchaseReqsItemsShoppingPrices.shoppinglistid==shoppingtrolleys.id)
        html1 = """
                    <p >
                    All Quotations from Suppliers  
                    </p>
                   <table id='purchase_req_quotation_suppliers' class='tablesupplier_quote'>
                    <th>ID</th>
                    <th>Supplier Name</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                    <th>Added By</th>
                    <th>Date Added</th>
                   """
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.reqitemid==itemid). \
                          order_by(desc(JistBuyingPurchaseReqsItemsShoppingPrices.id)). \
                          all()
        html2 = ''
        for shopprice in shoppingprices:
            useradded = User.by_user_id(shopprice.useridnew)
            html2temp = """
                        <tr>
                        <td>
                        %s
                        </td><td>
                        %s
                        </td><td>
                        %s
                        </td><td>
                        %s
                        </td><td align='right'>
                        %s                    
                        </td>
                        </td><td align='right'>
                        %s                    
                        </td>
                        </td><td align='right'>
                        %s                    
                        </td>
                        </td><td>
                        %s                    
                        </td>
                        </td><td width='80px'>
                        %s                    
                        </td>
                        </tr>

                    """%(shopprice.id,shopprice.suppliername,shopprice.description,
                            shopprice.unit,shopprice.quantity,shopprice.price,shopprice.total,
                            useradded.display_name,shopprice.dateadded)
            html2 = html2 + html2temp
        html3 = """
                </table>        

                """
        return html+html1+html2+html3

    @expose()
    def ajaxpurchase_reqs_get_quotation_prices_only(self,uniqid,itemid,**kw):
        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.id==int(itemid)). \
                     one()
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==trolleylist.reqitemid). \
                     one()
        #shoppingtrolleys = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList).filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==itemid).one()
        #shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
        #        filter(JistBuyingPurchaseReqsItemsShoppingPrices.shoppinglistid==shoppingtrolleys.id)

        html1 = """
                    <p id="contractheader">
                    All Quotations from Suppliers: %s  
                    </p>
                   <table id='purchase_req_quotation_suppliers_approval' class='tablesupplier_quote2'>
                    <th>ID</th>
                    <th>Item ID</th>
                    <th>Supplier Name</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                    <th>Added By</th>
                    <th>Date Added</th>
                    <th>USE</th>
                    <th>Approved</th>
                   """%(reqsitem.description)
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.reqitemid==itemid). \
                          order_by(desc(JistBuyingPurchaseReqsItemsShoppingPrices.id)). \
                          all()
        html2 = ''
        for shopprice in shoppingprices:
            useradded = User.by_user_id(shopprice.useridnew)
            html2temp = """
                        <tr>
                        <td>
                        %s
                        </td><td>
                        %s
                        </td><td>
                        %s
                        </td>
                        <td> %s </td>
                        <td>
                        %s
                        </td><td align='right'>
                        %s                    
                        </td>
                        </td><td align='right'>
                        %s                    
                        </td>
                        </td><td align='right'>
                        %s                    
                        </td>
                        </td><td>
                        %s                    
                        </td>
                        </td><td>
                        %s                    
                        </td>
                            <td width="25px" ><img  id="toggle_shopping_prices_use"
                            src="/images/flag_green_32.png"></img>
                            </td>
                        <td>
                        %s    
                        </td>
                        </tr>

                    """%(shopprice.id,reqsitem.id,shopprice.suppliername,shopprice.description,
                            shopprice.unit,shopprice.quantity,shopprice.price,shopprice.total,
                            useradded.display_name,shopprice.dateadded,shopprice.approved)
            html2 = html2 + html2temp
        html3 = """
                </table>        

                """

        return html1+html2+html3

    @expose()
    def ajaxpurchase_reqs_do_price_comparison_budget(self,uniqid,shoppinglistid,itemid,quoteid,**kw):
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.id==quoteid). \
                          one()
        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.id==int(shoppinglistid)). \
                     one()
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==trolleylist.reqitemid). \
                     one()
        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.id==reqsitem.budgetid). \
                one()
        matbudget = float(budgetdata.rate_material)*float(budgetdata.budget_qty)

        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.budgetid==budgetdata.id). \
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
                totalmatspent = totalmatspent + float(str(totexcl))

        #print totalmatspent 
        totalmatspent_format = format_decimal(totalmatspent,format='#,##0.00;-#0.00',locale='en')
        balance = float(matbudget)-float(totalmatspent)-float(shoppingprices.price)
        if balance > 0:
            blnApprove = True
        else:
            blnApprove = False
        html = """
                        <form id="purchase_approve_panel">
                        
                <fieldset>
                      <input type="text" name="app_shoppinglist_id"
                      id="app_shoppinglist_id" value = "%s"
                      style="display:none" />
                      <input type="text" name="app_reqitem_id"
                      id="app_reqitem_id"  value = "%s"
                      style="display:none" />
                      <input type="text" name="app_quote_id"
                      id="app_quote_id"  value = "%s"  style="display:none" />
                      <br/>
                      <label for="appr_name_shopping">Supplier Name</label><br/>
                      <input type="text" name="appr_name_shopping"
                      id="appr_name_shopping" value = "%s" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_description">Description</label><br/>
                      <input type="text" name="appr_description_shopping"  id="appr_description_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_unit">Unit</label><br/>
                      <input type="text" name="appr_unit" id="appr_unit_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_quantity">Quantity</label><br/>
                      <input type="text" name="appr_quantity" id="appr_quantity_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_price">Price</label><br/>
                      <input type="text" name="appr_price" id="appr_price_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_total">Total</label><br/>
                      <input type="text" name="appr_total" id="appr_total_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_budget_total">Total Budget</label><br/>
                      <input type="text" name="appr_budget_total"  id="appr_budget_total_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for="appr_total">Total Purchases Against Budget Item</label><br/>
                      <input type="text" name="appr_purchases_total" id="appr_purchases_total_shopping" value = "%s"  class="text ui-widget-content ui-corner-all" />
                      <br/>
               """%(trolleylist.id,reqsitem.id,quoteid,
                    shoppingprices.suppliername,shoppingprices.description,
                    shoppingprices.unit,shoppingprices.quantity,shoppingprices.price,shoppingprices.total,
                    matbudget,totalmatspent_format
                       )
        html2 = """
                      <button id="appr_shopping_price_submit_button"
                      class="text ui-widget-content ui-corner-all" >Approve Purchase</button>
                      <br/>
                </fieldset>
                        </form>

                """
        html3 = """
                      <p id='contractheader'> Budget Exceeded!!!!</p>
                      <br/>
                </fieldset>
                        </form>

                """
        if blnApprove:
            return html + html2
        else:
            return html + html3

    @expose()
    def ajaxApproveReqQuotation(self,uniqid,quoteid):
        #print reqitemid
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.id==quoteid). \
                          one()
        shoppingprices.approved = True
        return

    @expose()
    def ajax_purchase_reqs_approved(self,**kw):
        html1 = """
                    <p id="contractheader">
                    All Approved Requision Items:  
                    </p>
                   <table id='purchase_reqs_approved_table' class='tablesinglepoint'>
                    <th>ID</th>
                    <th>Req Item ID</th>
                    <th>JCNo</th>
                    <th>Req By</th>
                    <th>Supplier Name</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total</th>
                    <th>Added By</th>
                    <th>Date Added</th>
                    <th>Insert Current Order</th>
                    <th>Un Approve</th>
                   """
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.active==True). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.approved==True). \
                          order_by(desc(JistBuyingPurchaseReqsItemsShoppingPrices.id)). \
                          all()
        html2 = ''
        for shopprice in shoppingprices:
            useradded = User.by_user_id(shopprice.useridnew)
            #This piece of code is incorrect. The shoppinglistid below
            #should be reqitemid. This makes program work but should be
            #changed in future to be proper
            reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                         filter(JistBuyingPurchaseReqsItems.id==shopprice.shoppinglistid). \
                         one()
            usernow = User.by_user_id(reqsitem.useridnew)
            html2temp = """
                        <tr>
                        <td width="40px"> %s </td>
                        <td width="40px"> %s </td>
                        <td width="40px"> %s </td>
                        <td width="25px" >
                        <img  id="req_by_user" title="%s" src="/images/staffpics/%s.png"></img>
                        </td>
                        <td> %s </td>
                        <td> %s </td>
                        <td> %s </td>
                        <td align='right'>
                        %s                    
                        </td>
                        <td align='right'>
                        %s                    
                        </td>
                        <td align='right'>
                        %s                    
                        </td>
                        <td>
                        %s                    
                        </td>
                        <td>
                        %s                    
                        </td>
                        <td width="25px" ><img  id="toggle_shopping_prices_use"
                        src="/images/po_32.png"></img>
                        </td>
                        <td width="25px" ><img  id="toggle_un_approve"
                        src="/images/approve_not_32.png"></img>
                        </td>
                    </tr>

                    """%(shopprice.id,reqsitem.id,reqsitem.jcno,usernow.user_name,reqsitem.useridnew,shopprice.suppliername,shopprice.description,
                            shopprice.unit,shopprice.quantity,shopprice.price,shopprice.total,
                            useradded.display_name,shopprice.dateadded)
            html2 = html2 + html2temp
        html3 = """
                </table>        

                """
        return html1+html2+html3

    @expose()
    def ajaxpurchase_reqs_add_to_trolley(self,uniqid,itemid,**kw):
        if uniqid == self.last_saved_purchaseadd_trolley_rnd:
            return
        try:
            shoppingtrolley = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList).filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==itemid).one()
            blnactive = shoppingtrolley.active
            shoppingtrolley.active = not blnactive 
            return
        except:
           pass 
        newtrolley = JistBuyingPurchaseReqsItemsShoppingList()
        newtrolley.reqitemid = itemid 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newtrolley.useridnew = usernow.user_id
        newtrolley.useridedited = usernow.user_id
        newtrolley.dateadded = datetime.now()
        newtrolley.dateedited = datetime.now()
        DBS_JistBuying.add(newtrolley)
        DBS_JistBuying.flush()
        self.last_saved_purchaseadd_trolley_rnd = uniqid
        return  

    @expose()
    def ajaxpurchase_reqs_deactivate_trolley(self,itemid,**kw):
        shoppingtrolley = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList).filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==itemid).one()
        blnactive = shoppingtrolley.active
        shoppingtrolley.active = False 
        ###The code below calls the column reqitemid but is wrong. Anther comment somewhere else has this same problem. reqitemid and shoppinglistid should be turned around on database level
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices).filter(JistBuyingPurchaseReqsItemsShoppingPrices.reqitemid==shoppingtrolley.id).one()
        shoppingprices.approved = False
        return

    @expose()
    def ajaxpurchase_reqs_add_new_quote_price(self,uniqid,itemid,**kw):
        if uniqid == self.last_saved_shopping_prices_rnd:
            return
        newprice = JistBuyingPurchaseReqsItemsShoppingPrices()
        newprice.reqitemid = itemid 
        newprice.shoppinglistid = kw['shoppinglist_id']
        newprice.suppliername = kw['supp_name_shopping']
        newprice.description = kw['supp_description_shopping']
        newprice.unit = kw['supp_unit']
        newprice.quantity = kw['supp_quantity']
        newprice.price = float(kw['supp_price'])
        newprice.total = float(kw['supp_total'])
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newprice.useridnew = usernow.user_id
        newprice.useridedited = usernow.user_id
        newprice.dateadded = datetime.now()
        newprice.dateedited = datetime.now()
        DBS_JistBuying.add(newprice)
        DBS_JistBuying.flush()
        self.last_saved_shopping_prices_rnd = uniqid
        return

    @expose()
    def ajaxpurchase_reqs_add_new_note(self,uniqid,itemid,**kw):
        if uniqid == self.last_saved_purchasenote_rnd:
            return
        #for k,w in kw.iteritems():
        #    print k,w
        #return
        newnote = JistBuyingPurchaseReqsNotes()
        #newnote.reqid = int(newreqid)
        newnote.reqitemid = itemid 
        newnote.note = self.safe(kw['purchasereq_notes_new'])
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newnote.useridnew = usernow.user_id
        newnote.dateadded = datetime.now()
        DBS_JistBuying.add(newnote)
        DBS_JistBuying.flush()
        self.last_saved_purchasenote_rnd = uniqid
        return  

    @expose()
    def ajaxpurchase_reqs_add_new_note_buyingside(self,uniqid,itemid,**kw):
        if uniqid == self.last_saved_purchasenote_rnd:
            return
        #for k,w in kw.iteritems():
        #    print k,w
        #return
        newnote = JistBuyingPurchaseReqsNotes()
        #newnote.reqid = int(newreqid)
        newnote.reqitemid = itemid 
        newnote.note = self.safe(kw['purchasereq_notes_new_buying'])
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newnote.useridnew = usernow.user_id
        newnote.dateadded = datetime.now()
        DBS_JistBuying.add(newnote)
        DBS_JistBuying.flush()
        self.last_saved_purchasenote_rnd = uniqid
        return  

    @expose()
    def ajaxpurchase_reqs_notes_all(self,itemid,**kw):
        notes = DBS_JistBuying.query(JistBuyingPurchaseReqsNotes). \
                     filter(JistBuyingPurchaseReqsNotes.reqitemid==itemid). \
                     filter(JistBuyingPurchaseReqsNotes.active==True). \
                     order_by(desc(JistBuyingPurchaseReqsNotes.id)). \
                     all()
        html = ''
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_id(username)
        for note in notes:
            usernow = User.by_user_id(note.useridnew)
            htmltemp = """%s: %s \n %s \n\r"""%(usernow.display_name,note.dateadded,note.note)
            html = html + htmltemp
        return html 

    @expose()
    def purchase_reqs_items_add_form(self,jcno,suppid=0):
        reqslist = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                     filter(JistBuyingPurchaseReqsList.jcno==jcno). \
                     filter(JistBuyingPurchaseReqsList.active==False). \
                     order_by(asc(JistBuyingPurchaseReqsList.id)). \
                     all()
        reqsitems = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.jcno==jcno). \
                     order_by(asc(JistBuyingPurchaseReqsItems.id)). \
                     all()

        budgetdata = DBS_ContractData.query(JistContractBudget). \
                filter(JistContractBudget.budget_jno==jcno). \
                filter(JistContractBudget.active==True). \
                order_by(asc(JistContractBudget.id)). \
                all()
        #sitedata = "<div class='tablesinglepoint'>"
        #filter(JistBuyingOrderItems.description.like(str(searchphrase))). \
        oldorderitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.suppliercode==suppid). \
                limit(300)
        #oldorderitems = DBS_JistBuying.query(JistBuyingOrderItems.description).distinct()
        #print numberusers
        #for k in orderdesriptions:
        #    print k

        #print oldorderitems.count()
        sitedata = ""
        headerdata = """

            <form id="new_req_form">
                <fieldset>
                <table><tr>
                    """
        sitedata = sitedata + headerdata
        for k in self.newreqitemfields:
            if k == "req_jcno":
                contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
                           order_by(desc(JistContracts.jno)).all()
                sitedatatemp1 = """
                              <td>
                              <label for="%s">%s</label>
                              <select id="req_jcno" disabled="true">
                              """% (k,k)
                sitedatatemp2 = ""
                for cont in contracts:
                    sitedatatemp21 = """
                                   <option class="contract_req_select" value="%s" >%s</option>
                                    """ % (cont.jno,cont.jno)
                    sitedatatemp2 = sitedatatemp2 + sitedatatemp21
                sitedatatemp3 = """
                              </select>
                              </td>
                              """
                sitedatatemp = sitedatatemp1 + sitedatatemp2 + sitedatatemp3 
            elif k == "req_budget_item":
                sitedatatemp1 = """
                              <td >
                              <label for="%s">%s</label>
                              <select id="req_budget_item" class="contract_req_budget">
                              """% (k,k)
                sitedatatemp2 = ""
                for cont in budgetdata:
                    sitedatatemp21 = """
                                   <option  value="%s"; name="%s">%s</option>
                                    """ % (cont.id,cont.budget_description,cont.budget_description)
                    sitedatatemp2 = sitedatatemp2 + sitedatatemp21
                sitedatatemp3 = """
                              </select>
                              </td>
                              """
                sitedatatemp = sitedatatemp1 + sitedatatemp2 + sitedatatemp3 

            elif k == "req_description":
                sitedatatemp1 = """
                              <td>
                              <label for="%s">%s</label>
                              <input  id="%s" style="display:none"/>
                        <select id="combobox_req_description" style="display: none">
                        <option value="">Select one...</option>
                            """% (k,k,k)
                sitedatatemp2 = ""
                for old in oldorderitems:
                    sitedatatemp21 = """
                            <option value="%s">%s</option>
                                 """% (old.description,old.description)
                    sitedatatemp2 = sitedatatemp2 + sitedatatemp21 
                sitedatatemp3 = """
                              </select>
                              </td>
                              """
                sitedatatemp = sitedatatemp1 + sitedatatemp2 + sitedatatemp3 

            else:
                sitedatatemp = """
                              <td>
                              <label for="%s">%s</label>
                              <input  name="%s" id="%s" />
                             </td>
               
                                """ % (k,k,k,k)

            sitedata = sitedata + sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        taildata = """
                            </tr>
                            </table>
                            </fieldset>
                        </form>
                        <p/>

                    """
        sitedata = sitedata +taildata

        return sitedata  

    @expose()
    @expose('json')
    def search_supplier_items(self,supno,**kw):
        phrase = ''
        for k,w in kw.iteritems():
            #print k,w
            phrase = k
        searchphrase = "%"+phrase+"%"
        #filter(JistBuyingOrderItems.description.like(str(searchphrase))). \
        orderitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.suppliercode==supno). \
                distinct().limit(500)
        tempbox =""

        for ord in orderitems:
            #print ord.description
            tempbox1 = """
                   <li value="%s"> %s,</li>
                      """%(ord.id,ord.description)
            tempbox = tempbox + tempbox1
        #tempbox = tempbox  
        return tempbox  

    @expose()
    def savenew_requisition_test(self,**kw):
        #for k,w in kw.iteritems():
        #    print k,w
        #print kw['name']
        if kw['uniqid'] == self.last_saved_purchasereq_rnd:
            return '1'
        self.last_saved_purchasereq_rnd = kw['uniqid']
        return '2'

    @expose()
    def savenew_requisition(self,uniqid,jcno,prefered_date=datetime.date(datetime.now()),prefered_supplier='Nobody'):
        if uniqid == self.last_saved_purchasereq_rnd:
            reqslist = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                         order_by(desc(JistBuyingPurchaseReqsList.id)). \
                         first()
            return str(reqslist.id)
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newreq = JistBuyingPurchaseReqsList()
        newreq.jcno = int(jcno)
        newreq.prefered_supplier =safe(prefered_supplier)
        newreq.must_have_date =prefered_date
        newreq.useridnew = usernow.user_id
        DBS_JistBuying.add(newreq)
        DBS_JistBuying.flush()
        self.last_saved_purchasereq_rnd = uniqid
        self.last_saved_purchasereq_id = newreq.id
        return str(newreq.id) 

    @expose()
    def savenew_requisition_items(self,uniqid,newreqid,jcno,budgetid,req_item,description,unit,qty):
        if uniqid == self.last_saved_purchaseitem_rnd:
            return
        #print description
        newreqitem = JistBuyingPurchaseReqsItems()
        #newreqitem.reqid = int(newreqid)
        newreqitem.reqid = int(newreqid)
        newreqitem.jcno = int(jcno)
        newreqitem.budgetid = int(budgetid)
        newreqitem.item = safe(req_item)
        newreqitem.description =safe(description)
        newreqitem.unit =safe(unit)
        newreqitem.quantity =float(qty)
        newreqitem.active = 1
        #newreqitem.price =kw['price']
        #newreqitem.total =kw['total']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newreqitem.useridnew = usernow.user_id
        DBS_JistBuying.add(newreqitem)
        DBS_JistBuying.flush()
        self.last_saved_purchaseitem_rnd = uniqid
        return  

    @require(in_any_group("managers","logistics"))
    @expose('jistdocstore.templates.logistics.order_vs_grv_search')
    def search_open_orders_vs_grv(self,**named):
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        #for contract in contracts:
        #    print contract.jno
        return dict(page='GRV Console',
                    wip = contracts,
                    suppliers = supplierlist,
                    #newreqitemfields = self.newreqitemfields,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def get_supplier_open_orders(self,supplierid, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        suppliercode = int(supplierid)
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                        filter(JistBuyingOrderList.active=='Y'). \
                        filter(JistBuyingOrderList.suppliercode==suppliercode). \
                        order_by(desc(JistBuyingOrderList.id)).all()
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==suppliercode). \
                     value(func.sum(JistBuyingOrderList.totalexcl))

        supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()
        #for k in openorders:
        #    print k
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        supplier_text = "<p id='contractheader'> Purchase Orders to %s : </p>"%(suppliername)
        pdfstuff = ""
        sitedata = "<table id='grv_open_orders_table' class='tablegrvmain'>"
        headerdata = """
                    <colgroup></colgroup>
                    <colgroup></colgroup>
                    <th>ID </th>
                    <th>Purchase Order Number </th>
                    <th>Purchase Date</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr class='tablegrvmain'>
                            <td>
                             %s
                            </td>
                            <td>
                             %s
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.ponumber,
                                    k.podate
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def get_po_order_supplier_open_orders(self,supplierid, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        suppliercode = int(supplierid)
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                        filter(JistBuyingOrderList.active=='Y'). \
                        filter(JistBuyingOrderList.suppliercode==suppliercode). \
                        order_by(desc(JistBuyingOrderList.id)).all()
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==suppliercode). \
                     value(func.sum(JistBuyingOrderList.totalexcl))

        supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()
        #for k in openorders:
        #    print k
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        supplier_text = "<p id='contractheader'> Purchase Orders to %s : </p>"%(suppliername)
        pdfstuff = ""
        sitedata = "<table id='po_order_open_orders_table' class='tablegrvmain'>"
        headerdata = """
                    <colgroup></colgroup>
                    <colgroup></colgroup>
                    <th>ID </th>
                    <th>Purchase Date</th>
                    <th>Purchase Order Number </th>
                    <th align="right">Purchase Total Excl </th>
                    <th>Items</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr class='tablegrvmain'>
                            <td>
                             %s
                            </td>
                            <td>
                             %s
                            </td>
                            <td>%s
                            </td>
                            <td align="right">%s
                            </td>
                            <td width="25px" ><img  id="toggle_poitems"
                            src="/images/po_32.png"></img>
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.podate,k.ponumber,k.totalexcl
                                    
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def get_supplier_po_orders_time(self, **kw):
        #for k,w in kw.iteritems():
        #    print k,w
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        fromdate = kw['supplierview_from_date']
        todate = kw['supplierview_to_date']
        openorders_total_all = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.podate >= fromdate). \
                     filter(JistBuyingOrderList.podate <= todate). \
                     value(func.sum(JistBuyingOrderList.totalexcl))
        if not openorders_total_all: openorders_total_all = 0
        totalall_exl = format_decimal(openorders_total_all ,format='#,##0.00;-#0.00',locale='en')
        suppliers_all = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.active==True).all()
        supplier_text = """<p id='contractheader'> Suppliers Total Expenditure from: %s to: %s</p>
                        <p id='contractheader'>Total Orders Issued Excl Vat: %s</p>
                        """%(fromdate,todate,totalall_exl)
        pdfstuff = """
                    <a href="/logisticscont/exportsupplierExpenditureTime/%s/%s">
                    <img id="pdfsupplierExpenditure" src="/images/pdficon.jpg" align="right"></img>
                    </a>
                    """%(fromdate,todate)
        sitedata = "<table id='tbl_all_supplier_time_expenditure' class 'tablegrvmain'>"
        headerdata = """
                    <th>ID </th>
                    <th>Supplier Name</th>
                    <th align="right">Purchase Total Excl </th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        supplierdata = ""
        for sups in suppliers_all:
            openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                            filter(JistBuyingOrderList.active=='Y'). \
                            filter(JistBuyingOrderList.suppliercode==sups.id). \
                            order_by(desc(JistBuyingOrderList.id)).all()
            openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                         filter(JistBuyingOrderList.active=='Y'). \
                         filter(JistBuyingOrderList.suppliercode==sups.id). \
                         filter(JistBuyingOrderList.podate >= fromdate). \
                         filter(JistBuyingOrderList.podate <= todate). \
                         value(func.sum(JistBuyingOrderList.totalexcl))
            if openorders_total:
                totalexcl = format_decimal(openorders_total ,format='#,##0.00;-#0.00',locale='en')
                supplierdata_temp = """
                               <tr class='tablegrvmain'>
                                <td>
                                 %s
                                </td>
                                <td align="left">
                                %s
                                </td>
                                <td align="right">
                                %s
                                </td>
                                </tr>
                                """%(sups.id,sups.suppliername,totalexcl)
                supplierdata = supplierdata + supplierdata_temp
        return sitedata + supplierdata 

    @expose()
    def get_poitems_grv_info(self, **kw):
        fromdate = kw['grvview_from_date']
        todate = kw['grvview_to_date']
        poorders = DBS_JistBuying.query(JistBuyingOrderList). \
                 filter(JistBuyingOrderList.podate >= fromdate). \
                 filter(JistBuyingOrderList.podate <= todate). \
                all()
        htmldetails = htmlitemsheaders = htmlitems = htmlitemsfooters = ''
        htmlitemsheaders = """
                        <table id="grv_order_items_table" class="tablebuyingitemsgrv" border="0" cellspacing="0" cellpadding="2">
                                    <th>ID</th>
                                    <th>PO ID</th>
                                    <th>JCNo</th>
                                    <th>Purchase Date</th>
                                    <th>Supplier</th>
                                    <th>Description </th>
                                    <th>Unit</th>
                                    <th>Qty Ordered</th>
                                    <th>Req By</th>
                                    <th>Qty Delivered</th>
                                    <th>Qty Balance</th>
                                    <th>Buyer</th>

                           """
        for poorder in poorders:
            #print poorder
            supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                            filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                            one()
            poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                    filter(JistBuyingOrderItems.ponumber==int(poorder.id)). \
                    all()
            #htmldetails = """
            #      <div id='grv_order_details' class='sidebar_labour_payment_data'>
            #            <table class='tablelabourdata' border='0' cellspacing='0' cellpadding='2'>
            #                        <th>Order Number </th>
            #                        <th>Purchase Date</th>
            #                        <th>Supplier </th>
            #              <tr >
            #                        <td >
            #                            %s 
            #                        </td>
            #                        <td >
            #                            %s 
            #                        </td>
            #                        <td >
            #                            %s 
            #                        </td>
            #                </tr>
            #           </table>
            #      </div>
            #      """ %(str(poorder.ponumber),str(poorder.podate),str(supplier.suppliername))

            for item in poitems: 
                grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                        join(JistBuyingOrderItems). \
                        filter(JistBuyingGRV.buyingitemid==item.id). \
                        all()
                grvitemsqtytotal = DBS_JistBuying.query(JistBuyingGRV). \
                        filter(JistBuyingGRV.buyingitemid==item.id). \
                        value(func.sum(JistBuyingGRV.grvqty))
                if not grvitemsqtytotal: grvitemsqtytotal = 0
                try:
                    reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                                 filter(JistBuyingPurchaseReqsItems.id==item.reqid). \
                                 one()
                    thisuser = reqsitem.useridnew
                except:
                    thisuser = 1

                if grvitemsqtytotal:
                    if not item.quantity: item.quantity = 0
                    grvbalance = Decimal(item.quantity) - Decimal(grvitemsqtytotal)
                else:
                    #print item.quantity
                    if item.quantity == '': item.quantity = 0

                    grvitemsqtytotal = 0
                    grvbalance = Decimal(item.quantity) - Decimal(grvitemsqtytotal)
                htmlitemstemp = """
                                  <tr >
                                            <td align="left" width="60px">
                                                %s
                                            </td>
                                            <td align="left" width="60px" >
                                                %s
                                            </td>
                                            <td align="left"  width="60px">
                                                %s
                                            </td>
                                            <td align="left"  width="80px">
                                            %s 
                                            </td>
                                            <td align="left"  width="280px">
                                            %s 
                                            </td>
                                            <td align="left" >
                                            %s 
                                            </td>
                                            <td  align="left"  width="60px">
                                            %s 
                                            </td>
                                            <td  align="left"  width="60px">
                                            %s 
                                            </td>
                                            <td  align="left"  width="60px">
                                            <img src="/images/staffpics/%s.png"
                                                align="center"/>
                                            </td>
                                            <td  align="left"  width="60px">
                                            %s 
                                            </td>
                                            <td  align="left"  width="60px">
                                            %s 
                                            </td>
                                            <td  align="left"  width="60px">
                                            <img src="/images/staffpics/%s.png"
                                                align="center"/>
                                            </td>
                                    </tr>
                          """ %(  
                                  item.id,str(poorder.id), str(item.contract), str(item.podate), supplier.suppliername,
                                  item.description,item.unit,item.quantity,thisuser,grvitemsqtytotal,grvbalance,
                                  item.useridnew
                                  )
                htmlitems = htmlitems + htmlitemstemp
        htmlitemsfooters = """

                           </table>

                          """
        htmlall = htmldetails + htmlitemsheaders + htmlitems+ htmlitemsfooters
        return htmlall

    @expose()
    def new_po_order_supplier(self,uniqid,supplierid, **kw):
        #create new poorder
        if uniqid == self.last_saved_purchase_order_rnd:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        neworder = JistBuyingOrderList()
        neworder.podate = datetime.date(datetime.now())
        neworder.suppliercode = supplierid
        neworder.datecreated = datetime.now()
        neworder.useridnew = usernow.user_id
        DBS_JistBuying.add(neworder)
        DBS_JistBuying.flush()
        neworder.ponumber = "PO - " + str(neworder.id)
        self.last_saved_purchase_order_rnd = uniqid
        #show the records
        #username = request.identity['repoze.who.userid']
        #usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        suppliercode = int(supplierid)
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                        filter(JistBuyingOrderList.active=='Y'). \
                        filter(JistBuyingOrderList.suppliercode==suppliercode). \
                        order_by(desc(JistBuyingOrderList.id)).all()
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==suppliercode). \
                     value(func.sum(JistBuyingOrderList.totalexcl))

        supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()
        #for k in openorders:
        #    print k
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        supplier_text = "<p id='contractheader'> Purchase Orders to %s : </p>"%(suppliername)
        pdfstuff = ""
        sitedata = "<table id='po_order_open_orders_table' class='tablegrvmain'>"
        headerdata = """
                    <colgroup></colgroup>
                    <colgroup></colgroup>
                    <th>ID </th>
                    <th>Purchase Date</th>
                    <th>Purchase Order Number </th>
                    <th align="right">Purchase Total Excl </th>
                    <th>Items</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr class='tablegrvmain'>
                            <td>
                             %s
                            </td>
                            <td>
                             %s
                            </td>
                            <td>%s
                            </td>
                            <td align="right">%s
                            </td>
                            <td width="25px" ><img  id="toggle_poitems"
                            src="/images/po_32.png"></img>
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.podate,k.ponumber,k.totalexcl
                                    
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def get_open_orders_all_active(self, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                        filter(JistBuyingOrderList.active=='Y'). \
                        order_by(desc(JistBuyingOrderList.id)).limit(100)
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     value(func.sum(JistBuyingOrderList.totalexcl))

        locale.setlocale(locale.LC_ALL, '')
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        supplier_text = "<p id='contractheader'> Open Purchase Orders  : </p><p/>"
        pdfstuff = ""
        sitedata = "<table id='open_po_orders_table' class='tablegrvmain'>"
        headerdata = """
                    <colgroup></colgroup>
                    <colgroup></colgroup>
                    <th>ID </th>
                    <th>Purchase Order Number </th>
                    <th>Purchase Date</th>
                    <th>Supplier</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==k.suppliercode).one()
            #for k in openorders:
            #    print k
            suppliername = supn.suppliername
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr class='tablegrvmain'>
                            <td>
                             %s
                            </td>
                            <td>
                             %s
                            </td>
                            <td>%s
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.ponumber,
                                    k.podate,suppliername
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def get_contract_open_orders(self,jcno, **kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        suppliercode = int(supplierid)
        contract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jcno). \
                                            one()
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                        filter(JistBuyingOrderList.active=='Y'). \
                        filter(JistBuyingOrderList.contract==jcno). \
                        order_by(desc(JistBuyingOrderList.id)).all()
        openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.suppliercode==suppliercode). \
                     value(func.sum(JistBuyingOrderList.totalexcl))
        supn = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        if openorders_total is None:
            totalexcl = 0.00
        else:
            totalexcl = format_decimal(openorders_total,format='#,##0.00;-#0.00',locale='en')
        supplier_text = "<H3 align='center'> Purchase Orders for  %s: </H3><p/>"%(contract.site)
        pdfstuff = ""
        sitedata = "<table class='tablestandard'>"
        headerdata = """
                    <colgroup></colgroup>
                    <colgroup></colgroup>
                    <th>Purchase Order Number </th>
                    <th>Purchase Date</th>
                    """
        sitedata = supplier_text +pdfstuff+sitedata + headerdata
        for k in openorders:
            totalexcl = format_decimal(k.totalexcl,format='#,##0.00;-#0.00',locale='en')
            sitedatatemp = """
                            <tr>
                            <td>
                            <a href='/logisticscont/grv_order_one/%s'>%s
                            </a>
                            </td>
                            <td>%s
                            </td>
                            <p/>
                            </tr>
                            """ % (k.id,k.ponumber,
                                    k.podate
                                   )
            sitedata = sitedata +"</p>"+ sitedatatemp
        sitedata = sitedata +"</table>"
        return sitedata 

    @expose()
    def grv_order_one_details(self,ordernumber,**named):
        poorder = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==int(ordernumber)). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                        one()

        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==int(ordernumber)). \
                all()
        htmldetails = """
              <div id='grv_order_details' class='sidebar_labour_payment_data'>
                    <table class='tablelabourdata' border='0' cellspacing='0' cellpadding='2'>
                                <th>Order Number </th>
                                <th>Purchase Date</th>
                                <th>Supplier </th>
                      <tr >
                                <td >
                                    %s 
                                </td>
                                <td >
                                    %s 
                                </td>
                                <td >
                                    %s 
                                </td>
                        </tr>
                   </table>
              </div>
              """ %(str(poorder.ponumber),str(poorder.podate),str(supplier.suppliername))

        htmlitemsheaders = """
                        <table id="grv_order_items_table" class="tablelabourdata" border="0" cellspacing="0" cellpadding="2">
                                    <th>ID</th>
                                    <th>PO ID</th>
                                    <th>JCNo</th>
                                    <th>Purchase Date</th>
                                    <th>Description </th>
                                    <th>Unit</th>
                                    <th>Qty Ordered</th>
                                    <th>Req By</th>
                                    <th>Qty Delivered</th>
                                    <th>Qty Balance</th>
                                    <th>Buyer</th>

                           """
        htmlitems = ''
        for item in poitems: 
            grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                    join(JistBuyingOrderItems). \
                    filter(JistBuyingGRV.buyingitemid==item.id). \
                    all()
            grvitemsqtytotal = DBS_JistBuying.query(JistBuyingGRV). \
                    filter(JistBuyingGRV.buyingitemid==item.id). \
                    value(func.sum(JistBuyingGRV.grvqty))
            try:
                reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                             filter(JistBuyingPurchaseReqsItems.id==item.reqid). \
                             one()
                thisuser = reqsitem.useridnew
            except:
                thisuser = 1

            if grvitemsqtytotal:
                grvbalance = Decimal(item.quantity) - Decimal(grvitemsqtytotal)
            else:
                #print item.quantity
                if item.quantity == '': item.quantity = 0

                grvitemsqtytotal = 0
                grvbalance = Decimal(item.quantity) - Decimal(grvitemsqtytotal)
            htmlitemstemp = """
                              <tr >
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                        %s 
                                        </td>
                                        <td align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        <img src="/images/staffpics/%s.png"
                                            align="center"/>
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        <img src="/images/staffpics/%s.png"
                                            align="center"/>
                                        </td>
                                </tr>
                      """ %(  
                              item.id,str(poorder.id), str(item.contract), str(item.podate),
                              item.description,item.unit,item.quantity,thisuser,grvitemsqtytotal,grvbalance,
                              item.useridnew
                              )
            htmlitems = htmlitems + htmlitemstemp
        htmlitemsfooters = """

                           </table>

                          """
        htmlall = htmldetails + htmlitemsheaders + htmlitems+ htmlitemsfooters
        return htmlall

    @expose()
    def grv_order_one_item(self,po_item,ordernumber,**named):
        poorder = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==int(ordernumber)). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                        one()

        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.id==int(po_item)). \
                one()
        htmldetails = """
              <div id='grv_order_details' class='sidebar_labour_payment_data'>
                    <table class='tablelabourdata' border='0' cellspacing='0' cellpadding='2'>
                                <th>Order Number </th>
                                <th>Purchase Date</th>
                                <th>Supplier </th>
                      <tr >
                                <td >
                                    %s 
                                </td>
                                <td >
                                    %s 
                                </td>
                                <td >
                                    %s 
                                </td>
                        </tr>
                   </table>
              </div>
              """ %(str(poorder.ponumber),str(poorder.podate),str(supplier.suppliername))

        htmlitemsheaders = """
                        <table id="grv_order_item_one_table" class="tablelabourdata" border="0" cellspacing="0" cellpadding="2">
                                    <th>ID</th>
                                    <th>Order ID</th>
                                    <th>JCNo</th>
                                    <th>Purchase Date</th>
                                    <th>Description </th>
                                    <th>Unit</th>
                                    <th>Qty Ordered</th>
                                    <th>Qty Delivered</th>
                                    <th>Qty Balance</th>
                                    <th>Buyer</th>

                           """
        htmlitems = ''
        #for item in poitems: 
        grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                join(JistBuyingOrderItems). \
                filter(JistBuyingGRV.buyingitemid==poitems.id). \
                all()
        grvitemsqtytotal = DBS_JistBuying.query(JistBuyingGRV). \
                filter(JistBuyingGRV.buyingitemid==poitems.id). \
                value(func.sum(JistBuyingGRV.grvqty))
        stores = DBS_JistBuying.query(JistBuyingStoresLocation). \
                all()

        if grvitemsqtytotal:
            grvbalance = Decimal(poitems.quantity) - Decimal(grvitemsqtytotal)
        else:
            grvitemsqtytotal = 0
            grvbalance = Decimal(poitems.quantity) - Decimal(grvitemsqtytotal)
        htmlitemstemp = """
                          <tr >
                                    <td align="left" >
                                        %s
                                    </td>
                                    <td align="left" >
                                        %s
                                    </td>
                                    <td align="left" >
                                        %s
                                    </td>
                                    <td align="left" >
                                    %s 
                                    </td>
                                    <td align="left" >
                                    %s 
                                    </td>
                                    <td  align="left" >
                                    %s 
                                    </td>
                                    <td  align="left" >
                                    %s 
                                    </td>
                                    <td  align="left" >
                                    %s 
                                    </td>
                                    <td  align="left" >
                                    %s 
                                    </td>
                                    <td  align="left" >
                                    <img src="/images/staffpics/%s.png"
                                        align="center"/>
                                    </td>
                            </tr>
                  """ %(  
                          poitems.id,str(poorder.id), str(poitems.contract), str(poitems.podate),
                          poitems.description,poitems.unit,poitems.quantity,grvitemsqtytotal,grvbalance,
                          poitems.useridnew
                          )
        htmlitems = htmlitems + htmlitemstemp
        htmlitemsaddform = """

                           </table>
                           <p/>
                            <form id="new_grv_form">
                                <fieldset>
                                  <label for="grv_date">Delivery Date</label>
                                  <input type="text" name="grv_date" id="grv_date" class="text ui-widget-content ui-corner-all" />
                                  <label for="grv_del_num">Delivery Note - Invoice Number</label><br/>
                                  <input type="text" name="grv_del_num" id="grv_del_num" class="text ui-widget-content ui-corner-all" />
                                  <label for="grv_qty">Delivered Quantity</label><br/>
                                  <input type="text" name="grv_qty" id="grv_qty" class="text ui-widget-content ui-corner-all" />
                                  <label for="grv_store">Placed In</label>

                     """
        htmlform2 = "<select  id='grv_store'>"
        for store in stores:
            htmlform2temp = """
                    <option value="%s">%s</option>
                  
                  """%(store.id,store.store_name)
            htmlform2 = htmlform2 + htmlform2temp
        htmlform3 = """
                                  </select>
                                <button class="ui-state-default ui-corner-all" id="add-grv-to-list">Add Delivery </button>
                                </fieldset>
                            </form></p>

                    """
        htmlitemsaddform = htmlitemsaddform + htmlform2 + htmlform3
        htmlgrvfirst = ''
        htmlgrvheaders = """
                        <div id="grv_items_done_div">
                        <table id="grv_items_done_table" class="tablelabourdata" border="0" cellspacing="0" cellpadding="2">
                                    <th>ID</th>
                                    <th>GRV Date</th>
                                    <th>Description </th>
                                    <th>Unit</th>
                                    <th>Qty Ordered</th>
                                    <th>Del/Inv No</th>
                                    <th>Qty Delivered</th>
                                    <th>Done By</th>

                           """
        for grv in grvitems:
            htmlgrvtemp = """
                              <tr >
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                        %s 
                                        </td>
                                        <td align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        <img src="/images/staffpics/%s.png"
                                            align="center"/>
                                        </td>
                                </tr>
                      """ %(  
                              grv.grvid,grv.grvdate,
                              poitems.description,poitems.unit,poitems.quantity,grv.grvdelnum,grv.grvqty,
                              grv.useridnew
                              )
            htmlgrvfirst = htmlgrvfirst + htmlgrvtemp
        htmlgrvfooter = """
                           </table>
                        </div>

                     """
        htmlgrv = htmlgrvheaders + htmlgrvfirst + htmlgrvfooter
        htmlall = htmldetails + htmlitemsheaders + htmlitems + htmlitemsaddform +htmlgrv
        return htmlall

    @expose()
    def grv_save_new_item(self,uniqid,poitem,deldate=datetime.date(datetime.now()),delnoteno='None',delqty=0,instore=1,**kw):
        #for k,w in kw.iteritems():
        #    print k,w
        if self.last_saved_grv_item_rnd == uniqid:
            return
        new_grv = JistBuyingGRV()
        new_grv.buyingitemid = poitem
        new_grv.grvdate = deldate 
        new_grv.grvdelnum = delnoteno 
        new_grv.grvqty = delqty 
        new_grv.in_store = instore 
        new_grv.active = 1 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        new_grv.useridnew = usernow.user_id
        DBS_JistBuying.add(new_grv)
        DBS_JistBuying.flush()
        self.last_saved_grv_item_rnd = uniqid
        return

    @expose()
    def grv_req_one_items(self,reqid,**named):
        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.reqid==str(reqid)). \
                all()
        htmlitems = ''
        htmlgrvfirst = ''
        htmlgrvheaders = """
                        <table id="grv_items_done_table" class="tablelabourdata" border="0" cellspacing="0" cellpadding="2">
                                    <th>ID</th>
                                    <th>GRV Date</th>
                                    <th>Description </th>
                                    <th>Unit</th>
                                    <th>Qty Ordered</th>
                                    <th>Req By</th>
                                    <th>Del/Inv No</th>
                                    <th>Qty Delivered</th>
                                    <th>Done By</th>

                           """
        for poitem in poitems:
            grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                    join(JistBuyingOrderItems). \
                    filter(JistBuyingGRV.buyingitemid==poitem.id). \
                    all()
            for grv in grvitems:
                htmlgrvtemp = """
                                  <tr >
                                            <td align="left" >
                                                %s
                                            </td>
                                            <td align="left" >
                                                %s
                                            </td>
                                            <td align="left" >
                                                %s
                                            </td>
                                            <td align="left" >
                                            %s 
                                            </td>
                                            <td align="left" >
                                            %s 
                                            </td>
                                            <td  align="left" >
                                            <img src="/images/staffpics/%s.png"
                                                align="center"/>
                                            </td>
                                            <td  align="left" >
                                            %s 
                                            </td>
                                            <td  align="left" >
                                            %s 
                                            </td>
                                            <td  align="left" >
                                            <img src="/images/staffpics/%s.png"
                                                align="center"/>
                                            </td>
                                    </tr>
                          """ %(  
                                  grv.grvid,grv.grvdate,
                                  poitem.description,poitem.unit,poitem.quantity,1,grv.grvdelnum,grv.grvqty,
                                  grv.useridnew
                                  )
                htmlgrvfirst = htmlgrvfirst + htmlgrvtemp
        htmlgrvfooter = """

                           </table>
                           </p>
                           <div style="float:right">
                          <button class="ui-state-default ui-corner-all" id="grv_back_button">Remove Tab</button>
                           </div>
                     """
        htmlgrv = htmlgrvheaders + htmlgrvfirst + htmlgrvfooter
        return htmlgrv

    @require(in_any_group("managers","logistics","logistics_manager"))
    @expose('jistdocstore.templates.logistics.buyingconsole')
    def buyingconsole(self,**named):
        """Handle the 'requistion new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        userlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            if point:
                if point.user_id == 1:
                    userlist.append({'user_id':point.user_id,
                                      'user_name':point.user_name,
                                      'display_name':point.display_name
                                      })
                user = User.by_user_id(point.user_id)
                userpermissions = user.permissions
                for permis in userpermissions:
                    if permis.permission_name=='production':
                        userlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name,
                                          'display_name':point.display_name
                                          })
        return dict(page='Buying Console',
                    wip = contracts,
                    suppliers = supplierlist,
                    production_users = userlist,
                    newreqitemfields = self.newreqitemfields,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def po_order_one_details(self,ordernumber,**named):
        poorder = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==int(ordernumber)). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                        one()

        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==int(ordernumber)). \
                all()
        htmldetails = """
              <div id='grv_order_details' class='sidebar_labour_payment_data'>
                    <table class='tablelabourdata' border='0' cellspacing='0' cellpadding='2'>
                                <th>Order Number</th>
                                <th>Purchase Date</th>
                                <th>Supplier</th>
                                <th>PDF</th>
                      <tr>
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
                        <a href="/logisticscont/exportPurchaseOrderBuying/%s">
                        <img src="/images/pdficon.jpg"></img>
                        </a>
                                </td>
                                <p/></tr>
                     </tr>
                   </table>
              </div>
              """ %(str(poorder.ponumber),str(poorder.podate),str(supplier.suppliername),str(poorder.id))
        htmlitemsheaders = """
                        <table id="purchase_order_items_table" class="tablelabourdata" border="0" cellspacing="0" cellpadding="2">
                                    <th>ID</th>
                                    <th>PO ID</th>
                                    <th>JCNo</th>
                                    <th>Purchase Date</th>
                                    <th>Description </th>
                                    <th>Unit</th>
                                    <th>Req By</th>
                                    <th align="right">Qty Ordered</th>
                                    <th align="right">Price Excl</th>
                                    <th align="right">Total Excl</th>
                                    <th align="right">Qty Delivered</th>
                                    <th align="right">Qty Balance</th>
                                    <th>Buyer</th>
                                    <th>Edit</th>

                           """
        htmlitems = ''
        for item in poitems: 
            grvitems = DBS_JistBuying.query(JistBuyingGRV). \
                    join(JistBuyingOrderItems). \
                    filter(JistBuyingGRV.buyingitemid==item.id). \
                    all()
            grvitemsqtytotal = DBS_JistBuying.query(JistBuyingGRV). \
                    filter(JistBuyingGRV.buyingitemid==item.id). \
                    value(func.sum(JistBuyingGRV.grvqty))
            try:
                reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                             filter(JistBuyingPurchaseReqsItems.id==item.reqid). \
                             one()
                thisuser = reqsitem.useridnew
            except:
                thisuser = 1

            if grvitemsqtytotal:
                grvbalance = Decimal(item.quantity) - Decimal(grvitemsqtytotal)
            else:
                #print item.quantity
                if item.quantity == '': item.quantity = 0

                grvitemsqtytotal = 0
                grvbalance = Decimal(item.quantity) - Decimal(grvitemsqtytotal)
            htmlitemstemp = """
                              <tr >
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                            %s
                                        </td>
                                        <td align="left" >
                                        %s 
                                        </td>
                                        <td align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        <img src="/images/staffpics/%s.png"
                                            align="center"/>
                                        </td>
                                        <td  align="right" >
                                        %s 
                                        </td>
                                        <td  align="right" >
                                        %s 
                                        </td>
                                        <td  align="right" >
                                        %s 
                                        </td>
                                        <td  align="right" >
                                        %s 
                                        </td>
                                        <td  align="right" >
                                        %s 
                                        </td>
                                        <td  align="left" >
                                        <img src="/images/staffpics/%s.png"
                                            align="center"/>
                                        </td>
                                    <td width='25px'>
                                            <img id="edit_buying_item"
                                            src="/images/edit-4.png" >
                                            </img>
                                    </td>
                                    </tr>
                      """ %(  
                              item.id,str(poorder.id), str(item.contract), str(item.podate),
                              item.description,item.unit,thisuser,item.quantity,item.priceexcl,item.totalexcl,grvitemsqtytotal,grvbalance,
                              item.useridnew
                              )
            htmlitems = htmlitems + htmlitemstemp
        htmlitemsfooters = """

                           </table>

                          """
        htmlall = htmldetails + htmlitemsheaders + htmlitems+ htmlitemsfooters
        return htmlall

    @expose()
    def ajaxWriteOrderItemToPO(self,uniqid,ordernumber,reqitemid,shoppingid,**kw):
        #for k,w in kw.iteritems():
        #    print k,w
        if self.last_saved_order_item_rnd == uniqid:
            return
        poorder = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==int(ordernumber)). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                        one()

        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==int(ordernumber)). \
                all()

        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==reqitemid). \
                     one()
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==reqitemid). \
                     one()
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.id==shoppingid). \
                          one()
        data = {'poid':poorder.id,
                 'ponumber': poorder.ponumber,
                 'suppliercode': poorder.suppliercode,
                 'pototalexcl' : poorder.totalexcl,
                 'pototalvat'  : poorder.totalvat,
                 'pototalincl' : poorder.totalincl,
                 'req_id'      : reqsitem.reqid,
                 'req_itemid'      : reqsitem.id,
                 'req_jcno'      : reqsitem.jcno,
                 'trol_id'     : trolleylist.id,
                 'shop_id'     : shoppingprices.id,
                 'shop_description'     : shoppingprices.description,
                 'shop_unit'     : shoppingprices.unit,
                 'shop_quantity'     : shoppingprices.quantity,
                 'shop_price'     : shoppingprices.price,
                 'shop_total'     : shoppingprices.total
                }
        new_orderitem = JistBuyingOrderItems()
        new_orderitem.podate = datetime.date(datetime.now()) 
        new_orderitem.ponumber = data['poid'] 
        new_orderitem.reqid = data['req_itemid'] 
        new_orderitem.contract = data['req_jcno'] 
        new_orderitem.suppliercode = data['suppliercode'] 
        new_orderitem.description = data['shop_description'] 
        new_orderitem.unit = data['shop_unit'] 
        new_orderitem.quantity = data['shop_quantity'] 
        new_orderitem.priceexcl = data['shop_price'] 
        new_orderitem.totalexcl = data['shop_total'] 
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        new_orderitem.useridnew = usernow.user_id
        new_orderitem.useridedited = usernow.user_id
        new_orderitem.datecreated = datetime.now() 
        new_orderitem.dateedited =  datetime.now()
        DBS_JistBuying.add(new_orderitem)
        #print new_orderitem
        shoppingprices.active = 0
        trolleylist.active = 0
        reqsitem.poid = data['poid'] 
        DBS_JistBuying.flush()
        reqsitem.poitemid = new_orderitem.id 
        poitemstotal = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==data['poid']). \
                value(func.sum(JistBuyingOrderItems.totalexcl))
        poorder.totalexcl = poitemstotal
        totalvat = poitemstotal * VAT_RATE
        totalincl = poitemstotal + totalvat
        poorder.totalvat = totalvat
        poorder.totalincl = totalincl
        self.last_saved_order_item_rnd = uniqid
        return 

        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        new_grv.useridnew = usernow.user_id
        DBS_JistBuying.add(new_grv)
        DBS_JistBuying.flush()
        return

    @expose()
    def ajaxUnapprovePrice(self,reqitemid,shoppingid,**kw):
        #for k,w in kw.iteritems():
        #    print k,w
        trolleylist = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingList). \
                     filter(JistBuyingPurchaseReqsItemsShoppingList.reqitemid==reqitemid). \
                     one()
        reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                     filter(JistBuyingPurchaseReqsItems.id==reqitemid). \
                     one()
        shoppingprices = DBS_JistBuying.query(JistBuyingPurchaseReqsItemsShoppingPrices). \
                          filter(JistBuyingPurchaseReqsItemsShoppingPrices.id==shoppingid). \
                          one()
        shoppingprices.approved = 0
        #trolleylist.active = 0
        DBS_JistBuying.flush()
        return 

    @expose()
    def ajaxEditBuyingItem(self,**kw):
        #for k,w in kw.iteritems():
        #    print k,w
        #return
        poorder = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==int(kw['edit_orderno'])). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                        one()
        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.id==int(kw['edit_orderid'])). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        poitems.description = kw['edit_description']  
        poitems.unit = kw['edit_unit'] 
        poitems.quantity =  kw['edit_qty'] 
        poitems.priceexcl =  kw['edit_price'] 
        poitems.totalexcl =  kw['edit_total'] 
        poitems.useridedited = usernow.user_id
        poitems.dateedited = datetime.now() 
        poitemstotal = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==kw['edit_orderno']). \
                value(func.sum(JistBuyingOrderItems.totalexcl))
        poorder.totalexcl = poitemstotal
        totalvat = poitemstotal * VAT_RATE
        totalincl = poitemstotal + totalvat
        poorder.totalvat = totalvat
        poorder.totalincl = totalincl
        return 

    @expose()
    def exportPurchaseOrderBuying(self,ponumber):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
        pdffile = CreatePDF(filename)
        poorder = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.id==int(ponumber)). \
                one()
        supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                        filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                        one()
        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.ponumber==int(ponumber)). \
                all()
        poitems_total_excl = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.ponumber==int(ponumber)). \
                 value(func.sum(JistBuyingOrderList.totalexcl))
        userdata = []
        contractdata = []
        #count = len(wip1) 
        #pointperson_name = User.by_user_id(point).user_name
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        buyername = User.by_user_id(poorder.useridnew)
        #new_orderitem.useridedited = usernow.user_id
        userdata.append([
                        format_decimal(poorder.totalexcl,format='#,##0.00;-#0.00',locale='en'),
                        format_decimal(poorder.totalvat,format='#,##0.00;-#0.00',locale='en'),
                        format_decimal(poorder.totalincl,format='#,##0.00;-#0.00',locale='en'),
                        ])
        for sups in poitems:
            contractdata.append([sups.id,
                sups.description,
                sups.unit,
                sups.quantity,
                sups.priceexcl,
                sups.totalexcl,
                sups.useridnew,
                ])
                #sups.datecreated,
        headers =["Item ID","Description","Unit","Qty","Price","Total Excl"]
        headerwidths=[40,280,80,80,80,100]
        pdffile.CreatePDFPurchaseOrderBuying(userdata,contractdata,headers,headerwidths,supplier,poorder,buyername)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def exportsupplierExpenditureTime(self,fromdate=datetime.date(datetime.now()),todate=datetime.date(datetime.now())):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
        pdffile = CreatePDF(filename)
        userdata = []
        contractdata = []
        #count = len(wip1) 
        #pointperson_name = User.by_user_id(point).user_name
        openorders_total_all = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.podate >= fromdate). \
                     filter(JistBuyingOrderList.podate <= todate). \
                     value(func.sum(JistBuyingOrderList.totalexcl))
        userdata.append([datetime.date(datetime.now()),
                        "Purchase Orders Totals To Suppliers for period From: %s To: %s"%(fromdate, todate),
                         openorders_total_all 
                        ])
        suppliers_all = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.active==True).all()
        for sups in suppliers_all:
            openorders_total = DBS_JistBuying.query(JistBuyingOrderList). \
                         filter(JistBuyingOrderList.active=='Y'). \
                         filter(JistBuyingOrderList.suppliercode==sups.id). \
                         filter(JistBuyingOrderList.podate >= fromdate). \
                         filter(JistBuyingOrderList.podate <= todate). \
                         value(func.sum(JistBuyingOrderList.totalexcl))
            if openorders_total:
                totalexcl = format_decimal(openorders_total ,format='#,##0.00;-#0.00',locale='en')
                contractdata.append([sups.id,sups.suppliername,totalexcl])
        headers =["ID","Supplier Name","Total Excl"]
        headerwidths=[80,250,200]
        pdffile.CreatePDFSupplierExpenditureTime(userdata,contractdata,headers,headerwidths,openorders_total_all)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent


    @expose()
    #@validate(ajax_form)
    def do_search_description(self, **kw):
        #for k,w in enumerate(kw):
        #    print k,w
        sitename = "%(purchase_order_description_search)s" % kw
        searchphrase = "%"+sitename+"%"
        if len(sitename) < 3:
            return "<H1> Type something with more than 2 letters please.</H1>"
        ot = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.description.like(searchphrase)). \
                order_by(desc(JistBuyingOrderItems.id)).limit(500)
        sitedata = "<table class='tablesinglepoint'>"
        headerdata = """
                    <th>ID</th>
                    <th>Date </th>
                    <th>PO Number </th>
                    <th>Req ID</th>
                    <th>Contract</th>
                    <th>Supplier</th>
                    <th>Description</th>
                    <th>Unit</th>
                    <th>Qty</th>
                    <th>Price</th>
                    <th>Total Excl</th>
                    """
        sitedata = sitedata + headerdata
        for k in ot:
            supptemp = DBS_JistBuying.query(JistBuyingSupplierList).filter(JistBuyingSupplierList.id==k.suppliercode).one()
            sitedatatemp = """<tr><td><a href='/productioncont/get_one/%s'>%s</a></td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td>%s</td>
                                <td align="right">%s</td>
                                <td align="right">%s</td>
                                <td align="right">%s</td>
                                <p/></tr>
                            """ % (k.id,k.id,k.podate,k.ponumber,k.reqid,
                                   k.contract,supptemp.suppliername,k.description,
                                   k.unit,k.quantity,k.priceexcl,k.totalexcl)
            sitedata = sitedata +"</p>"+ sitedatatemp
        #return "<p>%s<br/></p>" % k.site
        #return "<p>Recieved Data:<br/>%(name)s<br/></p>" % kw
        sitedata = sitedata +"</table>"
        return sitedata 

    @require(in_any_group("managers","logistics","logistics_manager"))
    @expose('jistdocstore.templates.logistics.rentalconsole')
    def rentalconsole(self,**named):
        """Handle the 'requistion new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        userlist = []
        productionlist = []
        accountslist = []
        for point in activeusers:
            if point:
                if point.user_id == 1:
                    userlist.append({'user_id':point.user_id,
                                      'user_name':point.user_name,
                                      'display_name':point.display_name
                                      })
                user = User.by_user_id(point.user_id)
                userpermissions = user.permissions
                for permis in userpermissions:
                    if permis.permission_name=='production':
                        userlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name,
                                          'display_name':point.display_name
                                          })
        linkedlist = DBS_JistBuying.query(JistBuyingRentalsLink). \
                order_by(desc(JistBuyingRentalsLink.id)). \
                all()
        outputlist = []
        for k in linkedlist:
            supplierone = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==k.supplier_id). \
                    one()
            outputlist.append({
                         'id':k.supplier_id,
                         'supplier_name':supplierone.suppliername,
                         })
        return dict(page='Rental Console',
                    wip = contracts,
                    suppliers = supplierlist,
                    rentalsuppliers = outputlist,
                    production_users = userlist,
                    newreqitemfields = self.newreqitemfields,
                    currentPage=1,
                    value=named,
                    value2=named)



    @require(in_any_group("managers","logistics_manager"))
    @expose('jistdocstore.templates.logistics.buying_linking_console')
    def buying_linking_console(self,**named):
        """Handle the 'buying linking' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        userlist = []
        productionlist = []
        accountslist = []
        return dict(page='Buying Linking Console',
                    wip = contracts,
                    suppliers = supplierlist,
                    production_users = userlist,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose()
    def get_suppliers_minus_rentals_active_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        linkedlist = DBS_JistBuying.query(JistBuyingRentalsLink). \
                order_by(desc(JistBuyingRentalsLink.id)). \
                all()
        linklistids = []
        for m in linkedlist:
            linklistids.append(m.supplier_id)
        outputlist = []
        for k in supplierlist:
            if not k.id in linklistids:
                outputlist.append({
                             'id':k.id,
                             'supplier_name':k.suppliername,
                             })
        headers =["ID","Supplier Name",]
        dictlist = ['id','supplier_name']
        headerwidths=[50,80]
        tdclassnames=['','']
        htmltbl = self.build_buying_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_suppliers_resources")
        html = """
               <h3 class="ui-widget-shadow">All Active Suppliers</h3>  
               """
        return html + htmltbl

    @expose()
    def get_rentals_resources_active_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        outputlist = []
        linkedlist = DBS_JistBuying.query(JistBuyingRentalsLink). \
                order_by(desc(JistBuyingRentalsLink.id)). \
                all()
        for k in linkedlist:
            supplierone = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==k.supplier_id). \
                    one()
            outputlist.append({
                         'id':k.supplier_id,
                         'supplier_name':supplierone.suppliername,
                         })
        headers =["Supplier ID","Supplier Name"]
        dictlist = ['id','supplier_name']
        headerwidths=[50,80,100,100]
        tdclassnames=['','','','','']
        htmltbl = self.build_buying_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_rentals_resources")
        html = """
               <h3 class="ui-widget-shadow">All Active Rental - Hiring Accounts</h3>  
               """
        return html + htmltbl

    @expose()
    def link_buying_to_rentals(self,suppid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        suppone = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.id==suppid). \
                one()
        newlink = JistBuyingRentalsLink()
        newlink.supplier_id = suppid 
        newlink.useridnew = usernow.user_id
        DBS_JistBuying.add(newlink)
        DBS_JistBuying.flush()

    @expose()
    def delink_supplier_from_rentals(self,suppid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        suppone = DBS_JistBuying.query(JistBuyingRentalsLink). \
                filter(JistBuyingRentalsLink.supplier_id==suppid). \
                one()
        DBS_JistBuying.delete(suppone)
        DBS_JistBuying.flush()

    @expose()
    def get_suppliers_minus_maintenance_active_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        supplierlist = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        linkedlist = DBS_JistBuying.query(JistBuyingMaintenanceLink). \
                order_by(desc(JistBuyingMaintenanceLink.id)). \
                all()
        linklistids = []
        for m in linkedlist:
            linklistids.append(m.supplier_id)
        outputlist = []
        for k in supplierlist:
            if not k.id in linklistids:
                outputlist.append({
                             'id':k.id,
                             'supplier_name':k.suppliername,
                             })
        headers =["ID","Supplier Name",]
        dictlist = ['id','supplier_name']
        headerwidths=[50,80]
        tdclassnames=['','']
        htmltbl = self.build_buying_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_suppliers_resources")
        html = """
               <h3 class="ui-widget-shadow">All Active Suppliers</h3>  
               """
        return html + htmltbl

    @expose()
    def get_maintenance_resources_active_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        outputlist = []
        linkedlist = DBS_JistBuying.query(JistBuyingMaintenanceLink). \
                order_by(desc(JistBuyingMaintenanceLink.id)). \
                all()
        for k in linkedlist:
            supplierone = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==k.supplier_id). \
                    one()
            outputlist.append({
                         'id':k.supplier_id,
                         'supplier_name':supplierone.suppliername,
                         })
        headers =["Supplier ID","Supplier Name"]
        dictlist = ['id','supplier_name']
        headerwidths=[50,80,100,100]
        tdclassnames=['','','','','']
        htmltbl = self.build_buying_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_maintenance_resources")
        html = """
               <h3 class="ui-widget-shadow">All Active Maintenance Accounts</h3>  
               """
        return html + htmltbl

    @expose()
    def link_buying_to_maintenance(self,suppid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        suppone = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.id==suppid). \
                one()
        newlink = JistBuyingMaintenanceLink()
        newlink.supplier_id = suppid 
        newlink.useridnew = usernow.user_id
        DBS_JistBuying.add(newlink)
        DBS_JistBuying.flush()

    @expose()
    def delink_supplier_from_maintenance(self,suppid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        suppone = DBS_JistBuying.query(JistBuyingMaintenanceLink). \
                filter(JistBuyingMaintenanceLink.supplier_id==suppid). \
                one()
        DBS_JistBuying.delete(suppone)
        DBS_JistBuying.flush()

    def build_buying_html_table(self,dictlist,headers,headerwidths,outputlist,tdclassnames,tblname):
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
    def purchase_orders_for_supplier_tracked(self,suppliercode):
        todate = datetime.date(datetime.now()) 
        fromdate = datetime.date(datetime.now()) - timedelta(weeks=5)
        dateend = datetime.date(datetime.now()) 
        openorders = DBS_JistBuying.query(JistBuyingOrderList). \
                     filter(JistBuyingOrderList.active=='Y'). \
                     filter(JistBuyingOrderList.podate >= fromdate). \
                     filter(JistBuyingOrderList.podate <= todate). \
                     filter(JistBuyingOrderList.suppliercode==int(suppliercode)). \
                     order_by(desc(JistBuyingOrderList.id)). \
                     all()

        thissupplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                    filter(JistBuyingSupplierList.id==suppliercode).one()

        #userme = User.by_user_id(int(usrid))
        suppliername = thissupplier.suppliername
        outputlist = []
        for order in openorders:
            #thisorder = DBS_JistBuying.query(JistBuyingOrderList). \
                    #filter(JistBuyingOrderList.id==order.ponumber). \
                    #one()
            #print order.id
            poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                    filter(JistBuyingOrderItems.ponumber==order.id). \
                    all()
            for item in poitems:
                print item.reqid 
                #print type(item)
                #for k in item:
                    #print k, w
                #return
                reqsitem = DBS_JistBuying.query(JistBuyingPurchaseReqsItems). \
                         filter(JistBuyingPurchaseReqsItems.id==item.reqid). \
                         one()
                thisbuyer = User.by_user_id(item.useridnew)
                req_by = User.by_user_id(reqsitem.useridnew)
                
                outputlist.append({
                             'supplier_name':suppliername,
                             'po_date':order.podate,
                             'po_number':order.id,
                             'item_description':item.description,
                             'item_unit':item.unit,
                             'item_qty':item.quantity,
                             'buyer':thisbuyer.user_name,
                             'jcno':item.contract,
                             'reqid':item.reqid,
                             'by_user':'',
                             'by_user':req_by.user_name,
                             'tracking':"<img src='/images/False.png'></img>",
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'startdate':"<img src='/images/dates.png'></img>",
                             'showloading':"<img src='/images/clipboard_32.png'></img>",
                             })

        headers =["PO Number",'PO Date','JCNo','Description','Unit','Qty','Req By','','Tracking']
        dictlist = ['po_number','po_date','jcno','item_description','item_unit','item_qty','by_user','spacer','tracking']
        headerwidths=[50,80,50,200,100,100,100,80,100]
        tdclassnames=['','','','','','','','spacer','']
        htmltbl = self.build_buying_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_supplier_last_100_pos")
        html = """
               <h3 class="ui-widget-shadow">Orders To %s [Last 5 Weeks]</h3>  
               """%(suppliername)
        return html + htmltbl

