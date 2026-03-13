from __future__ import annotations

import logging
from dataclasses import asdict
from datetime import datetime
from typing import Dict, List

from .config import ProjectConfig
from .keywords import KeywordConfig, KeywordMatcher
from .logging_utils import configure_logging
from .models import EnrichedIntervention, InterventionRecord, SessionIndexEntry
from .paths import ProjectPaths
from .scraping.pipeline import ScrapingPipeline
from .storage import writers
from .enrichment.registry import OratorRegistry
from .enrichment.pipeline import EnrichmentPipeline

logger = logging.getLogger(__name__)


class FinalDataPipeline:
    """High-level orchestrator covering scraping (step 1) and enrichment (step 2)."""

    def __init__(self) -> None:
        self.paths = ProjectPaths.discover()
        self.project_config = ProjectConfig.load(self.paths)
        keyword_config = KeywordConfig.load(self.project_config.scraping.keywords_path)
        self.keyword_matcher = KeywordMatcher(keyword_config)
        self.scraping_pipeline = ScrapingPipeline(self.project_config, self.keyword_matcher)
        self.registry = OratorRegistry.from_project(self.paths)
        self.enrichment_pipeline = EnrichmentPipeline(self.registry)

    def run(self) -> Dict[str, object]:
        configure_logging()
        logger.info("Starting FINAL pipeline")
        sessions, interventions = self.scraping_pipeline.run()
        self._persist_step1(sessions, interventions)
        enriched = self.enrichment_pipeline.enrich(interventions)
        self._persist_step2(enriched)
        metadata = self._build_metadata(sessions, interventions, enriched)
        writers.write_json(self.project_config.storage.metadata, metadata)
        logger.info(
            "Pipeline finished: %s sessions considered, %s interventions retained, %s enriched",
            len(sessions),
            len(interventions),
            len(enriched),
        )
        return metadata

    def _persist_step1(self, sessions: List[SessionIndexEntry], interventions: List[InterventionRecord]) -> None:
        session_records = [self._serialize_session(entry) for entry in sessions]
        intervention_records = [self._serialize_intervention(record) for record in interventions]
        writers.write_jsonl(self.project_config.storage.raw_sessions, session_records)
        writers.write_jsonl(self.project_config.storage.relevant_interventions, intervention_records)

    def _persist_step2(self, enriched: List[EnrichedIntervention]) -> None:
        enriched_records = [self._serialize_enriched(record) for record in enriched]
        writers.write_jsonl(self.project_config.storage.enriched_interventions, enriched_records)

    def _build_metadata(
        self,
        sessions: List[SessionIndexEntry],
        interventions: List[InterventionRecord],
        enriched: List[EnrichedIntervention],
    ) -> Dict[str, object]:
        latest_date = max((s.sitting_date for s in sessions), default=None)
        return {
            "generated_at": datetime.utcnow().isoformat() + "Z",
            "sessions_count": len(sessions),
            "interventions_count": len(interventions),
            "enriched_count": len(enriched),
            "latest_session_date": latest_date.isoformat() if latest_date else None,
            "source_config": {
                "start_date": self.project_config.scraping.start_date.isoformat(),
                "legislatures": [leg.id for leg in self.project_config.scraping.legislatures],
                "min_text_length": self.project_config.scraping.min_text_length,
            },
        }

    def _serialize_session(self, entry: SessionIndexEntry) -> Dict[str, object]:
        return {
            "session_id": entry.session_id,
            "legislature": entry.legislature,
            "sitting_date": entry.sitting_date.isoformat(),
            "sitting_label": entry.sitting_label,
            "session_number": entry.session_number,
            "html_url": entry.html_url,
            "xml_url": entry.xml_url,
        }

    def _serialize_intervention(self, record: InterventionRecord) -> Dict[str, object]:
        payload = asdict(record)
        payload["sitting_date"] = record.sitting_date.isoformat()
        return payload

    def _serialize_enriched(self, record: EnrichedIntervention) -> Dict[str, object]:
        payload = asdict(record)
        payload["sitting_date"] = record.sitting_date.isoformat()
        return payload

