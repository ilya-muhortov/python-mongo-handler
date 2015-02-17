
from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TestData(Base):
    __tablename__ = 'test_data'

    id = Column(Integer, primary_key=True)
    author = Column(String(255))
    data_text = Column(String)