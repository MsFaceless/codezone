# -*- coding: utf-8 -*-
"""The application's model objects"""

from zope.sqlalchemy import ZopeTransactionExtension
from sqlalchemy.orm import scoped_session, sessionmaker
#from sqlalchemy import MetaData
from sqlalchemy.orm import mapper, relation
from sqlalchemy import Table, ForeignKey, Column, func
from sqlalchemy import MetaData
from sqlalchemy import *
from sqlalchemy.dialects.mysql  import *
from sqlalchemy.ext.declarative import declarative_base

# Global session manager: DBSession() returns the Thread-local
# session object appropriate for the current web request.
maker = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBSession = scoped_session(maker)

maker2 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_ContractData = scoped_session(maker2)

maker3 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistFleetTransport = scoped_session(maker3)

maker4 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistFileStore = scoped_session(maker4)

maker5 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistBuying = scoped_session(maker5)
maker6 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistManufacturing = scoped_session(maker6)
maker7 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistInvoicing = scoped_session(maker7)
maker8 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistLabour = scoped_session(maker8)
maker9 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_JistMarketing = scoped_session(maker9)
maker10 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_Jist3yrBuilding = scoped_session(maker10)
maker11 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_Jist5yrEskomFencing = scoped_session(maker11)
maker12 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_Jist3yrEssPalisade = scoped_session(maker12)
maker13 = sessionmaker(autoflush=True, autocommit=False,
                     extension=ZopeTransactionExtension())
DBS_Jist3yrEssHSF = scoped_session(maker13)

# Base class for all of our model classes: By default, the data model is
# defined with SQLAlchemy's declarative extension, but if you need more
# control, you can switch to the traditional method.
DeclarativeBase = declarative_base()
DeclarativeBase2 = declarative_base()
DeclarativeBase3 = declarative_base()
DeclarativeBase4 = declarative_base()
DeclarativeBase5 = declarative_base()
DeclarativeBase6 = declarative_base()
DeclarativeBase7 = declarative_base()
DeclarativeBase8 = declarative_base()
DeclarativeBase9 = declarative_base()
DeclarativeBase10 = declarative_base()
DeclarativeBase11 = declarative_base()
DeclarativeBase12 = declarative_base()
DeclarativeBase13 = declarative_base()

DeclarativeBase2.query = DBS_ContractData.query_property()

# There are two convenient ways for you to spare some typing.
# You can have a query property on all your model classes by doing this:
# DeclarativeBase.query = DBSession.query_property()
# Or you can use a session-aware mapper as it was used in TurboGears 1:
# DeclarativeBase = declarative_base(mapper=DBSession.mapper)

# Global metadata.
# The default metadata is the one from the declarative base.
metadata = DeclarativeBase.metadata
metadata2 = DeclarativeBase2.metadata
metadata3 = DeclarativeBase3.metadata
metadata4 = DeclarativeBase4.metadata
metadata5 = DeclarativeBase5.metadata
metadata6 = DeclarativeBase6.metadata
metadata7 = DeclarativeBase7.metadata
metadata8 = DeclarativeBase8.metadata
metadata9 = DeclarativeBase9.metadata
metadata10 = DeclarativeBase10.metadata
metadata11 = DeclarativeBase11.metadata
metadata12 = DeclarativeBase12.metadata
metadata13 = DeclarativeBase13.metadata
# If you have multiple databases with overlapping table names, you'll need a
# metadata for each database. Feel free to rename 'metadata2'.
#metadata2 = MetaData()

#####
# Generally you will not want to define your table's mappers, and data objects
# here in __init__ but will want to create modules them in the model directory
# and import them at the bottom of this file.
#
######

def init_model(engine1, engine2, engine3,engine4,engine5,engine6,engine7,engine8,engine9,engine10,engine11,engine12,engine13):
    """Call me before using any of the tables or classes in the model."""
    DBSession.configure(bind=engine1)
    DBS_ContractData.configure(bind=engine2)
    DBS_JistFleetTransport.configure(bind=engine3)
    DBS_JistFileStore.configure(bind=engine4)
    DBS_JistBuying.configure(bind=engine5)
    DBS_JistManufacturing.configure(bind=engine6)
    DBS_JistInvoicing.configure(bind=engine7)
    DBS_JistLabour.configure(bind=engine8)
    DBS_JistMarketing.configure(bind=engine9)
    DBS_Jist3yrBuilding.configure(bind=engine10)
    DBS_Jist5yrEskomFencing.configure(bind=engine11)
    DBS_Jist3yrEssPalisade.configure(bind=engine12)
    DBS_Jist3yrEssHSF.configure(bind=engine13)

    # If you are using reflection to introspect your database and create
    # table objects for you, your tables must be defined and mapped inside
    # the init_model function, so that the engine is available if you
    # use the model outside tg2, you need to make sure this is called before
    # you use the model.

    #
    # See the following example:

    #global t_reflected

    #t_reflected = Table("Reflected", metadata,
    #    autoload=True, autoload_with=engine)

    #mapper(Reflected, t_reflected)

