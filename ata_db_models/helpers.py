import json
import os
import random
import secrets
import string
from dataclasses import dataclass
from enum import Enum
from typing import Optional

import boto3
from mypy_boto3_ssm import SSMClient
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


class Stage(str, Enum):
    dev = "dev"
    prod = "prod"


class Partner(str, Enum):
    afro_la = "afro_la"
    dallas_free_press = "dallas_free_press"
    open_vallejo = "open_vallejo"
    the_19th = "the_19th"


@dataclass
class Grant:
    privileges: list[Privilege]
    tables: list[str]


@dataclass
class RowLevelSecurityPolicy:
    # TODO have table and user_column reference actual Table and Column objects
    table: str
    user_column: str
    policy_name: Optional[str] = None


@dataclass
class Component:
    # effectively a db-constrained role
    name: str
    grants: list[Grant]
    policies: list[RowLevelSecurityPolicy]


@dataclass
class DatabaseConnectionCredentials:
    HOST: str
    PORT: int
    DB_NAME: str
    USERNAME: str
    PASSWORD: str


def create_database(conn: Connection, db_name: Stage) -> None:
    statement = text(f"CREATE DATABASE {db_name}")
    conn.execution_options(isolation_level="AUTOCOMMIT").execute(statement)


def create_role(conn: Connection, role: str) -> None:
    statement = text(f"CREATE ROLE {role}")
    conn.execute(statement)


def generate_password() -> str:
    alphabet = string.ascii_letters + string.digits
    while True:
        password = "".join(secrets.choice(alphabet) for i in range(10))
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
        ):
            break
    return password


def create_user(conn: Connection, username: str) -> str:
    pw = generate_password()
    statement = text(f"CREATE USER {username} WITH PASSWORD :password")
    conn.execute(statement, {"password": pw})
    return pw


def assign_role(conn: Connection, role: str, usernames: list[str]) -> None:
    users = ", ".join(usernames)
    statement = text(f"GRANT {role} TO {users}")
    conn.execute(statement)


def grant_privileges(conn: Connection, user_or_role: str, table: str, privileges: list[Privilege]) -> None:
    formatted_privileges = ", ".join(privileges)
    statement = text(f"GRANT {formatted_privileges} ON {table} TO {user_or_role}")
    conn.execute(statement)


def enable_row_level_security(conn: Connection, table: str, target_column: str, role: str) -> None:
    s1 = text(f"ALTER TABLE {table} ENABLE ROW LEVEL SECURITY")
    conn.execute(s1)
    random_postfix = "%06x" % random.randrange(16**6)
    policy_name = f"{table}_{role}_{random_postfix}"
    s2 = text(f"CREATE POLICY {policy_name} ON {table} TO {role} USING (current_user LIKE '%' || {target_column} || '%')")
    conn.execute(s2)


def create_users(conn: Connection, stage: Stage, component: Component, partner_names: list[Partner]) -> None:
    ssm_client = get_ssm_client()
    for partner_name in partner_names:
        username = f"{stage}_{component.name}_{partner_name}"
        pw = create_user(conn, username=username)
        if ssm_client:
            user_creds = DatabaseConnectionCredentials(
                HOST=os.getenv("HOST", "localhost"),
                PORT=int(os.getenv("PORT", "5432")),
                DB_NAME=stage,
                USERNAME=username,
                PASSWORD=pw,
            )
            ssm_client.put_parameter(
                Name=f"/{stage}/ata/{partner_name}/{component.name}/database-credentials",
                Description=f"DB credentials for partner {partner_name}, component {component}, and env {stage}.",
                Value=json.dumps(user_creds.__dict__),
                Type="String",
                Overwrite=True,
            )


def get_conn_string(db_name: Optional[str] = None) -> str:
    # everything but dbname should be the same, since we are using the admin user for everything
    host = os.getenv("HOST", "localhost")
    port = os.getenv("PORT", "5432")
    user = os.getenv("USERNAME", "postgres")
    password = os.getenv("PASSWORD", "postgres")
    if not db_name:
        # if no db_name is passed, we assume it is for the default db. This is assumed to be "default"
        # unless indicated otherwise via this DB_NAME env var
        db_name = os.getenv("DB_NAME", "default")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


def get_ssm_client() -> Optional[SSMClient]:
    # ENABLE_SSM has to explicitly be set to exactly "TRUE" or else no SSM interactions take place
    if os.getenv("ENABLE_SSM", "FALSE") == "TRUE":
        return boto3.client("ssm")
    else:
        return None
