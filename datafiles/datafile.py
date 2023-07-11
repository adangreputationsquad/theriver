from typing import Any
from abc import ABC, abstractmethod
from datastudy_interface import IDataStudy
from datafiles.views.view import View, PointView, ListView, DictView, DfView
from dataviz.plot_types import PLOT


class DataFile(ABC):

    @abstractmethod
    def __init__(
            self, study: IDataStudy, data: Any, name="",
            desc=""
    ) -> None:
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

    def _add_view(self, view: View) -> None:
        """
        Add a view to the study's list of view
        :param view: View
        """
        self.assert_view_name(view.name)
        self._study.views[view.name] = view

    def add_plot(self, view, plot_type: PLOT, *args, **kwargs):
        """
        Add a plot to the study's list of plots that will be displayed in the
        dashboard
        :param view: View
        :param plot_type: Type of the plot
        """
        self._study.add_plot(view, plot_type, *args, **kwargs)

    @abstractmethod
    def make_point_view(self, *args) -> PointView:
        pass

    @abstractmethod
    def make_list_view(self, *args) -> ListView:
        pass

    @abstractmethod
    def make_dict_view(self, *args) -> DictView:
        pass

    @abstractmethod
    def make_df_view(self, *args) -> DfView:
        pass