# Import your model modules here.
from jistdocstore.model.auth import User, Group, Permission
from jistdocstore.model.userfile import FileStoreProduction 
from jistdocstore.model.userfile import PictureCategory 
from jistdocstore.model.userfile import PictureSharing 
from jistdocstore.model.userfile import ProductionTasks 
from jistdocstore.model.userfile import TasksDetails 
from jistdocstore.model.userfile import SiteDiaryContracts 
from jistdocstore.model.userfile import JistContracts
from jistdocstore.model.userfile import JistContractContractual
from jistdocstore.model.userfile import JistContractScope
from jistdocstore.model.userfile import JistContractBudget
from jistdocstore.model.userfile import JistContractOrderItems
from jistdocstore.model.userfile import JistContractStatus
from jistdocstore.model.userfile import JistContractStatusCodes
from jistdocstore.model.userfile import JistContractPlanningDates
from jistdocstore.model.userfile import JistLocationList
from jistdocstore.model.userfile import JistContractPlanningResource
from jistdocstore.model.userfile import JistBuyingPurchaseReqsList
from jistdocstore.model.userfile import JistBuyingRentalsLink
from jistdocstore.model.userfile import JistBuyingPORentalTable
from jistdocstore.model.userfile import JistBuyingMaintenanceLink
from jistdocstore.model.userfile import JistBuyingPurchaseReqsItems
from jistdocstore.model.userfile import JistBuyingPurchaseReqsNotes
from jistdocstore.model.userfile import JistBuyingPurchaseReqsItemsShoppingList
from jistdocstore.model.userfile import JistBuyingPurchaseReqsItemsShoppingPrices
from jistdocstore.model.userfile import JistReceptionTelephoneMessages
from jistdocstore.model.userfile import JistOutOfOfficeNotices
from jistdocstore.model.userfile import JistFleetList 
from jistdocstore.model.userfile import JistFleetFuelUsage 
from jistdocstore.model.userfile import JistFleetMaintenanceList 
from jistdocstore.model.userfile import JistFleetMaintenanceItems 
from jistdocstore.model.userfile import JistFleetDriverList 
from jistdocstore.model.userfile import JistTransportList 
from jistdocstore.model.userfile import JistTransportLoadingBill 
from jistdocstore.model.userfile import JistTransportScheduling 
from jistdocstore.model.userfile import JistTransportFleetLink 
from jistdocstore.model.userfile import JistTransportDailyTripSheets 
from jistdocstore.model.userfile import JistLabourList 
from jistdocstore.model.userfile import JistLabourDivisions 
from jistdocstore.model.userfile import JistLabourCategories 
from jistdocstore.model.userfile import JistLabourCategoryLink 
from jistdocstore.model.userfile import JistStaffDivisionLink 
from jistdocstore.model.userfile import JistStaffCategoryLink 
from jistdocstore.model.userfile import JistPointDivisionLink 
from jistdocstore.model.userfile import JistPointCategoryLink 
from jistdocstore.model.userfile import JistSubconDivisionLink 
from jistdocstore.model.userfile import JistSubconCategoryLink 
from jistdocstore.model.userfile import JistLabourTeamsList 
from jistdocstore.model.userfile import JistLabourTeamsMembers 
from jistdocstore.model.userfile import JistLabourTeamsSchedule 
from jistdocstore.model.userfile import JistEmployeeContactList 
from jistdocstore.model.userfile import JistLabourPaymentRunsList 
from jistdocstore.model.userfile import JistLabourPaymentRunsData 
from jistdocstore.model.userfile import JistSubconList 
from jistdocstore.model.userfile import JistSubconDivisions 
from jistdocstore.model.userfile import JistSubconPaymentRunsList 
from jistdocstore.model.userfile import JistSubconPaymentRunsData 
from jistdocstore.model.userfile import JistSubconClaimItems 
from jistdocstore.model.userfile import JistPaymentReqs
from jistdocstore.model.userfile import JistPaymentPayee
from jistdocstore.model.userfile import JistInvoicesList
from jistdocstore.model.userfile import JistInvoicesClients
from jistdocstore.model.userfile import JistInvoicesData
from jistdocstore.model.userfile import JistInvoicesPayments
#from jistdocstore.model.userfile import JistEstimating2yrQuotes
#from jistdocstore.model.userfile import JistEstimating2yrSites
from jistdocstore.model.userfile import JistMarketingClientLeads
from jistdocstore.model.userfile import JistMarketingLeadsHistory
from jistdocstore.model.userfile import JistMarketingSiteVisit
from jistdocstore.model.userfile import JistMarketingSiteVisitReport
from jistdocstore.model.userfile import JistMarketingScopeOfWork
from jistdocstore.model.userfile import JistFileStoreMarketing
from jistdocstore.model.userfile import JistBuyingOrderList
from jistdocstore.model.userfile import JistBuyingOrderItems
from jistdocstore.model.userfile import JistBuyingGRV
from jistdocstore.model.userfile import JistBuyingSupplierList
from jistdocstore.model.userfile import JistBuyingStoresLocation
from jistdocstore.model.userfile import JistEstimating3yrBuildingSchedules
from jistdocstore.model.userfile import JistEstimating3yrBuildingHeadings
from jistdocstore.model.userfile import JistEstimating3yrBuildingSubHeadings
from jistdocstore.model.userfile import JistEstimating3yrBuildingItems
from jistdocstore.model.userfile import JistEstimating3yrBuildingSites
from jistdocstore.model.userfile import JistEstimating3yrBuildingSiteSOW
from jistdocstore.model.userfile import JistEstimating3yrBuildingSOWBQItems
from jistdocstore.model.userfile import JistEstimating3yrBuildingStatusCodes
from jistdocstore.model.userfile import JistEstimating3yrBuildingStatusData
from jistdocstore.model.userfile import JistEstimating3yrBuildingQuotes
from jistdocstore.model.userfile import JistEstimating3yrBuildingQuoteScope
from jistdocstore.model.userfile import JistEstimating3yrBuildingQuoteBQItems
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingItems
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingSites
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingSiteSOW
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingSOWBQItems
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingQuotes
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingQuoteScope
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingQuoteBQItems
from jistdocstore.model.userfile import JistEstimating5yrEskomFencingPhotos

