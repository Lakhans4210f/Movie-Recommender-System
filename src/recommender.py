import os
import pickle
import pandas as pd
import numpy as np
import requests
from .tmdb_api import cached_fetch_poster

MOVIE_PATH = "data/movie_dict.pkl"
SIM_PATH = "data/similarity.pkl"

MOVIE_URL = "https://drive.google.com/file/d/1CTqPbcArGDjHC3Zmv4nMPox2KW3hIbhw/view?usp=sharing"       # TODO: replace
SIM_URL = "https://drive.google.com/file/d/1tCM6YIEycTvWOhzZO4wc8Xtb1FIW1GKq/view?usp=sharing"         # TODO: replace

def _download_file(url, path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    r = requests.get(url, stream=True)
    r.raise_for_status()
    with open(path, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)

def ensure_files():
    if not os.path.exists(MOVIE_PATH):
        _download_file(MOVIE_URL, MOVIE_PATH)
    if not os.path.exists(SIM_PATH):
        _download_file(SIM_URL, SIM_PATH)

def load_data(movie_path: str = MOVIE_PATH, sim_path: str = SIM_PATH):
    ensure_files()

    movies_dict = pickle.load(open(movie_path, "rb"))
    movies = pd.DataFrame(movies_dict)

    similarity = pickle.load(open(sim_path, "rb"))
    if isinstance(similarity, pd.DataFrame):
        similarity = similarity.apply(pd.to_numeric, errors="coerce").values
    else:
        similarity = np.array(similarity, dtype=float)

    return movies, similarity

