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

# 2) Kullanıcıdan cihaz seçmesini iste
device_id = input("\nÇalınacak cihazın ID'sini yaz: ").strip()

# 3) Başlangıç şarkısı ID veya URL
track_input = input("\nBaşlangıç şarkısı (ID veya URL): ").strip()

# Eğer URL verildiyse ID'yi çıkar
track_id = track_input.split("track/")[-1].split("?")[0]

print(f"\nŞarkı açılıyor: {track_id}")
sp.start_playback(device_id=device_id, uris=[f"spotify:track:{track_id}"])

print("Şarkı çalıyor... (10 saniye dinleyelim)")
time.sleep(10)

current = sp.current_playback()
print("\nO an çalan:", current["item"]["name"], "-", current["item"]["artists"][0]["name"])
print("Playback test TAMAM.")
