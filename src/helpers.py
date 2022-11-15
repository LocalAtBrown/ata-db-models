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
    statement = text(f"CREATE DATABASE {db_name}")
    conn.execute(statement)


def create_user(conn: Connection, user_name: str) -> None:
    statement = text(f"CREATE USER {user_name} WITH PASSWORD :password")
    conn.execute(statement, {"password": "todo"})


def grant_privileges(
    conn: Connection, user_name: str, table: str, privileges: list[Privilege]
) -> None:
    formatted_privileges = " ".join(privileges)
    statement = text(f"GRANT {formatted_privileges} ON {table} TO {user_name}")
    conn.execute(statement)


def enable_row_level_security(
    conn: Connection, table: str, target_column: str, user_name: str
) -> None:
    s1 = text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    conn.execute(s1)
    s2 = text(
        f"CREATE POLICY TODO ON {table} TO {user_name} USING (current_user LIKE '%' || {target_column} || '%')"
    )
    conn.execute(s2)
