# -*- coding: utf-8 -*-
"""
Global configuration file for TG2-specific settings in jistdocstore.

This file complements development/deployment.ini.

Please note that **all the argument values are strings**. If you want to
convert them into boolean, for example, you should use the
:func:`paste.deploy.converters.asbool` function, as in::
    
    from paste.deploy.converters import asbool
    setting = asbool(global_conf.get('the_setting'))
 
"""

from tg.configuration import AppConfig, config
#from pylons import config as pylons_config
from jistdocstore.model import init_model
import jistdocstore
from jistdocstore import model
from jistdocstore.lib import app_globals, helpers 

class MultiDBAppConfig(AppConfig):
    def setup_sqlalchemy(self):
        #print "Got It"
        from sqlalchemy import engine_from_config
        """Setup SQLAlchemy database engine(s)"""
        engine1 = engine_from_config(config, 'sqlalchemy.first.')
        engine2 = engine_from_config(config, 'sqlalchemy.second.')
        engine3 = engine_from_config(config, 'sqlalchemy.third.')
        engine4 = engine_from_config(config, 'sqlalchemy.fourth.')
        engine5 = engine_from_config(config, 'sqlalchemy.fifth.')
        engine6 = engine_from_config(config, 'sqlalchemy.six.')
        engine7 = engine_from_config(config, 'sqlalchemy.seven.')
        engine8 = engine_from_config(config, 'sqlalchemy.eight.')
        engine9 = engine_from_config(config, 'sqlalchemy.nine.')
        engine10 = engine_from_config(config, 'sqlalchemy.ten.')
        engine11 = engine_from_config(config, 'sqlalchemy.eleven.')
        engine12 = engine_from_config(config, 'sqlalchemy.twelve.')
        engine13 = engine_from_config(config, 'sqlalchemy.thirteen.')
        # engine1 should be assigned to sa_engine as well as your first engine's name
        config['tg.app_globals'].sa_engine = engine1
        config['tg.app_globals'].sa_engine_first = engine1
        config['tg.app_globals'].sa_engine_second = engine2
        config['tg.app_globals'].sa_engine_third = engine3
        config['tg.app_globals'].sa_engine_fourth = engine4
        config['tg.app_globals'].sa_engine_fifth = engine5
        config['tg.app_globals'].sa_engine_seven = engine7
        config['tg.app_globals'].sa_engine_eight = engine8
        config['tg.app_globals'].sa_engine_nine = engine9
        config['tg.app_globals'].sa_engine_six = engine6
        #config['tg.app_globals'].sa_engine_second = engine7
        #config['tg.app_globals'].sa_engine_second = engine9
        config['tg.app_globals'].sa_engine_ten = engine10
        config['tg.app_globals'].sa_engine_eleven = engine11
        config['tg.app_globals'].sa_engine_twelve = engine12
        config['tg.app_globals'].sa_engine_thirteen = engine13
        # Pass the engines to init_model, to be able to introspect tables
        init_model(engine1,engine2,engine3,engine4,engine5,engine6,engine7,engine8,engine9,engine10,engine11,engine12,engine13)


base_config = MultiDBAppConfig()
#base_config = AppConfig()
base_config.renderers = []
base_config.prefer_toscawidgets2 = True

base_config.package = jistdocstore

from tgext.pluggable import plug

#Enable json in expose
base_config.renderers.append('json')
#Enable genshi in expose to have a lingua franca for extensions and pluggable apps
#you can remove this if you don't plan to use it.
base_config.renderers.append('genshi')

#Set the default renderer
base_config.default_renderer = 'genshi'
# if you want raw speed and have installed chameleon.genshi
# you should try to use this renderer instead.
# warning: for the moment chameleon does not handle i18n translations
#base_config.renderers.append('chameleon_genshi')
#Configure the base SQLALchemy Setup
base_config.use_sqlalchemy = True
base_config.model = jistdocstore.model
base_config.DBSession = jistdocstore.model.DBS_ContractData
# Configure the authentication backend

# YOU MUST CHANGE THIS VALUE IN PRODUCTION TO SECURE YOUR APP 
base_config.sa_auth.cookie_secret = "544038ec-7cda-4952-bc7f-5c6240141c84"

base_config.auth_backend = 'sqlalchemy'

# what is the class you want to use to search for users in the database
base_config.sa_auth.user_class = model.User

from tg.configuration.auth import TGAuthMetadata

#This tells to TurboGears how to retrieve the data for your user
class ApplicationAuthMetadata(TGAuthMetadata):
    def __init__(self, sa_auth):
        self.sa_auth = sa_auth
    def authenticate(self, environ, identity):
        #print "Auth Run"
        user = self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(user_name=identity['login']).first()
        #print user
        #print identity
        #print user.validate_password(identity['password'])
        if user and user.validate_password(identity['password']):
            return identity['login']
    def get_user(self, identity, userid):
        return self.sa_auth.dbsession.query(self.sa_auth.user_class).filter_by(user_name=userid).first()
    def get_groups(self, identity, userid):
        return [g.group_name for g in identity['user'].groups]
    def get_permissions(self, identity, userid):
        return [p.permission_name for p in identity['user'].permissions]

base_config.sa_auth.dbsession = model.DBS_ContractData

base_config.sa_auth.authmetadata = ApplicationAuthMetadata(base_config.sa_auth)

# You can use a different repoze.who Authenticator if you want to
# change the way users can login
#base_config.sa_auth.authenticators = [('myauth', SomeAuthenticator()]

# You can add more repoze.who metadata providers to fetch
# user metadata.
# Remember to set base_config.sa_auth.authmetadata to None
# to disable authmetadata and use only your own metadata providers
#base_config.sa_auth.mdproviders = [('myprovider', SomeMDProvider()]

# override this if you would like to provide a different who plugin for
# managing login and logout of your application
base_config.sa_auth.form_plugin = None

# override this if you are using a different charset for the login form
#base_config.sa_auth.charset = 'utf-8'

# You may optionally define a page where you want users to be redirected to
# on login:
base_config.sa_auth.post_login_url = '/post_login'

# You may optionally define a page where you want users to be redirected to
# on logout:
base_config.sa_auth.post_logout_url = '/post_logout'

#plug(base_config,'tgext.debugbar')
