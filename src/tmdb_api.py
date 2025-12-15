import requests

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

def fetch_poster(movie_id):
    url = (
        f"https://api.themoviedb.org/3/movie/{movie_id}"
        f"?api_key={API_KEY}&language=en-US"
    )
    try:
        response = requests.get(url)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path, data
        else:
            return "https://via.placeholder.com/500x750?text=No+Image", data
    except Exception:
        return "https://via.placeholder.com/500x750?text=Error", {}
