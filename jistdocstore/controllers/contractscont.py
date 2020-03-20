# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group
from tg.decorators import paginate
import math
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
#from tw.extjs import ItemSelector
from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
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
from pkg_resources import resource_filename
import subprocess
import os
import random
from tg import session
#from tw.jquery import TreeView
from decimal import Decimal
from babel.numbers import format_currency, format_number, format_decimal

public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')
current_filestore_contract_id = 0 

__all__ = ['ContractsController']


class ContractsController(BaseController):
    """Sample controller-wide authorization"""
    
    # The predicate that must be met for all the actions in this controller:
    #allow_only = has_permission('manage','contractsgroup',
    #                            msg=l_(''))
    def __init__(self):
        self.last_saved_site_rnd = 0
        self.last_saved_scope_rnd = 0
        self.last_saved_bqitem_rnd = 0
        self.last_saved_quoteno = 0
        self.last_saved_scopelist = "" 
        self.last_saved_editscope = "" 
        self.last_saved_scopecontract = 0
        self.last_saved_budgetcontract =0 
        self.last_saved_contract_status_rnd = 0
        self.building_3yr_tender_number = "445Q"
        self.last_save_scopeiddeleted = 0
        self.last_saved_item_description = 0 
        self.last_save_scopecontractnew = 0
        self.last_saved_scopebudget = 0 
        self.ListCIDBCategories = ['None','GB', 'SQ', 'CE', 'ME']
        self.ListTrueFalse = ['False','True']
        self.ListWorkCategory = ['None','Fencing Standard','Fencing Palisade','Fencing High Security',
                                'Building Work','Building Maintenance','Carports',
                                'Manufacturing','CCTV','Supply Only','Alarm System','Entrance Control',
                                'Administrative','Software','Network Support' 
                                ]

    @require(in_any_group("managers", "contracts_group"))
    @expose()
    def index(self):
        redirect('contractscont/menu')

    @expose('jistdocstore.templates.contracts.logopage')
    def logopage(self):
        #flash(_("Secure Controller here"))
        return dict(page='Logo Page') 

    @expose('jistdocstore.templates.contracts.contractsindex')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='Contracts: Main Menu') 

    @require(in_any_group("managers", "contracts_group"))
    @expose('jistdocstore.templates.contracts.contractspage')
    def showcontracts(self,**named):
        #sitetree = TreeView(treeDiv='navTree')
        #tmpl_context.tree = sitetree 
        #tmpl_context.tree = sitetree 
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        contractscompleted = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="True"). \
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
        return dict(page='JIST Contracts',
                    wip = contracts,
                    contracts_completed = contractscompleted,
                    currentPage=1,
                    value=named,
                    newcontractfields = newcontractfields,
                    editcontractfields = editcontractfields,
                    addorderitem=addorderitem,
                    editorderitem=editorderitem,
                    cidbcategories = self.ListCIDBCategories,
                    cidbratings = range(11),
                    trueorfalse = self.ListTrueFalse,
                    workcategories = self.ListWorkCategory,
                    value2=named)
        
    @require(in_any_group("managers", "contracts_group"))
    @expose('jistdocstore.templates.contracts.contractsconsole')
    def contractsconsole(self,**named):
        #sitetree = TreeView(treeDiv='navTree')
        #tmpl_context.tree = sitetree 
        #tmpl_context.tree = sitetree 
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        contractscompleted = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="True"). \
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
        return dict(page='JIST Contracts',
                    wip = contracts,
                    contracts_completed = contractscompleted,
                    currentPage=1,
                    value=named,
                    newcontractfields = newcontractfields,
                    editcontractfields = editcontractfields,
                    addorderitem=addorderitem,
                    editorderitem=editorderitem,
                    cidbcategories = self.ListCIDBCategories,
                    cidbratings = range(11),
                    trueorfalse = self.ListTrueFalse,
                    workcategories = self.ListWorkCategory,
                    value2=named)

    @expose()
    def get_search_contracts(self,**kw):
        thisphrase = "%(searchphrase)s" % kw
        if len(thisphrase) < 4:
            return "<H1 class='warning'> Type something with more than 3 letters please.</H1>"
        html = ''
        html1 = """<table id='estimate_sites_table' class='table_estdata'>
                   <th> JNo</th>
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
            sites = DBS_ContractData.query(JistContracts). \
                   order_by(desc(JistContracts.id)).all()
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
        elif kw['switch']=="JCNo":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pic_contract_open' src='/images/project-open.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Edit","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','edit','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        elif kw['switch']=="SearchName":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.site.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pic_contract_open' src='/images/project-open.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Edit","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','edit','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 

            return html
        elif kw['switch']=="SearchClient":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.client.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pic_contract_open' src='/images/project-open.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Edit","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','edit','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        elif kw['switch']=="SearchDescription":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.description.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pic_contract_open' src='/images/project-open.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Edit","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','edit','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        elif kw['switch']=="SearchOrderNo":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.orderno.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pic_contract_open' src='/images/project-open.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Edit","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','edit','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        else:
            return "<H1 class='warning'> Zero Results</H1>"

    @expose()
    def get_search_pics(self,**kw):
        thisphrase = "%(searchphrase)s" % kw
        if len(thisphrase) < 4:
            return "<H1 class='warning'> Type something with more than 3 letters please.</H1>"
        if kw['switch']=="All":
            sites = DBS_ContractData.query(JistContracts). \
                   order_by(desc(JistContracts.id)).all()
        elif kw['switch']=="JCNo":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.jno.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                thisuploadsum = DBS_JistFileStore.query(FileStoreProduction). \
                        filter(FileStoreProduction.jcno==k.jno). \
                        value(func.count(FileStoreProduction.jcno))
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'open':"<img jcno='%s' class='pics_by_jcno' src='/images/project-open.png'></img>"%k.jno,
                             'picsum':thisuploadsum,
                             'edit':"<img jcno='%s' class='pics_by_jcno' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Pic Sum","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','picsum','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        elif kw['switch']=="SearchName":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.site.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                thisuploadsum = DBS_JistFileStore.query(FileStoreProduction). \
                        filter(FileStoreProduction.jcno==k.jno). \
                        value(func.count(FileStoreProduction.jcno))
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'open':"<img jcno='%s' class='pics_by_jcno' src='/images/project-open.png'></img>"%k.jno,
                             'picsum':thisuploadsum,
                             'edit':"<img jcno='%s' class='pics_by_jcno' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Pic Sum","Open"]
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','picsum','open']
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 

            return html
        elif kw['switch']=="SearchClient":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.client.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                thisuploadsum = DBS_JistFileStore.query(FileStoreProduction). \
                        filter(FileStoreProduction.jcno==k.jno). \
                        value(func.count(FileStoreProduction.jcno))
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'open':"<img jcno='%s' class='pics_by_jcno' src='/images/project-open.png'></img>"%k.jno,
                             'picsum':thisuploadsum,
                             'edit':"<img jcno='%s' class='pics_by_jcno' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Pic Sum","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','picsum','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        elif kw['switch']=="SearchDescription":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.description.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                thisuploadsum = DBS_JistFileStore.query(FileStoreProduction). \
                        filter(FileStoreProduction.jcno==k.jno). \
                        value(func.count(FileStoreProduction.jcno))
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pics_by_jcno' src='/images/project-open.png'></img>"%k.jno,
                             'picsum':thisuploadsum,
                             'edit':"<img jcno='%s' class='pics_by_jcno' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Pic Sum","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','picsum','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        elif kw['switch']=="SearchOrderNo":
            sitename = "%(searchphrase)s" % kw
            searchphrase = "%"+sitename+"%"
            sites = DBS_ContractData.query(JistContracts). \
                    filter(JistContracts.orderno.like(searchphrase)). \
                   order_by(desc(JistContracts.jno)).all()
            outputlist = []
            for k in sites:
                thisuploadsum = DBS_JistFileStore.query(FileStoreProduction). \
                        filter(FileStoreProduction.jcno==k.jno). \
                        value(func.count(FileStoreProduction.jcno))
                outputlist.append({
                             'jno':k.jno,
                             'orderdate':k.orderdate,
                             'orderno':k.orderno,
                             'client':k.client,
                             'site':k.site,
                             'description':k.description,
                             'useridnew':"<img src='/images/staffpics/%s.png'></img>"%k.useridnew,
                             'dateadded': k.dateadded,
                             'dateedited': k.dateedited,
                             'spacer':"<img src='/images/lillac_background.png'></img>",
                             'completed':"<img src='/images/%s.png'></img>"%k.completed,
                             'edit':"<img jcno='%s' class='pic_contract_new_edit' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             'open':"<img jcno='%s' class='pics_by_jcno' src='/images/project-open.png'></img>"%k.jno,
                             'picsum':thisuploadsum,
                             'edit':"<img jcno='%s' class='pics_by_jcno' src='/images/edit-text-frame-update.png'></img>"%k.jno,
                             })
            headers =["JNo","Order Date","Order No","Client","Site","Description","Completed",'',"Pic Sum","Open"]
            dictlist = ['jno','orderdate','orderno','client','site','description','completed','spacer','picsum','open']
            headerwidths=[50,80,90,180,180,'',80,80,30,30,30]
            tdclassnames=['','','','','','','','tdspacer','','','','']
            htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contracts_loading")
            html = htmltbl 
            return html
        else:
            return "<H1 class='warning'> Zero Results</H1>"


    @expose()
    def ajaxnewcontract(self,**kw):
        #for k, w in kw.iteritems():
            #print k, w
        #return
        client = kw['contract_clientname']
        sitename = kw['contract_sitename']
        description = kw['contract_description']
        orderno = kw['contract_orderno']
        orderdate = kw['contract_orderdate']
        contact = kw['contract_contact']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_site = JistContracts(orderno = orderno,
                                       description=description,
                                       orderdate = orderdate,
                                       client = client,
                                       site = sitename,
                                       contact = contact,
                                       pointperson = 1,
                                       completed = "False",
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       )
        DBS_ContractData.add(new_site)
        DBS_ContractData.flush()
        newcontractual = JistContractContractual(jno=new_site.jno,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       )
        DBS_ContractData.add(newcontractual)
        DBS_ContractData.flush()
        newcontractstatus = JistContractStatus(jno=new_site.jno,
                                       pointperson="1",
                                       siteagent="1",
                                       statuscode="1",
                                       sitehandoverdate=None,
                                       actualstartdate=None,
                                       firstdeldate=None,
                                       finalcompldate=None,
                                       dateadded = datetime.now(),
                                       dateedited = datetime.now(),
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       )
        DBS_ContractData.add(newcontractstatus)
        DBS_ContractData.flush()
        #self.last_saved_site_rnd = sitename 

    @expose()
    def get_edit_contract_dialog(self,**kw):
        #if self.last_saved_item_description == description:
        #    return
        jno_id = kw['jno']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        thisites = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==int(jno_id)).one()
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jno_id).one()
        lasteditedperson = DBS_ContractData.query(User).filter(User.user_id==statusall.useridedited).one()
        point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
        statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
        try:
            conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
            planstartdate = conplandates.planstartdate
            planenddate = conplandates.planenddate
        except:
            conplandates = None
            planstartdate = None 
            planenddate = None 

        timeframe = {'orderdate':thisites.orderdate,
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

        siteagent = DBS_ContractData.query(User).filter(User.user_id==status['siteagent']).one()
        dictsites = {'jno':thisites.jno,
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
                     'pointperson':point.user_name,
                     'siteagent':siteagent.user_name,
                     }

        html1 = """
            <form id="dialog_contract_edit_frm">
                <fieldset>

                      <label for=''>JCNo</label>
                      <input type="text" value="%s" name="contract_jcno_edit" id="contract_jcno_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Client Name</label>
                      <input type="text" value="%s" name="contract_clientname_edit" id="contract_clientname_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Site Name</label>
                      <input type="text" value="%s" name="contract_sitename_edit" id="contract_sitename_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Order Number</label>
                      <input type="text" value="%s" name="contract_orderno_edit" id="contract_orderno_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Order Date</label>
                      <input type="text" value="%s" name="contract_orderdate_edit" id="contract_orderdate_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Contract Description</label>
                      <input type="text" value="%s" name="contract_description_edit" id="contract_description_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Contact</label>
                      <input type="text" value="%s" name="contract_contact_edit" id="contract_contact_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Telephone No</label>
                      <input type="text" value="%s" name="contract_telephone_edit" id="contract_telephone_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Fax No</label>
                      <input type="text" value="%s" name="contract_fax_edit" id="contract_fax_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Cell No</label>
                      <input type="text" value="%s" name="contract_cell_edit" id="contract_cell_edit" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Work Category</label>
                """%(dictsites['jno'],dictsites['client'],dictsites['site'],dictsites['orderno'],dictsites['orderdate'],dictsites['description'],
                        dictsites['contact'],dictsites['tel'],dictsites['fax'],dictsites['cell'])

        html2 = "<select id='contract_edit_workcategory' name='contract_edit_workcategory'>"
        for m in self.ListWorkCategory: 
            if thisites.workcategory == m:
                html2temp = """
                              <option selected = 'selected' value="%s">%s </option>
                        """%(m,m)
                html2 = html2 + html2temp
            else:
                html2temp = """
                              <option value="%s">%s</option>
                        """%(m,m)
                html2 = html2 + html2temp

        html3 = "</select></br><label for=''>CIDB Category</label><select id='contract_edit_cidbcategory' name='contract_edit_cidbcategory'>"
        for m in self.ListCIDBCategories: 
            if thisites.cidbcategory == m:
                html3temp = """
                              <option selected = 'selected' value="%s">%s </option>
                        """%(m,m)
                html3 = html3 + html3temp
            else:
                html3temp = """
                              <option value="%s">%s</option>
                        """%(m,m)
                html3 = html3 + html3temp

        html4 = "</select></br><label for=''>Completed</label><select id='contract_edit_completed' name='contract_edit_completed'>"
        for m in self.ListTrueFalse: 
            if thisites.completed == m:
                html4temp = """
                              <option selected = 'selected' value="%s">%s </option>
                        """%(m,m)
                html4 = html4 + html4temp
            else:
                html4temp = """
                              <option value="%s">%s</option>
                        """%(m,m)
                html4 = html4 + html4temp



        htmlend = "</select></fieldset></form>"
        return html1 + html2 + html3 + html4 + htmlend 

    @expose()
    def get_contract_orderitems(self,jno_id,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        totalex = DBS_ContractData.query(JistContractOrderItems). \
                filter(JistContractOrderItems.jno==jno_id). \
                value(func.sum(JistContractOrderItems.total))
        for thisites in contractsitems:
            dictsites.append({
                        'jcno':thisites.jno,
                          'id':thisites.id,
                         'item':thisites.item,
                         'description':thisites.description,
                         'unit':thisites.unit,
                         'qty':thisites.qty,
                         'price':thisites.price,
                         'total':thisites.total,
                         })
        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        outputlist = []
        for k in contractsitems:
            outputlist.append({
                        'jcno':k.jno,
                        'id':k.id,
                         'item':k.item,
                         'description':k.description,
                         'unit':k.unit,
                         'qty':k.qty,
                         'price':k.price,
                         'total':k.total,
                         'spacer':"<img src='/images/lillac_background.png'></img>",
                         'edit':"<img jcno='%s' id='%s' class='pic_orderitem_edit' src='/images/edit-text-frame-update.png'></img>"%(k.jno,k.id),
                         'open':"<img class='pic_contract_open'src='/images/project-open.png'></img>",
                         })
        headers =["ID","Item","Description","Unit","Qty","Price","Total",'',"Edit"]
        dictlist = ['id','item','description','unit','qty','price','total','spacer','edit']
        headerwidths=[50,50,'',90,80,80,100,'30',30,30,30,30,30]
        tdclassnames=['','','','','','','','tdspacer','','','','']
        htmltbl = self.build_contracts_html_table(dictlist,headers,headerwidths,outputlist,tdclassnames,tblname="tbl_active_contract_orderitems_loading")
        html = htmltbl 
        addbutton = "<h3 class='effect6'><span='spanleft'>JCNo:%s</span><button value='%s' id='btn_add_new_orderitem'>Add New Order Item</button><span class='spanright'> Total Excl: %s</span></h3>"%(jno_id,jno_id,totalex)
               
        return addbutton + html

    @expose()
    def get_edit_orderitems_dialog(self,**kw):
        #if self.last_saved_item_description == description:
        #    return
        orderitemid = kw['orderitemid']
        contractsitem = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.id==orderitemid). \
               one()
        html1 = """
            <form id="dialog_orderitems_edit_frm">
                <fieldset>

                      <label for=''>ID</label>
                      <input type="text" value="%s" name="orderitem_id" id="orderitem_id" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Item</label>
                      <input type="text" value="%s" name="orderitem_item" id="orderitem_item" class="text ui-widget-content ui-corner-all" />
                      <br/>
                      <label for=''>Desciption</label>
                      <input type="text" value="%s" name="orderitem_description" id="orderitem_description" class="text ui-wdescriptionget-content ui-corner-all" />
                      <br/>
                      <label for=''>Unit</label>
                      <input type="text" value="%s" name="orderitem_unit" id="orderitem_unit" class="text ui-wunitget-content ui-corner-all" />
                      <br/>
                      <label for=''>Qty</label>
                      <input type="text" value="%s" name="orderitem_qty" id="orderitem_qty" class="text ui-wqtyget-content ui-corner-all" />
                      <br/>
                      <label for=''>Price</label>
                      <input type="text" value="%s" name="orderitem_price" id="orderitem_price" class="text ui-wpriceget-content ui-corner-all" />
                      <br/>
                      <label for=''>Total</label>
                      <input type="text" value="%s" name="orderitem_total" id="orderitem_total" class="text ui-wtotalget-content ui-corner-all" />
                      <br/>
                """%(contractsitem.id,contractsitem.item,contractsitem.description,contractsitem.unit,contractsitem.qty,contractsitem.price,contractsitem.total)

        htmlend = "</fieldset></form>"
        return html1  +  htmlend 

    @expose()
    def ajax_save_new_orderitem(self,**kw):
        siteid = kw['orderitem_new_jcno']
        item = kw['orderitem_new_item']
        description = kw['orderitem_new_description']
        unit = kw['orderitem_new_unit']
        qty = kw['orderitem_new_qty']
        price = kw['orderitem_new_price']
        total = kw['orderitem_new_total']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_item = JistContractOrderItems(jno = siteid,
                                       item=item,
                                       description=description,
                                       unit = unit,
                                       qty = qty,
                                       price = price,
                                       total = total,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.now(),
                                       dateedited = datetime.now(),
                                       )
        DBS_ContractData.add(new_item)
        DBS_ContractData.flush()
        return str(siteid)

    @expose()
    def ajax_save_edit_orderitem(self,**kw):
        itemid = kw['orderitem_id']
        item = kw['orderitem_item']
        description = kw['orderitem_description']
        unit = kw['orderitem_unit']
        qty = kw['orderitem_qty']
        price = kw['orderitem_price']
        total = kw['orderitem_total']

        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id

        orderitem = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.id==itemid).one()
        orderitem.item=item
        orderitem.description=description
        orderitem.unit = unit
        orderitem.qty = qty
        orderitem.price = price
        orderitem.total = Decimal(total)
        orderitem.useridedited=useridcreated
        orderitem.dateedited = datetime.now()
        DBS_ContractData.flush()
        return str(orderitem.jno)

    @expose()
    def ajaxeditcontract(self,**kw):
        siteid = kw['contract_jcno_edit']
        client = kw['contract_clientname_edit']
        sitename = kw['contract_sitename_edit']
        orderno = kw['contract_orderno_edit']
        description = kw['contract_description_edit']
        orderdate = kw['contract_orderdate_edit']
        contact = kw['contract_contact_edit']
        completed = kw['contract_edit_completed']
        cell = kw['contract_cell_edit']
        tel = kw['contract_telephone_edit']
        fax = kw['contract_fax_edit']
        cidbcat = kw['contract_edit_cidbcategory']
        workcat = kw['contract_edit_workcategory']
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        editcontract = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==int(siteid)).one()
        editcontract.orderno = orderno
        editcontract.description=description
        editcontract.orderdate = orderdate
        editcontract.client = client
        editcontract.site = sitename
        editcontract.contact = contact
        editcontract.completed = completed
        editcontract.cidbcategory =cidbcat 
        editcontract.workcategory = workcat 
        editcontract.useridedited=useridcreated
        DBS_ContractData.flush()

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

    @expose()
    def ajaxsiteswip(self,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()

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
                         })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """
               <h2 class="effect6">
               <span class='spanleft'>Contracts In Progress </span>
                <span class='spanright'>
               </span>
               </h2>
                            <div id='contracts_wip_div'>
                            <table id='contracts_wip_table' class='table_estdata'>
                            <th>JCNo</th>
                            <th>Order Date</th>
                            <th>Client</th>
                            <th>Site Name</th>
                            <th>Description</th>
                            <th>Point</th>
                """
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
                    </tr>
                    """%(scp["jno"],scp["orderdate"],scp["client"],scp["site"],scp["description"],scp["pointperson"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>
                            </div>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxsitescompleted(self,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="True"). \
               order_by(desc(JistContracts.jno)).all()
        for thisites in contracts:

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
                         'pointperson':thisites.pointperson,
                         })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """
                            Contracts Completed:
                            <table class='table_estdata'>
                            <th>JCNo</th>
                            <th>Order Date</th>
                            <th>Client</th>
                            <th>Site Name</th>
                """
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
                            <img src="/images/project-open.png"
                            onclick="loadXMLContractData(%s)">
                            </img>
                        </td>
                    </tr>
                    """%(scp["jno"],scp["orderdate"],scp["client"],scp["site"],scp["jno"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxsitescontractdata(self,jno_id,**kw):
        dictsites = []
        thisites = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
                               one()
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jno_id).one()
        lasteditedperson = DBS_ContractData.query(User).filter(User.user_id==statusall.useridedited).one()
        point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
        statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
        try:
            conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
            planstartdate = conplandates.planstartdate
            planenddate = conplandates.planenddate
        except:
            conplandates = None
            planstartdate = None 
            planenddate = None 

        timeframe = {'orderdate':thisites.orderdate,
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

        siteagent = DBS_ContractData.query(User).filter(User.user_id==status['siteagent']).one()
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
                     'pointperson':point.user_name,
                     'siteagent':siteagent.user_name,
                     })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """

               <h2 class="effect6">
               <span class='spanleft'>JCNo: %s </span>
                <span class='spanright'>
                            Client: %s
                            <img src="/images/pencil.png"
                            onclick="opencontractedit('%s','%s','%s','%s','%s','%s','%s','%s')" align="right">
                            </img>

               </span>
               </h2>
                            </p>
                            <table class='table_estdata'>
                            <th>Order No</th>
                            <th>Site</th>
                            <th>Description</th>
                            <th>Point</th>
                """%(jno_id,thisites.client,
                        jno_id,thisites.site,thisites.client,thisites.orderno,thisites.orderdate,thisites.contact,thisites.description,thisites.completed
                        )
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
                    </tr>
                    """%(scp["orderno"],scp["site"],scp["description"],scp["pointperson"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>
                            <p/>

                """
        html =  html1 + html2 + html3

        html4 = """
                            <div style="height:40px;"> &nbsp; </div>
                            
               <h2 class="effect6">
               <span class='spanleft'>Contractual Data for JCNo: %s </span>
                <span class='spanright'>
               </span>
               </h2>

                            <table class='table_estdata'>
                            <th>Site Agent</th>
                            <th>Work Category</th>
                            <th>CIDB Category</th>
                            <th>Completed</th>
                """%jno_id
        temphtml4 = ""

        html5 = ""
        for scp in dictsites:
            #print scp["name"]
            temphtml4 = """
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
                    </tr>
                    """%(scp["siteagent"],scp["workcategory"],scp["cidbcategory"],scp["completed"])
            html5 = html5 + temphtml4

        html6 = """
                            </table>
                            <p/>

                """
        htmlcontractual = html4 + html5 + html6
        html7 = """
                            <div style="height:40px;"> &nbsp; </div>
                            
                            <p id="contractheader">
                            Production Dates for JCNo: %s 
                            </p>
                            <table class='table_estdata'>
                            <th>Site Handover</th>
                            <th>Start Date</th>
                            <th>First Del</th>
                            <th>Final Completion</th>
                """%jno_id
        temphtml5 = ""

        html8 = ""
        #for scp in timeframe:
        #    #print scp["name"]
        scp = timeframe
        html8 = """
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
                </tr>
                """%(scp["sitehandover"],scp["startdate"],scp["firstdel"],scp["finalcompl"])

        html9 = """
                            </table>

                """
        htmlproduction = html7 + html8 + html9

        return html + htmlcontractual + htmlproduction

    @expose()
    def ajaxsitescontractstatusupdate(self,jno_id,**kw):
        dictsites = []
        thisites = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
                               one()
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jno_id).one()
        lasteditedperson = DBS_ContractData.query(User).filter(User.user_id==statusall.useridedited).one()
        point = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
        #planningdates = DBS_ContractData.query(JistContractPlanningDates). \
        #            filter(JistContractPlanningDates.jcno==jno_id).one()
        #for p in point:
        #    print p
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        #useridcreated = usernow.user_id
        #usernamecreated = usernow.user_name
        #print usernamecreated
        statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
        try:
            conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jno_id).one()
            planstartdate = conplandates.planstartdate
            planenddate = conplandates.planenddate
        except:
            conplandates = 'None'
            planstartdate = 'None' 
            planenddate = 'None' 

        timeframe = {'orderdate':thisites.orderdate,
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

        siteagent = DBS_ContractData.query(User).filter(User.user_id==status['siteagent']).one()
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
                     'pointperson':point.user_name,
                     'siteagent':siteagent.user_name,
                     'statuscode':status['statuscode'],
                     'planstart':planstartdate,
                     'planend':planenddate,
                     })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        activeusers = DBS_ContractData.query(User).filter(User.active_status==1).all()
        statcodeall  = DBS_ContractData.query(JistContractStatusCodes).all()
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
        formupdate1= """
                        <form id="contract_status_form">
                        <fieldset>
                      <label for="%s">%s</label>
                      <input  id="%s" style="display:none"/>
                    <select id="dropdown_points_status_update" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("status_point_person_list","Point Person","status_point_person_list")
        for point in pointlist:
            formupdate1temp = """
                            <option value="%s">%s</option>

                              """%(point['user_id'],point['user_name'])
        
            formupdate1 = formupdate1 + formupdate1temp 
        formupdate2 = """
                      </select>
                      <label for="%s">%s</label>
                      <input  id="%s" style="display:none"/>
                      <select id="dropdown_siteagent_status_update" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("status_site_agent_list","Site Agent Person","status_site_agent_list")
        for siteagent in productionlist:
            formupdate2temp = """

                            <option value="%s">%s</option>

                              """%(siteagent['user_id'],siteagent['user_name'])
        
            formupdate2 = formupdate2 + formupdate2temp 
        formupdate3 = """
                      </select>
                      <label for="%s">%s</label>
                      <input  id="%s" style="display:none"/>
                      <select id="dropdown_status_update" style="display: block" class="text ui-widget-content ui-corner-all">
                            """% ("status_update_list","Status Update","status_update_list")
        for sts in statcodeall:
            formupdate3temp = """

                            <option value="%s">%s</option>

                              """%(sts.id,sts.status)
        
            formupdate3 = formupdate3 + formupdate3temp 

        formupdate4 = """
                                </select>
                                          <label for="%s">%s</label>
                                          <input type="text" name="%s" id="%s" class="text ui-widget-content ui-corner-all" />
                                          <br/>
                                          <label for="%s">%s</label>
                                          <input type="text" name="%s" id="%s" class="text ui-widget-content ui-corner-all" />
                                          <br/>
                                          <label for="%s">%s</label>
                                          <input type="text" name="%s" id="%s" class="text ui-widget-content ui-corner-all" />
                                          <br/>
                                          <label for="%s">%s</label>
                                          <input type="text" name="%s" id="%s" class="text ui-widget-content ui-corner-all" />
                                          <br/>
                                          <label for="%s">%s</label>
                                          <input type="text" name="%s" id="%s" class="text ui-widget-content ui-corner-all" />
                                          <br/>
                                          <label for="%s">%s</label>
                                          <input type="text" name="%s" id="%s" class="text ui-widget-content ui-corner-all" />
                                          <br/>
                                          <label for="">Saved Location</label>
                                          <select id="locationlistid" name="locationlistid" style="display: block" class="text ui-widget-content ui-corner-all">
                                          <option value="None">Select Your Saved Location</option>
                               """%("Planned Start Date",
                                       "Planned Start Date",
                                       "cont_planned_start_date",
                                       "cont_planned_start_date",
                                       "Planned End Date",
                                       "Planned End Date",
                                       "cont_planned_end_date",
                                       "cont_planned_end_date",
                                       "Site Handover Date",
                                       "Site Handover Date",
                                       "cont_site_handover_date",
                                       "cont_site_handover_date",
                                       "Actual Start Date",
                                       "Actual Start Date",
                                       "cont_actual_start_date",
                                       "cont_actual_start_date",
                                       "First Delivery Date",
                                       "First Delivery Date",
                                       "cont_first_del_date",
                                       "cont_first_del_date",
                                       "Final Completion Date",
                                       "Final Completion Date",
                                       "cont_final_completion_date",
                                       "cont_final_completion_date",
                                       )
        locationlist = DBS_ContractData.query(JistLocationList). \
                filter(JistLocationList.active==True). \
                filter(JistLocationList.useridnew==usernow.user_id). \
                order_by(desc(JistLocationList.id)). \
                all()
        formupdate5 = ''
        thissitelocationid = thisites.locationid
        for loc in locationlist:
            if loc.id == thissitelocationid:
                html5temp = """
                            
                                <option selected="selected" value="%s">%s</option>

                                  """%(loc.id,loc.description)
            else:
                html5temp = """
                            
                                <option value="%s">%s</option>

                                  """%(loc.id,loc.description)
        
            formupdate5 = formupdate5 + html5temp 

        formupdate6 = """
                                </select>
                                <button class="ui-state-default ui-corner-all" id="button_status_update_pressed">Change Status</button>
                                </fieldset>
                                </form>
                            
                      """
        htmlformstatusupdate = formupdate1 + formupdate2 + formupdate3 + formupdate4 + formupdate5 + formupdate6
        html1 = """
               <h2 class='effect6'>
               <span class='spanleft'>JCNo: %s </span>
                <span class='spanright'>
                            Client: %s
               </span>
               </h2>
                            <table id="contractdata_table" class='table_estdata'>
                            <th>Order No</th>
                            <th>Site</th>
                            <th>Description</th>
                            <th>Point</th>
                            <th>Status</th>
                """%(jno_id,thisites.client,
                        )
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
                    <td >
                    %s
                    </td>
                    </tr>
                    """%(scp["orderno"],scp["site"],scp["description"],scp["pointperson"],status['statuscode'])
            html2 = html2 + temphtml1
        html3 = """
                            </table>
                            <p/>

                """
        html =  html1 + html2 + html3

        html4 = """
                            <div style="height:40px;"> &nbsp; </div>
               <h2 class="effect6">
               <span class='spanleft'>Contractual Data for JCNo: %s </span>
                <span class='spanright'>
               </span>
               </h2>
                            <table id="contractdata_contractual_table" class='table_estdata'>
                            <th>Site Agent</th>
                            <th>Work Category</th>
                            <th>CIDB Category</th>
                            <th>Completed</th>
                """%jno_id
        temphtml4 = ""

        html5 = ""
        for scp in dictsites:
            #print scp["name"]
            temphtml4 = """
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
                    </tr>
                    """%(scp["siteagent"],scp["workcategory"],scp["cidbcategory"],scp["completed"])
            html5 = html5 + temphtml4

        html6 = """
                            </table>
                            <p/>

                """
        htmlcontractual = html4 + html5 + html6
        html7 = """
                            <div style="height:40px;"> &nbsp; </div>
                            
               <h2 class="effect6">
               <span class='spanleft'>Production Dates for JCNo: %s </span>
                <span class='spanright'>
               </span>
               </h2>
                            <table  id="contractdata_dates_table" class='table_estdata'>
                            <th>Plan Start</th>
                            <th>Plan End</th>
                            <th>Site Handover</th>
                            <th>Start Date</th>
                            <th>First Del</th>
                            <th>Final Completion</th>
                """%jno_id
        temphtml5 = ""

        html8 = ""
        #for scp in timeframe:
        #    #print scp["name"]
        scp = timeframe
        html8 = """
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
                </tr>
                """%(planstartdate,planenddate,scp["sitehandover"],scp["startdate"],scp["firstdel"],scp["finalcompl"])

        html9 = """
                            </table>
                            <div id="point_siteagent_status"
                            style="display:none">
                            <input type="text" value="%s" id="activesitejcno"  disabled="true"/>
                            <input type="text" value="%s" id="activesitepoint"  disabled="true"/>
                            <input type="text" value="%s" id="activesitesiteagent"  disabled="true"/>
                            <input type="text" value="%s" id="activesitestatus"  disabled="true"/>
                            <input type="text" value="%s" id="activesiteplanstart"  disabled="true"/>
                            <input type="text" value="%s" id="activesiteplanend"  disabled="true"/>
                            <input type="text" value="%s" id="activesitesitehandover"  disabled="true"/>
                            <input type="text" value="%s" id="activesiteactualstart"  disabled="true"/>
                            <input type="text" value="%s" id="activesitefirstdel"  disabled="true"/>
                            <input type="text" value="%s" id="activesitefinalcompletion"  disabled="true"/>
                            </div>

                """%(jno_id,status['pointperson'],status['siteagent'],statcode.id,planstartdate,planenddate,scp["sitehandover"],scp["startdate"],scp["firstdel"],scp["finalcompl"])
        htmlproduction = html7 + html8 + html9

        return  "<div id='contract_contractual'>"+html + htmlcontractual + htmlproduction+"</div><div id='contract_contractual_form'>" + htmlformstatusupdate +"</div>"

    @expose()
    def ajaxsitescontractorderitems(self,jno_id,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        totalex = DBS_ContractData.query(JistContractOrderItems). \
                filter(JistContractOrderItems.jno==jno_id). \
                value(func.sum(JistContractOrderItems.total))
        for thisites in contractsitems:
            dictsites.append({'jno':thisites.jno,
                          'id':thisites.id,
                         'item':thisites.item,
                         'description':thisites.description,
                         'unit':thisites.unit,
                         'qty':thisites.qty,
                         'price':thisites.price,
                         'total':thisites.total,
                         })
        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """

               <h2 class="effect6">
               <span class='spanleft'>Contract Order Items for JCNo: %s </span>
                <span class='spanright'>
                            Total = %s
               </span>
               </h2></br>
                            <div id="button_space_orderitems"></div>
                            <table class='table_estdata'>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th align="right">Qty</th>
                            <th align="right">Price</th>
                            <th align="right">Total</th>
                """%(jno_id,totalex)
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
                    <td  align="right">
                    %s
                    </td>
                    <td  align="right">
                    %s
                    </td>
                        <td align="right">
                            %s
                        </td>
                        <td>
                        </td>
                    </tr>
                    """%(scp["item"],scp["description"],scp["unit"],scp["qty"],scp["price"],scp["total"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>

                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxsitescontractscopeofwork(self,jno_id,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        for scp in scope:
            dictsites.append({'jno':scp.jno,
                          'id':scp.id,
                         'item':scp.item,
                         'description':scp.description,
                         'unit':scp.unit,
                         'qty':scp.qty,
                         'price':scp.price,
                         'total':scp.total,
                         })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """

               <h2 class="effect6">
               <span class='spanleft'>Contract Scope for JCNo: %s </span>
                <span class='spanright'>
                            <img id="addcontractscope" src="/images/add.png" align="right"></img>
               </span>
               </h2>
                            <div id="button_space_sow"></div>
                            <table id='table_contracts_sow' class='table_estdata'>
                            <th>ID</th>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th align="right">Qty</th>
                            <th align="right">Price</th>
                            <th align="right">Total</th>
                            <th align="right">Edit</th>
                            <th align="right">Delete</th>
                            <th align="right">Add To Budget</th>
                """%jno_id
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
                    <td  align="right">
                    %s
                    </td>
                    <td  align="right">
                    %s
                    </td>
                        <td align="right">
                            %s
                        </td>
                    <td width='25px'>
                            <img id="editcontractscope" src="/images/Edit-16.png" >
                            </img>
                    </td>
                    <td width='25px'>
                            <img id="deletecontractscope"
                            src="/images/trash-16.png" >
                            </img>
                    </td>
                    <td width='25px'>
                            <img id="addtocontractscope"
                            src="/images/add_items.png" >
                            </img>
                    </td>
                    </tr>
                    """%(scp["id"],scp["item"],scp["description"],scp["unit"],scp["qty"],scp["price"],scp["total"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>


                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def ajaxsitescontractscopeofwork_production(self,jno_id,**kw):
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        for scp in scope:
            dictsites.append({'jno':scp.jno,
                          'id':scp.id,
                         'item':scp.item,
                         'description':scp.description,
                         'unit':scp.unit,
                         'qty':scp.qty,
                         'price':scp.price,
                         'total':scp.total,
                         })

        #subheadings = DBS_Jist3yrBuilding.query(JistEstimating3yrBuildingSubHeadings). \
        #            filter(JistEstimating3yrBuildingSubHeadings.id==int(jno)).one()
        html1 = """
               <h2 class="effect6">
               <span class='spanleft'>Contract Scope for JCNo: %s </span>
                <span class='spanright'>
                            <a href="/contractscont/exportcontract_scopepdf/%s">
                            <img id="pdfcontractscope" src="/images/pdficon.jpg"></img>
                            </a>
               </span>
               </h2>
                            <div id="button_space_sow"></div>
                            <table id='table_contracts_sow' class='table_estdata'>
                            <th>ID</th>
                            <th>Item</th>
                            <th>Description</th>
                            <th>Unit</th>
                            <th align="right">Qty</th>
                """%(jno_id,jno_id)
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
                    <td  align="right">
                    %s
                    </td>
                    </tr>
                    """%(scp["id"],scp["item"],scp["description"],scp["unit"],scp["qty"])
            html2 = html2 + temphtml1
        html3 = """
                            </table>


                """
        html =  html1 + html2 + html3
        return html

    @expose()
    def exportcontract_scopepdf(self,jno_id):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print jno_id 
        pdffile = CreatePDF(filename)
        userdata = []
        contractdata = []
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id).all()
        for scp in scope:
            dictsites.append({'jno':scp.jno,
                          'id':scp.id,
                         'item':scp.item,
                         'description':scp.description,
                         'unit':scp.unit,
                         'qty':scp.qty,
                         'price':scp.price,
                         'total':scp.total,
                         })
        count = len(scope) 
        #pointperson_name = User.by_user_id(point).user_name
        userdata.append([datetime.date(datetime.now()),
                        "Contract Scope For %s"%contracts.site,
                        ""
                        ])
        headers =["ID","Item","Description","Unit","Qty"]
        headerwidths=[40,120,350,80,60]
        pdffile.CreatePDFContractScope(userdata,dictsites,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent

    @expose()
    def ajax3yrOrderItemsAttachToScopeContract(self,uniqid,jno_id,**kw):
        if self.last_saved_scopecontract == uniqid:
            return
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        totalex = DBS_ContractData.query(JistContractOrderItems). \
                filter(JistContractOrderItems.jno==jno_id). \
                value(func.sum(JistContractOrderItems.total))
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        for thisites in contractsitems:
            dictsites.append({'jno':thisites.jno,
                          'id':thisites.id,
                         'item':thisites.item,
                         'description':thisites.description,
                         'unit':thisites.unit,
                         'qty':thisites.qty,
                         'price':thisites.price,
                         'total':thisites.total,
                         })
        for data in dictsites:
            newcontractscope = JistContractScope(jno=data['jno'],
                                         item=data['item'],
                                         description=data['description'],
                                         unit=data['unit'],
                                         qty=data['qty'],
                                         price=float(data['total'])/float(data['qty']),
                                         total=data['total'],
                                         dateadded = datetime.now(),
                                         dateedited = datetime.now(),
                                         useridnew=useridcreated,
                                         useridedited=useridcreated
                                       )
            
            DBS_ContractData.add(newcontractscope)
            DBS_ContractData.flush()
        self.last_saved_scopecontract = uniqid
        return

    @expose()
    def ajaxAttachSingleScopeToBudgets(self,uniqid,scope_id,**kw):
        if self.last_saved_scopecontract == uniqid:
            return
        dictsites = []
        scope = DBS_ContractData.query(JistContractScope).filter(JistContractScope.id==scope_id).one()
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        dictsites.append({'jno':scope.jno,
                      'id':scope.id,
                     'item':scope.item,
                     'description':scope.description,
                     'unit':scope.unit,
                     'qty':scope.qty,
                     'price':scope.price,
                     'total':scope.total,
                     })
        for data in dictsites:
            newcontractbudget = JistContractBudget(budget_jno=data['jno'],
                                         budget_item=data['item'],
                                         budget_description=data['description'],
                                         budget_unit=data['unit'],
                                         budget_qty=data['qty'],
                                         price_rate=data['price'],
                                         price_total=data['total'],
                                         dateadded = datetime.now(),
                                         dateedited = datetime.now(),
                                         useridnew=useridcreated,
                                         useridedited=useridcreated
                                       )
            DBS_ContractData.add(newcontractbudget)
            DBS_ContractData.flush()
        self.last_saved_scopecontract = uniqid
        return

    @expose()
    def ajax3yrOrderItemsAttachToBudgetContract(self,uniqid,jno_id,**kw):
        if self.last_saved_budgetcontract == uniqid:
            return
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractsitems = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.jno==jno_id). \
               all()
        totalex = DBS_ContractData.query(JistContractOrderItems). \
                filter(JistContractOrderItems.jno==jno_id). \
                value(func.sum(JistContractOrderItems.total))
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        for thisites in contractsitems:
            dictsites.append({'jno':thisites.jno,
                          'id':thisites.id,
                         'item':thisites.item,
                         'description':thisites.description,
                         'unit':thisites.unit,
                         'qty':thisites.qty,
                         'price':thisites.price,
                         'total':thisites.total,
                         })
        for data in dictsites:
            newcontractbudget = JistContractBudget(budget_jno=data['jno'],
                                         budget_item=data['item'],
                                         budget_description=data['description'],
                                         budget_unit=data['unit'],
                                         budget_qty=data['qty'],
                                         price_rate=data['price'],
                                         price_total=data['total'],
                                         dateadded = datetime.now(),
                                         dateedited = datetime.now(),
                                         useridnew=useridcreated,
                                         useridedited=useridcreated
                                       )
            DBS_ContractData.add(newcontractbudget)
            DBS_ContractData.flush()
        self.last_saved_budgetcontract = uniqid
        return

    @expose()
    def ajaxContractScopeAttachToBudgetContract(self,uniqid,jno_id,**kw):
        if self.last_saved_scopebudget == uniqid:
            return
        dictsites = []
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.jno==jno_id). \
               one()
        contractscopes = DBS_ContractData.query(JistContractScope).filter(JistContractScope.jno==jno_id). \
               all()
        totalex = DBS_ContractData.query(JistContractOrderItems). \
                filter(JistContractOrderItems.jno==jno_id). \
                value(func.sum(JistContractOrderItems.total))
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        for thisites in contractscopes:
            dictsites.append({'jno':thisites.jno,
                          'id':thisites.id,
                         'item':thisites.item,
                         'description':thisites.description,
                         'unit':thisites.unit,
                         'qty':thisites.qty,
                         'price':thisites.price,
                         'total':thisites.total,
                         })
        for data in dictsites:
            newcontractbudget = JistContractBudget(budget_jno=data['jno'],
                                         budget_item=data['item'],
                                         budget_description=data['description'],
                                         budget_unit=data['unit'],
                                         budget_qty=data['qty'],
                                         price_rate=data['price'],
                                         price_total=data['total'],
                                         dateadded = datetime.now(),
                                         dateedited = datetime.now(),
                                         useridnew=useridcreated,
                                         useridedited=useridcreated
                                       )
            
            DBS_ContractData.add(newcontractbudget)
            DBS_ContractData.flush()
        self.last_saved_scopebudget = uniqid
        return

    @expose()
    def ajaxDeleteContractScope(self,uniqid,scopeid,**kw):
        if uniqid == self.last_save_scopeiddeleted:
            return
        scopes=DBS_ContractData.query(JistContractScope). \
                            filter(JistContractScope.id==scopeid).one()
        #DBS_Jist3yrBuilding.delete(sitescope)
        DBS_ContractData.delete(scopes)
        self.last_save_scopeiddeleted = uniqid
        return

    @expose()
    def ajaxAddContractScope(self,uniqid,jno_id,**kw):
        if uniqid == self.last_save_scopecontractnew:
            return
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        newscopes = JistContractScope(jno=jno_id,
                                      item=kw['newscopeitem'],
                                      description=kw['newscopedescription'],
                                      unit=kw['newscopeunit'],
                                      qty=kw['newscopeqty'],
                                      price=kw['newscopeprice'],
                                      total=kw['newscopetotal'],
                                      useridnew = usernow.user_id,
                                      useridedited = usernow.user_id,
                                      dateadded = datetime.date(datetime.now()),
                                      dateedited = datetime.date(datetime.now())
                                      )                              
        DBS_ContractData.add(newscopes)
        DBS_ContractData.flush()
        self.last_save_scopecontractnew = uniqid
        return

    @expose()
    def ajaxEditContractScope(self,uniqid,scopeid,**kw):
        if uniqid == self.last_save_scopecontractnew:
            return
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        scopecontract = DBS_ContractData.query(JistContractScope).filter(JistContractScope.id==scopeid).one()
        #print scopecontract.id
        scopecontract.item=kw['editcontractscopeitem']
        scopecontract.description=kw['editcontractscopedescription']
        scopecontract.unit=kw['editcontractscopeunit']
        scopecontract.qty=kw['editcontractscopeqty']
        scopecontract.price=kw['editcontractscopeprice']
        scopecontract.total=kw['editcontractscopetotal']
        scopecontract.useridedited = usernow.user_id
        scopecontract.dateedited = datetime.date(datetime.now())
        DBS_ContractData.flush()
        self.last_save_scopecontractnew = uniqid
        return


    @expose()
    def ajaxaddorderitem(self,siteid,item='',description='',unit='',qty=0.00,price=0.00,total=0.00,**kw):
        if self.last_saved_item_description == description:
            return
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        new_item = JistContractOrderItems(jno = siteid,
                                       item=item,
                                       description=description,
                                       unit = unit,
                                       qty = qty,
                                       price = price,
                                       total = total,
                                       useridnew=useridcreated,
                                       useridedited=useridcreated,
                                       dateadded = datetime.now(),
                                       dateedited = datetime.now(),
                                       )
        DBS_ContractData.add(new_item)
        DBS_ContractData.flush()
        self.last_saved_item_description = description
        return

    @expose()
    def ajaxeditorderitem(self,uniq,itemid,siteid,item='',description='',unit='',qty=0.00,price=0.00,total=0.00,**kw):
        if self.last_saved_item_description == uniq:
            return
        #print itemid, siteid, description, total
        username = request.identity['repoze.who.userid']
        usernow = User.by_user_name(username)
        useridcreated = usernow.user_id
        orderitem = DBS_ContractData.query(JistContractOrderItems).filter(JistContractOrderItems.id==itemid). \
               one()
        orderitem.item=item
        orderitem.description=description
        orderitem.unit = unit
        orderitem.qty = qty
        orderitem.price = price
        orderitem.total = Decimal(total)
        orderitem.useridedited=useridcreated
        orderitem.dateedited = datetime.now()
        #DBS_ContractData.flush()
        self.last_saved_item_description = uniq 
        return


    @require(in_any_group("managers","contracts_group"))
    @expose('jistdocstore.templates.contracts.budgetconsole')
    def budgetconsole(self,**named):
        """Handle the 'requistion new' page."""
        contracts = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=="False"). \
               order_by(desc(JistContracts.jno)).all()
        return dict(page='Budget Console',
                    wip = contracts,
                    value=named)


    @expose()
    def ajaxeditcontractstatus(self,uniqid,jcno,point,siteagent,status,**kw):
        if self.last_saved_contract_status_rnd == uniqid:
            return
        #print point, siteagent,status
        #for k, w in kw.iteritems():
            #print k, w
        try:
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            useridcreated = usernow.user_id
            cdates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jcno).one()
        except:
            username = request.identity['repoze.who.userid']
            usernow = User.by_user_name(username)
            useridcreated = usernow.user_id
            new_contractdates = JistContractPlanningDates(jcno = int(jcno),
                                           useridnew = str(useridcreated),
                                           #dateadded = datetime.now(),
                                           #dateedited = datetime.now(),
                                           useridedited = useridcreated
                                           )
            DBS_ContractData.add(new_contractdates)
            DBS_ContractData.flush()
            cdates = DBS_ContractData.query(JistContractPlanningDates). \
                        filter(JistContractPlanningDates.jcno==jcno).one()
        #Change the locationid
        thissite = DBS_ContractData.query(JistContracts). \
                filter(JistContracts.jno==jcno).one()
        if kw['locationlistid'] != 'None':
            thissite.locationid = kw['locationlistid']
        else:
            pass
        cdates.planstartdate = kw['cont_planned_start_date']
        cdates.planenddate = kw['cont_planned_end_date']
        #print cdates.planstartdate
        #username = request.identity['repoze.who.userid']
        #usernow = User.by_user_name(username)
        #useridcreated = usernow.user_id
        cdates.useridnew = str(useridcreated)
        cdates.useridedited = str(useridcreated)
        DBS_ContractData.flush()
        #username = request.identity['repoze.who.userid']
        #usernow = User.by_user_name(username)
        statusjc = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jcno).one()
        statusjc.pointperson = point 
        statusjc.siteagent = siteagent
        statusjc.statuscode = status
        statusjc.sitehandoverdate = kw['cont_site_handover_date']
        statusjc.actualstartdate = kw['cont_actual_start_date']
        statusjc.firstdeldate = kw['cont_first_del_date']
        statusjc.finalcompldate = kw['cont_final_completion_date']
        statusjc.useridedited = usernow.user_id
        statusjc.dateedited = datetime.date(datetime.now())
        DBS_ContractData.flush()
        return

    @expose('jistdocstore.templates.contracts.contractsmaps')
    def contractsmaps(self, **kw):
        return dict(page='JIST Contracts Maps',
                    #twoweek = twoweek,
                    #points = pointlist,
                    )

    @expose()
    def get_map_contract_search_frm(self, **kw):
        html1 = """
            <form id="map_contract_search_frm">
                <fieldset class='fieldsetright'>

                    <label for="">Choose A Contract</label><br/>
                    <select name="filter_contract_one" id="filter_contract_one" class="text ui-widget-content ui-corner-all">
                    <option >Choose a Contract</option>
                """
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
                    filter(JistContracts.locationid!=None). \
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
        html2 = ''
        for scp in dictsites:
            html2temp = """
                        <option value='%s,%s,%s'>%s-%s-%s-%s-%s</option>
                        """%(scp["jno"],scp['loclat'],scp['loclng'],scp["jno"],scp["client"],scp["site"],scp["description"],scp['pointperson'])
            html2 = html2 + html2temp
        html3 = """
                    </select><br/>
                    <label for="">Filter By Point</label><br/>
                      <select id="filter_contract_point" style="display: block" class="text ui-widget-content ui-corner-all">
                """
        for point in pointlist:
            html3temp = """
                        <option value="%s">%s</option>

                          """%(point['user_id'],point['user_name'])
            html3 = html3 + html3temp
        
        html4 = """
                    </select><br/>
                    <label for="">Filter By Contract Group</label><br/>
                    <input type="text" name="filter_contract_group" id="filter_contract_group" class="text ui-widget-content ui-corner-all" /><br/>

                    <label for="">Filter By Min Contract Status</label><br/>
                    <input type="text" name="filter_min_contract_status" id="filter_min_contract_status" class="text ui-widget-content ui-corner-all" /><br/>

                    <label for="">Filter By Max Contract Status</label><br/>
                    <input type="text" name="filter_max_contract_status" id="filter_max_contract_status" class="text ui-widget-content ui-corner-all" /><br/>

                    <label for="">Filter By Min Contract Amount</label><br/>
                    <input type="text" name="filter_min_contract_amount" id="filter_min_contract_amount" class="text ui-widget-content ui-corner-all" /><br/>

                    <button class="ui-state-default ui-corner-all" id="btn_search_streetviewpic">Populate Map</button>                

                </fieldset>
            </form>

                """
        otherstuff = 'outerstuff'
        return html1 + html2 + html3  + html4 

    @expose()
    def get_point_contracts_coords(self, **kw):
        thispoint = kw['point']

        contracts = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                    filter(JistContracts.completed=="False"). \
                    filter(JistContracts.locationid!=None). \
                    filter(JistContractStatus.pointperson==int(thispoint)). \
                    order_by(desc(JistContracts.jno)).all()

        returnlist = []
        for con in contracts:
            try:
                statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==con.jno).one()
                pointperson = DBS_ContractData.query(User).filter(User.user_id==statusall.pointperson).one()
                locationone = DBS_ContractData.query(JistLocationList). \
                        filter(JistLocationList.id==con.locationid). \
                        one()
                returnlist.append({
                        'jcno':con.jno,
                        'point':pointperson.user_name,
                        'lat':locationone.lat,
                        'lng':locationone.lng

                    });
            except:
                pass

        return json.dumps({'pointlist':returnlist})
