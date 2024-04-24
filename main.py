import requests
from bs4 import BeautifulSoup

URL = "https://www.billboard.com/charts/hot-100/"

user_response = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(URL+user_response)
songs_page = response.text

soup = BeautifulSoup(songs_page, "html.parser")
titles = soup.select("li ul li h3")
top_songs = [song.get_text().strip() for song in titles]
print(top_songs)

