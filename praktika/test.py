from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import random
import string
import names
from datetime import datetime, timedelta


#генерация
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(length))

def generate_random_date(start_date, end_date):
    days = (end_date - start_date).days
    random_days = random.randint(0, days)
    random_date = (start_date + timedelta(days=random_days)).__str__()
    return random_date

def generate_random_phone_number():
    return ''.join(random.choices(string.digits, k=10))

def generate_random_email():
    return f"{generate_random_string(5)}@{generate_random_string(5)}.com"


#создание модели данных
engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')

Base=declarative_base()

class clients(Base):
    __tablename__='clientsss'
    id=Column(Integer, primary_key=True,autoincrement=True)
    firstname=Column(String)
    lastname=Column(String)
    dateofbirth=Column(Date)
    address=Column(String)
    phonenumber=Column(String)
    email=Column(String)
    passportdata=Column(String)
    registrationdate=Column(Date)
    bankaccount=relationship('bankaccounts',back_populates='client')
    

class bankaccounts(Base):
    __tablename__='bankaccountsss'
    id=Column(Integer,primary_key=True, autoincrement=True)
    clientid=Column(Integer,ForeignKey('clientsss.id'))
    client=relationship('clients',back_populates='bankaccount')
    accountnumber=Column(String)
    accounttype=Column(String)
    creationdate=Column(Date)
    balance=Column(Numeric)
    transaction=relationship()
    
class transactions(Base):
    __tablename__='transactionsss'
    id=Column(Integer, primary_key=True, autoincrement=True)
    senderaccountid=Column(Integer,ForeignKey('bankaccountsss.id'))
    receiveraccountid=Column(Integer,ForeignKey('bankaccountsss.id'))
    amount=Column(Numeric)
    
    

Base.metadata.create_all(engine)
Session=sessionmaker(bind=engine)
session=Session()
clients_ids=session.query(clients).count()
for i in range(10):
    user=clients(firstname=names.get_first_name(),lastname=names.get_last_name(),dateofbirth = generate_random_date(datetime(1980, 1, 1), datetime(2000, 12, 31)),
                 address = generate_random_string(10),phonenumber = generate_random_phone_number(),email = generate_random_email(),
                 passportdata = generate_random_string(8),registrationdate = generate_random_date(datetime(2010, 1, 1), datetime.now()))
    session.add(user)
    
session.commit()