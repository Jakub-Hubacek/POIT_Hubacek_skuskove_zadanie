from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Response, status, UploadFile
import requests
from sqlalchemy import or_
from sqlalchemy.orm import Session
from app import schemas
from .. import models
from ..hashing import Hash


def add_new_record(request: schemas.Vibrations, db: Session):
    new_record = models.Vibrations(
        timestamp=datetime.now() + timedelta(hours=2), vibrations=request.vibrations
    )
    db.add(new_record)
    db.commit()
    db.refresh(new_record)
    return new_record


def get_all_records(db: Session):
    records = db.query(models.Vibrations).all()
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return records


def get_record_from_to(db: Session, from_date: datetime, to_date: datetime):
    records = (
        db.query(models.Vibrations)
        .filter(
            models.Vibrations.timestamp >= from_date,
            models.Vibrations.timestamp <= to_date,
        )
        .all()
    )
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return records
