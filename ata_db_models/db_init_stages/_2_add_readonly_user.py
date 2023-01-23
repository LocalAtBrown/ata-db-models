import json
import os

from sqlalchemy.future.engine import create_engine

from ata_db_models.helpers import (
    Component,
    DatabaseConnectionCredentials,
    Grant,
    Privilege,
    Stage,
    create_user,
    get_conn_string,
    get_ssm_client,
    grant_privileges,
)

if __name__ == "__main__":
    stages = [Stage.dev, Stage.prod]
    reader = Component(
        name="reader", grants=[Grant(privileges=[Privilege.SELECT], tables=["event", "prescription"])], policies=[]
    )

    for stage in stages:
        engine = create_engine(get_conn_string())
        ssm_client = get_ssm_client()
        username = f"{stage}_{reader.name}"
        with engine.connect() as conn:
            pw = create_user(conn, username=username, bypassrls=True)
            conn.commit()

        stage_engine = create_engine(get_conn_string(db_name=stage))
        with stage_engine.connect() as conn:
            for grant in reader.grants:
                for table in grant.tables:
                    grant_privileges(conn=conn, user_or_role=username, table=table, privileges=grant.privileges)
            conn.commit()

        if ssm_client:
            user_creds = DatabaseConnectionCredentials(
                HOST=os.getenv("HOST", "localhost"),
                PORT=int(os.getenv("PORT", "5432")),
                DB_NAME=stage,
                USERNAME=username,
                PASSWORD=pw,
            )
            ssm_client.put_parameter(
                Name=f"/{stage}/ata/{reader.name}/all/database-credentials",
                Description=f"DB credentials for a read-only user, for {stage}.",
                Value=json.dumps(user_creds.__dict__),
                Type="String",
                Overwrite=True,
            )
