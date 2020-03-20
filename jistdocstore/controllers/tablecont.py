# -*- coding: utf-8 -*-
"""Table Controller"""
from sqlalchemy import select
from tg import expose, flash, require, url, request, redirect, response, tmpl_context
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tgext.admin.tgadminconfig import TGAdminConfig
from tgext.admin.controller import AdminController
from tg import predicates

from jistdocstore.lib.base import BaseController
from tgext.crud import CrudRestController

from jistdocstore.model import DBS_ContractData, metadata2
from jistdocstore.model import DBSession, metadata
from jistdocstore import model

from tw.forms.fields import TextField, TextArea, CheckBox
from tw.api import *
from tw.api import WidgetsList
#from tw.extjs import ItemSelector
from jistdocstore.controllers.error import ErrorController
from sprox.recordviewbase import RecordViewBase
from sprox.formbase import EditableForm, Field
from sprox.fillerbase import EditFormFiller
from sprox.widgets import PropertySingleSelectField
from tw.forms import *
from tw.forms import FileField, TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
from tw.forms.validators import Int, NotEmpty,DateTimeConverter, DateConverter
from tw.forms.validators import * 
from formencode import Schema
from formencode import validators
from formencode.validators import FieldsMatch
from formencode.validators import Int, NotEmpty, DateConverter,DateValidator,PostalCode,String,Email,UnicodeString
from formencode.validators import *

#from jistdocstore.model.userfile import UserFile
from jistdocstore.model import * 

#__all__ = ['TableController']

from tg.controllers import RestController, redirect
from sprox.tablebase import TableBase
from sprox.fillerbase import TableFiller
from sprox.formbase import AddRecordForm
from tg import predicates
from tg.predicates import *
from datetime import datetime
#from tw.jquery import FlexiGrid
from tw.jquery import AjaxForm
from tw2.forms import RadioButtonTable as RDBT
from tw2.forms import CheckBoxTable as CBoxT 
#import tw2.jqplugins.ui.widgets as tw2widgets

class PointField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_ContractData.query(User).filter(User.active_status==True).all()
        options = [(str(point.user_id), '%s'%(point.user_name))
                            for point in points]
        d['options']= options
        return d

class PointFieldInt(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_ContractData.query(User).filter(User.active_status==True).all()
        options = [(point.user_id, '%s'%(point.user_name))
                            for point in points]
        d['options']= options
        return d

class StoresLocationField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_JistBuying.query(JistBuyingStoresLocation).filter(active==True).all()
        options = [(point.user_id, '%s'%(point.store_location))
                            for point in points]
        d['options']= options
        return d

class StoresNameField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_JistBuying.query(JistBuyingStoresLocation).filter(JistBuyingStoresLocation.active==True).all()
        options = [(point.id, '%s'%(point.store_name))
                            for point in points]
        d['options']= options
        return d

class PointFieldManage(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        apoints = DBS_ContractData.query(User). \
                filter(User.active_status==True). \
                all()
        #this = User.permissions
        pointlist = []
        for point in apoints:
            if point:
                user = User.by_user_id(point.user_id)
                userpermissions = user.permissions
                for permis in userpermissions:
                    #print permis.permission_name
                    if permis.permission_name=='productionmanage':
                        pointlist.append({'user_id':point.user_id,
                                          'user_name':point.user_name
                                          })
        #for p in pointlist:
        #    print p['user_id']
        options = [(pint['user_id'], '%s'%(pint['user_name']))
                            for pint in pointlist]
        d['options']= options
        return d

class JCNoWIPField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=True):
        codes = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=='False').all()
        options = [(str(code.jno), '%s - %s - %s'%(code.jno,code.site,code.description))
                            for code in codes]
        """
        entity = self.entity
        #print type(options)
        #options = self.provider.get_dropdown_options(self.entity, self.field_name, self.dropdown_field_names)
        if nullable:
            options.append([None,"-----------"])
        if len(options) == 0:
            return {}
        """
        d['options']= options
        return d

class JCNoWIPFieldInt(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=True):
        codes = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=='False').all()
        options = [(code.jno, '%s - %s - %s'%(code.jno,code.site,code.description))
                            for code in codes]
        """
        entity = self.entity
        #print type(options)
        #options = self.provider.get_dropdown_options(self.entity, self.field_name, self.dropdown_field_names)
        if nullable:
            options.append([None,"-----------"])
        if len(options) == 0:
            return {}
        """
        d['options']= options
        return d

class JCNoContractField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_ContractData.query(JistContracts).all()
        options = [(str(code.jno), '%s'%(code.site))
                            for code in codes]
        d['options']= options
        return d

class JCNoContractInvField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_ContractData.query(JistContracts). \
        order_by(desc(JistContracts.jno)). \
        all()
        options = [(str(code.jno), '%s - %s - %s - %s'%(code.jno,code.client,code.site,code.description))
                            for code in codes]
        d['options']= options
        return d

class InvoiceInvField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_JistInvoicing.query(JistInvoicesList). \
        order_by(desc(JistInvoicesList.id)). \
        all()
        options = [(code.id, '%s - %s - %s - %s '%(code.id,code.invoiceno,code.client,code.value_incl))
                            for code in codes]
        d['options']= options
        return d

class InvoicePaymentField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_JistInvoicing.query(JistInvoicesPayments). \
        order_by(desc(JistInvoicesPayments.id)). \
        all()
        options = [(str(code.id), '%s - %s - %s'%(code.id,code.invoiceid,code.amount))
                            for code in codes]
        d['options']= options
        return d

class SupplierField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_JistBuying.query(JistBuyingSupplierList). \
                filter(JistBuyingSupplierList.active==True). \
                all()
        #for p in enumerate(points):
        #    print p
        options = [(point.id, '%s'%(point.suppliername))
                            for point in points]
        d['options']= options
        return d

class BuyingOpenOrderNoField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_JistBuying.query(JistBuyingOrderList). \
                filter(JistBuyingOrderList.active=='Y'). \
                all()
        #for p in enumerate(points):
        #    print p
        options = [(point.id, '%s'%(point.ponumber))
                            for point in points]
        d['options']= options
        return d

class InvoiceClientField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        points = DBS_JistInvoicing.query(JistInvoicesList.client).distinct()
        #for p in enumerate(points):
        #    print p
        options = [(point, '%s'%(point.client))
                            for point in points]
        d['options']= options
        return d

class PercentField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        #codes = DBS_ContractData.query(JistContracts).all()
        codes = range(0,101,5)
        #print codes
        options = [(code, '%s'%(code))
                            for code in codes]
        d['options']= options
        return d

class HourField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        #codes = DBS_ContractData.query(JistContracts).all()
        codes = range(0,9)
        #print codes
        options = [(code, '%s'%(code))
                            for code in codes]
        d['options']= options
        return d

class FleetRegField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=True):
        codes = DBS_ContractData.query(JistFleetList).filter(JistFleetList.active==True).all()
        options = [(str(code.id), '%s - %s - %s'%(code.registration_number,
                                                 code.vehicle_description,
                                                 code.driver
                                                 ))
                            for code in codes]
        d['options']= options
        return d

class FleetDriverField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=True):
        codes = DBS_ContractData.query(JistFleetDriverList).filter(JistFleetDriverList.active==True).all()
        options = [(str(code.id), '%s '%(code.driver_name,
                                                 ))
                            for code in codes]
        d['options']= options
        return d

class StatusField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_ContractData.query(JistContractStatusCodes).all()
        #for p in enumerate(codes):
        #    print p
        #return
        options = [(code.id, '%s'%(code.status))
                            for code in codes]
        d['options']= options
        return d

class PicCategoryField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_JistFileStore.query(PictureCategory).all()
        options = [(str(code.id), '%s'%(code.categoryname))
                            for code in codes]
        d['options']= options
        return d

class LabourDivisionField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_JistLabour.query(JistLabourDivisions).all()
        options = [(code.id, '%s'%(code.division_name))
                            for code in codes]
        d['options']= options
        return d

class SubconDivisionField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_JistLabour.query(JistSubconDivisions).all()
        options = [(code.id, '%s'%(code.division_name))
                            for code in codes]
        d['options']= options
        return d

class SubconTradingNameField(PropertySingleSelectField):
    def _my_update_params(self, d, nullable=False):
        codes = DBS_JistLabour.query(JistSubconList).all()
        options = [(code.id, '%s'%(code.trading_name))
                            for code in codes]
        d['options']= options
        return d

class PropertyMixin(Widget):
    params = ['entity', 'field_name', 'provider', 'dropdown_field_names']

    def _my_update_params(self, d, nullable=False):
        entity = self.entity
        options = self.provider.get_dropdown_options(self.entity, self.field_name, self.dropdown_field_names)
        if nullable:
            options.append([None,"-----------"])
        if len(options) == 0:
            return {}
        d['options']= options

        return d

class MyCalendarDatePicker(CalendarDatePicker):
    not_empty = False
    button_text = "Choose a Date"
    date_format = "%Y-%m-%d"

    def __init__(self, *args, **kw):
            super(CalendarDatePicker, self).__init__(*args, **kw)
            if self.default is None and self.not_empty:
                self.default = lambda: datetime.now()
                #self.default = None 
            self.validator = self.validator or validators.DateTimeConverter(
                format=self.date_format, not_empty=self.not_empty,
                tzinfo=self.tzinfo
                )
    def get_calendar_lang_file_link(self, lang):
            """
            Returns a CalendarLangFileLink containing a list of name
            patterns to try in turn to find the correct calendar locale
            file to use.
            """
            fname = 'static/calendar/lang/calendar-%s.js' % lang.lower()
            return JSLink(modname='tw.forms',
                          filename=fname,
                          javascript=self.javascript)

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class ContractsTable(TableBase):
    __model__ = JistContracts
    __omit_fields__ = ['__actions__','tel','fax','orderno',
                        'cell','cidbcategory',
                        'cidbrating','contact','workcategory',
                        'groupjno','completed','pointperson', 
                        'useridnew','useridedited',
                        'dateadded','dateedited']
    __column_widths__={'JCNo':"30em",
                        'Description':"170em",
                        'Client':"100em"
                      }
    __headers__={'jno':'JCNo',
                'description':'Description',
                'orderdate':'PO Date',
                'client':'Client',
                'site': 'Site',
                'status':'Point'
                }
    __field_order__ = ['jno','client','site','description']

    __xml_fields__ = ['JCNo','Point']
