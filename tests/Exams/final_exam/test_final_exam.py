import pytest

from src.Exams.final_exam.final_exam_main import *


def test_main():
    assert search_route("1934 Montreux Fascist conference", 2, "Totalitarianism") == [
        "Totalitarianism",
        "1934 Montreux Fascist conference",
        "Adolf Hitler",
    ]
    assert search_route("XX Bomber Command", 2, "Court-martial") is None
