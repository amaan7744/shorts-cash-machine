import random

# Deterministic-ish hooks (safe for reuse)
HOOK_TEMPLATES = [
    "This was supposed to be easy.",
    "Nobody expected this to happen.",
    "Everything went wrong in seconds.",
    "This changed the entire video.",
    "He immediately knew something was wrong.",
    "What happened next shocked everyone.",
]

def generate_hook_script() -> str:
    """
    Returns a short hook line for TTS.
    No context dependency. No randomness explosion.
    """
    return random.choice(HOOK_TEMPLATES)