spx_contracts_table = ContractsTable(DBS_ContractData);

class ContractsTableFiller(TableFiller):
    __model__ = JistContracts 
    def jno(self, obj):
        #jno = ', '.join(['<a href="/get_one/'+str(d.jno)+'"></a>'
        #                       for d in obj.JistContracts])
        #return jno.join(('<div>', '</div>'))
        jno = '<a href="/productioncont/get_one/'+str(obj.jno)+'">'+str(obj.jno)+'</a>'
        #print jno
        return jno.join(('<div>', '</div>'))

    def status(self, obj):
        for d in obj.status:
            #status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
        return status.user_name.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
        #movies = DBSession.query(Movie).filter(Movie.directors.contains(director)).all()
        wip1 = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=='False').all()
        return len(wip1),wip1 
contracts_filler = ContractsTableFiller(DBS_ContractData)

class MYContractsTableFiller(TableFiller):
    __model__ = JistContracts 
    def jno(self, obj):
           jno = '<a href="/productioncont/get_one/'+str(obj.jno)+'">'+str(obj.jno)+'</a>'
           return jno.join(('<div>', '</div>'))

    def status(self, obj):
            for d in obj.status:
                status = d.pointperson
                status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
            return status.user_name.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                    filter(JistContracts.completed=='False'). \
                    filter(JistContractStatus.pointperson==user.user_id). \
                    all()

            return len(wip1),wip1 
mycontracts_filler = MYContractsTableFiller(DBS_ContractData)

class ContractsSiteAgentFiller(TableFiller):
    __model__ = JistContracts 
    def jno(self, obj):
           jno = '<a href="/productioncont/get_one/'+str(obj.jno)+'">'+str(obj.jno)+'</a>'
           return jno.join(('<div>', '</div>'))

    def status(self, obj):
            for d in obj.status:
                status = d.pointperson
                status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
            return status.user_name.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                    filter(JistContracts.completed=='False'). \
                    filter(JistContractStatus.siteagent==user.user_id). \
                    all()

            return len(wip1),wip1 
contracts_siteagent_filler = ContractsSiteAgentFiller(DBS_ContractData)

class ContractFileListTable(TableBase):
        __model__ = FileStoreProduction 
        __omit_fields__ = ['__actions__','filecontent','fileunder','thumbname',
                            'id','useridcreated','datecreated']
        __column_widths__={'JCNo':"30em",
                            'Description':"170em",
                            'Client':"100em"
                          }
        __headers__={'jno':'JCNo',
                    'status':'Point'
                    }
        __field_order__ = ['jno']

        __xml_fields__ = ['JCNo']
        takenby = PointField
spx_contract_file_list = ContractFileListTable(DBS_JistFileStore);

class ContractsFileFiller(TableFiller):
    __model__ = FileStoreProduction 

    def jno(self, obj):
        #jno = ', '.join(['<a href="/get_one/'+str(d.jno)+'"></a>'
        #                       for d in obj.JistContracts])
        #return jno.join(('<div>', '</div>'))
        jno = '<a href="/production/get_one/'+str(obj.jno)+'">'+str(obj.jno)+'</a>'
        #print jno
        return jno.join(('<div>', '</div>'))

    def takenby(self, obj):
        #for d in obj.takenby:
            #status = d.pointperson
        status = DBS_ContractData.query(User).filter(User.user_id==obj.takenby).one()
        return status.user_name.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,jno=None, **kw):
        #print "JNo to provider is: %s"%jno
        #print kw
        #print kw['values']
        cfiles = DBS_JistFileStore.query(FileStoreProduction). \
                            filter(FileStoreProduction.jcno==jno).all()
            #p1 = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jno).one()
        #print "CFiles is %s"%cfiles
        return len(cfiles),cfiles 
contracts_file_filler = ContractsFileFiller(DBS_JistFileStore)

class JCNoWIPListBox(AddRecordForm):
    __model__ = JistContracts 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__ = ['__actions__','tel','fax','orderno',
                        'cell','cidbcategory',
                        'cidbrating','contact','workcategory',
                        'groupjno','completed','pointperson', 
                        'useridnew','useridedited',
                        'dateadded','dateedited']
    __hide_fields__ = [
                        'description',
                        'orderdate',
                        'jno',
                        'status',
                        'client',
                        'point',
                       ]
    site = JCNoWIPFieldInt 
jcno_wip_list_box = JCNoWIPListBox(DBS_ContractData,action="")

#************************************************************************************************
#************************************************************************************************

class PurchaseReqsTable(TableBase):
    __model__ = JistBuyingPurchaseReqsList
    __omit_fields__ = ['__actions__','useridnew']
    __column_widths__={'JCNo':"30em",
                        'Client':"100em"
                      }
    __headers__={
                'id':'ID',
                'jcno':'JCNo',
                'must_have_date':'Must Have Date',
                'prefered_supplier':'Preferred Supplier',
                'active':'Active',
                'dateadded':'Date Added'
                }
    """
                'client':'Client',
                'site': 'Site',
                'status':'Point'
                }
    __field_order__ = ['jno','client','site','description']
    """

    __xml_fields__ = ['ID','JCNo']
spx_purchase_reqs = PurchaseReqsTable(DBS_JistBuying);

class PurchaseReqsOpenTable(TableBase):
    __model__ = JistBuyingPurchaseReqsList
    __omit_fields__ = ['__actions__','active']
    __column_widths__={'JCNo':"30em",
                        'Client':"100em"
                      }
    __headers__={
                'id':'ID',
                'jcno':'JCNo',
                'must_have_date':'Must Have Date',
                'prefered_supplier':'Preferred Supplier',
                'dateadded':'Date Added',
                'useridnew':'Added By',
                }
    __xml_fields__ = ['ID','JCNo','Added By']
spx_open_purchase_reqs = PurchaseReqsOpenTable();

class MYPurchaseReqsOpenFiller(TableFiller):
    __model__ = JistBuyingPurchaseReqsList 
    def id(self, obj):
           id = '<a href="/logisticscont/requisition_buying_one/'+str(obj.id)+'">'+str(obj.id)+'</a>'
           return id.join(('<div>', '</div>'))

    def jcno(self, obj):
           jcno = '<a href="/productioncont/get_one/'+str(obj.jcno)+'">'+str(obj.jcno)+'</a>'
           return jcno.join(('<div>', '</div>'))

    def useridnew(self, obj):
           user = User.by_user_id(obj.useridnew)
           useridnew = user.user_name 
           return useridnew.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                    filter(JistBuyingPurchaseReqsList.active==True). \
                    order_by(desc(JistBuyingPurchaseReqsList.id)). \
                    all()

            return len(wip1),wip1 
openpurchasereq_filler = MYPurchaseReqsOpenFiller(DBS_JistBuying)

class MYPurchaseReqsFiller(TableFiller):
    __model__ = JistBuyingPurchaseReqsList 
    def id(self, obj):
           id = '<a href="/logisticscont/requisition_one/'+str(obj.id)+'">'+str(obj.id)+'</a>'
           return id.join(('<div>', '</div>'))

    def jcno(self, obj):
           jcno = '<a href="/productioncont/get_one/'+str(obj.jcno)+'">'+str(obj.jcno)+'</a>'
           return jcno.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_JistBuying.query(JistBuyingPurchaseReqsList). \
                    filter(JistBuyingPurchaseReqsList.useridnew==user.user_id). \
                    order_by(desc(JistBuyingPurchaseReqsList.id)). \
                    all()

            return len(wip1),wip1 
mypurchasereq_filler = MYPurchaseReqsFiller(DBS_JistBuying)

class MyTelephoneMsgs(TableBase):
    __model__ = JistReceptionTelephoneMessages 
    __omit_fields__ = ['__actions__','to_user',]
    __column_widths__={'JCNo':"30em",
                        'Client':"100em"
                      }
    __headers__={
                'id':'ID',
                'active':'Active',
                'from_person':'From Person',
                'call_back':'Call Back Please',
                'call_again':'Call You Again',
                'no_message':'No Message',
                'message':'Message',
                'dateadded':'Date Added',
                'return_tel':'Return Tel',
                'useridnew':'Added By',
                }
    """
                'client':'Client',
                'site': 'Site',
                'status':'Point'
                }
    __field_order__ = ['jno','client','site','description']
    """
    __xml_fields__ = ['Added By','Active']
spx_open_telephone_msgs = MyTelephoneMsgs(DBS_ContractData);

class MYReceptionMessagesFiller(TableFiller):
    __model__ = JistReceptionTelephoneMessages 
    def useridnew(self, obj):
            #for d in obj.status:
            #    status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==obj.useridnew).one()
            return status.user_name.join(('<div>', '</div>'))

    def active(self, obj):
            #for d in obj.status:
            #    status = d.pointperson
            #jno = '<a href="../togglemsgactive/'+str(obj.id)+'">'+str(obj.active)+'</a>'
            if str(obj.active) == "True":
                jno = '<a href="../togglemsgactive/'+str(obj.id)+'">'+'Hide</a>'
            else:
                jno = '<a href="../togglemsgactive/'+str(obj.id)+'">'+'UnHide</a>'
            return jno.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,**kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_ContractData.query(JistReceptionTelephoneMessages). \
                    filter(JistReceptionTelephoneMessages.to_user==user.user_id). \
                    filter(JistReceptionTelephoneMessages.active==True). \
                    order_by(desc(JistReceptionTelephoneMessages.id)). \
                    all()
            return len(wip1),wip1 
myreceptionmsgs_filler = MYReceptionMessagesFiller(DBS_ContractData)

class MyOutOfOfficeMovements(TableBase):
    __model__ = JistOutOfOfficeNotices 
    __omit_fields__ = ['__actions__',]
    __headers__={
                'id':'ID',
                'active':'Active',
                'from_person':'From Person',
                'call_back':'Call Back Please',
                'call_again':'Call You Again',
                'no_message':'No Message',
                'message':'Message',
                'dateadded':'Date Added',
                'return_tel':'Return Tel',
                'useridnew':'Added By',
                }
    __xml_fields__ = ['Active']
spx_open_out_of_office_notices = MyOutOfOfficeMovements();

