from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Response, status, UploadFile
import requests
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app import schemas
from .. import models
from ..hashing import Hash




def add_new_record(request: schemas.Temperature, db: Session):
    new_record = models.Tempterature(
        timestamp=request.timestamp,
        temp=request.temp
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record

def get_all_records(db: Session):
    records = db.query(models.Tempterature).all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found")
    return records

def get_record_from_to(db: Session, from_date: datetime, to_date: datetime):
    records = db.query(models.Tempterature).filter(
        models.Tempterature.timestamp >= from_date,
        models.Tempterature.timestamp <= to_date
    ).all()
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found")
    return records

def get_last_record(db: Session):
    record = db.query(models.Tempterature).order_by(models.Tempterature.timestamp.desc()).first()
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found")
    return record
