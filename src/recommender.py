import csv
from typing import List, Dict, Tuple
from dataclasses import dataclass

# Implied valence targets per mood, used for numeric proximity scoring
MOOD_VALENCE = {
    "happy": 0.88,
    "chill": 0.63,
    "intense": 0.54,
    "focused": 0.60,
    "moody": 0.43,
    "relaxed": 0.70,
}


@dataclass
class Song:
    """Represents a song and its audio attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's listening preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dicts with typed values."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id": int(row["id"]),
                "title": row["title"],
                "artist": row["artist"],
                "genre": row["genre"],
                "mood": row["mood"],
                "energy": float(row["energy"]),
                "tempo_bpm": float(row["tempo_bpm"]),
                "valence": float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs


DEFAULT_WEIGHTS = {
    "genre": 30.0,
    "mood": 25.0,
    "energy": 20.0,
    "valence": 15.0,
    "acoustic": 10.0,
}


def score_song(user_prefs: Dict, song: Dict, weights: Dict = None) -> Tuple[float, List[str]]:
    """Score a single song against user preferences; returns (score, reasons).

    Pass a custom ``weights`` dict to run experiments without touching DEFAULT_WEIGHTS.
    Keys: 'genre', 'mood', 'energy', 'valence', 'acoustic'.
    """
    w = weights if weights is not None else DEFAULT_WEIGHTS
    score = 0.0
    reasons = []

    # Genre match
    genre_pts = w["genre"]
    if song["genre"] == user_prefs.get("genre", ""):
        score += genre_pts
        reasons.append(f"genre match (+{genre_pts:.0f})")

    # Mood match
    mood_pts = w["mood"]
    if song["mood"] == user_prefs.get("mood", ""):
        score += mood_pts
        reasons.append(f"mood match (+{mood_pts:.0f})")

    # Energy proximity: up to w["energy"] pts
    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = w["energy"] * (1 - abs(song["energy"] - target_energy))
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.1f})")

    # Valence proximity: up to w["valence"] pts (derived from mood)
    implied_valence = MOOD_VALENCE.get(user_prefs.get("mood", ""), 0.65)
    valence_pts = w["valence"] * (1 - abs(song["valence"] - implied_valence))
    score += valence_pts
    reasons.append(f"valence proximity (+{valence_pts:.1f})")

    # Acousticness match: up to w["acoustic"] pts
    if user_prefs.get("likes_acoustic", False):
        acoustic_pts = w["acoustic"] * song["acousticness"]
    else:
        acoustic_pts = w["acoustic"] * (1 - song["acousticness"])
    score += acoustic_pts
    reasons.append(f"acousticness fit (+{acoustic_pts:.1f})")

    return round(score, 2), reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5, weights: Dict = None) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score descending, and return the top k results."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song, weights=weights)
        explanation = ", ".join(reasons)
        scored.append((song, score, explanation))

    # sorted() returns a new list and leaves the original unchanged; .sort() mutates in place
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)
    return ranked[:k]


class Recommender:
    """OOP wrapper around the scoring logic for use in tests."""

    def __init__(self, songs: List[Song]):
        """Initialize with a list of Song dataclass instances."""
        self.songs = songs

    def _song_to_dict(self, song: Song) -> Dict:
        """Convert a Song dataclass to a plain dict for score_song."""
        return {
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "valence": song.valence,
            "acousticness": song.acousticness,
        }

    def _user_to_dict(self, user: UserProfile) -> Dict:
        """Convert a UserProfile dataclass to a plain dict for score_song."""
        return {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
            "likes_acoustic": user.likes_acoustic,
        }

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k Song objects ranked by score for the given user."""
        user_dict = self._user_to_dict(user)
        scored = sorted(
            self.songs,
            key=lambda song: score_song(user_dict, self._song_to_dict(song))[0],
            reverse=True,
        )
        return scored[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why a song was recommended."""
        user_dict = self._user_to_dict(user)
        _, reasons = score_song(user_dict, self._song_to_dict(song))
        return ", ".join(reasons)
