"""SQLAlchemy Database configuration and session management."""

import os

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from pharma_platform.configuration.settings import get_settings

Base = declarative_base()

_engine = None
_SessionLocal = None


def get_engine():
    global _engine
    if _engine is None:
        settings = get_settings()
        db_url = settings.database_url
        if db_url.startswith("sqlite"):
            # Ensure local directory exists
            db_path = db_url.replace("sqlite:///", "")
            if db_path and not db_path.startswith(":memory:"):
                os.makedirs(os.path.dirname(os.path.abspath(db_path)), exist_ok=True)
            _engine = create_engine(db_url, connect_args={"check_same_thread": False})
        else:
            _engine = create_engine(db_url)
    return _engine


def get_session():
    global _SessionLocal
    if _SessionLocal is None:
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=get_engine())
    return _SessionLocal()


def init_db():
    """Create all tables in the database."""
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
