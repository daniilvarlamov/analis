from sqlalchemy import create_engine, Column, Integer, String, Date,ForeignKey, DateTime, Numeric,MetaData, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

# Создаем соединение с базой данных
engine = create_engine('postgresql://postgres:root@localhost:5432/Bank')
Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

# Определяем модель clients
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
#
class bankaccounts(Base):
    __tablename__='bankaccounts'
    id=Column(Integer,primary_key=True, autoincrement=True)
    clientid=Column(Integer,ForeignKey('clients.id'))
    accountnumber=Column(String)
    accounttype=Column(String)
    creationdate=Column(Date)
    balance=Column(Numeric)

# Определяем модель transactions
class transactions(Base):
    __tablename__ = 'transactions'
    id=Column(Integer, primary_key=True, autoincrement=True)
    senderaccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    receiveraccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    amount=Column(Numeric)
    transaction_date=Column(DateTime)

# Определяем модель suspensiontransactions
class suspensiontransactions(Base):
    __tablename__='suspensiontransactions'
    id=Column(Integer,primary_key=True,autoincrement=True)
    senderaccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    receiveraccountid=Column(Integer,ForeignKey('bankaccounts.id'))
    amount=Column(Numeric)
    transaction_date=Column(DateTime)
    Comment=Column(String)

# Выполняем запрос для нахождения подозрительных транзакций
suspicious_transactions = session.query(transactions).join(
    clients, clients.id == transactions.senderaccountid
).group_by(transactions.id).having(transactions.amount > func.avg(transactions.amount)).all()

# Добавляем информацию о подозрительных транзакциях в таблицу suspensiontransactions
for transaction in suspicious_transactions:
    suspicious_transaction = suspensiontransactions(client_id=transaction.senderaccountid, transaction_id=transaction.id)
    session.add(suspicious_transaction)

# Фиксируем изменения в базе данных
session.commit()