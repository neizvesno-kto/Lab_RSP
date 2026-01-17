from kafka import KafkaConsumer, KafkaProducer
import json

consumer = KafkaConsumer(
    'input-topic',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda x: json.dumps(x).encode('utf-8')
)

for msg in consumer:
    data = msg.value
    data['processed'] = True
    producer.send('output-topic', data)
    producer.flush()
    print("Преобразовано и отправлено:", data)
