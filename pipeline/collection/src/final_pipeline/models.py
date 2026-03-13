from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, date
from typing import Dict, List, Optional


@dataclass
class SessionIndexEntry:
    """Metadata collected from the listing pages before XML parsing."""

    session_id: str
    legislature: int
    sitting_date: date
    sitting_label: str
    session_number: Optional[str]
    html_url: str
    xml_url: str


@dataclass
class InterventionRecord:
    """Single speech or reaction extracted from the XML payload."""

    session_id: str
    legislature: int
    session_number: Optional[str]
    sitting_date: date
    sitting_label: str
    order_index: int
    code_style: Optional[str]
    speaker_name: str
    speaker_quality: Optional[str]
    speaker_uid: Optional[str]
    speaker_mandate_id: Optional[str]
    raw_text: str
    normalized_text: str
    keyword_hits: List[str] = field(default_factory=list)
    extra: Dict[str, str] = field(default_factory=dict)
    source_html: str = ""
    source_xml: str = ""


@dataclass
class EnrichedIntervention(InterventionRecord):
    """Intervention enriched with structured information about the orator."""

    match_score: Optional[float] = None
    matched_name: Optional[str] = None
    matched_legislature: Optional[int] = None
    matched_group: Optional[str] = None
    matched_group_long: Optional[str] = None
    matched_role: Optional[str] = None
    matched_source: Optional[str] = None
    matched_metadata: Dict[str, str] = field(default_factory=dict)

