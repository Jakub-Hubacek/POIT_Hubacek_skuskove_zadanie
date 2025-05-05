from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session

# Load environment variables from .env file
load_dotenv()

# Get the database URL from the environment
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")
if not SQLALCHEMY_DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment")

# SQLALCHEMY_DATABASE_URL = (
#     "postgresql://admin:admin@postgresql:5432/poit"  # conn for local
# )

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_pre_ping=True,  # Test the connection before using it from the pool
    pool_recycle=3600,  # Recycle connections after 1 hour
    connect_args={},
)


SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Initialize the database with a user
       

        # Call the init_db function to initialize the user
        init_db()

def init_db():
    from app.models import User  # Assuming you have a User model defined in app.models
    db: Session = SessionLocal()
    try:
        # Check if the user already exists
        user = db.query(User).filter(User.name == "jakub").first()
        if not user:
            # Add the user if it doesn't exist
            new_user = User(
                name="jakub",
                password="$2a$12$kqCQXu4xhtyo5rYKUtNe9uutnrA/EW3mUo6uE3flaso5aw9udodz6",
            )
            db.add(new_user)
            db.commit()
    finally:
        db.close()
