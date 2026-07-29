import os

KAFKA_BOOTSTRAP_SERVERS = os.getenv(
    "KAFKA_BOOTSTRAP_SERVERS",
    "kafka:29092"
)

SUPPORTED_EVENTS = {
    "push": "commit-events",
    "pull_request": "pr-events",
    "pull_request_review": "review-events",
    "issues": "issue-events",
}

NUM_PARTITIONS = 3
REPLICATION_FACTOR = 1