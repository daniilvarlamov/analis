from sqlalchemy import and_
from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, DateTime, Numeric, func
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import declarative_base
from datetime import datetime, timedelta
import create_tables_and_data as test
import tkinter as tk

# Функция-обработчик для кнопки
def button_click():
    engine = create_engine('postgresql://postgres:1qaz!QAZ@localhost:5432/Bank')
    Session = sessionmaker(bind=engine)
    session = Session()
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
                            existing_suspensiontransaction = session.query(test.suspensiontransactions).filter_by(transactionid=j.id,senderaccountid=j.senderaccountid,receiveraccountid=j.receiveraccountid,amount=j.amount,transaction_date=j.transaction_date,comm='Подозрительное время транзакции').first()
                            if existing_suspensiontransaction is not None:
                                pass
                            else:
                                trans=test.suspensiontransactions(transactionid=j.id,senderaccountid=j.senderaccountid,receiveraccountid=j.receiveraccountid,amount=j.amount,transaction_date=j.transaction_date,comm='Подозрительное время транзакции')
                                session.add(trans)
                    else:
                        continue
                    
    session.commit()
    session.close()

    session=Session()
    unique_names = session.query(test.transactions.senderaccountid).distinct().count()
    for i in range(1,unique_names+1):
        senderaccountid = i  # Создаем объект senderaccountid на основе значения i
        suspicious_transactions_avg = round(session.query(func.avg(test.transactions.amount)).filter(test.transactions.senderaccountid == senderaccountid).scalar(), 2)
        suspicious_transactions = session.query(test.transactions).filter(test.transactions.senderaccountid == senderaccountid).filter(test.transactions.amount > suspicious_transactions_avg).all()
        for row in suspicious_transactions:
            existing_suspensiontransaction = session.query(test.suspensiontransactions).filter_by(transactionid=row.id,senderaccountid=row.senderaccountid,receiveraccountid=row.receiveraccountid,amount=row.amount,transaction_date=row.transaction_date,comm='Подозрительная сумма транзакции').first()
            if existing_suspensiontransaction is not None:
                pass
            else:
                suspicious_transactions_data = test.suspensiontransactions(
                    transactionid=row.id,
                    senderaccountid=row.senderaccountid,
                    receiveraccountid=row.receiveraccountid,
                    amount=row.amount,
                    transaction_date=row.transaction_date,
                    comm='Подозрительная сумма транзакции'
                )
                session.add(suspicious_transactions_data)
                
    session.commit()

# Создание графического окна
window = tk.Tk()

# Создание кнопки
button = tk.Button(window, text="Нажми меня!", command=button_click)

button.pack()

window.mainloop()

