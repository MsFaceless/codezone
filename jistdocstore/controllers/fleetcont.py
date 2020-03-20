# -*- coding: utf-8 -*-
from tg.decorators import paginate
from tg import expose, flash, require, url, request, redirect, response, tmpl_context
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

from tg.predicates import has_permission,has_any_permission,in_any_group 
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
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
__all__ = ['FleetController']


class FleetController(BaseController):
    """Sample controller-wide authorization"""
    
    def __init__(self):
        self.last_saved_new_fleet = ''

    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage',
    #                            msg=l_('Only for people with the "manage" permission'))

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def index(self):
        redirect('/fleetcont/menu')

    @expose('jistdocstore.templates.fleet.fleetindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        #redirect('/fleetcont/fleet_console')
        return dict(page='Fleet: Main Menu') 

    @expose('jistdocstore.templates.transport.transportconsole')
    def transport_console(self,**named):
        allactivedrivers = DBS_ContractData.query(JistFleetDriverList). \
                filter(JistFleetDriverList.active==1). \
                all()
        allactivefleet = DBS_ContractData.query(JistFleetList). \
                filter(JistFleetList.active==1). \
                all()
        return dict(page='Transport Console',
                    wip = '',
                    activedrivers = allactivedrivers,
                    activefleet = allactivefleet,
                    currentPage=1,
                    value=named,
                    value2=named)

    @expose('jistdocstore.templates.fleet.fleetconsole')
    def fleet_console(self,**named):
        allactivedrivers = DBS_ContractData.query(JistFleetDriverList). \
                filter(JistFleetDriverList.active==1). \
                all()
        allactivefleet = DBS_ContractData.query(JistFleetList). \
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
    @expose('jistdocstore.templates.fleet.transport_all')
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
    @expose('jistdocstore.templates.fleet.newfleet')
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
        DBS_ContractData.add(new_fleet)
        DBS_ContractData.flush()
        self.last_saved_new_fleet = kw['uniqid']

    @expose('jistdocstore.templates.fleet.fleet_edit')
    def edit_fleet(self,*arg,**named):
        val = fleet_edit_filler.get_value(values={'id':arg[0]})
        tmpl_context.widget = edit_fleet_form 
        return dict(page='edit fleet',
                   value=val,
                   action = '/fleetcont/saveeditfleet/'+arg[0],
                   editid = arg[0]
                   )

    @expose()
    def saveeditfleet(self,*arg,**kw):
        editfleet = DBS_ContractData.query(JistFleetList). \
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
    @expose('jistdocstore.templates.fleet.fleet_service_history')
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

    @expose('jistdocstore.templates.fleet.fleet_fuel_usage')
    def fuel_usage(self,**named):
        tmpl_context.widget = choose_fleet_form 
        return dict(page='wip',
                    action='/fleetcont/redirect_fuel_usage')

    @expose()
    def redirect_fuel_usage(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        redirect("/fleetcont/fuel_usage_one/"+kw['registration_number'])

    @expose('jistdocstore.templates.fleet.fleet_fuel_usage_one')
    def fuel_usage_one(self,*arg,**named):
        """Handle the 'fuel usage ' page."""
        #tmpl_context.widget = spx_fleet_fuel_usage 
        #value = fleet_fuel_usage_filler.get_value(values={'id':arg[0],},offset=0,order_by='id',desc=True)
        #limit(100). \
        cont = DBS_ContractData.query(JistFleetFuelUsage). \
                            filter(JistFleetFuelUsage.fleetid==int(arg[0])). \
                            order_by(desc(JistFleetFuelUsage.id)). \
                            all()
        fleetdesc = DBS_ContractData.query(JistFleetList). \
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
    @expose('jistdocstore.templates.fleet.new_fuel_slip')
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
        DBS_ContractData.add(new_fuelslip)
        DBS_ContractData.flush()

        flash("New fuelslip entry successfully saved.")

        redirect("/fleetcont/fuel_usage_one/"+arg[0])

    @expose('jistdocstore.templates.fleet.edit_fuel_slip')
    def edit_fuelslip(self,*arg,**named):
        tmpl_context.widget = edit_fleet_fuel_form 
        val = fuel_edit_filler.get_value(values={'id':arg[0]})
        return dict(page='edit fuelslip',
                   value=val,
                   action = '/fleetcont/saveeditfuelslip/'+arg[0],
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
        editfuelslip = DBS_ContractData.query(JistFleetFuelUsage). \
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
        redirect("/fleetcont/fuel_usage_one/"+kw['fleetid'])

    @expose('jistdocstore.templates.fleet.fleet_driver_list')
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
    @expose('jistdocstore.templates.fleet.new_fleet_driver')
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
        DBS_ContractData.add(new_driver)
        DBS_ContractData.flush()

    @expose('jistdocstore.templates.fleet.edit_fleet_driver')
    def edit_driver(self,*arg,**named):
        tmpl_context.widget = edit_fleet_driver_form 
        val = driver_edit_filler.get_value(values={'id':arg[0]})
        return dict(page='edit driver',
                   value=val,
                   action = '/fleetcont/saveeditdriver/'+arg[0],
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
        editdriver = DBS_ContractData.query(JistFleetDriverList). \
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

    @expose('jistdocstore.templates.fleet.fleet_maintenance_usage')
    def fleet_maintenance_choose(self,**named):
        tmpl_context.widget = choose_fleet_form 
        return dict(page='wip',
                    action='/fleetcont/redirect_maintenance')

    @expose()
    def redirect_maintenance(self,*arg,**kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        redirect("/fleetcont/fleet_maintenance_list/"+kw['registration_number'])

    @expose('jistdocstore.templates.fleet.fleet_maintenance_list')
    def fleet_maintenance_list(self,*arg,**named):
        #tmpl_context.widget = spx_fleet_maintenance 
        cont = DBS_ContractData.query(JistFleetMaintenanceList). \
                            filter(JistFleetMaintenanceList.fleetid==int(arg[0])). \
                            order_by(desc(JistFleetMaintenanceList.id)). \
                            all()
        fleetdesc = DBS_ContractData.query(JistFleetList). \
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
    @expose('jistdocstore.templates.fleet.new_fleet_maintenance')
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
        DBS_ContractData.add(new_maintenance)
        DBS_ContractData.flush()

        flash("New maintenance entry successfully saved.")

        redirect("/fleetcont/fleet_maintenance_list/"+str(fleetid))


    @expose('jistdocstore.templates.fleet.edit_fleet_maintenance')
    def edit_maintenance(self,*arg,**named):
        tmpl_context.widget = edit_fleet_maintenance_form 
        val = maintenance_edit_filler.get_value(values={'id':arg[0]})
        return dict(page='edit maintenance',
                   value=val,
                   action = '/fleetcont/saveeditmaintenance/'+arg[0],
                   editid = arg[0]
                   )

    @expose()
    #@validate(edit_supplier_form,edit_supplier)
    def saveeditmaintenance(self,*arg,**kw):
        del kw['sprox_id']
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridedited = usernow.user_id
        editmaintenance = DBS_ContractData.query(JistFleetMaintenanceList). \
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
        redirect("/fleetcont/fleet_maintenance_list/"+kw['fleetid'])

    #@require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose('jistdocstore.templates.fleet.search_fleet_fuel')
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
        fuelslips = DBS_ContractData.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                              order_by(desc(JistFleetFuelUsage.transaction_date)).  \
                                              all()
        #print fuelslips
        fuelslips_sum = DBS_ContractData.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
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
                        href='/fleetcont/export_fleet_fuel_pdf/%s/%s'><p/> 
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
            fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
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
        fuelslips = DBS_ContractData.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                              order_by(desc(JistFleetFuelUsage.transaction_date)).  \
                                              all()
        fuelslips_sum = DBS_ContractData.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.transaction_date>=startdate). \
                                              filter(JistFleetFuelUsage.transaction_date<=enddate). \
                                             value(func.sum(JistFleetFuelUsage.amount))
        locale.setlocale(locale.LC_ALL, '')
        #return
        if not fuelslips_sum:
            totalexcl = 0.00
        else:
            totalexcl = locale.format('%.2f',fuelslips_sum,grouping=True,monetary=True)
        for k in fuelslips:
            fleettemp = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==k.fleetid).one()
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
        fleetlist = DBS_ContractData.query(JistFleetList). \
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
            drv = DBS_ContractData.query(JistFleetDriverList). \
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
        fleetlist = DBS_ContractData.query(JistFleetList). \
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
            drv = DBS_ContractData.query(JistFleetDriverList). \
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
        fleetone = DBS_ContractData.query(JistFleetList). \
              filter(JistFleetList.id==fleetid). \
                            one()
        allactivedrivers = DBS_ContractData.query(JistFleetDriverList). \
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
        driverlist = DBS_ContractData.query(JistFleetDriverList). \
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
        driverone = DBS_ContractData.query(JistFleetDriverList). \
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

    @expose()
    def get_fleet_resources_active_html(self):
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

    @expose()
    def get_transport_resources_active_html(self):
        wip1 = []
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        fleetlist = DBS_JistFleetTransport.query(JistTransportFleetLink). \
                order_by(desc(JistTransportFleetLink.id)). \
                all()
        outputlist = []
        for k in fleetlist:
            fleetone = DBS_JistFleetTransport.query(JistFleetList). \
                    filter(JistFleetList.id==k.fleet_id). \
                    one()
            thisdriver = DBS_JistFleetTransport.query(JistFleetDriverList). \
                    filter(JistFleetDriverList.id==fleetone.driver). \
                    one()
            outputlist.append({
                         'id':k.fleet_id,
                         'fleet_name':fleetone.vehicle_description,
                         'registration_number':fleetone.registration_number,
                         'driver':thisdriver.driver_name,
                         })
        headers =["Fleet ID","Registration","Description","Driver"]
        dictlist = ['id','registration_number','fleet_name','driver']
        headerwidths=[50,80,100,100]
        tdclassnames=['','','','','']
        htmltbl = self.build_transport_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_transport_resources")
        html = """
               <h3 class="ui-widget-shadow">All Active Transport Vehicles</h3>  
               """
        return html + htmltbl

    @expose()
    def link_fleet_to_transport(self,fleetid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        fleetone = DBS_JistFleetTransport.query(JistFleetList). \
                filter(JistFleetList.id==fleetid). \
                one()
        newlink = JistTransportFleetLink()
        newlink.fleet_id = fleetid
        newlink.useridnew = usernow.user_id
        DBS_JistFleetTransport.add(newlink)
        DBS_JistFleetTransport.flush()

    @expose()
    def delink_fleet_from_transport(self,fleetid):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        fleetone = DBS_JistFleetTransport.query(JistTransportFleetLink). \
                filter(JistTransportFleetLink.fleet_id==fleetid). \
                one()
        DBS_JistFleetTransport.delete(fleetone)
        DBS_JistFleetTransport.flush()

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
                print htmltemp1
                htmltbl = htmltbl + htmltemp1
            htmltbl = htmltbl + "</tr>" 
        htmltbl = htmltbl + "</table>"
        return htmltbl 

    def getthumbnail(self, inpath, outpath):
        retcode = subprocess.call(['convert',inpath,'-resize','50!x50!',outpath])
