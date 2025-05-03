from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Response, status, UploadFile
import requests
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app import schemas
from .. import models
from ..hashing import Hash


def start_measurement(request: schemas.Measurement, db: Session):
    existing_measurement = db.query(models.Measurement).filter(models.Measurement.to_timestamp == None).first()
    if existing_measurement:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"There is already an ongoing measurement with ID {existing_measurement.id}"
        )
    new_record = models.Measurement(from_timestamp=request.from_timestamp)
    
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


def get_all_records(db: Session):
    records = db.query(models.Measurement).all()
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return records

def get_measurement_by_id(id: int, db: Session):
    record = db.query(models.Measurement).filter(models.Measurement.id == id).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found")
    return record

def get_last_record(db: Session):
    record = db.query(models.Measurement).order_by(models.Measurement.id.desc()).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found")
    return record

def end_measurement(request: schemas.MeasurementEnd, db: Session):
    record = db.query(models.Measurement).filter(models.Measurement.to_timestamp == None).order_by(models.Measurement.from_timestamp.desc()).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No ongoing measurement found")
    record.to_timestamp = request.to_timestamp
    db.commit()
    db.refresh(record)
    return record