#************************************************************************************************
#************************************************************************************************
class FleetListTable(TableBase):
    __model__ = JistFleetList 
    __omit_fields__ = ['__actions__',
                       'vin_number','engine_number',
                       'n_r_number','tare','fuel_type',
                       'service_center','service_center_tel_no',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_list = FleetListTable();

class FleetListFiller(TableFiller):
    __model__ = JistFleetList 
    def id(self, obj):
        id = '<a href="/transportcont/edit_fleet/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def status(self, obj):
        for d in obj.status:
            #status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
        return status.user_name.join(('<div>', '</div>'))
fleet_list_filler = FleetListFiller(DBS_ContractData)

class FleetDriverListTable(TableBase):
    __model__ = JistFleetDriverList 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_drivers = FleetDriverListTable();

class FleetDriversFiller(TableFiller):
    __model__ = JistFleetDriverList 
    def id(self, obj):
        id = '<a href="/transportcont/edit_driver/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def status(self, obj):
        for d in obj.status:
            #status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
        return status.user_name.join(('<div>', '</div>'))
fleet_drivers_filler = FleetDriversFiller(DBS_ContractData)

class FleetMaintenanceListTable(TableBase):
    __model__ = JistFleetMaintenanceList 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_maintenance = FleetMaintenanceListTable();

class FleetmaintenanceFiller(TableFiller):
    __model__ = JistFleetMaintenanceList 
    def id(self, obj):
        id = '<a href="/transportcont/edit_maintenance/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def status(self, obj):
        for d in obj.status:
            #status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
        return status.user_name.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,fleetid=0, **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_ContractData.query(JistFleetMaintenanceList). \
                    filter(JistFleetMaintenanceList.fleetid==fleetid). \
                    all()
            return len(wip1),wip1 
fleet_maintenance_filler = FleetmaintenanceFiller(DBS_ContractData)

class FleetFuelUsage(TableBase):
    __model__ = JistFleetFuelUsage 
    __omit_fields__ = ['__actions__',
                       'vin_number','engine_number',
                       'n_r_number','tare','fuel_type',
                       'service_center','service_center_tel_no',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_fuel_usage = FleetFuelUsage();

class FleetFuelUsageFiller(TableFiller):
    __model__ = JistFleetFuelUsage 
    def id(self, obj):
        id = '<a href="/transportcont/edit_fleet/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            #for m in kw:
            #    print m
            wip1 = DBS_ContractData.query(JistFleetFuelUsage). \
                    filter(JistFleetFuelUsage.id==int(1)). \
                    all()
            return len(wip1),wip1 
fleet_fuel_usage_filler = FleetFuelUsageFiller(DBS_ContractData)

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class LabourList(TableBase):
    __model__ = JistLabourList 
    __omit_fields__ = ['__actions__',
                       'tel_number_home','bank','branch_code','account_number',
                       'address1','address2','next_of_kin_name','next_of_kin_tel',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID','division','emp_number']
spx_labour_list = LabourList();

class LabourFiller(TableFiller):
    __model__ = JistLabourList 

    def id(self, obj):
        id = '<a href="/labourcont/editlabour/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def emp_number(self, obj):
        emp_number = '<a href="/labourcont/editlabour/'+str(obj.id)+'">'+str(obj.emp_number)+'</a>'
        return emp_number.join(('<div>', '</div>'))

    def division(self, obj):
        if not obj.division:
            return('<div>None</div>')
        vision = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.id==obj.division). \
                    one()
        division = vision.division_name
        return division.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,**kw):
            p1 = DBS_JistLabour.query(JistLabourList). \
                    order_by(desc(JistLabourList.id)). \
                    all()
            return len(p1),p1 
labour_filler = LabourFiller(DBS_JistLabour)

class LabourList(EditableForm):
    __model__ = JistLabourList 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','emp_number','dateedited','contract',]
    __field_order__ = ['id','first_name','last_name','date_started',
                        'id_number','rate_per_day','tel_number_home',
                        'bank','account_number','next_of_kin_name',
                        'site_handover_date']
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id']
    division = LabourDivisionField
labour_list_form = LabourList(DBS_JistLabour,action="")

class LabourListFiller(EditFormFiller):
    __model__ = JistLabourList
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistLabourList). \
                    filter(JistLabourList.id==id).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
labour_list_filler = LabourListFiller(DBS_JistLabour)

class AddNewLabourList(AddRecordForm):
    __model__ = JistLabourList 
    __omit_fields__ = ['__actions__','id','emp_number',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    division = LabourDivisionField
add_new_labour_form = AddNewLabourList(DBS_JistLabour,action="")

class LabourActiveList(TableBase):
    __model__ = JistLabourList 
    __omit_fields__ = ['__actions__',
                       'tel_number_home','bank','branch_code','account_number',
                       'address1','address2','next_of_kin_name','next_of_kin_tel',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID','division','emp_number']
spx_active_labour_list = LabourActiveList();

class LabourActiveFiller(TableFiller):
    __model__ = JistLabourList 

    def id(self, obj):
        id = '<a href="/labourcont/showlabouronepaymentdata/'+str(obj.id)+'">View Payment History</a>'
        return id.join(('<div>', '</div>'))

    def division(self, obj):
        if not obj.division:
            return('<div>None</div>')
        vision = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.id==obj.division). \
                    one()
        division = vision.division_name
        return division.join(('<div>', '</div>'))

    def emp_number(self, obj):
        emp_number = '<a href="/labourcont/editlabour/'+str(obj.id)+'">'+str(obj.emp_number)+'</a>'
        return emp_number.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,id=None,**kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_JistLabour.query(JistLabourList). \
                    filter(JistLabourList.active==True). \
                    all()

            return len(wip1),wip1 
labour_active_filler = LabourActiveFiller(DBS_JistLabour)

#************************************************************************************************
#************************************************************************************************

class LabourdivisionsList(TableBase):
    __model__ = JistLabourDivisions 
    __omit_fields__ = ['__actions__','id',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    #__headers__={
    #            'id':'ID',
    #            }
    __xml_fields__ = ['division_leader','division_code']
spx_divisions_labour_list = LabourdivisionsList();

class LabourdivisionsFiller(TableFiller):
    __model__ = JistLabourDivisions 
    def id(self, obj):
        id = '<a href="/labourcont/editdivisions/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def division_code(self, obj):
        division_code = '<a href="/labourcont/editdivisions/'+str(obj.id)+'">'+str(obj.division_code)+'</a>'
        return division_code.join(('<div>', '</div>'))

    def division_leader(self, obj):
        if not obj.division_leader:
            return('<div>None</div>')
        status = DBS_ContractData.query(User).filter(User.user_id==obj.division_leader).one()
        division_leader = status.user_name
        return division_leader.join(('<div>', '</div>'))
labour_divisions_filler = LabourdivisionsFiller(DBS_JistLabour)

class LabourDivisionList(EditableForm):
    __model__ = JistLabourDivisions 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','emp_number','dateedited','contract',]
    __field_order__ = ['id','first_name','last_name','date_started',
                        'id_number','rate_per_day','tel_number_home',
                        'bank','account_number','next_of_kin_name',
                        'site_handover_date']
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','division_code']
    division_leader=PointFieldInt
labour_division_list_form = LabourDivisionList(DBS_JistLabour,action="")

class LabourDivisionListFiller(EditFormFiller):
    __model__ = JistLabourDivisions
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistLabourDivisions). \
                    filter(JistLabourDivisions.id==id).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
labour_division_list_filler = LabourDivisionListFiller(DBS_JistLabour)

class AddNewDivision(AddRecordForm):
    __model__ = JistLabourDivisions 
    __omit_fields__ = ['__actions__','division_code','id','emp_number',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    division_leader = PointField
add_new_labour_division_form = AddNewDivision(DBS_JistLabour,action="")

#************************************************************************************************
#************************************************************************************************

class Labourpayment_runsList(TableBase):
    __model__ = JistLabourPaymentRunsList 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded'
                       ]
    __headers__={
                'id':'edit_dates',
                'payment_number':'action',
                'useridnew':'division_summaries',
                }
    division_leader = PointField
    __xml_fields__ = ['edit_dates','action','division_summaries']
spx_payment_runs_labour_list = Labourpayment_runsList();

class Labourpayment_runsFiller(TableFiller):
    __model__ = JistLabourPaymentRunsList 
    def id(self, obj):
        id = '<a href="/labourcont/editlabourpaymentrun/'+str(obj.id)+'">Edit Dates</a>'
        return id.join(('<div>', '</div>'))

    def useridnew(self, obj):
        useridnew= '<a href="/labourcont/showdivsummariespaymentrun/'+str(obj.payment_number)+'">Division Summaries</a>'
        return useridnew.join(('<div>', '</div>'))

    def payment_number(self, obj):
        payment_number = '<a href="/labourcont/showlabourpaymentdata/'+str(obj.id)+'">Edit Timesheets</a>'
        return payment_number.join(('<div>', '</div>'))

    def division_leader(self, obj):
        if not obj.division_leader:
            return('<div>None</div>')
        status = DBS_ContractData.query(User).filter(User.user_id==obj.division_leader).one()
        division_leader = status.user_name
        return division_leader.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,**kw):
            p1 = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                    order_by(desc(JistLabourPaymentRunsList.payment_date)). \
                    all()
            return len(p1),p1 
payment_runs_filler = Labourpayment_runsFiller(DBS_JistLabour)

class LabourPaymentList(EditableForm):
    __model__ = JistLabourPaymentRunsList 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited','payment_number',
                        'dateadded','total_gross','dateedited','contract',]
    __field_order__ = ['id','payment_date','start_date','end_date',
                        'site_handover_date',]
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','division_code']
    division_leader=PointFieldInt
payment_run_list_form = LabourPaymentList(DBS_JistLabour,action="")

class LabourPaymentListFiller(EditFormFiller):
    __model__ = JistLabourPaymentRunsList
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistLabourPaymentRunsList). \
                    filter(JistLabourPaymentRunsList.id==id). \
                    one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
payment_run_list_filler = LabourPaymentListFiller(DBS_JistLabour)

