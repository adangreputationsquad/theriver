import json
from typing import Any, Optional

import pandas as pd

from utils import remove_lists_from_json, math_pattern_to_values
from datafile import DataFile
from datastudy import DataStudy


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

    def make_point_view(self, name: str, path: str) -> None:
        temp = self.data
        for field in path.split("/"):
            temp = temp[field]

        self.add_view(name, lambda: temp)

    def make_list_view(
            self,
            name: str,
            path: Optional[str] = None,
            paths: Optional[list[str]] = None
    ) -> None:
        if path is None and paths is None:
            raise ValueError("path or paths must be specified")
        if path is not None and paths is not None:
            raise ValueError("path and paths cannot both be specified")

        if path is not None:
            # case 1, there is at least one * in the path
            if "*" in path:
                matching_elements = math_pattern_to_values(self.data, path)
                self.add_view(name, lambda: list(matching_elements.values()))
                return
            temp = self.data
            for field in path.split("/"):
                if field != "":
                    temp = temp[field]

            # case 2, path is a path that leads to a dict
            self.add_view(name, lambda: temp.values())
            return

    def make_timeseries_view(self, name: str, *, pattern: str= None,
                             time_pattern: str= None,
                             value_pattern: str= None) -> None:
        if (pattern is not None and
                (time_pattern is not None or value_pattern is not None)):
            raise ValueError("pattern and time_pattern or value_pattern "
                             "cannot both be specified")
        if time_pattern is None and value_pattern is None and pattern is None:
            raise ValueError("You must specify pattern or time_pattern "
                             "and value_pattern")

        if pattern is not None:
            timeseries = math_pattern_to_values(self.data, pattern)

            self.add_view(
                name, lambda: pd.DataFrame.from_records(
                    {
                        "time": timeseries.keys(),
                        "value": timeseries.values()
                    }
                )
            )
        else:
            times = math_pattern_to_values(self.data, time_pattern).values()
            values = math_pattern_to_values(self.data, value_pattern).values()
            self.add_view(
                name, lambda: pd.DataFrame.from_records(
                    {
                        "time": times,
                        "value": values
                    }
                )
            )