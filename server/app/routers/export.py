from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile
from fastapi.responses import StreamingResponse
from datetime import datetime

from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import temperature, export

get_db = database.get_db
router = APIRouter(tags=["Export"], prefix="/export")


@router.get("/from_to", response_class=StreamingResponse)
def export_record_from_to(
    measurement_id: Optional[int] = Query(
        None, description="Measurement ID to filter by"
    ),
    from_date: Optional[datetime] = Query(
        None,
        description="From date in YYYY-MM-DD format (optionally add time as well by adding THH:MM:SS)",
    ),
    to_date: Optional[datetime] = Query(
        None,
        description="To date in YYYY-MM-DD format (optionally add time as well by adding THH:MM:SS)",
    ),
    db: Session = Depends(get_db),
):
    return export.export_records_to_csv(db, from_date, to_date, measurement_id)
