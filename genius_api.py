import requests

GENIUS_API_BASE_URL = "https://api.genius.com"
GENIUS_API_TOKEN = "YOUR_GENIUS_API_ACCESS_TOKEN"  # Replace with your actual token

headers = {
    "Authorization": f"Bearer {GENIUS_API_TOKEN}"
}

def search_songs(query):
    """Search songs on Genius API by query string."""
    search_url = f"{GENIUS_API_BASE_URL}/search"
    params = {"q": query}
    response = requests.get(search_url, headers=headers, params=params)
    if response.status_code == 200:
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
        return results
    else:
        return []

def get_song_lyrics(song_url):
    """Fetch song lyrics by scraping the Genius song page."""
    # Genius API does not provide lyrics directly, so we scrape the page
    from bs4 import BeautifulSoup
    page = requests.get(song_url)
    if page.status_code != 200:
        return None
    html = BeautifulSoup(page.text, "html.parser")
    # Lyrics are inside <div> with class 'lyrics' or in <div> with data-lyrics-container attribute
    lyrics_div = html.find("div", class_="lyrics")
    if lyrics_div:
        return lyrics_div.get_text(strip=True)
    else:
        # New Genius page layout
        lyrics_containers = html.find_all("div", attrs={"data-lyrics-container": "true"})
        lyrics = "\n".join([div.get_text(separator="\n", strip=True) for div in lyrics_containers])
        return lyrics if lyrics else None
