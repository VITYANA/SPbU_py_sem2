import src.Homeworks.homework2.Actions as Actions


class PerformedCommandStorage:
    def __init__(self, numbers: list) -> None:
        self.commands: list[Actions.Action] = []
        self.numbers: list = numbers

    def apply(self, action: Actions.Action) -> None:
        action.do(self.numbers)
        self.commands.append(action)

    def cancel(self) -> None:
        if len(self.commands) > 0:
            action_to_del = self.commands.pop(-1)
            action_to_del.undo(self.numbers)
        else:
            raise ValueError("Command storage is empty.")
