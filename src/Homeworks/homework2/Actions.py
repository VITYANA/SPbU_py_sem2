import abc
from typing import Optional

from src.Homeworks.homework1.task1.Registry import Registry

ACTIONS_REGISTRY = Registry["Action"]()


class Action(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def do(self, numbers: list) -> None:
        raise NotImplementedError

    @abc.abstractmethod
    def undo(self, numbers: list) -> None:
        raise NotImplementedError


@ACTIONS_REGISTRY.register(name="insert_start")
class ActionInsertStart(Action):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def do(self, numbers: list) -> None:
        numbers.insert(0, self.value)

    def undo(self, numbers: list) -> None:
        numbers.pop(0)


@ACTIONS_REGISTRY.register(name="insert_end")
class ActionInsertEnd(Action):
    def __init__(self, value: int) -> None:
        self.value: int = value

    def do(self, numbers: list) -> None:
        numbers.append(self.value)

    def undo(self, numbers: list) -> None:
        numbers.pop()


@ACTIONS_REGISTRY.register(name="move")
class ActionMove(Action):
    def __init__(self, first_pos: int, second_pos: int) -> None:
        self.first_pos: int = first_pos
        self.second_pos: int = second_pos

    def do(self, numbers: list) -> None:
        elem_to_move = numbers.pop(self.first_pos)
        numbers.insert(self.second_pos, elem_to_move)

    def undo(self, numbers: list) -> None:
        elem_to_move = numbers.pop(self.second_pos)
        numbers.insert(self.first_pos, elem_to_move)


@ACTIONS_REGISTRY.register(name="add_value")
class ActionAddValue(Action):
    def __init__(self, pos: int, value: int) -> None:
        self.pos: int = pos
        self.value: int = value

    def do(self, numbers: list) -> None:
        numbers[self.pos] += self.value

    def undo(self, numbers: list) -> None:
        numbers[self.pos] -= self.value


@ACTIONS_REGISTRY.register(name="insert")
class ActionInsert(Action):
    def __init__(self, pos: int, value: int):
        self.pos: int = pos
        self.value: int = value

    def do(self, numbers: list) -> None:
        numbers.insert(self.pos, self.value)

    def undo(self, numbers: list) -> None:
        numbers.pop(self.pos)


@ACTIONS_REGISTRY.register(name="subtract")
class ActionSubtract(Action):
    def __init__(self, pos: int, value: int) -> None:
        self.pos: int = pos
        self.value: int = value

    def do(self, numbers: list) -> None:
        numbers[self.pos] -= self.value

    def undo(self, numbers: list) -> None:
        numbers[self.pos] += self.value


@ACTIONS_REGISTRY.register(name="reverse")
class ActionReverse(Action):
    def do(self, numbers: list) -> None:
        numbers.reverse()

    def undo(self, numbers: list) -> None:
        self.do(numbers)


@ACTIONS_REGISTRY.register(name="swap")
class ActionSwap(Action):
    def __init__(self, first_pos: int, second_pos: int):
        self.first_pos: int = first_pos
        self.second_pos: int = second_pos

    def do(self, numbers: list) -> None:
        numbers[self.first_pos], numbers[self.second_pos] = numbers[self.second_pos], numbers[self.first_pos]

    def undo(self, numbers: list) -> None:
        self.do(numbers)


@ACTIONS_REGISTRY.register(name="pop")
class ActionPop(Action):
    def __init__(self, pos: int) -> None:
        self.pos: int = pos
        self.value: Optional[int] = None

    def do(self, numbers: list) -> None:
        self.value = numbers.pop(self.pos)

    def undo(self, numbers: list) -> None:
        numbers.insert(self.pos, self.value)


@ACTIONS_REGISTRY.register(name="clear")
class ActionClear(Action):
    def __init__(self) -> None:
        self.numbers: Optional[list] = None

    def do(self, numbers: list) -> None:
        self.numbers = list()
        self.numbers.extend(numbers)
        numbers.clear()

    def undo(self, numbers: list) -> None:
        if self.numbers:
            numbers.extend(self.numbers)
