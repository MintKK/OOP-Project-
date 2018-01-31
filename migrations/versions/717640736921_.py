"""empty message

Revision ID: 717640736921
Revises: 
Create Date: 2018-01-28 13:58:32.465447

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '717640736921'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('organisations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('email', sa.String(), nullable=True),
    sa.Column('address', sa.String(), nullable=True),
    sa.Column('phone', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('organisations')
    # ### end Alembic commands ###
