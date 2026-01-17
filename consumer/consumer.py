from kafka import KafkaConsumer
import json
import logging

logging.basicConfig(level=logging.INFO)

consumer = KafkaConsumer(
    'input-topic',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='consumer-group-1',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

count = 0

for message in consumer:
    try:
        count += 1
        logging.info(f"Получено сообщение #{count}: {message.value}")
    except Exception as e:
        logging.error(f"Ошибка обработки: {e}")
