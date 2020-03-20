# -*- coding: utf-8 -*-

from sqlalchemy import *
from sqlalchemy.orm import mapper, relation,  backref
from sqlalchemy import Table, ForeignKey, Column
from sqlalchemy.types import Integer, Unicode, BLOB,Numeric, Float
from sqlalchemy.dialects  import mysql
from sqlalchemy.dialects.mysql  import ENUM, FLOAT , NUMERIC, DECIMAL
#from sqlalchemy.dialects.mysql import LONGBLOB
#from sqlalchemy.types import LargeBinary
#from sqlalchemy.orm import relation, backref
from datetime import *
#from geoalchemy import *

from jistdocstore.model.auth import User, Group, Permission ,user_group_table
from jistdocstore.model import DeclarativeBase3,metadata3,DBS_JistFleetTransport
from jistdocstore.model import DeclarativeBase4,metadata4,DBS_JistFileStore,DBS_ContractData, DeclarativeBase2
from jistdocstore.model import DeclarativeBase5,metadata5,DBS_JistBuying
from jistdocstore.model import DeclarativeBase8,metadata8,DBS_JistLabour
from jistdocstore.model import DeclarativeBase7,metadata7,DBS_JistInvoicing
from jistdocstore.model import DeclarativeBase6,metadata6,DBS_JistManufacturing
from jistdocstore.model import DeclarativeBase9,metadata9,DBS_JistMarketing
from jistdocstore.model import DeclarativeBase10,metadata10,DBS_Jist3yrBuilding
from jistdocstore.model import DeclarativeBase11,metadata11,DBS_Jist5yrEskomFencing
from jistdocstore.model import DeclarativeBase12,metadata12,DBS_Jist3yrEssPalisade
from jistdocstore.model import DeclarativeBase13,metadata13,DBS_Jist3yrEssHSF

class PictureSharing(DeclarativeBase4):
    __tablename__ = 'tblsharedpics'
    pic_id = Column(Integer, primary_key=True,nullable=False)
    user_id = Column(Integer, primary_key=True,nullable=False)
    sharer_id = Column(Integer)


class PictureCategory(DeclarativeBase4):
    __tablename__ = 'tblpicturecategory'
    id = Column(Integer, primary_key=True,autoincrement=True)
    categoryname = Column(Unicode(32),unique=True, nullable=False)

class FileStoreProduction(DeclarativeBase4):
    __tablename__ = 'tblfilestoreproduction'
    pic_id = Column(Integer, primary_key=True)
    filesubject = Column(Unicode(255), nullable=False)
    filename = Column(Unicode(255), nullable=False)
    jcno = Column(Integer, nullable=True)
    takenby = Column(Integer, nullable=False)
    datetaken = Column(Date,nullable=False)
    description = Column(Text, nullable=True)
    thumbname = Column(Text, nullable=True)
    #filecontent = Column(LONGBLOB)
    datecreated = Column(DateTime, default=datetime.date(datetime.now()))
    useridnew = Column(Integer)
    #sharedusers = relation(User, secondary=shared_pictures_table, backref='usersharetable')
    
class ProductionTasks(DeclarativeBase2):
    __tablename__='tbltasks'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcno = Column(Integer,ForeignKey('tblcontractdata.jno'), nullable=True)
    short_text = Column(Text)
    request = Column(Text, nullable=False)
    owner = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    bearer = Column(Integer, nullable=False)
    sharer1 = Column(Integer, nullable=True)
    sharer2 = Column(Integer, nullable=True)
    sharer3 = Column(Integer, nullable=True)
    percent_complete = Column(Integer,nullable=False,default=0)
    completed = Column(Boolean, default=False, nullable=False)
    tied_to_jcno = Column(Boolean, default=False)
    datecreated = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class TasksDetails(DeclarativeBase2):
    __tablename__='tbltasksdetails'
    id = Column(Integer, autoincrement=True, primary_key=True)
    taskid = Column(Integer,ForeignKey('tbltasks.id'), nullable=False)
    story = Column(Text, nullable=False)
    datecreated = Column(DateTime, default=datetime.now)
    useridcreated = Column(Integer)

class SiteDiaryContracts(DeclarativeBase2):
    __tablename__='tblsitediarycontracts'
    id = Column(Integer, autoincrement=True, primary_key=True)
    report_date = Column(Date, nullable=False)
    jcno = Column(Integer,ForeignKey('tblcontractdata.jno'), nullable=False)
    entry = Column(Text)
    owner = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    datecreated = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistContractOrderItems(DeclarativeBase2):
    __tablename__='tblcontractorderitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jno = Column(Integer,ForeignKey('tblcontractdata.jno'), primary_key=True)
    item = Column(Text)
    description = Column(Text)
    unit = Column(Text)
    qty = Column(Numeric(10,2),default=0.00)
    price = Column(Numeric(10,2),default=0.00)
    total = Column(Numeric(10,2),default=0.00)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistContractBudget(DeclarativeBase2):
    __tablename__='tblcontractbudget'
    id = Column(Integer, autoincrement=True, primary_key=True)
    budget_jno = Column(Integer,ForeignKey('tblcontractdata.jno'), primary_key=True)
    budget_item = Column(Text)
    budget_description = Column(Text)
    budget_unit = Column(Text)
    budget_qty = Column(Numeric, default=0.00)
    price_rate = Column(Numeric, default=0.00)
    price_total = Column(Numeric, default=0.00)
    rate_material_percent = Column(Numeric, default=0.00)
    rate_material = Column(Numeric, default=0.00)
    rate_markup_percent = Column(Numeric, default=0.00)
    rate_markup = Column(Numeric, default=0.00)
    rate_labour_percent = Column(Numeric, default=0.00)
    rate_labour = Column(Numeric, default=0.00)
    rate_transport_percent = Column(Numeric, default=0.00)
    rate_transport = Column(Numeric, default=0.00)
    rate_healthsafety_percent = Column(Numeric, default=0.00)
    rate_healthsafety = Column(Numeric, default=0.00)
    rate_overheads_percent = Column(Numeric, default=0.00)
    rate_overheads = Column(Numeric, default=0.00)
    rate_specialist_percent = Column(Numeric, default=0.00)
    rate_specialist = Column(Numeric, default=0.00)
    rate_markup_specialist_percent = Column(Numeric, default=0.00)
    rate_markup_specialist = Column(Numeric, default=0.00)
    rate_other_percent = Column(Numeric, default=0.00)
    rate_other = Column(Numeric, default=0.00)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistContracts(DeclarativeBase2):
    __tablename__='tblcontractdata'
    jno = Column(Integer, autoincrement=True, primary_key=True)
    orderno = Column(Text)
    orderdate = Column(Date)
    client = Column(Text)
    description = Column(Text)
    site = Column(Text)
    contact = Column(Text)
    tel = Column(Text)
    fax = Column(Text)
    cell = Column(Text)
    workcategory = Column(Text)
    cidbcategory = Column(Text)
    cidbrating = Column(Integer)
    groupjno = Column(Text)
    completed = Column(ENUM('False','True'),default='False',nullable=False)
    pointperson = Column(Text)
    locationid = Column(Integer)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)
    def __repr__(self):
        return "<JISTContracts('%s','%s', '%s')>" % (self.jno, self.client, self.site)

