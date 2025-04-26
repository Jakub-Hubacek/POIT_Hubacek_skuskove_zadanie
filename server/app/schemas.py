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