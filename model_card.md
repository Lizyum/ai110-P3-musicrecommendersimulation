# Model Card: Music Recommender Simulation

## 1. Model Name

**VibeFinder 1.0**

---

## 2. Intended Use

VibeFinder is a rule-based music recommender designed to suggest songs from a small catalog based on a user's stated listening preferences. It is built for classroom exploration of how recommendation systems work, not for production deployment.

- It generates a ranked list of up to 5 song recommendations from a 20-song catalog.
- It assumes users can describe their preferences using four simple values: preferred genre, mood, desired energy level (0–1), and whether they like acoustic-sounding music.

---

## 3. How the Model Works

The recommender reads a list of songs, then assigns each song a numeric score based on how closely it matches what the user says they like. The song with the highest score is recommended first.

The score is built from five ingredients:

1. **Genre match** — the biggest reward (+30 points). If a song's genre matches the user's favorite, it gets a large bonus.
2. **Mood match** — the second-largest reward (+25 points). If the song's mood label matches the user's preferred mood, another bonus is added.
3. **Energy closeness** — up to +20 points. Songs closer in energy level to the user's target score higher. A user who wants high-energy music (0.9) will penalize quiet songs.
4. **Valence closeness** — up to +15 points. Each mood has an expected "happiness level" (valence). Songs whose valence matches that expectation score higher.
5. **Acoustic preference** — up to +10 points. If the user likes acoustic music, songs with high acousticness score higher; if they don't, low-acousticness songs score higher.

The maximum possible score is 100. A song that matches everything perfectly earns all 100 points.

---

## 4. Data

The catalog contains **20 songs** across 7 genres: pop, lofi, rock, ambient, jazz, synthwave, and indie pop. Moods include happy, chill, intense, focused, moody, and relaxed.

- Pop, lofi, rock, ambient, and jazz each have 3 songs; synthwave and indie pop have 2 each.
- Several real-world music categories are entirely absent: country, hip-hop, R&B, classical, metal, and electronic dance music (EDM) do not appear.
- With only 20 songs, users whose preferred genre is underrepresented (e.g., synthwave) will quickly exhaust all matching options.

---

## 5. Strengths

- The system works well for users whose preferences align clearly with one genre and mood. A "Chill Lofi" fan asking for lofi + chill will reliably surface the three lofi songs at the top of the list.
- The valence proxy (inferring emotional tone from mood label) provides an extra signal that helps distinguish between two songs in the same genre when one actually sounds more emotionally fitting.
- The scoring is fully transparent — every point awarded comes with a human-readable reason, making it easy to understand why a song ranked first.

---

## 6. Limitations and Bias

**Genre dominance causes a filter bubble.** Because genre match is worth 30 out of 100 points — the single largest weight — users will almost always see songs from their preferred genre at the top, even if those songs otherwise don't fit their mood or energy. A happy pop fan and a sad pop fan might receive very similar lists simply because pop songs all collect the same 30-point genre bonus.

**Pop songs are slightly overrepresented.** Three of the seven genres contain 3 songs each (pop, lofi, rock, ambient, jazz), but "pop-adjacent" genres like indie pop add two more upbeat, mid-to-high-energy songs. A user who prefers genres outside the catalog — such as classical or hip-hop — receives zero genre points for every song, so their recommendations are driven entirely by energy and mood, which may feel arbitrary.

**Conflicting preferences are not handled.** If a user requests high energy (0.9) but a moody mood, the system does not recognize the tension — it simply awards energy points to high-energy songs and mood points to moody songs independently. The winner is whichever song partially satisfies the most categories, which can feel like a random mix rather than a thoughtful recommendation.

**Mood valence mapping is fixed and coarse.** The implied valence per mood (e.g., "happy" → 0.88, "moody" → 0.43) was hand-tuned and is the same for everyone. A user who describes themselves as "happy" but listens to bittersweet songs will be steered away from valence values that might actually suit them.

**No listening history.** The system has no memory. It cannot learn that you skipped the first recommendation and loved the fifth, so it cannot improve over time.

---

## 7. Evaluation

Five user profiles were tested:

| Profile | Genre | Mood | Energy | Acoustic |
|---|---|---|---|---|
| High-Energy Pop | pop | happy | 0.9 | No |
| Chill Lofi | lofi | chill | 0.35 | Yes |
| Deep Intense Rock | rock | intense | 0.95 | No |
| Conflicted User | pop | moody | 0.9 | Yes |
| Unknown Genre | classical | relaxed | 0.2 | Yes |

**Observations:**

- For **High-Energy Pop**, "Bounce Theory" (pop, happy, energy=0.86) ranked first consistently — a result that matches intuition. The genre and mood double-bonus made it almost impossible for any non-pop song to compete.
- For **Chill Lofi**, "Library Rain" scored highest because its energy (0.35) was a perfect match for the target. The three lofi songs dominated the top 3.
- For **Deep Intense Rock**, "Iron Circuit" (rock, intense, energy=0.95) took the top spot. This felt correct — it is the heaviest-sounding song in the catalog.
- The **Conflicted User** (pop + moody + high energy + acoustic) surfaced surprising results. "Night Drive Loop" (synthwave, moody) appeared near the top despite not being pop, because mood match and acoustic preference pulled it up while the genre mismatch only cost 30 points.
- The **Unknown Genre** profile (classical — not in dataset) received zero genre points for all songs. The top result was driven almost entirely by energy proximity and acoustic preference, surfacing ambient songs — which is not unreasonable for a classical fan, but was not an intentional design decision.

**Weight-shift experiment:** Doubling the energy weight (20→40) and halving the genre weight (30→15) caused the High-Energy Pop ranking to shift. Songs with energy above 0.85 rose regardless of genre, and some non-pop songs leapfrogged pop songs that had slightly lower energy. This confirmed that the genre weight is the primary driver of current recommendations — reducing it immediately produces more energetically diverse results.

---

## 8. Future Work

- **Expand the dataset** to at least 100 songs across more genres (hip-hop, R&B, country, EDM) to reduce filter bubbles and give users with niche tastes real options.
- **Add a diversity penalty** so the same artist or genre cannot occupy all 5 slots — currently, a lofi fan's entire top-5 could be all lofi songs.
- **Detect conflicting preferences** and surface a warning or ask a clarifying question instead of producing a confusing mix.
- **Allow users to rate recommendations** so the system can adjust weights over time rather than using the same fixed values for everyone.
- **Expose weights as user-tunable parameters** so a user who cares more about energy than genre can say so explicitly.

---

## 9. Personal Reflection

Building this recommender made clear how much influence small design decisions have on what users actually see. Choosing genre as the top-weighted feature felt natural at first — of course people want songs in their genre — but testing with the Conflicted User and Unknown Genre profiles revealed that this choice locks users into a narrow slice of the catalog. The most surprising discovery was that the "Unknown Genre" profile (classical) still received reasonable recommendations through energy and acousticness alone, even though none of the songs were classical; the system accidentally found its way to a plausible answer through a different path than intended. This makes me think about how real streaming apps must constantly balance between "give users what they asked for" and "show them things they didn't know they'd like."