class AddNewLabourpayment_run(AddRecordForm):
    __model__ = JistLabourPaymentRunsList 
    __omit_fields__ = ['__actions__','payment_number','id','total_gross',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    #division_leader = PointField
add_new_payment_run_form = AddNewLabourpayment_run(DBS_JistLabour,action="")


#************************************************************************************************
#************************************************************************************************

class Labourpayment_dataList(TableBase):
    __model__ = JistLabourPaymentRunsData 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    #__headers__={
    #            'id':'ID',
    #            }
    __xml_fields__ = ['id',]
spx_payment_data_labour_list = Labourpayment_dataList();

class Labourpayment_dataFiller(TableFiller):
    __model__ = JistLabourPaymentRunsData 

    def _do_get_provider_count_and_objs(self,id=None,**kw):
        p1 = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                filter(JistLabourPaymentRunsData.paylist_id==id). \
                order_by(desc(JistLabourPaymentRunsData.id)). \
                all()
        return len(p1),p1 

    def id(self, obj):
        id = '<a href="/labourcont/editlabourpaymentrun/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))


payment_data_filler = Labourpayment_dataFiller(DBS_JistLabour)

class LabourPaymentDataList(EditableForm):
    __model__ = JistLabourPaymentRunsData 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited','payment_number',
                        'paylist_id','div_id','rate_per_day','empl_id',
                        'amount_net_total','amount_gross_total','amount_sunday_time',
                        'amount_normal_time','uif','amount_over_time','rate_per_hour',
                        'dateadded','total_gross','dateedited','contract',]
    __field_order__ = ['id','rate_per_day',
                       'hours_normal','hours_over_time',
                       'hours_sunday_time','paye','staff_loans',

                        ]
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','division_code']
payment_data_list_form = LabourPaymentDataList(DBS_JistLabour,action="")

class LabourPaymentListFiller(EditFormFiller):
    __model__ = JistLabourPaymentRunsData
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistLabourPaymentRunsData). \
                    filter(JistLabourPaymentRunsData.id==id). \
                    one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
payment_data_list_filler = LabourPaymentListFiller(DBS_JistLabour)

class AddNewPayment_data(AddRecordForm):
    __model__ = JistLabourPaymentRunsData 
    __omit_fields__ = ['__actions__','payment_number','id','total_gross',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    #division_leader = PointField
add_new_payment_data_form = AddNewPayment_data(DBS_JistLabour,action="")

#************************************************************************************************
#************************************************************************************************

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class SubconList(TableBase):
    __model__ = JistSubconList 
    __omit_fields__ = ['__actions__',
                       'tel_number_home','bank','branch_code','account_number',
                       'address1','address2','next_of_kin_name','next_of_kin_tel',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID',]
spx_subcon_list = SubconList(DBS_JistLabour)

class SubconFiller(TableFiller):
    __model__ = JistSubconList 

    def id(self, obj):
        #print obj.id
        id = '<a href="/labourcont/editsubcon/'+str(obj.id)+'">Edit Subcon</a>'
        return id.join(('<div>', '</div>'))

    def division(self, obj):
        if not obj.division:
            return('<div>None</div>')
        vision = DBS_JistLabour.query(JistSubconDivisions). \
                    filter(JistSubconDivisions.id==obj.division). \
                    one()
        division = vision.division_name
        return division.join(('<div>', '</div>'))

    def emp_number(self, obj):
        emp_number = '<a href="/labourcont/editsubcon/'+str(obj.id)+'">'+str(obj.emp_number)+'</a>'
        return emp_number.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,id=None,**kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_JistLabour.query(JistSubconList). \
                    all()

            return len(wip1),wip1 
    """
    def id(self, obj):
        id = '<a href="/labourcont/editsubcon/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def trading_name(self, obj):
        trading_name = '<a href="/labourcont/editsubcon/'+str(obj.id)+'">'+str(obj.trading_name)+'</a>'
        return trading_name.join(('<div>', '</div>'))

    def division(self, obj):
        if not obj.division:
            return('<div>None</div>')
        vision = DBS_JistLabour.query(JistSubconDivisions). \
                    filter(JistSubconDivisions.id==obj.division). \
                    one()
        division = vision.division_name
        return division.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,id=None,**kw):
            p1 = DBS_JistLabour.query(JistSubconList). \
                    all()
            return len(p1),p1 
    """
subcon_filler = SubconFiller(DBS_JistLabour)

class SubconListEdit(EditableForm):
    __model__ = JistSubconList 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','emp_number','dateedited','contract',]
    __field_order__ = ['trading_name','vat_number','first_name','last_name','date_started',
                        'id_number','rate_per_day','tel_number_home',
                        'bank','account_number','next_of_kin_name',
                        ]
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id']
    division = SubconDivisionField
subcon_list_form = SubconListEdit(DBS_JistLabour,action="")

class SubconListFiller(EditFormFiller):
    __model__ = JistSubconList
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.id==id).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
subcon_list_filler = SubconListFiller(DBS_JistLabour)

class AddNewSubconList(AddRecordForm):
    __model__ = JistSubconList 
    __omit_fields__ = ['__actions__','id','emp_number',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    division = SubconDivisionField
add_new_subcon_form = AddNewSubconList(DBS_JistLabour,action="")

class SubconActiveList(TableBase):
    __model__ = JistSubconList 
    __omit_fields__ = ['__actions__',
                       'tel_number_home','bank','branch_code','account_number',
                       'address1','address2','next_of_kin_name','next_of_kin_tel',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID','division','emp_number']
spx_active_subcon_list = SubconActiveList();

class SubconActiveFiller(TableFiller):
    __model__ = JistSubconList 

    def id(self, obj):
        id = '<a href="/labourcont/editsubcon/'+str(obj.id)+'">Edit Subcon</a>'
        return id.join(('<div>', '</div>'))

    def division(self, obj):
        if not obj.division:
            return('<div>None</div>')
        vision = DBS_JistLabour.query(JistSubconDivisions). \
                    filter(JistSubconDivisions.id==obj.division). \
                    one()
        division = vision.division_name
        return division.join(('<div>', '</div>'))

    def emp_number(self, obj):
        emp_number = '<a href="/labourcont/editsubcon/'+str(obj.id)+'">'+str(obj.emp_number)+'</a>'
        return emp_number.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,id=None,**kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_JistLabour.query(JistSubconList). \
                    filter(JistSubconList.active==True). \
                    all()

            return len(wip1),wip1 
subcon_active_filler = SubconActiveFiller(DBS_JistLabour)

class AddNewSubconData(AddRecordForm):
    __model__ = JistSubconPaymentRunsData 
    __omit_fields__ = ['__actions__','id','emp_number',
                        'sub_id','div_id','paylist_id',
                       'dateedited','useridedited','total_excl',
                       'dateadded','useridnew','active'
                       ]
    jcno = JCNoWIPField 
add_new_subcon_payment_data_form = AddNewSubconData(DBS_JistLabour,action="")


#************************************************************************************************
#************************************************************************************************

class SubcondivisionsList(TableBase):
    __model__ = JistSubconDivisions 
    __omit_fields__ = ['__actions__','id',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    #__headers__={
    #            'id':'ID',
    #            }
    __xml_fields__ = ['division_leader','division_code']
spx_divisions_subcon_list = SubcondivisionsList();

class SubcondivisionsFiller(TableFiller):
    __model__ = JistSubconDivisions 
    def id(self, obj):
        id = '<a href="/labourcont/editsubcondivisions/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def division_code(self, obj):
        division_code = '<a href="/labourcont/editsubcondivisions/'+str(obj.id)+'">'+str(obj.division_code)+'</a>'
        return division_code.join(('<div>', '</div>'))

    def division_leader(self, obj):
        if not obj.division_leader:
            return('<div>None</div>')
        status = DBS_ContractData.query(User).filter(User.user_id==obj.division_leader).one()
        division_leader = status.user_name
        return division_leader.join(('<div>', '</div>'))
subcon_divisions_filler = SubcondivisionsFiller(DBS_JistLabour)

class SubconDivisionList(EditableForm):
    __model__ = JistSubconDivisions 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','emp_number','dateedited','contract',]
    __field_order__ = ['id','first_name','last_name','date_started',
                        'id_number','rate_per_day','tel_number_home',
                        'bank','account_number','next_of_kin_name',
                        'site_handover_date']
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','division_code']
    division_leader=PointFieldInt
subcon_division_list_form = SubconDivisionList(DBS_JistLabour,action="")

class SubconDivisionListFiller(EditFormFiller):
    __model__ = JistSubconDivisions
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistSubconDivisions). \
                    filter(JistSubconDivisions.id==id).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
subcon_division_list_filler = SubconDivisionListFiller(DBS_JistLabour)

class AddNewDivision(AddRecordForm):
    __model__ = JistSubconDivisions 
    __omit_fields__ = ['__actions__','division_code','id','emp_number',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    division_leader = PointField
add_new_subcon_division_form = AddNewDivision(DBS_JistLabour,action="")

#************************************************************************************************
#************************************************************************************************

class Subconpayment_runsList(TableBase):
    __model__ = JistSubconPaymentRunsList 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded'
                       ]
    __headers__={
                'id':'edit_dates',
                'payment_number':'action',
                'useridnew':'division_summaries',
                }
    division_leader = PointField
    __xml_fields__ = ['edit_dates','action','division_summaries']
spx_payment_runs_subcon_list = Subconpayment_runsList();

class Subconpayment_runsFiller(TableFiller):
    __model__ = JistSubconPaymentRunsList 
    def id(self, obj):
        id = '<a href="/labourcont/editsubconpaymentrun/'+str(obj.id)+'"> Edit Dates Run' +str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def useridnew(self, obj):
        useridnew= '<a href="/labourcont/showsubsummariespaymentrun/'+str(obj.payment_number)+'">Subcon Summaries</a>'
        return useridnew.join(('<div>', '</div>'))

    def payment_number(self, obj):
        payment_number = '<a href="/labourcont/showsubconpaymentdata/'+str(obj.id)+'">Edit Claims</a>'
        return payment_number.join(('<div>', '</div>'))

    def division_leader(self, obj):
        if not obj.division_leader:
            return('<div>None</div>')
        status = DBS_ContractData.query(User).filter(User.user_id==obj.division_leader).one()
        division_leader = status.user_name
        return division_leader.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,**kw):
            p1 = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                    order_by(desc(JistSubconPaymentRunsList.payment_date)). \
                    all()
            return len(p1),p1 
subconpayment_runs_filler = Subconpayment_runsFiller(DBS_JistLabour)

class SubconPaymentList(EditableForm):
    __model__ = JistSubconPaymentRunsList 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited','payment_number',
                        'dateadded','total_gross','dateedited','contract',]
    __field_order__ = ['id','payment_date','start_date','end_date',
                        'site_handover_date',]
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','division_code']
    division_leader=PointFieldInt
subconpayment_run_list_form = SubconPaymentList(DBS_JistLabour,action="")

class SubconPaymentListFiller(EditFormFiller):
    __model__ = JistSubconPaymentRunsList
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistSubconPaymentRunsList). \
                    filter(JistSubconPaymentRunsList.id==id). \
                    one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
