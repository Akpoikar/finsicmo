from contextlib import contextmanager
from typing import Generator
from sqlalchemy.orm import Session
from .schema import SessionLocal

@contextmanager
def get_session() -> Generator[Session, None, None]:
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_db_session() -> Session:
    return SessionLocal()

# Quick test - remove later
if __name__ == "__main__":
    with get_session() as session:
        print("DB connection works!")
        # Add test data here maybe? 