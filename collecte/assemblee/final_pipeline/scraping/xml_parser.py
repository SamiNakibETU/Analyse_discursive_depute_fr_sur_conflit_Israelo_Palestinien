from __future__ import annotations

import logging
from datetime import datetime
from typing import Iterable, List, Optional

from lxml import etree

from ..keywords import KeywordMatcher
from ..models import InterventionRecord, SessionIndexEntry
from ..utils.text import collapse_whitespace, prepare_for_matching

logger = logging.getLogger(__name__)

NS = {"ns": "http://schemas.assemblee-nationale.fr/referentiel"}


class XmlParser:
    def __init__(self, keyword_matcher: KeywordMatcher, min_text_length: int) -> None:
        self.keyword_matcher = keyword_matcher
        self.min_text_length = min_text_length

    def parse(self, xml_content: bytes, session: SessionIndexEntry) -> List[InterventionRecord]:
        root = etree.fromstring(xml_content)
        interventions: List[InterventionRecord] = []

        legislature = session.legislature
        session_number = session.session_number or self._extract_text(root, "ns:metadonnees/ns:numSeance")
        sitting_label = self._extract_text(root, "ns:contenu/ns:quantiemes/ns:journee") or session.sitting_label
        # Confirm actual date from metadata if available
        date_value = self._extract_text(root, "ns:metadonnees/ns:dateSeance")
        if date_value:
            try:
                session_date = datetime.strptime(date_value[:8], "%Y%m%d").date()
            except ValueError:
                session_date = session.sitting_date
        else:
            session_date = session.sitting_date

        nodes = root.xpath(".//ns:paragraphe", namespaces=NS)
        for index, node in enumerate(nodes, start=1):
            text_node = node.find("ns:texte", namespaces=NS)
            if text_node is None:
                continue
            raw_text = collapse_whitespace("".join(text_node.itertext()))
            if len(raw_text) < self.min_text_length:
                continue
            normalized_text = prepare_for_matching(raw_text)
            if not normalized_text:
                continue
            keywords = self.keyword_matcher.find_matches(raw_text)
            if not keywords:
                continue
            speaker_name, speaker_quality = self._extract_speaker(node)
            record = InterventionRecord(
                session_id=session.session_id,
                legislature=legislature,
                session_number=session_number,
                sitting_date=session_date,
                sitting_label=sitting_label,
                order_index=index,
                code_style=node.get("code_style"),
                speaker_name=speaker_name,
                speaker_quality=speaker_quality,
                speaker_uid=node.get("id_acteur"),
                speaker_mandate_id=node.get("id_mandat"),
                raw_text=raw_text,
                normalized_text=normalized_text,
                keyword_hits=keywords,
                extra={
                    "ordre_absolu": node.get("ordre_absolu_seance", ""),
                    "code_grammaire": node.get("code_grammaire", ""),
                },
                source_html=session.html_url,
                source_xml=session.xml_url,
            )
            interventions.append(record)
        return interventions

    def _extract_text(self, root: etree._Element, xpath: str) -> Optional[str]:
        node = root.find(xpath, namespaces=NS)
        if node is not None and node.text:
            return collapse_whitespace(node.text)
        return None

    def _extract_speaker(self, node: etree._Element) -> tuple[str, Optional[str]]:
        orator = node.find("ns:orateurs/ns:orateur", namespaces=NS)
        if orator is None:
            return "", None
        name = collapse_whitespace("".join(orator.xpath("ns:nom/text()", namespaces=NS)))
        quality_list = orator.xpath("ns:qualite/text()", namespaces=NS)
        quality = collapse_whitespace(quality_list[0]) if quality_list else None
        return name, quality



