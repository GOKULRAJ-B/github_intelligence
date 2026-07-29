import os

TOPIC = "commit-events"

GROUP_ID = "commit-analytics-group"

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:29092",
)