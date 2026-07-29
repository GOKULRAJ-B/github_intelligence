import json
import time

from kafka import KafkaConsumer
from kafka.errors import NoBrokersAvailable

from shared.config import (
    AUTO_OFFSET_RESET,
    CONSUMER_TIMEOUT_MS,
    ENABLE_AUTO_COMMIT,
)

from shared.logger import get_logger

logger = get_logger("KafkaConsumer")


def create_consumer(
    topic,
    bootstrap_servers,
    group_id,
):

    while True:

        try:

            consumer = KafkaConsumer(
                topic,
                bootstrap_servers=[bootstrap_servers],
                group_id=group_id,
                auto_offset_reset=AUTO_OFFSET_RESET,
                enable_auto_commit=ENABLE_AUTO_COMMIT,
                consumer_timeout_ms=-1,
                value_deserializer=lambda x: json.loads(
                    x.decode("utf-8")
                ),
            )

            logger.info(
                "Connected to topic '%s'",
                topic,
            )

            return consumer

        except NoBrokersAvailable:

            logger.warning(
                "Kafka broker unavailable. Retrying in 5 seconds..."
            )

            time.sleep(5)