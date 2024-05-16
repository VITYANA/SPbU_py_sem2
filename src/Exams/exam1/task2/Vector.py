from typing import Generic, Protocol, TypeVar


class ArithmeticAvailable(Protocol):
    def __add__(self, other: "T") -> "T":
        raise NotImplementedError

    def __sub__(self, other: "T") -> "T":
        raise NotImplementedError

    def __mul__(self, other: "T") -> "T":
        raise NotImplementedError


class DimensionError(Exception):
    def __init__(self, *args: str | None) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self) -> str:
        if self.message:
            return f"DimensionError: {self.message}"
        else:
            return "DimensionError has been raised"


T = TypeVar("T", bound=ArithmeticAvailable)


class Vector(Generic[T]):
    def __init__(self, coordinates: list[T]) -> None:
        self.coordinates: list[T] = coordinates
        self.dimension: int = len(coordinates)

    def __len__(self) -> int:
        return self.dimension

    def __add__(self, second: "Vector") -> "Vector":
        if self.dimension != second.dimension:
            raise DimensionError("Vectors have different dimensions.")
        new_coord = [self.coordinates[i] + second.coordinates[i] for i in range(self.dimension)]
        return Vector(new_coord)

    def __sub__(self, second: "Vector") -> "Vector":
        if self.dimension != second.dimension:
            raise DimensionError("Vectors have different dimensions.")
        new_coord = [self.coordinates[i] - second.coordinates[i] for i in range(self.dimension)]
        return Vector(new_coord)

    def scalar_product(self, second: "Vector") -> T:
        if self.dimension != second.dimension:
            raise DimensionError("Vectors have different dimensions.")
        return sum([self.coordinates[i] * second.coordinates[i] for i in range(self.dimension)])

    def vector_product(self, second: "Vector") -> "Vector":
        if self.dimension != second.dimension:
            raise DimensionError("Vectors have different dimensions.")
        if self.dimension != 3:
            raise DimensionError("Dimension of vectors should be 3.")
        a1, a2, a3 = self.coordinates[0], self.coordinates[1], self.coordinates[2]
        b1, b2, b3 = second.coordinates[0], second.coordinates[1], second.coordinates[2]
        return Vector([a2 * b3 - a3 * b2, a3 * b1 - a1 * b3, a1 * b2 - a2 * b1])

    def is_null(self) -> bool:
        return not any(self.coordinates)
