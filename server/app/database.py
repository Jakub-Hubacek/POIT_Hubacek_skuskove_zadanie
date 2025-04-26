from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = 'postgresql://admin:admin@postgresql:5432/gem-manager' #conn for deployment
SQLALCHEMY_DATABASE_URL = (
    "postgresql://admin:admin@postgresql:5432/poit"  # conn for local
)

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
