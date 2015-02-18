
from mongo_handler.utils import import_string
from mongo_handler.config import Config
from mongo_handler.process import Process


class HandlerException(Exception):
    pass


class Handler(object):

    #: The class that is used for Process
    #: Defaults to :class:`~mongo_handler.Process`.
    process_base_class = Process

    #: Store all Process items
    process_list = []

    #: The class that is used for the ``config`` attribute of this handler.
    #: Defaults to :class:`~mongo_handler.Config`.
    config_class = Config

    def __init__(self):
        self.config = self.config_class()
        self.context = {}

    def context_register(self, **kwargs):
        """
        Registration context which is passed to Process
        """
        for key in kwargs:
            self.context[key] = kwargs[key]

    def process_register(self, *args):
        """
        Registration Processes for a handler
        Args may be one of the following types:
            - a string: in this case the object with that name will be imported
            - an actual object reference: that object is used directly
            - a list: must contains two arguments: first argument is a string or
            object and second is a dict for a custom Process config.

        Example:
            from example.process import MongoToMysql
            handler.process_register(
                MongoToMysql,
                'example.process.MysqlToMysql',
                (MongoToMysql, {'SOME_KEY': True})
            )
        """

        for arg in args:
            if isinstance(arg, (list, tuple)):
                class_, kwargs = arg[0], arg[1]
            else:
                class_, kwargs = arg, None

            if isinstance(class_, str):
                class_ = import_string(class_)

            if isinstance(class_, object) and issubclass(class_, self.process_base_class):
                self.process_list.append((class_, kwargs))
            else:
                raise HandlerException('Can\'t register process %s', str(class_))

    def run(self):
        """
        Starts step by step all registered Processes
        """
        for class_, kwargs in self.process_list:
            kwargs = kwargs or {}
            obj = class_(config=dict(self.config, **kwargs), **self.context)
            obj.process()