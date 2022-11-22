from sqlalchemy.future.engine import create_engine

from ata_db_models.helpers import (
    Component,
    Grant,
    Partner,
    Privilege,
    RowLevelSecurityPolicy,
    Stage,
    assign_role,
    create_database,
    create_role,
    create_users,
    enable_row_level_security,
    get_conn_string,
    grant_privileges,
)
from ata_db_models.models import SQLModel


def pre_table_initialization(stage: Stage, components: list[Component], partner_names: list[Partner]) -> None:
    engine = create_engine(get_conn_string())

    with engine.connect() as conn:
        create_database(conn, db_name=stage)
        for component in components:
            role = f"{stage}_{component.name}"
            create_role(conn, role=role)
            usernames = [f"{stage}_{component.name}_{partner_name}" for partner_name in partner_names]
            create_users(conn, stage=stage, component=component, partner_names=partner_names)
            assign_role(conn, role=role, usernames=usernames)
        conn.commit()


def initialize_tables(stage: Stage) -> None:
    engine = create_engine(get_conn_string(db_name=stage))
    SQLModel.metadata.create_all(engine)


def post_table_initialization(stage: Stage, components: list[Component]) -> None:
    engine = create_engine(get_conn_string(db_name=stage))

    with engine.connect() as conn:
        for component in components:
            for grant in component.grants:
                for table in grant.tables:
                    grant_privileges(
                        conn, user_or_role=f"{stage}_{component.name}", table=table, privileges=grant.privileges
                    )
            for policy in component.policies:
                enable_row_level_security(
                    conn, table=policy.table, target_column=policy.user_column, role=f"{stage}_{component.name}"
                )

        conn.commit()


def initialize_all_database_entities(stage: Stage, components: list[Component], partner_names: list[Partner]) -> None:
    # needs default db
    pre_table_initialization(stage=stage, components=components, partner_names=partner_names)
    # needs to connect to this stage's db
    initialize_tables(stage=stage)
    # needs this stage's db
    post_table_initialization(stage=stage, components=components)


if __name__ == "__main__":
    stages = [Stage.dev, Stage.prod]
    pipeline0 = Component(
        name="pipeline0",
        grants=[
            Grant(privileges=[Privilege.SELECT, Privilege.INSERT, Privilege.UPDATE, Privilege.DELETE], tables=["event"])
        ],
        policies=[RowLevelSecurityPolicy(table="event", user_column="site_name")],
    )
    components = [pipeline0]
    partner_names = [Partner.afro_la, Partner.dallas_free_press, Partner.open_vallejo, Partner.the_19th]

    # roles are dev-pipeline0 and prod-pipeline0
    # users are dev-pipeline0-afro-la, dev-pipeline0-dallas-free-press, ... , prod-pipeline0-the-19th

    for stage in stages:
        initialize_all_database_entities(stage=stage, components=components, partner_names=partner_names)
