from abc import abstractmethod
from extractors.base import BaseExtractor
from extractors.crawlers.checkpoint import load_checkpoint, save_checkpoint
from domain.canonical_job import CanonicalJob
from collections.abc import Iterator
from datetime import datetime, timezone
import httpx, time
from services.cdn_service import extract_arc_js, get_cdn_hash
from services.extract_service import get_xpath_first_element, remove_extra_spaces
from config.logging import logger


class BaseCrawler(BaseExtractor):
    request_delay_seconds: float = 1.0
    max_retries: int = 3
    user_agent: str = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
    headers: dict | None = None
    client: httpx.Client | None = None

    source_name: str | None = None

    def _fetch(
        self,
        url: str,
        method: str = "GET",
        headers: dict | None = None,
        params: dict | None = None,
        data: dict | None = None,
        files: list | None = None,
    ) -> str:
        last_error: Exception | None = None
        headers = headers or self.headers
        for attempt in range(self.max_retries):
            try:
                resp = self.client.request(
                    method, url, headers=headers, params=params, data=data, files=files
                )
                resp.raise_for_status()
                content = resp.text
                if "redirect__captcha" in content:
                    hash = extract_arc_js(content)
                    if not hash:
                        logger.error("hash error")
                        return None
                    # self.headers["cookie"] += f"__arcsjs={hash};"
                    # headers = {**headers, "cookie": f"__arcsjs={hash};"}
                    self.client.cookies.set("__arcsjs", hash)
                    headers = self.headers
                    resp = self.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        data=data,
                    )
                if "error-section__title" in content:
                    hash = get_cdn_hash(content)
                    if not hash:
                        logger.error("hash error")
                        return None
                    # self.headers["cookie"] += f"__arcsjs={hash};"
                    self.client.cookies.set("__arcsjs", hash)
                    # headers = {**headers, "cookie": f"__arcsjs={hash};"}
                    headers = self.headers
                    resp = self.request(
                        method=method,
                        url=url,
                        headers=headers,
                        params=params,
                        data=data,
                    )

                return resp.text
            except httpx._exceptions.RequestError as exc:
                last_error = exc
                time.sleep(self.request_delay_seconds * (attempt + 1))
        raise RuntimeError(
            f"Failed to fetch {url} after {self.max_retries} attempts"
        ) from last_error

    @abstractmethod
    def discover_urls(self, since: datetime | None = None) -> Iterator[str]:
        """Yield page URLs to crawl (from a sitemap, listing page, API, etc.)."""
        raise NotImplementedError

    @abstractmethod
    def parse(self, url: str, html: str) -> CanonicalJob:
        """Turn raw HTML for one page into a RawDocument."""
        raise NotImplementedError

    def iter_raw_documents(
        self, since: datetime | None = None
    ) -> Iterator[CanonicalJob]:
        checkpoint = load_checkpoint(self.source_name)
        seen_urls: set[str] = set(checkpoint.get("seen_urls", []))

        for url in self.discover_urls(since=since):
            if url in seen_urls:
                continue
            html = self._fetch(url)
            time.sleep(self.request_delay_seconds)
            yield self.parse(url, html)

            seen_urls.add(url)
            save_checkpoint(
                self.source_name,
                {
                    "seen_urls": list(seen_urls),
                    "last_run_at": datetime.now(timezone.utc).isoformat(),
                },
            )
