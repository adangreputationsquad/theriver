from typing import Callable


def smallest_index(names: list[str]) -> int:
    indexes = [int(name.split("_")[-1]) for name in names]
    for i in range(len(indexes) + 1):
        if i not in indexes:
            return i


class DataStudy:

    def __init__(self, name="data_study", desc=""):
        self._name = name
        self._desc = desc
        self._datas: dict[str, DataStudy] = dict()
        self._views = dict()

    def __repr__(self) -> str:
        return (f"DataStudy("
                f"name={self._name}, "
                f"desc={self._desc}, "
                f"datas={list(self.datas.values())})")

    def add_csv(
            self, path, name: str = "", desc: str = "", *args, **kwargs
    ) -> None:
        from framedatafile import FrameDataFile

        if not name:
            name = f"data_frame_{smallest_index(list(self.datas.keys()))}"
        self.datas[name] = FrameDataFile.from_csv(
            self, path, name=name, desc=desc,
            *args, **kwargs
        )

    def add_json(self, path: str, name: str = "", desc: str = "") -> None:
        from jsondatafile import JSONDataFile

        if not name:
            name = f"data_json_{smallest_index(list(self.datas.keys()))}"
        self.datas[name] = JSONDataFile.from_json(self, path, name, desc)

    @property
    def datas(self):
        return self._datas

    @property
    def views(self) -> dict[str, Callable]:
        return self._views
