from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile

from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import vibrations

get_db = database.get_db
router = APIRouter(tags=["Vibrations"], prefix="/vibrations")


@router.post("/", response_model=schemas.VibrationsCreate)
def add_new_record(
    request: schemas.VibrationsCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return vibrations.add_new_record(request, db)


@router.get("/", response_model=List[schemas.Vibrations])
def get_all_records(db: Session = Depends(get_db)):
    return vibrations.get_all_records(db)


@router.get("/from_to", response_model=List[schemas.Vibrations])
def get_record_from_to(
    from_date: str = Query(
        ...,
        description="From date in YYYY-MM-DD format (optionally add time as well by adding THH:MM:SS)",
    ),
    to_date: str = Query(
        ...,
        description="To date in YYYY-MM-DD format (optionally add time as well by adding THH:MM:SS)",
    ),
    db: Session = Depends(get_db),
):
    return vibrations.get_record_from_to(db, from_date, to_date)
