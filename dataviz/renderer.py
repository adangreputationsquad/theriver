import json

import pdfkit
from dash import Dash, html, Input, Output, State, dcc, dash_table
from datafiles.views.view import View, DfView, DictView, ListView, PointView
import dash_bootstrap_components as dbc

from dataviz.irenderer import IDataStudyRenderer
from dataviz.pages.main_dashboard import drag_canvas
from study.datastudy_interface import IDataStudy
from dataviz.plot_types import PLOT
import dash_draggable
import pandas as pd

pd.set_option('display.float_format', '{:.4e}'.format)


class DataStudyRenderer(IDataStudyRenderer):
    """
    We use this class to render a data study in a dashboard
    the quick brown fox jumps over the lazy dog
    """

    def run(self, debug):
        self.app.layout = self.create_layout()
        self.app.run(debug=debug)

    def create_layout(self) -> html.Div:

        self.register_callbacks()

        return html.Div(
            className="app-div",
            children=drag_canvas(self),
        )

    def add_plot(self, view: View, plot_type: PLOT, *args, **kwargs):
        from dataviz.src import components as cp

        for plot, view_type in [(PLOT.POINT, PointView),
                                (PLOT.LIST, ListView),
                                (PLOT.DICT, DictView),
                                (PLOT.DF, DfView)]:
            if (isinstance(plot_type, plot) and
                    not isinstance(view, view_type)):
                raise AssertionError(
                    f"plot_type does not match with view type "
                    f"{plot_type}, {view.__class__.__name__}"
                )

        match plot_type:
            case PLOT.POINT.NAME_VALUE:
                cp.point_name_value.add(
                    self, view,  # type: ignore
                    *args, **kwargs
                )
                return
            case PLOT.POINT.VALUE:
                cp.point_value.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DICT.ALL_VALUES | PLOT.LIST.ALL_VALUES:
                cp.all_values.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DICT.ALL_KEYS_VALUES:
                cp.all_keys_values.add(
                    self, view,  # type: ignore
                    *args, **kwargs
                )
                return
            case PLOT.DICT.TIMESERIES | PLOT.DF.TIMESERIES:
                cp.timeseries.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DF.SCATTER_PLOT:
                cp.scatter_plot.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DF.LINE_CHARTS:
                cp.line_charts.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DF.BAR_CHARTS:
                cp.bar_charts.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DF.PIE_CHARTS | PLOT.DICT.PIE_CHARTS:
                cp.pie_charts.add(self, view, *args, **kwargs)  # type: ignore
                return
            case PLOT.DF.BUBBLE_CHARTS:
                cp.bubble_charts.add(
                    self, view,  # type: ignore
                    *args, **kwargs
                )
                return
            case PLOT.DF.MAP | PLOT.DICT.MAP:
                cp.map.add(self, view, *args, **kwargs)  # type: ignore
                return

        raise NotImplementedError(plot_type)

    def next_id(self) -> str:
        self._next_id += 1
        return str(self._next_id)

    def register_callbacks(self):

        # Callback that makes the preview of the data selected
        @self.app.callback(
            Output("view_preview", "children"),
            [Input("select_view_dropdown", "value")]
        )
        def _view_preview_callback(value):
            if value is None:
                return []
            selected_view = self.study.views[value]
            if isinstance(selected_view, DfView):
                display = html.Div(
                    dash_table.DataTable(
                        id='table',
                        columns=[{"name": i, "id": i}
                                 for i in selected_view.data.columns],
                        data=selected_view.data.applymap(
                            lambda x: f"{x:.5e}" if isinstance(
                                x, float
                            ) else x
                        ).to_dict('records'),
                        style_cell=dict(textAlign='left'),
                        style_header=dict(
                            backgroundColor="paleturquoise",
                            color="black"
                        ),
                        style_data=dict(
                            backgroundColor="lavender",
                            color="black"
                        ),
                    ),

                )

                print(selected_view)
            elif isinstance(selected_view, PointView):
                display = html.Div(
                    html.Code(
                        f"{selected_view.data}",
                        lang="python"
                    ),
                    style={
                        "white-space": "pre-wrap",
                        "background-color": "beige",
                        "border-radius": "10px",
                        "padding": "10px",
                    },
                )
                print(selected_view)
            elif isinstance(selected_view, ListView):
                display = html.Div(
                    html.Code(
                        f"{selected_view.data}",
                        lang="python"
                    ),
                    style={
                        "white-space": "pre-wrap",
                        "background-color": "beige",
                        "border-radius": "10px",
                        "padding": "10px",
                    },
                )
                print(selected_view)
            elif isinstance(selected_view, DictView):

                display = html.Div(
                    html.Code(
                        f"{json.dumps(selected_view.data, indent=4)}",
                        lang="python"
                    ),
                    style={
                        "white-space": "pre-wrap",
                        "background-color": "beige",
                        "border-radius": "10px",
                        "padding": "10px",
                    },
                )
                print(selected_view)
            else:
                raise NotImplementedError()
            return display

        # Callback that hide or display the dropdown if a view is selected
        @self.app.callback(
            Output("select_plot_dropdown_div", "style"),
            [Input("select_view_dropdown", "value")]
        )
        def _select_plot_dropdown_callback_1(value):
            if value is None:
                return {"display": "none"}
            return {}

        # Callback that fills the dropdown with possible plots if a view is
        # selected
        @self.app.callback(
            Output("select_plot_dropdown", "options"),
            [Input("select_view_dropdown", "value")]
        )
        def _select_plot_dropdown_callback_2(value):
            if value is None:
                return []
            selected_view = self.study.views.get(value)
            return selected_view.get_plots()

        # Callback that hide or show the modal when we want to add a plot
        @self.app.callback(
            Output("modal", "is_open"),
            [Input("add_plot", "n_clicks"),
             Input("close", "n_clicks")],
            [State("modal", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

        # Callback that download the page when the download button is pressed
        @self.app.callback(
            Output("download", "style"),
            Input("download", "n_clicks"),
        )
        def _download(n):
            if n is not None:
                success = pdfkit.from_url(
                    "http://127.0.0.1:8050/", f'test.pdf'
                )
                print(success)
            return {}

        @self.app.callback(
            Output("plot_args_div", "children"),
            [Input("select_plot_dropdown", "value"),
             Input("select_view_dropdown", "value")]
        )
        def _plot_args_callback(value_plot, value_view):
            selected_view = self.study.views.get(value_view)
            print("WIP")
            print(value_plot)
            print(value_view)
            print(selected_view)
            raise NotImplementedError()