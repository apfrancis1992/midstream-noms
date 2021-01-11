"""empty message

Revision ID: 35b1e25f9c56
Revises: 827f6d3ecd50
Create Date: 2021-01-10 14:22:41.192587

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '35b1e25f9c56'
down_revision = '827f6d3ecd50'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('access',
    sa.Column('access_id', sa.Integer(), nullable=False),
    sa.Column('access_name', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('access_id')
    )
    op.create_foreign_key(None, 'user', 'access', ['access'], ['access_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user', type_='foreignkey')
    op.drop_table('access')
    # ### end Alembic commands ###
