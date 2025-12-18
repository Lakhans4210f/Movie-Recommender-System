import pickle
import pandas as pd
import numpy as np

from src.tmdb_api import cached_fetch_poster

MOVIE_PATH = "data/movie_dict.pkl"
SIM_PATH = "data/similarity.pkl"


def load_data(movie_path: str = MOVIE_PATH, sim_path: str = SIM_PATH):
    """Load movies DataFrame and similarity matrix from local data/ folder."""
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
