from dash import Dash, html

from study.views.view import View
from dataviz.plot_types import PLOT

class DataStudyRenderer:

    def __init__(self, title, desc):
        self.app = Dash(external_stylesheets=["assets/style.css"])
        self.app.title = title
        self.desc = desc
        self.plots: list[html.Div] = []

    def run(self):
        self.app.layout = self.create_layout()
        self.app.run()

    def create_layout(self) -> html.Div:
        from .src.components import point_name_value

        children = [
            html.H1(self.app.title),
            html.Hr(),
        ]

        for plot in self.plots:
            children.append(plot)

        return html.Div(
            className="app-div",
            children=children,
        )

    def add_plot(self, view: View, plot_type: PLOT):
        from .src.components import point_name_value, point_value
        from study.views.view import PointView, ListView, DictionaryView
        # TODO check plot type match with view

        match plot_type:
            case PLOT.POINT.NAME_VALUE:
                point_name_value.add(self, view)
                return
            case PLOT.POINT.VALUE:
                point_value.add(self, view)
                return
        raise NotImplementedError()
