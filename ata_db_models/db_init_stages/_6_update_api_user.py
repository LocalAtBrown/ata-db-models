from sqlalchemy.future.engine import create_engine

from ata_db_models.helpers import (
    Component,
    Grant,
    Privilege,
    Stage,
    get_conn_string,
    grant_privileges,
)

# Give dev_api and prod_api users SELECT privilege to the event table
if __name__ == "__main__":
    stages = [Stage.dev, Stage.prod]
    reader = Component(name="api", grants=[Grant(privileges=[Privilege.SELECT], tables=["event"])], policies=[])

    for stage in stages:
        username = f"{stage}_{reader.name}"
        stage_engine = create_engine(get_conn_string(db_name=stage))

        with stage_engine.connect() as conn:
            for grant in reader.grants:
                for table in grant.tables:
                    grant_privileges(conn=conn, user_or_role=username, table=table, privileges=grant.privileges)
            conn.commit()
