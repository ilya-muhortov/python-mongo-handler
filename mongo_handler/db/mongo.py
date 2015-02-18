
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, InvalidURI

from mongo_handler.db import ConnectionHandler
from mongo_handler import HandlerException


class MongoHandler(ConnectionHandler):

    def connect(self, conn_string):
        try:
            return MongoClient(conn_string)

        except (ConnectionFailure, InvalidURI) as e:
            raise HandlerException("Can't connect to %s. %s" % (conn_string, e.message))
