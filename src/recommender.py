"""
recommender.py
Core logic for the Music Recommender Simulation.
Run this project from the music_recommender/ folder:
    python -m src.main
"""

import csv
import os


def load_songs(filepath="data/songs.csv"):
    """Load songs from CSV and return a list of dicts with typed values."""
    # Build an absolute path so this works no matter where you run it from
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    full_path = os.path.join(base_dir, filepath)

    songs = []
    with open(full_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"].strip().lower(),
                "mood":         row["mood"].strip().lower(),
                "energy":       float(row["energy"]),
                "tempo_bpm":    int(row["tempo_bpm"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


def score_song(user_prefs, song):
    """
    Score one song against the user preference dictionary.

    Scoring recipe
    --------------
    +2.0   genre match (exact)
    +1.5   mood match  (exact)
    +1.0   energy similarity      → 1.0 - |user_target - song_value|
    +0.75  danceability similarity → 0.75 * (1.0 - |...|)
    +0.50  acousticness similarity → 0.50 * (1.0 - |...|)

    Returns
    -------
    (score: float, reasons: list[str])
    """
    score   = 0.0
    reasons = []

    # --- Categorical matches ---
    if song["genre"] == user_prefs.get("favorite_genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    if song["mood"] == user_prefs.get("favorite_mood", "").lower():
        score += 1.5
        reasons.append("mood match (+1.5)")

    # --- Numerical similarity: energy ---
    energy_score = round(1.0 - abs(user_prefs.get("target_energy", 0.5) - song["energy"]), 3)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    # --- Numerical similarity: danceability ---
    dance_score = round(0.75 * (1.0 - abs(user_prefs.get("target_danceability", 0.5) - song["danceability"])), 3)
    score += dance_score
    reasons.append(f"danceability similarity (+{dance_score})")

    # --- Numerical similarity: acousticness ---
    acoustic_score = round(0.5 * (1.0 - abs(user_prefs.get("target_acousticness", 0.2) - song["acousticness"])), 3)
    score += acoustic_score
    reasons.append(f"acousticness similarity (+{acoustic_score})")

    return round(score, 3), reasons


def recommend_songs(user_prefs, songs, k=5):
    """
    Rank every song by score and return the top-k results.

    Uses sorted() so the original songs list is never mutated.
    Each result dict contains all song fields + 'final_score' + 'reasons'.
    """
    scored = []
    for song in songs:
        final_score, reasons = score_song(user_prefs, song)
        scored.append({**song, "final_score": final_score, "reasons": reasons})

    # sorted() → new list, highest score first
    return sorted(scored, key=lambda x: x["final_score"], reverse=True)[:k]
