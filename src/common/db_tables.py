import uuid
from sqlalchemy.sql.functions import now
from sqlalchemy import Column, Integer, DateTime, String  # , Date, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class PythonTestTable(Base):
    __tablename__ = 'DS_python_celery_test'

    # id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    id = Column(String(), primary_key=True, default=lambda: str(uuid.uuid4()))
    vin = Column(String(20))
    bucketId = Column(Integer)
    CreationTime = Column(DateTime(), server_default=now())
    UpdateTime = Column(DateTime(), onupdate=now())
