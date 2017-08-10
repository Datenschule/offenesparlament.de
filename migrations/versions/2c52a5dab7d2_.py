"""initial migration

Revision ID: 2c52a5dab7d2
Revises: 
Create Date: 2017-08-04 15:12:35.330459

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c52a5dab7d2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('de_bundestag_plpr',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('wahlperiode', sa.Integer(), nullable=True),
    sa.Column('sitzung', sa.Integer(), nullable=True),
    sa.Column('sequence', sa.Integer(), nullable=True),
    sa.Column('speaker_cleaned', sa.String(), nullable=True),
    sa.Column('speaker_party', sa.String(), nullable=True),
    sa.Column('speaker', sa.String(), nullable=True),
    sa.Column('speaker_fp', sa.String(), nullable=True),
    sa.Column('type', sa.String(), nullable=True),
    sa.Column('text', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )

def downgrade():
    op.drop_table('de_bundestag_plpr')
