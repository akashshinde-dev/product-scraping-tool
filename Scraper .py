import requests
import time
import random
import logging
from typing import Dict, List, Any
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from save_to_csv import csv_dict


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class MultiPageScraper:
    """
    Generic multi-page product scraper.
    Supports flexible selectors and automatic pagination.
    """

    def __init__(self):
        ua = UserAgent()

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": ua.random
        })

        self.soup = None
        self.url = None
        self.response = None

    def get_page(self, url: str, max_try: int = 3) -> bool:
        """Fetch a webpage with retry support."""

        self.url = url

        for attempt in range(1, max_try + 1):
            try:
                self.response = self.session.get(url, timeout=8)
                self.response.raise_for_status()

                self.soup = BeautifulSoup(self.response.text, "html.parser")

                time.sleep(random.uniform(1.5, 3.5))
                return True

            except requests.RequestException as e:
                logging.warning(f"Attempt {attempt} failed: {e}")
                time.sleep(2)

        logging.error("Request failed after retries")
        return False

    def parse_page(self, item_selector: Dict, fields: Dict) -> List[Dict]:
        """Extract product data from current page."""

        if self.soup is None:
            raise RuntimeError("Call get_page() first")

        items = self.soup.find_all(
            item_selector.get("tag"),
            class_=item_selector.get("class_")
        )

        data = []

        for item in items:
            result = {}

            for field, selector in fields.items():

                parent = item
                if selector.get("parent"):
                    parent = item.find(
                        selector.get("parent"),
                        class_=selector.get("parent_class")
                    )

                if not parent:
                    result[field] = None
                    continue

                element = parent.find(
                    selector.get("tag"),
                    class_=selector.get("class_")
                )

                if not element:
                    result[field] = None
                    continue

                attr = selector.get("attr")

                if attr:
                    value = element.get(attr)

                    if attr == "href" and value:
                        value = urljoin(self.url, value)

                    if isinstance(value, list) and selector.get("index") is not None:
                        value = value[selector.get("index")]

                else:
                    value = element.get_text(strip=True)

                result[field] = value

            data.append(result)

        return data

    def scrape_multi_pages(
        self,
        start_url: str,
        item_selector: Dict,
        fields: Dict,
        next_page_selector: Dict,
        stop_page: int | None = None
    ) -> List[Dict]:
        """Scrape multiple pages automatically."""

        url = start_url
        all_data = []
        page_no = 0

        while True:

            logging.info(f"Scraping page: {url}")

            if not self.get_page(url):
                break

            page_no += 1

            page_data = self.parse_page(item_selector, fields)

            if page_data:
                all_data.extend(page_data)

            if stop_page and page_no >= stop_page:
                break

            parent = self.soup.find(
                next_page_selector.get("parent"),
                class_=next_page_selector.get("parent_class")
            )

            if not parent:
                break

            next_button = parent.find(
                next_page_selector.get("tag"),
                class_=next_page_selector.get("class_")
            )

            if not next_button:
                break

            link = next_button.select_one("a")

            if not link or not link.get("href"):
                break

            url = urljoin(url, link["href"])

        return all_data


def main():

    scraper = MultiPageScraper()

    url = "http://books.toscrape.com/"

    item_selector = {
        "tag": "article",
        "class_": "product_pod"
    }

    fields = {
        "Book_name": {
            "parent": "h3",
            "tag": "a",
            "attr": "title"
        },

        "Price": {
            "parent": "div",
            "parent_class": "product_price",
            "tag": "p",
            "class_": "price_color"
        },

        "Rating": {
            "tag": "p",
            "class_": "star-rating",
            "attr": "class",
            "index": 1
        },

        "Stock": {
            "tag": "p",
            "class_": "instock availability"
        },

        "Book_url": {
            "parent": "h3",
            "tag": "a",
            "attr": "href"
        }
    }

    next_page_selector = {
        "parent": "ul",
        "parent_class": "pager",
        "tag": "li",
        "class_": "next"
    }

    data = scraper.scrape_multi_pages(
        url,
        item_selector,
        fields,
        next_page_selector,
        stop_page=2
    )

    print(csv_dict.save(data))


if __name__ == "__main__":
    main()