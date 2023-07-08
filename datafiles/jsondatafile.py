import json
from typing import Any, Optional

import pandas as pd

from dataviz.plot_types import PLOT
from .utils import transform_lists_in_dict, match_pattern_to_values
from .datafile import DataFile
from datastudy_interface import IDataStudy
from .views.view import PointView, ListView, DictView, DfView


class JSONDataFile(DataFile):
    """
    DataFile object for JSON data, is used to make views
    """
    def __init__(self,
                 study: IDataStudy,
                 data: dict[str, Any],
                 name: str,
                 desc: str
                 ) -> None:
        """
        :param study: DataStudy parent
        :param data: Dictionary holding the data
        :param name: Name of the DataFile object
        :param desc: Description of the data
        """
        super().__init__(study, data, name, desc)

    @property
    def data(self) -> dict[str, Any]:
        """
        :return: Data, in format dictionary
        """
        return self._data

    @staticmethod
    def from_json(
            study: IDataStudy,
            path: str,
            name: str,
            desc: str
    ) -> 'JSONDataFile':
        """
        Initialize a JSONDataFile from a json
        :param study: Parent DataStudy
        :param path: Path to the json
        :param name: Name for the file
        :param desc: Description for the file
        :return: Instance of JSONDataFile
        """
        with open(path) as f:
            data = transform_lists_in_dict(json.load(f))
        return JSONDataFile(study, data, name, desc)

    def make_point_view(
            self,
            name: str,
            pattern: str,
            plot: Optional[PLOT.POINT] = None,
    ) -> PointView:
        """
        Make a point view from the data
        :param name: Name of the view
        :param pattern: Pattern to match the data with, use '/' for nested
        dictionaries
        :param plot: If left to None, make_point_view will not add the point as
        plot to the study, if set to a PLOT.POINT, will add the point to the
        study dashboard.
        :return: PointView object
        """
        temp = self.data
        for field in pattern.split("/"):
            temp = temp[field]
        view = PointView(name, temp)
        self._add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_list_view(
            self,
            name: str,
            pattern: Optional[str] = None,
            patterns: Optional[list[str]] = None,
            plot: Optional[PLOT.LIST] = None
    ) -> ListView:
        """
        Make a list view from the data
        :param name: Name of the view
        :param pattern: Pattern to match the data with, use '/' for nested
        dictionaries, use '*' as a wildcard to match multiple values
        :param patterns: List of patterns to match the data with
        :param plot: If left to None, make_list_view will not add the list as
        plot to the study, if set to a PLOT.LIST, will add the list to the
        study dashboard.
        :return: ListView object
        """
        if pattern is None and patterns is None:
            raise ValueError("pattern or patterns must be specified")
        if pattern is not None and patterns is not None:
            raise ValueError("pattern and patterns cannot both be specified")

        if pattern is not None:
            # case 1, there is at least one * in the path
            if "*" in pattern:
                matching_elements = match_pattern_to_values(self.data, pattern)
                view = ListView(name, list(matching_elements.values()))
                self._add_view(view)

                if plot is not None:
                    self.add_plot(view, plot)
                return view
            temp = self.data
            for field in pattern.split("/"):
                if field != "":
                    temp = temp[field]

            # case 2, path is a path that leads to a dict
            view = ListView(name, list(temp.values()))
            self._add_view(view)

            if plot is not None:
                self.add_plot(view, plot)
            return view

    def make_dict_view(
            self, name: str, *, pattern: str = None,
            key_pattern: str = None,
            value_pattern: str = None,
            plot: Optional[PLOT.DICT] = None
    ) -> DictView:
        """
        Make a dict view from the data
        :param name: Name of the view
        :param pattern: Pattern to match the data with (exclusive with
        key_pattern and value_pattern). Use '/' for nested dictionaries and '*'
        as a wildcard to match multiple values, values matched by '*' will be
        used as keys
        :param key_pattern: Pattern to match keys with (exclusive with pattern)
        :param value_pattern: Pattern to match values with (exclusive with
        pattern)
        :param plot: If left to None, make_dict_view will not add the dict as
        plot to the study, if set to a PLOT.DICT, will add the dict to the
        study dashboard.
        :return: DictView object
        """
        if (pattern is not None and
                (key_pattern is not None or value_pattern is not None)):
            raise ValueError(
                "pattern and time_pattern or value_pattern "
                "cannot both be specified"
            )
        if key_pattern is None and value_pattern is None and pattern is None:
            raise ValueError(
                "You must specify pattern or time_pattern "
                "and value_pattern"
            )

        if pattern is not None:
            dictionary = match_pattern_to_values(self.data, pattern)
            view = DictView(name, dictionary)
            self._add_view(view)
        else:
            keys = match_pattern_to_values(self.data, key_pattern).values()
            values = match_pattern_to_values(self.data, value_pattern).values()
            if len(keys) != len(values):
                raise IndexError(
                    f"Keys and values found are not the same length: "
                    f"{len(keys)},{len(values)}"
                )

            dictionary = {key: value for key, value in zip(keys, values)}
            view = DictView(name, dictionary)
            self._add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
        return view

    def make_df_view(
            self, name,
            pattern: Optional[str] = None,
            patterns: Optional[list[str]] = None,
            cols: Optional[list[str]] = None,
            plot: Optional[PLOT.DF] = None,
    ) -> DfView:
        """
        Make a df view from the data
        :param name: Name of the view
        :param pattern: Pattern to match the data with, use '/' for nested and
        '*' as a wildcard to match multiple values. Values matched with '*' will
        be recorded in a 'key' column and the values in 'value' column unless
        cols is specified. Exclusive with patterns
        :param patterns: Patterns to match the data with, use '/' for nested
        and '*' as a wildcard to match multiple values. Each pattern will match
        values and stored them in different columns. Keys matched with '*' will
        be discarded.
        :param cols: Name of the columns, must be of length 2 if pattern is
        specified, must be of length len(patterns) if patterns is specified.
        :param plot: If left to None, make_df_view will not add the df as
        plot to the study, if set to a PLOT.DF, will add the df to the
        study dashboard
        :return: DfView object
        """

        if pattern is None and patterns is None:
            raise ValueError("pattern or patterns must be specified")
        if pattern is not None and patterns is not None:
            raise ValueError("pattern and patterns cannot both be specified")

        if pattern is not None:
            dictionary = match_pattern_to_values(self.data, pattern)
            if cols is not None:
                col_1, col_2 = cols[0], cols[1]
            else:
                col_1, col_2 = "key", "value"
            df = pd.DataFrame.from_records(
                {
                    col_1: list(dictionary.keys()),
                    col_2: list(dictionary.values())
                }
            )
            view = DfView(name, df)
            self._add_view(view)
            if plot is not None:
                self.add_plot(view, plot)
            return view
        else:
            patterns = [] if patterns is None else patterns
            cols = ([f"col_{i}" for i in range(len(patterns))]
                    if cols is None else cols)
            if len(patterns) != len(cols):
                raise IndexError(
                    f"Keys and values found are not the same length: "
                    f"{len(patterns)},{len(cols)}"
                )
            dictionary = {
                col: list(match_pattern_to_values(self.data, pattern).values())
                for col, pattern in zip(cols, patterns)
            }
            df = pd.DataFrame.from_records(dictionary)
            view = DfView(name, df)
            self._add_view(view)
            if plot is not None:
                self.add_plot(view, plot)
            return view
