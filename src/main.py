"""
Command line runner for the Music Recommender Simulation.

Tests the recommender with multiple user profiles to see how it
handles different tastes and preferences.
"""

import os
from recommender import load_songs, recommend_songs

# figure out the project root so the csv path works from anywhere
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, "..")


def print_recommendations(profile_name: str, user_prefs: dict, songs: list):
    """Prints formatted recommendations for a single user profile."""
    print(f"\n{'='*55}")
    print(f"  Profile: {profile_name}")
    print(f"  Prefs: {user_prefs}")
    print(f"{'='*55}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, rec in enumerate(recommendations, 1):
        song, score, explanation = rec
        print(f"\n  {i}. {song['title']} by {song['artist']}")
        print(f"     Score: {score:.2f}")
        print(f"     Because: {explanation}")

    print()


def main() -> None:
    csv_path = os.path.join(PROJECT_ROOT, "data", "songs.csv")
    songs = load_songs(csv_path)

    # Profile 1: Happy pop listener - wants upbeat, danceable pop
    pop_happy = {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "valence": 0.85,
        "danceability": 0.85,
    }

    # Profile 2: Chill lofi studier - low energy, acoustic, focused vibes
    chill_lofi = {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.35,
        "valence": 0.58,
        "danceability": 0.55,
    }

    # Profile 3: Intense rock fan - high energy, intense, not acoustic
    intense_rock = {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "valence": 0.45,
        "danceability": 0.7,
    }

    # Profile 4 (edge case): conflicting prefs - high energy but sad/chill mood
    conflicting = {
        "genre": "pop",
        "mood": "chill",
        "energy": 0.95,
        "valence": 0.3,
        "danceability": 0.4,
    }

    print_recommendations("Happy Pop Fan", pop_happy, songs)
    print_recommendations("Chill Lofi Studier", chill_lofi, songs)
    print_recommendations("Intense Rock Listener", intense_rock, songs)
    print_recommendations("Edge Case: High Energy + Chill Mood", conflicting, songs)


if __name__ == "__main__":
    main()
