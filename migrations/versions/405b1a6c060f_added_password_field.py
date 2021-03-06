"""added password field

Revision ID: 405b1a6c060f
Revises: 86c7d1a3cf95
Create Date: 2021-06-16 20:37:15.086777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '405b1a6c060f'
down_revision = '86c7d1a3cf95'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'password_hash')
    # ### end Alembic commands ###
