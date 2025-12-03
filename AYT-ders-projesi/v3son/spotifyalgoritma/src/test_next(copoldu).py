import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time

load_dotenv()

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=os.getenv("SPOTIPY_CLIENT_ID"),
        client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
        redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
        scope=os.getenv("SPOTIPY_SCOPE")
    )
)

# 1) Cihazları listele
devices = sp.devices()
print("Cihazlar:")
for d in devices["devices"]:
    print("-", d["name"], "| ID:", d["id"], "| Type:", d["type"])

device_id = input("\nÇalınacak cihazın ID'sini yaz: ").strip()
track_input = input("\nBaşlangıç şarkısı (ID veya URL): ").strip()

# URL'den ID çıkar
track_id = track_input.split("track/")[-1].split("?")[0]

print(f"\nSeed şarkı açılıyor: {track_id}")
sp.start_playback(
    device_id=device_id,
    uris=[f"spotify:track:{track_id}"]
)
time.sleep(2)  # öneri kuyruğunun oluşması için
sp.next_track(device_id=device_id)

print("5 saniye dinleniyor...")
time.sleep(5)

# O an çalanı al
first = sp.current_playback()
print("\nBaşlangıç şarkısı:")
print("→", first["item"]["name"], "-", first["item"]["artists"][0]["name"])

# NEXT TEST
print("\nSpotify önerisine geçiliyor...")
sp.next_track(device_id=device_id)

# Yeni şarkının başlaması için Spotify'a 2 saniye ver
time.sleep(2)

second = sp.current_playback()
print("\nYeni çalan şarkı:")
print("→", second["item"]["name"], "-", second["item"]["artists"][0]["name"])

print("\nNEXT TEST TAMAM 🔥")
