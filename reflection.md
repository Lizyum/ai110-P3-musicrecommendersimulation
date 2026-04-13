# Reflection: Comparing Recommender Outputs

This file compares the top-5 recommendations produced for each user profile and explains what changed between them — and why that makes sense given the scoring logic.

---

## High-Energy Pop vs. Chill Lofi

These two profiles are almost opposites: one wants loud, danceable pop; the other wants quiet, atmospheric lofi.

**High-Energy Pop** (`genre=pop, mood=happy, energy=0.9, acoustic=False`) surfaces songs like *Bounce Theory* and *Sunrise City* at the top. Both are pop songs tagged as happy and have energy values above 0.82. They collect the full 55-point genre + mood bonus, and their low acousticness fits the user's preference. The genre weight alone (30 points) acts like a magnet — non-pop songs can't realistically compete unless they score near-perfectly on every other dimension.

**Chill Lofi** (`genre=lofi, mood=chill, energy=0.35, acoustic=True`) shifts the entire list to quiet, textured songs. *Library Rain* (energy=0.35, acoustic=0.86) scores almost perfectly because it matches genre, mood, energy, and acoustic preference simultaneously. *Midnight Coding* follows closely. The key shift from High-Energy Pop: **high energy now hurts instead of helps**. Any song above 0.7 energy gets penalized on the energy-proximity term, so the Gym Hero–style tracks that ranked near the top for the pop fan fall toward the bottom.

**What this tells us:** Energy and acoustic preference are effective at separating these two extremes. The recommendations feel intuitive — the system isn't confused between these profiles.

---

## Chill Lofi vs. Deep Intense Rock

**Deep Intense Rock** (`genre=rock, mood=intense, energy=0.95, acoustic=False`) pulls in the heaviest songs in the catalog. *Iron Circuit* (rock, intense, energy=0.95) is a near-perfect match: genre, mood, and energy all align. *Storm Runner* (rock, intense, energy=0.91) follows close behind. What's notable is that non-rock songs with very high energy — like *Gym Hero* (pop, intense) — can also appear in the top 5. The mood bonus (+25) for "intense" is enough to pull them in even without the genre bonus.

Compared to **Chill Lofi**, the difference is stark: the lofi profile rewards restraint (low energy, high acousticness) while the rock profile rewards aggression (high energy, low acousticness). No song appears in both top-5 lists. This is the clearest demonstration that the scoring logic actually differentiates between user types.

**Key insight:** Mood is the second-strongest signal. A rock fan and a pop fan who both prefer "intense" will share some recommendations (high-energy intense songs) regardless of genre. This is arguably correct behavior — but it also reveals that mood can override genre in some cases.

---

## High-Energy Pop vs. Conflicted User

The **Conflicted User** profile (`genre=pop, mood=moody, energy=0.9, acoustic=True`) deliberately mixes signals that don't naturally go together: pop music is rarely moody, high energy usually conflicts with acoustic preference, and moody pop is barely represented in the dataset.

Compared to **High-Energy Pop**, the top result changes significantly. The pop + happy songs that dominated before — *Bounce Theory*, *Sunrise City* — lose their mood bonus (they're tagged "happy," not "moody"). The genre bonus still rewards them for being pop, but without the mood bonus they slip in ranking. Songs from other genres that happen to be moody — like *Night Drive Loop* (synthwave, moody) — can climb up because they earn the mood bonus even without the genre bonus.

The result is a mixed list that includes pop songs, synthwave songs, and possibly jazz, depending on energy and acousticness scores. **This feels like a system that is confused rather than helpful.** A real recommender might ask "did you mean energetic but melancholic?" and rethink the query. VibeFinder just adds up the points and moves on.

**Plain-language explanation:** Imagine you ask for "a spicy sweet cake." The baker gives you something that is 30% spicy and 70% sweet, or something in between — but never quite what you actually wanted. The recommender doesn't understand that these preferences conflict; it just gives partial credit to anything that satisfies at least one of them.

---

## Deep Intense Rock vs. Unknown Genre (Classical)

The **Unknown Genre** profile (`genre=classical, mood=relaxed, energy=0.2, acoustic=True`) has no matching songs in the dataset. Classical music does not exist in the catalog at all.

Because there are zero genre matches, the 30-point genre bonus is never awarded to any song. The entire ranking is determined by mood, energy, and acousticness. Songs tagged "relaxed" get the mood bonus; songs with very low energy (0.2 target) and high acousticness score well on the remaining dimensions. The result is a list of ambient and jazz songs — *Still Waters*, *Rainy Window*, *Coffee Shop Stories* — which are the quietest, most acoustic songs in the catalog.

Compared to **Deep Intense Rock**, the shift is total. Not a single song overlaps. The rock profile rewards loud, electric, fast songs; the classical profile (by accident) rewards quiet, acoustic, calm songs. The system found its way to a reasonable-sounding result — ambient music is not a terrible suggestion for someone who listens to classical — but it got there by default, not by design.

**What this teaches us about bias:** A user whose favorite genre is missing from the catalog is silently disadvantaged. They never get the 30-point genre bonus anyone else gets. If you imagine a real app with millions of users, this means fans of underrepresented genres consistently receive lower-confidence recommendations, and they may never know why.

---

## Weight-Shift Experiment: High-Energy Pop (Default vs. Experimental)

Running the High-Energy Pop profile with doubled energy weight (40 instead of 20) and halved genre weight (15 instead of 30) changed the rankings noticeably.

Under **default weights**, genre dominates. Three pop songs sit at the top because each earns 30 genre points that no other song can match.

Under **experimental weights**, energy dominates. Songs with energy above 0.85 — regardless of genre — compete more fairly. A synthwave song like *Neon Pulse* (energy=0.88) can challenge a pop song if it matches the energy target closely enough, because the energy gap now costs more points than a genre mismatch.

The recommendations became more energetically consistent but less genre-consistent. Whether that is "better" depends entirely on what the user actually cares about. 
