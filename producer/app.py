from flask import Flask

from routes import webhook
from topic_manager import create_topics

app = Flask(__name__)

create_topics()

app.register_blueprint(webhook)


@app.route("/health")
def health():
    return {
        "status": "UP"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )