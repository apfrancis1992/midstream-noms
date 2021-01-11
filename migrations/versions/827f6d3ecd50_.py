"""empty message

Revision ID: 827f6d3ecd50
Revises: ff0c4c48577b
Create Date: 2021-01-10 14:18:29.350937

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '827f6d3ecd50'
down_revision = 'ff0c4c48577b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('access', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'access')
    # ### end Alembic commands ###