class JistContractContractual(DeclarativeBase2):
    __tablename__='tblcontractcontractual'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jno = Column(Integer)
    contractlaw = Column(Text)
    contractstartdate = Column(Date)
    contractperiod = Column(Text)
    contractenddate = Column(Date)
    guaranteetype = Column(Text)
    insurancelimit = Column(Text)
    retentionpercent = Column(Text)
    liabilityperiod = Column(Text)
    sitehandoverdate = Column(Date)
    actualstartdate = Column(Date)
    practicalcompldate = Column(Date)
    finalcompldate = Column(Date)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistContractStatusCodes(DeclarativeBase2):
    __tablename__='tblcontractstatuscodes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    status = Column(Text)

class JistContractStatus(DeclarativeBase2):
    __tablename__='tblcontractstatusdata'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jno = Column(Integer,ForeignKey('tblcontractdata.jno'), primary_key=True)
    statuscode = Column(Text)
    pointperson = Column(Text)
    siteagent = Column(Text)
    sitehandoverdate = Column(Date)
    actualstartdate = Column(Date)
    firstdeldate = Column(Date)
    finalcompldate = Column(Date)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistContractScope(DeclarativeBase2):
    __tablename__='tblcontractscope'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jno = Column(Integer,ForeignKey('tblcontractdata.jno'), primary_key=True)
    quoteno = Column(Text)
    item = Column(Text)
    description = Column(Text)
    unit = Column(Text)
    qty = Column(Numeric)
    price = Column(Numeric)
    total = Column(Numeric)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistContractPlanningDates(DeclarativeBase2):
    __tablename__='tblcontractplanningdates'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcno = Column(Integer,ForeignKey('tblcontractdata.jno'),
            nullable=False,primary_key=True)
    planstartdate = Column(Date)
    planenddate = Column(Date)
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistLocationList(DeclarativeBase2):
    __tablename__='tbljistlocationlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    lat = Column(Unicode(220))
    lng = Column(Unicode(220))
    description = Column(Unicode(255))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)


class JistContractPlanningResource(object):
    __tablename__='tblcontractplanningresources'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcno = Column(Integer,ForeignKey('tblcontractdata.jno'), nullable=False)
    planstartdate = Column(Date)
    planenddate = Column(Date)
    idformen = Column(Text)
    idsiteagent= Column(Text)        
    iddomesticsub= Column(Text)       
    idlaboursub= Column(Text)          
    idnominatedsub = Column(Text)       
    idselectedsub = Column(Text)         
    idsuppliersub = Column(Text) 
    useridnew = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    useridedited = Column(Integer,ForeignKey('tg_user.user_id'), nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistBuyingOrderList(DeclarativeBase5):
    __tablename__='tblpoorderlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    ponumber = Column(Unicode(20))
    podate = Column(Date())
    suppliercode = Column(Unicode(20))
    totalexcl = Column(Numeric(10,2), default=0.00)
    totalvat = Column(Numeric(10,2), default=0.00)
    totalincl = Column(Numeric(10,2), default=0.00)
    active = Column(ENUM('Y','N'),default='Y',nullable=False)
    datecreated = Column(DateTime, default=datetime.now)
    useridnew = Column(Integer,nullable=False)

class JistBuyingRentalsLink(DeclarativeBase5):
    __tablename__='tblbuying_rentals_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    supplier_id = Column(Integer,unique=True, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistBuyingPORentalTable(DeclarativeBase5):
    __tablename__='tblbuying_po_tracking'
    id = Column(Integer, autoincrement=True, primary_key=True)
    orderitem_id = Column(Integer,unique=True, nullable=False)
    delnote_no = Column(Unicode(20))
    daysrequired = Column(Integer)
    rental_start_date = Column(Date)
    contact_person = Column(Unicode(20))
    collected_by = Column(Unicode(20))
    comments = Column(Text)
    bookoff_no = Column(Unicode(30))
    dropped_by = Column(Unicode(20))
    rental_end_date = Column(Date)
    user_active = Column(Integer, nullable=False)
    buying_active = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)
    useridnew = Column(Integer,nullable=False)
    useridedited = Column(Integer,nullable=False)


class JistBuyingMaintenanceLink(DeclarativeBase5):
    __tablename__='tblbuying_maintenance_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    supplier_id = Column(Integer,unique=True, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)


class JistBuyingOrderItems(DeclarativeBase5):
    __tablename__='tblbuyingrecords'
    id = Column(Integer, autoincrement=True, primary_key=True)
    ponumber = Column(Unicode(20))
    podate = Column(Date())
    reqid = Column(Integer,ForeignKey('tblbuyingpurchasereqslist.id'), nullable=False)
    contract = Column(Unicode(20))
    suppliercode = Column(Integer,ForeignKey('tblbuyingsuppliers.id'), nullable=False)
    description = Column(Unicode(255))
    unit = Column(Unicode(25))
    quantity = Column(Numeric(10,3), default=0.000)
    priceexcl = Column(Numeric(10,2), default=0.00)
    totalexcl = Column(Numeric(10,2), default=0.00)
    datecreated = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)
    useridnew = Column(Integer,nullable=False)
    useridedited = Column(Integer,nullable=False)

class JistBuyingSupplierList(DeclarativeBase5):
    __tablename__='tblbuyingsuppliers'
    id = Column(Integer, autoincrement=True, primary_key=True)
    suppliername = Column(Unicode(255))
    accnumber = Column(Unicode(20))
    address = Column(Unicode(100))
    city = Column(Unicode(100))
    fax = Column(Unicode(100))
    phone = Column(Unicode(100))
    contact = Column(Unicode(100))
    active = Column(Boolean, default=True)

class JistBuyingGRV(DeclarativeBase5):
    __tablename__='tblbuyinggrv'
    grvid = Column(Integer, autoincrement=True, primary_key=True)
    buyingitemid = Column(Integer,ForeignKey('tblbuyingrecords.id'))
    grvdate = Column(Date)
    grvdelnum = Column(Unicode(100))
    grvqty = Column(Numeric(10,3), default=0.000)
    active = Column(Boolean, default=True)
    in_store = Column(Integer,ForeignKey('tblbuyingstoreslocation.id'))
    datecreated = Column(DateTime, default=datetime.now)
    useridnew = Column(Integer,nullable=False)

class JistBuyingPurchaseReqsList(DeclarativeBase5):
    __tablename__='tblbuyingpurchasereqslist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcno = Column(Integer,nullable=False,primary_key=True)
    prefered_supplier = Column(Unicode(255))
    must_have_date = Column(Date)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer,nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateclosed = Column(DateTime, default=datetime.now)

