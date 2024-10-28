Movieweb_app - Database using Flask, API, SQLAlchemy

This README provides information on how to use the various routes of the Movie Database application.
How to Use the Database

    Home Route:
    URL: http://127.0.0.1:8050/
    Add a New User:
    URL: http://127.0.0.1:8050/add_user
    List All Users:
    URL: http://127.0.0.1:8050/list_users/
    List Movies of a Specific User:
    URL: http://127.0.0.1:/list_movies/<user_id>
    Example: http://127.0.0.1:8050/list_movies/3 (for user with ID 3)
    Fetch Movie Information via OMDb API:
    URL: http://127.0.0.1:/fetch_movie?user_id=<'user_id'>
    Example: http://127.0.0.1:8050/fetch_movie?user_id=3
    Add a Movie to a User's Collection:
    URL: http://127.0.0.1:/fetch_movie?user_id=<'user_id'>
    Example: http://127.0.0.1:8050/fetch_movie?user_id=3
    Delete a Movie from a User's Collection:
    URL: http://127.0.0.1:/list_movies/<'user_id'>
    Example: http://127.0.0.1:/list_movies/3
    List of Directors:
    URL: http://127.0.0.1:/list_directors
    List of Genres:
    URL: http://127.0.0.1:/list_genres
    List of All Reviews:
    URL: http://127.0.0.1:/list_all_reviews
    Reviews from a Specific Reviewer:
    URL: http://127.0.0.1:/list_reviews/<'user_id'>
    Example: http://127.0.0.1:/list_reviews/8 (for reviewer with ID 8)
