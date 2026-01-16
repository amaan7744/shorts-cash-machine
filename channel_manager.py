import json
from pathlib import Path
from logger import logger

CHANNELS_FILE = Path("channels.txt")
STATE_FILE = Path("state.json")


def get_next_channel() -> str:
    # -----------------------------
    # Validate channels file
    # -----------------------------
    if not CHANNELS_FILE.exists():
        logger.error("channels.txt not found")
        raise SystemExit(1)

    channels = [
        line.strip()
        for line in CHANNELS_FILE.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]

    if not channels:
        logger.error("channels.txt is empty")
        raise SystemExit(1)

    # -----------------------------
    # Load or initialize state
    # -----------------------------
    if not STATE_FILE.exists():
        logger.warning("state.json missing — creating default state")
        STATE_FILE.write_text(json.dumps({"index": 0}, indent=2))

    try:
        state = json.loads(STATE_FILE.read_text(encoding="utf-8"))
    except Exception:
        logger.warning("state.json corrupted — resetting")
        state = {"index": 0}

    index = state.get("index", 0)

    # -----------------------------
    # Select channel
    # -----------------------------
    channel = channels[index % len(channels)]
    logger.info(f"Channel index {index} → {channel}")

    # -----------------------------
    # Update and persist state
    # -----------------------------
    state["index"] = (index + 1) % len(channels)
    STATE_FILE.write_text(json.dumps(state, indent=2))

    return channel
