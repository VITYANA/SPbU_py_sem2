from __future__ import annotations

from abc import abstractmethod
from concurrent.futures import Future, ProcessPoolExecutor, ThreadPoolExecutor
from typing import List, Protocol, TypeVar, Union


class Comparable(Protocol):
    @abstractmethod
    def __lt__(self: "CT", other: "CT") -> bool:
        ...

    @abstractmethod
    def __le__(self: "CT", other: "CT") -> bool:
        ...


CT = TypeVar("CT", bound=Comparable)


def merge_sorted_lists(list1: List[CT], list2: List[CT]) -> list:
    res = []
    i, j = 0, 0
    list1_len = len(list1)
    list2_len = len(list2)
    while i < list1_len and j < list2_len:
        if list1[i] <= list2[j]:
            res.append(list1[i])
            i += 1
        else:
            res.append(list2[j])
            j += 1
    if i == list1_len:
        res += list2[j:]
    else:
        res += list1[i:]
    return res


def recursive_merge_sort(lst: List[CT]) -> list:
    list_len = len(lst)
    mid = list_len // 2
    if list_len <= 1:
        return lst
    sublist1, sublist2 = recursive_merge_sort(lst[:mid]), recursive_merge_sort(lst[mid:])
    return merge_sorted_lists(sublist1, sublist2)


def multithread_merge_sort(lst: List[CT], threads_cnt: int, multiprocess: bool) -> list:
    list_len = len(lst)
    if list_len <= 1:
        return lst
    sublist1: Union[Future, list]
    sublist2: Union[Future, list]
    mid = list_len // 2
    left_half, right_half = lst[:mid], lst[mid:]
    if threads_cnt == 2:
        if multiprocess:
            with ProcessPoolExecutor(max_workers=2) as executor:
                sublist1 = executor.submit(recursive_merge_sort, left_half)
                sublist2 = executor.submit(recursive_merge_sort, right_half)
                return merge_sorted_lists(sublist1.result(), sublist2.result())
        with ThreadPoolExecutor(max_workers=2) as executor:
            sublist1 = executor.submit(recursive_merge_sort, left_half)
            sublist2 = executor.submit(recursive_merge_sort, right_half)
            return merge_sorted_lists(sublist1.result(), sublist2.result())
    elif threads_cnt > 2:
        new_threads_cnt = threads_cnt // 2
        sublist1 = multithread_merge_sort(left_half, new_threads_cnt, multiprocess)
        sublist2 = multithread_merge_sort(right_half, new_threads_cnt, multiprocess)
        return merge_sorted_lists(sublist1, sublist2)
    else:
        return merge_sorted_lists(recursive_merge_sort(left_half), recursive_merge_sort(right_half))


def merge_sort(lst: list[CT], threads_cnt: int, multiprocess: bool) -> list:
    if threads_cnt > 0:
        result = multithread_merge_sort(lst, threads_cnt, multiprocess)
    else:
        result = recursive_merge_sort(lst)
    return result


if __name__ == "__main__":
    pass
