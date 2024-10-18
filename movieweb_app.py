from flask import Flask, request, render_template, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, ForeignKey, Column
from sqlalchemy.orm import relationship
from DataManager_Interface import IDataManager  # Ensure this is the correct path

# Initialize the Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/masterschool/Documents/Masterschool_projects_2024/moviweb_app/MoviWeb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the User model
class User(db.Model):
    __tablename__ = 'Users'  # Make sure this matches the foreign key reference

    id = Column(Integer, primary_key=True)  # Unique identifier for each user
    name = Column(String, nullable=False)  # User's name
    movies = relationship("Movie", back_populates="user")  # Relationship with Movie (lowercase 'user')

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

# Define the Movie model
class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)  # Unique identifier for each movie
    name = Column(String, nullable=False)  # Movie's name
    director = Column(String, nullable=False)  # Movie's director
    year = Column(Integer, nullable=False)  # Year of release
    rating = Column(Integer, nullable=False)  # Movie's rating
    user_id = Column(Integer, ForeignKey('Users.id'))  # Foreign key referencing User (capital 'Users')

    user = relationship("User", back_populates="movies")  # Relationship with User (lowercase 'user')

    def __repr__(self):
        return f"Movie(id={self.id}, name={self.name}, director={self.director}, year={self.year}, rating={self.rating})"

# Create all tables within an application context
with app.app_context():
    db.create_all()

# DataManager Class for Data Management
class SQLiteDataManager(IDataManager):
    def __init__(self, db: SQLAlchemy):
        self.db = db

    def add_movie(self, user_id: int, name: str, director: str, year: int, rating: int):
        """Add a new movie to the database."""
        existing_movie = self.db.session.query(Movie).filter(Movie.name == name, Movie.user_id == user_id).one_or_none()
        if existing_movie:
            print(f"Movie '{name}' already exists for user {user_id}.")
            return

        new_movie = Movie(name=name, director=director, year=year, rating=rating, user_id=user_id)
        self.db.session.add(new_movie)
        self.db.session.commit()
        print("Added Movie:", new_movie)

    def update_movie(self, movie_id: int, new_rating: int):
        """Update an existing movie's rating based on movie ID."""
        movie_to_update = self.db.session.query(Movie).filter(Movie.id == movie_id).one_or_none()
        if movie_to_update:
            movie_to_update.rating = new_rating
            self.db.session.commit()
            print("Updated Movie Rating:", movie_to_update)
        else:
            print("Movie not found.")

    def delete_movie(self, name: str, user_id: int):
        """Delete a movie from the database by its name for a specific user."""
        movies_to_delete = self.db.session.query(Movie).filter(Movie.name == name, Movie.user_id == user_id).all()
        if movies_to_delete:
            for movie in movies_to_delete:
                self.db.session.delete(movie)
            self.db.session.commit()
            print(f"Deleted {len(movies_to_delete)} Movie(s): {[str(movie) for movie in movies_to_delete]}")
        else:
            print("Movie not found.")

    def get_movies_by_user(self, user_id: int):
        """Retrieve all movies for a specific user."""
        movies = self.db.session.query(Movie).filter(Movie.user_id == user_id).all()
        return movies

    def get_all_users(self):
        """Retrieve all users from the database."""
        return self.db.session.query(User).all()

    def clear_movies(self):
        """Clear all movies from the database."""
        self.db.session.query(Movie).delete()
        self.db.session.commit()
        print("All movies cleared from the database.")

# Instantiate SQLiteDataManager
data_manager = SQLiteDataManager(db)

# Route for Home Page
@app.route('/')
def home():
    return "Welcome to MovieWeb App!"
# Route to list all users
@app.route('/users')
def list_users():
    try:
        users = data_manager.get_all_users()
        return render_template('user_list.html', users=users)
    except Exception as e:
        print(f"Error fetching users: {e}")
        return "Internal Server Error", 500

# Route to display movies for a specific user
@app.route('/users/<int:user_id>')
def user_movies(user_id):
    movies = data_manager.get_movies_by_user(user_id)
    user = db.session.query(User).get(user_id)
    return render_template('user_movies.html', user=user, movies=movies)

# Route to add a new user
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    if request.method == 'POST':
        name = request.form['name']
        new_user = User(name=name)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('list_users'))
    return render_template('add_user.html')

# Route to add a new movie for a specific user
@app.route('/users/<int:user_id>/add_movie', methods=['GET', 'POST'])
def add_movie(user_id):
    if request.method == 'POST':
        name = request.form['name']
        director = request.form['director']
        year = request.form['year']
        rating = request.form['rating']
        data_manager.add_movie(user_id, name, director, year, rating)
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('add_movie.html', user_id=user_id)

# Route to update a movie for a specific user
@app.route('/users/<int:user_id>/update_movie/<int:movie_id>', methods=['GET', 'POST'])
def update_movie(user_id, movie_id):
    movie = db.session.query(Movie).get(movie_id)
    if request.method == 'POST':
        movie.name = request.form['name']
        movie.director = request.form['director']
        movie.year = request.form['year']
        movie.rating = request.form['rating']
        db.session.commit()
        return redirect(url_for('user_movies', user_id=user_id))
    return render_template('update_movie.html', movie=movie, user_id=user_id)

# Route to delete a movie for a specific user
@app.route('/users/<int:user_id>/delete_movie/<int:movie_id>', methods=['POST'])
def delete_movie(user_id, movie_id):
    movie = db.session.query(Movie).get(movie_id)
    if movie:
        data_manager.delete_movie(movie.name, user_id)
    return redirect(url_for('user_movies', user_id=user_id))

if __name__ == "__main__":
    app.run(debug=True)

    # Use the application context when interacting with the database
    with app.app_context():
        # Create an instance of the User table if it doesn't exist
        if db.session.query(User).count() == 0:
            user = User(name="John Doe")
            db.session.add(user)
            db.session.commit()

        # Adding movies interactively (Not recommended for production)
        while True:
            movie_name = input("Enter movie name (or 'exit' to stop): ")
            if movie_name.lower() == 'exit':
                break
            director = input("Enter Director: ")
            year = int(input("Enter Year: "))
            rating = int(input("Enter Rating: "))
            data_manager.add_movie(user.id, movie_name, director, year, rating)

        # Update and delete movies (these can be modified as needed)
        data_manager.update_movie(1, 9)  # Assuming ID 1 for the movie to update (replace with a valid ID if needed)
        movie_to_delete = input("Enter movie name to delete: ")
        data_manager.delete_movie(movie_to_delete, user.id)  # Change to an existing movie name if necessary

        # Print all movies for the user
        print("\nAll Movies for User:")
        for movie in data_manager.get_movies_by_user(user.id):
            print(movie)
