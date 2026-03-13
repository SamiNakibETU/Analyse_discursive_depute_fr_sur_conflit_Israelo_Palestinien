from __future__ import annotations

import re
from typing import Iterable

from .normalization import strip_accents, normalize_whitespace

_PUNCT_RE = re.compile(r"[^a-z0-9\s']")


def prepare_for_matching(text: str) -> str:
    if not text:
        return ""
    lowered = strip_accents(text).lower()
    lowered = lowered.replace("œ", "oe")
    lowered = _PUNCT_RE.sub(" ", lowered)
    lowered = normalize_whitespace(lowered)
    return lowered


def collapse_whitespace(text: str) -> str:
    return normalize_whitespace(text)


def truncate(text: str, limit: int = 280) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 1] + "…"


def iter_unique(values: Iterable[str]) -> Iterable[str]:
    seen = set()
    for value in values:
        if value not in seen:
            seen.add(value)
            yield value

