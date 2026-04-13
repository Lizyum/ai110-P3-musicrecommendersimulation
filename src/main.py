"""
Command line runner for the Music Recommender Simulation.

Run with:
    python -m src.main
"""

from src.recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    user_prefs = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "likes_acoustic": False,
    }

    print(f"\nUser profile: genre={user_prefs['genre']} | mood={user_prefs['mood']} | energy={user_prefs['energy']}\n")
    print("=" * 55)

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print(f"{'Rank':<5} {'Title':<25} {'Artist':<18} {'Score'}")
    print("-" * 55)
    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"{rank:<5} {song['title']:<25} {song['artist']:<18} {score:.1f}/100")
        print(f"      Why: {explanation}\n")

    print("=" * 55)


if __name__ == "__main__":
    main()
