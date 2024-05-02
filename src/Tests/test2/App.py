import asyncio
from tkinter import Tk

from Model import HTMLParser
from ViewModel import MainViewModel


class App:
    APPLICATION_NAME = "Quotes"
    START_SIZE = 512, 512
    MIN_SIZE = 256, 256

    def __init__(self) -> None:
        self._root = self._setup_root()
        self._model = HTMLParser()
        self._viewmodel = MainViewModel(self._model, asyncio.get_event_loop())
        self.start()

    def _setup_root(self) -> Tk:
        root = Tk()
        root.geometry("x".join(map(str, self.START_SIZE)))
        root.minsize(*self.MIN_SIZE)
        root.title(self.APPLICATION_NAME)
        root.grid_columnconfigure(0, weight=1)
        root.grid_rowconfigure(0, weight=1)
        return root

    async def update(self) -> None:
        while True:
            self._root.update()
            await asyncio.sleep(0)

    def start(self) -> None:
        self._viewmodel.start(self._root)


class Ex:
    @staticmethod
    async def exec() -> None:
        await App().update()


if __name__ == "__main__":
    app = Ex()
    asyncio.run(app.exec())
