
from mongo_handler import Process
from sqlalchemy.orm import sessionmaker

from .models import TestData

Session = sessionmaker()


class MysqlToMysql(Process):

    def process(self):
        db_default = self.mysql['default']
        session_default = Session(bind=db_default)

        db_other = self.mysql['other']

        result = db_other.execute('SELECT title, short_content FROM entity')
        for item in result.fetchall():
            obj = TestData(data_text=item[0], author=item[1])
            session_default.add(obj)

        session_default.commit()


class MongoToMysql(Process):

    def process(self):
        db = self.mongo.default['test_database']
        session = Session(bind=self.mysql.default)

        for item in db['test_data'].find():
            obj = TestData(data_text=item['text'], author=item['author'])
            session.add(obj)

        session.commit()