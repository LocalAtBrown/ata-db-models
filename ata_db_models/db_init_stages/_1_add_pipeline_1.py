from ata_db_models.helpers import (
    Component,
    Grant,
    Partner,
    Privilege,
    RowLevelSecurityPolicy,
    Stage,
    post_table_initialization,
    pre_table_initialization,
)


def add_pipeline_1(stage: Stage, components: list[Component], partner_names: list[Partner]) -> None:
    pre_table_initialization(stage=stage, components=components, partner_names=partner_names, create_dbs=False)
    # SQLAlchemy is idempotent so running this wouldn't break anything, but we don't need to run it
    # initialize_tables(stage=stage)
    post_table_initialization(stage=stage, components=components)


if __name__ == "__main__":
    stages = [Stage.dev, Stage.prod]
    pipeline1 = Component(
        name="pipeline1",
        grants=[
            Grant(privileges=[Privilege.SELECT], tables=["event"]),
            Grant(
                privileges=[Privilege.SELECT, Privilege.INSERT, Privilege.UPDATE, Privilege.DELETE],
                tables=["prescription"],
            ),
        ],
        policies=[
            RowLevelSecurityPolicy(table="event", user_column="site_name"),
            RowLevelSecurityPolicy(table="prescription", user_column="site_name"),
        ],
    )
    components = [pipeline1]
    partner_names = [Partner.afro_la, Partner.dallas_free_press, Partner.open_vallejo, Partner.the_19th]

    for stage in stages:
        add_pipeline_1(stage=stage, components=components, partner_names=partner_names)
