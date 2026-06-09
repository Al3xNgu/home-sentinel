import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, sessionmaker

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is missing from environment")

class Base(DeclarativeBase):
    pass

engine = create_engine(DATABASE_URL)

with engine.connect() as connection:
    connection.execute(text("SELECT 1"))
    print("DB connection successful")

import app.models
Base.metadata.create_all(bind=engine)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def get_db():
    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()