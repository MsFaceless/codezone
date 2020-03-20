# -*- coding: utf-8 -*-
"""Setup the jistdocstore application"""
from __future__ import print_function

import logging
from tg import config
from jistdocstore import model
import transaction

def bootstrap(command, conf, vars):
    """Place any commands to setup jistdocstore here"""

    # <websetup.bootstrap.before.auth
    from sqlalchemy.exc import IntegrityError
    try:
        u = model.User()
        u.user_name = 'manager'
        u.display_name = 'Example manager'
        u.email_address = 'manager@somedomain.com'
        u.password = 'managepass'
    
        model.DBS_ContractData.add(u)
    
        g = model.Group()
        g.group_name = 'managers'
        g.display_name = 'Managers Group'
    
        g.users.append(u)
    
        model.DBS_ContractData.add(g)
    
        p = model.Permission()
        p.permission_name = 'manage'
        p.description = 'This permission give an administrative right to the bearer'
        p.groups.append(g)
    
        model.DBS_ContractData.add(p)
    
        u1 = model.User()
        u1.user_name = 'editor'
        u1.display_name = 'Example editor'
        u1.email_address = 'editor@somedomain.com'
        u1.password = 'editpass'
    
        model.DBS_ContractData.add(u1)
        model.DBS_ContractData.flush()
        transaction.commit()
    except IntegrityError:
        print('Warning, there was a problem adding your auth data, it may have already been added:')
        import traceback
        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')

    try:
        manstages = ['Not Started', 'Specification', 'Drawings','Mat Req','Mat Lead Time','Planning',
                  'Cutting', 'Bending','Milling','Drilling','Punching',
                  'Welding','Assembly','Grinding','Outsource Assembly','Cleaning','Pre-Coating Insp',
                  'Galvanising','Epoxy Coating','Zinc Coating','Painting','Outsource Coating','Touch Up',
                  'Quality Insp','Packing','Stores','Despatch','Completed'
                  ]
        for stage in manstages: 
            x = model.JistManufacturingStages()
            x.name = stage 
            x.useridnew = 2 
            x.useridedited = 2 
            model.DBS_JistManufacturing.add(x)
            model.DBS_JistManufacturing.flush()
            transaction.commit()
    except IntegrityError:
        print ("Warning, there was a problem adding Manufacturing Stages, it may have already been added:")
        import traceback
        print( traceback.format_exc())
        transaction.abort()
        print ('Continuing with bootstrapping...')
        
    # <websetup.bootstrap.after.auth>
