from abc import ABC, abstractmethod
from dash import html


class AddPlotPanel(ABC):

    @abstractmethod
    def render(self) -> html.Div:
        pass
