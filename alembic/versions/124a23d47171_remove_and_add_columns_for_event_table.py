"""remove and add columns for event table

Revision ID: 124a23d47171
Revises: 73bdc21caa16
Create Date: 2023-02-14 11:59:21.849593

"""
import sqlalchemy as sa
import sqlmodel
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "124a23d47171"
down_revision = "73bdc21caa16"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("event", sa.Column("br_viewheight", sa.Float(), nullable=True))
    op.add_column("event", sa.Column("br_viewwidth", sa.Float(), nullable=True))
    op.add_column("event", sa.Column("refr_urlhost", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.add_column("event", sa.Column("refr_urlpath", sqlmodel.sql.sqltypes.AutoString(), nullable=True))
    op.drop_column("event", "network_userid")
    op.drop_column("event", "unstruct_event_com_snowplowanalytics_snowplow_change_form_1")
    op.drop_column("event", "unstruct_event_com_snowplowanalytics_snowplow_focus_form_1")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "event",
        sa.Column(
            "unstruct_event_com_snowplowanalytics_snowplow_focus_form_1",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column(
        "event",
        sa.Column(
            "unstruct_event_com_snowplowanalytics_snowplow_change_form_1",
            postgresql.JSON(astext_type=sa.Text()),
            autoincrement=False,
            nullable=True,
        ),
    )
    op.add_column("event", sa.Column("network_userid", postgresql.UUID(), autoincrement=False, nullable=False))
    op.drop_column("event", "refr_urlpath")
    op.drop_column("event", "refr_urlhost")
    op.drop_column("event", "br_viewwidth")
    op.drop_column("event", "br_viewheight")
    # ### end Alembic commands ###
