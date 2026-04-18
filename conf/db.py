import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DB_URL = os.getenv(
    "DB_URL",
    "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres",
)

engine = create_engine(DB_URL, echo=False, future=True)
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)
