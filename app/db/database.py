from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import create_engine
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://restaurant_user:restaurant_password@localhost:5432/restaurant_db")

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
