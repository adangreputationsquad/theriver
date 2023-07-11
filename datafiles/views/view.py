from abc import ABC, abstractmethod
from typing import Any, Callable

import pandas as pd


class View(ABC):
    """
    View object, we use it to get data from the datafiles and giving it the
    structure we want (point, list, dict, dataframe).
    Each view can lead to different plot
    """

    def __init__(self, name: str, data: Any) -> None:
        self.name = name
        self.data = data

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"name: {self.name},\ndata:\n{self.data}\n)")

    @abstractmethod
    def apply(self, func: Callable, *args, **kwargs):
        pass


class PointView(View):
    def __init__(self, name: str, data: Any) -> None:
        super().__init__(name, data)

    def apply(self, func: Callable, *args):
        self.data = func(self.data)


class ListView(View):
    def __init__(self, name: str, data: list) -> None:
        super().__init__(name, data)

    def apply(self, func: Callable, *args):
        self.data = [func(elem) for elem in self.data]


class DictView(View):
    def __init__(self, name: str, data: dict) -> None:
        super().__init__(name, data)

    def apply(self, func: Callable, on_keys=False, *args):
        if on_keys:
            self.data = {func(key): val for key, val in self.data.items()}
        self.data = {key: func(val) for key, val in self.data.items()}


class DfView(View):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        super().__init__(name, data)

    def apply(self, func: Callable, axis=0, *args, **kwargs):
        self.data.apply(func, axis, *args, **kwargs)