subconpayment_run_list_filler = SubconPaymentListFiller(DBS_JistLabour)

class AddNewpayment_run(AddRecordForm):
    __model__ = JistSubconPaymentRunsList 
    __omit_fields__ = ['__actions__','payment_number','id','total_gross',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    #division_leader = PointField
subconadd_new_payment_run_form = AddNewpayment_run(DBS_JistLabour,action="")

#************************************************************************************************
#************************************************************************************************

class Subconpayment_dataList(TableBase):
    __model__ = JistSubconPaymentRunsData 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    #__headers__={
    #            'id':'ID',
    #            }
    __xml_fields__ = ['id',]
spx_payment_data_subcon_list = Subconpayment_dataList();

class Subconpayment_dataFiller(TableFiller):
    __model__ = JistSubconPaymentRunsData 

    def _do_get_provider_count_and_objs(self,id=None,**kw):
        p1 = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                filter(JistSubconPaymentRunsData.paylist_id==id). \
                order_by(desc(JistSubconPaymentRunsData.id)). \
                all()
        return len(p1),p1 

    def id(self, obj):
        id = '<a href="/labourcont/editsubconpaymentrun/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))


payment_data_filler = Subconpayment_dataFiller(DBS_JistLabour)

class SubconPaymentDataList(EditableForm):
    __model__ = JistSubconPaymentRunsData 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited','payment_number',
                        'paylist_id','div_id','rate_per_day','sub_id',
                        'amount_net_total','amount_gross_total','amount_sunday_time',
                        'amount_normal_time','uif','amount_over_time','rate_per_hour',
                        'dateadded','total_gross','dateedited','total_excl',]
    __field_order__ = ['jcno','item',
                       'description','unit',
                       'qty','price',

                        ]
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','division_code']
    jcno = JCNoWIPFieldInt
subconpayment_data_list_form = SubconPaymentDataList(DBS_JistLabour,action="")

class SubconPaymentListFiller(EditFormFiller):
    __model__ = JistSubconPaymentRunsData
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistLabour.query(JistSubconPaymentRunsData). \
                    filter(JistSubconPaymentRunsData.id==id). \
                    one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
subconpayment_data_list_filler = SubconPaymentListFiller(DBS_JistLabour)

class AddNewSubconPayment_data(AddRecordForm):
    __model__ = JistSubconPaymentRunsData 
    __omit_fields__ = ['__actions__','payment_number','id','total_gross',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
    #division_leader = PointField
subconadd_new_payment_data_form = AddNewSubconPayment_data(DBS_JistLabour,action="")

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class StoreLocationList(TableBase):
    __model__ = JistBuyingStoresLocation 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    #__headers__={
    #            'id':'ID',
    #            }
    __xml_fields__ = ['id','division_code']
spx_location_list = StoreLocationList();

class StoreLocationFiller(TableFiller):
    __model__ = JistBuyingStoresLocation 
    def id(self, obj):
        id = '<a href="/logisticscont/editstores_location/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

stores_location_filler = StoreLocationFiller(DBS_JistBuying)

class StoreLocationList(EditableForm):
    __model__ = JistBuyingStoresLocation 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','emp_number','dateedited','contract',]
    #__dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id']
stores_location_list_form = StoreLocationList(DBS_JistBuying,action="")

class StoreLocationListFiller(EditFormFiller):
    __model__ = JistBuyingStoresLocation
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistBuying.query(JistBuyingStoresLocation). \
                    filter(JistBuyingStoresLocation.id==id).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
stores_location_list_filler = StoreLocationListFiller(DBS_JistBuying)

class AddNewStore(AddRecordForm):
    __model__ = JistBuyingStoresLocation 
    __omit_fields__ = ['__actions__','division_code','id','emp_number',
                       'dateedited','useridedited',
                       'dateadded','useridnew','active'
                       ]
add_new_stores_location_form = AddNewStore(DBS_JistBuying,action="")
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class MarketingListTable(TableBase):
    __model__ = JistMarketingClientLeads 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited','dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID','client_name','point_person']
spx_marketing_client_list = MarketingListTable();

class MarketingListFiller(TableFiller):
    __model__ = JistMarketingClientLeads 
    def id(self, obj):
        id = '<a href="/marketingcont/editclientleadone/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def point_person(self, obj):
        point_person = DBS_ContractData.query(User).filter(User.user_id==obj.point_person).one()
        return point_person.user_name.join(('<div>', '</div>'))

    def client_name(self, obj):
        client_name = '<a href="/marketingcont/view_one_client_lead/'+str(obj.id)+'">'+str(obj.client_name)+'</a>'
        return client_name.join(('<div>', '</div>'))


marketing_client_list_filler = MarketingListFiller(DBS_JistMarketing)

class MarketingClientLead(EditableForm):
    __model__ = JistMarketingClientLeads 
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','dateedited']
    point_person=PointFieldInt
clientlead_list_form = MarketingClientLead(DBS_JistMarketing,action="")

class MarketingClientLeadFiller(EditFormFiller):
    __model__ = JistMarketingClientLeads
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_JistMarketing.query(JistMarketingClientLeads). \
                    filter(JistMarketingClientLeads.id==id). \
                    one()
            return len(p1),p1 
clientlead_list_filler = MarketingClientLeadFiller(DBS_JistMarketing)

"""
class MarketingDriverListTable(TableBase):
    __model__ = JistMarketingDriverList 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_drivers = MarketingDriverListTable();

class MarketingDriversFiller(TableFiller):
    __model__ = JistMarketingDriverList 
    def id(self, obj):
        id = '<a href="/transportcont/edit_driver/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def status(self, obj):
        for d in obj.status:
            #status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
        return status.user_name.join(('<div>', '</div>'))
fleet_drivers_filler = MarketingDriversFiller(DBS_ContractData)

class MarketingMaintenanceListTable(TableBase):
    __model__ = JistMarketingMaintenanceList 
    __omit_fields__ = ['__actions__',
                       'dateedited','useridedited',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_maintenance = MarketingMaintenanceListTable();

class MarketingmaintenanceFiller(TableFiller):
    __model__ = JistMarketingMaintenanceList 
    def id(self, obj):
        id = '<a href="/transportcont/edit_maintenance/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def status(self, obj):
        for d in obj.status:
            #status = d.pointperson
            status = DBS_ContractData.query(User).filter(User.user_id==d.pointperson).one()
        return status.user_name.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,fleetid=0, **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            wip1 = DBS_ContractData.query(JistMarketingMaintenanceList). \
                    filter(JistMarketingMaintenanceList.fleetid==fleetid). \
                    all()
            return len(wip1),wip1 
fleet_maintenance_filler = MarketingmaintenanceFiller(DBS_ContractData)

class MarketingFuelUsage(TableBase):
    __model__ = JistMarketingFuelUsage 
    __omit_fields__ = ['__actions__',
                       'vin_number','engine_number',
                       'n_r_number','tare','fuel_type',
                       'service_center','service_center_tel_no',
                       'dateadded','useridnew',
                       ]
    __headers__={
                'id':'ID',
                }
    __xml_fields__ = ['ID']
spx_fleet_fuel_usage = MarketingFuelUsage();

class MarketingFuelUsageFiller(TableFiller):
    __model__ = JistMarketingFuelUsage 
    def id(self, obj):
        id = '<a href="/transportcont/edit_fleet/'+str(obj.id)+'">'+str(obj.id)+'</a>'
        return id.join(('<div>', '</div>'))

    def _do_get_provider_count_and_objs(self,status='False', **kw):
            userid = request.identity['repoze.who.userid']
            user = User.by_user_name(userid)
            #print user.user_id
            #for m in kw:
            #    print m
            wip1 = DBS_ContractData.query(JistMarketingFuelUsage). \
                    filter(JistMarketingFuelUsage.id==int(1)). \
                    all()
            return len(wip1),wip1 
fleet_fuel_usage_filler = MarketingFuelUsageFiller(DBS_ContractData)

"""
class AddNewMarketingClient(AddRecordForm):
    __model__ = JistMarketingClientLeads 
    __omit_fields__ = ['id','active','dateedited','useridedited', 
                        'useridnew',
                        'dateadded']
    point_person = PointField
add_new_mar_client_form = AddNewMarketingClient(DBS_JistMarketing,action="savenewfleet")

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class PointChangerBasic(EditableForm):
    __model__ = JistContractStatus 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__ = ['useridnew','useridedited','contract_status',
                        'dateadded','dateedited','contract',
                        'sitehandoverdate','siteperson','code']
    __dropdown_field_names__ = {'point':'pointperson','code':'status'}
    __hide_fields__ = ['id','siteagent','actualstartdate','firstdeldate',
                       'finalcompldate','jno','statuscode']
    pointperson = PointFieldManage
status_point_changer = PointChangerBasic(DBS_ContractData,action="")

class SiteAgentChangerBasic(EditableForm):
    __model__ = JistContractStatus 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__ = ['useridnew','useridedited','contract_status',
                        'dateadded','dateedited','contract',
                        'sitehandoverdate','pointperson','code','jno','statuscode']
    #__dropdown_field_names__ = {'siteperson':'siteperson','code':'status'}
    __hide_fields__ = ['id','pointperson','actualstartdate','firstdeldate',
                       'finalcompldate']
    siteagent = PointField
status_siteagent_changer = SiteAgentChangerBasic(DBS_ContractData,action="")

class ContractStatusChanger(EditableForm):
    __model__ = JistContractStatus 
    __hide_fields__ = ['id']
    __omit_fields__ = ['id','siteagent','actualstartdate','useridnew',
                        'useridnew','finalcompldate','firstdeldate',
                        'useridedited',
                        'dateadded','dateedited','contract',
                        'sitehandoverdate','pointperson','jno']
    statuscode = StatusField 

contract_status_chooser = ContractStatusChanger(DBS_ContractData,action="")

class LabourDivisionBox(EditableForm):
    __model__ = JistLabourDivisions 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','dateedited','contract',
                        'division_leader','division_code','active']
    __hide_fields__ = ['id','siteagent','actualstartdate','firstdeldate',
                       'finalcompldate']
    division_name = LabourDivisionField 
