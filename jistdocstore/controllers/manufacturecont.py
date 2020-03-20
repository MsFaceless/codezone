# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
from tg.decorators import paginate

#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
#from tw.jquery import AjaxForm
#from tw.jquery import FlexiGrid
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
from jistdocstore.lib.jist_generic_reportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import FileStoreProduction
from jistdocstore.model import DBS_JistBuying, metadata5
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
from babel.numbers import format_currency, format_number, format_decimal
from bs4 import BeautifulSoup

public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
__all__ = ['ManufacturingController']


class ManufacturingController(BaseController):
    """Sample controller-wide authorization"""
    
    #The predicate that must be met for all the actions in this controller:
    #allow_only = has_any_permission('manage','manufacturing',
                                #msg=l_('Only for people with the "manage" permission'))
    def __init__(self):
        self.Allmatlistdata = ['Choose One','Round Tubing','Sq-Rect Tubing','Unequal Angle','Equal Angle','IPE',
                               'Flats','Round Bar','Octagonal Bar','Hexagonal Bar','Square Bar',
                               'Sheet to 4mm','Sheet from 4.5mm','Non Standard Item']

    @expose()
    def index(self):
        redirect('manufacturecont/menu')

    @expose('jistdocstore.templates.jjmc.manufacturingindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='JJMC Main Menu') 

    @expose('jistdocstore.templates.jjmc.manuf_orders_console')
    def orders_console(self,**named):
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
        return dict(page='JJMC Orders Console',
                    contracts = contracts,
                    users = activeusers,
                    boq = boq,
                    myjistid = myid,
                    sites = sites
                    )

    @expose('jistdocstore.templates.jjmc.manuf_raw_mat_console')
    def raw_material_console(self,**named):
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
        uneq_angle_data = DBS_JistManufacturing.query(JistManufactureAngleNonEqualData).all()
        eq_angle_data = DBS_JistManufacturing.query(JistManufactureAngleEqualData).all()
        ipe_data = DBS_JistManufacturing.query(JistManufactureIPEData).all()
        flats_data = DBS_JistManufacturing.query(JistManufactureFlatsData).all()
        return dict(page='JJMC Raw Material Console',
                    contracts = contracts,
                    users = activeusers,
                    boq = boq,
                    myjistid = myid,
                    sites = sites
                    )

    @expose('jistdocstore.templates.jjmc.manuf_process_console')
    def manufacture_process_console(self,**named):
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
        return dict(page='JJMC Process Flow Console',
                    contracts = contracts,
                    users = activeusers,
                    boq = boq,
                    myjistid = myid,
                    sites = sites
                    )

    @expose()
    def get_raw_mat_data(self,**named):
        formupdate3 = """
                   <h3 class="ui-widget-shadow">Component To Add To Manufacturing Item List</h3> 
                   <form id = 'material_calc_form'>
                      <div='choose_material_group'>
                      <fieldset>
                      <label for="%s">%s</label>
                      <select id="select_raw_mat_group" name="select_raw_mat_group" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("select_raw_mat_group","Choose Raw Material Group To Use:")
        for i,sts in enumerate(self.Allmatlistdata):
            formupdate3temp = """
                            <option value="%s">%s </option>
                              """%(i,sts)
            formupdate3 = formupdate3 + formupdate3temp 
        formupdate3 = formupdate3 + "</select><div id='choose_material_each'></div></fieldset></form></div>"
        return formupdate3

    @expose()
    def get_raw_mat_data_each(self,**kw):
        groupid = kw['groupid']
        txtboxes = """
                    <label for="length">Length Required(mm)</label>
                    <input type="text" name="length" id="length" class="text ui-widget-content ui-corner-all" />
                    <label for="quantity">Quantity Required</label>
                    <input type="text" name="quantity" id="quantity" class="text ui-widget-content ui-corner-all" />
                    <label for="stand_len">Standard Supplier Lens(mm)</label>
                    <input type="text" name="stand_len" id="stand_len" class="text ui-widget-content ui-corner-all" />
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_add_component_to_item">Add Component To Item List</button> <br/>
                    <label for="mass_kg">Mass kg/m</label>
                    <input type="text" name="mass_kg" id="mass_kg" class="text ui-widget-content ui-corner-all" />
                  """
        rndboxes = """
                    <label for="diameter">Diameter(mm)</label>
                    <input type="text" name="diameter" id="diameter" class="text ui-widget-content ui-corner-all" />
                    <label for="thickness">Thickness(mm)</label>
                    <input type="text" name="thickness" id="thickness" class="text ui-widget-content ui-corner-all" />
                    <label for="length">Length Required (mm)</label>
                    <input type="text" name="length" id="length" class="text ui-widget-content ui-corner-all" />
                    <label for="quantity">Quantity Required</label>
                    <input type="text" name="quantity" id="quantity" class="text ui-widget-content ui-corner-all" />
                    <label for="stand_len">Standard Supplier Lens(mm)</label>
                    <input type="text" name="stand_len" id="stand_len" class="text ui-widget-content ui-corner-all" />
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_add_component_to_item">Add Component To Item</button> <br/>
                    <label for="mass_kg">Mass kg/m</label>
                    <input type="text" name="mass_kg" id="mass_kg" class="text ui-widget-content ui-corner-all" />
                  """
        rectboxes = """
                    <label for="width">Width(mm)</label>
                    <input type="text" name="width" id="width" class="text ui-widget-content ui-corner-all" />
                    <label for="height">Height(mm)</label>
                    <input type="text" name="height" id="height" class="text ui-widget-content ui-corner-all" />
                    <label for="thickness">Thickness(mm)</label>
                    <input type="text" name="thickness" id="thickness" class="text ui-widget-content ui-corner-all" />
                    <label for="length">Length Required (mm)</label>
                    <input type="text" name="length" id="length" class="text ui-widget-content ui-corner-all" />
                    <label for="quantity">Quantity Required</label>
                    <input type="text" name="quantity" id="quantity" class="text ui-widget-content ui-corner-all" />
                    <label for="stand_len">Standard Supplier Lens(mm)</label>
                    <input type="text" name="stand_len" id="stand_len" class="text ui-widget-content ui-corner-all" />
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_add_component_to_item">Add Component To Item List</button> <br/>
                    <label for="diameter">Diameter</label>
                    <input type="text" name="diameter" id="diameter" class="text ui-widget-content ui-corner-all" />
                    <label for="mass_kg">Mass kg/m</label>
                    <input type="text" name="mass_kg" id="mass_kg" class="text ui-widget-content ui-corner-all" />
                  """
        sheetboxes = """
                    <label for="width">Width(mm)</label>
                    <input type="text" name="width" id="width" class="text ui-widget-content ui-corner-all" />
                    <label for="height">Height(mm)</label>
                    <input type="text" name="height" id="height" class="text ui-widget-content ui-corner-all" />
                    <label for="thickness">Thickness(mm)</label>
                    <input type="text" name="thickness" id="thickness" class="text ui-widget-content ui-corner-all" />
                    <label for="quantity">Quantity Required</label>
                    <input type="text" name="quantity" id="quantity" class="text ui-widget-content ui-corner-all" />
                    <label for="stand_len">Standard Supplier Sizes(mm)</label>
                    <input type="text" name="stand_len" id="stand_len" class="text ui-widget-content ui-corner-all" />
                    <button class="ui-widget ui-widget-content ui-state-default" id="button_add_component_to_item">Add Component To Item List</button> <br/>
                    <label for="mass_kg">Mass kg/each</label>
                    <input type="text" name="mass_kg" id="mass_kg" class="text ui-widget-content ui-corner-all" />
                  """
                  
        if groupid == str(1):  #Round Material
            return rndboxes
        elif groupid == str(2): #Square Rectangle
            return rectboxes 
        elif groupid == str(3): #Unequal Angle
            uneq_angle_data = DBS_JistManufacturing.query(JistManufactureAngleNonEqualData).all()
            formupdate3 = """
                          <label for="%s">%s</label>
                          <select id="id_mat_dropdown" mattype="Unequal_Angle" name="id_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("id_mat_dropdown","Choose An Unequal Angle")
            for sts in uneq_angle_data:
                formupdate3temp = """
                                <option weight="%s" value="%s">%s x %s x %s</option>
                                  """%(sts.mass_kg_m,sts.id,sts.width,sts.height,sts.thickness)
                formupdate3 = formupdate3 + formupdate3temp 
            formupdate3 = formupdate3 + "</select>"
            return formupdate3 + txtboxes
        elif groupid == str(4): #Equal Angle
            eq_angle_data = DBS_JistManufacturing.query(JistManufactureAngleEqualData).all()
            formupdate3 = """
                          <label for="%s">%s</label>
                          <select id="id_mat_dropdown" name="id_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("id_mat_dropdown","Choose An Equal Angle")
            for sts in eq_angle_data:
                formupdate3temp = """
                                <option value="%s">%s x %s x %s</option>
                                  """%(sts.id,sts.width,sts.height,sts.thickness)
                formupdate3 = formupdate3 + formupdate3temp 
            formupdate3 = formupdate3 + "</select>"
            return formupdate3 + txtboxes
        elif groupid == str(5): #IPE
            ipe_data = DBS_JistManufacturing.query(JistManufactureIPEData).all()
            formupdate3 = """
                          <label for="%s">%s</label>
                          <select id="id_mat_dropdown" name="id_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("id_mat_dropdown","Choose An IPE")
            for sts in ipe_data:
                formupdate3temp = """
                                <option value="%s">%s x %s x %s</option>
                                  """%(sts.id,sts.width,sts.height,sts.thickness)
                formupdate3 = formupdate3 + formupdate3temp 
            formupdate3 = formupdate3 + "</select>"
            return formupdate3 + txtboxes
        elif groupid == str(6): #Flats
            flats_data = DBS_JistManufacturing.query(JistManufactureFlatsData).all()
            formupdate3 = """
                          <label for="%s">%s</label>
                          <select id="id_mat_dropdown" name="id_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("id_mat_dropdown","Choose A Flat")
            for sts in flats_data:
                formupdate3temp = """
                                <option value="%s">%s x %s </option>
                                  """%(sts.id,sts.width,sts.thickness)
                formupdate3 = formupdate3 + formupdate3temp 
            formupdate3 = formupdate3 + "</select>"
            return formupdate3 + txtboxes
        elif groupid == str(7) or groupid==str(9) or groupid==str(10): #Round Bar ,Hexagonal, Square
            formupdate3 = """
                          <label for="%s">%s</label>
                          <input id="diameter" name="diameter" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("diameter","Diameter")
            return formupdate3 + txtboxes
        elif groupid == str(8) : #Octagonal
            formupdate3 = """
                          <label for="%s">%s</label>
                          <input id="thickness" name="thickness" style="display: block" class="text ui-widget-content ui-corner-all">
                          <label for="%s">%s</label>
                          <input id="diameter" name="diameter" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("thickness","Thickness","diameter","Diameter")
            return formupdate3 + txtboxes
        elif groupid == str(11) : #Sheets <= 4mm
            return sheetboxes 
        elif groupid == str(12) : #Sheets > 4,5mm
            return sheetboxes 
        elif groupid == str(13) : #Non Standard Item
            formupdate3 = """
                          <label for="%s">%s</label>
                          <input id="id_mat_dropdown" mattype="Non Standard" name="id_mat_dropdown" style="display: block" class="text ui-widget-content ui-corner-all">
                                """% ("id_mat_dropdown","Non Standard")

            return formupdate3 + rectboxes 
        else:
            return
    
    @expose()
    def get_material_item_weight(self,**kw):
        groupid = kw['groupid']
        listid = kw['listid']
        if groupid == str(1):  #Rounds
            pass
        elif groupid == str(2): #Rect
            pass
        elif groupid == str(3): #Unequal Angle
            uneq_angle_data = DBS_JistManufacturing.query(JistManufactureAngleNonEqualData). \
                    filter(JistManufactureAngleNonEqualData.id == listid).one()
            return uneq_angle_data.mass_kg_m
        elif groupid == str(4): #Equal Angle
            eq_angle_data = DBS_JistManufacturing.query(JistManufactureAngleEqualData). \
                    filter(JistManufactureAngleEqualData.id == listid).one()
            return eq_angle_data.mass_kg_m
        elif groupid == str(5): #IPE
            ipe_data = DBS_JistManufacturing.query(JistManufactureIPEData). \
                    filter(JistManufactureIPEData.id == listid).one()
            return ipe_data.mass_kg_m
        elif groupid == str(6): #Flats
            flats_data = DBS_JistManufacturing.query(JistManufactureFlatsData). \
                    filter(JistManufactureFlatsData.id == listid).one()
            return flats_data.mass_kg_m
        else:
            return "None"

    @expose()
    def get_material_rounds_weight(self,**kw):
        diameter = kw['diameter']
        thickness = kw['thickness']
        if isnumeric(diameter) and isnumeric(thickness):
            dia = float(diameter)
            thik = float(thickness)
            weight = (dia-thik)*thik*0.02466
            return str(weight)
        return str("None")

    @expose()
    def get_material_sqrect_weight(self,**kw):
        diameter = kw['diameter']
        thickness = kw['thickness']
        if isnumeric(diameter) and isnumeric(thickness):
            dia = float(diameter)
            thik = float(thickness)
            weight = (dia)-(thik*thik)*0.02466
            return str(weight)
        return str("None")

    @expose()
    def get_material_solids_weight(self,**kw):
        diameter = kw['diameter']
        groupid = kw['groupid']
        if groupid == str(7):  # Round Bar
            if isnumeric(diameter):
                dia = float(diameter)
                weight = (dia)*(dia)*0.00616
                return str(weight)
        if groupid == str(8):  #Octagonal  
            thickness = kw['thickness']
            if isnumeric(diameter):
                dia = float(diameter)
                thickness = float(thickness)
                weight = (dia)*(thickness)*0.00651
                return str(weight)
        if groupid == str(9):  #Hexagonal  
            if isnumeric(diameter):
                dia = float(diameter)
                weight = (dia)*(dia)*0.0068
                return str(weight)
        if groupid == str(10):  #Square Bar 
            if isnumeric(diameter):
                dia = float(diameter)
                weight = (dia)*(dia)*0.00787
                return str(weight)
        return str("None")

    @expose()
    def get_material_sheets_weight(self,**kw):
        width = kw['width']
        height = kw['height']
        thickness = kw['thickness']
        groupid = kw['groupid']
        if groupid == str(11):  # Below 4.5mm
            if isnumeric(width):
                width = float(width)
                height = float(height)
                thickness = float(thickness)
                weight = (width/1000)*(height/1000)*thickness*8.039
                return str(weight)
        if groupid == str(12):  #Above 4.5mm  
            if isnumeric(width):
                width = float(width)
                height = float(height)
                thickness = float(thickness)
                weight = (width/1000)*(height/1000)*thickness*7.85
                return str(weight)
        return str("None")


    @expose()
    def get_skeleton_component_factory(self,**named):
        formupdate3 = """
                   <h3 class="ui-widget-shadow">Component List - To Create New Item: </h3> 
                      <fieldset>
                        <label for="">Name Of New Item:</label>
                        <input type="text" name="item_name" id="item_name" class="text ui-widget-content ui-corner-all" />
                      <table id='tbl_component_list'>
                      <th>Group ID</th>
                      <th>Group Name</th>
                      <th>Material ID</th>
                      <th>Material Name</th>
                      <th>Diameter</th>
                      <th>Thickness</th>
                      <th>Width</th>
                      <th>Height</th>
                      <th>Length</th>
                      <th>Mass kg/m</th>
                      <th>Supplier Lens</th>
                      <th>Quantity Required</th>
                      <th>Delete</th>
                              """
        formupdate3 = formupdate3 + "</table>"
        buttonadd = """<button class="ui-widget ui-widget-content ui-state-default" id="button_add_item_to_list">Add Item To Manufacturing List</button>"""
        return formupdate3 + buttonadd+'</fieldset>'

    @expose()
    def get_table_data_manufacturing_list(self,**kw):
        stndlist = DBS_JistManufacturing.query(JistManufactureStandardList). \
               order_by(desc(JistManufactureStandardList.id)).all()
        outputlist = []
        for item in stndlist:
            outputlist.append({
                               'id':item.id ,
                               'description':item.description,
                               'add':"<img id='add_manufacturing_item' src='/images/shopping_basket_add_32.png'></img>",
                               'edit':"<img id='delete_manufacturing_item' src='/images/edit-4.png'></img>",
                               'trash':"<img id='delete_manufacturing_item' src='/images/trash.png'></img>",
                               'pdf':"<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_manufacturing_item' src='/images/pdficon.jpg'></img></a>".format(item.id),
                               'open':"<img id='open_manufacturing_item' src='/images/project-open.png'></img>",
                               'spacer':''
                               })
        headers =["ID","Description","Add","Edit","","","Open"]
        dictlist = ['id','description','add','edit','spacer','spacer','open']
        headerwidths=[30,'',30,30,30,10,10,30,30,30,30,30]
        tdclassnames=['','','','','tdspacer','tdspacer','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_manufacturing_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_comp_list")
        #return htmltbl
        header = """<h4 class="modal-content"> Standard Item List</h4>"""
                  
        return header + "<div id='divstandardmatlist'>" + htmltbl + "</div><div id='divstandardmatlistitems'></div>"  

    @expose()
    def get_table_data_manufacturing_item(self,**kw):
        itemid = kw['itemid']
        item = DBS_JistManufacturing.query(JistManufactureStandardList). \
               filter(JistManufactureStandardList.id== itemid).one()
        items = DBS_JistManufacturing.query(JistManufactureStandardListItems). \
               filter(JistManufactureStandardListItems.listid== itemid).all()
        description = item.description
        outputlist = []
        grandtotalkg = 0
        for it in items:
            thistotalkg = float(it.qty_req)*float(it.length)/1000*float(it.weight)
            grandtotalkg = grandtotalkg + thistotalkg 
            outputlist.append({
                               'id':it.id ,
                               'groupname':it.groupname ,
                               'materialname':it.materialname,
                               'diameter':it.diameter,
                               'thickness':it.thickness,
                               'width':it.width,
                               'length':it.length,
                               'height':it.height,
                               'weight':it.weight,
                               'supp_lens':it.supp_lens,
                               'qty_req':it.qty_req,
                               'total_kgs':"{0:10.2f}".format(thistotalkg),
                               'trash':"<img id='delete_manufacturing_item' src='/images/trash.png'></img>",
                               })

        headers =["ID","Group Name","Material Name","Diameter","Thickness","Width","Height","Length","Kg/m","Supplier","Qty Req","Total Kgs","Delete"]
        dictlist = ['id','groupname','materialname','diameter','thickness','width','height','length','weight','supp_lens','qty_req','total_kgs','trash']
        headerwidths=[50,150,150,90,50,50,80,50,50,50,50,50,50]
        tdclassnames=['','','','','','','','','','','tdspacer','tdspacer','','tdrightalign']
        htmltbl = self.build_manufacturing_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_comp_list_items")
        pdfstring = "<a href='/manufacturecont/export_standard_item_list_pdf/{0}'><img id='print_manufacturing_item' src='/images/pdficon.jpg'></img></a>".format(item.id)
        header = """<h4 class="modal-content"> Component List: ID - {0} - {1} <span class='spanright'> {2:10.2f} kgs {3}</span></h4>""".format(itemid,description,grandtotalkg,pdfstring)
                
        return header + htmltbl 

    @expose()
    def delete_standard_list_item(self,**kw):
        itemid = kw['itemid']
        items = DBS_JistManufacturing.query(JistManufactureStandardListItems). \
               filter(JistManufactureStandardListItems.id== itemid).one()
        DBS_JistManufacturing.delete(items)
        DBS_JistManufacturing.flush()

    @expose()
    def post_table_data_manufacturing_item(self,**kw):
        data_list = []
        data_listall = []
        #for k, w in kw.iteritems():
            #print  k,w
        #table_data = [cell.text for cell in row("td")]
        #tr_data = [row.context for row in BeautifulSoup(kw['rows'])("tr")]
        itemname = kw['item_name']
        row_data = [cell.text for cell in BeautifulSoup(kw['rows'])("td")]
        norows = len(row_data)/13
        thisdatarows = []
        startpos = 0
        endpos = 13
        tdsize = 13
        for i in range(1,norows+1):
            thismoretemp = row_data[startpos:endpos]
            thisdatarows.append(thismoretemp)
            startpos = i * tdsize 
            endpos = startpos +  tdsize
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        list_item = JistManufactureStandardList()
        list_item.description = itemname
        list_item.useridnew = usernow.user_id
        list_item.useridedited = usernow.user_id
        DBS_JistManufacturing.add(list_item)
        DBS_JistManufacturing.flush()
        itemlist = DBS_JistManufacturing.query(JistManufactureStandardList). \
                filter(JistManufactureStandardList.id == list_item.id). \
                one()
        for data_list in thisdatarows:
            #print row
            item = JistManufactureStandardListItems()
            item.listid = itemlist.id 
            item.groupid = data_list[0]
            item.groupname = data_list[1]
            #item.materialid = data_list[2]
            item.materialname = data_list[3]
            item.diameter = data_list[4]
            item.thickness = data_list[5]
            item.width = data_list[6]
            item.height = data_list[7]
            item.length = data_list[8]
            item.weight = data_list[9]
            item.supp_lens = data_list[10]
            item.qty_req = data_list[11]
            item.useridnew = usernow.user_id
            item.useridedited = usernow.user_id
            DBS_JistManufacturing.add(item)
        DBS_JistManufacturing.flush()

    @expose()
    def export_standard_item_list_pdf(self,listid, **kw):
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
        fname = "Manufacturing-Item-"+ datename +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        pdffile = CreatePDFA4(filename)
        wip1 = []
        userdata = {}
        outputdata = []
        outputlist = []
        #reqid = kw['reqid']
        item = DBS_JistManufacturing.query(JistManufactureStandardList). \
               filter(JistManufactureStandardList.id== listid).one()
        items = DBS_JistManufacturing.query(JistManufactureStandardListItems). \
               filter(JistManufactureStandardListItems.listid== listid).all()
        description = item.description
        outputlist = []
        thistotalkg = 0
        grandtotalkg = 0
        for k in items:
            outputdata.append({
                         'id':k.id,
                         'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                         'dateadded': k.dateadded,
                         'dateedited': k.dateedited,
                         })
        for x in items:
            thistotalkg = float(x.qty_req)*float(x.length)/1000*float(x.weight)
            grandtotalkg = grandtotalkg + thistotalkg 
            outputlist.append((
                             x.id,
                             Paragraph(checknullvalue(x.groupname),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.materialname),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.diameter),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.thickness),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.width),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.height),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.length),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.weight),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.supp_lens),pdffile.styleNormal),
                             Paragraph(checknullvalue(x.qty_req),pdffile.styleNormal),
                             "{0:10.2f}".format(thistotalkg),
                              ))
        userdata = {
                'title1_header':'Manufacturing:', 'title1':'Standard Manufactured Item ',
                'title2_header':'Material Component List', 'title2':'',
                'title3_header':'Item Description:', 'title3':item.description,
                'title4_header':'Item ID', 'title4':str(item.id),
                'datenow_header': "Date Printed:", 'datenow':datetime.date(datetime.now()),
                'headerl1_header':'', 'headerl1':'',
                'headerl2_header':'Total Kgs', 'headerl2':"{0:10.2f}".format(grandtotalkg),
                'headerl3_header':'', 'headerl3':'',
                'headerl4_header':'', 'headerl4':' ',
                'id_header_header': "", 'id_header':'',
                'headerr1_header':'', 'headerr1':'',
                'headerr2_header':'', 'headerr2':'',
                'headerr3_header':'', 'headerr3':'',
                'headerr4_header':'', 'headerr4':' ',
                } 
        headers =["ID","Group Name","Material Name","Diameter","Thickness","Width","Height","Length","KG/M","Supplier Lens","Qty Cut Lens Req","Total KG's"]
        headerwidths=[50,90,90,50,50,50,50,50,50,70,90,70,32,21]
        pdffile.CreatePDFGenericReport(userdata,outputlist,headers,headerwidths,11)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent


    @expose()
    def get_jjmc_order_list(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        endtoday = datetime.date(datetime.now()) - timedelta(weeks=10)
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(endtoday,sttimestart)
        enddate = datetime.combine(datetime.now(),sttimeend)
        kw['supplier_name'] = 682 
        suppliercode = "%(supplier_name)s" % kw
        #print startdate, enddate
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
        suppliername = supn.suppliername
        locale.setlocale(locale.LC_ALL, '')
        outputlist =[]
        for poorder in openorders:
            supplier = DBS_JistBuying.query(JistBuyingSupplierList). \
                            filter(JistBuyingSupplierList.id==int(poorder.suppliercode)). \
                            one()
            poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                    filter(JistBuyingOrderItems.ponumber==int(poorder.id)). \
                    all()
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
                #check if item exist in manufacturing schedule
                try:
                    itemlist = DBS_JistManufacturing.query(JistManufactureOrderItems). \
                            filter(JistManufactureOrderItems.jist_po_itemid == item.id). \
                            one()
                    if itemlist.active_production == 1:
                        statehml = self.produce_state_inmanufacturing(True)
                    else:
                        statehml = self.produce_state_inmanufacturing(False)
                except:
                    statehml = self.produce_state_inmanufacturing(False)

                htmlitems = ''
                htmldetails = ''
                outputlist.append({'id': item.id,
                                   'po_number': str(poorder.id),
                                   'contracts': str(item.contract),
                                   'po_date': str(item.podate), 
                                   'supplier_name': supplier.suppliername,
                                   'description': item.description,
                                   'unit':item.unit,
                                   'quantity':item.quantity,
                                   'this_user':thisuser,
                                   'grv_qty_total':grvitemsqtytotal,
                                   'grv_balance':grvbalance,
                                   'userid_new':item.useridnew,
                                   'state':statehml
                                   })
        headers =["ID","PO-No","JCNo","Date","Supplier","Description","Unit","Ordered","Delivered","Balance","In Production"]
        dictlist = ['id','po_number','contracts','po_date','supplier_name','description','unit','quantity','grv_qty_total','grv_balance','state']
        headerwidths=[50,50,50,90,50,'',50,50,50,50,50,50]
        tdclassnames=['','','','','','','','','','tdspacer','','','']
        htmltbl = self.build_manufacturing_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_jjmc_orderlist")
        return htmltbl

    @expose()
    def get_jjmc_progress_list(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        endtoday = datetime.date(datetime.now()) - timedelta(weeks=10)
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(endtoday,sttimestart)
        outputlist =[]
        poitems = DBS_JistManufacturing.query(JistManufactureOrderItems). \
                filter(JistManufactureOrderItems.active_production==1). \
                order_by(desc(JistManufactureOrderItems.id)). \
                all()
        htmlitems = ''
        htmldetails = ''
        for item in poitems:
            outputlist.append({'id': item.id,
                               'po_number': item.jist_po,
                               'description': item.description,
                               'unit':item.unit,
                               'quantity':item.qty,
                               'userid_new':item.useridnew,
                               'date_added':item.dateadded,
                               })
        headers =["ID","PO-Number","Date","Description","Unit","Ordered"]
        dictlist = ['id','po_number','date_added','description','unit','quantity']
        headerwidths=[50,50,90,'',50,80,50,50,50,50,50]
        tdclassnames=['','','','','','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_manufacturing_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_jjmc_progresslist")
        return htmltbl

    @expose()
    def get_jjmc_progress_stages(self,**kw):
        man_orderid = kw['order_id']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        thisuseridnew = usernow.user_id
        endtoday = datetime.date(datetime.now()) - timedelta(weeks=10)
        sttimestart = time(0,0,0)
        sttimeend = time(23,59,59)
        startdate = datetime.combine(endtoday,sttimestart)
        outputlist =[]
        poitem = DBS_JistManufacturing.query(JistManufactureOrderItems). \
                filter(JistManufactureOrderItems.id==man_orderid). \
                one()
        manstages =DBS_JistManufacturing.query(JistManufacturingStages).all()
        #Create html accordion for stages
        html1 = """<div id="process_flow_accordion">"""
        html2 = ''
        htmltemp = ''
        man_stages_list = []
        for stage in manstages:
            poqties = DBS_JistManufacturing.query(JistManufacturingWorkFlow). \
                filter(JistManufacturingWorkFlow.man_order_id==man_orderid). \
                filter(JistManufacturingWorkFlow.man_stage_id==stage.id). \
                value(func.sum(JistManufacturingWorkFlow.man_stage_qty))
            man_poitems = DBS_JistManufacturing.query(JistManufacturingWorkFlow). \
                filter(JistManufacturingWorkFlow.man_order_id==man_orderid). \
                filter(JistManufacturingWorkFlow.man_stage_id==stage.id). \
                all()
            if not poqties: poqties = 0
            man_transactions = ''
            for manpo in man_poitems:
                man_stage =DBS_JistManufacturing.query(JistManufacturingStages). \
                        filter(JistManufacturingStages.id==stage.id).one()
                usernow = User.by_user_id(manpo.useridnew)
                thisusername = usernow.user_name
                man_transactionstemp = """
                                    <li>{0} Unit(s) was / were moved by {1} on {2} : {3}</li>

                                   """.format(manpo.man_stage_qty,thisusername,manpo.dateadded,man_stage.name)
                man_transactions = man_transactions + man_transactionstemp
                man_stages_list.append(man_transactionstemp)
            htmltemp = """
                        <div class='accord_header'>
                        <h3>{0}<span class='accord_qty'>{1}</span></h3>
                            <div>
                                <button class="button_move_on" man_po_item="{3}" man_stage_id="{4}">Move Units</button>
                                {2}
                            </div>
                        </div>

                       """.format(stage.name,
                               poqties,
                               man_transactions,
                               man_orderid,
                               stage.id,
                               )
            html2 = html2 + htmltemp
        html3 = "</div>"
        htmlitems = ''
        htmldetails = ''
        #for item in poitems:
        outputlist.append({'id': poitem.id,
                           'po_number': poitem.jist_po,
                           'description': poitem.description,
                           'unit':poitem.unit,
                           'quantity':poitem.qty,
                           'userid_new':poitem.useridnew,
                           'date_added':poitem.dateadded,
                           })
        headers =["ID","PO-Number","Date","Description","Unit","Ordered"]
        dictlist = ['id','po_number','date_added','description','unit','quantity']
        headerwidths=[50,50,90,'',50,80,50,50,50,50,50]
        tdclassnames=['','','','','','tdrightalign','','','','tdspacer','','','']
        htmltbl = self.build_manufacturing_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_jjmc_progresslist")
        #return htmltbl
        header = """<h4 class="modal-content"> Workflow</h4>"""
        accordionhtml =  html1 + html2 + html3
        htmla = """<div id="process_flow_accordion_sum">"""
        man_transactionshtml =''
        for manpo in man_stages_list:
            man_transactionstemp = """
                                  {0}
                               """.format(manpo)
            man_transactionshtml =man_transactionshtml +man_transactionstemp
        htmlb = """</div>"""
        sumhtml = htmla + man_transactionshtml + htmlb
        return htmltbl + header + accordionhtml + sumhtml 


    @expose()
    def get_edit_dialog_workflow(self,**kw):
        man_orderid = kw['man_po_item']
        man_stage_id = kw['man_stage_id']
        #print ('Man Orderid = {0}'.format(kw['man_po_item']))
        #print ('Man Stages = {0}'.format(kw['man_stage_id']))
        try:
            poqties = DBS_JistManufacturing.query(JistManufacturingWorkFlow). \
                filter(JistManufacturingWorkFlow.man_order_id==man_orderid). \
                filter(JistManufacturingWorkFlow.man_stage_id==man_stage_id). \
                value(func.sum(JistManufacturingWorkFlow.man_stage_qty))
            man_poitems = DBS_JistManufacturing.query(JistManufacturingWorkFlow). \
                filter(JistManufacturingWorkFlow.man_order_id==man_orderid). \
                filter(JistManufacturingWorkFlow.man_stage_id==man_stage_id). \
                all()
        except:
            poqties = 0

        manstages =DBS_JistManufacturing.query(JistManufacturingStages).all()
        html1 = """
        <div id="dialog_workflow_edit" title="Edit Workflow">
            <form id="dialog_workflow_frm_edit">
                <fieldset>
                    <label for="">JJMC Job No</label><br/>
                    <input value="{0}" id="man_jobid" name="man_jobid" class="text ui-widget-content ui-corner-all" /><br/>
                    <label for="">Total Qty To Move</label><br/>
                    <input value="{1}" id="man_stages_qty" name="man_stages_qty" class="text ui-widget-content ui-corner-all" /><br/>
                    <label for="">Move From</label><br/>

                """.format(man_orderid,poqties)

        html2 = """
                  <select id='manstage_from' name='manstage_from' class="text ui-widget-content ui-corner-all" >
                """
        for m in manstages: 
            if int(man_stage_id) == m.id:
                html2temp = """
                              <option selected = 'selected' typ='disabled' value="%s">%s</option>
                        """%(m.id,m.name)
                html2 = html2 + html2temp
            else:
                html2temp = """
                              <option value="%s">%s</option>
                        """%(m.id,m.name)
                html2 = html2 + html2temp

        html2 = html2 + "</select><br/>"

        html3 = """
                    <label for="">Move To Stage</label><br/>
                    <select id='manstage_to' name='manstage_to' class="text ui-widget-content ui-corner-all" >
                """
        for m in manstages: 
            html3temp = """
                          <option value="%s">%s</option>
                    """%(m.id,m.name)
            html3 = html3 + html3temp
        html3 = html3 + "</select><br/>"
        html4 = """
                </fieldset>
                </form>
       </div>
                """
        return html1 + html2 + html3 + html4

    @expose()
    def save_edit_dialog_workflow(self,**kw):
        man_orderid = kw['man_jobid']
        man_stage_to = kw['manstage_to']
        man_stage_from = kw['manstage_from']
        man_stages_qty = kw['man_stages_qty']
        poqties = DBS_JistManufacturing.query(JistManufacturingWorkFlow). \
            filter(JistManufacturingWorkFlow.man_order_id==man_orderid). \
            filter(JistManufacturingWorkFlow.man_stage_id==man_stage_from). \
            value(func.sum(JistManufacturingWorkFlow.man_stage_qty))
        man_poitems = DBS_JistManufacturing.query(JistManufacturingWorkFlow). \
            filter(JistManufacturingWorkFlow.man_order_id==man_orderid). \
            filter(JistManufacturingWorkFlow.man_stage_id==man_stage_from). \
            all()
        if float(man_stages_qty) > int(poqties):
            print man_stages_qty, poqties
            return
        if not isnumeric(man_stages_qty): return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)

        flow = JistManufacturingWorkFlow()
        flow.man_order_id = man_orderid
        flow.man_stage_id = man_stage_to 
        flow.man_stage_qty = float(man_stages_qty) 
        flow.useridnew = usernow.user_id 
        flow.useridedited = usernow.user_id 
        DBS_JistManufacturing.add(flow)

        flow2 = JistManufacturingWorkFlow()
        flow2.man_order_id = man_orderid
        flow2.man_stage_id = man_stage_from 
        flow2.man_stage_qty = float(man_stages_qty) * (-1) 
        flow2.useridnew = usernow.user_id 
        flow2.useridedited = usernow.user_id 
        DBS_JistManufacturing.add(flow2)

        DBS_JistManufacturing.flush()

    @expose()
    def get_dialog_standarditem_add(self,**kw):
        itemid = kw['item_id']
        html1 = """
                <div id="dialog_add_manufacturing_item" title="Add Manufacturing Item">
                    <form id="dialog_add_manufacturing_item_frm">
                        <fieldset>
                            <label for="">ID</label>
                            <input type="text" value={0} name="listid" id="listid" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Mat Name</label>
                            <input type="text" name="matname" id="matname" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Diameter (mm)</label>
                            <input type="text" name="matdia" id="matdia" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Thickness (mm)</label>
                            <input type="text" name="matthickness" id="matthickness" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Width (mm)</label>
                            <input type="text" name="matwidth" id="matwidth" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Height (mm)</label>
                            <input type="text" name="matheight" id="matheight" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Length (mm)</label>
                            <input type="text" name="matlen" id="matlen" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Kg/m</label>
                            <input type="text" name="matmass" id="matmass" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Supplier Lens (mm)</label>
                            <input type="text" name="matsuplens" id="matsuplens" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Qty Req</label>
                            <input type="text" name="matqtyreq" id="matqtyreq" class="text ui-widget-content ui-corner-all" /><br/>
                        </fieldset>
                    </form>
                </div>
                """.format(itemid)
        return html1

    @expose()
    def get_dialog_standarditem_edit(self,**kw):
        itemid = kw['item_id']
        item = DBS_JistManufacturing.query(JistManufactureStandardList). \
               filter(JistManufactureStandardList.id== itemid).one()
        #item.listid = listid 
        html1 = """
                <div id="dialog_edit_manufacturing_item" title="Edit Manufacturing List Item">
                    <form id="dialog_edit_manufacturing_item_frm">
                        <fieldset>
                            <label for="">ID</label>
                            <input type="text" value='{0}' name="listid" id="listid" class="text ui-widget-content ui-corner-all" /><br/>
                            <label for="">Description</label>
                            <input type="text" value='{1}' name="matname" id="matname" class="text ui-widget-content ui-corner-all" /><br/>
                        </fieldset>
                    </form>
                </div>
                """.format(itemid,item.description)
        return html1

    @expose()
    def add_new_manufacturing_item_to_list(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        listid = kw['listid']
        matname = kw['matname']
        matdia = kw['matdia']
        matthickness = kw['matthickness']
        matwidth = kw['matwidth']
        matheight = kw['matheight']
        matlen = kw['matlen']
        matmass = kw['matmass']
        matsuplens = kw['matsuplens']
        matqtyreq = kw['matqtyreq']
        item = JistManufactureStandardListItems()
        item.listid = listid 
        item.materialname = matname 
        item.diameter = matdia
        item.thickness = matthickness
        item.width = matwidth
        item.height = matheight 
        item.length = matlen 
        item.weight =  matmass
        item.supp_lens =  matsuplens
        item.qty_req = matqtyreq 
        item.useridnew = usernow.user_id
        item.useridedited = usernow.user_id
        DBS_JistManufacturing.add(item)
        DBS_JistManufacturing.flush()

    @expose()
    def save_edit_manufacturing_item_to_list(self,**kw):
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        listid = kw['listid']
        matname = kw['matname']
        item = DBS_JistManufacturing.query(JistManufactureStandardList). \
               filter(JistManufactureStandardList.id== listid).one()
        #item.listid = listid 
        item.description = matname 
        DBS_JistManufacturing.flush()

    @expose()
    def ajaxToggleManufacturingProduction(self,**kw):
        orderitemid = kw["orderitem_id"]
        poitems = DBS_JistBuying.query(JistBuyingOrderItems). \
                filter(JistBuyingOrderItems.id==orderitemid). \
                one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        try:
            itemlist = DBS_JistManufacturing.query(JistManufactureOrderItems). \
                    filter(JistManufactureOrderItems.jist_po_itemid == poitems.id). \
                    one()
            itemlist.active_production = not itemlist.active_production 
        except:
            itemlist = JistManufactureOrderItems()
            itemlist.jist_po = int(poitems.ponumber)
            itemlist.jist_po_itemid = int(poitems.id)
            itemlist.active_production = True 
            itemlist.description = poitems.description
            itemlist.unit = poitems.unit
            itemlist.qty = poitems.quantity
            itemlist.price = poitems.priceexcl
            itemlist.total = poitems.totalexcl
            itemlist.useridnew = usernow.user_id 
            itemlist.useridedited = usernow.user_id 
            DBS_JistManufacturing.add(itemlist)
            DBS_JistManufacturing.flush()

            #Start the Production Flow
            flow = JistManufacturingWorkFlow()
            flow.man_order_id = itemlist.id
            flow.man_stage_id = 1
            flow.man_stage_qty = poitems.quantity
            flow.useridnew = usernow.user_id 
            flow.useridedited = usernow.user_id 
            DBS_JistManufacturing.add(flow)
            DBS_JistManufacturing.flush()

        #newnote = JistBuyingPurchaseReqsNotes()
        #newnote.reqitemid = reqitemid 
        #newnote.note = self.safe(html)
        #newnote.useridnew = usernow.user_id
        #newnote.dateadded = datetime.now()
        #DBS_JistBuying.add(newnote)
        #DBS_JistBuying.flush()
        return

    def build_manufacturing_html_table(self,dictlist,headers,headerwidths,outputlist,tdclassnames,tblname):
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

    def produce_state_inmanufacturing(self,state):
        if state:
            html = """<img id="addtoproduction"
            src="/images/True.png" >
            </img>"""
        else:
            html = """<img id="addtoproduction"
            src="/images/False.png" >
            </img>"""

        return html



def isnumeric(value):
    return str(value).replace(".", "").replace("-", "").isdigit()

def checknullvalue(value):
    if value:
        return str(value)
    else:
        return 'undefined'

