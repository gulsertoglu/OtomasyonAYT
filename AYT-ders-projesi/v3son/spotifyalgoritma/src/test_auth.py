import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=os.getenv("SPOTIPY_SCOPE")
    )
)

user = sp.current_user()
print("Bağlantı başarılı!")
print("Kullanıcı adı:", user["display_name"])
print("Kullanıcı ID:", user["id"])



## Bu sistem, Spotify üzerinden doğrulama almamızı sağlıyor.