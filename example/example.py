
import sys

sys.path.insert(0, '../')

from mongo_handler.handler import Handler, Process
from mongo_handler.db import MongoHandler, SQLAlchemyHandler


class Config(object):

    MYSQL_DATABASE = {
        'default': 'mysql://root:@localhost/mongo_handler'
    }

    MONGO_DATABASE = {
        'default': 'mongodb://localhost:27017/'
    }


class DevelopConfig(Config):
    pass

handler = Handler()

handler.config.from_object(DevelopConfig)
handler.config.from_dict({
    'SOME_KEY': 'some value'
})

handler.context_register(
    mongo=MongoHandler(handler.config['MONGO_DATABASE']),
    mysql=SQLAlchemyHandler(handler.config['MYSQL_DATABASE'])
)
handler.process_register(
    'example.entries.article.Article',
)

if __name__ == '__main__':
    handler.run()