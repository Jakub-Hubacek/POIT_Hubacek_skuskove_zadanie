from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile

from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import measurement

get_db = database.get_db
router = APIRouter(tags=["Measurement"], prefix="/measurement")


@router.post("/start", response_model=schemas.MeasurementCreate)
def start_measurement(
    request: schemas.MeasurementCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return measurement.start_measurement(request, db)


@router.post("/end", response_model=schemas.MeasurementEnd)
def end_measurement(
    request: schemas.MeasurementEnd,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return measurement.end_measurement(request, db)


@router.get("/", response_model=List[schemas.Measurement])
def get_all_records(db: Session = Depends(get_db)):
    return measurement.get_all_records(db)


@router.get("/last", response_model=schemas.Measurement)
def get_last_record(
    db: Session = Depends(get_db),
):
    return measurement.get_last_record(db)


@router.get("/{id}", response_model=schemas.Measurement)
def get_measurement_by_id(
    id: int,
    db: Session = Depends(get_db),
):
    return measurement.get_measurement_by_id(id, db)
