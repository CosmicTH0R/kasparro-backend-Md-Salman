import time
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from src.core.database import engine, Base
from src.core import models
from src.api.routes import router as api_router

app = FastAPI(title="Kasparro Backend Assignment")

# Register the routes
app.include_router(api_router)

@app.on_event("startup")
def startup_event():
    """
    On startup, try to create tables. 
    If DB is not ready, wait 2 seconds and try again.
    Keep trying until successful.
    """
    print("Starting up... connecting to database...")
    while True:
        try:
            # Try to create tables to verify connection
            Base.metadata.create_all(bind=engine)
            print("--- SUCCESS: Database connected & Tables created ---")
            break # Exit the loop if successful
        except OperationalError:
            print("Database not ready yet... waiting 3 seconds.")
            time.sleep(3)
        except Exception as e:
            print(f"Unexpected error: {e}")
            time.sleep(3)

@app.get("/")
def read_root():
    return {"message": "System is running!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db": "connected"}

from sqlalchemy import inspect
@app.get("/tables")
def get_tables():
    inspector = inspect(engine)
    return {"tables": inspector.get_table_names()}