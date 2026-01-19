from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.api.core.config import settings

database_url = settings.DATABASE_URL
if database_url is None:
    raise ValueError("DATABASE_URL not found.")

engine = create_engine(str(database_url))
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
