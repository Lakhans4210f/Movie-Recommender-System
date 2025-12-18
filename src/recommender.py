import os
import pickle
import pandas as pd
import numpy as np
import requests

from src.tmdb_api import cached_fetch_poster

# Use new file names so Streamlit Cloud downloads fresh, correct pickles
MOVIE_PATH = "data/movie_dict_v2.pkl"
SIM_PATH = "data/similarity_v2.pkl"

# Direct-download links for Google Drive
MOVIE_URL = "https://drive.google.com/uc?export=download&id=1CTqPbcArGDjHC3Zmv4nMPox2KW3hIbhw"
SIM_URL = "https://drive.google.com/uc?export=download&id=1tCM6YIEycTvWOhzZO4wc8Xtb1FIW1GKq"


def _download_file(url: str, path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)


def ensure_files() -> None:
    if not os.path.exists(MOVIE_PATH):
        _download_file(MOVIE_URL, MOVIE_PATH)
    if not os.path.exists(SIM_PATH):
        _download_file(SIM_URL, SIM_PATH)


def load_data(movie_path: str = MOVIE_PATH, sim_path: str = SIM_PATH):
    """Download (if needed) and load movies DataFrame and similarity matrix."""
    ensure_files()

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
    """Return list of (title, poster_url) for top_n similar movies."""
    movie_title = movie_title.strip().lower()
    titles = movies["title"].str.lower()

    if movie_title not in titles.values:
        return []

    idx = titles[titles == movie_title].index[0]
    distances = similarity[idx]

    sim_scores = sorted(
        list(enumerate(distances)),
        key=lambda x: x[1],
        reverse=True
    )[1 : top_n + 1]

    recommendations = []
    for i, _ in sim_scores:
        title = movies.iloc[i].title
        movie_id = int(movies.iloc[i].movie_id)
        poster = cached_fetch_poster(movie_id)
        recommendations.append((title, poster))

    return recommendations

