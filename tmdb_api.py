"""
tmdb_api.py – Handles communication with The Movie Database (TMDb) API.

Provides functions to:
- Search for movies by title
- Retrieve full movie details
- Fetch trailer links
- Format genre names for display
"""

import os
import requests
import logging
from dotenv import load_dotenv

# Load TMDb API key from .env
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Base URLs
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie"

if not TMDB_API_KEY:
    logging.warning("TMDB_API_KEY is not set. API calls will fail.")


def search_movies(title):
    """
    Search for movies by title using the TMDb API.

    Args:
        title (str): Movie title to search for

    Returns:
        list: A list of matching movie dictionaries (may be empty)
    """
    try:
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "language": "en-US"
        }
        response = requests.get(TMDB_SEARCH_URL, params=params)
        response.raise_for_status()
        return response.json().get("results", [])
    except Exception as e:
        logging.error(f"Error searching movies for title '{title}': {e}")
        return []


def get_movie_trailer(tmdb_id):
    """
    Fetch the YouTube trailer URL for a given TMDb movie ID.

    Args:
        tmdb_id (int): TMDb movie ID

    Returns:
        str or None: YouTube trailer URL if found, otherwise None
    """
    try:
        url = f"{TMDB_MOVIE_DETAILS_URL}/{tmdb_id}/videos"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        videos = response.json().get("results", [])

        for video in videos:
            if video["site"] == "YouTube" and video["type"] == "Trailer":
                return f"https://www.youtube.com/watch?v={video['key']}"
    except Exception as e:
        logging.error(f"Error fetching trailer for movie ID {tmdb_id}: {e}")

    return None


def get_movie_details(tmdb_id):
    """
    Retrieve detailed information for a movie by its TMDb ID.

    Args:
        tmdb_id (int): TMDb movie ID

    Returns:
        dict: A dictionary containing movie details including genre names and trailer URL
    """
    try:
        url = f"{TMDB_MOVIE_DETAILS_URL}/{tmdb_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        movie_data = response.json()

        # Add trailer URL
        movie_data["trailer_url"] = get_movie_trailer(tmdb_id)

        # Extract and format genre names
        genres = movie_data.get("genres", [])
        genre_names = [g["name"] for g in genres]
        movie_data["genre_names"] = ", ".join(genre_names)

        return movie_data

    except Exception as e:
        logging.error(f"Error fetching movie details for ID {tmdb_id}: {e}")
        return {}
