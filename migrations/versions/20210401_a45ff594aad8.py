"""Add User table"""
import sqlalchemy as sa

from alembic import op

revision = 'a45ff594aad8'
down_revision = '09afcab3dd88'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'user',
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('reddit', sa.String(), nullable=True),
        sa.Column('instagram', sa.String(), nullable=True),
        sa.Column('twitter', sa.String(), nullable=True),
        sa.PrimaryKeyConstraint('name')
    )
    op.create_foreign_key(None, 'recipe', 'user', ['user_name'], ['name'])


def downgrade() -> None:
    op.drop_constraint(None, 'recipe', type_='foreignkey')
    op.drop_table('user')
