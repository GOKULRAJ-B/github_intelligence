import os

TOPIC = "pr-events"

GROUP_ID = "pr-analytics-group"

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:29092",
)