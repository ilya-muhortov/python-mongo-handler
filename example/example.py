# coding: utf-8

import sys

sys.path.insert(0, '../')

from mongo_handler import Handler
from mongo_handler.db.mongo import MongoHandler
from mongo_handler.db.alchemy import SQLAlchemyHandler


class Config(object):

    MYSQL_DATABASE = {
        'default': 'mysql://root:@localhost/mongo_handler',
        'other': 'mysql://root:@localhost/armada'
    }

    MONGO_DATABASE = {
        'default': 'mongodb://localhost:27017/'
    }

    SOME_KEY = False


class DevelopConfig(Config):
    pass

handler = Handler()

# Регистрируем первоначальные настройки для соединения с бд и др.
handler.config.from_object(DevelopConfig)
handler.config.update({
    'SOME_KEY_DICT': 'some value'
})

# Регистрируем соединения с бд, используя конфиг
handler.context_register(
    mongo=MongoHandler(handler.config['MONGO_DATABASE']),
    mysql=SQLAlchemyHandler(handler.config['MYSQL_DATABASE']),
)

# Добавляем обработчики
from example.process import MongoToMysql
handler.process_register(
    MongoToMysql,
    'example.process.MysqlToMysql',
    (MongoToMysql, {'SOME_KEY': True})
)

if __name__ == '__main__':
    # Запускаем обработчики
    handler.run()