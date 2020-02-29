# -*- coding: utf-8 -*-

"""Setup the rocket application"""

from __future__ import print_function

import os
import traceback
import transaction

from datetime import datetime
from pkg_resources import resource_filename

from rocket import model
from rocket.lib.type_utils import RawTypeDictionary

from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, MetaData, Table

def create_app_folders():

    try:
        APPROOT = os.getcwd()
        FILENAME = os.path.abspath(resource_filename('rocket', 'public'))
        CODE_ROOT = os.path.join(APPROOT, "rocket")

        LOGS_DIRNAME = os.path.join(APPROOT, 'logs')
        if not os.path.exists(LOGS_DIRNAME): os.mkdir(LOGS_DIRNAME)

        MIGRATION_DIRNAME = os.path.join(APPROOT, 'migration')
        if not os.path.exists(MIGRATION_DIRNAME): os.mkdir(MIGRATION_DIRNAME)

        VERSIONS_DIRNAME = os.path.join(MIGRATION_DIRNAME, 'versions')
        if not os.path.exists(VERSIONS_DIRNAME): os.mkdir(VERSIONS_DIRNAME)

        PUBLIC_DIRNAME = os.path.join(CODE_ROOT, "public")
        if not os.path.exists(PUBLIC_DIRNAME): os.mkdir(PUBLIC_DIRNAME)

        CSV_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'csv')
        if not os.path.exists(CSV_DIRNAME): os.mkdir(CSV_DIRNAME)

        EXCEL_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'excel')
        if not os.path.exists(EXCEL_DIRNAME): os.mkdir(EXCEL_DIRNAME)

        PAYMENTS_DIRNAME = os.path.join(CSV_DIRNAME, 'payments')
        if not os.path.exists(PAYMENTS_DIRNAME): os.mkdir(PAYMENTS_DIRNAME)

        PDF_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'pdf')
        if not os.path.exists(PDF_DIRNAME): os.mkdir(PDF_DIRNAME)

        EXCEL_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'excel')
        if not os.path.exists(PDF_DIRNAME): os.mkdir(EXCEL_DIRNAME)

        UPLOADS_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'uploads')
        if not os.path.exists(UPLOADS_DIRNAME): os.mkdir(UPLOADS_DIRNAME)

        IMAGES_DIRNAME = os.path.join(PUBLIC_DIRNAME, 'images')
        if not os.path.exists(IMAGES_DIRNAME): os.mkdir(IMAGES_DIRNAME)

        STAFFPIC_DIRNAME = os.path.join(IMAGES_DIRNAME, 'staff_pictures')
        if not os.path.exists(STAFFPIC_DIRNAME): os.mkdir(STAFFPIC_DIRNAME)

        CATALOG_DIRNAME = os.path.join(IMAGES_DIRNAME, 'catalog_pictures')
        if not os.path.exists(CATALOG_DIRNAME): os.mkdir(CATALOG_DIRNAME)
    except Exception as e:
        print("There was a problem adding the folders.  Exception: {0} ".format(e))

create_app_folders()
def bootstrap(command, conf, vars):

##################################################################################################################
#   AUTHENTICATION
##################################################################################################################
    timestart = datetime.now()
    try:

        u, u1 = None, None

        FIRST = 'Developer'
        devexists = model.DBSession.query(model.User). \
                filter(model.User.username==FIRST). \
                first()
        if not devexists:
            u = model.User()
            u.username = FIRST
            u.name = FIRST
            u.email = 'developer@dotxmltech.com'
            u.password = 'developpass'
            u.expires = datetime.now()
            u.added_by = 1
            model.DBSession.add(u)
            print(f'Adding USER: {FIRST}')
        else:
            u = devexists

        SECOND = 'User'
        userexists = model.DBSession.query(model.User). \
                filter(model.User.username==SECOND). \
                first()
        if not userexists:
            u1 = model.User()
            u1.username = SECOND
            u1.name = SECOND
            u1.email = 'user@dotxmltech.com'
            u1.password = 'userpass'
            u1.expires = datetime.now()
            u1.added_by = 1
            model.DBSession.add(u1)
            print(f'Adding USER: {SECOND}')
        else:
            u1 = userexists

        model.DBSession.flush()
        transaction.commit()

        devrolexists = model.DBSession.query(model.Role). \
                filter(model.Role.name==FIRST). \
                first()
        if not devrolexists:
            dev_g = model.Role()
            dev_g.name = FIRST
            dev_g.users.append(u)
            model.DBSession.add(dev_g)
            print(f'Adding ROLES: {FIRST}')

            dev_p = model.Permission()
            dev_p.name = FIRST
            dev_p.description = f'Permission for {FIRST} Access'
            dev_p.roles.append(dev_g)
            model.DBSession.add(dev_p)

            model.DBSession.flush()
            transaction.commit()

    except IntegrityError:
        print('Warning, there was a problem adding your auth data, it may have already been added: ')

        print(traceback.format_exc())
        transaction.abort()
        print('Continuing with bootstrapping...')
    timeend = datetime.now()
