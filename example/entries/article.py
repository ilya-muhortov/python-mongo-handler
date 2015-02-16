
from mongo_handler.handler import Handler, Process
from sqlalchemy import *
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Session = sessionmaker()
Base = declarative_base()


class TestData(Base):
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True)
    author = Column(String(255))
    data_text = Column(String)


class Article(Process):

    def __init__(self, *args, **kwargs):
        super(Article, self).__init__(*args, **kwargs)

    def process(self):
        db = self.mongo.default['test_database']
        session = Session(bind=self.mysql.default)

        for item in db['test_data'].find():
            obj = TestData(data_text=item['text'], author=item['author'])
            session.add(obj)

        session.commit()