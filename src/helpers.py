import os

from sqlmodel import create_engine, text

engine = create_engine(
    os.getenv(
        "DB_CONNECTION_STRING", "postgresql://postgres:postgres@localhost:5432/postgres"
    )
)


def create_database(db_name: str) -> None:
    statement = text("CREATE DATABASE :db_name")
    with engine.connect() as conn:
        conn.execute(statement, {"db_name": db_name})
        conn.commit()


def create_user(user_name: str) -> None:
    # create a user per component per partner per stage (per stage corresponds to per db)
    # for example: afrola should have 1 for pipeline0, one for pipeline1, and one for the api, all with appropriate
    # permissions (p0  reads/writes to events, p1 reads from events and reads/writes to X, api only reads X)
    # and this would all be for one stage, e.g. prod
    statement = text("CREATE USER :user_name WITH PASSWORD ':password'")
    with engine.connect() as conn:
        conn.execute(statement, {"user_name": user_name, "password": "todo"})
        conn.commit()


def grant_privileges(user_name: str, privileges: list[str]) -> None:
    pass
