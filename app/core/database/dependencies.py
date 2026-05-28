from typing import Generator
from sqlalchemy.orm import Session
from app.core.database.connection import connection


def get_db(db_name: str) -> Generator[Session, None, None]:
    SessionLocal = connection.get_session(db_name)

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
