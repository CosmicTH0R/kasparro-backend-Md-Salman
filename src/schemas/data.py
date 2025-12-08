from pydantic import BaseModel, Field, validator
from typing import Optional, Any
from datetime import datetime

# --- Incoming Data Models (Validation) ---

class SourceAPIItem(BaseModel):
    # Adjust these fields to match the ACTUAL API response you get later
    id: str
    title: str
    description: Optional[str] = None
    published_at: Optional[datetime] = None
    
    class Config:
        extra = "ignore" # Ignore extra fields from API

class SourceCSVRow(BaseModel):
    # Adjust these to match the CSV columns
    csv_id: str
    headline: str
    body: Optional[str] = None
    date_str: Optional[str] = None 

    @validator('date_str')
    def parse_date(cls, v):
        # Basic cleaning: ensure we can handle strings
        return v if v else None

# --- Unified Model (Output) ---
class UnifiedRecord(BaseModel):
    source_type: str
    original_id: str
    title: str
    content: Optional[str]
    published_date: Optional[datetime]
    data_hash: str # For deduplication