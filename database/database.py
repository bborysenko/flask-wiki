from mongodb.mongodb import MongoDB
from postgresql.postgresql import Postgresql


def get_database_object(name, host, port, database):
    if name == 'mongodb':
        obj = MongoDB(host, port, database)
        return obj
    else:
        obj = Postgresql()
        return obj
