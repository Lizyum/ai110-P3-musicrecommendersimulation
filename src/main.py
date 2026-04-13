"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs

DIVIDER = "=" * 65


def print_recommendations(label: str, user_prefs: dict, songs: list, weights: dict = None) -> None:
    """Print top-5 recommendations for a given user profile."""
    print(f"\n{DIVIDER}")
    print(f"  Profile: {label}")
    print(f"  genre={user_prefs['genre']} | mood={user_prefs['mood']} | "
          f"energy={user_prefs['energy']} | acoustic={user_prefs['likes_acoustic']}")
    print(DIVIDER)
    print(f"{'Rank':<5} {'Title':<25} {'Artist':<18} {'Score':>6}")
    print("-" * 65)

    recommendations = recommend_songs(user_prefs, songs, k=5, weights=weights)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank:<5} {song['title']:<25} {song['artist']:<18} {score:>6.1f}/100")
        print(f"      Why: {explanation}\n")

    print(DIVIDER)


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs from catalog.\n")

    # ---------------------------------------------------------------
    # STEP 1 — Three distinct core profiles
    # ---------------------------------------------------------------
    high_energy_pop = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.9,
        "likes_acoustic": False,
    }

    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "likes_acoustic": True,
    }

    deep_intense_rock = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.95,
        "likes_acoustic": False,
    }

    print_recommendations("High-Energy Pop", high_energy_pop, songs)
    print_recommendations("Chill Lofi", chill_lofi, songs)
    print_recommendations("Deep Intense Rock", deep_intense_rock, songs)

    # ---------------------------------------------------------------
    # STEP 1 (cont.) — Edge / adversarial profiles
    # ---------------------------------------------------------------

    # Conflicting: high energy + sad/moody mood — tests whether genre+energy
    # or mood wins when signals disagree
    conflicted_user = {
        "genre": "pop",
        "mood": "moody",
        "energy": 0.9,
        "likes_acoustic": True,   # acoustic preference also fights high energy
    }

    # Impossible match: genre that doesn't exist in dataset
    unknown_genre = {
        "genre": "classical",
        "mood": "relaxed",
        "energy": 0.2,
        "likes_acoustic": True,
    }

    print_recommendations("Conflicted User (high energy + moody pop + acoustic)", conflicted_user, songs)
    print_recommendations("Unknown Genre (classical — not in dataset)", unknown_genre, songs)

    # ---------------------------------------------------------------
    # STEP 3 — Weight-shift experiment
    # Double energy weight (20→40), halve genre weight (30→15).
    # New totals: genre(15)+mood(25)+energy(40)+valence(15)+acoustic(10) = 105
    # Scores are still comparable; only relative ranking matters here.
    # ---------------------------------------------------------------
    experimental_weights = {
        "genre": 15.0,
        "mood": 25.0,
        "energy": 40.0,
        "valence": 15.0,
        "acoustic": 10.0,
    }

    print("\n" + "~" * 65)
    print("  EXPERIMENT: Double energy weight | Halve genre weight")
    print("  (genre 30→15, energy 20→40, all other weights unchanged)")
    print("  Re-running 'High-Energy Pop' with experimental weights:")
    print("~" * 65)
    print_recommendations(
        "High-Energy Pop [EXPERIMENT]",
        high_energy_pop,
        songs,
        weights=experimental_weights,
    )


if __name__ == "__main__":
    main()
