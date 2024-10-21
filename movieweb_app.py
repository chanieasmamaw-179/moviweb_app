import requests
from flask import Flask, request, render_template, redirect, url_for, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Column, Table
from sqlalchemy.orm import relationship
from dotenv import load_dotenv
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv()

# Initialize the Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///MoviWeb.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Association table for many-to-many relationship between Movie and Genre
movie_genre_association = db.Table('movie_genre_association',
                                   Column('movie_id', Integer, ForeignKey('movies.id')),
                                   Column('genre_id', Integer, ForeignKey('genres.id'))
                                   )

# Define the User model
class User(db.Model):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    movies = relationship("Movie", back_populates="user")
    reviews = relationship("Review", back_populates="user")

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

# Define the Movie model
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    director_id = Column(Integer, ForeignKey('directors.id'))
    year = Column(Integer, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'))

    user = relationship("User", back_populates="movies")
    director = relationship("Director", back_populates="movies")
    genres = relationship("Genre", secondary=movie_genre_association, back_populates="movies")
    reviews = relationship("Review", back_populates="movie")

    def __repr__(self):
        return f"Movie(id={self.id}, name={self.name}, year={self.year}, rating={self.rating})"

# Define the Director model
class Director(db.Model):
    __tablename__ = 'directors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    birth_date = Column(String)  # Use Date type if necessary

    movies = relationship("Movie", back_populates="director")

    def __repr__(self):
        return f"Director(id={self.id}, name={self.name}, birth_date={self.birth_date})"

# Define the Genre model
class Genre(db.Model):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    movies = relationship("Movie", secondary=movie_genre_association, back_populates="genres")

    def __repr__(self):
        return f"Genre(id={self.id}, name={self.name})"

# Define the Review model
class Review(db.Model):
    __tablename__ = 'reviews'

    id = Column(Integer, primary_key=True)
    review_text = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('Users.id'), nullable=False)
    movie_id = Column(Integer, ForeignKey('movies.id'), nullable=False)

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")

    def __repr__(self):
        return f"Review(id={self.id}, rating={self.rating}, user_id={self.user_id}, movie_id={self.movie_id})"

# Create all tables within an application context
with app.app_context():
    db.create_all()

def fetch_movie_details_from_omdb(movie_name):
    """Fetch movie details from OMDb API."""
    api_key = os.getenv('API_KEY')  # Ensure your .env file contains 'API_KEY=<your_api_key>'
    if not api_key:
        logging.error("API Key is not set. Please check your .env file.")
        return None

    url = f"http://www.omdbapi.com/?t={movie_name}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if data['Response'] == 'True':
            return {
                'name': data.get('Title'),
                'director': data.get('Director'),
                'year': int(data.get('Year', 0)),
                'rating': float(data.get('imdbRating', 0.0)),
                'genres': data.get('Genre').split(', ') if data.get('Genre') else []
            }
        else:
            logging.error("Movie not found: %s", data.get('Error'))
            return None
    else:
        logging.error("Failed to fetch movie details: %s", response.status_code)
        return None
@app.route('/fetch_movie', methods=['GET', 'POST'])
def fetch_movie():
    """Fetch movie details and allow adding to the user's collection."""
    user_id = request.args.get('user_id')  # Get user_id from query parameters

    if request.method == 'POST':
        # Check if 'name' exists in the form data
        movie_name = request.form.get('name')  # Use .get() to avoid KeyError

        if not movie_name:  # If movie_name is None or empty
            return render_template('add_movie.html', error="Movie name is required.", user_id=user_id)

        movie_details = fetch_movie_details_from_omdb(movie_name)

        if movie_details:
            return render_template('confirm_add_movie.html', movie_details=movie_details)
        else:
            return render_template('add_movie.html', error="Movie not found. Please try again.", user_id=user_id)

    return render_template('add_movie.html', user_id=user_id)  # Pass user_id to the template


@app.route('/add_movie', methods=['POST'])
def add_movie():
    """Handle the addition of a movie."""
    movie_name = request.form['name']
    movie_details = fetch_movie_details_from_omdb(movie_name)

    if not movie_details:
        return render_template('add_movie.html', error="Movie not found. Please try another title.")

    # Extract details from the API response
    director = movie_details['director']
    year = movie_details['year']
    rating = movie_details['rating']
    genre_names = movie_details['genres']

    # Get user ID from form (hidden input)
    user_id = request.form.get('user_id', type=int)

    try:
        # Create a new movie instance
        new_movie = Movie(name=movie_details['name'], year=year, rating=rating, user_id=user_id)

        # Check for existing director
        existing_director = db.session.query(Director).filter_by(name=director).first()
        if existing_director:
            new_movie.director = existing_director
        else:
            new_director = Director(name=director)
            db.session.add(new_director)
            new_movie.director = new_director

        # Add genres based on fetched genre names
        for genre_name in genre_names:
            existing_genre = db.session.query(Genre).filter_by(name=genre_name).first()
            if not existing_genre:
                new_genre = Genre(name=genre_name)
                db.session.add(new_genre)
                existing_genre = new_genre

            new_movie.genres.append(existing_genre)

        # Save the new movie to the database
        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for('list_movies', user_id=user_id))
    except Exception as e:
        logging.error(f"Error adding movie: {e}")
        return render_template('add_movie.html', error="Failed to add movie. Please try again.")

@app.route('/delete_movie/<int:user_id>/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    """Handle the deletion of a movie."""
    movie = db.session.query(Movie).filter(Movie.id == movie_id, Movie.user_id == user_id).one_or_none()
    if movie:
        db.session.delete(movie)
        db.session.commit()
        logging.info(f"Deleted movie: {movie.name}")
        return redirect(url_for('list_movies', user_id=user_id))
    else:
        logging.warning("Movie not found for deletion.")
        return abort(404)

@app.route('/list_movies/<int:user_id>', methods=['GET'])
def list_movies(user_id):
    """Display the list of movies for a specific user."""
    movies = db.session.query(Movie).filter(Movie.user_id == user_id).all()
    return render_template('list_movies.html', movies=movies, user_id=user_id)

@app.route('/')
def index():
    """Render the homepage."""
    return render_template('index.html')

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    """Handle the addition of a user."""
    if request.method == 'POST':
        user_name = request.form['name']
        existing_user = db.session.query(User).filter(User.name == user_name).one_or_none()
        if existing_user:
            logging.warning(f"User '{user_name}' already exists.")
            return render_template('add_user.html', error="User already exists.")

        new_user = User(name=user_name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_user.html')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500



if __name__ == '__main__':
    app.run(debug=True)
