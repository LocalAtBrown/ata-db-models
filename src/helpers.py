import os

from sqlmodel import Session, create_engine


engine = create_engine(os.getenv("DB_CONNECTION_STRING", "postgresql://postgres:postgres@localhost:5432/postgres"))


def get_session() -> Session:
    return Session(engine, autocommit=False, autoflush=False)


def create_databases() -> None:
    pass


def create_users() -> None:
    pass
