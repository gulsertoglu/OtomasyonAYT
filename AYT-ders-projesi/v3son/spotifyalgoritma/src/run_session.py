import os
import time
import json
from datetime import datetime
from typing import Dict, List, Optional

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()

def get_spotify_client() -> spotipy.Spotify:
    return spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=os.getenv("SPOTIPY_CLIENT_ID"),
            client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"),
            redirect_uri=os.getenv("SPOTIPY_REDIRECT_URI"),
            scope=os.getenv("SPOTIPY_SCOPE")
        )
    )

def wait_until_new_track(sp: spotipy.Spotify, previous_id: str, timeout: int = 15) -> Optional[Dict]:
    """next_track sonrası gerçekten yeni bir parçaya geçildi mi, onu bekler."""
    start = time.time()
    while time.time() - start < timeout:
        pb = sp.current_playback()
        if pb and pb.get("item"):
            tid = pb["item"]["id"]
            if tid and tid != previous_id:
                return pb
        time.sleep(1)
    return None

def get_track_info(sp: spotipy.Spotify, track_id: str) -> Dict:
    track = sp.track(track_id)

    artist_id = track["artists"][0]["id"] if track["artists"] else None
    artist_genres = []
    if artist_id:
        artist = sp.artist(artist_id)
        artist_genres = artist.get("genres", [])

    return {
        "id": track["id"],
        "name": track["name"],
        "artists": [a["name"] for a in track["artists"]],
        "album": track["album"]["name"],
        "album_id": track["album"]["id"],
        "release_date": track["album"]["release_date"],
        "duration_ms": track["duration_ms"],
        "popularity": track["popularity"],
        "artist_genres_main": artist_genres,
        # audio_features olmadan da yaşayacağız şimdilik :)
    }


def run_session(num_steps: int = 10, listen_seconds: int = 60) -> Dict:
    sp = get_spotify_client()

    # Cihaz seçimi (next_track için)
    devices = sp.devices()
    print("Cihazlar:")
    for d in devices["devices"]:
        print("-", d["name"], "| ID:", d["id"], "| Type:", d["type"])

    device_id = input("\nKullanılacak cihaz ID'si: ").strip()

    print("\nSpotify'da bir şarkı radyosu / autoplay kuyruğu BAŞLATMIŞ olman gerekiyor.")
    input("Hazırsan Enter'a bas (şu an bir şarkı çalıyor olmalı)... ")

    session_tracks: List[Dict] = []

    for step in range(num_steps):
        pb = sp.current_playback()
        if not pb or not pb.get("item"):
            print("Şu an çalan bir şarkı bulunamadı, biraz bekleyip tekrar dene.")
            break

        item = pb["item"]
        current_id = item["id"]
        name = item["name"]
        artist = item["artists"][0]["name"] if item["artists"] else "Unknown"

        print(f"\n[{step+1}/{num_steps}] Şarkı: {name} - {artist}")
        print(f"{listen_seconds} saniye dinleniyor...")
        time.sleep(listen_seconds)

        info = get_track_info(sp, current_id)
        info["order_index"] = step
        session_tracks.append(info)

        if step == num_steps - 1:
            print("\nSon şarkıya geldik, next yapmıyorum.")
            break

        print("Spotify önerisine (sıradaki şarkıya) geçiliyor...")
        sp.next_track(device_id=device_id)
        wait_until_new_track(sp, previous_id=current_id)

    session_data = {
        "created_at": datetime.utcnow().isoformat() + "Z",
        "num_steps": num_steps,
        "listen_seconds": listen_seconds,
        "tracks": session_tracks,
    }

    return session_data

def save_session(session_data: Dict, out_dir: str = "data/sessions") -> str:
    os.makedirs(out_dir, exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    first = session_data["tracks"][0] if session_data["tracks"] else {}
    seed_name = first.get("name", "unknown").replace(" ", "_")[:25]
    filename = f"session_{ts}_{seed_name}.json"
    path = os.path.join(out_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(session_data, f, ensure_ascii=False, indent=2)

    return path

if __name__ == "__main__":
    steps_inp = input("Kaç şarkı loglansın? (örnek: 5): ").strip()
    steps = int(steps_inp or "5")

    listen_inp = input("Her şarkı kaç saniye dinlensin? (varsayılan 60): ").strip()
    listen_sec = int(listen_inp or "60")

    session = run_session(num_steps=steps, listen_seconds=listen_sec)
    out_path = save_session(session)
    print(f"\nOturum JSON olarak kaydedildi:\n{out_path}")
