
import six
from mongo_handler.utils import import_string


class Config(dict):

    """
    Holder for user configured settings.
    """

    def __init__(self, defaults=None):
        dict.__init__(self, defaults or {})

    def __getattr__(self, item):
        return self[item]

    def from_object(self, obj):
        """
        Updates the values from the given object. An object may be one on
        the following types:
        - a string: in this case the object with that name will be imported
        - an actual object reference: that object is used directly
        """

        if isinstance(obj, six.string_types):
            obj = import_string(obj)

        for key in dir(obj):
            if key.isupper():
                self[key] = getattr(obj, key)
