
from mongo_handler import HandlerException

DEFAULT_DB_ALIAS = 'default'


class ConnectionHandler(object):
    """
    Stores database connections
    """

    def __init__(self, databases):
        self._databases = databases
        self._connections = dict()

    @property
    def databases(self):
        if DEFAULT_DB_ALIAS not in self._databases:
            raise HandlerException('You must define a "%s" database' % DEFAULT_DB_ALIAS)

        return self._databases

    @property
    def default(self):
        return self[DEFAULT_DB_ALIAS]

    def __getitem__(self, alias):
        if alias not in self._connections:
            try:
                conn_string = self.databases[alias]
            except KeyError:
                raise HandlerException("The connection %s doesn't exist" % alias)

            self._connections[alias] = self.connect(conn_string)

        return self._connections[alias]

    def connect(self, conn_string):
        raise NotImplementedError