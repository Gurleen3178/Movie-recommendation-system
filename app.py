import streamlit as st
import movies as mv

st.set_page_config(
    page_title="MovieVerse",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 MovieVerse")

# --- GLOBAL SEARCH BAR ---
search_query = st.text_input("🔍 Search for a movie of your liking:", placeholder="Type movie name here and press Enter...")

# --- REUSABLE GRID WITH EXPANSION MECHANICS ---
def display_movie_row(title_label, movies_list, key_prefix):
    if not movies_list:
        st.warning("No movies found.")
        return

    st.subheader(title_label)
    
    # Initialize a toggle state for this specific row section
    state_key = f"expand_{key_prefix}"
    if state_key not in st.session_state:
        st.session_state[state_key] = False

    # Decide whether to show just 5 movies, or the full 100 pack
    is_expanded = st.session_state[state_key]
    display_limit = len(movies_list) if is_expanded else 5
    visible_movies = movies_list[:display_limit]

    # Create a layout grid dynamically (5 items per row)
    for i in range(0, len(visible_movies), 5):
        chunk = visible_movies[i:i+5]
        cols = st.columns(5)
        for index, movie in enumerate(chunk):
            with cols[index]:
                poster_path = movie.get("poster_path")
                if poster_path:
                    st.image(f"https://image.tmdb.org/t/p/w500{poster_path}", use_container_width=True)
                else:
                    st.image("https://placehold.co/500x750?text=No+Poster", use_container_width=True)
                
                st.write(f"**{movie.get('title', 'N/A')}**")
                st.write(f"⭐ {movie.get('vote_average', 'N/A')}")
                
                # Interactive Summary Expander Clicker
                with st.expander("📖 View Summary"):
                    st.write(movie.get("overview", "No summary available for this movie."))

    # Show the expansion control button underneath the first 5 items (Don't need it for search results)
    if len(movies_list) > 5 and key_prefix != "search":
        if not is_expanded:
            if st.button("➕ Show More Movies", key=f"btn_more_{key_prefix}"):
                st.session_state[state_key] = True
                st.rerun()
        else:
            if st.button("➖ Show Less", key=f"btn_less_{key_prefix}"):
                st.session_state[state_key] = False
                st.rerun()

# --- APPLICATION DISPATCH LOGIC ---
if search_query:
    search_results = mv.search_movies(search_query)
    display_movie_row(f"🔍 Search Results for: '{search_query}'", search_results, key_prefix="search")
    
    # Simple reset helper link
    st.write("---")
    st.info("💡 To go back to the home genres, clear the search text bar above.")

else:
    # 1. Trending
    display_movie_row("🔥 Trending Movies", mv.get_trending_movies(), key_prefix="trending")
    st.write("---")
    
    # 2. Romance
    display_movie_row("💖 Romance Stories", mv.get_movies_by_genre(10749), key_prefix="romance")
    st.write("---")
    
    # 3. Action
    display_movie_row("💥 Action Pack", mv.get_movies_by_genre(28), key_prefix="action")
    st.write("---")
    
    # 4. Comedy
    display_movie_row("😂 Comedy Club", mv.get_movies_by_genre(35), key_prefix="comedy")
    st.write("---")
    
    # 5. Sci-Fi
    display_movie_row("🚀 Sci-Fi Adventures", mv.get_movies_by_genre(878), key_prefix="scifi")
    st.write("---")
    
    # 6. Horror
    display_movie_row("😱 Horror Night", mv.get_movies_by_genre(27), key_prefix="horror")
    
