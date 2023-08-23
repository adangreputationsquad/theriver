import json
from enum import Enum

import pdfkit
from dash import html, Input, Output, State, dash_table, ALL
from datafiles.views.view import View, DfView, DictView, ListView, PointView

from dataviz.irenderer import IDataStudyRenderer
from dataviz.pages.main_dashboard import drag_canvas
from dataviz.plot_types import PLOT, name_to_plot
import pandas as pd

from dataviz.src.components.iplot import IPlot

pd.set_option('display.float_format', '{:.4e}'.format)
DATA_PREVIEW_STYLE = {
    "white-space": "pre-wrap",
    "background-color": "beige",
    "border-radius": "10px",
    "padding": "10px",
}


class DataStudyRenderer(IDataStudyRenderer):
    """
    We use this class to render a data study in a dashboard
    the quick brown fox jumps over the lazy dog
    """

    def run(self, debug):
        self.app.layout = self.create_layout()
        self.app.run(debug=debug)

    def create_layout(self) -> html.Div:

        dc = drag_canvas(self)

        self.register_callbacks()

        return html.Div(
            className="app-div",
            children=dc,
        )

    def add_plot(self, view: View, plot_type: Enum, *args, **kwargs):
        plot_type: IPlot = plot_type.value
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
        next_id = self.next_id()
        self.plots[next_id] = plot_type.new(next_id, self, view,
                                            *args, **kwargs)

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
                        data=selected_view.data.head(10).applymap(
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
                    style=DATA_PREVIEW_STYLE,
                )
                print(selected_view)
            elif isinstance(selected_view, ListView):
                display = html.Div(
                    html.Code(
                        f"{selected_view.data}",
                        lang="python"
                    ),
                    style=DATA_PREVIEW_STYLE,
                )
                print(selected_view)
            elif isinstance(selected_view, DictView):

                display = html.Div(
                    html.Code(
                        f"{json.dumps(selected_view.data, indent=4)}",
                        lang="python"
                    ),
                    style=DATA_PREVIEW_STYLE,
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
             Input("validate_add_plot", "n_clicks")],
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
             Input("select_view_dropdown", "value"),
             Input("plot_args_div", "children"), ],
            [State("select_plot_dropdown", "value")],
        )
        def _plot_args_callback(plot_name, value_view, plot_args_div_children,
                                select_plot_state):
            from dataviz.pages.add_plot_modal import plot_args_div_callback
            selected_view = self.study.views.get(value_view)
            return plot_args_div_callback(plot_name, selected_view,
                                          plot_args_div_children,
                                          select_plot_state)

        @self.app.callback(
            Output("validate_add_plot", "style"),
            [Input({"type": "add_plot_arg", "index": ALL}, "value"),
             Input("select_plot_dropdown", "value"),
             Input("select_view_dropdown", "value"),
             Input("validate_add_plot", "style"),
             ]
        )
        def update_validate_add_plot(values, selected_plot, selected_view,
                                     style) -> dict:
            if style is None:
                style = {}
            style.update({"display": "None"})
            if selected_view is None or selected_plot is None:
                return style
            selected_view = self.study.views.get(selected_view)
            selected_plot = name_to_plot(selected_plot)

            if selected_plot.are_plot_args_valid(values, selected_view):
                style.update({"display": "block"})
            return style
