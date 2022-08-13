# ----------------------------------------------------------------------------#
# Imports
# ----------------------------------------------------------------------------#
import sys

import dateutil.parser
import babel
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_migrate import Migrate
from forms import *

# ----------------------------------------------------------------------------#
# App Config.
# ----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
from models import Venue, Show, Artist

'''# TODO: connect to a local postgresql database'''


# ----------------------------------------------------------------------------#
# Models.
# ----------------------------------------------------------------------------#


'''# TODO: implement any missing fields, as a database migration using Flask-Migrate'''


'''# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database 
migration. '''

# ----------------------------------------------------------------------------#
# Filters.
# ----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
    date = dateutil.parser.parse(str(value))
    if format == 'full':
        format = "EEEE MMMM, d, y 'at' h:mma"
    elif format == 'medium':
        format = "EE MM, dd, y h:mma"
    return babel.dates.format_datetime(date, format, locale='en')


app.jinja_env.filters['datetime'] = format_datetime


# ----------------------------------------------------------------------------#
# Controllers.
# ----------------------------------------------------------------------------#

@app.route('/')
def index():
    return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------
# the method. below returns an obj if there's one with a matching key and value in the specified array
def get_object(key, val, lis):
    # from gh
    return next((i for i, d in enumerate(lis) if d[key] == val), None)


@app.route('/venues')
def venues():
    venues_list = Venue.query.group_by(Venue.city, Venue.state, Venue.id).all()
    data_array = []
    for venue in venues_list:
        # getting the index of the current venue's city,
        # so that we can added the venue to the correct obj(if it exists) in the array
        city_index = get_object("city", venue.city, data_array)
        if city_index is not None:
            city = data_array[city_index]
            # adding the venue to the venues array of the city
            city['venues'].append(venue)
        else:
            # if city doesn't exist then we create it
            data_array.append({"city": venue.city,
                               "state": venue.state, "venues": [venue]})

        # if any(obj['city'] == venue_city for obj, k in data_array):


    '''# TODO: replace with real venues data num_upcoming_shows should be aggregated based on number of upcoming shows per venue.'''
    return render_template('pages/venues.html', areas=data_array)


@app.route('/venues/search', methods=['POST'])
def search_venues():

    '''#ODO: implement search on artists with partial string search. Ensure it is case-insensitive.'''
    # seach for Hop should return "The Musical Hop".
    # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
    search_term = request.form.get('search_term')
    data = Venue.query.filter(Venue.name.contains(search_term)).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_venues.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    '''
    ODO: replace with real venue data from the venues table, using venue_id
    '''
    current_date = format_datetime(str(datetime.today()))
    # the filter order is important (it enhances the performance)
    # past_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time <= current_date).all()
    # upcoming_shows = Show.query.filter(Show.venue_id == venue_id).filter(Show.start_time >= current_date).all()

    past_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time < datetime.now()).all()
    upcoming_shows = db.session.query(Show).join(Venue).filter(Show.venue_id == venue_id).filter(Show.start_time > current_date).all()

    data = Venue.query.filter_by(id=venue_id).first()
    response = {
        "id": data.id,
        "name": data.name,
        "genres": data.genres,
        "address": data.address,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "website": data.website_link,
        "facebook_link": data.facebook_link,
        "seeking_talent": data.seeking_talent,
        "seeking_description": data.seeking_description,
        "image_link": data.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }
    return render_template('pages/show_venue.html', venue=response)


#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
    '''ODO: insert form data as a new Venue record in the db, instead'''
    '''TODO: modify data to be the data object returned from db insertion'''
    try:
        genres = request.form.get('genres')
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        address = request.form.get('address')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')
        seeking_talent = request.form.get('seeking_talent')
        seeking_description = request.form.get('seeking_description')

        # the if changes the val of the var from a str to a bool
        if seeking_talent == 'y':
            seeking_talent = True
        else:
            seeking_talent = False

        # add the data to the server
        venue_item = Venue(genres=genres, name=name, city=city, state=state, address=address, phone=phone,
                           image_link=image_link, facebook_link=facebook_link, website_link=website_link,
                           seeking_talent=seeking_talent, seeking_description=seeking_description)
        db.session.add(venue_item)
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        print("The venue was created")
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    finally:
        db.session.close()

    '''# TODO: on unsuccessful db insert, flash an error instead.'''
    return render_template('pages/home.html')


