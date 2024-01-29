from functools import lru_cache

from sqlmodel import Session

from .config import Settings
from .database import engine


@lru_cache
def get_settings():
    return Settings()


def get_session():
    with Session(engine) as session:
        yield session
