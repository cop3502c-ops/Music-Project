"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    # Starter example profile
    profiles = [
        {
            "name": "Happy Pop Fan",
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.80,
            "target_valence": 0.80,
            "target_danceability": 0.80,
            "likes_acoustic": False
        },
        {
            "name": "Chill Lofi Listener",
            "favorite_genre": "lofi",
            "favorite_mood": "chill",
            "target_energy": 0.35,
            "target_valence": 0.55,
            "target_danceability": 0.55,
            "likes_acoustic": True
        },
        {
            "name": "High-Energy EDM Fan",
            "favorite_genre": "edm",
            "favorite_mood": "euphoric",
            "target_energy": 0.95,
            "target_valence": 0.90,
            "target_danceability": 0.95,
            "likes_acoustic": False
        },
    ]

    for user_prefs in profiles:
        print(f"\n{'=' * 50}")
        print(f"Profile: {user_prefs['name']}")
        print(f"{'=' * 50}")
        recommendations = recommend_songs(user_prefs, songs, k=5)
        for i, rec in enumerate(recommendations, 1):
            # You decide the structure of each returned item.
            # A common pattern is: (song, score, explanation)
            song, score, explanation = rec
            print(f"{i}. {song['title']} by {song['artist']}")
            print(f"   Score:   {score:.2f}")
            print(f"   Reasons: {explanation}")
            print("-" * 50)


if __name__ == "__main__":
    main()