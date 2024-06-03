from tkinter import DISABLED, Button, ttk
from typing import Any


class MainView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.easy_bot_button = Button(self, text="Play with easy bot", width=15, height=3)
        self.hard_bot_button = Button(self, text="Play with hard bot", width=15, height=3)
        self.one_pc_button = Button(self, text="Play on one pc", width=15, height=3)
        self.multiplayer_button = Button(self, text="Play multiplayer", width=15, height=3)

        self.easy_bot_button.grid(row=0, column=0)
        self.hard_bot_button.grid(row=0, column=3)
        self.one_pc_button.grid(row=1, column=0)
        self.multiplayer_button.grid(row=1, column=3)


class PlayingFieldView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.player1_button = Button(self, width=10, state=DISABLED)
        self.player1_button.grid(row=0, column=0)
        self.player2_button = Button(self, width=10, state=DISABLED)
        self.player2_button.grid(row=0, column=2)
        self.buttons_list = []
        for i in range(9):
            button = Button(self, bd=5, height=5, width=10)
            button.grid(row=3 + i // 3, column=i % 3)
            self.buttons_list.append(button)

    def set_names(self, player1_name: str, player1_sign: str, player2_name: str, player2_sign: str) -> None:
        self.player1_button.config(text=f"{player1_name}: {player1_sign}")
        self.player2_button.config(text=f"{player2_name}: {player2_sign}")


class ChooseSideView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.choose_side = ttk.Label(self, text="Choose side")
        self.choose_side.grid(row=0, column=1)

        self.x_button = Button(self, text="X")
        self.x_button.grid(row=1, column=0)

        self.o_button = Button(self, text="O")
        self.o_button.grid(row=1, column=2)


class ResultView(ttk.Frame):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)

        self.winner = ttk.Label(self)
        self.winner.grid(row=0, column=0)

        self.back_button = Button(self, text="Back to menu")
        self.back_button.grid(row=1, column=0)

    def set_name(self, winner_name: str) -> None:
        if winner_name is not None:
            self.winner.config(text=f"{winner_name} win the game!")
        else:
            self.winner.config(text="Tie")
