from dataclasses import dataclass
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


class TimeseriesView(View):
    def __init__(self, name: str, data: pd.DataFrame,
                 time_col: str, value_col: str,
                 time_format="mixed") -> None:
        data = data[[time_col, value_col]]
        super().__init__(name, data)
        self.time_col = time_col
        self.value_col = value_col
        self.data.loc[:, self.time_col] = (
            pd.to_datetime(self.data[self.time_col], format=time_format)
        )

    def __getitem__(self, item):
        return self.data.query(f"{self.time_col} == {item}")

    @property
    def times(self):
        return self.data[self.time_col]

    @property
    def values(self):
        return self.data[self.value_col]