from mongodb.mongodb import MongoDB
from postgresql.postgresql import Postgresql

def get_database_object( name = None ):
    if name == 'mongodb':
        obj = MongoDB()
        return obj
    else:
        obj = Postgresql()
        return obj

