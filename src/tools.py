from smolagents import tool
import streamlit as st
import requests
import pandas as pd
# from duckduckgo_search import DDGS

# def duckduckgo_search(query: str, max_results: int = 3) -> list:
#     """Search the web using DuckDuckGo"""
#     with DDGS() as ddgs:
#         return [r for r in ddgs.text(query, max_results=max_results)]

#MAL Tools
@tool
def add_anime(anime_id: int, status:str = "Watching", episodes_watched: int = 0, score: int = 0) -> str:
    """
    Add an anime to your MyAnimeList.
    Args:
        anime_id (int): The ID of the anime to add.
        status (str): The status of the anime (e.g., "Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch").
        episodes_watched (int): The number of episodes watched.
        score (int): Your score for the anime (0-10).
    Returns:
        str: A message indicating the success or failure of the operation.
    """
    try:
        response = requests.patch(  # Changed to PATCH
            f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
            headers={
                "Authorization": f"Bearer {st.session_state.access_token}",
                "Content-Type": "application/x-www-form-urlencoded"  # Required
            },
            data={  # Use data instead of json
                "status": status,
                "num_watched_episodes": episodes_watched,
                "score": score
            }
        )
        response.raise_for_status()
        return "Anime added/updated successfully!"
    except Exception as e:
        return f"Failed to add anime: {str(e)}"

@tool
def remove_anime(anime_id: int) -> str:
    """
    Remove an anime from your MyAnimeList.
    Args:
        anime_id (int): The ID of the anime to remove.
    Returns:
        str: A message indicating the success or failure of the operation.
    """
    try:
        response = requests.delete(
            f"https://api.myanimelist.net/v2/anime/{anime_id}/my_list_status",
            headers={
                "Authorization": f"Bearer {st.session_state.access_token}",
            }
        )
        response.raise_for_status()
        return "Anime removed successfully!"
    except Exception as e:
        return f"Failed to remove anime: {e}"
    
@tool
def get_anime_list(status_filter: str = None) -> str:
    """
    Get the list of anime in your MyAnimeList.
    Args:
        status_filter (str): Filter by status (e.g., "Watching", "Completed", "On-Hold", "Dropped", "Plan to Watch").
    Returns:
        str: A markdown table representation of the anime list with columns: Name, Status, Episodes Watched, Total Episodes, and Score.
    """
    try:
        params = {
            "fields": "list_status,media_type,num_episodes",
            "limit": 100
        }
        if status_filter:
            params["status"] = status_filter.lower().replace(" ", "_")  # Convert to MAL format

        response = requests.get(
            "https://api.myanimelist.net/v2/users/@me/animelist",
            headers={"Authorization": f"Bearer {st.session_state.access_token}"},
            params=params
        )
        response.raise_for_status()  # Check for HTTP errors
        return format_anime_list(response.json().get("data", []))
    except Exception as e:
        return f"Error fetching list: {str(e)}"

    