labour_division_box = LabourDivisionBox(DBS_JistLabour,action="")

class SubconDivisionBox(EditableForm):
    __model__ = JistSubconDivisions 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','dateedited','contract',
                        'division_leader','division_code','active']
    __hide_fields__ = ['id','siteagent','actualstartdate','firstdeldate',
                       'finalcompldate']
    division_name = SubconDivisionField 
subcon_division_box = SubconDivisionBox(DBS_JistLabour,action="")

class SubconListBox(EditableForm):
    __model__ = JistSubconList 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__= ['id','first_name','last_name','date_started',
                        'id_number','rate_per_day','tel_number_home',
                        'bank','account_number','next_of_kin_name',
                        'vat_number','branch_code','address1','address2','next_of_kin_tel',
                        'division','useridnew','useridedited',
                        'dateadded','dateedited',
                        'active']
    __hide_fields__ = ['id','siteagent','actualstartdate','firstdeldate',
                       'finalcompldate']
    trading_name = SubconTradingNameField 
subcon_list_box = SubconListBox(DBS_JistLabour,action="")

class SubconJCNoListBox(EditableForm):
    __model__ = JistSubconPaymentRunsData 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__= ['id','first_name','last_name','date_started',
                        'div_id','paylist_id','unit','item',
                        'description','qty','price','total_excl',
                        'useridnew','useridedited','dateadded','dateedited',
                        'active']
    __hide_fields__ = ['id','siteagent','actualstartdate','firstdeldate',
                       'finalcompldate']
    trading_name = SubconTradingNameField 
    jcno = JCNoWIPFieldInt 
    sub_id = SubconTradingNameField 
subcon_jcno_list_box = SubconJCNoListBox(DBS_JistLabour,action="")

class JCNoListBox(EditableForm):
    __model__ = JistSubconPaymentRunsData 
    __headers__= {'sitehandoverdate':'Site Handover Date'}
    __omit_fields__= ['id','first_name','last_name','date_started',
                        'div_id','paylist_id','unit','item',
                        'description','qty','price','total_excl',
                        'useridnew','useridedited','dateadded','dateedited',
                        'active','trading_name','sub_id']
    __hide_fields__ = ['id','siteagent','actualstartdate','firstdeldate',
                       'finalcompldate']
    jcno = JCNoWIPFieldInt 
    sub_id = SubconTradingNameField 
jcno_list_box = JCNoListBox(DBS_JistLabour,action="")

class StatusChangeContract(EditableForm):
    __model__ = JistContractStatus 
    #__headers__= {'sitehandoverdate':'Site Handover Date',
    #                }
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','dateedited','contract',]
    __field_order__ = ['id','pointperson','siteagent','contract_status',
                        'site_handover_date']
    __dropdown_field_names__ = {'contract_status':'status'}
    __hide_fields__ = ['id','jno']
    pointperson = PointField
    siteagent = PointField
    #code = StatusField
    statuscode = StatusField
    site_handover_date = MyCalendarDatePicker
    actualstartdate = MyCalendarDatePicker
    firstdeldate = MyCalendarDatePicker
    finalcompldate = MyCalendarDatePicker
status_contract_form = StatusChangeContract(DBS_ContractData,action="savestatus")

class PlanDateChangeContract(EditableForm):
    __model__ = JistContractPlanningDates 
    __omit_fields__ = ['useridnew','useridedited',
                        'dateadded','dateedited','contract',]
    #__field_order__ = ['id','point','siteperson','code',
    #                    'Site Handover Date']
    #__dropdown_field_names__ = {'point':'user_name','code':'status'}
    __hide_fields__ = ['id','jcno']
    #pointperson = PointField
    #siteagent = PointField
    planstartdate = MyCalendarDatePicker
    planenddate = MyCalendarDatePicker
    #firstdeldate = MyCalendarDatePicker
    #finalcompldate = MyCalendarDatePicker
    __headers__= {'planstartdate':'Site Handover Date'}
plandates_contract_form = PlanDateChangeContract(DBS_ContractData)

class StatusChangerFiller(EditFormFiller):
    __model__ = JistContractStatus
    def _do_get_provider_count_and_objs(self,jno=None):
            p1 = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==jno).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
status_changer_filler = StatusChangerFiller(DBS_ContractData)

class EditSupplier(EditableForm):
    __model__ = JistBuyingSupplierList 
    __hide_fields__ = ['id','datecreated',]
    suppliername = TextField('suppliername',validator=validators.NotEmpty())
    accnumber = TextField
    address = TextField
    city = TextField
    fax = TextField
    phone = TextField
    contact = TextField
    active = CheckBox
edit_supplier_form = EditSupplier(DBS_JistBuying)

class EditSupplierFiller(EditFormFiller):
    __model__ = JistBuyingSupplierList
    def _do_get_provider_count_and_objs(self,jno=None):
            p1 = DBS_JistBuying.query(JistBuyingSupplierList).filter(JistBuyingSupplierList.id==jno).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
edit_supplier_filler = EditSupplierFiller(DBS_JistBuying)

class EditAddGRVForm(TableForm):
    __hide_fields__ = ['id','grvid','buyingitemid','active','datecreated','useridnew']
    storenames = []
    stonames = DBS_JistBuying.query(JistBuyingStoresLocation).filter(JistBuyingStoresLocation.active==True).all()
    for m in stonames:
        storenames.append(m.store_name) 

    fields = [
            MyCalendarDatePicker('Delivery_Date',
                    validator=validators.NotEmpty()),
            TextField('grvdelnum',label_text='Delivery Note or Invoice Number'),
            TextField('grvqty',label_text='Quantity_Delivered'),
            SingleSelectField('In_Store',
                        options=storenames)
            ]
    submit_text = 'Add Delivery'
edit_grv_form = EditAddGRVForm('edit_grv_form')

class EditAddGRVFiller(EditFormFiller):
    __model__ = JistBuyingGRV
    def _do_get_provider_count_and_objs(self,jno=None):
            p1 = DBS_JistBuying.query(JistBuyingGRV).filter(JistBuyingGRV.id==jno).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
edit_grv_filler = EditAddGRVFiller(DBS_JistBuying)

class EditPurchaseOrderItem(EditableForm):
    __model__ = JistBuyingOrderItems 
    __omit_fields__ = ['id','podate','reqid','suppliercode',
                        'ponumber','totalexcl','totalincl',
                        'dateedited','useridedited','totalvat',
                        'active','datecreated','useridnew']
    podate = MyCalendarDatePicker('podate',
                    validator=validators.NotEmpty())
edit_purchase_order = EditPurchaseOrderItem(DBS_JistBuying)

class EditPurchaseOrderFiller(EditFormFiller):
    __model__ = JistBuyingOrderItems
    def _do_get_provider_count_and_objs(self,ponumber=None):
            p1 = DBS_JistBuying.query(JistBuyingOrderItems).filter(JistBuyingOrderItems.ponumber==ponumber).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
edit_purchase_order_filler = EditPurchaseOrderFiller(DBS_JistBuying)

class PlanDatesChangerFiller(EditFormFiller):
    __model__ = JistContractPlanningDates
    def _do_get_provider_count_and_objs(self,jno='500'):
            p1 = DBS_ContractData.query(JistContractPlanningDates). \
                    filter(JistContractPlanningDates.jcno==jno).one()
            #for k,w in p1.iteritems():
            #    print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
plandates_changer_filler = PlanDatesChangerFiller(DBS_ContractData)

class EditTaskStatus(EditableForm):
    __model__ = ProductionTasks 
    __hide_fields__ = ['id','datecreated','request','bearer',
                       'sharer1','sharer2','sharer3',
                       'tied_to_jcno','owner','short_text','jcno','dateedited'
                        ]
    __field_order__ = ['percent_complete','completed']
    jcno = JCNoWIPField
    bearer = PointField
    sharer1 = PointField
    sharer2 = PointField
    sharer3 = PointField
    percent_complete = PercentField
edit_task_status = EditTaskStatus(DBS_ContractData, action="edittaskstatus")

class TaskStatusFiller(EditFormFiller):
    __model__ = ProductionTasks 
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_ContractData.query(ProductionTasks).filter(ProductionTasks.id==id).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
request_changer_filler = TaskStatusFiller(DBS_ContractData)

class EditBearerSharerStatus(EditableForm):
    __model__ = ProductionTasks 
    __hide_fields__ = ['id','datecreated','request','bearer',
                       'sharer1','sharer2','sharer3',
                       'tied_to_jcno','owner','completed','short_text','jcno','dateedited'
                        ]
    __field_order__ = ['percent_complete']
    jcno = JCNoWIPField
    bearer = PointField
    sharer1 = PointField
    sharer2 = PointField
    sharer3 = PointField
    percent_complete = PercentField
edit_bearer_sharer_status = EditBearerSharerStatus(DBS_ContractData, action="edittaskstatus")

class EditFleetOne(EditableForm):
    __model__ = JistFleetList 
    __hide_fields__ = ['dateadded',
                       'useridnew']
edit_fleet_form = EditFleetOne(DBS_ContractData)

class FleetEditFiller(EditFormFiller):
    __model__ = JistFleetList 
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_ContractData.query(JistFleetList).filter(JistFleetList.id==id).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
fleet_edit_filler = FleetEditFiller(DBS_ContractData)

class EditUser(EditableForm):
    __model__ = User 
    __hide_fields__ = ['id',
                        ]
edit_user = EditUser(DBS_ContractData, action="")

class EditFleetFuelOne(EditableForm):
    __model__ = JistFleetFuelUsage 
    __hide_fields__ = ['dateadded',
                       'useridnew']
    #suppliername = TextField('suppliername',validator=validators.NotEmpty())
    #accnumber = TextField
    #address = TextField
    #city = TextField
    #fax = TextField
    #phone = TextField
    #contact = TextField
    fleetid = FleetRegField 
    person = FleetDriverField
edit_fleet_fuel_form = EditFleetFuelOne(DBS_ContractData)

class FleetFuelEditFiller(EditFormFiller):
    __model__ = JistFleetFuelUsage 
    def _do_get_provider_count_and_objs(self,id=None):
            p1 = DBS_ContractData.query(JistFleetFuelUsage).filter(JistFleetFuelUsage.id==id).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
fuel_edit_filler = FleetFuelEditFiller(DBS_ContractData)

