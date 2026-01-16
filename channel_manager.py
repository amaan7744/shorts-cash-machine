import json
from pathlib import Path

CHANNELS_FILE = Path("channels.txt")
STATE_FILE = Path("state.json")

def get_next_channel() -> str:
    channels = [
        line.strip()
        for line in CHANNELS_FILE.read_text().splitlines()
        if line.strip()
    ]

    state = json.loads(STATE_FILE.read_text())
    index = state.get("index", 0)

    channel = channels[index % len(channels)]

    # update state
    state["index"] = (index + 1) % len(channels)
    STATE_FILE.write_text(json.dumps(state, indent=2))

    return channel
