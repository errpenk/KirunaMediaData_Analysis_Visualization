# Core Classification

import re
import pandas as pd
from typing import Tuple, List

from config import (
    KIRUNA_DIRECT,
    INDIRECT_KEYWORDS,
    EXCLUSION_PATTERNS,
    CORE_CATEGORIES,
)


# Text Preprocessing

def preprocess_text(*fields) -> str:
    """
    Merge multiple text fields (title + body), convert them all to lowercase, and remove extra spaces
    Any NaN/None fields will be skipped
    """
    parts = []
    for f in fields:
        if not pd.isna(f):
            parts.append(str(f).strip())
    return ' '.join(parts).lower()


# Classifier

def check_exclusions(text: str) -> bool:
    """Exclusion Detection: 
      Hitting any pattern: Classified as 0-Irrelevant"""
    for pattern in EXCLUSION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def check_direct_kiruna(text: str) -> bool:
    """directly Kiruna"""
    for pattern in KIRUNA_DIRECT:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


def check_indirect_keywords(text: str) -> Tuple[bool, List[str]]:
    """
    Indirectly related keyword detection
    Returns (whether indirectly related, list of hit categories)
    """
    matched = []
    for category, patterns in INDIRECT_KEYWORDS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                matched.append(category)
                break   # Each category is recorded only once
    return len(matched) >= 1, matched


# Confidence calculation

def compute_confidence(matched_cats: List[str]) -> float:
    """
    Confidence score is calculated based on the overlap between the number of hit categories and the core categories.
    """
    core_hits = len(set(matched_cats) & CORE_CATEGORIES)
    other_hits = len(matched_cats) - core_hits
    score = 0.60 + 0.10 * core_hits + 0.03 * other_hits
    return round(min(score, 0.95), 2)


# Main classification function

def classify_post(title, body=None) -> Tuple[int, str, float]:
    """
    Categorize individual posts into three levels.

    title: Post title (can be NaN)
    body: Post body (can be None / NaN)

    Returns: (category_code, reason, confidence)
    - 1 Directly relevant → Keep (Core data)
    - 2 Indirectly relevant → Keep (Background data)
    - 0 Irrelevant → Delete
    """
    # Empty title
    if pd.isna(title):
        return 0, 'Empty title', 0.95

    # Merge title and body text
    combined = preprocess_text(title, body) if body is not None else preprocess_text(title)

    # Prioritize exclusion
    if check_exclusions(combined):
        return 0, 'Exclusion pattern matched', 0.90

    # Directly Kiruna
    if check_direct_kiruna(combined):
        return 1, 'Kiruna mentioned directly', 0.95

    # Indirectly related
    is_indirect, matched_cats = check_indirect_keywords(combined)
    if is_indirect:
        confidence = compute_confidence(matched_cats)
        reason = f"Indirectly related: {', '.join(sorted(matched_cats))}"
        return 2, reason, confidence

    # Unrelated
    return 0, 'No matching keywords', 0.85
