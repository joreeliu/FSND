"""empty message

Revision ID: 36fb9d673d4d
Revises: 70fad21df34f
Create Date: 2020-06-19 23:32:47.297611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '36fb9d673d4d'
down_revision = '70fad21df34f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('Artist_Show',
    sa.Column('artist_id', sa.Integer(), nullable=False),
    sa.Column('show_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['artist_id'], ['Artist.id'], ),
    sa.ForeignKeyConstraint(['show_id'], ['Show.id'], ),
    sa.PrimaryKeyConstraint('artist_id', 'show_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('Artist_Show')
    # ### end Alembic commands ###