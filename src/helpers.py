from enum import Enum

from sqlalchemy.future.engine import Connection
from sqlmodel import text


class Privilege(str, Enum):
    """
    Possible privileges to grant to Postgres users: https://www.postgresql.org/docs/15/ddl-priv.html
    """

    SELECT = "SELECT"
    INSERT = "INSERT"
    UPDATE = "UPDATE"
    DELETE = "DELETE"
    TRUNCATE = "TRUNCATE"
    REFERENCES = "REFERENCES"
    TRIGGER = "TRIGGER"
    CREATE = "CREATE"
    CONNECT = "CONNECT"
    TEMPORARY = "TEMPORARY"
    EXECUTE = "EXECUTE"
    USAGE = "USAGE"
    SET = "SET"
    ALTER_SYSTEM = "ALTER_SYSTEM"


def create_database(conn: Connection, db_name: str) -> None:
    statement = text("CREATE DATABASE :db_name")
    conn.execute(statement, {"db_name": db_name})


def create_user(conn: Connection, user_name: str) -> None:
    statement = text("CREATE USER :user_name WITH PASSWORD ':password'")
    conn.execute(statement, {"user_name": user_name, "password": "todo"})


def grant_privileges(
    conn: Connection, user_name: str, table: str, privileges: list[Privilege]
) -> None:
    formatted_privileges = " ".join(privileges)
    statement = text(f"GRANT :formatted_privileges ON :table TO :user_name")
    conn.execute(
        statement,
        {
            "formatted_privileges": formatted_privileges,
            "table": table,
            "user_name": user_name,
        },
    )
