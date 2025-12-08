from sqlalchemy import Column, Integer, String, JSON, DateTime, Boolean, Text
from sqlalchemy.sql import func
from src.core.database import Base

# --- 1. Raw Data Tables ---
class RawDataAPI(Base):
    __tablename__ = "raw_api_data"
    id = Column(Integer, primary_key=True, index=True)
    raw_payload = Column(JSON)
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

class RawDataCSV(Base):
    __tablename__ = "raw_csv_data"
    id = Column(Integer, primary_key=True, index=True)
    raw_row_content = Column(JSON) 
    ingested_at = Column(DateTime(timezone=True), server_default=func.now())

# --- 2. Unified Schema ---
class UnifiedData(Base):
    __tablename__ = "unified_data"
    id = Column(Integer, primary_key=True, index=True)
    source_type = Column(String)
    original_id = Column(String)
    title = Column(String, nullable=True)
    content = Column(Text, nullable=True)
    published_date = Column(DateTime(timezone=True), nullable=True)
    data_hash = Column(String, unique=True, index=True)
    normalized_at = Column(DateTime(timezone=True), server_default=func.now())

# --- 3. ETL Job Metadata ---
class ETLJob(Base):
    __tablename__ = "etl_jobs"
    id = Column(Integer, primary_key=True, index=True)
    run_id = Column(String, unique=True)
    status = Column(String)
    records_processed = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    start_time = Column(DateTime(timezone=True), server_default=func.now())
    end_time = Column(DateTime(timezone=True), nullable=True)