import pytest
from flask import url_for
from movieweb_app import app, db, User, Movie, SQLiteDataManager

# Initialize the Flask application for testing
@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory database for testing
    with app.test_client() as client:
        with app.app_context():
            db.create_all()  # Create tables
        yield client
        with app.app_context():
            db.drop_all()  # Clean up after tests

# Fixture for creating a sample user
@pytest.fixture
def sample_user(client):
    user = User(name="Test User")
    db.session.add(user)
    db.session.commit()
    return user

# Fixture for creating a sample movie
@pytest.fixture
def sample_movie(sample_user):
    movie = Movie(name="Test Movie", director="Test Director", year=2024, rating=8, user_id=sample_user.id)
    db.session.add(movie)
    db.session.commit()
    return movie

# Test home page
def test_home(client):
    response = client.get('/')
    assert response.data == b'Welcome to MovieWeb App!'

# Test adding a user
def test_add_user(client):
    response = client.post('/add_user', data={'name': 'New User'})
    assert response.status_code == 302  # Redirect status code
    assert User.query.filter_by(name='New User').count() == 1

# Test listing users
def test_list_users(client, sample_user):
    response = client.get('/users')
    assert b'Test User' in response.data

# Test fetching movies for a user
def test_user_movies(client, sample_user, sample_movie):
    response = client.get(f'/users/{sample_user.id}')
    assert b'Test Movie' in response.data

# Test adding a movie
def test_add_movie(client, sample_user):
    response = client.post(f'/users/{sample_user.id}/add_movie', data={'name': 'Inception'})
    assert response.status_code == 302  # Redirect status code
    assert Movie.query.filter_by(name='Inception', user_id=sample_user.id).count() == 1

# Test updating a movie
def test_update_movie(client, sample_movie):
    response = client.post(f'/users/{sample_movie.user_id}/update_movie/{sample_movie.id}', data={
        'name': 'Updated Movie',
        'director': 'Updated Director',
        'year': 2025,
        'rating': 9
    })
    assert response.status_code == 302  # Redirect status code
    updated_movie = Movie.query.get(sample_movie.id)
    assert updated_movie.name == 'Updated Movie'
    assert updated_movie.director == 'Updated Director'
    assert updated_movie.year == 2025
    assert updated_movie.rating == 9

# Test deleting a movie
def test_delete_movie(client, sample_movie):
    response = client.post(f'/users/{sample_movie.user_id}/delete_movie/{sample_movie.id}')
    assert response.status_code == 302  # Redirect status code
    assert Movie.query.filter_by(id=sample_movie.id).count() == 0

# Test 404 handling for non-existent user
def test_non_existent_user(client):
    response = client.get('/users/999')  # Assuming user with ID 999 doesn't exist
    assert response.status_code == 404

# Test 404 handling for non-existent movie
def test_non_existent_movie(client, sample_user):
    response = client.get(f'/users/{sample_user.id}/update_movie/999')  # Assuming movie with ID 999 doesn't exist
    assert response.status_code == 404

# Test database connection route
def test_test_db(client, sample_user):
    response = client.get('/test_db')
    assert b'Number of users: 1' in response.data

if __name__ == "__main__":
    pytest.main()
