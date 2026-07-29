import json
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    TOPIC,
    GROUP_ID,
)


def create_consumer():
    while True:
        try:
            consumer = KafkaConsumer(
                TOPIC,
                bootstrap_servers=[KAFKA_BOOTSTRAP_SERVERS],
                group_id=GROUP_ID,
                auto_offset_reset="earliest",
                value_deserializer=lambda m: json.loads(m.decode("utf-8")),
                api_version=(3, 6, 0),
            )

            print("Connected to Kafka")
            return consumer

        except NoBrokersAvailable:
            print("Kafka not ready. Retrying in 5 seconds...")
            time.sleep(5)