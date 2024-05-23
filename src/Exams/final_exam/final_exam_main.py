import multiprocessing
import warnings

import wikipedia
from bs4 import GuessedAtParserWarning

warnings.filterwarnings("ignore", category=GuessedAtParserWarning)


def bfs(start_page: str, target_page: str, depth: int, start_name: str) -> list | None:
    visited = set()
    queue = [(start_page, [start_page])]
    counter = 0
    while queue:
        page, path = queue.pop(0)
        visited.add(page)
        if counter == 20:
            counter = 0
            print(f"Now on page {page}")
        counter += 1
        try:
            if page == target_page:
                return [start_name, *path]

            if len(path) < depth:
                links = wikipedia.page(page).links
                for link in links:
                    if link not in visited:
                        queue.append((link, path + [link]))
        except wikipedia.exceptions.PageError:
            continue
        except wikipedia.exceptions.DisambiguationError:
            continue
        except KeyError:
            continue

    return None


def search_route(start_page: str, depth: int, start_name: str) -> list[str] | None:
    target_page = "Adolf Hitler"  # Заданный конечный элемент
    path = bfs(start_page, target_page, depth, start_name)
    if path:
        return path
    else:
        print("Путь не найден.")


def main() -> None:
    depth = int(input("Введите глубину поиска: "))
    num_processors = int(input("Введите число процессоров: "))
    start_name = input("Введите опциональное название статьи (оставьте пустым для случайной страницы): ")
    if not start_name:
        start_name = wikipedia.random()

    links = wikipedia.page(start_name).links
    if len(links) < num_processors:
        num_processors = len(links)
    procs = []
    for i in range(num_processors):
        start_page = links[i]
        p = multiprocessing.Process(target=search_route, args=(start_page, depth, start_name))
        procs.append(p)
        p.start()

    for proc in procs:
        proc.join()


if __name__ == "__main__":
    main()
