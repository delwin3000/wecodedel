import requests
import time

GENIUS_API_BASE_URL = "https://api.genius.com"
GENIUS_API_TOKEN = "YOUR_GENIUS_API_ACCESS_TOKEN"  # Replace with your actual token

headers = {
    "Authorization": f"Bearer {GENIUS_API_TOKEN}"
}

# Simple in-memory cache for search results to reduce API calls
_search_cache = {}
_CACHE_EXPIRY = 60 * 5  # 5 minutes

def search_songs(query):
    """Search songs on Genius API by query string with caching."""
    current_time = time.time()
    if query in _search_cache:
        cached_time, cached_results = _search_cache[query]
        if current_time - cached_time < _CACHE_EXPIRY:
            return cached_results

    search_url = f"{GENIUS_API_BASE_URL}/search"
    params = {"q": query}
    try:
        response = requests.get(search_url, headers=headers, params=params, timeout=5)
        response.raise_for_status()
    except requests.RequestException:
        return []

    data = response.json()
    hits = data.get("response", {}).get("hits", [])
    results = []
    for hit in hits:
        song_info = hit.get("result", {})
        results.append({
            "id": song_info.get("id"),
            "title": song_info.get("title"),
            "artist": song_info.get("primary_artist", {}).get("name"),
            "url": song_info.get("url")
        })

    _search_cache[query] = (current_time, results)
    return results

def get_song_lyrics(song_url):
    """Fetch song lyrics by scraping the Genius song page."""
    from bs4 import BeautifulSoup
    try:
        page = requests.get(song_url, timeout=5)
        page.raise_for_status()
    except requests.RequestException:
        return None

    html = BeautifulSoup(page.text, "html.parser")
    lyrics_div = html.find("div", class_="lyrics")
    if lyrics_div:
        return lyrics_div.get_text(strip=True)
    else:
        lyrics_containers = html.find_all("div", attrs={"data-lyrics-container": "true"})
        lyrics = "\n".join([div.get_text(separator="\n", strip=True) for div in lyrics_containers])
        return lyrics if lyrics else None
