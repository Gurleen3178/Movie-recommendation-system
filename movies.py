import requests
import streamlit as st

API_KEY = st.secrets["TMDB_API_KEY"]
BASE_URL = "https://api.themoviedb.org/3"

headers = {
    "accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

def fetch_100_movies(endpoint, extra_params=None):
    """Helper to pull 5 pages (100 movies) safely"""
    if extra_params is None:
        extra_params = {}
    
    combined_results = []
    for page in range(1, 6):
        params = {"api_key": API_KEY, "page": page, **extra_params}
        try:
            url = f"{BASE_URL}/{endpoint}"
            response = requests.get(url, params=params, headers=headers, timeout=5)
            if response.status_code == 200:
                page_data = response.json().get("results", [])
                combined_results.extend(page_data)
        except Exception:
            break
            
    return combined_results

@st.cache_data(ttl=3600)
def get_trending_movies():
    return fetch_100_movies("trending/movie/day")

@st.cache_data(ttl=3600)
def get_movies_by_genre(genre_id):
    return fetch_100_movies("discover/movie", {"with_genres": genre_id, "sort_by": "popularity.desc"})

@st.cache_data(ttl=600)
def search_movies(query):
    if not query.strip():
        return []
    url = f"{BASE_URL}/search/movie"
    params = {"api_key": API_KEY, "query": query}
    try:
        # Fixed: Included headers here so TMDB doesn't block the request
        res = requests.get(url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            return res.json().get("results", [])
    except Exception:
        pass
    return []