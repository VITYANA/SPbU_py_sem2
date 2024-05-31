import argparse
import re
from concurrent.futures import ProcessPoolExecutor
from multiprocessing import Manager, active_children
from typing import Any, Optional

import requests
from bs4 import BeautifulSoup


class URLWithParent:
    def __init__(self, cur_url: str, prev_url: Optional["URLWithParent"]):
        self.cur_url = cur_url
        self.prev_url = prev_url

    def build_path(self) -> list[str]:
        path = [self.cur_url]
        if self.prev_url is None:
            return path

        def recursion(prev_url: Optional["URLWithParent"]) -> list[str]:
            if prev_url:
                path.append(prev_url.cur_url)
                return recursion(prev_url.prev_url)
            return path[::-1]

        return recursion(self.prev_url)


class BFS:
    def __init__(self, process_cnt: int, unique: bool) -> None:
        self.process_cnt: int = process_cnt
        self.unique: bool = unique
        self.visited: set[str] = set()

    @staticmethod
    def get_links(page_link: URLWithParent) -> list[URLWithParent]:
        response = requests.get(page_link.cur_url)
        soup = BeautifulSoup(response.text, "html.parser")
        div_content = soup.find("div", class_="mw-content-ltr mw-parser-output")
        if div_content:
            all_links = [
                "https://en.wikipedia.org" + link.get("href")
                for link in div_content.find_all("a", href=re.compile("^/wiki/+"))
            ]
            good_links = []
            for link in all_links:
                name_of_page = link.split("/wiki/")[-1]
                if ":" not in name_of_page and "ISBN" not in name_of_page:
                    good_links.append(URLWithParent(link, page_link))

            return good_links
        else:
            return []

    def multithread_bfs(self, start_page: str, next_page: str, deep: int) -> list[str]:
        queue = Manager().Queue()
        self.visited.add(start_page)
        queue.put(URLWithParent(start_page, None))
        with ProcessPoolExecutor(max_workers=self.process_cnt) as executor:
            for i in range(deep):
                futures = [executor.submit(self.get_links, queue.get()) for _ in range(queue.qsize())]
                for worker in futures:
                    links = worker.result()
                    for link in links:
                        if self.unique and link.cur_url in self.visited:
                            continue
                        print(link.cur_url)
                        if link.cur_url == next_page:
                            for process in active_children():
                                process.kill()
                            return link.build_path()
                        if link.cur_url not in self.visited:
                            queue.put(link)
                            self.visited.add(link.cur_url)
            raise ValueError(f"Can not find path with deep {deep}")


def main(links_path: list[str], deep: int, n_jobs: int, unique: bool) -> list[str]:
    bfs_wiki = BFS(n_jobs, unique)
    all_paths = []
    with ProcessPoolExecutor(len(links_path)) as executor:
        for i in range(len(links_path) - 1):
            start_url = links_path[i]
            end_url = links_path[i + 1]
            all_paths.append(executor.submit(bfs_wiki.multithread_bfs, start_url, end_url, deep))
    result_path = []
    for path in all_paths:
        result_path = path.result()
    return result_path


def parse_args() -> dict[str, Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument("pages", type=str, nargs="+")
    parser.add_argument("processor_count", type=int)
    parser.add_argument("--unique", action="store_true")
    args = parser.parse_args()
    return vars(args)


if __name__ == "__main__":
    args = parse_args()
    print(main(*args.values()))
