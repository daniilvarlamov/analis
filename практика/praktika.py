import random
import string
import names

from datetime import datetime, timedelta
import psycopg2
import copy

connection = psycopg2.connect("dbname=Bank user=postgres password=1qaz!QAZ")

cursor = connection.cursor()

cursor.execute("select MAX(ID) from clients")
client_id = cursor.fetchall()[0][0]
if client_id==None:
    client_id=0
    
cursor.execute("select MAX(ID) from bankaccounts")
account_id = cursor.fetchall()[0][0]
if account_id==None:
    account_id=0
    
cursor.execute("select MAX(ID) from transactions")
transaction_id = cursor.fetchall()[0][0]
if transaction_id==None:
    transaction_id=0
    
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

# Таблица "Клиенты"
client_id_2= copy.copy(client_id)
clients_data = []
for i in range(10):
    client_id = client_id_2 + i + 1
    first_name = names.get_first_name()
    last_name = names.get_last_name()
    birth_date = generate_random_date(datetime(1980, 1, 1), datetime(2000, 12, 31))
    address = generate_random_string(10)
    phone_number = generate_random_phone_number()
    email = generate_random_email()
    passport_data = generate_random_string(8)
    registration_date = generate_random_date(datetime(2010, 1, 1), datetime.now())
    clients_data.append((client_id, first_name, last_name, birth_date, address, phone_number, email, passport_data, registration_date))


account_id_2= copy.copy(account_id)
accounts_data = []
for i in range(10):
    account_id = account_id_2 + i + 1
    client_id = i + 1
    account_number = generate_random_string(10)
    account_type = random.choice(["дебетовый", "кредитный"])
    creation_date = generate_random_date(datetime(2010, 1, 1), datetime.now())
    balance = random.randint(1000, 10000)
    accounts_data.append((account_id, client_id, account_number, account_type, creation_date, balance))

transaction_id_2= copy.copy(transaction_id)
transactions_data = []
for i in range(10):
    transaction_id = transaction_id + i + 1
    sender_account_id = random.randint(1, 10)
    recipient_account_id = random.randint(1, 10)
    while sender_account_id == recipient_account_id:
        recipient_account_id = random.randint(1, 10)
    transaction_amount = random.randint(10, 1000)
    transaction_date = generate_random_date(datetime(2022, 1, 1), datetime.now())
    transactions_data.append((transaction_id, sender_account_id, recipient_account_id, transaction_amount, transaction_date))


query = "INSERT INTO Clients (ID, FirstName, LastName, DateOfBirth,Address,PhoneNumber,Email,PassportData,RegistrationDate) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

for item in clients_data:
    cursor.execute(query, item)

query="INSERT INTO BankAccounts (ID, ClientID, AccountNumber, AccountType, CreationDate, Balance) VALUES (%s, %s, %s, %s, %s, %s)"

for item in accounts_data:
    cursor.execute(query, item)

query="INSERT INTO Transactions (ID, SenderAccountID, ReceiverAccountID, Amount, TransactionDate) VALUES (%s, %s, %s, %s, %s)"

for item in transactions_data:
    cursor.execute(query, item)
    
connection.commit()
cursor.close()
connection.close()