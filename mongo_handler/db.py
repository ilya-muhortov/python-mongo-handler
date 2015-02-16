
from pymongo import MongoClient
from sqlalchemy import create_engine


DEFAULT_DB_ALIAS = 'default'


class ConnectionHandler(object):

    def __init__(self, databases):
        self._databases = databases
        self._connections = dict()

    @property
    def databases(self):
        if DEFAULT_DB_ALIAS not in self._databases:
            raise Exception("You must define a '%s' database" % DEFAULT_DB_ALIAS)

        return self._databases

    @property
    def default(self):
        return self[DEFAULT_DB_ALIAS]

    def connect(self, conn_string):
        raise NotImplementedError

    def __getitem__(self, alias):
        if alias not in self._connections:
            try:
                conn_string = self.databases[alias]
            except KeyError:
                raise Exception("The connection %s doesn't exist" % alias)

            self._connections[alias] = self.connect(conn_string)

        return self._connections[alias]


class MongoHandler(ConnectionHandler):

    def connect(self, conn_string):
        try:
            return MongoClient(conn_string)
        except Exception as e:
            raise Exception(e)


class SQLAlchemyHandler(ConnectionHandler):

    def connect(self, conn_string):
        try:
            engine = create_engine(conn_string)
            return engine.connect()
        except Exception as e:
            raise Exception(e)