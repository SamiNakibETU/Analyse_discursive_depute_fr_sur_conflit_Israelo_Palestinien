from __future__ import annotations

import logging
import re
from datetime import date
from typing import Iterable, List
from urllib.parse import urljoin

from bs4 import BeautifulSoup

from ..config import LegislatureConfig, ScrapingConfig
from ..http import HttpClient
from ..models import SessionIndexEntry
from ..utils.normalization import strip_accents, normalize_whitespace

logger = logging.getLogger(__name__)

_MONTHS = {
    "janvier": 1,
    "fevrier": 2,
    "fevrier": 2,
    "mars": 3,
    "avril": 4,
    "mai": 5,
    "juin": 6,
    "juillet": 7,
    "aout": 8,
    "aout": 8,
    "septembre": 9,
    "octobre": 10,
    "novembre": 11,
    "decembre": 12,
    "decembre": 12,
}

_SESSION_NUMBER_RE = re.compile(r"(\d+)")


def _parse_french_date(value: str) -> date:
    normalized = strip_accents(value).lower()
    normalized = normalized.replace("1er", "1")
    tokens = normalize_whitespace(normalized).split()
    if len(tokens) < 4:
        raise ValueError(f"Unexpected date format: {value}")
    day_token = re.sub(r"[^0-9]", "", tokens[1])
    day = int(day_token)
    month_name = tokens[2]
    month = _MONTHS.get(month_name)
    if not month:
        raise ValueError(f"Unknown month '{month_name}' in '{value}'")
    year = int(tokens[3])
    return date(year, month, day)


def _extract_session_number(container) -> str | None:
    span = container.select_one("div.flex1 span")
    if not span:
        return None
    match = _SESSION_NUMBER_RE.search(span.get_text())
    return match.group(1) if match else None


class SessionIndexer:
    def __init__(self, http: HttpClient, config: ScrapingConfig) -> None:
        self.http = http
        self.config = config

    def iter_sessions(self) -> Iterable[SessionIndexEntry]:
        for legislature in self.config.legislatures:
            yield from self._iterate_legislature(legislature)

    def _iterate_legislature(self, legislature: LegislatureConfig) -> Iterable[SessionIndexEntry]:
        page = 1
        while True:
            page_url = f"{legislature.base_url}?page={page}"
            logger.debug("Fetching listing page %s", page_url)
            response = self.http.get(page_url, referer=legislature.base_url)
            html = response.text
            entries = self._parse_listing(html, legislature)
            if not entries:
                logger.debug("No sessions found on page %s", page_url)
                break
            kept_any = False
            older_only = True
            for entry in entries:
                if entry.sitting_date < self.config.start_date:
                    continue
                older_only = False
                kept_any = True
                yield entry
            if older_only:
                logger.debug(
                    "Stopping pagination for legislature %s at page %s (entries older than start date)",
                    legislature.id,
                    page,
                )
                break
            if not kept_any:
                logger.debug("All sessions on page %s before start date, peeking next page", page_url)
            page += 1

    def _parse_listing(self, html: str, legislature: LegislatureConfig) -> List[SessionIndexEntry]:
        soup = BeautifulSoup(html, "html.parser")
        results: List[SessionIndexEntry] = []
        for day_node in soup.select("ul.crs-index-days > li"):
            heading = day_node.select_one("h2")
            if not heading:
                continue
            date_text = heading.get_text(strip=True)
            try:
                sitting_date = _parse_french_date(date_text)
            except ValueError as exc:
                logger.warning("Unable to parse date '%s': %s", date_text, exc)
                continue

            for grid_item in day_node.select("div.ha-grid-item"):
                block = grid_item.select_one("div.an-bloc")
                if not block:
                    continue
                data_id = (block.get("data-id") or "").strip()
                session_parts = data_id.split()
                if not session_parts:
                    continue
                session_id = session_parts[0]
                if not session_id.startswith("CRSAN"):
                    continue
                link = grid_item.select_one("a.link.h5")
                if not link:
                    continue
                relative_url = link.get("href")
                if not relative_url:
                    continue
                html_url = urljoin(legislature.base_url, relative_url)
                title = normalize_whitespace(link.get_text())
                label = f"{date_text} - {title}" if title else date_text
                session_number = _extract_session_number(grid_item)
                xml_url = f"https://www.assemblee-nationale.fr/dyn/opendata/{session_id}.xml"
                results.append(
                    SessionIndexEntry(
                        session_id=session_id,
                        legislature=legislature.id,
                        sitting_date=sitting_date,
                        sitting_label=label,
                        session_number=session_number,
                        html_url=html_url,
                        xml_url=xml_url,
                    )
                )
        return results



