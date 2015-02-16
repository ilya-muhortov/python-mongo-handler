
import importlib


def import_string(import_name, silent=True):
    """
    Imports an object based on a string.
    :param import_name: the dotted name for the object to import.
    :param silent: if set to `True` import errors are ignored.
    :return: imported object.
    """

    module_name, obj_name = import_name.rsplit('.', 1)
    try:
        try:
            module = importlib.import_module(module_name)
        except ImportError as e:
            raise ImportError(e)

        try:
            return getattr(module, obj_name)
        except AttributeError as e:
            raise ImportError(e)

    except ImportError as e:
        if silent is True:
            raise Exception(e)
