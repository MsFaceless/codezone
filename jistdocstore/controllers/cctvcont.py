# -*- coding: utf-8 -*-
"""Sample controller with all its actions protected."""
from tg import expose, flash, require, url, request, redirect, response,tmpl_context,validate
from tg.i18n import ugettext as _, lazy_ugettext as l_
from tg.predicates import has_permission, in_any_group
from tg.decorators import paginate
#from dbsprockets.dbmechanic.frameworks.tg2 import DBMechanic
#from dbsprockets.saprovider import SAProvider
#from tgext.ajaxforms import ajaxloaded, ajaxform

from jistdocstore.lib.base import BaseController
from jistdocstore.lib.jistdocstorereportlab import *
#from jistdocstore.model import DBSession, metadata
#from jistdocstore.controllers.tablecont import * 

from jistdocstore.model.userfile import JistFileStoreMarketing
from jistdocstore.model import * 
from pkg_resources import resource_filename
import subprocess
import os
#from jistdocstore.controllers.widgets import *

#import tw.forms as twf
#from tw.forms.fields import TextField, TextArea, CheckBox
#from tw.api import *
#from tw.api import WidgetsList
#from tw.extjs import ItemSelector
#from tw.forms import FileField, TableForm, TextField, CalendarDatePicker, SingleSelectField, TextArea
#from tw.forms.validators import Int, NotEmpty,DateTimeConverter, DateConverter
#from tw.forms.validators import * 
from formencode import Schema
from formencode import validators
from formencode.validators import FieldsMatch
from formencode.validators import Int, NotEmpty, DateConverter,DateValidator,PostalCode,String,Email,UnicodeString
from formencode.validators import *

import random
from babel.numbers import format_currency, format_number, format_decimal

public_dirname = os.path.join(os.path.abspath(resource_filename('jistdocstore', 'public')))
pics_dirname = os.path.join(public_dirname, 'production_pictures')
pdf_dirname = os.path.join(public_dirname, 'pdf')

__all__ = ['CCTVController']

camsvivotek = ['192.168.0.64',]
camsaxis = ['192.168.0.96',]
camsmobotix = [
                      'jisttrading.no-ip.org:10091',
                      'jisttrading.no-ip.org:10097',
                      'jisttrading.no-ip.org:10096',
                      'jisttrading.no-ip.org:10095',
                      'jisttrading.no-ip.org:10100',
                      'jisttrading.no-ip.org:10090',
                      'jisttrading.no-ip.org:10094',
                      'jisttrading.no-ip.org:10106',
                      'jisttrading.no-ip.org:10104',
                      'jisttrading.no-ip.org:10102',
                      'jisttrading.no-ip.org:10103',
                      'jisttrading.no-ip.org:10105',
            ]
camsjistfamily = [
               'jistfamily.dyndns.org:10100',
               'jistfamily.dyndns.org:10101',
               'jistfamily.dyndns.org:10090',
               'jistfamily.dyndns.org:10091',
               'jistfamily.dyndns.org:10092',
               'jistfamily.dyndns.org:10093',
               'jistfamily.dyndns.org:10094',
               'jistfamily.dyndns.org:10095',
               'jistfamily.dyndns.org:10097',
               'jistfamily.dyndns.org:10099',
               'jistfamily.dyndns.org:10102',
               'jistfamily.dyndns.org:10103',
            ]

