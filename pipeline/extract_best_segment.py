from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from nltk.sentiment import SentimentIntensityAnalyzer
import random
import nltk

nltk.download("vader_lexicon", quiet=True)


def extract_best_segment(video_id, min_len=20, max_len=40):
    """
    Returns (start, end) ALWAYS.
    Uses transcript if available, otherwise fallback to random clip.
    """

    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        analyzer = SentimentIntensityAnalyzer()
        scored = []

        for entry in transcript:
            score = analyzer.polarity_scores(entry["text"])["compound"]
            scored.append({
                "start": entry["start"],
                "score": abs(score),
            })

        if scored:
            peak = max(scored, key=lambda x: x["score"])
            start = max(0, peak["start"] - 5)
            duration = min(max_len, max(min_len, 30))
            return start, start + duration

    except (TranscriptsDisabled, NoTranscriptFound, Exception):
        pass

    # -----------------------------
    # FALLBACK: random clip
    # -----------------------------
    start = random.randint(10, 60)
    duration = random.randint(min_len, max_len)

    return start, start + duration
