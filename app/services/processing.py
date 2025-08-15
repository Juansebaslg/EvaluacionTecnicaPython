import re
from datetime import datetime, timezone
from typing import List, Tuple

def mask_banned_words(text: str, banned: List[str]) -> tuple[str, bool]:
    if not banned:
        return text, False
    pattern = re.compile(r"\b(" + "|".join(map(re.escape, banned)) + r")\b", flags=re.IGNORECASE)
    found = bool(pattern.search(text))
    masked = pattern.sub(lambda m: "*" * len(m.group(0)), text)
    return masked, found

def compute_metadata(text: str) -> tuple[int, int, datetime]:
    # word_count counts tokens separated by whitespace
    words = [w for w in re.split(r"\s+", text.strip()) if w]
    word_count = len(words)
    character_count = len(text)
    processed_at = datetime.now(timezone.utc)
    return word_count, character_count, processed_at
