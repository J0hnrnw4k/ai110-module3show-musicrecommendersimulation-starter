# Reflection — Music Recommender Simulation

---

## Profile Comparisons

**High-Energy Pop Fan vs. Chill Lofi / Indie Listener**

These two profiles produced completely opposite results. The Pop Fan's top songs — Shake It Off, Levitating, Blinding Lights — all have energy above 0.75 and are tagged "happy." The Indie Listener's top songs — Sweater Weather, Heat Waves — sit below 0.6 energy and carry a "melancholic" mood. This makes total sense: genre and mood act as hard gates. No song cracks the top 2 spots without matching both categorical signals. The numerical scores (energy, danceability, acousticness) only act as tiebreakers among songs that already cleared that hurdle.

**Chill Lofi / Indie Listener vs. Deep Intense Rock Head**

The most interesting contrast is what happens when a genre is underrepresented. The Indie profile only has 3 indie songs in the catalog, so slots #3–#5 get filled by r&b and folk songs that happened to score well on numerical similarity (low energy, higher acousticness) — not because they are actually indie. The Rock Head benefits from 5 rock songs, so genre coherence holds throughout the full top-5. This shows that dataset size per genre directly affects recommendation quality even when the algorithm is identical.

**High-Energy Pop Fan vs. Deep Intense Rock Head**

Both profiles target high energy (0.80 vs. 0.85), so their lower-ranked results start to overlap in feel. High-energy hip-hop songs like DNA. by Kendrick Lamar creep into the Rock Head's list at slot #5 purely on energy similarity, once all 5 rock songs are exhausted. This reveals how the genre gate eventually breaks down at the edges of the top-K window when a genre has too few songs to fill every slot.

---

## Biggest Learning Moment

The most surprising thing was how much of the work the genre weight does on its own. Before running the tests, I expected energy and danceability to be the main differentiators. In practice, a 2.0-point genre bonus means the worst-possible genre-match song — one that scores zero on all numerical features — still earns 2.0 points. Meanwhile, the best-possible non-genre-match song maxes out all numerical features at 2.25 points. Genre is almost a prerequisite for the top spots, not just a preference. Changing that single weight has a massive downstream effect on every result — that is a design decision, not a law of nature.

## How AI Tools Helped (and Where I Had to Check)

AI tools helped generate the dataset quickly and verify that the scoring math always stays between 0 and 1. One place I had to double-check was the file path logic in `load_songs()`. An early suggestion used a hardcoded relative path like `"data/songs.csv"` directly in `open()`, which breaks when you run the script from a different directory. I replaced it with `os.path.dirname(os.path.abspath(__file__))` to build an absolute path from the file's location — which works no matter where VS Code's terminal is pointed.

## What Surprised Me About Simple Algorithms

Even with just five scoring signals and a single `sorted()` call, the output genuinely feels like a recommendation engine. The Pop Fan's list reads like a real Spotify pop playlist. That's humbling — it means a lot of what we perceive as "intelligent" recommendation is really just careful weighting of a few well-chosen features. The system isn't smart, it's just consistent. Real intelligence would mean knowing when to break its own rules — for example, surfacing an electronic song for a rock listener because the energy profile is nearly identical.

## What I Would Try Next

I would add a listening-history layer: after each session, the system slightly adjusts the user's target values toward the songs they engaged with longest (implicit feedback). Over time, the profile would drift toward actual preferences rather than stated ones — which is exactly how Spotify's taste profiles evolve week to week. I would also implement the diversity penalty from the model card: no more than 2 songs from the same genre or artist in the top-K, forcing the system to explore the catalog more broadly instead of locking into one lane.
