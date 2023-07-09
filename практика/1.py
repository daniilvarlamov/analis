from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import test
import random

# Создаем соединение с базой данных
engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')
Session = sessionmaker(bind=engine)
session = Session()

result=session.query(test.bankaccounts.id).all()
res=random.randint(min(result)[0],max(result)[0])
print(type(max(result)[0]))