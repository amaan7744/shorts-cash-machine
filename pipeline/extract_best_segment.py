from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk

nltk.download("vader_lexicon", quiet=True)


def extract_best_segment(video_id, min_len=20, max_len=40):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
    except (TranscriptsDisabled, NoTranscriptFound):
        # Signal caller to skip this video
        return None

    analyzer = SentimentIntensityAnalyzer()

    scored = []
    for entry in transcript:
        score = analyzer.polarity_scores(entry["text"])["compound"]
        scored.append({
            "start": entry["start"],
            "score": abs(score),
        })

    if not scored:
        return None

    peak = max(scored, key=lambda x: x["score"])

    start = max(0, peak["start"] - 5)
    duration = min(max_len, max(min_len, 30))

    return start, start + duration
