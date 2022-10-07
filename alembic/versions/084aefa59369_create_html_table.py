"""create Html table

Revision ID: 084aefa59369
Revises: 
Create Date: 2022-10-07 20:04:03.718352

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "084aefa59369"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "tblHtml",
        sa.Column("key", sa.VARCHAR(), autoincrement=False, nullable=False),
        sa.Column("html", sa.TEXT(), autoincrement=False, nullable=True),
        sa.PrimaryKeyConstraint("key", name="tblHtml_pkey"),
    )
    op.create_index("ix_tblHtml_key", "tblHtml", ["key"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ix_tblHtml_key", table_name="tblHtml")
    op.drop_table("tblHtml")
    # ### end Alembic commands ###