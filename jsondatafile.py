import json
from typing import Any, Optional
from utils import remove_lists_from_json, get_matching_elements
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
                matching_elements = get_matching_elements(self.data, path)
                self.add_view(name, lambda: list(matching_elements.values()))
                return
            temp = self.data
            for field in path.split("/"):
                if field != "":
                    temp = temp[field]

            # case 2, path is a path that leads to a dict
            self.add_view(name, lambda: temp.values())
            return
