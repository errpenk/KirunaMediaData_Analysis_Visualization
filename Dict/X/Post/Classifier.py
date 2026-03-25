# Classification 1 (directly related)  keep, label = 1
# Classification 2 (indirectly related) keep, label = 2
# Classification 0 (irrelevant) delete, label = 0


import re
import pandas as pd
from typing import Tuple

from keywords import (
    DIRECT_KEYWORDS,
    NORTHERN_SWEDEN_KEYWORDS,
    MINING_KEYWORDS,
    SAMI_KEYWORDS,
    RARE_EARTH_KEYWORDS,
    TOWN_RELOCATION_KEYWORDS,
    SPAM_SHORT_LINK_PATTERNS,
    SPAM_HASHTAG_THRESHOLD,
)



def _normalise(text) -> str:
    """Return lowercase stripped string; empty string if null."""
    if pd.isna(text):
        return ""
    return str(text).strip().lower()


def _contains_any(text_lower: str, keywords: list[str]) -> bool:
    return any(kw in text_lower for kw in keywords)


# noise / spam checks

def is_empty_or_noise(text) -> bool:
    """True if post carries no meaningful text."""
    raw = _normalise(text)
    if not raw:
        return True
    # emoji CDN URL only
    if re.match(r'^https://abs-0\.twimg\.com/emoji/', raw):
        return True
    # bare URL only
    if re.match(r'^https?://[^\s]+$', raw):
        return True
    # no letters / digits at all
    if not re.search(r'[a-zA-ZåäöÅÄÖ\u4e00-\u9fff0-9]', raw):
        return True
    return False


def is_spam(text) -> bool:
    """True if post looks like a promotional / bot post."""
    raw = str(text) if not pd.isna(text) else ""
    hashtag_count = len(re.findall(r'#\w+', raw))
    has_short_link = any(re.search(p, raw) for p in SPAM_SHORT_LINK_PATTERNS)
    return hashtag_count >= SPAM_HASHTAG_THRESHOLD and has_short_link


# classifier

def classify(text) -> Tuple[int, str]:
    """
    Returns
    (label, reason)
        label  : 1 = directly related, 2 = indirectly related, 0 = irrelevant
        reason : short human-readable explanation
    """
    # prefilter
    if is_empty_or_noise(text):
        return (0, "empty/noise")
    if is_spam(text):
        return (0, "spam/advertisement")

    t = _normalise(text)

    # Classification 1: direct mention of Kiruna
    if _contains_any(t, DIRECT_KEYWORDS):
        return (1, "directly related – Kiruna mentioned")

    # Classification 2: indirect / background topics
    if _contains_any(t, NORTHERN_SWEDEN_KEYWORDS):
        return (2, "indirectly related – northern Sweden")
    if _contains_any(t, MINING_KEYWORDS):
        return (2, "indirectly related – mining/LKAB")
    if _contains_any(t, SAMI_KEYWORDS):
        return (2, "indirectly related – Sámi culture")
    if _contains_any(t, RARE_EARTH_KEYWORDS):
        return (2, "indirectly related – rare earth/critical minerals")
    if _contains_any(t, TOWN_RELOCATION_KEYWORDS):
        return (2, "indirectly related – town relocation")

    # Classification 0: irrelevant
    return (0, "irrelevant – no matching keywords")
