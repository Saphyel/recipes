"""Add user table"""
import sqlalchemy as sa

from alembic import op

revision = "61b3cdf1369f"
down_revision = "44a4e5ba0789"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "user",
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("name"),
    )


def downgrade() -> None:
    op.drop_table("user")
