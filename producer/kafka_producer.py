import json

from kafka import KafkaProducer

from config import KAFKA_BOOTSTRAP_SERVERS


producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    value_serializer=lambda v: json.dumps(v).encode("utf-8"),
)