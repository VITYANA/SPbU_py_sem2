import hypothesis.strategies as st
from hypothesis import given, settings

from src.Homeworks.homework4.Sort import *


@settings(max_examples=100, deadline=None)
@given(st.lists(st.integers()), st.integers(min_value=1, max_value=32), st.booleans())
def test_merge(lst, num_threads, multiprocess):
    expected = list(sorted(lst))
    actual = merge_sort(lst, num_threads, multiprocess)
    assert actual == expected


@settings(max_examples=100, deadline=None)
@given(st.lists(st.integers()), st.integers(min_value=2, max_value=32))
def test_multithread_merge_sort(lst, threads):
    assert list(sorted(lst)) == multithread_merge_sort(lst, threads, True)


@settings(max_examples=100, deadline=None)
@given(st.lists(st.integers()))
def test_recursive_merge_sort(lst):
    assert list(sorted(lst)) == recursive_merge_sort(lst)
