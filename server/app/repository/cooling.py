from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Response, status, UploadFile
import requests
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app import schemas
from .. import models
from ..hashing import Hash


def add_new_record(request: schemas.Cooling, db: Session):
    new_record = models.Cooling(
        timestamp=datetime.now() + timedelta(hours=2), cooling=request.cooling
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


def get_all_records(db: Session):
    records = db.query(models.Cooling).all()
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return records


def get_record_from_to(db: Session, from_date: datetime, to_date: datetime):
    records = (
        db.query(models.Cooling)
        .filter(
            models.Cooling.timestamp >= from_date,
            models.Cooling.timestamp <= to_date,
        )
        .all()
    )
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return records

def get_cooling_status(db: Session):
    records = db.query(models.Cooling).order_by(models.Cooling.timestamp.desc()).first()
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return records.cooling