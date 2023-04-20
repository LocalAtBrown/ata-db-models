from sqlalchemy.future.engine import create_engine

from ata_db_models.helpers import (
    Component,
    Grant,
    Privilege,
    Stage,
    get_conn_string,
    get_ssm_client,
    grant_privileges,
)

if __name__ == "__main__":
    stages = [Stage.dev, Stage.prod]
    reader = Component(
        name="api", grants=[Grant(privileges=[Privilege.SELECT, Privilege.INSERT], tables=["usergroup"])], policies=[]
    )

    for stage in stages:
        engine = create_engine(get_conn_string())
        ssm_client = get_ssm_client()
        username = f"{stage}_{reader.name}"

        stage_engine = create_engine(get_conn_string(db_name=stage))
        with stage_engine.connect() as conn:
            for grant in reader.grants:
                for table in grant.tables:
                    grant_privileges(conn=conn, user_or_role=username, table=table, privileges=grant.privileges)
            conn.commit()
