"""Add category"""
import sqlalchemy as sa

from alembic import op

revision = "42ffb12de511"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table("category", sa.Column("name", sa.String(), nullable=False), sa.PrimaryKeyConstraint("name"))


def downgrade() -> None:
    op.drop_table("category")
