from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status, File, UploadFile

from .. import schemas, database, oauth2
from sqlalchemy.orm import Session
from ..repository import cooling

get_db = database.get_db
router = APIRouter(tags=["Cooling"], prefix="/cooling")


@router.post("/", response_model=schemas.CoolingCreate)
def add_new_record(
    request: schemas.CoolingCreate,
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
):
    return cooling.add_new_record(request, db)


@router.get("/", response_model=List[schemas.Cooling])
def get_all_records(db: Session = Depends(get_db)):
    return cooling.get_all_records(db)


@router.get("/from_to", response_model=List[schemas.Cooling])
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
    return cooling.get_record_from_to(db, from_date, to_date)

@router.post("/control", status_code=status.HTTP_200_OK)
def control_cooling(
    state: bool = Query(..., description="Set to true to turn on cooling, false to turn off"),
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(oauth2.get_current_user),
    ):
    # Logic to send the command to ESP32
    if state:
        # Code to turn on cooling
        cooling.add_new_record(schemas.CoolingCreate(cooling=1), db)
        return {"message": "Cooling turned on"}
    else:
        # Code to turn off cooling
        cooling.add_new_record(schemas.CoolingCreate(cooling=0), db)
        return {"message": "Cooling turned off"} 
    
@router.get("/status", response_model=int)
def get_cooling_status(
    db: Session = Depends(get_db),
   
):
    # Logic to get the current status of the cooling system
    # This could be a database query or a call to the ESP32
    status = cooling.get_cooling_status(db)
    return status