import pickle
import pandas as pd
import numpy as np
from .tmdb_api import fetch_poster

def load_data(
    movie_path: str = "data/movie_dict.pkl",
    sim_path: str = "data/similarity.pkl",
):
    movies_dict = pickle.load(open(movie_path, "rb"))
    movies = pd.DataFrame(movies_dict)

    similarity = pickle.load(open(sim_path, "rb"))
    if isinstance(similarity, pd.DataFrame):
        similarity = similarity.apply(pd.to_numeric, errors="coerce").values
    else:
        similarity = np.array(similarity, dtype=float)

    return movies, similarity

def recommend(movie: str, movies, similarity, top_n: int = 5):
    if movie not in movies["title"].values:
        return [], [], []

    movie_index = movies[movies["title"] == movie].index[0]

    distances = np.array(similarity[movie_index], dtype=float)

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1],
    )[1 : top_n + 1]

    recommended_movies = []
    recommended_posters = []
    meta_info = []

    for i, score in movies_list:
        movie_row = movies.iloc[i]
        movie_id = movie_row.movie_id

        poster_url, meta = fetch_poster(movie_id)

        year = None
        rating = None
        overview = None
        tmdb_id = None
        if meta:
            year = (meta.get("release_date") or "")[:4]
            rating = meta.get("vote_average")
            overview = meta.get("overview")
            tmdb_id = meta.get("id")

        recommended_movies.append(movie_row.title)
        recommended_posters.append(poster_url)
        meta_info.append(
            {
                "year": year,
                "rating": rating,
                "overview": overview,
                "tmdb_id": tmdb_id,
            }
        )

    return recommended_movies, recommended_posters, meta_info
