from __future__ import annotations

import re
import unicodedata
from typing import Iterable, List, Optional


_WHITESPACE_RE = re.compile(r"\s+")
_PARENTHESES_RE = re.compile(r"\s*\([^)]*\)")


def strip_accents(value: str) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value)
    return "".join(ch for ch in normalized if not unicodedata.combining(ch))


def normalize_whitespace(value: str) -> str:
    return _WHITESPACE_RE.sub(" ", value or "").strip()


def remove_parenthetical(value: str) -> str:
    return _PARENTHESES_RE.sub("", value or "")


def strip_titles(value: str, titles: Iterable[str]) -> str:
    if not value:
        return ""
    lowered = value.lower().strip()
    for title in titles:
        title_clean = title.lower()
        if lowered.startswith(title_clean + " "):
            remainder = value[len(title):].lstrip()
            return remainder
    return value


def simplify_name(value: str, *, titles: Optional[Iterable[str]] = None, suffixes: Optional[Iterable[str]] = None) -> str:
    """Build a canonical ASCII-friendly key for matching."""

    if not value:
        return ""
    cleaned = value.strip()
    cleaned = remove_parenthetical(cleaned)
    if titles:
        cleaned = strip_titles(cleaned, titles)
    if suffixes:
        lower = cleaned.lower()
        for suffix in suffixes:
            suffix = suffix.lower()
            if lower.endswith(suffix):
                cleaned = cleaned[: -len(suffix)].rstrip()
                break
    cleaned = strip_accents(cleaned)
    cleaned = normalize_whitespace(cleaned)
    cleaned = re.sub(r"[^a-zA-Z\s'-]", "", cleaned)
    cleaned = normalize_whitespace(cleaned)
    return cleaned.lower()


def build_variants(firstname: str, lastname: str, *, titles: Optional[Iterable[str]] = None) -> List[str]:
    variants = []
    firstname = firstname.strip()
    lastname = lastname.strip()
    base = f"{firstname} {lastname}".strip()
    if base:
        variants.append(base)
    if lastname:
        variants.append(lastname)
    if firstname and lastname:
        variants.append(f"{lastname} {firstname}")
    if firstname:
        variants.append(firstname)
    if titles:
        for title in titles:
            if base:
                variants.append(f"{title} {base}")
            if lastname:
                variants.append(f"{title} {lastname}")
    normalized_variants = []
    for variant in variants:
        simple = simplify_name(variant, titles=titles)
        if simple and simple not in normalized_variants:
            normalized_variants.append(simple)
    return normalized_variants