class CCTVController(BaseController):
    """
    allow_only = Any(
            has_permission('manage'),
            has_permission('marketingmanage'),
            has_permission('marketing'),
                     msg=l_('Only for people with the "marketing" permission')
                     )

    """
    @expose('jistdocstore.templates.cctv.cctvindex')
    def index(self):
        return dict(page="Index",form=test_form)

    @expose('jistdocstore.templates.cctv.cctvindex')
    def menu(self):
        cam1 = camsmobotix[0]
        cam1_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam1 
        cams = self.setup5camtopbar()
        return dict(page='Camera Views',
                    cam1 = cam1_stream_src, 
                    cam2 = cams[0],
                    cam3 = cams[1],
                    cam4 = cams[2],
                    cam5 = cams[3],
                    cam6 = cams[4],
                    selfname="getfastframe"
                )

    @expose('jistdocstore.templates.cctv.cctvgridviewresponsive')
    def cctvgridviewresponsive(self):
        return dict(page="CCTV Grid View Responsive")

    @expose('jistdocstore.templates.cctv.cctvcarousel')
    def cctvcarousel(self):
        return dict(page="CCTV Carousel")

    @expose('jistdocstore.templates.cctv.cctvinternalcams_grid')
    def cctvinternalcams_grid(self):
        return dict(page="CCTV Grid View")

    @expose('jistdocstore.templates.cctv.cctvinternalcams_carousel')
    def cctvinternalcams_carousel(self):
        return dict(page="CCTV Carousel")

    @expose()
    #@validate(test_form, error_handler=form_show)
    def form_submit(self, **kw):
        return 'Thanks: {name} {surname}'.format(**kw)

    @expose('jistdocstore.templates.cctv.jistcams_single')
    def view_single_cam_jist(self, **kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        imgtag = "<img class='cctv_img_small' src="
        httptag = "http://admin:m0bx2@"
        iptag = "jisttrading.no-ip.org:10091"
        cgitag = "/cgi-bin/faststream.jpg?"
        pic_cgi = "/cgi-bin/image.jpg?size=100x75&quality=60"
        #imgsrc = imgtag + httptag + iptag + cgitag + params
        html1 = ''
        camimglist = []
        for cam in camsmobotix:
            rnd = random.random()
            rnd = str(rnd).split('.')[1]
            iptag = cam 
            params = "stream=full&amp;fps=1.0&amp;error=picture&amp;dummy="+str(rnd)
            valuetag = httptag + iptag + cgitag + params 
            imgsrc = httptag + iptag + pic_cgi
            camimglist.append({'src':imgsrc,
                               'value':httptag+iptag+cgitag})

        return dict(page='Single Camera View',
                    camimg_srclist = camimglist)

    @expose('jistdocstore.templates.cctv.jistcams_single')
    def view_single_cam_jistfamily_home(self, **kw):
        #for k, w in kw.iteritems():
        #    print k, w
        #return
        imgtag = "<img class='cctv_img_small' src="
        httptag = "http://admin:mobx1@"
        iptag = "jistfamily.dyndns.org:10090"
        cgitag = "/cgi-bin/faststream.jpg?"
        pic_cgi = "/cgi-bin/image.jpg?size=100x75&quality=60"
        #imgsrc = imgtag + httptag + iptag + cgitag + params
        html1 = ''
        camimglist = []
        for cam in camsjistfamily:
            rnd = random.random()
            rnd = str(rnd).split('.')[1]
            iptag = cam 
            params = "stream=full&amp;fps=1.0&amp;error=picture&amp;dummy="+str(rnd)
            valuetag = httptag + iptag + cgitag + params 
            imgsrc = httptag + iptag + pic_cgi
            camimglist.append({'src':imgsrc,
                               'value':httptag+iptag+cgitag})

        return dict(page='JIST Family Home Camera View',
                    camimg_srclist = camimglist)


    @expose()
    def view_single_cam_jist_ajax(self, **kw):
        #for k, w in kw.iteritems():
            #print k, w
        rnd = random.random()
        rnd = str(rnd).split('.')[1]
        src = kw['src']
        imgtag = "<img class='cctv_main' src="+src
        #httptag = "http://admin:m0bx2@"
        #iptag = "jisttrading.no-ip.org:10091"
        cgitag = "/cgi-bin/faststream.jpg?"
        #pic_cgi = "/cgi-bin/image.jpg?size=100x75&quality=60"
        #imgsrc = imgtag + httptag + iptag + cgitag + params
        params = "stream=full&amp;fps=1.0&amp;error=picture&amp;dummy="+str(rnd)
        html = imgtag + cgitag + params + '/>' 
        return html 

    @expose()
    def indexold(self):
        redirect('cctvcont/menu')


    @expose('jistdocstore.templates.cctv.camconnected')
    def view_connect_came_dir(self,**named):
        """Handle the 'cam connected' page."""
        from tg.decorators import paginate
        return dict(selfname='view_connected_came_dir',
                    src = '192.168.0.11:8080',
                    page = 'View Connected Server Directory',
                    )

    @expose('jistdocstore.templates.cctv.viewaxiscam')
    @require(in_any_group("managers", ))
    def viewaxiscam(self):
        cam1 = camsaxis[0]
        cam1_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam1 
        cams = self.setup5camtopbar()
        return dict(page='Axis Camera View',
                    cam1 = cam1_stream_src, 
                    cam2 = cams[0],
                    cam3 = cams[1],
                    cam4 = cams[2],
                    cam5 = cams[3],
                    cam6 = cams[4],
                    selfname="viewaxiscam"
                )

    @expose('jistdocstore.templates.cctv.viewvivotekcam')
    @require(in_any_group("managers", ))
    def viewvivotekcam(self):
        cam1 = camsvivotek[0]
        cam1_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam1 
        cams = self.setup5camtopbar()
        return dict(page='Vivotek Camera View',
                    cam1 = cam1_stream_src, 
                    cam2 = cams[0],
                    cam3 = cams[1],
                    cam4 = cams[2],
                    cam5 = cams[3],
                    cam6 = cams[4],
                    selfname="viewvivotekcam"
                )

    @expose('jistdocstore.templates.cctv.fastframe')
    @require(in_any_group("managers", ))
    def getfastframe(self):
        cam1 = camsmobotix[0]
        cam1_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam1 
        cams = self.setup5camtopbar()
        return dict(page='Mobotix Camera View',
                    cam1 = cam1_stream_src, 
                    cam2 = cams[0],
                    cam3 = cams[1],
                    cam4 = cams[2],
                    cam5 = cams[3],
                    cam6 = cams[4],
                    selfname="getfastframe"
                )


    @expose('jistdocstore.templates.cctv.getanycam')
    @require(in_any_group("managers", ))
    def getanycam(self,thiscamip=None,cambrand=None):
        if not thiscamip:
            cam1 = camsmobotix[0]
            cam1_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam1 
        else:
            cam1 = thiscamip
            if cambrand == "mob":
                cam1_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam1 
            elif cambrand == "axi":
                cam1_stream_src="http://%s/axis-cgi/mjpg/video.cgi?"%cam1 
            elif cambrand == "viv":
                cam1_stream_src="http://%s/video.mjpg"%cam1 
            else:
                pass

        cams = self.setup5camtopbar()
        return dict(page='Mobotix,Axis,Vivotek Camera View',
                    cam1 = cam1_stream_src, 
                    cam2 = cams[0],
                    cam3 = cams[1],
                    cam4 = cams[2],
                    cam5 = cams[3],
                    cam6 = cams[4],
                    selfname="getanycam"
                )
    expose()
    def setup5sidebarbar(self):
        cam2 = camsmobotix[1]
        cam2_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam2 
        cam3 = camsmobotix[2]
        cam3_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam3 
        cam4 = camsmobotix[3]
        cam4_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam4 
        cam5 = camsaxis[0]
        cam5_stream_src="http://%s/axis-cgi/mjpg/video.cgi?"%cam5 
        cam6 = camsvivotek[0]
        cam6_stream_src="http://%s/video.mjpg"%cam6 
        return(cam2_stream_src,cam3_stream_src,cam4_stream_src,cam5_stream_src,cam6_stream_src)

    expose()
    def setup5camtopbar(self):
        cam2 = camsmobotix[1]
        cam2_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam2 
        cam3 = camsmobotix[2]
        cam3_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam3 
        cam4 = camsmobotix[3]
        cam4_stream_src="http://%s/control/faststream.jpg?stream=full&amp;fps=10.0&amp;dummy=1804289385"%cam4 
        cam5 = camsaxis[0]
        cam5_stream_src="http://%s/axis-cgi/mjpg/video.cgi?"%cam5 
        cam6 = camsvivotek[0]
        cam6_stream_src="http://%s/video.mjpg"%cam6 
        return(cam2_stream_src,cam3_stream_src,cam4_stream_src,cam5_stream_src,cam6_stream_src)
