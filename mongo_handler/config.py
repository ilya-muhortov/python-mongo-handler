
import six
from mongo_handler.utils import import_string


class Config(dict):

    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def __getattr__(self, item):
        return self[item]

    def from_object(self, obj):
        if isinstance(obj, six.string_types):
            obj = import_string(obj)

        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)

    def from_dict(self, data):
        for key in data:
            self[key.upper()] = data[key]
