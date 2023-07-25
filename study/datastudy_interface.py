from abc import ABC, abstractmethod
from datafiles.views.view import View
from dataviz.plot_types import PLOT


class IDataStudy(ABC):

    @abstractmethod
    def add_csv(
            self, path: str, name: str = "", desc: str = "", *args, **kwargs
    ):
        pass

    @abstractmethod
    def add_json(
            self, path: str, name: str = "", desc: str = ""
    ):
        pass

    @property
    @abstractmethod
    def datas(self):
        pass

    @property
    @abstractmethod
    def views(self) -> dict[str, View]:
        pass

    @abstractmethod
    def render(self) -> None:
        pass

    @abstractmethod
    def add_plot(self, view: View, plot_type: PLOT, *args, **kwargs):
        pass