class JistBuyingPurchaseReqsItems(DeclarativeBase5):
    __tablename__='tblbuyingpurchasereqsitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcno = Column(Integer,nullable=False,primary_key=True)
    reqid = Column(Integer,primary_key=True)
    poid = Column(Integer)
    poitemid = Column(Integer)
    budgetid = Column(Integer)
    item = Column(Unicode(255))
    description = Column(Unicode(255))
    unit = Column(Unicode(255))
    quantity = Column(Numeric(10,3), default=0.000)
    price = Column(Numeric(10,2), default=0.00)
    total = Column(Numeric(10,2), default=0.00)
    buyingactive = Column(Boolean, default=True)
    useractive = Column(Boolean, default=True)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistBuyingPurchaseReqsNotes(DeclarativeBase5):
    __tablename__='tblbuyingpurchasereqsnotes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    reqid = Column(Integer,primary_key=True)
    reqitemid = Column(Integer, primary_key=True)
    note = Column(Text)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistBuyingPurchaseReqsItemsShoppingList(DeclarativeBase5):
    __tablename__='tblbuyingpurchasereqsitemsshoppinglist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    reqitemid = Column(Integer,primary_key=True)
    suppliername = Column(Unicode(255))
    description = Column(Unicode(255))
    unit = Column(Unicode(80))
    quantity = Column(Numeric(10,3), default=0.000)
    price = Column(Numeric(10,2), default=0.00)
    total = Column(Numeric(10,2), default=0.00)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer,nullable=False)
    dateedited = Column(DateTime, default=datetime.now)

class JistBuyingPurchaseReqsItemsShoppingPrices(DeclarativeBase5):
    __tablename__='tblbuyingpurchasereqsitemsshoppingprices'
    id = Column(Integer, autoincrement=True, primary_key=True)
    reqitemid = Column(Integer,primary_key=True)
    shoppinglistid = Column(Integer)
    suppliername = Column(Unicode(255))
    description = Column(Unicode(255))
    quotefilename = Column(Unicode(255))
    unit = Column(Unicode(80))
    quantity = Column(Numeric(10,3), default=0.000)
    price = Column(Numeric(10,2), default=0.00)
    total = Column(Numeric(10,2), default=0.00)
    approved = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer,nullable=False)
    dateedited = Column(DateTime, default=datetime.now)

class JistBuyingStoresLocation(DeclarativeBase5):
    __tablename__='tblbuyingstoreslocation'
    id = Column(Integer, autoincrement=True, primary_key=True)
    store_name = Column(Unicode(55))
    store_location = Column(Unicode(55))
    store_address_1 = Column(Unicode(55))
    store_address_2 = Column(Unicode(55))
    store_address_3 = Column(Unicode(55))
    store_person_name = Column(Unicode(55))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer,nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistReceptionTelephoneMessages(DeclarativeBase2):
    __tablename__='tblreceptiontelmessages'
    id = Column(Integer, autoincrement=True, primary_key=True)
    to_user = Column(Integer,primary_key=True)
    from_person = Column(Unicode(255))
    call_back = Column(Boolean, default=False)
    call_again = Column(Boolean, default=False)
    no_message = Column(Boolean, default=False)
    message = Column(Text)
    return_tel = Column(Unicode(255))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistOutOfOfficeNotices(DeclarativeBase2):
    __tablename__='tbloutofofficenotices'
    id = Column(Integer, autoincrement=True, primary_key=True)
    for_user = Column(Integer,primary_key=True)
    site = Column(Text)
    other_destination = Column(Text)
    purpose = Column(Text)
    est_hours_there = Column(Unicode(255))
    time_start = Column(Time)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistFleetList(DeclarativeBase3):
    __tablename__='tblfleetlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    vehicle_description = Column(Unicode(80))
    registration_number = Column(Unicode(80))
    year_model = Column(Unicode(80))
    date_acquired = Column(Date)
    vin_number = Column(Unicode(80))
    engine_number = Column(Unicode(80))
    n_r_number = Column(Unicode(80))
    tare = Column(Unicode(80))
    fuel_type = Column(Unicode(80))
    tank_capacity = Column(Unicode(80))
    fuel_card_number = Column(Unicode(80))
    fuel_card_expiry_date = Column(Date)
    ext_colour = Column(Unicode(80))
    service_center = Column(Unicode(80))
    service_center_tel_no = Column(Unicode(80))
    driver = Column(Unicode(80))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistFleetFuelUsage(DeclarativeBase3):
    __tablename__='tblfleetfuelusage'
    id = Column(Integer, autoincrement=True, primary_key=True)
    fleetid = Column(Integer)
    transaction_date = Column(Date)
    place = Column(Unicode(80))
    odometer = Column(Unicode(40))
    fuel_qty = Column(Unicode(40))
    fuel_type = Column(Unicode(40))
    amount = Column(Numeric)
    description = Column(Unicode(80))
    person = Column(Unicode(80))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistFleetMaintenanceList(DeclarativeBase3):
    __tablename__='tblfleetmaintenancelist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    fleetid = Column(Integer)
    reqid = Column(Integer)
    transaction_date = Column(Date)
    supplier = Column(Unicode(80))
    odometer = Column(Unicode(40))
    work_description = Column(Unicode(255))
    next_service = Column(Unicode(40))
    amount = Column(Unicode(40))
    person = Column(Unicode(80))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistFleetMaintenanceItems(DeclarativeBase3):
    __tablename__='tblfleetmaintenanceitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    maintenancelist_id = Column(Integer)
    fleetid = Column(Integer)
    unit = Column(Unicode(80))
    qty = Column(Unicode(80))
    price = Column(Unicode(80))
    total = Column(Unicode(80))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistFleetDriverList(DeclarativeBase3):
    __tablename__='tblfleetdriverlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    driver_name = Column(Unicode(40))
    id_number = Column(Unicode(40))
    licence_code = Column(Unicode(80))
    licence_exp_date = Column(Date)
    pdp_code = Column(Unicode(80))
    pdp_exp_date = Column(Date)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistTransportList(DeclarativeBase3):
    __tablename__='tbltransportlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcno = Column(Integer)
    date_required = Column(Date)
    from_place = Column(Unicode(80))
    from_area = Column(Unicode(80))
    from_address= Column(Unicode(180))
    from_contact= Column(Unicode(80))
    to_place = Column(Unicode(80))
    to_area = Column(Unicode(80))
    to_address= Column(Unicode(180))
    to_contact= Column(Unicode(80))
    special_inst= Column(Unicode(200))
    request_person = Column(Integer, nullable=False)

    user_active = Column(Boolean, default=True)
    scheduled = Column(Boolean, default=False)
    date_scheduled = Column(Date)
    completed = Column(Boolean, default=False)
    date_completed = Column(Date)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistTransportLoadingBill(DeclarativeBase3):
    __tablename__='tbltransport_loading_bills'
    id = Column(Integer, autoincrement=True, primary_key=True)
    req_id = Column(Integer,ForeignKey('tbltransportlist.id'))
    item = Column(Unicode(80))
    description = Column(Unicode(200))
    unit = Column(Unicode(80))
    qty = Column(Unicode(80))
    active = Column(Boolean, default=1, nullable=False)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistTransportScheduling(DeclarativeBase3):
    __tablename__='tbltransport_scheduling'
    id = Column(Integer, autoincrement=True, primary_key=True)
    req_id = Column(Integer,ForeignKey('tbltransportlist.id'))
    fleet_id= Column(Integer)
    schedule_date = Column(Date)
    schedule_time = Column(Time)
    estimate_duration_hrs = Column(Integer)
    estimate_kms = Column(Integer)
    estimate_trips = Column(Integer)
    active = Column(Boolean, default=1,nullable=False)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistTransportDailyTripSheets(DeclarativeBase3):
    __tablename__='tbltransport_dailytripsheets'
    id = Column(Integer, autoincrement=True, primary_key=True)
    req_id = Column(Integer,ForeignKey('tbltransportlist.id'))
    fleet_id= Column(Integer)
    schedule_id = Column(Integer,ForeignKey('tbltransport_scheduling.id'))
    trip_date = Column(Date)
    trip_time_start = Column(Time)
    trip_time_end = Column(Time)
    odometer_start = Column(Integer)
    odometer_end = Column(Integer)
    kms_travelled = Column(Integer)
    trip_from = Column(Unicode(255))
    trip_to = Column(Unicode(255))
    estimate_kms = Column(Integer)
    estimate_trips = Column(Integer)
    person_received = Column(Unicode(255))
    person_signed = Column(Boolean,default=0,nullable=False)
    path_waybill = Column(Unicode(1024), nullable=True)
    active = Column(Boolean, default=1,nullable=False)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistTransportFleetLink(DeclarativeBase3):
    __tablename__='tbltransport_fleetlink'
    id = Column(Integer, autoincrement=True, primary_key=True)
    fleet_id = Column(Integer,unique=True, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)


