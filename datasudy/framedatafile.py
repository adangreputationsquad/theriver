from typing import Any
import pandas as pd
from .datafile import DataFile
from .datastudy import DataStudy
from .views.view import PointView, ListView, TimeseriesView


class FrameDataFile(DataFile):
    def __init__(
            self, study: DataStudy, data: Any, name: str, desc: str
    ) -> None:
        super().__init__(study, data, name, desc)

    @property
    def data(self) -> Any:
        return self._data

    @staticmethod
    def from_csv(study: DataStudy, *args, **kwargs) -> 'FrameDataFile':
        instance = FrameDataFile(
            study=study,
            name=kwargs.pop("name", ""),
            desc=kwargs.pop("desc", ""),
            data=pd.read_csv(*args, **kwargs),
        )
        return instance

    @staticmethod
    def from_xlsx(study, *args, **kwargs) -> 'FrameDataFile':
        instance = FrameDataFile(
            study=study,
            name=kwargs.pop("name", ""),
            desc=kwargs.pop("desc", ""),
            data=pd.read_excel(*args, **kwargs),
        )
        return instance

    def make_point_view(self, name: str, col: str, row: int) -> None:
        view = PointView(name, self.data[col].loc[row])
        self.add_view(name, view)

    def make_list_view(self, name: str,
                       col: str = None,
                       row: int = None,
                       elems: list[str, int] = None) -> None:
        if col is None and row is None and elems is None:
            raise ValueError("col, row, or elems must be specified")
        if (col is not None) + (row is not None) + (elems is not None) > 1:
            raise ValueError("only row, col or elems can be specified")

        if row is not None:
            view = ListView(name, self.data.loc[row].tolist())
            self.add_view(name, view)
        elif col is not None:
            view = ListView(name, self.data[col].tolist())
            self.add_view(name, view)
        else:
            view = ListView(name, [self.data[elem[0]].loc[elem[1]]
                                         for elem in elems])
            self.add_view(name, view)

    def make_timeseries_view(self, name: str,
                             time_col: str,
                             value_col: str) -> None:
        view = TimeseriesView(name, self.data, time_col, value_col)
        return self.add_view(name, view)
