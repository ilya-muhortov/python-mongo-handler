
from sqlalchemy import create_engine

from mongo_handler.db import ConnectionHandler
from mongo_handler import HandlerException


class SQLAlchemyHandler(ConnectionHandler):

    def connect(self, conn_string):
        try:
            engine = create_engine(conn_string)
            return engine.connect()
        
        except Exception as e:
            raise HandlerException(e.message)