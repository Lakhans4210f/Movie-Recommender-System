import os
import requests
import streamlit as st

API_KEY = os.getenv("TMDB_API_KEY")

def fetch_poster(movie_id):
    if not API_KEY:
        return "https://via.placeholder.com/500x750?text=API+Key+Missing", {}

    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=en-US"
    )

    try:
        response = requests.get(url, timeout=5)
        data = response.json()

        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path, data
        else:
            return "https://via.placeholder.com/500x750?text=No+Image", data

    except Exception:
        return "https://via.placeholder.com/500x750?text=Error", {}

@st.cache_data(show_spinner=False)
def cached_fetch_poster(movie_id):
    return fetch_poster(movie_id)

