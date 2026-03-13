from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, List, Set

from .utils.text import prepare_for_matching


@dataclass
class KeywordConfig:
    categories: Dict[str, List[str]]
    phrases: List[str]

    @classmethod
    def load(cls, path: Path) -> "KeywordConfig":
        data = json.loads(path.read_text(encoding="utf-8"))
        categories = data.get("keywords", {})
        phrases = data.get("phrases", [])
        return cls(categories=categories, phrases=phrases)

    @property
    def flattened(self) -> List[str]:
        seen: Set[str] = set()
        ordered: List[str] = []
        for values in self.categories.values():
            for value in values:
                key = value.strip().lower()
                if key and key not in seen:
                    seen.add(key)
                    ordered.append(key)
        return ordered


class KeywordMatcher:
    def __init__(self, config: KeywordConfig) -> None:
        self.config = config
        self._word_patterns: Dict[str, re.Pattern[str]] = {}
        self._phrase_terms: Set[str] = set()
        for term in config.flattened:
            normalized = prepare_for_matching(term)
            if " " in normalized:
                self._phrase_terms.add(normalized)
            else:
                self._word_patterns[normalized] = re.compile(rf"\b{re.escape(normalized)}\b")
        for phrase in config.phrases:
            normalized = prepare_for_matching(phrase)
            if normalized:
                self._phrase_terms.add(normalized)

    def find_matches(self, text: str) -> List[str]:
        normalized = prepare_for_matching(text)
        if not normalized:
            return []
        hits: Set[str] = set()
        for term, pattern in self._word_patterns.items():
            if pattern.search(normalized):
                hits.add(term)
        for term in self._phrase_terms:
            if term in normalized:
                hits.add(term)
        return sorted(hits)

    def has_match(self, text: str) -> bool:
        return bool(self.find_matches(text))

