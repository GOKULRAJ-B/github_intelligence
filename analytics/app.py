from flask import Flask

from database.db import Base, engine
import database.models

print("Registered tables:")
print(Base.metadata.tables.keys())

print("Creating database tables...")
Base.metadata.create_all(bind=engine)
print("Database initialized successfully.")

from routes import analytics_bp

app = Flask(__name__)
app.register_blueprint(analytics_bp)

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True,
    )