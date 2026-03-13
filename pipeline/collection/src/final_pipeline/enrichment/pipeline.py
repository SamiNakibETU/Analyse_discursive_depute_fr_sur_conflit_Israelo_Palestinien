from __future__ import annotations

from dataclasses import asdict
from typing import Iterable, List

from ..models import EnrichedIntervention, InterventionRecord
from .registry import OratorMatch, OratorRegistry


class EnrichmentPipeline:
    def __init__(self, registry: OratorRegistry) -> None:
        self.registry = registry

    def enrich(self, interventions: Iterable[InterventionRecord]) -> List[EnrichedIntervention]:
        enriched_records: List[EnrichedIntervention] = []
        for record in interventions:
            match = self.registry.match(record.speaker_name, legislature=record.legislature)
            data = asdict(record)
            enriched = EnrichedIntervention(**data)
            if match:
                self._apply_match(enriched, match)
            enriched_records.append(enriched)
        return enriched_records

    def _apply_match(self, record: EnrichedIntervention, match: OratorMatch) -> None:
        profile = match.profile
        record.match_score = match.score
        record.matched_name = profile.canonical_name
        record.matched_legislature = profile.legislature
        record.matched_group = profile.group_code
        record.matched_group_long = profile.group_label
        record.matched_role = profile.metadata.get("type")
        record.matched_source = profile.source
        record.matched_metadata = profile.metadata

