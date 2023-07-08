from datafiles.datafile import DataFile
from datastudy_interface import IDataStudy
from dataviz.dataviz import DataStudyRenderer
from dataviz.plot_types import PLOT
from datafiles.views.view import View
from datafiles.framedatafile import FrameDataFile
from datafiles.jsondatafile import JSONDataFile


def _smallest_index(names: list[str]) -> int:
    indexes = [int(name.split("_")[-1]) for name in names]
    for i in range(len(indexes) + 1):
        if i not in indexes:
            return i


class DataStudy(IDataStudy):

    def __init__(self, name="data_study", desc=""):
        """
        The DataStudy class is a manager that holds DataFile, apply Views on
        them to rearrange data then display them on a dashboard with a
        DataRenderer
        :param name: Name of the study
        :param desc: Description of the study
        """
        from datafiles.datafile import DataFile
        self._name = name
        self._desc = desc
        self._datas: dict[str, DataFile] = dict()
        self._views: dict[str, View] = dict()
        self._renderer = DataStudyRenderer(name, desc)

    def __repr__(self) -> str:
        return (f"DataStudy("
                f"name={self._name}, "
                f"desc={self._desc}, "
                f"datas={list(self.datas.values())})")

    def add_csv(
            self, path: str, name: str = "", desc: str = "", *args, **kwargs
    ) -> FrameDataFile:
        """
        Add a csv file to the DataStudy
        :param path: Path to the csv file
        :param name: Name for the DataFile
        :param desc: Description for the file
        :param args: args and kwargs will be passed to read_csv from Pandas
        :param kwargs: args and kwargs will be passed to read_csv from Pandas
        :return: FrameDataFile object holding the data
        """
        from datafiles.framedatafile import FrameDataFile

        if name == "":
            name = f"data_frame_{_smallest_index(list(self.datas.keys()))}"
        out = FrameDataFile.from_csv(
            self, path, name=name, desc=desc,
            *args, **kwargs
        )
        self.datas[name] = out
        return out

    def add_json(
            self, path: str, name: str = "", desc: str = ""
    ) -> JSONDataFile:
        """
        Add a json file to the DataStudy
        :param path: Path to the file
        :param name: Name for the DataFile
        :param desc: Description of the file
        :return: JSONDataFile object holding the data
        """
        if name == "":
            name = f"data_json_{_smallest_index(list(self.datas.keys()))}"
        out = JSONDataFile.from_json(self, path, name, desc)
        self.datas[name] = out
        return out

    @property
    def datas(self) -> dict[str, DataFile]:
        """
        :return: Dict of DataFile objects indexed by name
        """
        return self._datas

    @property
    def views(self) -> dict[str, View]:
        """
        :return: Dict of View objects indexed by name
        """
        return self._views

    def render(self) -> None:
        """
        Render the DataStudy on a local dashboard
        """
        self._renderer.run()

    def add_plot(self, view: View, plot_type: PLOT, *args, **kwargs):
        """
        Add a plot to the DataStudy
        :param view: View of the data to plot
        :param plot_type: Type of plot, from the PLOT enum
        :param args: args for the plot
        :param kwargs: kwargs for the plot
        """
        self._renderer.add_plot(view, plot_type, *args, **kwargs)