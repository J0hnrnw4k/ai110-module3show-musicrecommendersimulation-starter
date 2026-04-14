"""
main.py
Entry point for the Music Recommender Simulation.

HOW TO RUN (from inside the music_recommender/ folder):
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs

# ──────────────────────────────────────────────────────────
#  User Profiles  –  edit these or add more to experiment!
# ──────────────────────────────────────────────────────────

PROFILES = {
    "🎉 High-Energy Pop Fan": {
        "favorite_genre":     "pop",
        "favorite_mood":      "happy",
        "target_energy":      0.8,
        "target_danceability": 0.85,
        "target_acousticness": 0.05,
    },
    "😌 Chill Lofi / Indie Listener": {
        "favorite_genre":     "indie",
        "favorite_mood":      "melancholic",
        "target_energy":      0.4,
        "target_danceability": 0.45,
        "target_acousticness": 0.5,
    },
    "🤘 Deep Intense Rock Head": {
        "favorite_genre":     "rock",
        "favorite_mood":      "energetic",
        "target_energy":      0.85,
        "target_danceability": 0.6,
        "target_acousticness": 0.05,
    },
}

TOP_K = 5  # number of recommendations per profile


# ──────────────────────────────────────────────────────────
#  Output formatter
# ──────────────────────────────────────────────────────────

def print_recommendations(profile_name, user_prefs, recs):
    """Print a clean terminal block for one user profile."""
    print("\n" + "═" * 62)
    print(f"  Profile : {profile_name}")
    print(f"  Genre   : {user_prefs['favorite_genre']}  |  "
          f"Mood: {user_prefs['favorite_mood']}  |  "
          f"Energy target: {user_prefs['target_energy']}")
    print("═" * 62)

    for rank, song in enumerate(recs, start=1):
        print(f"\n  #{rank}  {song['title']}  —  {song['artist']}")
        print(f"       Score   : {song['final_score']}")
        print(f"       Reasons : {', '.join(song['reasons'])}")

    print()


# ──────────────────────────────────────────────────────────
#  Main
# ──────────────────────────────────────────────────────────

def main():
    songs = load_songs()
    print(f"\nLoaded songs: {len(songs)}")

    for profile_name, user_prefs in PROFILES.items():
        recs = recommend_songs(user_prefs, songs, k=TOP_K)
        print_recommendations(profile_name, user_prefs, recs)


if __name__ == "__main__":
    main()
