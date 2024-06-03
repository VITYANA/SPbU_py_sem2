import abc
import random
from dataclasses import dataclass
from typing import Any, Callable, Optional

from src.Homeworks.homework6.Observer import Observable

WIN_CONDITION = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]


class Player:
    def __init__(self, name: str) -> None:
        self.name = name
        self.sign = ""

    def set_sign(self, sign: str) -> None:
        self.sign = sign


class Bot(Player, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def make_move(self, board: list[Optional[str]]) -> int:
        raise NotImplementedError


class EasyBot(Bot):
    def make_move(self, board: list[Optional[str]]) -> int:
        free_cells = [i for i in range(9) if board[i] is None]
        return random.choice(free_cells)


class HardBot(Bot):
    def make_move(self, board: list[Optional[str]]) -> int:
        free_cells = [i for i in range(9) if board[i] is None]
        if 4 in free_cells:
            return 4
        cur_board_o = [i for i in range(9) if board[i] == "O"]
        cur_board_x = [i for i in range(9) if board[i] == "X"]
        for win_pos in WIN_CONDITION:
            if len(set(win_pos) & set(cur_board_x)) == 2:
                pos = list(set(win_pos) - set(cur_board_x))[0]
                if pos in free_cells:
                    return pos
            if len(set(win_pos) & set(cur_board_o)) == 2:
                pos = list(set(win_pos) - set(cur_board_o))[0]
                if pos in free_cells:
                    return pos

        free_diagonal_cages = [num_cage for num_cage in free_cells if num_cage % 2 == 0 and num_cage != 4]

        if free_diagonal_cages:
            return random.choice(free_diagonal_cages)
        if free_cells:
            return random.choice(free_cells)

        raise ValueError("Bot broke")


class MultiplayerUser(Player):
    pass


@dataclass
class Session:
    name: str
    data: Any


class GameBoard:
    def __init__(self) -> None:
        self.cells: list[Observable] = [Observable() for _ in range(9)]
        self.free_cells = list(range(9))

    def get_board(self) -> list[Optional[str]]:
        return [cell.value for cell in self.cells]

    def make_move(self, coord: int, sign: str) -> None:
        self.cells[coord].value = sign
        self.free_cells.remove(coord)

    def restart_board(self) -> None:
        for cell in self.cells:
            del cell.value
        self.free_cells = list(range(9))


def check_win(board: list[Optional[str]], sign: str) -> bool:
    cur_board = list(i for i in range(9) if board[i] == sign)
    for win_pos in WIN_CONDITION:
        if len(set(win_pos) & set(cur_board)) == 3:
            return True
    return False


class GameModel:
    def __init__(self) -> None:
        self.board: GameBoard = GameBoard()
        self.first_player: Optional[Player] = None
        self.second_player: Optional[Player] = None
        self.current_player: Optional[Player] = None
        self.current_session: Observable = Observable()
        self.active: bool = False

    def make_bot_move(self) -> None:
        if isinstance(self.current_player, EasyBot):
            self.make_move(self.current_player.make_move(self.board.get_board()))
        if isinstance(self.current_player, HardBot):
            self.make_move(self.current_player.make_move(self.board.get_board()))

    def make_move(self, coord: int) -> None:
        if coord in self.board.free_cells and self.current_player is not None:
            self.board.make_move(coord, self.current_player.sign)
            if check_win(self.board.get_board(), self.current_player.sign):
                self.active = False
                self.current_session.value = Session("game_result", self.current_player.name)
                return
            if len(self.board.free_cells) == 0:
                self.current_session.value = Session("game_result", None)
                return
            if self.current_player == self.first_player:
                self.current_player = self.second_player
            else:
                self.current_player = self.first_player
            self.make_bot_move()

    def choose_side(self, type_game: str) -> None:
        if type_game == "multiplayer":
            players: tuple[Player, Player] = (MultiplayerUser("You"), MultiplayerUser("Player2"))
        elif type_game == "easy":
            players = (Player("Player1"), EasyBot("Easy bot"))
        elif type_game == "hard":
            players = (Player("Player1"), HardBot("Hard bot"))
        else:
            players = (Player("Player1"), Player("Player2"))
        self.current_session.value = Session("choose_side", players)

    def start_game(self, player1: Player, player2: Player) -> None:
        self.first_player = player1
        self.second_player = player2
        self.current_player = player1
        self.active = True
        self.current_session.value = Session("game_field", (player1, player2))
        self.make_bot_move()

    def restart_game(self) -> None:
        self.board.restart_board()
        self.current_session.value = Session("main", None)

    def add_session_listener(self, callback: Callable) -> Callable:
        return self.current_session.add_callback(callback)
