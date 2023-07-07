import json
from typing import Any, Optional

from dataviz.plot_types import PLOT
from .utils import remove_lists_from_json, math_pattern_to_values
from .datafile import DataFile
from .datastudy import DataStudy
from .views.view import PointView, ListView, DictionaryView


class JSONDataFile(DataFile):

    def __init__(self, study: DataStudy, data: Any, name, desc) -> None:
        super().__init__(study, data, name, desc)

    @property
    def data(self) -> Any:
        return self._data

    @staticmethod
    def from_json(
            study: DataStudy,
            path: str,
            name: str,
            desc: str
    ) -> 'JSONDataFile':
        with open(path) as f:
            data = remove_lists_from_json(json.load(f))
        return JSONDataFile(study, data, name, desc)

    def make_point_view(
            self,
            name: str,
            path: str,
            plot: Optional[PLOT.POINT] = None,
    ) -> None:
        temp = self.data
        for field in path.split("/"):
            temp = temp[field]
        view = PointView(name, temp)
        self.add_view(view)

        if plot is not None:
            self.add_plot(view, plot)

    def make_list_view(
            self,
            name: str,
            path: Optional[str] = None,
            paths: Optional[list[str]] = None,
            plot: Optional[PLOT.LIST] = None
    ) -> None:
        if path is None and paths is None:
            raise ValueError("path or paths must be specified")
        if path is not None and paths is not None:
            raise ValueError("path and paths cannot both be specified")

        if path is not None:
            # case 1, there is at least one * in the path
            if "*" in path:
                matching_elements = math_pattern_to_values(self.data, path)
                view = ListView(name, list(matching_elements.values()))
                self.add_view(view)

                if plot is not None:
                    self.add_plot(view, plot)
                return
            temp = self.data
            for field in path.split("/"):
                if field != "":
                    temp = temp[field]

            # case 2, path is a path that leads to a dict
            view = ListView(name, list(temp.values()))
            self.add_view(view)

            if plot is not None:
                self.add_plot(view, plot)
            return

    def make_dict_view(
            self, name: str, *, pattern: str = None,
            key_pattern: str = None,
            value_pattern: str = None,
            plot: Optional[PLOT.DICT] = None
    ) -> None:
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
            dictionary = math_pattern_to_values(self.data, pattern)
            view = DictionaryView(name, dictionary)
            self.add_view(view)
        else:
            keys = math_pattern_to_values(self.data, key_pattern).values()
            values = math_pattern_to_values(self.data, value_pattern).values()
            if len(keys) != len(values):
                raise IndexError(
                    f"Keys and values found are not the same length: "
                    f"{len(keys)},{len(values)}"
                )

            dictionary = {key: value for key, value in zip(keys, values)}
            view = DictionaryView(name, dictionary)
            self.add_view(view)

        if plot is not None:
            self.add_plot(view, plot)
