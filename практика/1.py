from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB    
import random
import string
import names
from datetime import datetime, timedelta
import test

engine,bind=test.create_con('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')

Session=sessionmaker(bind=engine)
session=Session()
result=session.query(test.clients).all()
for row in result:
    print(row.id,row.address)
