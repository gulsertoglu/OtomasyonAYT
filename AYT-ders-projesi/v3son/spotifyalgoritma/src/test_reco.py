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

seed_input = input("Seed şarkı (ID veya URL): ").strip()
seed_id = seed_input.split("track/")[-1].split("?")[0]

print(f"\nSpotify'a soruluyor: {seed_id} için öneriler...\n")

recs = sp.recommendations(seed_tracks=[seed_id], limit=5)

for i, track in enumerate(recs["tracks"], start=1):
    name = track["name"]
    artists = ", ".join(a["name"] for a in track["artists"])
    tid = track["id"]
    print(f"{i}. {name} - {artists} | id: {tid}")
