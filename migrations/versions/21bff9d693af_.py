"""empty message

Revision ID: 21bff9d693af
Revises: ae8f840cc666
Create Date: 2023-12-07 05:15:50.857380

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '21bff9d693af'
down_revision = 'ae8f840cc666'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('accountNumber', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_column('accountNumber')

    # ### end Alembic commands ###
