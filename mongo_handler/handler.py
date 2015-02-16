
import importlib

from mongo_handler.utils import import_string
from mongo_handler.config import Config


class HandlerException(Exception):
    pass


class Process(object):

    def __init__(self, config, **kwargs):
        self.config = config
        self.mongo = kwargs.pop('mongo')
        self.mysql = kwargs.pop('mysql')


class Handler(object):

    process_base_class = Process

    process_list = []

    config_class = Config

    config_default = {
    }

    def __init__(self):
        self.config = self.config_class(self.config_default)
        self.context = {}

    def context_register(self, **kwargs):
        for key in kwargs:
            self.context[key] = kwargs[key]

    def process_add(self, class_, kwargs=None):
        self.process_list.append((class_, kwargs))

    def process_register(self, *args):
        for arg in args:
            kwargs = None
            if isinstance(arg, (list, tuple)):
                arg, kwargs = arg[0], arg[1]

            if isinstance(arg, str):
                class_ = import_string(arg)
                self.process_add(class_, kwargs)

            elif isinstance(arg, object):
                self.process_add(arg, kwargs)

            else:
                raise HandlerException('Can\'t register entry %s', arg)

    def run(self):
        for entry_class, kwargs in self.process_list:
            instance = entry_class(config=self.config, **self.context)
            instance.process()