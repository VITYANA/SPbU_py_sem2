import pytest

from src.Tests.test1.task1 import *


def test_add_to_basket():
    store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
    basket = Basket()
    store.add(basket, "apple", 3)
    store.add(basket, "banana", 3)
    assert (
        {"apple": [4, 3, 1], "banana": [5, 3, 4]} == basket.list
        and store.all_products_list["apple"][1] == 9
        and store.all_products_list["banana"][1] == 9
    )


def test_remove_from_basket():
    store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
    basket = Basket()
    store.add(basket, "apple", 3)
    store.add(basket, "banana", 3)
    store.remove(basket, "banana")
    store.remove(basket, "apple")
    assert (
        {} == basket.list and store.all_products_list["apple"][1] == 12 and store.all_products_list["banana"][1] == 12
    )


def test_error_add_volume():
    with pytest.raises(ValueError):
        store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
        basket = Basket()
        store.add(basket, "apple", 15)


def test_error_add_name():
    with pytest.raises(ValueError):
        store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
        basket = Basket()
        store.add(basket, "orange", 15)


def test_error_remove():
    with pytest.raises(ValueError):
        store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
        basket = Basket()
        store.remove(basket, "banana")


def test_sell():
    store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
    basket = Basket()
    store.add(basket, "apple", 4)
    client_money = 123
    assert "Congrats, have a good day." == store.sell(basket, client_money)


def test_error_sell():
    with pytest.raises(ValueError):
        store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4]})
        basket = Basket()
        store.add(basket, "apple", 4)
        client_money = 0
        store.sell(basket, client_money)


def test_find_min_max():
    store = Store({"apple": [4, 12, 1], "banana": [5, 12, 4], "orange": [13, 12, 11], "kiwi": [12, 19, 10]})
    assert store.min_max == [
        {"apple": [4, 12, 1]},
        {"orange": [13, 12, 11]},
        {"apple": [4, 12, 1]},
        {"orange": [13, 12, 11]},
    ]


# some changes
