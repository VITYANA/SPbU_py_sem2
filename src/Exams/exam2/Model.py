from typing import Any, List

import requests
from bs4 import BeautifulSoup


class HTMLParser:
    @staticmethod
    def get_text_page(url: str) -> str:
        return requests.get(url).text

    async def parse(self, url: str, name: str, limit: int) -> List[Any]:
        soup = BeautifulSoup(self.get_text_page(url), "html.parser")
        for br in soup("br"):
            br.replace_with("\n")
        new_list = soup.findAll("div", {"class": ["quote__body"]}, limit=limit if name != "recent" else limit + 1)
        if name == "recent":
            new_quotes = [quote.text.strip() for quote in new_list][1:]
        else:
            new_quotes = [quote.text.strip() for quote in new_list]
        return new_quotes
