import asyncio

import pytest

from src.Tests.test2.Model import *

parser = HTMLParser()


@pytest.mark.parametrize("limit", [5, 10, 15])
def test_get_recent(limit):
    quotes = asyncio.run(parser.parse("https://башорг.рф", "recent", limit))
    assert len(quotes) == limit


@pytest.mark.parametrize("limit", [5, 10, 15])
def test_get_best(limit):
    quotes = asyncio.run(parser.parse("https://башорг.рф/best/2024", "best", limit))
    assert len(quotes) == limit


@pytest.mark.parametrize("limit", [5, 10, 15])
def test_get_random(limit):
    quotes = asyncio.run(parser.parse("https://башорг.рф/random", "random", limit))
    assert len(quotes) == limit
