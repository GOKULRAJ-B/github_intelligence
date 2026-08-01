from parser import parse_push_event
from config import (
    TOPIC,
    GROUP_ID,
    KAFKA_BOOTSTRAP_SERVERS,
)

from shared.kafka_consumer import create_consumer
from database.repository import RepositoryService

print("Starting Hotspot Consumer...", flush=True)

consumer = create_consumer(
    topic=TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=GROUP_ID,
)

repository = RepositoryService()

print("Hotspot Consumer Connected", flush=True)

while True:

    records = consumer.poll(timeout_ms=5000)

    if not records:
        continue

    for _, messages in records.items():

        for message in messages:

            files = parse_push_event(
                message.value,
            )

            for file in files:

                repository.save_hotspot(
                    file,
                )