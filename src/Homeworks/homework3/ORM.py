import json
from dataclasses import asdict
from typing import Any, Generic, Type, TypeVar

T = TypeVar("T")


def dump_dataclass(obj: Any, path: str) -> None:
    with open(path, "w+") as json_file:
        json.dump(asdict(obj), json_file)


class Descriptor(Generic[T]):
    def __init__(self, key: str) -> None:
        self.key = key

    def __set__(self, instance: T, value: Any) -> None:
        instance.__dict__[self.key] = value

    def __get__(self, instance: T, owner: Type[T]) -> None:
        if instance is None:
            return self
        if not hasattr(instance, "__data__"):
            raise AttributeError("Data is missing")
        value = instance.__data__.get(self.key, None)
        if value is None:
            json_dict = getattr(instance, "branch_name")
            new_value = json_dict.get(self.key, None)
            if new_value is None:
                raise AttributeError(f"No {self.key} in data")
            value = new_value
            instance.__data__[self.key] = value
        return value


class ORM(type):
    def __init__(cls, name: str, bases: Any, dct: dict):
        all_branches = dict()
        for field_name, field_type in cls.__annotations__.items():
            if isinstance(field_type, ORM):
                all_branches[field_name] = field_type
                setattr(cls, field_name, None)
            else:
                setattr(cls, field_name, Descriptor(field_name))
        setattr(cls, "__branches__", all_branches)
        super(ORM, cls).__init__(name, bases, dct)

    def parse_json(cls: Type[T], data: dict) -> T:
        setattr(cls, "__data__", data)
        obj = cls(*[None for _ in range(len(cls.__annotations__.keys()))])
        for branch_name, branch_class in getattr(cls, "__branches__", {}).items():
            branch_data = data.get(branch_name, None)
            if branch_data is None:
                raise AttributeError(f"The {branch_name} is missing in json data")
            setattr(obj, branch_name, branch_class.parse_json(branch_data))
        return obj
