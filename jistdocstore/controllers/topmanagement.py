# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group,has_any_permission, Any, is_user
from tg.decorators import paginate
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider

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

__all__ = ['TopManagementController']


class TopManagementController(BaseController):
    """Sample controller-wide authorization"""
    
    # The predicate that must be met for all the actions in this controller:
    allow_only = has_permission('manage',
                                msg=l_('Only for people with the "manage" permission'))

    @require(in_any_group("managers", "production","marketing","healthsafety","logistics","stores","estimates"))
    @expose()
    def index(self):
        redirect('topmngntcont/menu')

    @expose('jistdocstore.templates.topmanagement')
    def menu(self):
        #flash(_("Secure Controller here"))
        return dict(page='refreshpage') 
    
    @expose('jistdocstore.templates.managepoints')
    def managepoints(self,usrid=0,**kw):
        """Handle the 'managepoints' page."""
        if not usrid:
            usrid = '1'
        wip = DBS_ContractData.query(JistContracts).join(JistContractStatus). \
                filter(JistContracts.completed=='False'). \
                filter(JistContractStatus.pointperson==usrid). \
                all()
        wip1 = []
        tmpl_context.widget = status_point_changer 
        for w in wip:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==w.jno).one()
            statcode  = DBS_ContractData.query(JistContractStatusCodes).filter(JistContractStatusCodes.id==statusall.statuscode).one()
            wip1.append({'jno':w.jno,
                         'client':w.client,
                         'site':w.site,
                         'description':w.description,
                         'status':statcode.status,
                         'pointperson':statusall.pointperson
                         })
        
        count = len(wip1) 
        page =int( kw.get( 'page', '1' ))
        currentPage = paginate.Page(
            wip1, page, item_count=count,
            items_per_page=15,
        )
        items = currentPage.items
        return dict(page='managepoints',
                    wip = items,
                    thiscurrentPage=currentPage,
                    point = usrid,
                    count=count)

    @expose()
    def getmanagedpoints(self,*args,**kw):
        if not kw['point']:
            point = 1
        else:
            point = kw['point']
        redirect('/topmngntcont/managepoints/'+str(point))
    
    @expose()
    def exportsinglepointpdf(self,point):
        import random
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        fname = str(datetime.now()).split(' ')[0] + rnd +'.pdf'
        filename = os.path.join(pdf_dirname, str(fname))
        #print filename
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
                filter(JistContractStatus.pointperson==point). \
                all()
        wip1 = []
        for w in wip:
            statusall = DBS_ContractData.query(JistContractStatus).filter(JistContractStatus.jno==w.jno).one()
            try:
                conplandates = DBS_ContractData.query(JistContractPlanningDates). \
                            filter(JistContractPlanningDates.jcno==w.jno).one()
                #print type(conplandates)
                #print conplandates.planstartdate
                #planstart = str(conplandates.planstartdate).split(' ')[0]
                #planend = str(conplandates.planenddate).split(' ')[0],
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
                         'pointperson':statusall.pointperson
                         })
        
        count = len(wip1) 
        pointperson_name = User.by_user_id(point).user_name
        userdata.append([datetime.date(datetime.now()),
                        "Point Contracts For %s"%pointperson_name,
                        ""
                        ])
        headers =["JCNo","Client","Site","Description","Plan Start","Plan End","Status"]
        headerwidths=[40,120,200,200,60,60,80]
        pdffile.CreatePDFPointContracts(userdata,wip1,headers,headerwidths)
        response.headers["Content-Type"] = 'application/pdf'
        response.headers["Content-Disposition"] = 'attachment; filename="'+fname+'"'
        filecontent = file(filename, "r")
        return filecontent
        #redirect('/topmngntcont/managepoints/'+str(point))
        #print "Got Here again"
