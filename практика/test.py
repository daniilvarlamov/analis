from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB    
import random
import string
import names
from datetime import datetime, timedelta


def create_con(con_str):
    engine = create_engine(con_str)
    Base=declarative_base()
    return engine,Base

engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')
Base=declarative_base()


#создание модели данных
class clients(Base):
    __tablename__='clients'
    id=Column(Integer, primary_key=True,autoincrement=True)
    # data=Column(JSONB)
    firstname=Column(String)
    lastname=Column(String)
    dateofbirth=Column(Date)
    address=Column(String)
    phonenumber=Column(String)
    email=Column(String)
    passportdata=Column(String)
    registrationdate=Column(Date)
    bankaccount=relationship('bankaccounts')


class bankaccounts(Base):
    __tablename__='bankaccounts'
    id=Column(Integer,primary_key=True, autoincrement=True)
    clientid=Column(Integer,ForeignKey('clients.id'))
    accountnumber=Column(String)
    accounttype=Column(String)
    creationdate=Column(Date)
    balance=Column(Numeric)
    

class transactions(Base):
    __tablename__='transactions'
    id=Column(Integer, primary_key=True, autoincrement=True)
    senderaccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    receiveraccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    amount=Column(Numeric)
    transaction_date=Column(DateTime)
    

class suspensiontransactions(Base):
    __tablename__='suspensiontransactions'
    id=Column(Integer,primary_key=True,autoincrement=True)
    transactionid=Column(Integer,ForeignKey('transactions.id'))
    senderaccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    receiveraccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    amount=Column(Numeric)
    transaction_date=Column(DateTime)
    Comment=Column(String)

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

def create_clients_data(session,count):
    result=session.query(clients.id).all()
    if(result==[]):
        count_id=1
    else:
        count_id=max(result)[0]+1
    for i in range(count_id,count+1):
        user=clients(id=i,firstname=names.get_first_name(),lastname=names.get_last_name(),dateofbirth = generate_random_date(datetime(1980, 1, 1), datetime(2000, 12, 31)),
                 address = generate_random_string(10),phonenumber = generate_random_phone_number(),email = generate_random_email(),
                 passportdata = generate_random_string(8),registrationdate = generate_random_date(datetime(2010, 1, 1), datetime.now()))
        session.add(user)
    session.commit()

def create_acconts_data(session):
    result=session.query(clients.id).all()
    result_bank=session.query(bankaccounts.id).all()
    if(result_bank==[]):
        count_id=1
    else:
        count_id=max(result)[0]+1
    for i in range(count_id,max(result)[0]+1):
        account=bankaccounts(id=i,clientid=i,
                             accountnumber = generate_random_string(10),
                             accounttype = random.choice(["дебетовый", "кредитный"]),
                             creationdate = generate_random_date(datetime(2010, 1, 1), datetime.now()),
                             balance = random.randint(1000, 10000))
        session.add(account)
    session.commit()

def gen_receiver(senderaccountid):
    accountids=session.query(bankaccounts.id).all()
    accid=random.randint(min(accountids)[0],max(accountids)[0])
    if accid==senderaccountid:
        gen_receiver(senderaccountid)
    else:
        return accid

def create_transactions_data(session,count):
    result_id=session.query(bankaccounts.id).all()
    result_date=session.query(bankaccounts.creationdate).all()
    for item in range(max(result_id)[0]):
        for i in range(count):
            senderaccountid=random.randint(min(result_id)[0],max(result_id)[0])
            receiveraccountid=gen_receiver(senderaccountid)
            transaction=transactions(senderaccountid=senderaccountid,
                                    receiveraccountid=receiveraccountid,
                                    amount=random.randint(500, 15000),
                                    transaction_date=generate_random_date(datetime.combine(result_date[item][0],datetime.min.time()), datetime.now()))
            session.add(transaction)
    session.commit()


if __name__=='__main__':
    Base.metadata.create_all(bind=engine)
    Session=sessionmaker(bind=engine)
    session=Session()
    c=int(input("Сколько клиентов?\n"))
    create_clients_data(session,c)
    session.close()
    session1=Session()
    create_acconts_data(session1)
    session.close()
    session2=Session()
    count=int(input("Сколько транзакций у 1 клиента?\n"))
    create_transactions_data(session2,count)