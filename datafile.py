from typing import Any, TYPE_CHECKING
from abc import ABC, abstractmethod

from datastudy import DataStudy


class DataFile(ABC):

    @abstractmethod
    def __init__(self, study: DataStudy, data: Any, name="",
                 desc="") -> None:
        self._study = study
        self._data = data
        self._name = name
        self._desc = desc

    @property
    @abstractmethod
    def data(self) -> Any:
        pass

    @property
    def name(self) -> str:
        return self._name

    @property
    def desc(self) -> str:
        return self._desc

    def __repr__(self):
        return (f"{self.__class__.__name__}(name={self._name}, "
                f"desc={self._desc})")

    def assert_view_name(self, name: str) -> None:
        if name in self._study.views.keys():
            raise ValueError(f"View {name} already exists")

    def add_view(self, name, func) -> None:
        self.assert_view_name(name)
        self._study.views[name] = func

    @abstractmethod
    def make_point_view(self, *args) -> None:
        pass

    @abstractmethod
    def make_list_view(self, *args) -> None:
        pass
