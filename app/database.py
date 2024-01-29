from sqlmodel import SQLModel, create_engine

from .config import Settings

connect_args = {"check_same_thread": False}
engine = create_engine(Settings().DATABASE_URL, connect_args=connect_args)


def create_tables():
    SQLModel.metadata.create_all(engine)
