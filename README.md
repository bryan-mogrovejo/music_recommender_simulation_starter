# Music Recommender Simulation

## Project Summary

This project is a content-based music recommender that I built to understand how platforms like Spotify figure out what songs to suggest. It takes a user's taste profile (favorite genre, mood, energy level, etc.) and scores every song in a small CSV catalog against those preferences. The highest-scoring songs become the recommendations, and for each one the system explains *why* it was picked.

I focused on content-based filtering, meaning the system only looks at song attributes and user preferences — it doesn't know what other people are listening to. It's a simplified version of what real apps do, but building it helped me understand the tradeoffs involved.

---

## How The System Works

Real streaming platforms like Spotify use a combination of collaborative filtering (what do users similar to you listen to?) and content-based filtering (what attributes does this song have that match your taste?). My version only does content-based filtering since we don't have multiple users — but even that simple approach produces surprisingly reasonable results.

### Song Features
Each song in `data/songs.csv` has these attributes:
- **genre** — the category (pop, lofi, rock, etc.)
- **mood** — the general feeling (happy, chill, intense, focused, relaxed, moody)
- **energy** — how high-energy the song is (0.0 to 1.0)
- **valence** — musical positivity (0.0 = sad, 1.0 = cheerful)
- **danceability** — how easy it is to dance to (0.0 to 1.0)
- **acousticness** — how acoustic the track sounds (0.0 to 1.0)
- **tempo_bpm** — beats per minute

### User Profile
The `UserProfile` stores:
- `favorite_genre` — the genre the user prefers
- `favorite_mood` — their preferred mood
- `target_energy` — their ideal energy level
- `likes_acoustic` — whether they prefer acoustic sounds

For the functional (dict-based) approach in `main.py`, the user can also specify target `valence` and `danceability`.

### Scoring Algorithm ("Algorithm Recipe")
For each song, the system calculates a score:
1. **+2.0 points** for a genre match
2. **+1.0 point** for a mood match
3. **Up to +1.5 points** for energy closeness (calculated as `(1.0 - |song_energy - target_energy|) * 1.5`)
4. **Up to +0.5 points** for valence closeness
5. **Up to +0.5 points** for danceability closeness

The songs are then sorted by score (highest first), and the top K are returned as recommendations.

I weighted genre the highest because in my experience, if someone asks for rock and gets jazz, it doesn't matter how perfect the energy level is — it just feels wrong. Mood is second because it captures the vibe. The numerical features are bonuses that help differentiate between songs in the same genre/mood.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   cd src
   python3 main.py
   ```

### Running Tests

```bash
pytest
```

---

## Experiments I Tried

### Experiment 1: Doubled energy weight, halved genre weight
I changed genre from +2.0 to +1.0 and energy from 1.5x to 3.0x to see what happens.

**Result:** The recommendations became less intuitive. For the "Happy Pop Fan" profile, the system started recommending rock and EDM songs that happened to have similar energy levels, which doesn't really feel like a good recommendation for someone who wants pop. Genre matters more than I initially thought.

### Experiment 2: Removed mood check entirely
I commented out the mood scoring to see how rankings shifted.

**Result:** Without mood, the system couldn't distinguish between "intense rock" and "happy rock" scenarios. The "Intense Rock Listener" started getting some happier-sounding songs mixed in. It showed me that mood acts as a useful secondary filter after genre.

### Experiment 3: Edge case — conflicting preferences
I created a user profile with high energy (0.95) but a chill mood. The system leaned toward pop songs with high energy since genre + energy outweighed the mood match. This makes sense given the weights, but it reveals that the system can't really handle contradictory preferences gracefully.

---

## Limitations and Risks

- **Tiny catalog** — With only 18 songs, the recommendations are limited. A real system needs thousands or millions of tracks.
- **No collaborative filtering** — We never consider what other users with similar taste enjoy, which is a huge part of how Spotify works.
- **Genre dominance** — The +2.0 genre weight means genre almost always wins. A lofi fan will mostly see lofi songs regardless of other preferences.
- **No understanding of lyrics or language** — The system has no idea what a song is about or what language it's in.
- **Static preferences** — Real people's taste changes based on time of day, activity, and mood. This system assumes taste is fixed.

---

## Reflection

Building this recommender taught me that even a simple scoring system can produce results that feel like real recommendations. When I ran the Happy Pop profile and saw "Sunrise City" at the top, it genuinely seemed like a reasonable suggestion. That was kind of surprising, I expected it to feel more random.

At the same time, I noticed how easy it is for bias to creep in. Since I expanded the dataset myself, the genres I'm familiar with got more representation. If this were a real product, that kind of imbalance would mean certain users consistently get worse recommendations. Real platforms face this same problem at a much larger scale, and now I understand why "filter bubbles" are such a big topic in AI ethics.

Using AI tools helped me think through the scoring math and generate CSV data faster. But I had to double-check the suggestions, for example, the AI initially suggested equal weights for all features, which would have made genre matches feel weak. I adjusted the weights based on my own intuition about what makes a recommendation feel right.

---

