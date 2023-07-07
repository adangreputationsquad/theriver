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
        from .src import components as cp
        from study.views.view import PointView, ListView, DictionaryView

        for plot, view_type in [(PLOT.POINT, PointView),
                                (PLOT.LIST, ListView),
                                (PLOT.DICT, DictionaryView)]:
            if (isinstance(plot_type, plot) and
                    not isinstance(view, view_type)):
                raise AssertionError(
                    f"plot_type does not match with view type"
                    f"{plot_type}, {view.__class__.__name__}"
                )

        match plot_type:
            case PLOT.POINT.NAME_VALUE:
                cp.point_name_value.add(self, view)
                return
            case PLOT.POINT.VALUE:
                cp.point_value.add(self, view)
                return
            case PLOT.DICT.ALL_VALUES | PLOT.LIST.ALL_VALUES:
                cp.all_values.add(self, view)
                return

        raise NotImplementedError()