class JistLabourList(DeclarativeBase8):
    __tablename__='tbllabourlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    emp_number = Column(Unicode(20))
    last_name = Column(Unicode(40))
    first_name = Column(Unicode(40))
    id_number = Column(Unicode(40))
    date_started = Column(Date)
    rate_per_day = Column(Numeric(10,2))
    division = Column(Integer,ForeignKey('tbllabourdivisions.id'))
    bank = Column(Unicode(40))
    branch_code = Column(Unicode(40))
    account_number = Column(Unicode(40))
    address1 = Column(Unicode(80))
    address2 = Column(Unicode(40))
    tel_number_home = Column(Unicode(40))
    next_of_kin_name = Column(Unicode(40))
    next_of_kin_tel = Column(Unicode(40))
    active = Column(Boolean, default=1,nullable=False)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistLabourDivisions(DeclarativeBase8):
    __tablename__='tbllabourdivisions'
    id = Column(Integer, autoincrement=True, primary_key=True)
    division_code = Column(Unicode(40))
    division_name = Column(Unicode(40))
    division_leader = Column(Integer)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistLabourCategories(DeclarativeBase8):
    __tablename__='tbllabourcategories'
    id = Column(Integer, autoincrement=True, primary_key=True)
    category_name = Column(Unicode(40),unique=True)
    listpos = Column(Integer)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistLabourCategoryLink(DeclarativeBase8):
    __tablename__='tbllabourcategory_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_category_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistStaffCategoryLink(DeclarativeBase8):
    __tablename__='tblstaffcategory_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_category_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistStaffDivisionLink(DeclarativeBase8):
    __tablename__='tblstaffdivisions_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_division_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistPointDivisionLink(DeclarativeBase8):
    __tablename__='tblpointdivisions_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_division_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistPointCategoryLink(DeclarativeBase8):
    __tablename__='tblpointcategory_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_category_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconDivisionLink(DeclarativeBase8):
    __tablename__='tblsubcondivisions_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_division_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconCategoryLink(DeclarativeBase8):
    __tablename__='tblsubconcategory_link'
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer,unique=True, nullable=False)
    lab_category_id = Column(Integer, nullable=False)
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistLabourTeamsList(DeclarativeBase8):
    __tablename__='tbllabourteams_list'
    id = Column(Integer, autoincrement=True, primary_key=True)
    team_name = Column(Unicode(80))
    team_staff_leader_id = Column(Integer,unique=True, nullable=True)
    team_lab_leader_id = Column(Integer,unique=True, nullable=True)
    team_subcon_leader_id = Column(Integer,unique=True, nullable=True)
    team_description = Column(Unicode(80))
    team_vehicle_id = Column(Integer,unique=True, nullable=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    
class JistLabourTeamsMembers(DeclarativeBase8):
    __tablename__='tbllabourteams_members'
    id = Column(Integer, autoincrement=True, primary_key=True)
    team_id = Column(Integer,unique=False, nullable=True)
    team_staff_member_id = Column(Integer,unique=True, nullable=True)
    team_lab_member_id = Column(Integer,unique=True, nullable=True)
    team_subcon_member_id = Column(Integer,unique=True, nullable=True)
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistEmployeeContactList(DeclarativeBase8):
    __tablename__='tblemployee_contact_list'
    id = Column(Integer, autoincrement=True, primary_key=True)
    staff_id = Column(Integer,unique=True, nullable=True)
    lab_id = Column(Integer,unique=True, nullable=True)
    subcon_id = Column(Integer,unique=True, nullable=True)
    office = Column(Unicode(80))
    office_tel = Column(Unicode(20))
    office_ext = Column(Unicode(10))
    mobile_tel1 = Column(Unicode(20))
    mobile_tel2 = Column(Unicode(20))
    mobile_tel3 = Column(Unicode(20))
    email = Column(Unicode(20))
    sip = Column(Unicode(20))
    description = Column(Unicode(200))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)


class JistLabourTeamsSchedule(DeclarativeBase8):
    __tablename__='tbllabourteams_schedule'
    id = Column(Integer, autoincrement=True, primary_key=True)
    team_id = Column(Integer,unique=False, nullable=False)
    schedule_date = Column(Date, nullable=False)
    jcno = Column(Integer,unique=False, nullable=False)
    work_percent = Column(Integer)
    task_name = Column(Unicode(80))
    useridnew = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)

