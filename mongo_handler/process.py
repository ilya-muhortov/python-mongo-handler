
import abc


class Process(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, config, **kwargs):
        self.config = config
        print(self.config)
        for key, val in kwargs.items():
            setattr(self, key, val)

    def process(self):
        raise NotImplementedError