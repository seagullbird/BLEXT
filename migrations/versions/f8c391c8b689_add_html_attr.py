"""add html attr

Revision ID: f8c391c8b689
Revises: 339b0274997c
Create Date: 2016-10-27 16:25:41.120610

"""

# revision identifiers, used by Alembic.
revision = 'f8c391c8b689'
down_revision = '339b0274997c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('blogs', sa.Column('html', sa.Text(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('blogs', 'html')
    ### end Alembic commands ###
