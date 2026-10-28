# creating sqlalhemy engine nd session

from sqlalchemy import create_engine, URL
from sqlalchemy.orm import Session,sessionmaker

from app.core.config import settings

from collections.abc import Generator

database_url = URL.create(  # creating database url
    drivername="postgresql+psycopg",  # tells sqlalchemy to use postgres through psycopg driver
    username=settings.db_user,
    password=settings.db_password,
    host=settings.db_host,
    port=settings.db_port,
    database=settings.db_name,
)

engine = create_engine(database_url)

SessionLocal = sessionmaker(  # creating a session factory ,prepares a factory for creating sessions
    bind=engine,
    autoflush=False,
    autocommit=False,
)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()  # calling the session factory

    try:
        yield db # like return ,yield pauses the fxn nd provide the session to fastapi, fasatapi can uses that session while processing the request 
    finally:
        db.close()  # once the request finishes ,fastapi closes the session

