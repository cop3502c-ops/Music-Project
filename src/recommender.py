from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    # TODO: Implement CSV loading logic
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, str]:
    """
    Scores a single song against user preferences and returns a score and explanation.
    Required by src/main.py
    """
    score = 0.0
    reasons = []

    # Genre match: +2.0 points
    if song["genre"] == user_prefs.get("favorite_genre"):
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match: +1.0 points
    if song["mood"] == user_prefs.get("favorite_mood"):
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy proximity: (1.0 - |song_energy - target_energy|) x 1.5
    energy_score = round((1.0 - abs(song["energy"] - user_prefs.get("target_energy", 0.5))) * 1.5, 2)
    score += energy_score
    reasons.append(f"energy proximity (+{energy_score})")

    # Valence proximity: (1.0 - |song_valence - target_valence|) x 1.0
    valence_score = round((1.0 - abs(song["valence"] - user_prefs.get("target_valence", 0.5))) * 1.0, 2)
    score += valence_score
    reasons.append(f"valence proximity (+{valence_score})")

    # Danceability proximity: (1.0 - |song_danceability - target_danceability|) x 1.0
    dance_score = round((1.0 - abs(song["danceability"] - user_prefs.get("target_danceability", 0.5))) * 1.0, 2)
    score += dance_score
    reasons.append(f"danceability proximity (+{dance_score})")

    return round(score, 2), ", ".join(reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # TODO: Implement scoring and ranking logic
    # Expected return format: (song_dict, score, explanation)
    # scored is a list of tuples: (song, score, explanation)
    scored = [(song, *score_song(user_prefs, song)) for song in songs]

    # sorted() is used here instead of .sort() because it returns a new list
    # without modifying the original songs list, which is safer and more Pythonic
    scored = sorted(scored, key=lambda x: x[1], reverse=True)

    # Diversity penalty: prevent too many songs from the same artist or genre
    # in the top results. If an artist or genre is already in the results,
    # apply a 0.5 point penalty to the score of the next song from that artist/genre.
    seen_artists = {}
    seen_genres = {}
    results = []

    for song, score, explanation in scored:
        artist = song["artist"]
        genre = song["genre"]
        penalty = 0.0
        penalty_notes = []

        if seen_artists.get(artist, 0) >= 1:
            penalty += 0.5
            penalty_notes.append("artist repeat (-0.5)")
        if seen_genres.get(genre, 0) >= 2:
            penalty += 0.5
            penalty_notes.append("genre repeat (-0.5)")

        if penalty > 0:
            score = round(score - penalty, 2)
            explanation += ", " + ", ".join(penalty_notes)

        seen_artists[artist] = seen_artists.get(artist, 0) + 1
        seen_genres[genre] = seen_genres.get(genre, 0) + 1
        results.append((song, score, explanation))

    return sorted(results, key=lambda x: x[1], reverse=True)[:k]