from dash import Dash, html

from datafiles.views.view import View, DfView
from dataviz.plot_types import PLOT


class DataStudyRenderer:
    """
    We use this class to render a data study in a dashboard
    """
    def __init__(self, title, desc):
        self.app = Dash(external_stylesheets=["assets/style.css"])
        self.app.title = title
        self.desc = desc
        self.plots: list[html.Div] = []

    def run(self):
        self.app.layout = self.create_layout()
        self.app.run()

    def create_layout(self) -> html.Div:

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

    def add_plot(self, view: View, plot_type: PLOT, *args, **kwargs):
        from .src import components as cp
        from datafiles.views.view import PointView, ListView, DictView

        for plot, view_type in [(PLOT.POINT, PointView),
                                (PLOT.LIST, ListView),
                                (PLOT.DICT, DictView),
                                (PLOT.DF, DfView)]:
            if (isinstance(plot_type, plot) and
                    not isinstance(view, view_type)):
                raise AssertionError(
                    f"plot_type does not match with view type"
                    f"{plot_type}, {view.__class__.__name__}"
                )

        match plot_type:
            case PLOT.POINT.NAME_VALUE:
                cp.point_name_value.add(self, view,  # type: ignore
                                        *args, **kwargs)
                return
            case PLOT.POINT.VALUE:
                cp.point_value.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DICT.ALL_VALUES | PLOT.LIST.ALL_VALUES:
                cp.all_values.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DICT.ALL_KEYS_VALUES:
                cp.all_keys_values.add(self, view,  # type: ignore
                                       *args, **kwargs)
                return
            case PLOT.DICT.TIMESERIES | PLOT.DF.TIMESERIES:
                cp.timeseries.add(self, view, *args, **kwargs)  # type: ignore
                return

        raise NotImplementedError(plot_type)
