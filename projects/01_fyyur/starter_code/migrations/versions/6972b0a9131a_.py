"""empty message

Revision ID: 6972b0a9131a
Revises: 36fb9d673d4d
Create Date: 2020-06-20 15:04:38.359551

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6972b0a9131a'
down_revision = '36fb9d673d4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('Artist_Show_show_id_fkey', 'Artist_Show', type_='foreignkey')
    op.drop_constraint('Artist_Show_artist_id_fkey', 'Artist_Show', type_='foreignkey')
    op.create_foreign_key(None, 'Artist_Show', 'Show', ['show_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'Artist_Show', 'Artist', ['artist_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('Genres_Artists_artist_id_fkey', 'Genres_Artists', type_='foreignkey')
    op.drop_constraint('Genres_Artists_genre_id_fkey', 'Genres_Artists', type_='foreignkey')
    op.create_foreign_key(None, 'Genres_Artists', 'Artist', ['artist_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'Genres_Artists', 'Genre', ['genre_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('Genres_Venue_genre_id_fkey', 'Genres_Venue', type_='foreignkey')
    op.drop_constraint('Genres_Venue_venue_id_fkey', 'Genres_Venue', type_='foreignkey')
    op.create_foreign_key(None, 'Genres_Venue', 'Genre', ['genre_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'Genres_Venue', 'Venue', ['venue_id'], ['id'], ondelete='CASCADE')
    op.drop_constraint('Venue_Show_show_id_fkey', 'Venue_Show', type_='foreignkey')
    op.drop_constraint('Venue_Show_venue_id_fkey', 'Venue_Show', type_='foreignkey')
    op.create_foreign_key(None, 'Venue_Show', 'Venue', ['venue_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key(None, 'Venue_Show', 'Show', ['show_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'Venue_Show', type_='foreignkey')
    op.drop_constraint(None, 'Venue_Show', type_='foreignkey')
    op.create_foreign_key('Venue_Show_venue_id_fkey', 'Venue_Show', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key('Venue_Show_show_id_fkey', 'Venue_Show', 'Show', ['show_id'], ['id'])
    op.drop_constraint(None, 'Genres_Venue', type_='foreignkey')
    op.drop_constraint(None, 'Genres_Venue', type_='foreignkey')
    op.create_foreign_key('Genres_Venue_venue_id_fkey', 'Genres_Venue', 'Venue', ['venue_id'], ['id'])
    op.create_foreign_key('Genres_Venue_genre_id_fkey', 'Genres_Venue', 'Genre', ['genre_id'], ['id'])
    op.drop_constraint(None, 'Genres_Artists', type_='foreignkey')
    op.drop_constraint(None, 'Genres_Artists', type_='foreignkey')
    op.create_foreign_key('Genres_Artists_genre_id_fkey', 'Genres_Artists', 'Genre', ['genre_id'], ['id'])
    op.create_foreign_key('Genres_Artists_artist_id_fkey', 'Genres_Artists', 'Artist', ['artist_id'], ['id'])
    op.drop_constraint(None, 'Artist_Show', type_='foreignkey')
    op.drop_constraint(None, 'Artist_Show', type_='foreignkey')
    op.create_foreign_key('Artist_Show_artist_id_fkey', 'Artist_Show', 'Artist', ['artist_id'], ['id'])
    op.create_foreign_key('Artist_Show_show_id_fkey', 'Artist_Show', 'Show', ['show_id'], ['id'])
    # ### end Alembic commands ###
