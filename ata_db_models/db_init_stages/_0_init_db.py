from ata_db_models.helpers import (
    Component,
    Grant,
    Partner,
    Privilege,
    RowLevelSecurityPolicy,
    Stage,
    initialize_tables,
    post_table_initialization,
    pre_table_initialization,
)


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
