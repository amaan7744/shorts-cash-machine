from youtube_transcript_api import get_transcript
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

# Ensure lexicon is available
nltk.download("vader_lexicon", quiet=True)


def extract_best_segment(video_id, min_len=20, max_len=40):
    transcript = get_transcript(video_id)

    analyzer = SentimentIntensityAnalyzer()

    scored = []
    for entry in transcript:
        score = analyzer.polarity_scores(entry["text"])["compound"]
        scored.append({
            "start": entry["start"],
            "text": entry["text"],
            "score": abs(score),
        })

    # Pick highest emotional moment
    peak = max(scored, key=lambda x: x["score"])

    start = max(0, peak["start"] - 5)
    duration = min(max_len, max(min_len, 30))

    return start, start + duration

