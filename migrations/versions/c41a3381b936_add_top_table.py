"""add top table

Revision ID: c41a3381b936
Revises: 2c52a5dab7d2
Create Date: 2017-08-04 16:21:01.145126

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c41a3381b936'
down_revision = '2c52a5dab7d2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('tops',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wahlperiode', sa.Integer(), nullable=True),
    sa.Column('sitzung', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('de_bundestag_plpr', sa.Column('top_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'de_bundestag_plpr', 'tops', ['top_id'], ['id'])


def downgrade():
    op.drop_constraint(None, 'de_bundestag_plpr', type_='foreignkey')
    op.drop_column('de_bundestag_plpr', 'top_id')
    op.drop_table('tops')
