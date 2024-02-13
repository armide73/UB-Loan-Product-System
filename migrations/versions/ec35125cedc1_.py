"""empty message

Revision ID: ec35125cedc1
Revises: 21bff9d693af
Create Date: 2023-12-07 05:29:12.442252

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ec35125cedc1'
down_revision = '21bff9d693af'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('administration', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profilePic', sa.String(length=100), nullable=True))

    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profilePic', sa.String(length=100), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('client', schema=None) as batch_op:
        batch_op.drop_column('profilePic')

    with op.batch_alter_table('administration', schema=None) as batch_op:
        batch_op.drop_column('profilePic')

    # ### end Alembic commands ###
