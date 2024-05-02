from tkinter import Tk, ttk
from tkinter.scrolledtext import ScrolledText


class MainView(ttk.Frame):
    GREETINGS = 'Welcome to "quotes"!'
    RAND = "Show random quotes"
    RECENT = "Show recent quotes"
    BEST = "Show best quotes"

    def __init__(self, root: Tk) -> None:
        super().__init__(root)

        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self.header = ttk.Label(self, text=self.GREETINGS)
        self.header.grid(row=0, column=0, columnspan=2, padx=10, pady=10)

        self.best_btn = ttk.Button(self, text=self.BEST)
        self.best_btn.grid(row=1, column=1, padx=10, pady=10, sticky="W")

        self.rand_btn = ttk.Button(self, text=self.RAND)
        self.rand_btn.grid(row=2, column=1, padx=10, pady=10, sticky="W")

        self.resc_btn = ttk.Button(self, text=self.RECENT)
        self.resc_btn.grid(row=3, column=1, padx=10, pady=10, sticky="W")

        self.entry = ScrolledText(self)
        self.entry.grid(row=4, column=1, padx=(0, 20), sticky="EW")

    def set_message(self, message: str) -> None:
        self.entry.insert("1.0", f"{message}")
