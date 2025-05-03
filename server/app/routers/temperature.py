from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile

from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import temperature

get_db = database.get_db
router = APIRouter(tags=["Temperature"], prefix="/temp")


@router.post("/", response_model=schemas.TemperatureCreate)
def add_new_record(
    request: schemas.TemperatureCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return temperature.add_new_record(request, db)


@router.get("/", response_model=List[schemas.Temperature])
def get_all_records(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return temperature.get_all_records(db)


@router.get("/last", response_model=schemas.Temperature)
def get_last_record(
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return temperature.get_last_record(db)


@router.get("/from_to", response_model=List[schemas.Temperature])
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
    return temperature.get_record_from_to(db, from_date, to_date)
