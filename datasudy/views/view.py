from abc import ABC
from typing import Any

import pandas as pd


class View(ABC):

    def __init__(self, name: str, data: Any) -> None:
        self.name = name
        self.data = data

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"name: {self.name},\ndata:\n{self.data}\n)")


class PointView(View):
    def __init__(self, name: str, data: Any) -> None:
        super().__init__(name, data)


class ListView(View):
    def __init__(self, name: str, data: list) -> None:
        super().__init__(name, data)

    def __getitem__(self, key: int) -> Any:
        return self.data[key]

    def __len__(self) -> int:
        return len(self.data)


class DictionaryView(View):
    def __init__(self, name: str, data: dict) -> None:
        super().__init__(name, data)

    def __getitem__(self, item):
        return self.data[item]

    def keys(self):
        return self.data.keys()

    def values(self):
        return self.data.values()

    def items(self):
        return self.data.items()