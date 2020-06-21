#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from sqlalchemy.orm import relationship
from sqlalchemy import func

#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)



#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

Genres_Venue = db.Table('Genres_Venue',
  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id', ondelete='CASCADE'), primary_key=True)
                         )

Genres_Artists = db.Table('Genres_Artists',
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), primary_key=True),
  db.Column('genre_id', db.Integer, db.ForeignKey('Genre.id', ondelete='CASCADE'), primary_key=True)
                          )

Venue_Show = db.Table('Venue_Show',
  db.Column('venue_id', db.Integer, db.ForeignKey('Venue.id', ondelete='CASCADE'), primary_key=True),
  db.Column('show_id', db.Integer, db.ForeignKey('Show.id', ondelete='CASCADE'), primary_key=True)
                          )

Artist_Show = db.Table('Artist_Show',
  db.Column('artist_id', db.Integer, db.ForeignKey('Artist.id', ondelete='CASCADE'), primary_key=True),
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

    genres_venues = db.relationship('Genre', secondary=Genres_Venue, backref=db.backref('genres_venues', lazy=True), cascade='all, delete')
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
    genres_artists = db.relationship('Genre', secondary=Genres_Artists, backref=db.backref('genres_artists', lazy=True), cascade='all, delete')
    artist_show = db.relationship('Show', secondary=Artist_Show, backref=db.backref('artist_show', lazy=True), cascade='all, delete')


class Show(db.Model):
  __tablename__ = 'Show'

  id = db.Column(db.Integer, primary_key=True)

  start_time = db.Column(db.DateTime)

  venue_show = db.relationship('Venue', secondary=Venue_Show, backref=db.backref('venue_show', lazy=True), cascade="all,delete")
  show_artist = db.relationship('Artist', secondary=Artist_Show, backref=db.backref('show_artist', lazy=True), cascade="all,delete")


# class Genres(db.Model):
#   __tablename__ = 'Genres'
#
#   id = db.Column(db.Integer, primary_key=True)
#   genre = db.Column(db.String(50), unique=True)





#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # DO: replace with real venues data.
  #       num_shows should be aggregated based on number of upcoming shows per venue.
  #Venue.query.join('generes')
  '''
  data = [{
    "city": "San Francisco",
    "state": "CA",
    "venues": [{
      "id": 1,
      "name": "The Musical Hop",
      "num_upcoming_shows": 0,
    }, {
      "id": 3,
      "name": "Park Square Live Music & Coffee",
      "num_upcoming_shows": 1,
    }]
  }, {
    "city": "New York",
    "state": "NY",
    "venues": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }]
  '''
  res = db.session.query(Venue).join(Venue.show_venue, isouter=True).all()
  store_result = {}
  data = []
  for v in res:
    tmp_state = v.state
    tmp_city = v.city

    if tmp_state not in store_result:
      store_result[tmp_state] = {}
    if tmp_city not in store_result[tmp_state]:
      store_result[tmp_state][tmp_city] = []

    tmp_dct = {}
    tmp_dct['id'] =  v.id
    tmp_dct['name'] = v.name
    tmp_dct['num_upcoming_shows'] = 0
    for s in v.venue_show:
      if s.start_time >=datetime.now():
        tmp_dct['num_upcoming_shows'] += 1
    store_result[tmp_state][tmp_city].append(tmp_dct)

  for state in store_result:
    for city, val in store_result[state].items():
      tmp_dct = {}
      tmp_dct['city'] = city
      tmp_dct['state'] = state
      tmp_dct['venues'] = val
      data.append(tmp_dct)

  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # DO: implement search on artists with partial string search. Ensure it is case-insensitive.
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  response={
    "count": 1,
    "data": [{
      "id": 2,
      "name": "The Dueling Pianos Bar",
      "num_upcoming_shows": 0,
    }]
  }

  search_term = request.form.get('search_term')
  res = db.session.query(Venue).join(Venue.show_venue, isouter=True).filter(
    Venue.name.ilike(f'%{search_term}%')).all()

  response = {}
  response['count'] = len(res)
  response['data'] = []

  for r in res:
    tmp_dct = {}
    tmp_dct['id'] = r.id
    tmp_dct['name'] = r.name
    tmp_dct['num_upcoming_shows'] = 0
    for s in r.venue_show:
      if s.start_time >= datetime.now():
        tmp_dct['num_upcoming_shows'] += 1
    response['data'].append(tmp_dct)

  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # DO: replace with real venue data from the venues table, using venue_id
  data1={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
    "past_shows": [{
      "artist_id": 4,
      "artist_name": "Guns N Petals",
      "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }
  res = db.session.query(Venue).join(Venue.genres_venues, isouter=True).join(Venue.venue_show,
                                                                                isouter=True).filter(
    Venue.id == venue_id).first()

  venue_ = res
  data = {}
  data['id'] = venue_.id
  data['name'] = venue_.name
  data['city'] = venue_.city
  data['image_link'] = venue_.image_link
  data['phone'] = venue_.phone
  data['state'] = venue_.state
  data['website'] = venue_.website
  data['facebook_link'] = venue_.facebook_link
  data['seeking_talent'] = venue_.seeking_talent
  data['genres'] = []
  data['past_shows'] = []
  data['upcoming_shows'] = []

  past_shows = 0
  future_shows = 0

  for g in venue_.genres_venues:
    data['genres'].append(g.name)
  for s in venue_.venue_show:
    tmp_start_time = s.start_time
    if tmp_start_time < datetime.now():
      show_type = 'past_shows'
      past_shows += 1
    else:
      show_type = 'upcoming_shows'
      future_shows += 1
    tmp_show = {}
    tmp_artist = s.show_artist[0]
    tmp_show['artist_id'] = tmp_artist.id
    tmp_show['artist_name'] = tmp_artist.name
    tmp_show['artist_image_link'] = tmp_artist.image_link
    tmp_show['start_time'] = tmp_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    # tmp_show['start_time'] = str(format_datetime(tmp_start_time))
    data[show_type].append(tmp_show)

  data['past_shows_count'] = past_shows
  data['upcoming_shows_count'] = future_shows


  ##data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  error = False
  try:
    # called upon submitting the new artist listing form
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    seeking_talent = True if request.form.get('seeking_venue') == 'y' else False
    website = request.form.get('website')
    image_link = request.form.get('image_link')

    address = request.form.get('address')
    facebook_link = request.form.get('facebook_link')

    venue = Venue(name=name, city=city, state=state, phone=phone, address=address, facebook_link=facebook_link,
                  seeking_talent=seeking_talent, website=website, image_link=image_link)
    for genre in genres:
      g = db.session.query(Genre).filter(Genre.name == genre).first()
      if not g:
        g = Genre(name=genre)
      venue.genres_venues.append(g)
    db.session.add(venue)
    db.session.commit()

  except Exception as e:
    print(e)
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # DO: Complete this endpoint for taking a venue_id, and using
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
  try:
    error = False
    db.session.query(Venue).filter(Venue.id == venue_id).delete()
    db.session.commit()
  except Exception as e:
    logging.error(e)
    error = True
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Show was successfully deleted!')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return jsonify({ 'success': False })

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  ''''
  data=[{
    "id": 4,
    "name": "Guns N Petals",
  }, {
    "id": 5,
    "name": "Matt Quevedo",
  }, {
    "id": 6,
    "name": "The Wild Sax Band",
  }]
  '''
  res = db.session.query(Artist).all()
  data = []
  for r in res:
    tmp_dct = {}
    tmp_dct['id'] = r.id
    tmp_dct['name'] = r.name
    data.append(tmp_dct)
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')

  res = db.session.query(Artist).join(Artist.artist_show, isouter=True).filter(Artist.name.ilike(f'%{search_term}%')).all()

  response = {}
  response['count'] = len(res)
  response['data'] = []
  for r in res:
    tmp_dct = {}
    tmp_dct['id'] = r.id
    tmp_dct['name'] = r.name
    tmp_dct['num_upcoming_shows'] = 0
    for s in r.show_artist:
      if s.start_time >= datetime.now():
        tmp_dct['num_upcoming_shows'] += 1
    response['data'].append(tmp_dct)

  '''
  response={
    "count": 1,
    "data": [{
      "id": 4,
      "name": "Guns N Petals",
      "num_upcoming_shows": 0,
    }]
  }
  '''
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the venue page with the given venue_i
  '''
  data1={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "at&fit=crop&w=30https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=form0&q=80",
    "past_shows": [{
      "venue_id": 1,
      "venue_name": "The Musical Hop",
      "venue_image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60",
      "start_time": "2019-05-21T21:30:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data2={
    "id": 5,
    "name": "Matt Quevedo",
    "genres": ["Jazz"],
    "city": "New York",
    "state": "NY",
    "phone": "300-400-5000",
    "facebook_link": "https://www.facebook.com/mattquevedo923251523",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "past_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [],
    "past_shows_count": 1,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 6,
    "name": "The Wild Sax Band",
    "genres": ["Jazz", "Classical"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "432-325-5432",
    "seeking_venue": False,
    "image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "past_shows": [],
    "upcoming_shows": [{
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "venue_id": 3,
      "venue_name": "Park Square Live Music & Coffee",
      "venue_image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 0,
    "upcoming_shows_count": 3,
  }
  data = list(filter(lambda d: d['id'] == artist_id, [data1, data2, data3]))[0]
  '''
  res = db.session.query(Artist).join(Artist.genres_artists, isouter=True).join(Artist.artist_show, isouter=True).filter(Artist.id == artist_id).first()

  artist_ = res
  data = {}
  data['id'] = artist_.id
  data['name'] = artist_.name
  data['city'] = artist_.city
  data['image_link'] = artist_.image_link
  data['phone'] = artist_.phone
  data['state'] = artist_.state
  data['website'] = artist_.website
  data['facebook_link'] = artist_.facebook_link
  data['seeking_venue'] = artist_.seeking_venue
  data['seeking_description'] = artist_.seeking_description
  data['genres'] = []
  data['past_shows'] = []
  data['upcoming_shows'] = []

  past_shows = 0
  future_shows = 0

  for g in artist_.genres_artists:
    data['genres'].append(g.name)
  for s in artist_.show_artist:
    tmp_start_time = s.start_time
    if tmp_start_time < datetime.now():
      show_type = 'past_shows'
      past_shows += 1
    else:
      show_type = 'upcoming_shows'
      future_shows += 1
    tmp_show = {}
    tmp_venue = s.venue_show[0]
    tmp_show['venue_id'] = tmp_venue.id
    tmp_show['venue_name'] = tmp_venue.name
    tmp_show['venue_image_link'] = tmp_venue.image_link
    tmp_show['start_time'] = tmp_start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    #tmp_show['start_time'] = str(format_datetime(tmp_start_time))
    data[show_type].append(tmp_show)

  data['past_shows_count'] = past_shows
  data['upcoming_shows_count'] = future_shows

  return render_template('pages/show_artist.html', artist=data)

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist={
    "id": 4,
    "name": "Guns N Petals",
    "genres": ["Rock n Roll"],
    "city": "San Francisco",
    "state": "CA",
    "phone": "326-123-5000",
    "website": "https://www.gunsnpetalsband.com",
    "facebook_link": "https://www.facebook.com/GunsNPetals",
    "seeking_venue": True,
    "seeking_description": "Looking for shows to perform at in the San Francisco Bay Area!",
    "image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80"
  }


  # DO: populate form with fields from artist with ID <artist_id>

  res = db.session.query(Artist).filter(Artist.id == artist_id).first()
  artist = {}
  artist['id'] = res.id
  artist['name'] = res.name
  artist['city'] = res.city
  artist['state'] = res.state
  artist['phone'] = res.phone
  artist['website'] = res.website
  artist['facebook_link'] = res.facebook_link
  artist['seeking_venue'] = res.seeking_venue
  artist['seeking_description'] = res.seeking_description
  artist['image_link'] = res.image_link
  artist['genres'] = []
  for g in res.genres_artists:
    artist['genres'].append(g.name)

  form.name.data = artist['name']
  form.city.data = artist['city']
  form.state.data = artist['state']
  form.phone.data = artist['phone']
  form.genres.data = artist['genres']
  form.seeking_venue.data = artist['seeking_venue']
  form.seeking_description.data = artist['seeking_description']
  form.website.data = artist['website']
  form.image_link.data = artist['image_link']
  form.facebook_link.data = artist['facebook_link']
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # artist record with ID <artist_id> using the new attributes
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
  seeking_description = request.form.get('seeking_description')
  website = request.form.get('website')
  image_link = request.form.get('image_link')
  facebook_link = request.form.get('facebook_link')

  res = db.session.query(Artist).filter(Artist.id == artist_id).first()
  if res:
    res.name = name
    res.city = city
    res.state = state
    res.phone = phone
    res.facebook_link = facebook_link
    res.seeking_venue = seeking_venue
    res.seeking_description = seeking_description
    res.website = website
    res.image_link = image_link
    new_genres = []


    for gname in genres:
      g = db.session.query(Genre).filter(Genre.name == gname).first()
      if g:
        new_genres.append(g)
      else:
        new_genres.append(Genre(name=gname))

    res.genres_artists = new_genres
  else:
    raise

  try:
    error = False
    db.session.add(res)
    db.session.commit()
  except Exception as e:
    logging.error(e)
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully updated!')

  return render_template('forms/home.html')

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue={
    "id": 1,
    "name": "The Musical Hop",
    "genres": ["Jazz", "Reggae", "Swing", "Classical", "Folk"],
    "address": "1015 Folsom Street",
    "city": "San Francisco",
    "state": "CA",
    "phone": "123-123-1234",
    "website": "https://www.themusicalhop.com",
    "facebook_link": "https://www.facebook.com/TheMusicalHop",
    "seeking_talent": True,
    "seeking_description": "We are on the lookout for a local artist to play every two weeks. Please call us.",
    "image_link": "https://images.unsplash.com/photo-1543900694-133f37abaaa5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=400&q=60"
  }
  res = db.session.query(Venue).filter(Venue.id == venue_id).first()
  venue = {}
  venue['id'] = res.id
  venue['name'] = res.name
  venue['city'] = res.city
  venue['state'] = res.state
  venue['address'] = res.address
  venue['phone'] = res.phone
  venue['website'] = res.website
  venue['facebook_link'] = res.facebook_link
  venue['seeking_talent'] = res.seeking_talent
  venue['image_link'] = res.image_link
  venue['genres'] = []
  for g in res.genres_venues:
    venue['genres'].append(g.name)

  form.name.data = venue['name']
  form.city.data = venue['city']
  form.state.data = venue['state']
  form.phone.data = venue['phone']
  form.genres.data = venue['genres']
  form.seeking_talent.data = venue['seeking_talent']
  form.website.data = venue['website']
  form.image_link.data = venue['image_link']
  form.facebook_link.data = venue['facebook_link']

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # artist record with ID <artist_id> using the new attributes
  name = request.form.get('name')
  city = request.form.get('city')
  state = request.form.get('state')
  phone = request.form.get('phone')
  genres = request.form.getlist('genres')
  seeking_talent = True if request.form.get('seeking_talent') == 'y' else False
  website = request.form.get('website')
  image_link = request.form.get('image_link')
  facebook_link = request.form.get('facebook_link')

  res = db.session.query(Venue).filter(Venue.id == venue_id).first()
  if res:
    res.name = name
    res.city = city
    res.state = state
    res.phone = phone
    res.facebook_link = facebook_link
    res.seeking_talent = seeking_talent
    res.website = website
    res.image_link = image_link
    new_genres = []


    for gname in genres:
      g = db.session.query(Genre).filter(Genre.name == gname).first()
      if g:
        new_genres.append(g)
      else:
        new_genres.append(Genre(name=gname))

    res.genres_venues = new_genres
  else:
    raise

  try:
    error = False
    db.session.add(res)
    db.session.commit()
  except Exception as e:
    logging.error(e)
    error = True
    db.session.rollback()
    flash('An error occurred. Venue ' + request.form['name'] + ' could not be updated.')
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Venue ' + request.form['name'] + ' was successfully updated!')
  # venue record with ID <venue_id> using the new attributes
  return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  error = False
  try:
    # called upon submitting the new artist listing form
    name = request.form.get('name')
    city = request.form.get('city')
    state = request.form.get('state')
    phone = request.form.get('phone')
    genres = request.form.getlist('genres')
    seeking_venue = True if request.form.get('seeking_venue') == 'y' else False
    seeking_description = request.form.get('seeking_description')
    website = request.form.get('website')
    image_link = request.form.get('image_link')
    facebook_link = request.form.get('facebook_link')

    artist = Artist(name=name, city=city, state=state, phone=phone, facebook_link=facebook_link, seeking_venue=seeking_venue,
                    seeking_description=seeking_description, website=website, image_link=image_link)
    for genre in genres:
      g = db.session.query(Genre).filter(Genre.name == genre).first()
      if not g:
        g = Genre(name=genre)
      artist.genres_artists.append(g)

    db.session.add(artist)
    db.session.commit()

  except Exception as e:
    logging.error(e)
    error = True
    db.session.rollback()
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Artist ' + request.form['name'] + ' was successfully listed!')

  return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  data=[{
    "venue_id": 1,
    "venue_name": "The Musical Hop",
    "artist_id": 4,
    "artist_name": "Guns N Petals",
    "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
    "start_time": "2019-05-21T21:30:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 5,
    "artist_name": "Matt Quevedo",
    "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
    "start_time": "2019-06-15T23:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-01T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-08T20:00:00.000Z"
  }, {
    "venue_id": 3,
    "venue_name": "Park Square Live Music & Coffee",
    "artist_id": 6,
    "artist_name": "The Wild Sax Band",
    "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
    "start_time": "2035-04-15T20:00:00.000Z"
  }]

  res = db.session.query(Show).join(Venue_Show, isouter=True).join(Artist_Show,isouter=True).all()
  data = []
  for r in res:
    tmp_dct = {}
    tmp_dct['start_time'] = r.start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
    if len(r.show_artist) == 0 or len(r.venue_show) == 0:
      logging.warning(f'{r.id} doesnt have artists or venues')
      continue
    tmp_dct['artist_id'] = r.show_artist[0].id
    tmp_dct['artist_name'] = r.show_artist[0].name
    tmp_dct['artist_image_link'] = r.show_artist[0].image_link
    tmp_dct['venue_id'] = r.venue_show[0].id
    tmp_dct['venue_name'] = r.venue_show[0].name
    data.append(tmp_dct)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  error = False
  try:
    # called upon submitting the new artist listing form
    artist_id = request.form.get('artist_id')
    venue_id = request.form.get('venue_id')
    start_time = request.form.get('start_time')

    show = Show(start_time=start_time )

    a = db.session.query(Artist).filter(Artist.id == artist_id).first()
    if not a:
      logging.error('artist doesnt exist!')
      raise

    v = db.session.query(Venue).filter(Venue.id == venue_id).first()

    if not v:
      logging.error('venue doesnt exist!')
      raise

    show.show_artist.append(a)
    show.venue_show.append(v)

    db.session.add(show)
    db.session.commit()

  except Exception as e:
    logging.error(e)
    error = True
    db.session.rollback()
    flash('An error occurred. Show could not be listed.')
  finally:
    db.session.close()
  if not error:
    # on successful db insert, flash success
    flash('Show was successfully listed!')

  # called to create new shows in the db, upon submitting new show listing form

  # on successful db insert, flash success
  #flash('Show was successfully listed!')
  # e.g., flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
