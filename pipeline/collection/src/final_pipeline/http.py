from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Dict, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


@dataclass
class HttpClientConfig:
    timeout: int
    retries: int
    backoff_factor: float
    headers: Dict[str, str]
    referer: Optional[str] = None


class HttpClient:
    def __init__(self, config: HttpClientConfig) -> None:
        self.config = config
        self.session = requests.Session()
        retry = Retry(
            total=config.retries,
            connect=config.retries,
            read=config.retries,
            backoff_factor=config.backoff_factor,
            status_forcelist=(429, 500, 502, 503, 504),
            allowed_methods=("GET", "HEAD"),
            raise_on_status=False,
            respect_retry_after_header=True,
        )
        adapter = HTTPAdapter(max_retries=retry)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)
        self.session.headers.update(config.headers)

    def get(self, url: str, *, referer: Optional[str] = None, stream: bool = False) -> requests.Response:
        headers = {}
        ref = referer or self.config.referer
        if ref:
            headers["Referer"] = ref
        response = self.session.get(url, timeout=self.config.timeout, headers=headers, stream=stream)
        if response.status_code >= 400:
            logger.warning("GET %s returned status %s", url, response.status_code)
        response.raise_for_status()
        return response