class JistLabourPaymentRunsList(DeclarativeBase8):
    __tablename__='tbllabourpaymentrunlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    payment_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    payment_number = Column(Integer)
    total_gross = Column(Numeric(10,2))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistLabourPaymentRunsData(DeclarativeBase8):
    __tablename__='tbllabourpaymentrundata'
    id = Column(Integer, autoincrement=True, primary_key=True)
    empl_id = Column(Integer)
    div_id = Column(Integer)
    paylist_id = Column(Integer,ForeignKey('tbllabourpaymentrunlist.id'))
    rate_per_day = Column(Numeric(10,2))
    rate_per_hour = Column(Numeric(10,2))
    hours_normal = Column(Numeric(10,2))
    amount_normal_time = Column(Numeric(10,2))
    hours_over_time = Column(Numeric(10,2))
    amount_over_time = Column(Numeric(10,2))
    hours_sunday_time = Column(Numeric(10,2))
    amount_sunday_time = Column(Numeric(10,2))
    amount_gross_total = Column(Numeric(10,2))
    uif = Column(Numeric(10,2))
    paye = Column(Numeric(10,2))
    staff_loans = Column(Numeric(10,2))
    amount_net_total = Column(Numeric(10,2))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconList(DeclarativeBase8):
    __tablename__='tblsubconlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    trading_name = Column(Unicode(80))
    last_name = Column(Unicode(40))
    first_name = Column(Unicode(40))
    id_number = Column(Unicode(40))
    date_started = Column(Date)
    rate_per_day = Column(Numeric(10,2))
    division = Column(Integer,ForeignKey('tblsubcondivisions.id'))
    vat_number = Column(Unicode(40))
    bank = Column(Unicode(40))
    branch_code = Column(Unicode(40))
    account_number = Column(Unicode(40))
    address1 = Column(Unicode(80))
    address2 = Column(Unicode(40))
    tel_number_home = Column(Unicode(40))
    next_of_kin_name = Column(Unicode(40))
    next_of_kin_tel = Column(Unicode(40))
    active = Column(Boolean, default=True,nullable=False)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconDivisions(DeclarativeBase8):
    __tablename__='tblsubcondivisions'
    id = Column(Integer, autoincrement=True, primary_key=True)
    division_code = Column(Unicode(40))
    division_name = Column(Unicode(40))
    division_leader = Column(Integer)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconPaymentRunsList(DeclarativeBase8):
    __tablename__='tblsubconpaymentrunlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    payment_date = Column(Date)
    start_date = Column(Date)
    end_date = Column(Date)
    payment_number = Column(Integer)
    total_gross = Column(Numeric(10,2))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconPaymentRunsData(DeclarativeBase8):
    __tablename__='tblsubconpaymentrundata'
    id = Column(Integer, autoincrement=True, primary_key=True)
    sub_id = Column(Integer)
    div_id = Column(Integer)
    jcno = Column(Integer)
    paylist_id = Column(Integer,ForeignKey('tblsubconpaymentrunlist.id'))
    item = Column(Unicode(80))
    description = Column(Unicode(255))
    unit = Column(Unicode(40))
    qty = Column(Numeric(10,2))
    price = Column(Numeric(10,2))
    total_excl = Column(Numeric(10,2))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistSubconClaimItems(DeclarativeBase8):
    __tablename__='tblsubconclaimitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    sub_id = Column(Integer)
    div_id = Column(Integer)
    jcno = Column(Integer)
    paylist_id = Column(Integer,ForeignKey('tblsubconpaymentrunlist.id'))
    item = Column(Unicode(80))
    description = Column(Unicode(255))
    unit = Column(Numeric(10,2))
    qty = Column(Numeric(10,2))
    price = Column(Numeric(10,2))
    total_excl = Column(Numeric(10,2))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)

class JistPaymentReqs(DeclarativeBase7):
    __tablename__='tblpaymentsreq'
    id = Column(Integer, autoincrement=True, primary_key=True)
    payreq_date = Column(Numeric(10,2),default=0)  
    payreq_ponumber = Column(Integer)
    payreq_payee  = Column(Integer) 
    payreq_by  = Column(Integer)    
    payreq_jcno  = Column(Integer)  
    payreq_purchasereq_number = Column(Integer)
    payreq_description   = Column(Unicode(255))
    payreq_unit = Column(Unicode(80))        
    payreq_qty  = Column(Numeric(10,2),default=0)        
    payreq_rate = Column(Numeric(10,2),default=0)        
    payreq_total_excl = Column(Numeric(10,2),default=0)      
    payreq_total_vat = Column(Numeric(10,2),default=0)      
    payreq_total_incl = Column(Numeric(10,2),default=0)      
    payreq_must_pay_date = Column(Date,nullable=False)      
    payreq_promised_pay_date = Column(Date,nullable=False)    
    payreq_date_topay = Column(Date,nullable=False)       
    payreq_paid  = Column(Boolean, default=False)          
    payreq_date_paid = Column(Date,nullable=True)       
    payreq_approved_bln = Column(Boolean,default=False)       
    userid_approved = Column(Integer)         
    payreq_approved_date = Column(Date,nullable=True)       
    payreq_active  = Column(Boolean, default=True)         
    useridnew = Column(Integer)         
    dateadded = Column(DateTime, default=datetime.now)         
    dateedited = Column(DateTime, default=datetime.now)        
    useridedited = Column(Integer)       

class JistPaymentPayee(DeclarativeBase7):
    __tablename__='tblpaymentspayee'
    id = Column(Integer, autoincrement=True, primary_key=True)
    payee_name = Column(Unicode(255))  
    payee_add1 = Column(Unicode(255))
    payee_add2 = Column(Unicode(255))
    payee_add3 = Column(Unicode(255))
    payee_add4 = Column(Unicode(255))
    payee_vat_no = Column(Unicode(80))
    payee_bank = Column(Unicode(80))
    payee_branch = Column(Unicode(80))
    payee_accno = Column(Unicode(80))
    payee_contact = Column(Unicode(80))
    payee_email = Column(Unicode(80))
    payee_tel = Column(Unicode(80))
    payee_fax = Column(Unicode(80))

class JistInvoicesList(DeclarativeBase7):
    __tablename__='tblinvoices'
    id = Column(Integer, autoincrement=True, primary_key=True)
    invoiceno = Column(Unicode(50),nullable=False)
    invdate = Column(Date,nullable=False)
    ordernumber = Column(Unicode(50))
    client = Column(Unicode(50),nullable=False)
    value_excl = Column(Numeric(10,2),default=0)
    value_vat = Column(Numeric(10,2),default=0)
    value_incl = Column(Numeric(10,2),default=0)
    blnpayed = Column(ENUM('Y','N'),default='N',nullable=False)
    contract = Column(Integer)

class JistInvoicesClients(DeclarativeBase7):
    __tablename__='tblinvclients'
    id = Column(Integer, autoincrement=True, primary_key=True)
    invoiceid = Column(Integer,nullable=False)
    add1 = Column(Text)
    add2 = Column(Text)
    add3 = Column(Text)
    vatno = Column(Text)
    delvToname = Column(Text)
    delvToadd1 = Column(Text)
    delvToadd2 = Column(Text)
    delvTocontperson = Column(Text)
    delvToconttel = Column(Text)

class JistInvoicesData(DeclarativeBase7):
    __tablename__='tblinvoicedata'
    id = Column(Integer, autoincrement=True, primary_key=True)
    invid = Column(Integer,nullable=False)
    item = Column(Text)
    description = Column(Text)
    unit = Column(Text)
    qty = Column(Text)
    price = Column(Text)
    total = Column(Text)
    orderitemsid = Column(Integer)

class JistInvoicesPayments(DeclarativeBase7):
    __tablename__='tblinvpayments'
    id = Column(Integer, autoincrement=True, primary_key=True)
    #paylist_id = Column(Integer,ForeignKey('tblsubconpaymentrunlist.id'))
    invoiceid = Column(Integer,ForeignKey('tblinvoices.id'),)
    paymentdate = Column(Date)
    amount = Column(Numeric(10,2),default=0)


