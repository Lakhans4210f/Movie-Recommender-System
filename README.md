Movie Recommender System

This project is a movie recommender system built using Python and Streamlit.
It recommends similar movies based on a selected movie from the dataset.
Movie posters and basic information are fetched using the TMDB API.

This project was created to understand the working of recommendation systems and to practice building a small ML-based web application.

About the Project

The system uses a content-based filtering approach.
Movies are compared using their features and similarity scores are calculated.
Based on this similarity, the most relevant movies are recommended to the user.

Features

Recommend similar movies
Display movie posters
Show rating, release year, and overview
Select number of recommendations
Preview movie dataset

Technologies Used

Python
Pandas
NumPy
Scikit-learn
Streamlit
TMDB API

Folder Structure
Movie-Recommender-System/
│── app.py
│── README.md
│── requirements.txt
│── .gitignore
│
├── src/
│   ├── __init__.py
│   ├── recommender.py
│   └── tmdb_api.py
│
└── data/
    ├── movie_dict.pkl
    └── similarity.pkl
    
How It Works

Movie data is converted into feature vectors
Cosine similarity is used to compare movies
Top similar movies are selected
TMDB API is used to fetch posters and details
Results are displayed using Streamlit

What I Learned

Basics of recommendation systems
Working with similarity matrices
Handling large ML files in Git
Using environment variables for API keys
Future Scope
Add collaborative filtering
Improve UI design
Deploy the application online

Author
Lakhan Shelke
AI & Data Science Student
GitHub: https://github.com/Lakhans4210f
