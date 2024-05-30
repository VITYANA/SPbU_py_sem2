from io import StringIO

import hypothesis
import hypothesis.strategies as st
import pytest

from src.Homeworks.homework2.Actions import *
from src.Homeworks.homework2.main import *


class TestActions:
    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers())
    def test_action_insert_start_do(self, initial_list, value) -> None:
        action = ActionInsertStart(value)
        action.do(initial_list)
        assert initial_list[0] == value

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers())
    def test_action_insert_start_undo(self, initial_list, value) -> None:
        start_list = initial_list
        action = ActionInsertStart(value)
        action.do(initial_list)
        action.undo(initial_list)
        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers())
    def test_action_insert_end_do(self, initial_list, value) -> None:
        action = ActionInsertEnd(value)
        action.do(initial_list)
        assert initial_list[-1] == value

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250), st.integers())
    def test_action_insert_end_do(self, initial_list, value) -> None:
        start_list = initial_list[:]
        action = ActionInsertEnd(value)
        action.do(initial_list)
        action.undo(initial_list)
        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_insert_do(self, initial_list, insert_pos, value) -> None:
        start_len = len(initial_list)

        hypothesis.assume(insert_pos < start_len)

        action = ActionInsert(insert_pos, value)
        action.do(initial_list)

        assert start_len == len(initial_list) - 1
        assert initial_list[insert_pos] == value

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_insert_undo(self, initial_list, insert_pos, value) -> None:
        start_list = initial_list
        start_len = len(initial_list)

        hypothesis.assume(insert_pos < start_len)

        action = ActionInsert(insert_pos, value)
        action.do(initial_list)
        action.undo(initial_list)

        assert start_list == initial_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250),
        st.integers(min_value=0, max_value=250),
        st.integers(min_value=0, max_value=250),
    )
    def test_action_move_do(self, initial_list, pos1, pos2) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len and pos2 < start_len)

        action = ActionMove(pos1, pos2)
        action.do(initial_list)

        assert len(initial_list) == start_len
        assert start_list[pos1] == initial_list[pos2]

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250),
        st.integers(min_value=0, max_value=250),
        st.integers(min_value=0, max_value=250),
    )
    def test_action_move_undo(self, initial_list, pos1, pos2) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len and pos2 < start_len)

        action = ActionMove(pos1, pos2)
        action.do(initial_list)
        action.undo(initial_list)

        assert len(initial_list) == start_len
        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250),
        st.integers(min_value=0, max_value=250),
        st.integers(min_value=0, max_value=250),
    )
    def test_action_swap_do(self, initial_list, pos1, pos2) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len and pos2 < start_len)

        action = ActionSwap(pos1, pos2)
        action.do(initial_list)

        assert len(initial_list) == start_len
        assert initial_list[pos1] == start_list[pos2]
        assert initial_list[pos2] == start_list[pos1]

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250),
        st.integers(min_value=0, max_value=250),
        st.integers(min_value=0, max_value=250),
    )
    def test_action_swap_undo(self, initial_list, pos1, pos2) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len and pos2 < start_len)

        action = ActionSwap(pos1, pos2)
        action.do(initial_list)
        action.undo(initial_list)

        assert start_list == initial_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_add_value_do(self, initial_list, pos1, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionAddValue(pos1, value)
        action.do(initial_list)

        assert len(initial_list) == start_len
        assert initial_list[pos1] == start_list[pos1] + value

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_add_value_undo(self, initial_list, pos1, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionAddValue(pos1, value)
        action.do(initial_list)
        action.undo(initial_list)

        assert start_list == initial_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_subtract_do(self, initial_list, pos1, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionSubtract(pos1, value)
        action.do(initial_list)

        assert initial_list[pos1] == start_list[pos1] - value
        assert len(initial_list) == start_len

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(
        st.lists(st.integers(), min_size=0, max_size=250), st.integers(min_value=0, max_value=250), st.integers()
    )
    def test_action_subtract_undo(self, initial_list, pos1, value) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionSubtract(pos1, value)
        action.do(initial_list)
        action.undo(initial_list)

        assert start_list == initial_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250))
    def test_action_reverse_do(self, initial_list) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        action = ActionReverse()
        action.do(initial_list)

        assert initial_list == start_list[::-1]
        assert len(initial_list) == start_len

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250))
    def test_action_reverse_undo(self, initial_list) -> None:
        start_list = initial_list[:]

        action = ActionReverse()
        action.do(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=1, max_size=250), st.integers(min_value=0, max_value=250))
    def test_action_pop_do(self, initial_list, pos1) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionPop(pos1)
        action.do(initial_list)

        start_list.pop(pos1)
        assert initial_list == start_list
        assert len(initial_list) == start_len - 1

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=1, max_size=250), st.integers(min_value=0, max_value=250))
    def test_action_pop_undo(self, initial_list, pos1) -> None:
        start_len = len(initial_list)
        start_list = initial_list[:]

        hypothesis.assume(pos1 < start_len)

        action = ActionPop(pos1)
        action.do(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250))
    def test_action_clear_do(self, initial_list) -> None:
        action = ActionClear()
        action.do(initial_list)

        assert initial_list == []

    @hypothesis.settings(max_examples=100)
    @hypothesis.given(st.lists(st.integers(), min_size=0, max_size=250))
    def test_action_clear_undo(self, initial_list) -> None:
        start_list = initial_list[:]

        action = ActionClear()
        action.do(initial_list)
        action.undo(initial_list)

        assert initial_list == start_list


