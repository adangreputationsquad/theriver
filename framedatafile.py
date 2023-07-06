from typing import Any
import pandas as pd
from datafile import DataFile
from datastudy import DataStudy


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
        self.add_view(name, lambda: self._data[col].loc[row])

    def make_list_view(self, name: str,
                       col: str = None,
                       row: int = None,
                       elems: list[str, int] = None) -> None:
        if col is None and row is None and elems is None:
            raise ValueError("col, row, or elems must be specified")
        if (col is not None) + (row is not None) + (elems is not None) > 1:
            raise ValueError("only row, col or elems can be specified")

        if row is not None:
            self.add_view(name, lambda: self.data.loc[row].tolist())
        elif col is not None:
            self.add_view(name, lambda: self.data[col].tolist())
        else:
            self.add_view(name, lambda: [self.data[elem[0]].loc[elem[1]]
                                         for elem in elems])
