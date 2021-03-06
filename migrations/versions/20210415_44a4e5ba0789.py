"""Add ingredients"""
import sqlalchemy as sa

from alembic import op

revision = "44a4e5ba0789"
down_revision = "a45ff594aad8"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table("ingredient", sa.Column("name", sa.String(), nullable=False), sa.PrimaryKeyConstraint("name"))
    op.create_table(
        "recipe_ingredient",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("recipe_title", sa.String(), nullable=True),
        sa.Column("ingredient_name", sa.String(), nullable=True),
        sa.Column("quantity", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(
            ["ingredient_name"],
            ["ingredient.name"],
        ),
        sa.ForeignKeyConstraint(
            ["recipe_title"],
            ["recipe.title"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("recipe_ingredient")
    op.drop_table("ingredient")
    # ### end Alembic commands ###
