Movieweb_app - Database using Flask, API, SQLAlchemy

This README provides information on how to use the various routes of the Movie Database application.
How to Use the Database

    Home Route:
    URL: https://moviweb-app-3.onrender.com
    Add a New User:
    URL: https://moviweb-app-3.onrender.com/add_user
    List All Users:
    URL: https://moviweb-app-3.onrender.com/list_users/
    List Movies of a Specific User:
    URL: https://moviweb-app-3.onrender.com/<user_id>
    Example: https://moviweb-app-3.onrender.com/list_movies/3 (for user with ID 3)
    Fetch Movie Information via OMDb API:
    URL:https://moviweb-app-3.onrender.com/fetch_movie?user_id=<'user_id'>
    Example: https://moviweb-app-3.onrender.com/fetch_movie?user_id=3
    Add a Movie to a User's Collection:
    URL: https://moviweb-app-3.onrender.com/fetch_movie?user_id=<'user_id'>
    Example:https://moviweb-app-3.onrender.com/fetch_movie?user_id=3
    Delete a Movie from a User's Collection:
    URL: https://moviweb-app-3.onrender.com/list_movies/<'user_id'>
    Example: https://moviweb-app-3.onrender.com/list_movies/3
    List of Directors:
    URL: https://moviweb-app-3.onrender.com/list_directors
    List of Genres:
    URL: https://moviweb-app-3.onrender.com/list_genres
    List of All Reviews:
    URL: https://moviweb-app-3.onrender.com/list_all_reviews
    Reviews from a Specific Reviewer:
    URL: https://moviweb-app-3.onrender.com/list_reviews/<'user_id'>
    Example: https://moviweb-app-3.onrender.com/list_reviews/8 (for reviewer with ID 8)
