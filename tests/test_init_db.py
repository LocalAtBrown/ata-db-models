import pytest
from sqlalchemy import create_engine, text

from src.helpers import (
    Component,
    Grant,
    Partner,
    Privilege,
    RowLevelSecurityPolicy,
    Stage,
    get_conn_string,
)
from src.init_db import pre_table_initialization


@pytest.fixture
def components():
    pipeline_uno = Component(
        name="pipeline_uno",
        grants=[
            Grant(privileges=[Privilege.SELECT, Privilege.INSERT, Privilege.UPDATE, Privilege.DELETE], tables=["events"])
        ],
        policies=[RowLevelSecurityPolicy(table="events", user_column="partner")],
    )

    pipeline_duo = Component(
        name="pipeline_duo",
        grants=[Grant(privileges=[Privilege.SELECT], tables=["events"])],
        policies=[RowLevelSecurityPolicy(table="events", user_column="partner")],
    )

    return [pipeline_uno, pipeline_duo]


@pytest.fixture
def partners():
    return [Partner.afro_la, Partner.dallas_free_press]


def test_pre_table_initialization(components, partners):
    # run function
    stage = Stage.dev
    pre_table_initialization(stage=stage, components=components, partner_names=partners)

    engine = create_engine(get_conn_string(db_name="postgres"))
    with engine.connect() as conn:
        # make sure db exists
        statement = text("SELECT 1 AS result FROM pg_database WHERE datname=:db_name")
        result = conn.execute(statement, {"db_name": stage})
        result_data = result.fetchone()
        assert result_data[0] == 1

        # check if roles exist
        role_name_literals = [f"'{stage}_{component.name}'" for component in components]
        formatted_role_names = ", ".join(role_name_literals)
        statement = text(f"SELECT COUNT(*) AS result FROM pg_authid WHERE rolname IN ({formatted_role_names})")
        result = conn.execute(statement)
        result_data = result.fetchone()
        assert result_data[0] == len(components)

        # check if users exist
        username_literals = []
        for component in components:
            names_to_add = [f"'{stage}_{component.name}_{partner_name}'" for partner_name in partners]
            username_literals.extend(names_to_add)
        formatted_usernames = ", ".join(username_literals)
        statement = text(f"SELECT COUNT(*) AS result FROM pg_authid WHERE rolname IN ({formatted_usernames})")
        result = conn.execute(statement)
        result_data = result.fetchone()
        assert result_data[0] == len(components) * len(partners)

        # check if users are in correct roles
        for component in components:
            statement = text(
                f"WITH t AS (SELECT pg_auth_members.member from pg_authid "
                f"JOIN pg_auth_members ON oid = roleid "
                f"WHERE rolname = :role_name) "
                f"SELECT rolname FROM t JOIN pg_authid ON member = oid"
            )
            result = conn.execute(statement, {"role_name": f"{stage}_{component.name}"})
            result_data = result.fetchall()
            assert len(result_data) == len(partners)
            expected_usernames = [f"{stage}_{component.name}_{partner_name}" for partner_name in partners]
            assert sorted([row[0] for row in result_data]) == sorted(expected_usernames)


def test_post_table_initialization():
    pass
