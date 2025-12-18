import os
import sys

# Ensure root directory is on sys.path (needed on Streamlit Cloud)
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
if ROOT_DIR not in sys.path:
    sys.path.append(ROOT_DIR)

import streamlit as st
from src.recommender import load_data, recommend
from src.tmdb_api import cached_fetch_poster

import streamlit as st
from src.recommender import load_data, recommend
from src.tmdb_api import cached_fetch_poster

# ---------- Page config ----------
st.set_page_config(
    page_title="🎬 Movie Recommender",
    page_icon="🎥",
    layout="wide",
)

# ---------- Custom CSS ----------
st.markdown(
    """
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        text-align: center;
        padding: 0.5rem 0 1rem 0;
    }
    .movie-card {
        background-color: #111827;
        border-radius: 12px;
        padding: 10px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.35);
        text-align: center;
    }
    .movie-title {
        font-size: 16px;
        font-weight: 700;
        margin-top: 8px;
        color: #f9fafb;
    }
    .movie-meta {
        font-size: 12px;
        color: #9ca3af;
        margin-bottom: 4px;
    }
    .movie-overview {
        font-size: 12px;
        color: #d1d5db;
        height: 60px;
        overflow: hidden;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Optional gradient header background
st.markdown(
    """
    <div style="
        background: linear-gradient(90deg,#1f2933,#111827);
        padding: 0.5rem 1rem;
        border-radius: 0 0 18px 18px;
        margin-bottom: 1rem;">
        <div class="main-title">🎬 Movie Recommender System</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------- Load data ----------
movies, similarity = load_data()

# ---------- Sidebar controls ----------
with st.sidebar:
    st.header("⚙️ Settings")
    st.markdown("Adjust how recommendations are shown.")
    top_n = st.slider("Number of recommendations", 3, 10, 5)
    show_overview = st.checkbox("Show overview snippet", True)
    show_rating = st.checkbox("Show rating & year", True)
    st.markdown("---")
    st.markdown("Tip: Try different movies and compare suggestions.")

# ---------- Main layout with tabs ----------
tab1, tab2 = st.tabs(["🔍 Recommend", "📚 Explore dataset"])

with tab1:
    st.subheader("Find similar movies")

    col_left, col_right = st.columns([2, 1])

    with col_left:
        selected_movie = st.selectbox(
            "Select a movie you like",
            movies["title"].values,
        )

    with col_right:
        st.info(
            "Pick a movie and get similar recommendations based on content features."
        )

    # Selected movie poster + info with spinner + cache
    if selected_movie:
        sel_id = movies.loc[
            movies["title"] == selected_movie, "movie_id"
        ].values[0]
        with st.spinner("Loading selected movie details..."):
            sel_poster, sel_meta = cached_fetch_poster(sel_id)

        st.markdown("### Selected movie")
        c1, c2 = st.columns([1, 2])
        with c1:
            st.image(sel_poster, width=230)
        with c2:
            st.write(selected_movie)
            if sel_meta.get("release_date"):
                st.write("Year:", sel_meta["release_date"][:4])
            if sel_meta.get("vote_average") is not None:
                st.write("Rating:", f"{sel_meta['vote_average']:.1f}")
            if sel_meta.get("overview"):
                ov = sel_meta["overview"]
                st.write(ov if len(ov) <= 350 else ov[:350] + "…")

    if st.button("Recommend 🎯", type="primary"):
        with st.spinner("Fetching great movies for you..."):
            names, posters, meta_info = recommend(
                selected_movie, movies, similarity, top_n=top_n
            )

        if names and posters:
            cols = st.columns(min(top_n, 5))

            for idx, name in enumerate(names):
                col = cols[idx % len(cols)]
                with col:
                    st.markdown(
                        '<div class="movie-card">', unsafe_allow_html=True
                    )

                    st.image(posters[idx], width=230)

                    st.markdown(
                        f'<div class="movie-title">{name}</div>',
                        unsafe_allow_html=True,
                    )

                    meta = meta_info[idx]
                    meta_text_parts = []
                    if show_rating and meta.get("rating") is not None:
                        meta_text_parts.append(f"⭐ {meta['rating']:.1f}")
                    if show_rating and meta.get("year"):
                        meta_text_parts.append(f"📅 {meta['year']}")
                    if meta_text_parts:
                        st.markdown(
                            f'<div class="movie-meta">{" • ".join(meta_text_parts)}</div>',
                            unsafe_allow_html=True,
                        )

                    if show_overview and meta.get("overview"):
                        short_ov = (
                            meta["overview"][:180] + "…"
                            if len(meta["overview"]) > 180
                            else meta["overview"]
                        )
                        st.markdown(
                            f'<div class="movie-overview">{short_ov}</div>',
                            unsafe_allow_html=True,
                        )

                    if meta.get("tmdb_id"):
                        tmdb_url = f"https://www.themoviedb.org/movie/{meta['tmdb_id']}"
                        st.markdown(
                            f"[🔗 More details]({tmdb_url})",
                            unsafe_allow_html=True,
                        )

                    st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.warning("No similar movies found. Try another title.")

with tab2:
    st.subheader("Dataset preview")
    st.markdown("Preview of the movies used in this recommender.")
    st.dataframe(movies.head(50))
