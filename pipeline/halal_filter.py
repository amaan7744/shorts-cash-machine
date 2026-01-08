BLOCK_KEYWORDS = [
    "nsfw", "sexy", "onlyfans", "twerk", "bikini", "lingerie",
    "boobs", "ass", "thong", "bra", "strip", "porn",
    "drunk", "weed", "alcohol", "vodka", "beer",
    "fight", "beating", "blood", "knife", "gun",
    "kissing", "making out"
]

BLOCK_SUBSTRINGS = [
    "gonewild", "nsfw", "hotgirls", "thirst", "model"
]

def is_halal(post: dict) -> bool:
    title = post["title"].lower()
    url = post["url"].lower()

    if post.get("over_18"):
        return False

    for k in BLOCK_KEYWORDS:
        if k in title or k in url:
            return False

    for s in BLOCK_SUBSTRINGS:
        if s in title or s in url:
            return False

    return True
