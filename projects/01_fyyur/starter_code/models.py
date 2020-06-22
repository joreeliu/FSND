from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#

Genres_Venue = db.Table('Genres_Venue',
                        db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'),
                                  primary_key=True),
                        db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id', ondelete='CASCADE'),
                                  primary_key=True)
                        )

Genres_Artists = db.Table('Genres_Artists',
                          db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'),
                                    primary_key=True),
                          db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id', ondelete='CASCADE'),
                                    primary_key=True)
                          )

Venue_Show = db.Table('Venue_Show',
                      db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'),
                                primary_key=True),
                      db.Column('show_id', db.Integer, db.ForeignKey('Show.id', ondelete='CASCADE'), primary_key=True)
                      )

Artist_Show = db.Table('Artist_Show',
                       db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'),
                                 primary_key=True),
                       db.Column('show_id', db.Integer, db.ForeignKey('Show.id', ondelete='CASCADE'), primary_key=True)
                       )


class Genre(db.Model):
    __tablename__ = 'Genre'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)


class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))

    genres_venues = db.relationship('Genre', secondary=Genres_Venue, backref=db.backref('genres_venues', lazy=True),
                                    cascade='all, delete')
    show_venue = db.relationship('Show', secondary=Venue_Show, backref=db.backref('show_venue', lazy=True),
                                 cascade="all,delete")


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(500))
    genres_artists = db.relationship('Genre', secondary=Genres_Artists, backref=db.backref('genres_artists', lazy=True),
                                     cascade='all, delete')
    artist_show = db.relationship('Show', secondary=Artist_Show, backref=db.backref('artist_show', lazy=True),
                                  cascade='all, delete')


class Show(db.Model):
    __tablename__ = 'Show'

    id = db.Column(db.Integer, primary_key=True)

    start_time = db.Column(db.DateTime)

    venue_show = db.relationship('Venue', secondary=Venue_Show, backref=db.backref('venue_show', lazy=True),
                                 cascade="all,delete")
    show_artist = db.relationship('Artist', secondary=Artist_Show, backref=db.backref('show_artist', lazy=True),
                                  cascade="all,delete")

