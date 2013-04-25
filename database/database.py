#from mongodb.mongodb import MongoDB
from postgresql.postgresql import Postgresql

from flask import current_app

def get_database_object(name, *args):
    if name == 'mongodb':
#        obj = MongoDB(host, port, database)
#        return obj
        pass
    else:
        obj = Postgresql()
        return obj
