from typing import Mapping
import pytest
from src.Homeworks.homework1.task1.Registry import *

MAPPING_REGISTRY = Registry[Mapping]()
MAPPING_REGISTRY_default = Registry[Mapping](default=dict)


@MAPPING_REGISTRY.register(name="avl_tree")
class AVL_tree(Mapping):
    def __init__(self):
        pass

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass


@MAPPING_REGISTRY_default.register(name="cartesian_tree")
class Cartesian_tree(Mapping):
    def __init__(self):
        pass

    def __getitem__(self, item):
        pass

    def __iter__(self):
        pass

    def __len__(self):
        pass


def test_register():
    assert (
        MAPPING_REGISTRY.registry["avl_tree"] == AVL_tree
        and MAPPING_REGISTRY_default.registry["cartesian_tree"] == Cartesian_tree
        and MAPPING_REGISTRY_default.default == dict
    )


def test_dispatch():
    assert (
        MAPPING_REGISTRY.dispatch("avl_tree") == AVL_tree
        and MAPPING_REGISTRY_default.dispatch("cartesian_tree") == Cartesian_tree
        and MAPPING_REGISTRY_default.dispatch("missed_name") == dict,
    )


def test_register_error():
    with pytest.raises(ValueError):

        @MAPPING_REGISTRY.register(name="avl_tree")
        class DeadEnd:
            pass


def test_dispatch_error():
    with pytest.raises(ValueError):
        MAPPING_REGISTRY.dispatch("dropdown")
