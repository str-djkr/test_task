import requests
from bs4 import BeautifulSoup
import re
from typing import List
from dataclasses import dataclass


@dataclass
class CountryRecord:
    name: str
    region: str
    population: int
    source: str = "wikipedia"


class Scraper:
    def __init__(self, source_url: str):
        self.source_url = source_url

    def fetch(self):
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        }
        resp = requests.get(self.source_url, headers=headers, timeout=20)
        resp.raise_for_status()
        return resp.text

    def parse_wikipedia_table(self, html: str) -> List[CountryRecord]:
        soup = BeautifulSoup(html, "html.parser")

        table = soup.find("table", class_=re.compile(r"wikitable"))
        if not table:
            raise RuntimeError("Could not find expected table on page")

        rows = table.find_all("tr")[1:]
        records = []

        for row in rows:
            cols = [c.get_text(strip=True) for c in row.find_all("td")]
            if len(cols) < 5:
                continue

            print(cols)

            country = cols[0]
            population = cols[2]
            region = cols[4]

            # Чистимо
            pop_text = population.strip().replace(",", "")

            if not pop_text.isdigit():
                continue

            population = int(pop_text)

            # 🔥 повертаємо клас, а не dict
            records.append(
                CountryRecord(
                    name=country,
                    region=region,
                    population=population,
                    source=self.source_url
                )
            )

        return records

    def parse(self) -> List[CountryRecord]:
        html = self.fetch()
        return self.parse_wikipedia_table(html)