class EditFleetdriverOne(EditableForm):
    __model__ = JistFleetDriverList 
    __hide_fields__ = ['dateadded',
                        'dateedited',
                        'useridedited',
                       'useridnew']
    #suppliername = TextField('suppliername',validator=validators.NotEmpty())
    #accnumber = TextField
    #address = TextField
    #city = TextField
    #fax = TextField
    #phone = TextField
    #contact = TextField
    fleetid = FleetRegField 
edit_fleet_driver_form = EditFleetdriverOne(DBS_ContractData)

class FleetdriverEditFiller(EditFormFiller):
    __model__ = JistFleetDriverList 
    def _do_get_provider_count_and_objs(self,id=None):
            p1 =DBS_ContractData.query(JistFleetDriverList).filter(JistFleetDriverList.id==id).one()
            return len(p1),p1 
driver_edit_filler = FleetdriverEditFiller(DBS_ContractData)

class EditFleetmaintenanceOne(EditableForm):
    __model__ = JistFleetMaintenanceList 
    __hide_fields__ = ['dateadded',
                        'dateedited',
                        'useridedited',
                       'useridnew']
    fleetid = FleetRegField 
edit_fleet_maintenance_form = EditFleetmaintenanceOne(DBS_ContractData)

class FleetmaintenanceEditFiller(EditFormFiller):
    __model__ = JistFleetMaintenanceList 
    def _do_get_provider_count_and_objs(self,id=None):
            p1 =DBS_ContractData.query(JistFleetMaintenanceList).filter(JistFleetMaintenanceList.id==id).one()
            #for k,w in p1.iteritems():
            #    #print k,w
            #    #if 'code' in k:
            #    #    print "It was made"
            #    #    print w
            return len(p1),p1 
maintenance_edit_filler = FleetmaintenanceEditFiller(DBS_ContractData)

class EditUser(EditableForm):
    __model__ = User 
    __hide_fields__ = ['id',
                        ]
edit_user = EditUser(DBS_ContractData, action="")


#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

#class EstContractsTable(TableBase):
#    __model__ = JistEstimating2yrQuotes
#    __omit_fields__ = ['__actions__',
#                        'useridnew','useridedited',
#                        'dateadded','timeedited',
#                        '','dateedited']
#    __column_widths__={'JCNo':"30em",
#                        'Description':"170em",
#                        'Client':"100em"
#                      }
#    __headers__={
#                }
#    __field_order__ = ['id','date']

#    __xml_fields__ = ['id','jcno','idsite']
#spx_est_contracts_table = EstContractsTable(DBS_JistEstimating);

#class EstimateContractsTableFiller(TableFiller):
#    __model__ = JistEstimating2yrQuotes 
#    def id(self, obj):
#        id = '<a href="/productioncont/get_one/'+str(obj.id)+'">'+str(obj.id)+'</a>'
#        #print jno
#        return id.join(('<div>', '</div>'))

#    def jcno(self, obj):
#        for d in obj.jcno:
#            wip1 = DBS_ContractData.query(JistContracts). \
#                    filter(JistContracts.jno==obj.jcno). \
#                    one()
#        temp = '<a href="/productioncont/get_one/'+str(obj.jcno)+'">'+obj.jcno+'-'+wip1.site+'</a>'
#        return temp.join(('<div>', '</div>'))

#    def idsite(self, obj):
#        for d in obj.idsite:
#            wip1 = DBS_JistEstimating.query(JistEstimating2yrSites). \
#                    filter(JistEstimating2yrSites.id==obj.idsite). \
#                    one()
#        temp = '<a href="//get_one/'+str(obj.idsite)+'">'+obj.idsite+'-'+wip1.name+'</a>'
#        return temp.join(('<div>', '</div>'))

#    def _do_get_provider_count_and_objs(self,status='False', **kw):
#        wip1 = DBS_JistEstimating.query(JistEstimating2yrQuotes). \
#                                           filter(JistEstimating2yrQuotes.jcno<>"None"). \
#                                           filter(JistEstimating2yrQuotes.date>"2011-03-01"). \
#                                           order_by(desc(JistEstimating2yrQuotes.id)).all()
#        #wip1 = DBS_ContractData.query(JistContracts).filter(JistContracts.completed=='False').all()
#        return len(wip1),wip1 
#Est_contracts_filler = EstimateContractsTableFiller(DBS_ContractData)

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class AddFileToContract(AddRecordForm):
    __model__ = FileStoreProduction 
    __omit_fields__ = ['filecontent',
                        'thumbname',
                        'useridcreated',
                        'datecreated']
    __hide_fields__ = ['id','jcno']
    takenby = PointField
    fileunder = PicCategoryField 
    filename = FileField('filename',help_text='Click To Add File',
                         validator =validators.NotEmpty())
add_file_to_contract = AddFileToContract(DBS_JistFileStore, action="savefile")

class AddPicToUser(AddRecordForm):
    __model__ = FileStoreProduction 
    __omit_fields__ = ['filecontent',
                        'thumbname',
                        'useridcreated',
                        'datecreated']
    __hide_fields__ = ['id','jcno','takenby',
                       'datetaken','description','fileunder']
    #takenby = PointField
    #fileunder = PicCategoryField 
    filename = FileField('filename',help_text='Click To Add File',
                         validator =validators.NotEmpty())
add_pic_to_user = AddPicToUser(DBS_JistFileStore)

class AddNewContract(AddRecordForm):
    __model__ = JistContracts 
    __omit_fields__ = ['jno','cidbcategory',
                        'cidbrating','contact',
                        'groupjno','completed','pointperson', 
                        'useridnew','useridedited',
                        'dateadded','dateedited']
    __field_attrs__ = {'orderno':{'rows':'5'}}
    __dropdown_field_names__ = {'contact':'description','jno':'pointperson'}
add_new_contract_form = AddNewContract(DBS_ContractData)

class AddNewSupplier(AddRecordForm):
    __model__ = JistBuyingSupplierList 
    __omit_fields__ = ['id',]
    suppliername = TextField('suppliername',validator=validators.NotEmpty())
    accnumber = TextField
    address = TextField
    city = TextField
    fax = TextField
    phone = TextField
    contact = TextField
add_new_supplier_form = AddNewSupplier(DBS_JistBuying)

class AddNewReceptionMessage(AddRecordForm):
    __model__ = JistReceptionTelephoneMessages 
    __omit_fields__ = ['id','active','useridnew','dateadded',]
    to_user = PointFieldInt
    from_person = TextField
    return_tel = TextField
add_new_reception_message = AddNewReceptionMessage(DBS_ContractData)

class AddNewOutOfOfficeNotice(AddRecordForm):
    __model__ = JistOutOfOfficeNotices 
    __omit_fields__ = ['id','active','useridnew','dateadded',]
    for_user = PointField
    site = JCNoWIPField 
    other_destination = TextField 
    purpose = TextField 
    est_hours_there = HourField
add_new_out_of_office_notice = AddNewOutOfOfficeNotice(DBS_ContractData)

class AddNewPurchaseReq(AddRecordForm):
    __model__ = JistBuyingPurchaseReqsList 
    __omit_fields__ = ['id','dateclosed','active','useridnew','dateadded']
    jcno = JCNoWIPField 
    prefered_supplier = TextField('prefered_supplier',validator=validators.NotEmpty())
    must_have_date = MyCalendarDatePicker('must_have_date',validator=validators.NotEmpty())
add_new_purchase_req = AddNewPurchaseReq(DBS_JistBuying)

class AddNewPurchaseReqItem(AddRecordForm):
    __model__ = JistBuyingPurchaseReqsItems 
    __omit_fields__ = ['id','poid','reqid','price','total','active','useridnew','dateadded']
    item = TextField
    description = TextField('description',attrs={'size':50})
    unit = TextField
    quantity = TextField('quantity',validator=Int)
add_new_purchase_req_item = AddNewPurchaseReqItem(DBS_JistBuying)

class AddNewPurchaseOrder(AddRecordForm):
    __model__ = JistBuyingOrderList 
    __omit_fields__ = ['id','ponumber','totalexcl','totalincl',
                    'totalvat','active','datecreated','useridnew']
    suppliercode = SupplierField
    podate = MyCalendarDatePicker('podate',
                    validator=validators.NotEmpty())
add_new_purchase_order = AddNewPurchaseOrder(DBS_JistBuying)

class AddNewPurchaseItem(AddRecordForm):
    __model__ = JistBuyingOrderItems 
    __omit_fields__ = ['id','podate','ponumber',
                        'contract','active',]
    suppliercode = SupplierField
    unit = TextField('unit',validator=validators.String)
    quantity = TextField('quantity',validator=validators.Int)
    priceexcl = TextField('priceexcl',validator=Int)
    totalexcl = TextField('totalexcl',validator=Int)
add_new_purchase_item = AddNewPurchaseItem(DBS_JistBuying)

class AddNewPurchaseItemGRV(AddRecordForm):
    __model__ = JistBuyingGRV 
    __omit_fields__ = ['id','podate','ponumber',
                        'contract','active',]
    suppliercode = SupplierField
    unit = TextField('unit',validator=validators.String)
    quantity = TextField('quantity',validator=validators.Int)
    priceexcl = TextField('priceexcl',validator=Int)
    totalexcl = TextField('totalexcl',validator=Int)
add_new_purchase_item_grv = AddNewPurchaseItemGRV(DBS_JistBuying)

class AddNewTask(AddRecordForm):
    __model__ = ProductionTasks 
    __omit_fields__ = [ 'datecreated','dateedited']
    __field_order__ = ['request','bearer',
                       'sharer1','sharer2','sharer3',
                       'percent_complete','completed','tied_to_jcno'
                        ]
    __hide_fields__ = ['id','short_text','completed','percent_complete','owner']
    jcno = JCNoWIPField
    bearer = PointField
    sharer1 = PointField
    sharer2 = PointField
    sharer3 = PointField
    percent_complete = PercentField
add_new_task_form = AddNewTask(DBS_ContractData, action="savenewtask")

class AddNewTaskReply(AddRecordForm):
    __model__ = TasksDetails 
    __omit_fields__ = [ 'datecreated']
    __field_order__ = ['request','bearer',
                        ]
    __hide_fields__ = ['id','taskid','useridcreated','dateedited']
add_new_task_reply = AddNewTaskReply(DBS_ContractData, action="savenewtaskreply")

