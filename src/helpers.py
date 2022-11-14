import os

from sqlmodel import Session, create_engine


engine = create_engine(os.getenv("DB_CONNECTION_STRING"))


def get_session() -> Session:
    return Session(engine, autocommit=False, autoflush=False)


def create_databases():
    pass


def create_users():
    pass
