import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """Represents a song and its attributes."""
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
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """OOP implementation of the recommendation logic."""
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Scores all songs against user profile and returns top k."""
        scored = []
        for song in self.songs:
            score = 0.0

            # genre match is the biggest factor
            if song.genre == user.favorite_genre:
                score += 2.0

            # mood match matters but less than genre
            if song.mood == user.favorite_mood:
                score += 1.0

            # energy closeness - the closer the better, max 1.5 points
            energy_diff = abs(song.energy - user.target_energy)
            score += (1.0 - energy_diff) * 1.5

            # acoustic preference bonus
            if user.likes_acoustic and song.acousticness > 0.6:
                score += 0.5
            elif not user.likes_acoustic and song.acousticness < 0.4:
                score += 0.3

            scored.append((song, score))

        # sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        reasons = []

        if song.genre == user.favorite_genre:
            reasons.append(f"genre match ({song.genre})")
        if song.mood == user.favorite_mood:
            reasons.append(f"mood match ({song.mood})")

        energy_diff = abs(song.energy - user.target_energy)
        if energy_diff < 0.15:
            reasons.append(f"energy is very close to your target ({song.energy:.2f} vs {user.target_energy:.2f})")
        elif energy_diff < 0.3:
            reasons.append(f"energy is somewhat close ({song.energy:.2f} vs {user.target_energy:.2f})")

        if user.likes_acoustic and song.acousticness > 0.6:
            reasons.append("acoustic sound you like")

        if not reasons:
            reasons.append("general fit based on combined features")

        return "Recommended because: " + ", ".join(reasons)


def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file and returns a list of dictionaries."""
    songs = []
    with open(csv_path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # convert numeric fields so we can do math later
            row['id'] = int(row['id'])
            row['energy'] = float(row['energy'])
            row['tempo_bpm'] = float(row['tempo_bpm'])
            row['valence'] = float(row['valence'])
            row['danceability'] = float(row['danceability'])
            row['acousticness'] = float(row['acousticness'])
            songs.append(row)
    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a single song against user preferences and explains why."""
    score = 0.0
    reasons = []

    # genre match = +2.0
    if song['genre'] == user_prefs.get('genre'):
        score += 2.0
        reasons.append(f"genre match: {song['genre']} (+2.0)")

    # mood match = +1.0
    if song['mood'] == user_prefs.get('mood'):
        score += 1.0
        reasons.append(f"mood match: {song['mood']} (+1.0)")

    # energy closeness - reward songs close to target, max 1.5 pts
    if 'energy' in user_prefs:
        energy_diff = abs(song['energy'] - user_prefs['energy'])
        energy_score = (1.0 - energy_diff) * 1.5
        score += energy_score
        reasons.append(f"energy closeness (+{energy_score:.2f})")

    # valence closeness bonus - max 0.5 pts
    if 'valence' in user_prefs:
        val_diff = abs(song['valence'] - user_prefs['valence'])
        val_score = (1.0 - val_diff) * 0.5
        score += val_score
        reasons.append(f"valence closeness (+{val_score:.2f})")

    # danceability closeness bonus - max 0.5 pts
    if 'danceability' in user_prefs:
        dance_diff = abs(song['danceability'] - user_prefs['danceability'])
        dance_score = (1.0 - dance_diff) * 0.5
        score += dance_score
        reasons.append(f"danceability closeness (+{dance_score:.2f})")

    return (score, reasons)


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Ranks all songs by score and returns the top k with explanations."""
    scored_songs = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = ", ".join(reasons)
        scored_songs.append((song, score, explanation))

    # sort highest score first
    scored_songs.sort(key=lambda x: x[1], reverse=True)
    return scored_songs[:k]
