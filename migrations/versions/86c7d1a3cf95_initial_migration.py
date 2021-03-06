"""Initial Migration

Revision ID: 86c7d1a3cf95
Revises: 
Create Date: 2021-06-14 21:22:47.491754

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '86c7d1a3cf95'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('favorite_color', sa.String(length=120), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'favorite_color')
    # ### end Alembic commands ###