##################################################################################################################
#  ROLES
##################################################################################################################

    timestart_roles = datetime.now()
    role_list = [
            'Sales',
            'Administrator',
            'Business Process',
            'Catalog Maintenance',
            'Claims Approval',
            'Claims Management',
            'Claims Registration',
            'Contact Centre',
            'Financial Reports',
            'Membership',
            'Product Setup',
            'Statistical Reports',
            'Users And Access',
            ]
    try:
        for new_role in role_list:

            exists = model.DBSession.query(model.Role). \
                    filter(model.Role.name==new_role). \
                    first()

            if not exists:
                print('Adding ROLES: {0}'.format(new_role))
                role = model.Role()
                role.name = new_role
                role.users.append(u)
                role.users.append(u1)
                model.DBSession.add(role)

                perm = model.Permission()
                perm.name = new_role
                perm.description = 'Permission for {0} Access'.format(new_role.capitalize())
                perm.roles.append(role)
                model.DBSession.add(perm)

                model.DBSession.flush()
                transaction.commit()
    except IntegrityError:
        print ("Warning, there was a problem adding LIST OF ROLES, it may have already been added: ")

        print( traceback.format_exc())
        transaction.abort()
        print ('Continuing with bootstrapping...')

    dotxml_userlist = [
        {'username' : 'deonbez', 'name' : 'Deon Bezuidenhout', 'email' : 'deon@dotxmltech.com'},
        {'username' : 'lucasgrey', 'name' : 'Lucas Greyling', 'email' : 'lucas@dotxmltech.com'},
        {'username' : 'jpbez', 'name' : 'JP Bezuidenhout', 'email' : 'jp@dotxmltech.com'},
        {'username' : 'trevjou', 'name' : 'Trevor Joubert', 'email' : 'trevor@dotxmltech.com'},
        {'username' : 'tjaart_rocket', 'name' : 'Tjaart Swanepoel', 'email' : 'tjaart@dotxmltech.com'},
        {'username' : 'hans', 'name' : 'Hannes Toerien', 'email' : 'hannes@dotxmltech.com'},
        {'username' : 'camilla007', 'name' : 'Camilla Buys', 'email' : 'camilla@dotxmltech.com'},
            ]

    timeend_roles = datetime.now()

##################################################################################################################
#  TEXT MERGE
##################################################################################################################

    mergelist = [
            {'code' : 'policy_number', 'name' : 'Policy Number'},
            {'code' : 'customer_name', 'name' : 'Customer Name'},
            {'code' : 'cover_type', 'name' : 'Cover Type'},
            {'code' : 'life_assured_type', 'name' : 'Life Assured Type'},
            {'code' : 'description', 'name' : 'Product Description'},
            {'code' : 'price', 'name' : 'Product Price'},
            {'code' : 'sum_assured', 'name' : 'Sum Assured'},
            {'code' : 'currency', 'name' : 'Currency'},
            {'code' : 'start_date', 'name' : 'Start Date'},
            {'code' : 'waiting_period', 'name' : 'Waiting Period'},
            {'code' : 'active_period', 'name' : 'Active Period'},
            {'code' : 'end_date', 'name' : 'End Date'},
            {'code' : 'benefits', 'name' : 'Benefits'},
            ]
    try:
        for merge in mergelist:
            name = merge.get('name')
            code = merge.get('code')
            exists = model.DBSession.query(model.MailMerge). \
                filter(model.MailMerge.name == name). \
                first()
            if not exists:
                merge = model.MailMerge()
                merge.name = name
                merge.code = code
                merge.added_by = 1
                model.DBSession.add(merge)
                model.DBSession.flush()
                transaction.commit()
    except IntegrityError:
        print ("Warning, there was a problem adding LIST OF MailMerge, it may have already been added:")
        import traceback
        print( traceback.format_exc())
        transaction.abort()
        print ('Continuing with bootstrapping...')

##################################################################################################################
#  TYPES
##################################################################################################################


    from rocket.lib.type_utils import create_type_tables
    timestart_types = datetime.now()

    dict_of_types = RawTypeDictionary().raw_dictionary_of_types
    create_type_tables(DBSession=model.DBSession, dict_of_types=dict_of_types)

    from rocket.lib.type_utils import TypeDictionary as TypeDict
    from rocket.lib.type_utils import create_cover_link_tables
    coverlist = TypeDict().get_dict_of_types('cover_and_exclusion_type')
    create_cover_link_tables(DBSession=model.DBSession, dictlist=coverlist)

    #import rocket.public.csv.test_member_import
    timeend_types = datetime.now()

##################################################################################################################
#  ISO Utils
##################################################################################################################

    timestart_iso = datetime.now()
    from rocket.lib.iso_utils import create_currencies, create_languages, create_countries
    create_currencies(model.DBSession)
    create_languages(model.DBSession)
    create_countries(model.DBSession)
    timeend_iso = datetime.now()

##################################################################################################################
#  Output
##################################################################################################################

    print(f"Total Time Normal Bootstraps: {timeend-timestart}")
    print(f"Total Time Roles: {timeend_roles-timestart_roles}")
    print(f"Total Time Types: {timeend_types-timestart_types}")
    print(f"Total Time ISO: {timeend_iso-timestart_iso}")
    print(f"Total Time All Bootstrap: {timeend_iso-timestart}")
