from typing import Any, Optional
import pandas as pd

from dataviz.plot_types import PLOT
from .datafile import DataFile
from .datastudy import DataStudy
from .views.view import PointView, ListView, DictView, DfView


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

    def make_point_view(
            self, name: str, col: str, row: int,
            plot: Optional[PLOT.POINT] = None
            ) -> PointView:
        view = PointView(name, self.data[col].loc[row])
        self.add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_list_view(
            self, name: str,
            col: str = None,
            row: int = None,
            elems: list[str, int] = None,
            plot: Optional[PLOT.LIST] = None
    ) -> ListView:
        if col is None and row is None and elems is None:
            raise ValueError("col, row, or elems must be specified")
        if (col is not None) + (row is not None) + (elems is not None) > 1:
            raise ValueError("only row, col or elems can be specified")

        if row is not None:
            view = ListView(name, self.data.loc[row].tolist())
            self.add_view(view)
        elif col is not None:
            view = ListView(name, self.data[col].tolist())
            self.add_view(view)
        else:
            view = ListView(
                name, [self.data[elem[0]].loc[elem[1]]
                       for elem in elems]
            )
            self.add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_dict_view(
            self, name: str,
            col_key: str,
            col_value: str,
            plot: Optional[PLOT.LIST] = None
    ) -> DictView:

        dictionary = {
            key: value for key, value in
            zip(self.data[col_key], self.data[col_value])
        }
        view = DictView(name, dictionary)
        self.add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_df_view(self,
                     name: str,
                     cols: list[str] | str,
                     rows: Optional[list[int]] = None,
                     plot: Optional[PLOT.DF] = None
                     ) -> DfView:

        if isinstance(cols, str):
            cols = [cols]

        df = self.data[cols]
        if rows is not None:
            df = df.loc[rows]
        view = DfView(name, df)
        self.add_view(view)

        if plot is not None:
            self.add_plot(view, plot)

        return view
