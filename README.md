# 🎵 Music Recommender Simulation

A content-based music recommendation engine built in Python.  
Given a user taste profile, it scores every song in the catalog and returns the **Top-5 most relevant tracks** — with a plain-English explanation for every recommendation.

---

## How to Run

> **Open the `music_recommender/` folder in VS Code, then open the integrated terminal.**

```bash
python -m src.main
```

No external libraries required — only Python's built-in `csv` and `os` modules.

---

## Folder Structure

```
music_recommender/
├── data/
│   └── songs.csv          ← 35-song catalog (7 genres, 5 moods)
├── src/
│   ├── __init__.py
│   ├── recommender.py     ← load_songs / score_song / recommend_songs
│   └── main.py            ← 3 user profiles + terminal output
├── README.md
├── model_card.md
└── reflection.md
```

---

## How The System Works

Real platforms like Spotify and YouTube Music use two main strategies:

- **Collaborative filtering** — learns from what millions of similar users liked or skipped.
- **Content-based filtering** — matches songs to a user based on audio attributes (tempo, energy, mood, etc.).

This simulation uses **content-based filtering** because it is transparent: you can see exactly why each song was recommended.

### Algorithm Recipe

| Signal | Method | Max Points |
|--------|--------|-----------|
| Genre match | Exact string match | +2.0 |
| Mood match | Exact string match | +1.5 |
| Energy similarity | `1.0 − |user_target − song_value|` | +1.0 |
| Danceability similarity | `0.75 × (1.0 − |...|)` | +0.75 |
| Acousticness similarity | `0.50 × (1.0 − |...|)` | +0.50 |
| **Total possible** | | **5.75** |

### Data Flow

```
User Preference Dict
        ↓
  load_songs()  →  35 songs from data/songs.csv
        ↓
  score_song()  →  (numeric score, list of reasons)  ← run for every song
        ↓
  sorted()      →  ranked from highest to lowest score
        ↓
  Top-K results printed to terminal with title, score, and reasons
```

### Features Used

**Song attributes:** `id`, `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `danceability`, `acousticness`

**User profile keys:** `favorite_genre`, `favorite_mood`, `target_energy`, `target_danceability`, `target_acousticness`

---

## Terminal Output Screenshots

*(Paste your screenshots here after running `python -m src.main`)*

**Profile 1 — High-Energy Pop Fan**

```
#1  Shake It Off  —  Taylor Swift
    Score   : 5.75
    Reasons : genre match (+2.0), mood match (+1.5), energy similarity (+1.0), danceability similarity (+0.75), acousticness similarity (+0.5)
```

**Profile 2 — Chill Lofi / Indie Listener**

```
#1  Sweater Weather  —  The Neighbourhood
    Score   : 5.425
    Reasons : genre match (+2.0), mood match (+1.5), energy similarity (+0.85), danceability similarity (+0.675), acousticness similarity (+0.4)
```

**Profile 3 — Deep Intense Rock Head**

```
#1  R U Mine?  —  Arctic Monkeys
    Score   : 5.7
    Reasons : genre match (+2.0), mood match (+1.5), energy similarity (+0.95), danceability similarity (+0.75), acousticness similarity (+0.5)
```

---

## Potential Biases

- **Genre gate:** Genre is worth 2.0 points — the single largest signal. Songs in the wrong genre almost never crack the top results even if every numerical feature matches perfectly.
- **Dataset skew:** Pop has ~10 songs; indie has only 3. Pop listeners get more variety; indie listeners' top-5 gets filled with non-indie songs at the lower ranks.
- **Filter bubble:** A rock listener will never see a great electronic song with identical energy, because genre acts as a hard barrier before numerical similarity is even considered.
