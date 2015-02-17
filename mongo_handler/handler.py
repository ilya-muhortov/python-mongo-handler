
from mongo_handler.utils import import_string
from mongo_handler.config import Config
from mongo_handler.process import Process


class HandlerException(Exception):
    pass


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

    def process_register(self, *args):
        for arg in args:
            if isinstance(arg, (list, tuple)):
                class_, kwargs = arg[0], arg[1]
            else:
                class_, kwargs = arg, None

            if isinstance(class_, str):
                class_ = import_string(class_)

            if isinstance(class_, object) and issubclass(class_, Process):
                self.process_list.append((class_, kwargs))
            else:
                raise HandlerException('Can\'t register process %s', str(class_))

    def run(self):
        for class_, kwargs in self.process_list:
            kwargs = kwargs or {}
            obj = class_(config=dict(self.config, **kwargs), **self.context)
            obj.process()