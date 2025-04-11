import requests
import os
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

# Base URLs
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"
TMDB_MOVIE_DETAILS_URL = "https://api.themoviedb.org/3/movie"

def search_movies(title):
    params = {
        "api_key": TMDB_API_KEY,
        "query": title,
        "language": "en-US"
    }
    response = requests.get(TMDB_SEARCH_URL, params=params)
    response.raise_for_status()
    return response.json().get("results", [])

def get_movie_trailer(tmdb_id):
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
    return None

def get_movie_details(tmdb_id):
    url = f"{TMDB_MOVIE_DETAILS_URL}/{tmdb_id}"
    params = {
        "api_key": TMDB_API_KEY,
        "language": "en-US"
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    movie_data = response.json()
    movie_data["trailer_url"] = get_movie_trailer(tmdb_id)
    return movie_data
