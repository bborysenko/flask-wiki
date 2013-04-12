#from mongodb.mongodb import MongoDB
from postgresql.postgresql import Postgresql

from flask import current_app
from appwiki.conf import *

def get_database_object( name ):
    if name == 'mongodb':
#        obj = MongoDB(host, port, database)
#        return obj
        pass
    else:
        current_app.config['SQLALCHEMY_BINDS'] = {
            'psql' : 'postgresql://' + USER + ':' + PASSWORD + '@' + HOST + '/' + DATABASE
        }
        obj = Postgresql()
        return obj
