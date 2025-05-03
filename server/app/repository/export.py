from datetime import datetime, timedelta
from typing import Optional
from fastapi import HTTPException, Response, status, UploadFile
import requests
from sqlalchemy import or_, DateTime
from sqlalchemy.orm import Session
from app import schemas
from .. import models
from ..hashing import Hash
import csv
from io import StringIO
from fastapi.responses import StreamingResponse


def get_record_from_to(db: Session, from_date: datetime, to_date: datetime, measurement_id: Optional[int] = None):
    if measurement_id is not None:
        measurement = db.query(models.Measurement).filter(models.Measurement.id == measurement_id).first()
        if not measurement:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Measurement not found"
            )
        from_date = measurement.from_timestamp
        to_date = measurement.to_timestamp
    records = (
        db.query(
            models.Tempterature.timestamp,
            models.Tempterature.temp,
            models.Humidity.humidity,
            models.Cooling.cooling,
        )
        .join(models.Humidity, models.Tempterature.timestamp.cast(DateTime).op('=')(models.Humidity.timestamp.cast(DateTime)), isouter=True)
        .join(models.Cooling, models.Tempterature.timestamp.cast(DateTime).op('=')(models.Cooling.timestamp.cast(DateTime)), isouter=True)
        .filter(
            models.Tempterature.timestamp >= from_date,
            models.Tempterature.timestamp <= to_date,
        )
        .all()
    )
    if not records:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No records found"
        )
    return [
        {
            "timestamp": record[0],
            "temperature": record[1] if record[1] is not None else None,
            "humidity": record[2] if record[2] is not None else None,
            "cooling": record[3] if record[3] is not None else None,
        }
        for record in records
    ]


def export_records_to_csv(db: Session, from_date: datetime, to_date: datetime, measurement_id: Optional[int] = None):
    records = get_record_from_to(db, from_date, to_date, measurement_id)

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(["timestamp", "temperature", "humidity", "cooling"])

    for record in records:
        writer.writerow(
            [
                record["timestamp"],
                record["temperature"],
                record["humidity"],
                record["cooling"],
            ]
        )

    output.seek(0)
    print(output.getvalue())  # Debugging line to check CSV content
    return StreamingResponse(
        output,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=records.csv"},
    )
