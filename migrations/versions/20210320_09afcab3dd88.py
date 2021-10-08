"""Add Recipe table"""
import sqlalchemy as sa

from alembic import op

revision = "09afcab3dd88"
down_revision = "42ffb12de511"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "recipe",
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("image", sa.String(), nullable=True),
        sa.Column("active_cook", sa.Integer(), nullable=True),
        sa.Column("total_cook", sa.Integer(), nullable=True),
        sa.Column("serves", sa.Integer(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("instructions", sa.String(), nullable=True),
        sa.Column("url", sa.String(), nullable=True),
        sa.Column("category_name", sa.String(), nullable=True),
        sa.Column("profile_name", sa.String(), nullable=True),
        sa.Column("updated", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_name"],
            ["category.name"],
        ),
        sa.PrimaryKeyConstraint("title"),
    )
    op.create_index(op.f("ix_recipe_category_name"), "recipe", ["category_name"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_recipe_category_name"), table_name="recipe")
    op.drop_table("recipe")
