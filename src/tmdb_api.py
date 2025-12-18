import os
import requests
import streamlit as st

TMDB_BASE_URL = "https://api.themoviedb.org/3/movie/{}?api_key={}&language=en-US"
TMDB_IMG_BASE_URL = "https://image.tmdb.org/t/p/w500"


def _get_api_key():
    """Read TMDB API key from env or Streamlit secrets."""
    env_key = os.getenv("TMDB_API_KEY")
    if env_key:
        return env_key
    try:
        return st.secrets["TMDB_API_KEY"]
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def cached_fetch_poster(movie_id: int):
    """Return poster URL for a movie id, or None if not available."""
    api_key = _get_api_key()
    if not api_key:
        return None

    url = TMDB_BASE_URL.format(movie_id, api_key)
    r = requests.get(url, timeout=10)
    if r.status_code != 200:
        return None

    data = r.json()
    poster_path = data.get("poster_path")
    if not poster_path:
        return None

    return TMDB_IMG_BASE_URL + poster_path

