from database.db import Base, engine
import database.models

print("Creating database tables...")

Base.metadata.create_all(bind=engine)

print("Database initialized successfully.")