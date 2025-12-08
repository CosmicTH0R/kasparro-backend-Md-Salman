import time
from fastapi import FastAPI
from sqlalchemy.exc import OperationalError
from apscheduler.schedulers.background import BackgroundScheduler # This line should now work
from src.core.database import engine, Base, SessionLocal
from src.ingestion.pipeline import ETLPipeline
from src.api.routes import router as api_router

app = FastAPI(title="Kasparro Backend Assignment")
app.include_router(api_router)

def run_etl_job():
    print("--- ⏰ CRON TRIGGER: Starting Scheduled ETL ---")
    db = SessionLocal()
    try:
        pipeline = ETLPipeline(db)
        pipeline.run()
    except Exception as e:
        print(f"Cron Error: {e}")
    finally:
        db.close()

@app.on_event("startup")
def startup_event():
    # Database connection wait loop
    print("Starting up... connecting to database...")
    while True:
        try:
            Base.metadata.create_all(bind=engine)
            break
        except OperationalError:
            time.sleep(3)
        except Exception:
            time.sleep(3)
            
    # Start the Scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(run_etl_job, 'interval', hours=1)
    scheduler.start()
    print("--- Scheduler Started ---")
    
    # Run once immediately so you see data right away
    run_etl_job()

@app.get("/")
def read_root():
    return {"message": "System is running on Render!"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db": "connected"}

from sqlalchemy import inspect
@app.get("/tables")
def get_tables():
    inspector = inspect(engine)
    return {"tables": inspector.get_table_names()}