@app.route('/venues/<venue_id>/delete')
def delete_venue(venue_id):
    '''# ODO: Complete this endpoint for taking a venue_id, and using'''
    try:
        deleted_venue = Venue.query.get(venue_id)
        db.session.delete(deleted_venue)
        db.session.commit()
        flash("The venue was deleted successfully")
    except:
        print(sys.exc_info())
        db.session.rollback()
        flash("Unfortunately, the venue wasn't deleted successfully")
    finally:
        db.session.close()

    # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
    # clicking that button delete it from the db then redirect the user to the homepage
    return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
    """# ODO: replace with real data returned from querying the database"""
    data = Artist.query.all()
    return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
    # ODO: implement search on artists with partial string search. Ensure it is case-insensitive.
    # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
    # search for "band" should return "The Wild Sax Band".
    search_term = request.form.get('search_term')
    data = Artist.query.filter(Artist.name.contains(search_term)).all()
    response = {
        "count": len(data),
        "data": data
    }
    return render_template('pages/search_artists.html', results=response,
                           search_term=request.form.get('search_term', ''))


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
    # shows the artist page with the given artist_id
    # ODO: replace with real artist data from the artist table, using artist_id
    current_date = format_datetime(str(datetime.today()))
    # past_shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time <= current_date).all()
    # upcoming_shows = Show.query.filter(Show.artist_id == artist_id).filter(Show.start_time >= current_date).all()

    past_shows = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.now()).all()
    upcoming_shows = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time > current_date).all()

    # data = list(filter(lambda d: d['id'] == venue_id, [data1, data2, data3]))[0]
    data = Artist.query.filter_by(id=artist_id).first()
    response = {
        "id": data.id,
        "name": data.name,
        "genres": data.genres,
        "city": data.city,
        "state": data.state,
        "phone": data.phone,
        "website": data.website_link,
        "facebook_link": data.facebook_link,
        "seeking_venues": data.seeking_venues,
        "seeking_description": data.seeking_description,
        "image_link": data.image_link,
        "past_shows": past_shows,
        "upcoming_shows": upcoming_shows,
        "past_shows_count": len(past_shows),
        "upcoming_shows_count": len(upcoming_shows),
    }

    return render_template('pages/show_artist.html', artist=response)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    form = ArtistForm()
    artist = Artist.query.get(artist_id)
    if artist:
        # if we get an item with the id passed int the route then we can make an attempt to process it
        return render_template('forms/edit_artist.html', form=form, artist=artist)
    else:
        flash("The artist doesn't exist")
        return redirect(url_for('index'))


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
    # ODO: take values from the form submitted, and update existing
    # artist record with ID <artist_id> using the new attributes
    artist = Artist.query.get(artist_id)
    try:
        if artist is not None:
            artist.genres = request.form.get('genres')
            artist.name = request.form.get('name')
            artist.city = request.form.get('city')
            artist.state = request.form.get('state')
            artist.phone = request.form.get('phone')
            artist.image_link = request.form.get('image_link')
            artist.facebook_link = request.form.get('facebook_link')
            artist.website_link = request.form.get('website_link')
            seeking_venue = request.form.get('seeking_venue')
            artist.seeking_description = request.form.get('seeking_description')

            # converting the seeking_venue str val to a bool
            if seeking_venue == 'y':
                artist.seeking_venue = True
            else:
                artist.seeking_venue = False

            db.session.commit()
            # on successful db insert, flash success
            flash('Artist ' + request.form['name'] + ' was successfully updated!')
        else:
            flash("The artist doesn't exist")
    except:
        print(sys.exc_info())
        db.session.rollback()
        # on successful db insert, flash success
        flash('An error occurred. Artist ' + request.form.get('name') + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    form = VenueForm()
    # ODO: populate form with values from venue with ID <venue_id>
    venue = Venue.query.get(venue_id)
    if venue:
        # if we get an item with the id passed int the route then we can make an attempt to process it
        return render_template('forms/edit_venue.html', form=form, venue=venue)
    else:
        flash("The artist doesn't exist")
        return redirect(url_for('index'))


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
    # ODO: take values from the form submitted, and update existing
    venue = Venue.query.get(venue_id)
    # venue record with ID <venue_id> using the new attributes
    try:
        venue.genres = request.form.get('genres')
        venue.name = request.form.get('name')
        venue.city = request.form.get('city')
        venue.state = request.form.get('state')
        venue.address = request.form.get('address')
        venue.phone = request.form.get('phone')
        venue.image_link = request.form.get('image_link')
        venue.facebook_link = request.form.get('facebook_link')
        venue.website_link = request.form.get('website_link')
        seeking_talent = request.form.get('seeking_talent')
        venue.seeking_description = request.form.get('seeking_description')

        # converting the seeking_venue str val to a bool
        if seeking_talent == 'y':
            venue.seeking_talent = True
        else:
            venue.seeking_talent = False
        # add the data to the server
        db.session.commit()
        # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        # on successful db insert, flash success
        flash('An error occurred. Venue ' + request.form.get('name') + ' could not be updated.')
    finally:
        db.session.close()
    return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
    # called upon submitting the new artist listing form
    # ODO: insert form data as a new Venue record in the db, instead
    # ODO: modify data to be the data object returned from db insertion
    try:
        genres = request.form.get('genres')
        name = request.form.get('name')
        city = request.form.get('city')
        state = request.form.get('state')
        phone = request.form.get('phone')
        image_link = request.form.get('image_link')
        facebook_link = request.form.get('facebook_link')
        website_link = request.form.get('website_link')
        seeking_venue = request.form.get('seeking_venue')
        seeking_description = request.form.get('seeking_description')

        # converting the seeking_venue str val to a bool
        if seeking_venue == 'y':
            seeking_venue = True
        else:
            seeking_venue = False
        # add the data to the server
        artist_item = Artist(genres=genres, name=name, city=city, state=state, phone=phone, image_link=image_link,
                             facebook_link=facebook_link, website_link=website_link, seeking_venues=seeking_venue,
                             seeking_description=seeking_description)
        db.session.add(artist_item)
        db.session.commit()
        # on successful db insert, flash success
        flash('Artist ' + request.form['name'] + ' was successfully added!')
    except:
        print(sys.exc_info())
        db.session.rollback()
        # on successful db insert, flash success
        flash('An error occurred. Artist ' + request.form.get('name') + ' could not be added.')
    finally:
        db.session.close()

    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
    # displays list of shows at /shows
    # ODO: replace with real venues data.

    data = Show.query.all()
    return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
    # called to create new shows in the db, upon submitting new show listing form
    # ODO: insert form data as a new Show record in the db, instead
    try:
        artist_id = request.form.get('artist_id')
        artist = Artist.query.get(artist_id)
        venue_id = request.form.get('venue_id')
        venue = Venue.query.get(venue_id)
        start_time = request.form.get('start_time')

        if artist and venue:
            # add the data to the server
            show_item = Show(artist_id=artist_id, venue_id=venue_id, start_time=format_datetime(start_time), venue_name=venue.name,
                             artist_name=artist.name, artist_image_link=artist.image_link)
            db.session.add(show_item)
            db.session.commit()
            # on successful db insert, flash success
            flash('Show was successfully listed!')
        else:
            flash("The artist or the venue doesn't exist")
    except:
        db.session.rollback()
        flash('An error occurred. Show could not be listed.')
    finally:
        db.session.close()
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

# ----------------------------------------------------------------------------#
# Launch.
# ----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
