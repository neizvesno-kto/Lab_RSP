from kafka import KafkaProducer
import json
import logging

logging.basicConfig(level=logging.INFO)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_message(topic, message):
    try:
        producer.send(topic, message)
        producer.flush()
        logging.info(f"Сообщение отправлено: {message}")
    except Exception as e:
        logging.error(f"Ошибка отправки: {e}")
        producer.send("dlq-topic", {"error": str(e), "data": message})
