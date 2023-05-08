from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from configurations import DBConfigurations

engine = create_engine(
    DBConfigurations.sql_alchemy_url,
    pool_recycle=3600,
    echo=False,
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)


def get_db() -> Session:
    return SessionLocal()


@contextmanager
def get_context_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
