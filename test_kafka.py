from kafka import KafkaProducer, KafkaConsumer
import json, time

#producer - sends 1 message
producer = KafkaProducer(
    bootstrap_servers = 'localhost:9092',
    value_serializer = lambda v:json.dumps(v).encode('utf-8')
)
producer.send('test-topic',{'message':'hello kafka','amount':500})
producer.flush()
print("Message sent")

#consumer- reads it back
consumer = KafkaConsumer(
    'test-topic',
    bootstrap_servers = 'localhost:9092',
    auto_offset_reset = 'earliest',
    value_deserializer = lambda v:json.loads(v.decode('utf-8'))
)

print("Waiting for message")
for message in consumer:
    print("Received",message.value)
    break