class AddNewSiteDiary(AddRecordForm):
    __model__ = SiteDiaryContracts 
    __omit_fields__ = [ 'datecreated','dateedited']
    __hide_fields__ = ['id','jcno','owner']

    report_date = MyCalendarDatePicker('report_date',
                    validator=validators.NotEmpty())
add_new_sitediary_form = AddNewSiteDiary(DBS_ContractData, action="savenewsitediary")

class AddNewFleet(AddRecordForm):
    __model__ = JistFleetList 
    __omit_fields__ = ['active', 
                        'useridnew',
                        'dateadded']
add_new_fleet_form = AddNewFleet(DBS_ContractData,action="savenewfleet")

class ChooseFleet(AddRecordForm):
    __model__ = JistFleetList 
    __limit_fields__ = ['registration_number',
                        ]
    registration_number = FleetRegField 
choose_fleet_form = ChooseFleet(DBS_ContractData,action="")

class AddNewFleetFuelSlip(AddRecordForm):
    __model__ = JistFleetFuelUsage 
    __omit_fields__ = ['id','fleetid', 
                        'useridnew',
                        'dateadded']

    person = FleetDriverField
add_new_fuelslip_form = AddNewFleetFuelSlip(DBS_ContractData,action="")

class AddNewFleetdriver(AddRecordForm):
    __model__ = JistFleetDriverList 
    __omit_fields__ = ['id','fleetid', 
                        'dateedited',
                        'useridedited',
                        'useridnew',
                        'active',
                        'dateadded']
add_new_driver_form = AddNewFleetdriver(DBS_ContractData,action="")

class AddNewMaintenanceList(AddRecordForm):
    __model__ = JistFleetMaintenanceList 
    __omit_fields__ = ['id','fleetid', 
                        'useridnew',
                        'dateadded']
add_new_maintenance_form = AddNewMaintenanceList(DBS_ContractData,action="")


#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class SproxContractsController(CrudRestController):
    model = JistContracts
    table = spx_contracts_table
    table_filler = contracts_filler

class AddUserForm(ListForm):
    class fields(WidgetsList):
        id = HiddenField(default="I'm hidden!")
        name = TextField(
            validator = UnicodeString(), 
            default = "Your name here"
            )
        gender = RadioButtonList(
            options = "Male Female".split(),
            )
        age = SingleSelectField(
            validator = Int, 
            options = range(100)
            )
        email = TextField(
            validator = Email()
            )
        date = CalendarDateTimePicker()
        roles = CheckBoxList(
            options = "Manager Admin Editor User".split(),
            )
        groups = MultipleSelectField(
            options = "Group1 Group2 Group3".split(),
            )
        password = PasswordField(
            validator = String(), 
            max_size = 10
            )
        password_confirm = PasswordField(
            validator = String(), 
            max_size=10
            )
        # We wrap the address fieldset with a FormFieldRepeater to handle
        # repetitions. This can be done with *any* FormField.
        """
        address = FormFieldRepeater(
            widget = AddressFieldset(), 
            repetitions = 2, 
            max_repetitions = 5
            )
        """

    def update_params(self, d):
        super(AddUserForm, self).update_params(d)
        # Focus and select the 'name' field on the form
        # The adapter we just wrote lets us pass formfields as parameters and
        # the right thing will be done.
        if not d.error:
            self.add_call(focus_element(d.c.name))
        else:
            self.add_call(
                alert('The form contains invalid data\n%s'% unicode(d.error))
                )
userForm = AddUserForm()

class UserRecordView(RecordViewBase):
    __model__ = User
    __omit_fields__ = ['created']
user_view = UserRecordView(DBS_ContractData)

from sprox.fillerbase import RecordFiller
class UserRecordFiller(RecordFiller):
    __model__ = User

class TextField(InputField):
    """A text field"""
    params = ["size", "max_size", "maxlength"]
    size__doc = "The size of the text field."
    maxlength__doc = "The maximum size of the field"
    max_size__doc = ("The maximum size of the field (DEPRECATED: use maxlength "
                     "instead)")
    type = "text"
    def update_params(self,d):
        super(TextField, self).update_params(d)
        if d.max_size is not None:
            d.maxlength = d.max_size
            warn("max_size is deprecated, use maxlength instead",
                 DeprecationWarning, 6)
        self.update_attrs(d, "size", "maxlength")

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
class StatusItems(WidgetsList):
    supplier_name = StatusField() 

class DescriptionSearch(WidgetsList):
    contract_description_search = TextField(validator=validators.NotEmpty())

class POItemSearch(WidgetsList):
    purchase_order_description_search = TextField(validator=validators.NotEmpty())

class SupplierNameSearch(WidgetsList):
    supplier_name = TextField("supp_name",validator=validators.NotEmpty())

class SupplierComboSearch(WidgetsList):
    supplier_name = SupplierField("supplier_name",validator=validators.NotEmpty())
    #startdate = CalendarDatePicker()
    #enddate = CalendarDatePicker()
    startdate = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    enddate = MyCalendarDatePicker('enddate',
                    validator=validators.NotEmpty())

class GRVEnterForm(WidgetsList):
    delivery_date = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    delivery_note_or_invoice_number = TextField(validator=validators.NotEmpty())
    
    qty_delivered = TextField(validator=validators.Int)

    in_store = StoresNameField() 

class InvoiceDateComboSearch(WidgetsList):
    startdate = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    enddate = MyCalendarDatePicker('enddate',
                    validator=validators.NotEmpty())

class InvoiceDateClientComboSearch(WidgetsList):
    client_name = InvoiceClientField("client",validator=validators.NotEmpty())
    startdate = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    enddate = MyCalendarDatePicker('enddate',
                    validator=validators.NotEmpty())

class InvoiceContractSearch(WidgetsList):
    contract_name = JCNoContractInvField("contract_name",validator=validators.NotEmpty())

class InvoicesPaymentTime(WidgetsList):
    startdate = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    enddate = MyCalendarDatePicker('enddate',
                    validator=validators.NotEmpty())

class InvoicesUnpaid(WidgetsList):
    unpaid_invoices = CheckBox(label_text="Unpaid Invoices",default=True)

class InvoicesBalances(WidgetsList):
    balance_on_invoice = CheckBox(label_text="Invoices with Balances",default=True)

class EstimateJCNoSearch(WidgetsList):
    all = CheckBox(label_text="All JCNo",default=True)

class EstimateColor(WidgetsList):
    all = RadioButton(label_text="All JCNo",default=True)
    sall = RadioButton(label_text="SAll JCNo",default=False)
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']
    cols = 2 
    value = ['Red','Green','Blue']
    soall = CBoxT(options=options,cols=cols,value=value)

class EstimateCololr(CBoxT):
    options = ['Red', 'Orange', 'Yellow', 'Green', 'Blue']
    cols = 2 
    value = ['Red','Green','Blue']
    all = CBoxT(options=options,cols=cols,value=value)

class SiteNameSearch(WidgetsList):
    site_name = TextField("site_name",validator=validators.NotEmpty())

class ReceptionTelephoneMessage(WidgetsList):
    #to_user = PointFieldManage(validator=validators.NotEmpty())
    #to_user = PointField(validator=validators.NotEmpty())
    from_person = TextField("from_person",validator=validators.NotEmpty()) 
    call_back = CheckBox(label_text="Call Back Please",default=False)
    #notify = CheckBox(label="Notify me")
    call_again = CheckBox(label_text="Will Call Again ",default=True)
    no_message = CheckBox(label_text="No Message Left ")
    message = TextField(validator=validators.NotEmpty())
    return_tel = TextField("return_tel",validator=validators.NotEmpty())

class ReceptionTelephoneDateMessage(WidgetsList):
    #dateadded = MyCalendarDatePicker()
    dateadded = MyCalendarDatePicker('dateadded',
                    validator=validators.NotEmpty())
class OutOfOfficeDateMovments(WidgetsList):
    #dateadded = MyCalendarDatePicker()
    dateadded = MyCalendarDatePicker('dateadded',
                    validator=validators.NotEmpty())

class AddNewPurchaseReqItem(WidgetsList):
    item = TextField() 
    description = TextField()
    unit = TextField()
    quantity = TextField()
    price = TextField()
    total = TextField()
    
class AddNewPurchaseOrderItem(WidgetsList):
    reqid = TextField()
    reqitemid = TextField()
    item = TextField() 
    description = TextField()
    unit = TextField()
    quantity = TextField()
    price = TextField()
    total = TextField()

class AddNewPurchaseGRV(WidgetsList):
    item = TextField() 
    description = TextField()
    unit = TextField()
    quantity = TextField()
    price = TextField()
    total = TextField()

class SearchFleetFuel(WidgetsList):
    #dateadded = MyCalendarDatePicker
    startdate = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    enddate = MyCalendarDatePicker('enddate',
                    validator=validators.NotEmpty())

class SearchPurchaseOrderDate(WidgetsList):
    #startdate = CalendarDatePicker()
    #enddate = CalendarDatePicker()
    startdate = MyCalendarDatePicker('startdate',
                    validator=validators.NotEmpty())
    enddate = MyCalendarDatePicker('enddate',
                    validator=validators.NotEmpty())

class CommentFields(WidgetsList):
    site_search = TextField('site_search',validator=validators.NotEmpty())
    #email = TextField(validator=validators.Email(not_empty=True),
    #                attrs={'size':30})
    #comment = TextArea(validator=validators.NotEmpty())
    #notify = CheckBox(label="Notify me")

class TrolleyOptions(WidgetsList):
    clear_trolley = CheckBox(label_text="Clear Trolley",default=True)

#************************************************************************************************
#************************************************************************************************
#************************************************************************************************
#************************************************************************************************

class MyAjaxForm(AjaxForm):
    id="myAjaxContractSearch"
    fields=CommentFields()
    target="output"
    action="/productioncont/do_search"
site_ajax_form = MyAjaxForm()

class BuyingItemSelector(ItemSelector):
    def __init__(self,from_data,to_data):
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
#order_item_selector = BuyingItemSelector()

"""
import tw.forms as twf
movie_form = twf.TableForm('movie_form', action='save_movie', children=[
    twf.HiddenField('id'),
    twf.TextField('title'),
    twf.TextField('year', size=4),
    twf.CalendarDatePicker('release_date'),
    twf.SingleSelectField('genera', options=['', 'Action', 'Comedy', 'Other']),
    twf.TextArea('description'),
])
"""

