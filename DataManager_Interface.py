from abc import ABC, abstractmethod

class IDataManager(ABC):
    @abstractmethod
    def add_movie(self, user_id: int, name: str, director: str, year: int, rating: int):
        """Add a new movie to the database."""
        pass

    @abstractmethod
    def update_movie(self, movie_id: int, new_rating: int):
        """Update an existing movie's rating based on movie ID."""
        pass

    @abstractmethod
    def delete_movie(self, name: str, user_id: int):
        """Delete a movie from the database by its name for a specific user."""
        pass

    @abstractmethod
    def get_movies_by_user(self, user_id: int):
        """Retrieve all movies for a specific user."""
        pass

    @abstractmethod
    def clear_movies(self):
        """Clear all movies from the database."""
        pass
