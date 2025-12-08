from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://kasparro_user:kasparro_password@localhost:5432/kasparro_db")

# Create the engine lazily (don't connect yet)
engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        # Simple check to ensure DB is actually alive when a request comes in
        yield db
    finally:
        db.close()