from fastapi import FastAPI
from . import models
from .database import engine
from contextlib import asynccontextmanager
from .database import get_db
from .routers import authentication, temperature, humidity, vibrations, cooling, export, measurement
from fastapi.middleware.cors import CORSMiddleware

# models.Base.metadata.drop_all(bind=engine)
models.Base.metadata.create_all(bind=engine)  # creates all tables in the database


@asynccontextmanager
async def lifespan(app: FastAPI):
    # this code is executed before startup
    yield
    # this code is executed before shutdown


app = FastAPI(lifespan=lifespan)

app.include_router(authentication.router)
app.include_router(temperature.router)
app.include_router(humidity.router)
app.include_router(measurement.router)
app.include_router(cooling.router)
app.include_router(export.router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can replace "*" with ["http://127.0.0.1:5500"] for more security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
