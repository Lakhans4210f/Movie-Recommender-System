import os
import pickle
import pandas as pd
import numpy as np
from src.tmdb_api import cached_fetch_poster

# Build paths relative to project root so it works on Streamlit Cloud
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT_DIR, "data")

MOVIE_PATH = os.path.join(DATA_DIR, "movie_dict.pkl")
SIM_PATH = os.path.join(DATA_DIR, "similarity.pkl")


def load_data(movie_path: str = MOVIE_PATH, sim_path: str = SIM_PATH):
    """Load movies DataFrame and similarity matrix from data/ folder."""
    with open(movie_path, "rb") as f:
        movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)

    with open(sim_path, "rb") as f:
        similarity = pickle.load(f)

    if isinstance(similarity, pd.DataFrame):
        similarity = similarity.apply(pd.to_numeric, errors="coerce").values
    else:
        similarity = np.array(similarity, dtype=float)

    return movies, similarity


def recommend(movie_title: str, movies, similarity, top_n: int = 5):
    """
    Return:
        names: list[str]
        posters: list[str or None]
        meta_info: list[dict] with keys: rating, year, overview, tmdb_id
    """
    movie_title_norm = movie_title.strip().lower()
    titles = movies["title"].str.lower()

    if movie_title_norm not in titles.values:
        return [], [], []

    idx = titles[titles == movie_title_norm].index[0]
    distances = similarity[idx]

    sim_scores = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1 : top_n + 1]

    names = []
    posters = []
    meta_info = []

    for i, _ in sim_scores:
        row = movies.iloc[i]
        title = row["title"]
        movie_id = int(row["movie_id"])

        # Expect cached_fetch_poster to return (poster_url, meta_dict)
        poster_url, meta = cached_fetch_poster(movie_id)

        names.append(title)
        posters.append(poster_url)

        meta_dict = {
            "rating": meta.get("vote_average"),
            "year": meta.get("release_date", "")[:4] if meta.get("release_date") else None,
            "overview": meta.get("overview"),
            "tmdb_id": meta.get("id"),
        }
        meta_info.append(meta_dict)

    return names, posters, meta_info
