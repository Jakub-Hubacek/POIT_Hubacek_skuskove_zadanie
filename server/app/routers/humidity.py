from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile

from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import  humidity

get_db = database.get_db
router = APIRouter(tags=["Humidity"], prefix="/humidity")


@router.post("/", response_model=schemas.HumidityCreate)
def add_new_record(request: schemas.HumidityCreate, db: Session = Depends(get_db), current_user: schemas.User = Depends(oauth2.get_current_user)):
    return  humidity.add_new_record(request, db)


@router.get("/", response_model=List[schemas.Humidity])
def get_all_records(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return  humidity.get_all_records(db)


@router.get("/last", response_model=schemas.Humidity)
def get_last_record(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return humidity.get_last_record(db)


@router.get("/from_to", response_model=List[schemas.Humidity])
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
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return humidity.get_record_from_to(db, from_date, to_date)
