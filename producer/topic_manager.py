from kafka.admin import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

from config import (
    KAFKA_BOOTSTRAP_SERVERS,
    SUPPORTED_EVENTS,
    NUM_PARTITIONS,
    REPLICATION_FACTOR
)


def create_topics():

    admin = KafkaAdminClient(
        bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS,
        client_id="topic-manager"
    )

    existing_topics = admin.list_topics()

    new_topics = []

    for topic in SUPPORTED_EVENTS.values():

        if topic not in existing_topics:

            new_topics.append(
                NewTopic(
                    name=topic,
                    num_partitions=NUM_PARTITIONS,
                    replication_factor=REPLICATION_FACTOR
                )
            )

    if new_topics:
        try:
            admin.create_topics(new_topics=new_topics)
            print("Topics created successfully.")
        except TopicAlreadyExistsError:
            print("Topics already exist.")

    else:
        print("All Kafka topics already exist.")

    admin.close()