@tool
def search_anime(query: str) -> str:
    """
    Search for anime by title.
    Args:
        query (str): The title of the anime to search for.
    Returns:
        str: A string representation of the search results.
    """
    try:
        response = requests.get(
            "https://api.myanimelist.net/v2/anime",
            headers={
                "Authorization": f"Bearer {st.session_state.access_token}",
            },
            params={
                "q": query,
                "limit": 10
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return f"Failed to search anime: {e}"
    
@tool    
def format_anime_list(anime_list: list) -> str:
    """
    Format the anime list as a markdown table.
    Args:
        anime_list (list): The list of anime entries.
    Returns:
        str: A markdown table representation of the anime list with columns: Name, Status, Episodes Watched, Total Episodes, and Score.
    """
    if not anime_list:
        return "No anime found."
    
    # Create markdown table header
    table = "| Name | Status | Episodes Watched | Total Episodes | Score |\n"
    table += "|------|--------|------------------|----------------|-------|\n"
    
    # Add rows for each anime
    for entry in anime_list:
        anime = entry["node"]
        list_status = entry["list_status"]
        
        title = anime["title"]
        status = list_status["status"].replace("_", " ").title()
        episodes_watched = list_status["num_episodes_watched"]
        total_episodes = anime.get("num_episodes", "Unknown")
        score = list_status.get("score", "Not Rated")
        
        # Handle score display
        score_display = str(score) if score and score > 0 else "Not Rated"
        
        # Escape pipe characters in title if any
        title_escaped = title.replace("|", "\\|")
        
        table += f"| {title_escaped} | {status} | {episodes_watched} | {total_episodes} | {score_display} |\n"
    
    return table
@tool
def display_anime_cards(search_results: list[dict]) -> str:
     """
    Render a list of anime search results as visually formatted cards using Streamlit.

    This function displays multiple anime entries in a structured, scrollable layout,
    where each anime is presented as a card with its cover image, title (linked to detail page),
    rating, episode count, and a truncated synopsis. Designed for use in interactive applications
    like SmolAgents, this enhances user experience by presenting search data in an intuitive format.

    Args:
        search_results (list[dict]): A list of dictionaries, where each dictionary contains metadata
            for a single anime. Expected keys in each dictionary:
                - title (str): Title of the anime.
                - cover_image (str): URL of the anime’s cover/poster image.
                - rating (float): Average rating (0.0 to 10.0 scale).
                - episodes (int): Total number of episodes.
                - synopsis (str): Brief plot summary.
                - url (str): Link to the anime’s full detail page.

    Returns:
        None: The function does not return any value.
        It directly renders UI components using the Streamlit.

    Example:
         search_results = [
             {
                 "title": "Naruto",
                 "cover_image": "https://cdn.example.com/naruto.jpg",
                 "rating": 7.9,
                 "episodes": 220,
                 "synopsis": "A young ninja strives to become Hokage...",
                 "url": "https://myanimelist.net/anime/20/Naruto"
             },
             ...
         ]
        display_anime_cards(search_results)
    """
     pass
    # for anime in search_results:
    #     # Extract cover image URL (prefer large, then medium, then fallback)
    #     cover_url = None
    #     if "main_picture" in anime:
    #         cover_url = anime["main_picture"].get("large") or anime["main_picture"].get("medium")
    #     elif "cover_url" in anime:
    #         cover_url = anime["cover_url"]
    #     else:
    #         cover_url = "https://via.placeholder.com/150x220.png?text=No+Image"

    #     with st.container(border=True):
    #         col1, col2 = st.columns([1, 3])
    #         with col1:
    #             st.image(cover_url, width=150)
    #         with col2:
    #             st.markdown(f"### {anime.get('title', 'Untitled')}")
    #             mal_score = anime.get('score', 0)
    #             normalized_rating = mal_score / 2  # Convert to 0-5 scale
    #             full_stars = int(normalized_rating)
    #             half_star = 1 if normalized_rating - full_stars >= 0.5 else 0
    #             empty_stars = 5 - full_stars - half_star
    #             stars = "⭐" * full_stars + "⯨" * half_star + "✰" * empty_stars
    #             st.markdown(f"**MAL Score:** {stars} ({mal_score}/10)")
    #             if 'episodes' in anime:
    #                 st.caption(f"Episodes: {anime['episodes']}")
    #             if 'status' in anime:
    #                 st.caption(f"Airing Status: {anime['status'].capitalize()}")
    # return "Displayed anime results successfully"

@tool
def hianime_watchlink(query: str) -> str:
    """
    Search for a HiAnime watch link for the anime in query make Sure its hianime.sx link.
    Args:
        query (str): The title of the anime to search for.
    Returns:
        str: A string representation of the hianime watch link or an error message.
    """
    pass
    # try:
    #     results = duckduckgo_search(f"{query} site:hianime.tv", max_results=1)
    #     return results[0]['href'] if results else "No HiAnime link found"
    # except Exception as e:
    #     return f"Search failed: {str(e)}"
    

@tool
def anime_suggestion(query: str) -> str:
    """
    Suggest an anime based on a query.
    Args:
        query (str): The title or description of the anime to suggest.
    Returns:
        str: A tabular representation of the suggested anime or an error message, this suggestion than searched through search_anime tool to get more information.
    """
    # try:
    #     results = duckduckgo_search(query + " anime suggestion")
    #     if not results:
    #         return "No anime suggestion found."
    #     return results[0].get("href", "No valid suggestion found.")
    # except Exception as e:
    #     return f"Failed to suggest anime: {e}"
    pass
