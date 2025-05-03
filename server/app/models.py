from .database import Base
from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, Date, Enum, Float


class User(Base):
    __tablename__ = "users"
    username = Column(String, primary_key=True, unique=True, nullable=False)
    password = Column(String)

class Tempterature(Base):
    __tablename__ = "temp_data"
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    temp = Column(Float, nullable=False)    


class Humidity(Base):
    __tablename__ = "humidity_data"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    humidity = Column(Float, nullable=False)


class Vibrations(Base):
    __tablename__ = "vibration_data"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    vibration_level = Column(Float, nullable=False)


class Cooling(Base):
    __tablename__ = "cooling_data"
    id = Column(
        Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    timestamp = Column(DateTime, nullable=False)
    cooling = Column(Integer, nullable=False)


class Measurement(Base):
    __tablename__ = "measurements"
    id = Column(Integer, primary_key=True, unique=True, nullable=False, autoincrement=True)
    from_timestamp = Column(DateTime, nullable=False)
    to_timestamp = Column(DateTime, nullable=True)