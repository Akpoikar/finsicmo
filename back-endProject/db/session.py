from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from .schema import engine

Session = sessionmaker(bind=engine)

@contextmanager
def get_session():
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()

# Quick test - remove later
if __name__ == "__main__":
    with get_session() as session:
        print("DB connection works!")
        # Add test data here maybe? 