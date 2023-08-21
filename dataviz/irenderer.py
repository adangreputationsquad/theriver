from abc import abstractmethod

from dash import Dash, html
import dash_bootstrap_components as dbc
from study.datastudy_interface import IDataStudy


class IDataStudyRenderer:
    """
    We use this class to render a data study in a dashboard
    the quick brown fox jumps over the lazy dog
    """

    def __init__(self, study: IDataStudy, title, desc):
        self._study = study
        self._app = Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.app.title = title
        self._desc = desc
        self._plots: dict[str, html.Div] = dict()
        self._next_id = -1

    @property
    def study(self):
        return self._study

    @property
    def app(self):
        return self._app

    @property
    def desc(self):
        return self._desc

    @property
    def plots(self):
        return self._plots

    @abstractmethod
    def next_id(self) -> str:
        pass