class JistManufactureClients(DeclarativeBase6):
    __tablename__='tblman_clients'
    id = Column(Integer, autoincrement=True, primary_key=True)
    clientname = Column(Text)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistManufactureOrderItems(DeclarativeBase6):
    __tablename__='tblman_orderitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jist_po = Column(Integer)
    jist_po_itemid = Column(Integer,unique=True)
    item = Column(Unicode(80))
    description = Column(Unicode(280))
    unit = Column(Unicode(80))
    qty = Column(Numeric(10,2),default=0.00)
    price = Column(Numeric(10,2),default=0.00)
    total = Column(Numeric(10,2),default=0.00)
    active_production = Column(Boolean, default=False)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistManufactureStandardList(DeclarativeBase6):
    __tablename__='tblman_standard_matlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Unicode(80))
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistManufacturingStages(DeclarativeBase6):
    __tablename__='tblman_stages'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(80),unique=True)
    description = Column(Unicode(280))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistManufacturingWorkFlow(DeclarativeBase6):
    __tablename__='tblman_workflow'
    id = Column(Integer, autoincrement=True, primary_key=True)
    man_order_id = Column(Integer, nullable=False)
    man_stage_id = Column(Integer, nullable=False)
    man_stage_qty = Column(Numeric(10,2),default=0.00)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)
    active = Column(Boolean, default=True)



class JistManufactureStandardListItems(DeclarativeBase6):
    __tablename__='tblman_standard_matlist_items'
    id = Column(Integer, autoincrement=True, primary_key=True)
    listid = Column(Integer)
    groupname = Column(Unicode(80))
    qty_req = Column(Unicode(80))
    materialname = Column(Unicode(80))
    diameter = Column(Unicode(80))
    width = Column(Unicode(80))
    height = Column(Unicode(80))
    length = Column(Unicode(80))
    supp_lens = Column(Unicode(80))
    weight = Column(Unicode(80))
    diameter = Column(Unicode(80))
    thickness = Column(Unicode(80))
    price = Column(Numeric(10,2),default=0.00)
    total = Column(Numeric(10,2),default=0.00)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistManufactureNonStandardList(DeclarativeBase6):
    __tablename__='tblman_nonstandard_matlist'
    id = Column(Integer, autoincrement=True, primary_key=True)
    groupname = Column(Unicode(80))
    qty_req = Column(Unicode(80))
    materialname = Column(Unicode(80))
    diameter = Column(Unicode(80))
    width = Column(Unicode(80))
    height = Column(Unicode(80))
    length = Column(Unicode(80))
    supp_lens = Column(Unicode(80))
    weight = Column(Unicode(80))
    diameter = Column(Unicode(80))
    thickness = Column(Unicode(80))
    price = Column(Numeric(10,2),default=0.00)
    total = Column(Numeric(10,2),default=0.00)
    useridnew = Column(Integer, nullable=False)
    useridedited = Column(Integer, nullable=False)
    dateadded = Column(DateTime, default=datetime.now)
    dateedited = Column(DateTime, default=datetime.now)

class JistManufactureAngleEqualData(DeclarativeBase6):
    __tablename__='tblman_angle_eq_data'
    id = Column(Integer, autoincrement=True, primary_key=True)
    width = Column(Unicode(20))
    height = Column(Unicode(20))
    thickness = Column(Unicode(20))
    mass_kg_m = Column(Unicode(20))
    paint_area_ton = Column(Unicode(20))

class JistManufactureAngleNonEqualData(DeclarativeBase6):
    __tablename__='tblman_angle_noneq_data'
    id = Column(Integer, autoincrement=True, primary_key=True)
    width = Column(Unicode(20))
    height = Column(Unicode(20))
    thickness = Column(Unicode(20))
    mass_kg_m = Column(Unicode(20))
    paint_area_ton = Column(Unicode(20))

class JistManufactureIPEData(DeclarativeBase6):
    __tablename__='tblman_ipe_data'
    id = Column(Integer, autoincrement=True, primary_key=True)
    width = Column(Unicode(20))
    height = Column(Unicode(20))
    thickness = Column(Unicode(20))
    mass_kg_m = Column(Unicode(20))
    paint_area_ton = Column(Unicode(20))

class JistManufactureFlatsData(DeclarativeBase6):
    __tablename__='tblman_flats_data'
    id = Column(Integer, autoincrement=True, primary_key=True)
    width = Column(Unicode(20))
    height = Column(Unicode(20))
    thickness = Column(Unicode(20))
    mass_kg_m = Column(Unicode(20))
    paint_area_ton = Column(Unicode(20))


class JistMarketingClientLeads(DeclarativeBase9):
    __tablename__='tblmarleads'
    id = Column(Integer, autoincrement=True, primary_key=True)
    date = Column(Date)
    client_name = Column(Unicode(80))
    contact_person = Column(Unicode(80))
    site_location = Column(Unicode(80))
    contact_tel = Column(Unicode(80))
    point_person = Column(Integer)
    active = Column(Boolean, default=True)
    last_followup_date = Column(Date())
    next_followup_date = Column(Date())
    comments = Column(Unicode(250))
    useridnew = Column(Integer)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer)

class JistMarketingLeadsHistory(DeclarativeBase9):
    __tablename__='tblmarhistory'
    id = Column(Integer, autoincrement=True, primary_key=True)
    lead_id = Column(Integer)
    report_date = Column(Date)
    report_body = Column(Text)
    useridnew = Column(Integer)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer)

class JistMarketingSiteVisit(DeclarativeBase9):
    __tablename__='tblmarsitevisits'
    id = Column(Integer, autoincrement=True, primary_key=True)
    lead_id = Column(Integer)
    site_visit_date = Column(Date)
    site_visit_time = Column(Time)
    site_name = Column(Unicode(255))
    site_location = Column(Unicode(255))
    scope_type = Column(Unicode(255))
    closing_date = Column(Date)
    closing_time = Column(Time)
    contact_person = Column(Unicode(255))
    contact_tel = Column(Unicode(255))
    reference_number = Column(Unicode(255))
    document_price = Column(Unicode(255))
    cidb_rating = Column(Unicode(25))
    comments = Column(Text)
    assigned_to = Column(Integer)
    assigned_by = Column(Integer)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer)

class JistMarketingScopeOfWork(DeclarativeBase9):
    __tablename__='tblmarscopeofwork'
    id = Column(Integer, autoincrement=True, primary_key=True)
    lead_id = Column(Integer)
    site_visit_id = Column(Integer)
    item = Column(Unicode(80))
    description = Column(Unicode(255))
    unit = Column(Unicode(255))
    quantity = Column(Numeric)
    price = Column(Numeric)
    total = Column(Numeric)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer)

class JistMarketingSiteVisitReport(DeclarativeBase9):
    __tablename__='tblmarsitevisitreport'
    id = Column(Integer, autoincrement=True, primary_key=True)
    lead_id = Column(Integer)
    site_visit_id = Column(Integer)
    site_visit_date = Column(Date)
    report_body = Column(Text)
    useridnew = Column(Integer)
    dateedited = Column(DateTime, default=datetime.now)
    dateadded = Column(DateTime, default=datetime.now)
    useridedited = Column(Integer)

