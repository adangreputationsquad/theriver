import json

import pdfkit
from dash import Dash, html, Input, Output, State, dcc, dash_table
from datafiles.views.view import View, DfView, DictView, ListView, PointView
import dash_bootstrap_components as dbc
from study.datastudy_interface import IDataStudy
from dataviz.plot_types import PLOT
import dash_draggable
import pandas as pd

pd.set_option('display.float_format', '{:.4e}'.format)


class DataStudyRenderer:
    """
    We use this class to render a data study in a dashboard
    the quick brown fox jumps over the lazy dog
    """

    def __init__(self, study: IDataStudy, title, desc):
        self.study = study
        self.app = Dash(
            __name__,
            external_stylesheets=[dbc.themes.BOOTSTRAP]
        )
        self.app.title = title
        self.desc = desc
        self.plots: dict[str, html.Div] = dict()
        self._next_id = -1

    def run(self, debug):
        self.app.layout = self.create_layout()
        self.app.run(debug=debug)

    def create_layout(self) -> html.Div:

        modal_add_plot = dbc.ModalBody(
            children=[dbc.Modal(
                [
                    dbc.ModalHeader("Add plot", style={"color": "#171F26"}),
                    dbc.ModalBody(
                        id="modal_body_add_plot",
                        children=[
                            dcc.Dropdown(
                                list(self.study.views.keys()),
                                id="add_plot_dropdown",
                                style={"araton": "black"},
                            ),

                        ],
                        style={"height": "80vh"}
                    ),
                    dbc.ModalFooter(
                        dbc.Button(
                            "CLOSE BUTTON", id="close",
                            className="ml-auto"
                        )
                    ),
                ],
                id="modal",
                is_open=False,  # Open the modal at opening the webpage.
                backdrop=True,
                # Modal to not be closed by clicking on backdrop
                scrollable=True,
                # Scrollable in case of large amount of text
                centered=True,  # Vertically center modal
                keyboard=True,  # Close modal when escape is pressed
                fade=True,  # Let the modal fade instead of appear.

            ),
            ],
            style={
                "max-width": "none", "width": "90%",
                "max-height": "none", "height": "90%"
            },
        )

        drag_canvas = [
            html.H1(self.app.title),
            html.Div(
                children=[
                    html.P(self.desc),
                    dbc.Button(
                        "download", id="download",
                        style={"display": "inline-block"},
                        className="ml-auto"
                    ),
                    dbc.Button(
                        "add plot", id="add_plot",
                        style={"display": "inline-block"},
                        className="ml-auto"
                    ),
                ]
            ),

            html.Hr(),
            dash_draggable.GridLayout(
                className="draggable",
                id='draggable',
                children=list(self.plots.values()),
            ),
            html.Hr(),
            modal_add_plot
        ]

        # TODO Fuse the two callbacks, add the plot option for all the plot
        # refactor the code
        @self.app.callback(
            Output("modal_body_add_plot", "children", allow_duplicate=True),
            [Input("add_plot_dropdown", "value"),
             Input("modal_body_add_plot", "children")]
        )
        def _add_plot_1(value, children):
            if value is not None:
                view = self.study.views[value]
                if len(children) < 2:
                    children.append("")
                if isinstance(view, DfView):
                    display = html.Div(
                        dash_table.DataTable(
                            id='table',
                            columns=[{"name": i, "id": i}
                                     for i in view.data.columns],
                            data=view.data.applymap(
                                lambda x: f"{x:.5e}" if isinstance(x, float) else x
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

                    print(view)
                elif isinstance(view, PointView):
                    display = html.Div(html.Code(
                        f"{view.data}",
                        lang="python"),
                        style={
                            "white-space": "pre-wrap",
                            "background-color": "beige",
                            "border-radius": "10px",
                            "padding": "10px",
                        },
                    )
                    print(view)
                elif isinstance(view, ListView):
                    display = html.Div(html.Code(
                        f"{view.data}",
                        lang="python"),
                        style={
                            "white-space": "pre-wrap",
                            "background-color": "beige",
                            "border-radius": "10px",
                            "padding": "10px",
                        },
                    )
                    print(view)
                elif isinstance(view, DictView):
                    # display = dcc.Markdown(
                    #     f"```json\n"
                    #     f"{json.dumps(view.data, indent=4)}",
                    #
                    # )
                    display = html.Div(html.Code(
                        f"{json.dumps(view.data, indent=4)}",
                        lang="python"),
                        style={
                            "white-space": "pre-wrap",
                            "background-color": "beige",
                            "border-radius": "10px",
                            "padding": "10px",
                        },
                    )
                    print(view)
                else:
                    raise NotImplementedError()

                children[1] = display
                children[2] = html.Div(
                    children=[
                        dcc.Dropdown(
                            view.get_plots(),
                            id="add_plot_dropdown_2"
                        )
                    ]
                )
                return children
            else:
                return children

        @self.app.callback(
            Output("modal_body_add_plot", "children"),
            [Input("add_plot_dropdown_2", "value"),
            Input("add_plot_dropdown", "value"),
             Input("modal_body_add_plot", "children")]
        )
        def _add_plot_2(value_2, value, children):
            from dataviz.src.components import (timeseries)
            if len(children) < 3:
                children.append("")
            if value_2 is not None:
                match value_2:
                    case PLOT.DF.TIMESERIES | PLOT.DICT.TIMESERIES:
                        children[2] = timeseries.html_input(self.study.views[value])

                return children

        @self.app.callback(
            Output("modal", "is_open", allow_duplicate=True),
            [Input("add_plot", "n_clicks"), Input("close", "n_clicks")],
            [State("modal", "is_open")],
        )
        def toggle_modal(n1, n2, is_open):
            if n1 or n2:
                return not is_open
            return is_open

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

        return html.Div(
            className="app-div",
            children=drag_canvas,
        )

    def add_plot(self, view: View, plot_type: PLOT, *args, **kwargs):
        from .src import components as cp

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
