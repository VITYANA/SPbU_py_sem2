import typing
from collections import Counter, OrderedDict, defaultdict

T = typing.TypeVar("T")


class Registry(typing.Generic[T]):
    def __init__(self, default: typing.Optional[typing.Type[T]] = None):
        self.registry: dict[str, typing.Type[T]] = dict()
        self.default: typing.Optional[typing.Type[T]] = default

    def register(self, name: str) -> typing.Callable[[typing.Type[T]], typing.Type[T]]:
        def _add(cls: typing.Type[T]) -> typing.Type[T]:
            if name in self.registry:
                raise ValueError(f"Name {name} already in registry.")
            self.registry[name] = cls
            return cls
        return _add

    def dispatch(self, name: str) -> ValueError | typing.Type[T]:
        if name not in self.registry.keys():
            if self.default is None:
                raise ValueError(f"Registry haven't class named {name}.")
            return self.default
        return self.registry[name]


if __name__ == "__main__":
    try:
        register = Registry[dict](default=dict)
        register.register("Counter")(Counter)
        register.register("OrderedDict")(OrderedDict)
        register.register("defaultdict")(defaultdict)
        print("Enter one name of bellowed classes:")
        print("1)Counter")
        print("2)OrderedDict")
        print("3)defaultdict")
        user_input = input()
        print("Result:", register.dispatch(user_input))
    except Exception:
        print(f"No such class in registry.")
