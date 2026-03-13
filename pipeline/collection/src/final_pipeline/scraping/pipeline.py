from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Iterable, List, Tuple

import requests
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from ..config import ProjectConfig
from ..http import HttpClient
from ..keywords import KeywordMatcher
from ..models import InterventionRecord, SessionIndexEntry
from .page_indexer import SessionIndexer
from .xml_parser import XmlParser

logger = logging.getLogger(__name__)


class ScrapingPipeline:
    def __init__(self, project_config: ProjectConfig, keyword_matcher: KeywordMatcher) -> None:
        self.project_config = project_config
        self.http_client = HttpClient(project_config.scraping.http)
        self.indexer = SessionIndexer(self.http_client, project_config.scraping)
        self.parser = XmlParser(keyword_matcher, project_config.scraping.min_text_length)

    def run(self) -> Tuple[List[SessionIndexEntry], List[InterventionRecord]]:
        sessions: List[SessionIndexEntry] = []
        interventions: List[InterventionRecord] = []
        for session in self.indexer.iter_sessions():
            sessions.append(session)
            try:
                xml_bytes = self._download_xml(session)
            except requests.HTTPError as exc:
                logger.error("Failed to download XML for %s: %s", session.session_id, exc)
                continue
            except requests.RequestException as exc:
                logger.error("Network error for %s: %s", session.session_id, exc)
                continue
            parsed = self.parser.parse(xml_bytes, session)
            if parsed:
                interventions.extend(parsed)
        return sessions, interventions

    @retry(
        retry=retry_if_exception_type(requests.RequestException),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    def _download_xml(self, session: SessionIndexEntry) -> bytes:
        logger.debug("Downloading XML %s", session.xml_url)
        response = self.http_client.get(session.xml_url, referer=session.html_url)
        return response.content

