from typing import Callable
from framedatafile import FrameDataFile
from jsondatafile import JSONDataFile


def smallest_index(names: list[str]) -> str:
    indexes = [int(name.split("_")[-1]) for name in names]
    for i in range(len(indexes) + 1):
        if i not in indexes:
            return i


class DataStudy:

    def __init__(self, name="data_study", desc=""):
        self._name = name
        self._desc = desc
        self.dfs: dict[str, FrameDataFile] = dict()
        self.jsons: dict[str, JSONDataFile] = dict()
        self._views = dict()

    def __repr__(self) -> str:
        return (f"DataStudy("
                f"name={self._name}, "
                f"desc={self._desc}, "
                f"dfs={list(self.dfs.values())}, "
                f"jsons={list(self.jsons.values())})")

    def add_csv(
            self, path, name: str = "", desc: str = "", *args, **kwargs
    ) -> None:
        if not name:
            name = f"data_frame_{smallest_index(self.dfs.keys())}"
        self.dfs[name] = FrameDataFile.from_csv(
            self, path, name=name, desc=desc,
            *args, **kwargs
        )

    def add_json(self, path: str, name: str = "", desc: str = "") -> None:
        if not name:
            name = f"data_json_{smallest_index(self.jsons.keys())}"
        self.jsons[name] = JSONDataFile.from_json(self, path, name, desc)

    @property
    def data(self):
        nb_data = len(self.dfs) + len(self.jsons)
        if nb_data == 0:
            raise Exception("DataStudy has no data")
        elif nb_data == 1:
            if len(self.dfs) == 1:
                return list(self.dfs.values())[0]
            else:
                return list(self.jsons.values())[0]

        out = self.dfs.copy()
        out.update(self.jsons)
        return out

    @property
    def views(self) -> dict[str, Callable]:
        return self._views


if __name__ == '__main__':
    ds = DataStudy("Test data study", "my data study")
    ds.add_csv(
        "data/example_data.csv",
        "My first data",
        "This data is a dataframe",
        encoding="utf-16",
        sep="\t"
    )
    ds.add_json(
        "data/example_data.json",
        "My first data but json",
        "This one is a json"
    )

