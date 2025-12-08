from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.core.models import UnifiedData, ETLJob
from typing import Optional, List

router = APIRouter()

@router.get("/data")
def get_data(
    page: int = 1,
    limit: int = 10,
    source: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Calculate offset for pagination (P0.2 Requirement)
    offset = (page - 1) * limit
    
    # Start building the query
    query = db.query(UnifiedData)
    
    # Apply Filtering (P0.2 Requirement)
    if source:
        query = query.filter(UnifiedData.source_type == source)
    
    # Get total count (for metadata)
    total_records = query.count()
    
    # Apply Pagination
    data = query.offset(offset).limit(limit).all()
    
    return {
        "metadata": {
            "page": page,
            "limit": limit,
            "total_records": total_records,
            "request_id": "req_" + str(offset) # Simple mock ID
        },
        "data": data
    }

@router.get("/stats") # (P1.3 Requirement)
def get_stats(db: Session = Depends(get_db)):
    # Get the latest job status
    last_job = db.query(ETLJob).order_by(ETLJob.start_time.desc()).first()
    
    total_processed = db.query(UnifiedData).count()
    
    return {
        "total_records_processed": total_processed,
        "last_run_status": last_job.status if last_job else "never_run",
        "last_run_time": last_job.start_time if last_job else None
    }