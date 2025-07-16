

import os
import requests
import logging
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie"

if not TMDB_API_KEY:
    logging.warning("TMDB_API_KEY is not set. API calls will fail.")


def search_movies(title):
    
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
   
    try:
        url = f"{TMDB_MOVIE_DETAILS_URL}/{tmdb_id}"
        params = {
            "api_key": TMDB_API_KEY,
            "language": "en-US"
        }
        response = requests.get(url, params=params)
        response.raise_for_status()
        movie_data = response.json()

        movie_data["trailer_url"] = get_movie_trailer(tmdb_id)

        genres = movie_data.get("genres", [])
        genre_names = [g["name"] for g in genres]
        movie_data["genre_names"] = ", ".join(genre_names)

        return movie_data

    except Exception as e:
        logging.error(f"Error fetching movie details for ID {tmdb_id}: {e}")
        return {}
