import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100/"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
USERNAME = os.getenv("SPOTIFY_USERNAME")

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,
                                               client_secret=CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               scope="playlist-modify-private",
                                               cache_path="token.txt",
                                               show_dialog=True,
                                               username=USERNAME))
user_id = sp.current_user()['id']

user_response = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year_input = user_response.split("-")[0]
response = requests.get(URL+user_response)
songs_page = response.text

soup = BeautifulSoup(songs_page, "html.parser")
titles = soup.select("li ul li h3")
top_songs = [song.get_text().strip() for song in titles]

song_uris = []

for song in top_songs:
    search_result = sp.search(q=f"track:{song} year:{year_input}", type="track")

    try:
        song_uris.append(search_result['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped")

playlist = sp.user_playlist_create(name=user_response, public=False, user=user_id, description="Top 100 Songs of this day")["id"]
sp.playlist_add_items(playlist_id=playlist, items=song_uris)




