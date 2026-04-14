# Model Card — VibeFinder 1.0

---

## Model Name
**VibeFinder 1.0** — a content-based music recommendation simulator.

---

## Goal / Task
Given a user's taste profile, VibeFinder scores every song in a CSV catalog and returns the top-K most relevant tracks. Each recommendation includes a plain-English explanation of why it ranked highly. This is an educational simulation — its purpose is to show how real recommendation engines transform preferences into ranked suggestions.

---

## Data Used
- **Source:** Hand-curated CSV file (`data/songs.csv`)
- **Size:** 35 songs
- **Attributes:** `id`, `title`, `artist`, `genre`, `mood`, `energy` (0–1), `tempo_bpm`, `danceability` (0–1), `acousticness` (0–1)
- **Genres covered:** pop, hip-hop, rock, alternative, indie, r&b, electronic
- **Moods covered:** happy, sad, melancholic, energetic, dark
- **Limits:** Small dataset. Only mainstream Western pop music from ~2015–2023. No classical, jazz, country, Latin, or K-pop.

---

## Algorithm Summary (Plain Language)

VibeFinder uses a **weighted scoring recipe** to judge each song:

1. **Genre match:** If the song's genre equals the user's preferred genre → +2.0 points. This is the biggest single signal.
2. **Mood match:** If the song's mood equals the user's preferred mood → +1.5 points.
3. **Energy similarity:** The closer a song's energy is to the user's target, the more points — up to +1.0. Formula: `1.0 - |user_target - song_value|`
4. **Danceability similarity:** Same method, worth up to +0.75 points.
5. **Acousticness similarity:** Same method, worth up to +0.50 points.

After scoring every song, the list is sorted from highest to lowest and the top-K results are returned.

---

## Observed Behavior / Biases

**Genre dominance (filter bubble):** Because genre is worth 2.0 points, a song that matches genre and mood has a 3.5-point head start over every other song — even if those songs have nearly identical energy and danceability. A "Chill Rock" listener will never see a great "Chill Electronic" track in their top results. This is a classic filter bubble: the system keeps recommending inside one lane and never surfaces adjacent genres.

**Dataset imbalance:** Pop has ~10 songs in the catalog, indie has only 3. Pop listeners get a wider variety of results. Indie listeners will see the same 3 indie songs dominate the top spots every time, with non-indie songs filling the remaining slots based purely on numerical similarity.

**Cold-start problem:** The system requires users to manually define their preference dictionary. It cannot learn from listening history, skips, or replays. If stated preferences don't match actual behavior, recommendations will be wrong with no way to self-correct.

---

## Evaluation Process

Three user profiles were tested:

| Profile | Genre | Mood | Energy Target |
|---------|-------|------|--------------|
| High-Energy Pop Fan | pop | happy | 0.80 |
| Chill Lofi / Indie Listener | indie | melancholic | 0.40 |
| Deep Intense Rock Head | rock | energetic | 0.85 |

Each produced a clearly distinct top-5 list. Genre matches dominated rankings in all three cases, confirming that genre weight acts as a strong primary filter before numerical signals matter.

**Weight-shift experiment:** Doubling energy's weight and halving genre's weight caused cross-genre songs to enter the top results (e.g., high-energy hip-hop appeared in the Rock Head's list). This confirmed that the default weights create a genre-first, energy-second ordering.

**Adversarial profile tested:** A profile with `energy: 0.9` and `mood: sad` (conflicting signals) ranked high-energy songs first regardless of mood. The system has no way to detect or resolve internally contradictory preferences.

---

## Intended Use
- Educational simulation to understand content-based recommendation logic
- Portfolio demonstration of Python data processing and scoring algorithms
- Learning tool for exploring algorithmic bias and filter bubbles

## Non-Intended Use
- Commercial music recommendation (dataset too small, not licensed)
- High-stakes personalization where accuracy directly affects users
- Any application requiring learning from real user behavior over time

---

## Ideas for Improvement

1. **Add collaborative filtering** — surface songs that taste-alike users enjoy, even outside the stated genre preference.
2. **Diversity penalty** — cap results to a max of 2 songs per genre or artist so the top-K never gets dominated by a single cluster.
3. **Expand and balance the dataset** — at least 10 songs per genre and equal mood distribution to reduce bias from catalog skew.
