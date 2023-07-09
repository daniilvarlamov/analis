from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import relationship
import test


engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')

Session=sessionmaker(bind=engine)
session=Session()
a=session.query(test.clients).all()
for item in a:
    print(item.id)