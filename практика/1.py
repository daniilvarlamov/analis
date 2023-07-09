from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import test
import random
from datetime import datetime, timedelta
import time

# Создаем соединение с базой данных
# engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')
# Session = sessionmaker(bind=engine)
# session = Session()


def generate_random_date(start_date, end_date):
    days = (end_date - start_date).days
    random_days = random.randint(0, days)
    random_date = (start_date + timedelta(days=random_days)).__str__()
    return random_date

start_date = datetime(2023, 1, 1)
end_date = datetime(2023, 12, 31)

random_datetime = generate_random_date(start_date, end_date)
print(random_datetime)