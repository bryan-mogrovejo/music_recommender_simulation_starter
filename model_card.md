# Model Card: Music Recommender Simulation

## 1. Model Name

**FindMyVibe**

---

## 2. Intended Use

This recommender suggests 3-5 songs from a small catalog based on a user's preferred genre, mood, and target energy level. It is built for classroom exploration and learning about how recommendation systems work. It is not intended for real users or production use — the catalog is too small and the algorithm is too simple for that.
The system assumes the user knows what genre and mood they want ahead of time. It doesn't learn from listening history or adapt over time.

---

## 3. How the Model Works

The system looks at each song in the catalog and gives it a score based on how well it matches what the user asked for. Think of it like a judge giving points in a competition:

- If the song's genre matches the user's favorite genre, it gets 2 points. This is the biggest factor because in my experience, genre is the first thing people care about.
- If the song's mood matches (like "chill" or "intense"), it gets 1 point.
- The system also looks at how close the song's energy level is to what the user wants. A song with energy 0.82 and a target of 0.80 gets almost full points, but a song at 0.30 gets much less.
- Valence (how positive/cheerful the song sounds) and danceability also contribute smaller bonuses.

After every song is scored, the system sorts them from highest to lowest and picks the top results. For each recommendation, it also generates a plain-English explanation of why that song scored well.

---

## 4. Data

The dataset is a CSV file with 18 songs. I started with the 10 songs that came with the starter code, then added 8 more to cover genres and moods that were missing (EDM, R&B, folk, and more jazz/ambient tracks).

**Genres represented:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, edm, r&b, folk

**Moods represented:** happy, chill, intense, focused, relaxed, moody

The dataset is still pretty small and skews toward the genres I'm personally familiar with. There's no hip-hop, classical, Latin, or K-pop, which means users who prefer those genres would get poor recommendations.

---

## 5. Strengths

- **Works well for clear-cut profiles.** When someone asks for "chill lofi" the system reliably returns lofi songs with low energy. The top results feel right.
- **Explainable.** Every recommendation comes with a breakdown showing exactly which features contributed to the score and by how much. You can trace why any song appeared where it did.
- **Simple enough to reason about.** Because the scoring is just addition, it's easy to predict what will happen when you change weights or preferences. There's no black box here.
- **Handles the "pop/happy" archetype well.** With multiple pop songs in the catalog, the system can differentiate between them based on energy and mood.

---

## 6. Limitations and Bias

- **Genre dominance.** The +2.0 genre weight means genre almost always beats other features. A lofi song with perfect energy/mood for a rock fan still won't crack the top 3 because it's missing the 2-point genre bonus. This creates a "filter bubble" where users only see their favorite genre.
- **Small and unbalanced dataset.** Pop and lofi have more songs than other genres, so users who prefer pop get more variety while folk or R&B fans have limited options. This mirrors a real bias problem: if training data over-represents certain groups, those groups get better service.
- **No handling of contradictions.** When a user asks for high energy AND a chill mood, the system just adds up the points independently. It doesn't recognize that these preferences conflict or try to find a creative compromise.
- **Treats all users the same shape.** Everyone gets scored with the same formula. But real people have different patterns — some care deeply about tempo and don't care about mood; others are the opposite. One formula can't capture that.
- **No temporal awareness.** The system doesn't know if it's 6 AM or midnight, workout time or study time. Real recommenders factor in context.

---

## 7. Evaluation

I tested with four user profiles:

1. **Happy Pop Fan** (genre: pop, mood: happy, energy: 0.8) — Top results were "Sunrise City" and "Saturday Fever," both upbeat pop tracks. This matched my expectations perfectly.

2. **Chill Lofi Studier** (genre: lofi, mood: chill, energy: 0.35) — Got "Library Rain" and "Midnight Coding" at the top. These are exactly the kind of songs you'd put on while studying, so this felt accurate.

3. **Intense Rock Listener** (genre: rock, mood: intense, energy: 0.9) — "Neon Breakdown" and "Storm Runner" came up first. Both are high-energy rock tracks with intense mood. Makes sense.

4. **Edge Case: High Energy + Chill Mood** (genre: pop, mood: chill, energy: 0.95) — This was interesting. The system prioritized pop songs with high energy over chill songs with low energy. The genre + energy combo outweighed the mood match. This showed me that with conflicting preferences, the weightier features always win.

**Comparing profiles:** The EDM/rock profiles naturally gravitate toward high energy songs, while the acoustic/lofi profile shifts toward low energy tracks with higher acousticness. The happy pop profile picks songs with high valence and danceability. These differences make sense — they show the user preferences are actually testing for different things and the output reflects that.

I also ran experiments changing the weights (documented in README.md) which confirmed that genre is doing most of the heavy lifting in this system.

---

## 8. Future Work

- **Add diversity penalties.** Right now the top 5 could all be the same genre. A real recommender should mix in some variety so users can discover new music.
- **Support multiple users and collaborative filtering.** If I tracked what multiple users liked, I could recommend songs based on "users similar to you also enjoyed..."
- **Weight learning.** Instead of hand-picking weights, the system could learn optimal weights from user feedback (thumbs up/down on recommendations).
- **Add tempo and acousticness to scoring.** I have this data in the CSV but only used acousticness in the OOP version. Incorporating these into the scoring could help differentiate similar songs better.
- **Context-aware recommendations.** Time of day, activity type (workout vs study vs commute) could influence which features matter most.

---

## 9. Personal Reflection

The biggest thing I learned is that recommendation systems are fundamentally about turning subjective human taste into math. The formula itself is simple, just adding up points, but choosing which features to score and how much to weight them is where all the real decisions happen. Those choices encode assumptions about what matters, and they can inadvertently exclude entire groups of users.

I was genuinely surprised by how "smart" the results felt for such a basic algorithm. When the Chill Lofi profile got "Library Rain" as its top pick, I thought that's exactly what I'd want. But then I realized that's partly because I designed the dataset and the weights, of course it matches my intuition. A real system serving millions of diverse users would run into much harder edge cases.

Using AI tools was helpful for speeding up the implementation, especially for the CSV data expansion and the math behind the closeness formulas. But I had to push back on some suggestions. AI wanted to make things more complex than needed,like adding TF-IDF on genre names, and I had to decide what actually made sense for a simple simulation. That experience of using AI as a tool while still making your own judgment calls feels like an important skill going forward.

If I kept working on this, the first thing I'd add is a diversity mechanism so the system doesn't just return five songs from the same genre every time. In real life, the best recommendation playlists mix familiar comfort with new discovery, and that balance is hard to get right with pure scoring.