class JistFileStoreMarketing(DeclarativeBase9):
    __tablename__ = 'tblfilestoremarketing'
        
    id = Column(Integer, primary_key=True)
    filename = Column(Unicode(255), nullable=False)
    jcno = Column(Integer, nullable=False)
    takenby = Column(Integer, nullable=False)
    datetaken = Column(Date,nullable=False)
    description = Column(Text, nullable=True)
    thumbname = Column(Text, nullable=True)
    datecreated = Column(DateTime, default=datetime.now)
    useridcreated = Column(Integer)
    
    def __init__(self,jcno , filename,
            fileunder,takenby,datetaken,description,
            useridcreated):
        self.filename = filename
        self.jcno = jcno
        self.takenby = takenby
        self.fileunder = fileunder
        self.datetaken = datetaken 
        self.description = description 
        self.useridcreated =useridcreated 

class JistEstimating3yrBuildingSites(DeclarativeBase10):
    __tablename__='tbl3yrsites'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(80))
    description = Column(Unicode(255))
    wonumber = Column(Unicode(50))
    supervisor = Column(Unicode(80))
    date = Column(Date)
    area = Column(Unicode(80))
    visit_by = Column(Unicode(80))
    #active = Column(Boolean, default=True)
    active = Column(Unicode(1))
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrBuildingQuotes(DeclarativeBase10):
    __tablename__='tbl3yrQuotes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    estdate = Column(Date)
    idsite = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrBuildingQuoteScope(DeclarativeBase10):
    __tablename__='tbl3yrQuoteScope'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idscope = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrBuildingQuoteBQItems(DeclarativeBase10):
    __tablename__='tbl3yrQuotebqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idbqitem = Column(Integer)
    idscope = Column(Integer)
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrBuildingSchedules(DeclarativeBase10):
    __tablename__='tbl3yrschedules'
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Unicode(255))

class JistEstimating3yrBuildingHeadings(DeclarativeBase10):
    __tablename__='tbl3yrheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idschedule = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating3yrBuildingSubHeadings(DeclarativeBase10):
    __tablename__='tbl3yrsubheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idheading = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating3yrBuildingItems(DeclarativeBase10):
    __tablename__='tbl3yritems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsubheading = Column(Unicode(80))
    pageno = Column(Unicode(80))
    itemno = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    price = Column(Numeric(10,2),default=0)

class JistEstimating3yrBuildingSiteSOW(DeclarativeBase10):
    __tablename__='tbl3yrscopeofwork'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsite = Column(Unicode(80))
    scope = Column(Unicode(250))
    unit = Column(Unicode(80))
    quantity = Column(Unicode(80))
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrBuildingSOWBQItems(DeclarativeBase10):
    __tablename__='tbl3yrbqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id3yritem = Column(Unicode(80))
    idscope = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrBuildingStatusCodes(DeclarativeBase10):
    __tablename__='tbl3yrsitestatuscodes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    status = Column(Unicode(250))

class JistEstimating3yrBuildingStatusData(DeclarativeBase10):
    __tablename__='tbl3yrsitestatusdata'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsite = Column(Unicode(80))
    statuscode = Column(Unicode(250))
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingSites(DeclarativeBase11):
    __tablename__='tbl5yrsites'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(80))
    coordinates = Column(Unicode(255))
    province = Column(Unicode(255))
    area = Column(Unicode(80))
    description = Column(Unicode(255))
    wonumber = Column(Unicode(50))
    supervisor = Column(Unicode(80))
    date = Column(Date)
    visit_by = Column(Unicode(80))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingQuotes(DeclarativeBase11):
    __tablename__='tbl5yrQuotes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    estdate = Column(Date)
    idsite = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingQuoteScope(DeclarativeBase11):
    __tablename__='tbl5yrQuoteScope'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idscope = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingQuoteBQItems(DeclarativeBase11):
    __tablename__='tbl5yrQuotebqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idbqitem = Column(Integer)
    idscope = Column(Integer)
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingSchedules(DeclarativeBase11):
    __tablename__='tbl5yrschedules'
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Unicode(255))

class JistEstimating5yrEskomFencingHeadings(DeclarativeBase11):
    __tablename__='tbl5yrheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idschedule = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating5yrEskomFencingSubHeadings(DeclarativeBase11):
    __tablename__='tbl5yrsubheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idheading = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating5yrEskomFencingItems(DeclarativeBase11):
    __tablename__='tbl5yrbill'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsubheading = Column(Unicode(80))
    pageno = Column(Unicode(80))
    itemno = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    price = Column(Numeric(10,2),default=0)

class JistEstimating5yrEskomFencingSiteSOW(DeclarativeBase11):
    __tablename__='tbl5yrscopeofwork'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsite = Column(Unicode(80))
    scope = Column(Unicode(250))
    unit = Column(Unicode(80))
    quantity = Column(Unicode(80))
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingSOWBQItems(DeclarativeBase11):
    __tablename__='tbl5yrbqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id5yritem = Column(Unicode(80))
    idscope = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating5yrEskomFencingPhotos(DeclarativeBase11):
    __tablename__ = 'tblestphotos'
    pic_id = Column(Integer, primary_key=True)
    filesubject = Column(Unicode(255), nullable=False)
    filename = Column(Unicode(255), nullable=False)
    jcno = Column(Integer, nullable=True)
    takenby = Column(Integer, nullable=False)
    datetaken = Column(Date,nullable=False)
    description = Column(Text, nullable=True)
    thumbname = Column(Text, nullable=True)
    datecreated = Column(DateTime, default=datetime.date(datetime.now()))
    useridnew = Column(Integer)
    defaultpic = Column(Boolean, default=False)

class JistEstimating3yrEssPalisadeSites(DeclarativeBase12):
    __tablename__='tbl3yrsites'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(80))
    coordinates = Column(Unicode(255))
    province = Column(Unicode(255))
    area = Column(Unicode(80))
    description = Column(Unicode(255))
    wonumber = Column(Unicode(50))
    supervisor = Column(Unicode(80))
    date = Column(Date)
    visit_by = Column(Unicode(80))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeQuotes(DeclarativeBase12):
    __tablename__='tbl3yrQuotes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    estdate = Column(Date)
    idsite = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeQuoteScope(DeclarativeBase12):
    __tablename__='tbl3yrQuoteScope'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idscope = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeQuoteBQItems(DeclarativeBase12):
    __tablename__='tbl3yrQuotebqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idbqitem = Column(Integer)
    idscope = Column(Integer)
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeSchedules(DeclarativeBase12):
    __tablename__='tbl3yrschedules'
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Unicode(255))

class JistEstimating3yrEssPalisadeHeadings(DeclarativeBase12):
    __tablename__='tbl3yrheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idschedule = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating3yrEssPalisadeSubHeadings(DeclarativeBase12):
    __tablename__='tbl3yrsubheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idheading = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating3yrEssPalisadeItems(DeclarativeBase12):
    __tablename__='tbl3yrbill'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsubheading = Column(Unicode(80))
    pageno = Column(Unicode(80))
    itemno = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    price = Column(Numeric(10,2),default=0)

