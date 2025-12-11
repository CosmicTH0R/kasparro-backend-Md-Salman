import os
import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# FIX: No default hardcoded password. It must come from the environment.
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    # Fallback ONLY for local testing if .env isn't loaded, but safer to warn
    print("WARNING: DATABASE_URL not found. Defaulting to local dev credentials.")
    DATABASE_URL = "postgresql://kasparro_user:kasparro_password@localhost:5432/kasparro_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()