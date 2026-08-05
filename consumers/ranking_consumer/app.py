from parser import parse_push_event
from config import (
    TOPIC,
    GROUP_ID,
    KAFKA_BOOTSTRAP_SERVERS,
)

from shared.kafka_consumer import create_consumer
from database.ranking_service import RankingService

print("Starting Ranking Consumer...", flush=True)

consumer = create_consumer(
    topic=TOPIC,
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
    group_id=GROUP_ID,
)

service = RankingService()

print("Ranking Consumer Connected", flush=True)

while True:

    records = consumer.poll(timeout_ms=5000)

    if not records:
        continue

    for _, messages in records.items():

        for message in messages:

            event = message.value

            print("Received Kafka event")
            print(event)

            data = parse_push_event(event)

            print(data)

            print("Updating ranking for:", data["repository"])

            service.update_ranking(
                data["repository"]
            )