class JistEstimating3yrEssPalisadeSiteSOW(DeclarativeBase12):
    __tablename__='tbl3yrscopeofwork'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsite = Column(Unicode(80))
    scope = Column(Unicode(250))
    unit = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeSOWBQItems(DeclarativeBase12):
    __tablename__='tbl3yrbqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id3yritem = Column(Unicode(80))
    idscope = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadePhotos(DeclarativeBase12):
    __tablename__ = 'tblestphotos'
    pic_id = Column(Integer, primary_key=True)
    filesubject = Column(Unicode(255), nullable=False)
    filename = Column(Unicode(255), nullable=False)
    jcno = Column(Integer, nullable=True)
    takenby = Column(Integer, nullable=False)
    datetaken = Column(Date,nullable=False)
    description = Column(Text, nullable=True)
    thumbname = Column(Text, nullable=True)
    datecreated = Column(DateTime, default=datetime.date(datetime.now()))
    useridnew = Column(Integer)
    defaultpic = Column(Boolean, default=False)

class JistEstimating3yrEssPalisadeJCNOEstLink(DeclarativeBase12):
    __tablename__='tbl3yrjcnoestlink'
    id = Column(Integer, autoincrement=True, primary_key=True)
    jcnoid = Column(Integer)
    siteid = Column(Integer)
    quoteid = Column(Integer)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeSiteRequirements(DeclarativeBase12):
    __tablename__='tbl3yr_site_requirements'
    id = Column(Integer, autoincrement=True, primary_key=True)
    linkid = Column(Integer)
    matlistid = Column(Integer)
    quoteid = Column(Integer)
    active = Column(Boolean, default=True)
    qty = Column(Numeric(10,3),default=0)
    instruction = Column(Unicode(80))
    date_req = Column(Date)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeStandardMaterialList(DeclarativeBase12):
    __tablename__='tbl3yr_standard_material_list'
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Unicode(255))
    size = Column(Unicode(80))
    length = Column(Unicode(80))
    height = Column(Unicode(80))
    weight = Column(Unicode(80))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeStoresReceiveList(DeclarativeBase12):
    __tablename__='tbl3yr_stores_receive_list'
    id = Column(Integer, autoincrement=True, primary_key=True)
    matlistid = Column(Integer)
    qty = Column(Numeric(10,3),default=0)
    received_from = Column(Unicode(255))
    comment = Column(Unicode(255))
    date_received = Column(Date)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeStoresDespatchList(DeclarativeBase12):
    __tablename__='tbl3yr_stores_despatch_list'
    id = Column(Integer, autoincrement=True, primary_key=True)
    matlistid = Column(Integer)
    jcno = Column(Integer)
    qty = Column(Numeric(10,3),default=0)
    despatch_to = Column(Unicode(255))
    comment = Column(Unicode(255))
    date_despatch = Column(Date)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssPalisadeStoresReturnList(DeclarativeBase12):
    __tablename__='tbl3yr_stores_return_list'
    id = Column(Integer, autoincrement=True, primary_key=True)
    matlistid = Column(Integer)
    jcno = Column(Integer)
    qty = Column(Numeric(10,3),default=0)
    return_by = Column(Unicode(255))
    comment = Column(Unicode(255))
    date_returned = Column(Date)
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)


class JistEstimating3yrEssHSFSites(DeclarativeBase13):
    __tablename__='tbl3yrsites'
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Unicode(80))
    coordinates = Column(Unicode(255))
    province = Column(Unicode(255))
    area = Column(Unicode(80))
    description = Column(Unicode(255))
    wonumber = Column(Unicode(50))
    supervisor = Column(Unicode(80))
    date = Column(Date)
    visit_by = Column(Unicode(80))
    active = Column(Boolean, default=True)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssHSFQuotes(DeclarativeBase13):
    __tablename__='tbl3yrQuotes'
    id = Column(Integer, autoincrement=True, primary_key=True)
    estdate = Column(Date)
    idsite = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssHSFQuoteScope(DeclarativeBase13):
    __tablename__='tbl3yrQuoteScope'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idscope = Column(Integer)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssHSFQuoteBQItems(DeclarativeBase13):
    __tablename__='tbl3yrQuotebqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idquote = Column(Integer)
    idbqitem = Column(Integer)
    idscope = Column(Integer)
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssHSFSchedules(DeclarativeBase13):
    __tablename__='tbl3yrschedules'
    id = Column(Integer, autoincrement=True, primary_key=True)
    description = Column(Unicode(255))

class JistEstimating3yrEssHSFHeadings(DeclarativeBase13):
    __tablename__='tbl3yrheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idschedule = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating3yrEssHSFSubHeadings(DeclarativeBase13):
    __tablename__='tbl3yrsubheadings'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idheading = Column(Unicode(80))
    description = Column(Unicode(255))

class JistEstimating3yrEssHSFItems(DeclarativeBase13):
    __tablename__='tbl3yrbill'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsubheading = Column(Unicode(80))
    pageno = Column(Unicode(80))
    itemno = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    price = Column(Numeric(10,2),default=0)

class JistEstimating3yrEssHSFSiteSOW(DeclarativeBase13):
    __tablename__='tbl3yrscopeofwork'
    id = Column(Integer, autoincrement=True, primary_key=True)
    idsite = Column(Unicode(80))
    scope = Column(Unicode(250))
    unit = Column(Unicode(80))
    quantity = Column(Unicode(80))
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssHSFSOWBQItems(DeclarativeBase13):
    __tablename__='tbl3yrbqitems'
    id = Column(Integer, autoincrement=True, primary_key=True)
    id3yritem = Column(Unicode(80))
    idscope = Column(Unicode(80))
    description = Column(Unicode(255))
    units = Column(Unicode(80))
    quantity = Column(Numeric(10,3),default=0)
    price = Column(Numeric(10,2),default=0)
    total = Column(Numeric(10,2),default=0)
    useridnew = Column(Integer)
    dateadded = Column(Date)
    dateedited = Column(Date)
    timeedited = Column(Time)
    useridedited = Column(Integer)

class JistEstimating3yrEssHSFPhotos(DeclarativeBase13):
    __tablename__ = 'tblestphotos'
    pic_id = Column(Integer, primary_key=True)
    filesubject = Column(Unicode(255), nullable=False)
    filename = Column(Unicode(255), nullable=False)
    jcno = Column(Integer, nullable=True)
    takenby = Column(Integer, nullable=False)
    datetaken = Column(Date,nullable=False)
    description = Column(Text, nullable=True)
    thumbname = Column(Text, nullable=True)
    datecreated = Column(DateTime, default=datetime.date(datetime.now()))
    useridnew = Column(Integer)
    defaultpic = Column(Boolean, default=False)


class ServerHit(DeclarativeBase2):
    __tablename__ = 'server_hit'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, nullable=False, default=datetime.now)
    remote_addr = Column(Unicode(15), nullable=False)
    path_info = Column(Unicode(1024), nullable=False)
    query_string = Column(Unicode(1024), nullable=False)
