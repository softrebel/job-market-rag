import httpx
from .base import BaseCrawler
from config.settings import settings
from pathlib import Path
from domain.canonical_job import CanonicalJob
from collections.abc import Iterator
from datetime import datetime
import pickle
from config.logging import logger
import lxml
import random
import time
from services.extract_service import get_xpath_first_element, remove_extra_spaces
from lxml.html import Element
from lxml.etree import tostring


class JobinjaCrawler(BaseCrawler):
    LOGIN_PAGE_URL: str = "https://jobinja.ir/login/user?redirect_url=https%3A%2F%2Fjobinja.ir%2Fjobs%3Ffilters%255Bjob_categories%255D%2"
    LOGIN_URL: str = "https://jobinja.ir/login/user"
    HOME_PAGE_URL: str = "https://jobinja.ir/jobs/category/it-software-web-development-jobs/%D8%A7%D8%B3%D8%AA%D8%AE%D8%AF%D8%A7%D9%85-%D9%88%D8%A8-%D8%A8%D8%B1%D9%86%D8%A7%D9%85%D9%87-%D9%86%D9%88%DB%8C%D8%B3-%D9%86%D8%B1%D9%85-%D8%A7%D9%81%D8%B2%D8%A7%D8%B1"

    source_name = "jobinja_crawler"

    def __init__(
        self,
        username: str,
        password: str,
        data_path: Path,
        start_url: str | None = None,
        client: httpx.Client | None = None,
        headers: dict | None = None,
        cookies_file: Path | None = None,
        save_path: str = "data",
        proxy: str | None = None,
        *args,
        **kwargs,
    ):
        self.username: str = username
        self.password: str = password

        self.headers: dict | None = headers or {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "content-type": "application/x-www-form-urlencoded",
            "origin": "https://jobinja.ir",
            "priority": "u=0, i",
            "referer": "https://jobinja.ir/login/user?redirect_url=https%3A%2F%2Fjobinja.ir%2Fjobs%3Ffilters%255Bjob_categories%255D%2",
            "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "upgrade-insecure-requests": "1",
            "user-agent": self.user_agent,
        }
        self.start_url: str = start_url or self.HOME_PAGE_URL

        self.paginator_xpath = '//div[@class="paginator"]/ul/li[last()-1]/a/text()'  # xpath to get the last page number

        self.save_path = save_path
        self._crawled_links: list[str] = []
        self.proxy = proxy

        self.cookies_file: Path = (
            cookies_file or data_path / f"{self.source_name}.cookies"
        )

        self.client = client or httpx.Client(follow_redirects=True, proxy=self.proxy)
        if self.cookies_file.exists():
            logger.info("Loading Jobinja Cookies")
            self.load_cookies()
        else:
            logger.info("Attempting Jobinja Login")
            self.login()

        super().__init__(*args, **kwargs)

    def login(self):
        response = self.client.get(self.LOGIN_PAGE_URL, headers=self.headers)
        response.raise_for_status()
        tree = lxml.html.fromstring(response.content)
        input_tags = tree.xpath('//input[@name="_token"]/attribute::value')
        if input_tags and len(input_tags) > 0:
            _token = input_tags[0]
        data = {
            "redirect_url": "https://jobinja.ir/jobs?filters%5Bjob_categories%5D%2",
            "remember_me": "on",
            "identifier": self.username,
            "password": self.password,
            "_token": _token,
        }
        post_response = self._fetch(
            method="POST", url=self.LOGIN_URL, headers=self.headers, data=data
        )
        self.save_cookies()

    def load_cookies(self):
        with open(self.cookies_file, "rb") as file:
            cookies_dict = pickle.load(file)
        for name, value in cookies_dict.items():
            self.client.cookies.set(name, value)

    def save_cookies(self):
        cookies_dict = {cookie.name: cookie.value for cookie in self.client.cookies.jar}
        with open(self.cookies_file, "wb") as file:
            pickle.dump(cookies_dict, file)

    def crawl_job_link(self, node: Element) -> str | None:
        return get_xpath_first_element(
            node,
            '*/*/h2[contains(@class,"o-listView__itemTitle c-jobListView__title")]/a/attribute::href',
        )

    def discover_urls(self, since: datetime | None = None) -> Iterator[str]:
        """Yield page URLs to crawl (from a sitemap, listing page, API, etc.)."""
        page = 1
        while True:
            # TODO: Implement since logic later. For now, crawl just 10 pages.
            # TODO: Debug only 1 page
            if page >= 2:
                break
            logger.info("Crawling Jobinja page %s", page)
            jobs_params = {"page": page, "sort_by": "published_at_desc"}
            response = self._fetch(
                method="GET",
                url=self.HOME_PAGE_URL,
                headers=self.headers,
                params=jobs_params,
            )
            if not response:
                break
            tree = lxml.html.fromstring(response)
            jobs = tree.xpath('//li[contains(@class,"o-listView__item__application")]')
            for item in jobs:
                link: str = self.crawl_job_link(item)
                if link:
                    logger.info(f"Crawling job link {link}")

                    yield link

            rnd = random.randint(0, 2)
            logger.info(f"Page {page} done, waiting for {rnd} seconds")
            time.sleep(rnd)
            page += 1

    def extract_job_title(self, node: Element) -> str | None:
        return get_xpath_first_element(
            node,
            '//div[@class="c-jobView__titleText"]/h1/text()',
        )

    def extract_job_metas(self, node: Element) -> dict[str, str]:
        lis = node.xpath("//ul[contains(@class,'c-infoBox')]/li")
        output: dict[str, str] = {}
        for li in lis:
            key = li.xpath("h4")[0].text.strip()
            tags = [
                remove_extra_spaces(span.text.strip().replace("\n", " "))
                for span in li.xpath('div[@class="tags"]/span')
            ]
            output[key] = tags

        return output

    def extract_job_id(self, url: str):
        return url.split("/jobs/")[-1].split("/")[0]

    def extract_job_description(self, node: Element) -> str:
        return (
            node.xpath('//div[contains(@class,"s-jobDesc")]')[0].text_content().strip()
        )

    def extract_job_body(self, node: Element) -> str:
        el = node.find("body")
        body = tostring(el).decode("utf-8")
        return body

    def extract_company_name(self, node: Element) -> str:
        return node.xpath("//h2[@class='c-companyHeader__name']")[0].text_content()

    def extract_company_description(self, node: Element) -> str:
        description: str = "\n".join(
            [
                x.text_content().strip()
                for x in node.xpath("//span[@class='c-companyHeader__metaItem']")
            ]
        )
        return description

    def extract_company_photo_url(self, node: Element) -> str | None:
        return node.xpath("//img[@class='c-companyHeader__logoImage']/attribute::src")[
            0
        ]

    def extract_company_link(self, node: Element) -> str | None:
        return node.xpath("//a[@class='c-companyHeader__logoLink']/attribute::href")[0]

    def extract_job(self, link: str, node: Element) -> CanonicalJob:
        title: str = self.extract_job_title(node)
        job_id: str = self.extract_job_id(link)
        job_metas: dict[str, str] = self.extract_job_metas(node=node)
        description: str = self.extract_job_description(node)
        # body: str = self.extract_job_body(node)

        company_name: str = self.extract_company_name(node)
        city = next(
            value[0]
            for key, value in job_metas.items()
            if key == "city" or "مکان" in key
        )
        return CanonicalJob(
            id=job_id,
            title=title,
            company=company_name,
            description=description,
            city=city,
            meta=job_metas,
            source=self.source_name,
            url=link,
            created_at=datetime.now(),
        )

    def parse(self, url: str, html: str) -> CanonicalJob:
        """Turn raw HTML for one page into a RawDocument."""
        logger.info(f"Parsing job {url}")
        tree = lxml.html.fromstring(html)
        job: CanonicalJob = self.extract_job(link=url, node=tree)
        return job
