from abc import ABC, abstractmethod
from typing import Any, Callable, Optional

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
    def __call__(self):
        pass

    @abstractmethod
    def apply(self, func: Callable, *args, **kwargs):
        pass


class PointView(View):
    def __init__(self, name: str, data: Any) -> None:
        super().__init__(name, data)

    def apply(self,
              func: Callable,
              name: Optional[str] = None,
              *args):
        if name is not None:
            return PointView(
                name=name,
                data=func(self.data)
            )
        self.data = func(self.data)

    def __call__(self) -> Any:
        return self.data


class ListView(View):
    def __init__(self, name: str, data: list) -> None:
        super().__init__(name, data)

    def apply(self,
              func: Callable,
              name: Optional[str] = None,
              *args):
        if name is not None:
            return ListView(
                name=name,
                data=[func(elem) for elem in self.data]
            )
        self.data = [func(elem) for elem in self.data]

    def __call__(self) -> list:
        return self.data


class DictView(View):
    def __init__(self, name: str, data: dict) -> None:
        super().__init__(name, data)

    def apply(self,
              func: Callable,
              on_keys=False,
              name: Optional[str] = None,
              *args):
        if on_keys:
            data = {func(key): val for key, val in self.data.items()}
        else:
            data = {key: func(val) for key, val in self.data.items()}
        if name is not None:
            return DictView(
                name=name,
                data=data
            )
        self.data = data

    def __call__(self) -> dict:
        return self.data


class DfView(View):
    def __init__(self, name: str, data: pd.DataFrame) -> None:
        super().__init__(name, data)

    def apply(self,
              func: Callable,
              axis=0,
              name: Optional[str] = None,
              *args, **kwargs):
        if name is not None:
            return DfView(
                name=name,
                data=self.data.apply(
                    func,  axis, *args, **kwargs
                )
            )
        self.data = self.data.apply(func, axis, *args, **kwargs)

    def __call__(self) -> pd.DataFrame:
        return self.data
