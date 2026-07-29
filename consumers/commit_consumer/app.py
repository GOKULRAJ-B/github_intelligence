from parser import parse_push_event
from config import (
    TOPIC,
    GROUP_ID,
    KAFKA_BOOTSTRAP_SERVERS,
)

from shared.kafka_consumer import create_consumer
from database.repository import RepositoryService

print("Starting Commit Consumer...", flush=True)

consumer = create_consumer(
    topic=TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=GROUP_ID,
)

repository = RepositoryService()

print("Commit Consumer Connected", flush=True)

while True:

    records = consumer.poll(timeout_ms=5000)

    if not records:
        continue

    for _, messages in records.items():

        for message in messages:

            event = message.value

            commits = parse_push_event(event)

            for commit in commits:

                repository.save_commit(commit)