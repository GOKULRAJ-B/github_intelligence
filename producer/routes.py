from flask import Blueprint
from flask import jsonify
from flask import request

from config import SUPPORTED_EVENTS
from kafka_producer import producer

webhook = Blueprint("webhook", __name__)


@webhook.route("/webhook", methods=["POST"])
def github_webhook():

    event = request.headers.get("X-GitHub-Event")

    if event not in SUPPORTED_EVENTS:
        return jsonify(
            {
                "status": "ignored",
                "event": event,
            }
        ), 200

    payload = request.get_json()

    topic = SUPPORTED_EVENTS[event]

    producer.send(topic, payload)
    producer.flush()

    return jsonify(
        {
            "status": "published",
            "topic": topic,
            "event": event,
        }
    ), 200