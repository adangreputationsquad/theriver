from typing import Optional, Tuple
import pandas as pd

from dataviz.plot_types import PLOT
from datafiles.datafile import DataFile
from datastudy_interface import IDataStudy
from datafiles.views.view import PointView, ListView, DictView, DfView


class FrameDataFile(DataFile):
    """
    DataFile object for frame data, is used to make views
    """
    def __init__(
            self,
            study: IDataStudy,
            data: pd.DataFrame,
            name: str,
            desc: str
    ) -> None:
        """
        :param study: DataStudy parent
        :param data: DataFrame holding the data
        :param name: Name of the DataFile object
        :param desc: Description of the data
        """
        super().__init__(study, data, name, desc)

    @property
    def data(self) -> pd.DataFrame:
        """
        :return: Data, in format pd.DataFrame
        """
        return self._data

    @staticmethod
    def from_csv(study: IDataStudy,
                 path: str,
                 name: str = "",
                 desc: str = "",
                 *args, **kwargs) -> "FrameDataFile":
        """
        Initialize a FrameDataFile from a csv
        :param path: Path to the csv
        :param study: Parent DataStudy
        :param name: Name for the file
        :param desc: Description for the file
        :param args:
        :param kwargs:
        :return: Instance of FrameDataFile
        """
        instance = FrameDataFile(
            study=study,
            name=name,
            desc=desc,
            data=pd.read_csv(path, *args, **kwargs),
        )
        return instance

    @staticmethod
    def from_xlsx(study,
                  name: str = "",
                  desc: str = "",
                  *args,
                  **kwargs) -> 'FrameDataFile':
        """
        Initialize a FrameDataFile from a xlsx
        :param study: Parent DataStudy
        :param name: Name for the file
        :param desc: Description for the file
        :param args:
        :param kwargs:
        :return: Instance of FrameDataFile
        """
        instance = FrameDataFile(
            study=study,
            name=name,
            desc=desc,
            data=pd.read_excel(*args, **kwargs),
        )
        return instance

    def make_point_view(
            self, name: str, col: str, row: int,
            plot: Optional[PLOT.POINT] = None
            ) -> PointView:
        """
        Make a point view from the data
        :param name: Name of the view
        :param col: Column of the point
        :param row: Row of the point
        :param plot: If left to None, make_point_view will not add the point as
        plot to the study, if set to a PLOT.POINT, will add the point to the
        study dashboard.
        :return: PointView object
        """
        view = PointView(name, self.data[col].loc[row])
        self._add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_list_view(
            self, name: str,
            col: Optional[str] = None,
            row: Optional[int] = None,
            elems: list[Tuple[str, int]] = None,
            plot: Optional[PLOT.LIST] = None
    ) -> ListView:
        """
        Make a list view from the data
        :param name: Name of the view
        :param col: Column of the list (exclusive with row)
        :param row: Row of the list (exclusive with col)
        :param elems: List of tuple (column, row) of single elements
        :param plot: If left to None, make_list_view will not add the list as
        plot to the study, if set to a PLOT.LIST, will add the list to the
        study dashboard
        :return: ListView object
        """
        if col is None and row is None and elems is None:
            raise ValueError("col, row, or elems must be specified")
        if (col is not None) + (row is not None) + (elems is not None) > 1:
            raise ValueError("only row, col or elems can be specified")

        if row is not None:
            view = ListView(name, self.data.loc[row].tolist())
            self._add_view(view)
        elif col is not None:
            view = ListView(name, self.data[col].tolist())
            self._add_view(view)
        else:
            view = ListView(
                name, [self.data[elem[0]].loc[elem[1]]
                       for elem in elems]  # type: ignore
                # We know elems is not None because we checked above in first if
            )
            self._add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_dict_view(
            self, name: str,
            col_key: str,
            col_value: str,
            plot: Optional[PLOT.LIST] = None
    ) -> DictView:
        """
        Make a dict view from the data
        :param name: Name of the view
        :param col_key: Column that will be used as keys
        :param col_value: Column that will be used as values
        :param plot: If left to None, make_dict_view will not add the dict as
        plot to the study, if set to a PLOT.DICT, will add the dict to the
        study dashboard
        :return: DictView object
        """
        dictionary = {
            key: value for key, value in
            zip(self.data[col_key], self.data[col_value])
        }
        view = DictView(name, dictionary)
        self._add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_df_view(self,
                     name: str,
                     cols: list[str] | str,
                     rows: Optional[list[int]] = None,
                     plot: Optional[PLOT.DF] = None
                     ) -> DfView:
        """
        Make a df view from the data
        :param name: Name of the view
        :param cols: Columns of the df
        :param rows: Rows of the df
        :param plot: If left to None, make_df_view will not add the df as
        plot to the study, if set to a PLOT.DF, will add the df to the
        study dashboard
        :return: DfView object
        """
        if isinstance(cols, str):
            cols = [cols]

        df = self.data[cols]
        if rows is not None:
            df = df.loc[rows]
        view = DfView(name, df)
        self._add_view(view)

        if plot is not None:
            self.add_plot(view, plot)

        return view