from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeItems
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeSites
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeSiteSOW
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeSOWBQItems
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeQuotes
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeQuoteScope
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeQuoteBQItems
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeJCNOEstLink
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeSiteRequirements
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeStandardMaterialList
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadePhotos
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeStoresReceiveList
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeStoresDespatchList
from jistdocstore.model.userfile import JistEstimating3yrEssPalisadeStoresReturnList


from jistdocstore.model.userfile import JistEstimating3yrEssHSFItems
from jistdocstore.model.userfile import JistEstimating3yrEssHSFSites
from jistdocstore.model.userfile import JistEstimating3yrEssHSFSiteSOW
from jistdocstore.model.userfile import JistEstimating3yrEssHSFSOWBQItems
from jistdocstore.model.userfile import JistEstimating3yrEssHSFQuotes
from jistdocstore.model.userfile import JistEstimating3yrEssHSFQuoteScope
from jistdocstore.model.userfile import JistEstimating3yrEssHSFQuoteBQItems
from jistdocstore.model.userfile import JistEstimating3yrEssHSFPhotos

from jistdocstore.model.userfile import JistManufactureClients
from jistdocstore.model.userfile import JistManufactureOrderItems
from jistdocstore.model.userfile import JistManufacturingStages
from jistdocstore.model.userfile import JistManufacturingWorkFlow
from jistdocstore.model.userfile import JistManufactureStandardList
from jistdocstore.model.userfile import JistManufactureStandardListItems
from jistdocstore.model.userfile import JistManufactureNonStandardList
from jistdocstore.model.userfile import JistManufactureAngleEqualData
from jistdocstore.model.userfile import JistManufactureAngleNonEqualData
from jistdocstore.model.userfile import JistManufactureIPEData
from jistdocstore.model.userfile import JistManufactureFlatsData

from jistdocstore.model.userfile import ServerHit 
#from jistdocstore.model.jistdb import JistStories
#from jistdocstore.model.collections import  LabourTeam
#from jistdocstore.model.collections import  LabourMember