class TestPerformedCommandStorage:
    initial_list = []
    command_storage = PerformedCommandStorage(initial_list)
    action_insert1 = ActionInsertStart(12)
    action_insert2 = ActionInsertEnd(100)
    action_add = ActionAddValue(1, 900)
    action_move = ActionMove(1, 0)
    action_clear = ActionClear()

    def test_performed_command_storage(self):
        assert self.initial_list == []

        self.command_storage.apply(self.action_insert1)
        self.command_storage.apply(self.action_insert2)
        self.command_storage.apply(self.action_add)
        self.command_storage.apply(self.action_move)
        assert self.initial_list == [1000, 12]

        self.command_storage.apply(self.action_clear)
        assert self.initial_list == []

        self.command_storage.cancel()
        assert self.initial_list == [1000, 12]

        self.command_storage.cancel()
        self.command_storage.cancel()
        assert self.initial_list == [12, 100]

        self.command_storage.cancel()
        self.command_storage.cancel()
        assert self.initial_list == []

        with pytest.raises(ValueError):
            self.command_storage.cancel()


@pytest.mark.parametrize(
    "user_input, expected",
    [
        [["[]", "exit"], ["End programme\n"]],
        [["[1, 2]", "cancel", "exit"], ["Command storage is empty.\nEnd programme\n"]],
        [
            ["[100, 200, 300]", "insert_start 12", "insert_end 9", "exit"],
            ["Your collection: [12, 100, 200, 300]\nYour collection: [12, 100, 200, 300, 9]\nEnd programme\n"],
        ],
        [
            ["[1, 2, 3]", "info", "clear", "cancel", "exit"],
            [
                write_info(ACTIONS_REGISTRY)
                + "Your collection: [1, 2, 3]\nYour collection: []\nYour collection:  [1, 2, 3]\nEnd programme\n"
            ],
        ],
        [
            ["[1]", "move 3 13", "exit"],
            ["Unexpected error: pop index out of range\nYour collection: [1]\nEnd programme\n"],
        ],
        [["[]", "insert_start 1 2", "exit"], ["Wrong number of arguments\nYour collection: []\nEnd programme\n"]],
    ],
)
def test_main_scenario(monkeypatch, user_input, expected):
    monkeypatch.setattr("builtins.input", lambda _: user_input.pop(0))
    fake_output = StringIO()
    monkeypatch.setattr("sys.stdout", fake_output)
    main()
    output = fake_output.getvalue()
    expected.insert(0, write_info(ACTIONS_REGISTRY))
    assert output == "\n".join(expected)
