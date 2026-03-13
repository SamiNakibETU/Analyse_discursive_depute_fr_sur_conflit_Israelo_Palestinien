from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Tuple

import requests
from rapidfuzz import fuzz

from ..paths import ProjectPaths
from ..utils.normalization import build_variants, simplify_name

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class NormalizationRules:
    titles: Tuple[str, ...]
    suffixes: Tuple[str, ...]


@dataclass(frozen=True)
class OratorProfile:
    canonical_name: str
    group_code: Optional[str]
    group_label: Optional[str]
    legislature: Optional[int]
    source: str
    metadata: Dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class OratorMatch:
    profile: OratorProfile
    matched_variant: str
    score: float


class OratorRegistry:
    def __init__(self, rules: NormalizationRules, score_cutoff: float = 82.0) -> None:
        self.rules = rules
        self.score_cutoff = score_cutoff
        self._exact: Dict[str, List[Tuple[str, OratorProfile]]] = {}
        self._fuzzy_entries: List[Tuple[str, OratorProfile]] = []

    @classmethod
    def from_project(cls, paths: ProjectPaths, config_filename: str = "orators_sources.json") -> "OratorRegistry":
        config_path = paths.config_dir / config_filename
        config = json.loads(config_path.read_text(encoding="utf-8"))
        normalization_cfg = config.get("normalization", {})
        rules = NormalizationRules(
            titles=tuple(normalization_cfg.get("strip_titles", [])),
            suffixes=tuple(normalization_cfg.get("remove_suffixes", [])),
        )
        registry = cls(rules=rules)
        for source in config.get("sources", []):
            try:
                registry._load_source(paths, source)
            except Exception as exc:
                logger.exception("Failed to load orator source %s: %s", source.get("name"), exc)
        logger.info("Loaded %s orator variants (exact keys: %s)", len(registry._fuzzy_entries), len(registry._exact))
        return registry

    def match(self, speaker_name: str, *, legislature: Optional[int] = None) -> Optional[OratorMatch]:
        key = simplify_name(speaker_name, titles=self.rules.titles, suffixes=self.rules.suffixes)
        if not key:
            return None
        exact_candidates = self._exact.get(key)
        if exact_candidates:
            profile = self._pick_candidate(exact_candidates, legislature)
            return OratorMatch(profile=profile[1], matched_variant=profile[0], score=100.0)

        best_score = 0.0
        best_profile: Optional[OratorProfile] = None
        best_variant = ""
        for variant_key, profile in self._fuzzy_entries:
            score = fuzz.WRatio(key, variant_key)
            if legislature and profile.legislature and profile.legislature != legislature:
                score -= 5
            if score > best_score:
                best_score = score
                best_profile = profile
                best_variant = variant_key
        if best_profile and best_score >= self.score_cutoff:
            return OratorMatch(profile=best_profile, matched_variant=best_variant, score=best_score)
        return None

    def _pick_candidate(self, candidates: List[Tuple[str, OratorProfile]], legislature: Optional[int]) -> Tuple[str, OratorProfile]:
        if legislature is not None:
            for variant, profile in candidates:
                if profile.legislature == legislature:
                    return variant, profile
        return candidates[0]

    def _normalize_variants(self, variants: Iterable[str]) -> List[str]:
        normalized: List[str] = []
        for variant in variants:
            key = simplify_name(variant, titles=self.rules.titles, suffixes=self.rules.suffixes)
            if key and key not in normalized:
                normalized.append(key)
        return normalized

    def _register_profile(self, profile: OratorProfile, variants: Iterable[str]) -> None:
        normalized_variants = self._normalize_variants(variants)
        for variant_key in normalized_variants:
            self._exact.setdefault(variant_key, []).append((variant_key, profile))
            self._fuzzy_entries.append((variant_key, profile))

    def _load_source(self, paths: ProjectPaths, source: Dict[str, object]) -> None:
        source_type = source.get("type")
        name = source.get("name", "unknown")
        legislature = source.get("legislature")
        if source_type == "local_json":
            path_str = source.get("path")
            if not path_str:
                raise ValueError("Missing path for local_json source")
            raw_path = Path(path_str)
            if not raw_path.is_absolute():
                absolute = (paths.config_dir / raw_path).resolve()
            else:
                absolute = raw_path
            data = json.loads(absolute.read_text(encoding="utf-8"))
            self._ingest_local_dataset(name, data, legislature)
        elif source_type == "remote_json":
            url = source.get("url")
            if not url:
                raise ValueError("Missing url for remote_json source")
            payload = self._download_remote(url)
            self._ingest_remote_dataset(name, payload, legislature)
        else:
            raise ValueError(f"Unsupported source type '{source_type}' for {name}")

    def _ingest_local_dataset(self, source_name: str, data: Dict[str, object], legislature: Optional[int]) -> None:
        if source_name == "external_speakers":
            entries = data.get("entries", [])
            for entry in entries:
                label = entry.get("label")
                patterns = entry.get("patterns", [])
                group_code = entry.get("groupe")
                group_long = entry.get("groupe_long")
                profile = OratorProfile(
                    canonical_name=label,
                    group_code=group_code,
                    group_label=group_long,
                    legislature=legislature,
                    source=source_name,
                    metadata={"type": "external"},
                )
                self._register_profile(profile, patterns or [label])
            return

        deputes = data.get("deputes") or []
        for deputy in deputes:
            canonical_name = deputy.get("nom_complet") or deputy.get("nom")
            if not canonical_name:
                continue
            firstname = deputy.get("prenom", "")
            lastname = deputy.get("nom", "")
            variants = deputy.get("variantes_nom", []) + [canonical_name]
            variants.extend(build_variants(firstname, lastname, titles=self.rules.titles))
            profile = OratorProfile(
                canonical_name=canonical_name,
                group_code=deputy.get("groupe_actuel"),
                group_label=deputy.get("groupe_long"),
                legislature=legislature,
                source=source_name,
                metadata={
                    "id": deputy.get("id"),
                    "sexe": deputy.get("sexe"),
                    "circo": deputy.get("circo"),
                    "departement": deputy.get("departement"),
                    "photo": deputy.get("photo_url"),
                },
            )
            self._register_profile(profile, variants)

    def _ingest_remote_dataset(self, source_name: str, payload: Dict[str, object], legislature: Optional[int]) -> None:
        deputes = payload.get("deputes") or []
        for wrapper in deputes:
            deputy = wrapper.get("depute") if isinstance(wrapper, dict) else wrapper
            if not deputy:
                continue
            canonical_name = deputy.get("nom")
            firstname = deputy.get("prenom", "")
            lastname = deputy.get("nom_de_famille", "") or deputy.get("nom", "")
            if not canonical_name:
                continue
            # Filter by mandate start when possible
            start = deputy.get("mandat_debut")
            if legislature == 16 and start and not start.startswith("2022"):
                continue
            variants = [canonical_name]
            variants.extend(build_variants(firstname, lastname, titles=self.rules.titles))
            group_code = deputy.get("groupe_sigle")
            group_label = deputy.get("parti_ratt_financier") or group_code
            profile = OratorProfile(
                canonical_name=canonical_name,
                group_code=group_code,
                group_label=group_label,
                legislature=legislature,
                source=source_name,
                metadata={
                    "id_an": deputy.get("id_an"),
                    "slug": deputy.get("slug"),
                    "mandat_debut": deputy.get("mandat_debut"),
                    "mandat_fin": deputy.get("mandat_fin"),
                },
            )
            self._register_profile(profile, variants)

    def _download_remote(self, url: str) -> Dict[str, object]:
        logger.info("Downloading remote orator dataset %s", url)
        response = requests.get(url, timeout=40)
        response.raise_for_status()
        return response.json()

