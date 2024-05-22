import pytest

from src.Homeworks.homework1.task2.Treap import *


class TestTreap:
    @staticmethod
    def create_treap(items: list[list[Key, Value]]) -> Treap:
        treap = Treap()
        for key, value in items:
            treap[key] = value
        return treap

    @pytest.mark.parametrize("size", (5, 10, 15, 20, 25))
    def test_len(self, size):
        treap = Treap()
        for i in range(size):
            treap[i] = i
        assert len(treap) == size

    @pytest.mark.parametrize(
        "items",
        (
            [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
            [[12, 12], [144, 144], [-154, -154], [1203, 1203], [12, 12]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ),
    )
    def test_setitem(self, items):
        treap = self.create_treap(items)
        for k, v in treap.items():
            assert k == v
        for i in range(len(items)):
            assert items[i] in treap.items()

    @pytest.mark.parametrize(
        "items",
        (
            [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
            [[2, 2], [4, 4], [-1, -1], [13, 13], [2, 2]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ),
    )
    def test_getitem(self, items):
        treap = self.create_treap(items)
        for key, value in treap.items():
            assert treap[key] == value

    @pytest.mark.parametrize(
        "items, item_for_exc",
        (
            ([[11, 11], [22, 22], [3, 3], [-2303, -2303], [52, 52]], 999),
            ([[123, 123], [14, 14], [-4, -4], [203, 203], [2, 2]], 0),
            ([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], 1),
        ),
    )
    def test_getitem_exc(self, items, item_for_exc):
        tree = self.create_treap(items)
        with pytest.raises(KeyError):
            assert tree[item_for_exc]

    @pytest.mark.parametrize(
        "items",
        (
            [[111, 111], [221, 221], [13, 13], [-203, -203], [5, 5]],
            [[13, 13], [1, 1], [-4, -4], [2, 2], [3, 3]],
            [[1, 1], [-1, -1], [0, 0], [2, 2], [-2, -2]],
        ),
    )
    def test_del(self, items):
        treap = self.create_treap(items)
        for key in treap.keys():
            del treap[key]
            assert not treap.__contains__(key)

    @pytest.mark.parametrize(
        "items, item_for_exc",
        (
            ([[1, 1], [2, 2], [3, 3], [-3, -3], [2, 2]], 999),
            ([[123, 123], [144, 144], [-414, -414], [4203, 4203], [232, 232]], 0),
            ([[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]], 1),
        ),
    )
    def test_del_exc(self, items, item_for_exc):
        tree = self.create_treap(items)
        with pytest.raises(ValueError):
            del tree[item_for_exc]

    @pytest.mark.parametrize(
        "items",
        (
            [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
            [[12, 12], [144, 144], [-154, -154], [1203, 1203], [12, 12]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ),
    )
    def test_iter(self, items):
        treap = self.create_treap(items)
        assert list(treap.__iter__()) == list(treap.keys())

    @pytest.mark.parametrize(
        "items",
        (
            [[111, 111], [221, 221], [13, 13], [-203, -203], [5, 5]],
            [[13, 13], [1, 1], [-4, -4], [2, 2], [3, 3]],
            [[1, 1], [-1, -1], [0, 0], [2, 2], [-2, -2]],
        ),
    )
    def test_split(self, items):
        treap = self.create_treap(items)
        key = randint(-1000, 1000)
        left_treap, right_treap = treap.split(treap.root, key)
        left, right = Treap(), Treap()
        left.root, right.root = left_treap, right_treap
        if left.root is None:
            for right_treap_key in right.keys():
                assert right_treap_key >= key
        elif right.root is None:
            for left_treap_key in left.keys():
                assert left_treap_key < key
        else:
            for left_treap_key in left.keys():
                assert left_treap_key < key
            for right_treap_key in right.keys():
                assert right_treap_key >= key

    @pytest.mark.parametrize(
        "items",
        (
            [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5]],
            [[2, 2], [4, 4], [-1, -1], [13, 13], [2, 2]],
            [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0]],
        ),
    )
    def test_merge(self, items):
        treap = self.create_treap(items)
        for i in range(10):
            left_treap, right_treap = treap.split(treap.root, randint(-10, 10))
            res_treap = Treap()
            res_treap.root = Treap.merge(left_treap, right_treap)
            assert treap == res_treap
