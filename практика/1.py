from sqlalchemy import and_
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta

import test
#Создаем соединение с базой данных
engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')
Session = sessionmaker(bind=engine)
session = Session()

#Определяем временной интервал 10 секунд
timelimit = datetime.now() - timedelta(seconds=10)
#Получаем все записи с одинаковым значением столбца id и разницей в 10 секунд
count=session.query(test.transactions).count()
records = session.query(test.transactions.senderaccountid).group_by(test.transactions.senderaccountid).all()
for item in range(1,count+1):
    for i in records:
        result=session.query(test.transactions).filter(test.transactions.senderaccountid==i[0]).all()
        for j in result:
            count=0
            date_last=j.transaction_date
            for k in result:
                timelimit_min = j.transaction_date - timedelta(seconds=5)
                timelimit_max = j.transaction_date + timedelta(seconds=5)
                if k.transaction_date>=timelimit_min and k.transaction_date<=timelimit_max:
                    count=count+1
                    if count>=3:
                        res=session.query(test.suspensiontransactions).filter(and_())
                        trans=test.suspensiontransactions(transactionid=j.id,senderaccountid=j.senderaccountid,receiveraccountid=j.receiveraccountid,amount=j.amount,transaction_date=j.transaction_date,Comment="Подозрительная транзакция времени")
                        session.add(trans)
                        count=0
                else:
                    continue
                


session.commit()