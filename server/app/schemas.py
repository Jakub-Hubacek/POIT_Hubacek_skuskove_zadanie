from typing import List, Optional, TypeVar, Generic
from pydantic import BaseModel
from datetime import date
from datetime import datetime


DataT = TypeVar("DataT")


class Pagination(BaseModel, Generic[DataT]):
    total: int
    count: int
    data: List[DataT]

class TokenData(BaseModel):
    username: Optional[str] = None


class RefreshToken(BaseModel):
    refresh_token: str


class User(BaseModel):
    username: str
    password: str


class ShowUser(BaseModel):
    username: str
    class Config:
        from_attributes = True


class TemperatureCreate(BaseModel):
    temp: float
    timestamp: datetime


class Temperature(BaseModel):
    id: int
    timestamp: datetime
    temp: float

    class Config:
        from_attributes = True


class HumidityCreate(BaseModel):
    humidity: float
    timestamp: datetime


class Humidity(BaseModel):
    id: int
    timestamp: datetime
    humidity: float

    class Config:
        from_attributes = True


class VibrationsCreate(BaseModel):
    vibration_level: float


class Vibrations(BaseModel):
    id: int
    timestamp: datetime
    vibration_level: float

    class Config:
        from_attributes = True


class CoolingCreate(BaseModel):
    cooling: int
    timestamp: datetime
    
    
class Cooling(BaseModel):
    id: int
    timestamp: datetime
    cooling: int

    class Config:
        from_attributes = True
        
class CoolingStatus(BaseModel):
    cooling: int

    class Config:
        from_attributes = True