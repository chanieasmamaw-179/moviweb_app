Movie Database using FLASK, API, SQAlchemy 

This README provides information on how to use the various routes of the Movie Database FLASK, API, SQAlchemy .
How to Use the Database
1. Home Route:
    Description: Displays the homepage.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/

2. Add a New User:
    Description: Displays a form to add a new user to the database. If a user already exists, an error message is shown.
    HTTP Methods: GET (to display the form), POST (to submit the form)
    URL: http://127.0.0.1:5000/add_user

3. List All Users:
    Description: Lists all users in the database.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_users/

4. List Movies of a Specific User:
    Description: Lists all movies added by a specific user.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_movies/<user_id>
        Example: http://127.0.0.1:5000/list_movies/3 (for user with ID 3)

5. Fetch Movie Information via OMDb API:
    Description: Fetch movie details from the OMDb API by providing a movie name (through POST) and link it to a specific user. If no movie is provided or found, it shows an error.
    HTTP Methods: GET (to display the form), POST (to fetch movie details)
    URL: http://127.0.0.1:5000/fetch_movie?user_id=<user_id>
        Example: http://127.0.0.1:5000/fetch_movie?user_id=3

6. Add a Movie to a User's Collection:
    Description: Adds the fetched movie (from the OMDb API) to the user's movie collection. The movie details and user ID must be provided via POST request.
    HTTP Method: POST
    URL: http://127.0.0.1:5000/fetch_movie?user_id=<user_id>
        Example: http://127.0.0.1:5000/fetch_movie?user_id=3

7. Delete a Movie from a User's Collection:
    Description: Deletes a specific movie from a specific user's collection.
    HTTP Method: POST
    URL: http://127.0.0.1:5000/list_movies/<user_id> and then delete the movie from that page.
        Example: http://127.0.0.1:5000/list_movies/3

8. List of Directors:
    Description: Displays a list of all directors in the database.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_directors

9. List of Genres:
    Description: Displays a list of all genres in the database.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_genres

10. List of Reviewers:
    Description: Displays a list of all reviewers in the database.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_reviewers

11. List of All Reviews:
    Description: Displays a list of all reviews in the database.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_all_reviews
12. Reviews from a Specific Reviewer:
    Description: Displays a list of reviews added by a specific reviewer.
    HTTP Method: GET
    URL: http://127.0.0.1:5000/list_reviews/<user_id>
        Example: http://127.0.0.1:5000/list_reviews/8 (for reviewer with ID 8)