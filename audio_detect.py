from pydub import AudioSegment
import numpy as np
from logger import logger

def detect_spikes(video_path):
    try:
        audio = AudioSegment.from_file(video_path)
        samples = np.array(audio.get_array_of_samples())
        samples = np.abs(samples)

        window = 5000
        energies = [
            samples[i:i+window].mean()
            for i in range(0, len(samples), window)
        ]

        threshold = np.percentile(energies, 92)

        spikes = []
        for i, e in enumerate(energies):
            if e > threshold:
                start = i * 5
                end = start + 15
                spikes.append((start, end))

        logger.info(f"Detected {len(spikes)} spikes")
        return spikes
    except Exception as e:
        logger.error(f"Audio detection failed: {e}")
        return []
