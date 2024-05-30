import pytest

from src.Exams.final_exam.Wikiracer import *


class TestBFS:
    bfs_unique = BFS(8, True)
    bfs = BFS(8, False)

    @pytest.mark.parametrize(
        "start_page, next_page, deep",
        (
            (
                "https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College",
                "https://en.wikipedia.org/wiki/Napoleon",
                3,
            ),
            ("https://en.wikipedia.org/wiki/Saint_Lucia", "https://en.wikipedia.org/wiki/Napoleon", 1),
            ("https://en.wikipedia.org/wiki/Napoleon", "https://en.wikipedia.org/wiki/Adolf_Hitler", 1),
        ),
    )
    def test_multithread_bfs(self, start_page, next_page, deep):
        res1 = self.bfs_unique.multithread_bfs(start_page, next_page, deep)
        res2 = self.bfs.multithread_bfs(start_page, next_page, deep)
        assert res1[0] == start_page and res1[-1] == next_page
        assert res2[0] == start_page and res2[-1] == next_page

    @pytest.mark.parametrize(
        "start_page, next_page, deep",
        (
            (
                "https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College",
                "https://en.wikipedia.org/wiki/Napoleon",
                3,
            ),
            ("https://en.wikipedia.org/wiki/Saint_Lucia", "https://en.wikipedia.org/wiki/Napoleon", 1),
            ("https://en.wikipedia.org/wiki/Napoleon", "https://en.wikipedia.org/wiki/Adolf_Hitler", 1),
        ),
    )
    def test_multithread_bfs_error(self, start_page, next_page, deep):
        deep -= 1
        with pytest.raises(ValueError):
            self.bfs.multithread_bfs(start_page, next_page, deep)
            self.bfs_unique.multithread_bfs(start_page, next_page, deep)


@pytest.mark.parametrize(
    "cur_url, prev_url, expected",
    (
        (
            "https://en.wikipedia.org/wiki/Saint_Lucia",
            URLWithParent("https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College", None),
            [
                "https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College",
                "https://en.wikipedia.org/wiki/Saint_Lucia",
            ],
        ),
        (
            "https://en.wikipedia.org/wiki/Adolf_Hitler",
            URLWithParent(
                "https://en.wikipedia.org/wiki/Napoleon",
                URLWithParent(
                    "https://en.wikipedia.org/wiki/Saint_Lucia",
                    URLWithParent("https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College", None),
                ),
            ),
            [
                "https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College",
                "https://en.wikipedia.org/wiki/Saint_Lucia",
                "https://en.wikipedia.org/wiki/Napoleon",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ),
    ),
)
def test_build_path_method(cur_url, prev_url, expected):
    path = URLWithParent(cur_url, prev_url).build_path()
    assert path == expected


@pytest.mark.parametrize(
    "links_path, deep, n_jobs, unique, expected",
    (
        (
            [
                "https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
            4,
            4,
            True,
            [
                "https://en.wikipedia.org/wiki/Sir_Arthur_Lewis_Community_College",
                "https://en.wikipedia.org/wiki/Saint_Lucia",
                "https://en.wikipedia.org/wiki/Napoleon",
                "https://en.wikipedia.org/wiki/Adolf_Hitler",
            ],
        ),
        (
            ["https://en.wikipedia.org/wiki/Mein_Kampf", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
            1,
            1,
            False,
            ["https://en.wikipedia.org/wiki/Mein_Kampf", "https://en.wikipedia.org/wiki/Adolf_Hitler"],
        ),
    ),
)
def test_main(links_path, deep, n_jobs, unique, expected):
    assert main(links_path, deep, n_jobs, unique) == expected
