from kafka import KafkaProducer
import json, time, random, uuid
from datetime import datetime

producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v:json.dumps(v).encode('utf-8')
)

MERCHANTS = ['Amazon','Flipkart','Swiggy','Zomato','BigBasket','Mytra','Uber','Ola','BookMyShow','PhonePe']
CITIES = ['Mumbai','Delhi','Bangalore','Chennai','Hyderabad','Pune']
USERS = [f'USR_{i:03d}' for i in range(1,51)] #50 fake users

#track last transaction per user - to simulate fraud patterns
user_last_city = {}
user_avg_amount = {user: random.uniform(200,300) for user in USERS}

def generate_transaction():
    user = random.choice(USERS)
    city = random.choice(CITIES)

    #2% chance of fraud
    is_fraud = random.random() < 0.2

    if is_fraud:
        #fraud pattern: very high amount or different city from last transaction
        amount = round(random.uniform(15000,50000),2)
    else:
        avg = user_avg_amount[user]
        amount = round(random.gauss(avg,avg * 0.3),2)
        amount = max(10,amount) #no negative amounts
    
    txn = {
        'txn_id': str(uuid.uuid4()),
        'user_id': user,
        'amount': amount,
        'merchant': random.choice(MERCHANTS),
        'city':city,
        'timestamp':datetime.now().isoformat(),
        'is_fraud_label': int(is_fraud) #for testing onlu
    }

    user_last_city[user] = city
    return txn

print("Starting transaction generator")
count = 0
while True:
    txn = generate_transaction()
    producer.send('transactions',txn)
    count += 1
    print(f"Sent txn #{count}: {txn['user_id']} | Rs{txn['amount']} | {"Fraud" if txn['is_fraud_label'] else "OK"}")
    time.sleep(0.5) #1 transaction ever 0.5 seconds
