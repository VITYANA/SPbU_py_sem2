import abc
import asyncio
from tkinter import Tk, ttk

from Model import HTMLParser
from View import MainView


class IViewModel(metaclass=abc.ABCMeta):
    def __init__(self, model: HTMLParser, loop: asyncio.AbstractEventLoop):
        self._model = model
        self._loop = loop

    @abc.abstractmethod
    def start(self, root: Tk) -> ttk.Frame:
        raise NotImplementedError


class MainViewModel(IViewModel):
    def _bind(self, view: MainView) -> None:
        view.best_btn.config(
            command=lambda: self._loop.create_task(self.request_apply("https://башорг.рф/best/2024", view, "best", 10))
        )

        view.rand_btn.config(
            command=lambda: self._loop.create_task(self.request_apply("https://башорг.рф/random", view, "random", 10))
        )

        view.resc_btn.config(
            command=lambda: self._loop.create_task(self.request_apply("https://башорг.рф", view, "recent", 10))
        )

    async def request_apply(self, url: str, view: MainView, name: str, limit: int) -> None:
        new_text = ""
        text = await self._model.parse(url, name, limit)
        for quote in text:
            new_text += quote
        view.set_message(new_text)

    def start(self, root: Tk) -> MainView:
        frame = MainView(root)
        self._bind(frame)
        frame.grid(row=0, column=0, sticky="NSEW")
        return frame
