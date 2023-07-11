from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import create_tables_and_data

# Создаем соединение с базой данных
engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')
Session = sessionmaker(bind=engine)
session = Session()

unique_names = session.query(create_tables_and_data.transactions.senderaccountid).distinct().count()

print(unique_names)
