import pytest

from src.Exams.exam1.task2.Vector import *


@pytest.mark.parametrize(
    "first_coord, second_coord, expected",
    (([1, 2, 3], [2, 3, 4], [3, 5, 7]), ([12, 12], [24, 24], [36, 36]), ([16], [-7], [9])),
)
def test_vector_sum(first_coord, second_coord, expected):
    vector1 = Vector(first_coord)
    vector2 = Vector(second_coord)
    sum_vector = vector1 + vector2
    assert sum_vector.coordinates == expected


@pytest.mark.parametrize(
    "first_coord, second_coord, expected",
    (
        ([1, 2, 3], [1, 2, 3], [0, 0, 0]),
        ([3, 15, 9], [5, 7, 12], [-2, 8, -3]),
        ([-3, -300, 9], [120, 16, 82], [-123, -316, -73]),
    ),
)
def test_vector_differ(first_coord, second_coord, expected):
    vector1 = Vector(first_coord)
    vector2 = Vector(second_coord)
    sum_vector = vector1 - vector2
    assert sum_vector.coordinates == expected


@pytest.mark.parametrize(
    "first_coord, second_coord, expected",
    (([1, 2, 3], [1, 2, 3], 14), ([3, 15, 9], [5, 7, 12], 228), ([-3, -300, 9], [120, 16, 82], -4422)),
)
def test_scalar_product(first_coord, second_coord, expected):
    vector1 = Vector(first_coord)
    vector2 = Vector(second_coord)
    result = vector1.scalar_product(vector2)
    assert result == expected


@pytest.mark.parametrize(
    "first_coord, second_coord, expected",
    (
        ([14, 50, 60], [2, 3, 7], [170, 22, -58]),
        ([13, 13, 13], [14, 15, 16], [13, -26, 13]),
        ([200, 100, 3000], [500, 600, 400], [-1760000, 1420000, 70000]),
    ),
)
def test_vector_product(first_coord, second_coord, expected):
    vector1 = Vector(first_coord)
    vector2 = Vector(second_coord)
    result = vector1.vector_product(vector2)
    assert result.coordinates == expected


def test_sum_error():
    vector1, vector2 = Vector([1, 2]), Vector([1])
    with pytest.raises(DimensionError):
        vector1 + vector2


def test_differ_error():
    vector1, vector2 = Vector([1, 2]), Vector([1, 2, 3])
    with pytest.raises(DimensionError):
        vector1 - vector2


def test_scalar_error():
    vector1, vector2 = Vector([1, 2]), Vector([1, 2, 3])
    with pytest.raises(DimensionError):
        vector1.scalar_product(vector2)


def test_vector_error_not_3_dimension():
    vector1, vector2 = Vector([1, 2]), Vector([1, 2])
    with pytest.raises(DimensionError):
        vector1.vector_product(vector2)


def test_vector_error_different_dimensions():
    vector1, vector2 = Vector([1, 2, 3]), Vector([1, 2])
    with pytest.raises(DimensionError):
        vector1.vector_product(vector2)
