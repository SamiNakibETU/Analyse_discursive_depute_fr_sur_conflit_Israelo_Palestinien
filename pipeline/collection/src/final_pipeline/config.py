from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import datetime, date
from pathlib import Path
from typing import Dict, List

from .http import HttpClientConfig
from .paths import ProjectPaths


@dataclass(frozen=True)
class LegislatureConfig:
    id: int
    base_url: str


@dataclass(frozen=True)
class ScrapingConfig:
    start_date: date
    min_text_length: int
    keywords_path: Path
    legislatures: List[LegislatureConfig]
    http: HttpClientConfig


@dataclass(frozen=True)
class StorageConfig:
    raw_sessions: Path
    raw_interventions: Path
    relevant_interventions: Path
    enriched_interventions: Path
    metadata: Path


@dataclass(frozen=True)
class ProjectConfig:
    scraping: ScrapingConfig
    storage: StorageConfig
    paths: ProjectPaths

    @classmethod
    def load(cls, paths: ProjectPaths) -> "ProjectConfig":
        config_path = paths.config_dir / "project_settings.json"
        data = json.loads(config_path.read_text(encoding="utf-8"))

        scraping_data = data["scraping"]
        http_data = scraping_data.get("http", {})

        legislatures = [
            LegislatureConfig(id=item["id"], base_url=item["base_url"])
            for item in scraping_data.get("legislatures", [])
        ]

        http_config = HttpClientConfig(
            timeout=http_data.get("timeout", 30),
            retries=http_data.get("retries", 3),
            backoff_factor=http_data.get("backoff_factor", 1.0),
            headers=http_data.get("headers", {}),
            referer=legislatures[0].base_url if legislatures else None,
        )

        scraping_config = ScrapingConfig(
            start_date=datetime.strptime(scraping_data.get("start_date", "2022-01-01"), "%Y-%m-%d").date(),
            min_text_length=scraping_data.get("min_text_length", 40),
            keywords_path=paths.config_dir / scraping_data.get("keywords_file", "keywords.json"),
            legislatures=legislatures,
            http=http_config,
        )

        storage_data = data.get("storage", {})
        storage_config = StorageConfig(
            raw_sessions=paths.root / storage_data.get("raw_sessions", "data/raw/sessions.jsonl"),
            raw_interventions=paths.root / storage_data.get("raw_interventions", "data/raw/interventions.jsonl"),
            relevant_interventions=paths.root / storage_data.get("relevant_interventions", "data/processed/interventions_relevant.jsonl"),
            enriched_interventions=paths.root / storage_data.get("enriched_interventions", "data/processed/interventions_enriched.jsonl"),
            metadata=paths.root / storage_data.get("metadata", "data/processed/run_metadata.json"),
        )

        return cls(scraping=scraping_config, storage=storage_config, paths=paths)

