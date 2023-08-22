from abc import ABC, abstractmethod

from dash import html, dcc
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer


class IPlot(ABC):
    _name = None

    @staticmethod
    @abstractmethod
    def new(plot_id: str,
            renderer: IDataStudyRenderer,
            source: View,
            *args, **kwargs) -> list[Component]:
        pass

    @staticmethod
    @abstractmethod
    def config_panel(selected_view: View) -> list[Component]:
        pass

    @staticmethod
    @abstractmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        pass

    @staticmethod
    @abstractmethod
    def from_config(next_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        pass

    @classmethod
    @abstractmethod
    def name(cls) -> str:
        pass

    @staticmethod
    def get_close_button(plot_id):
        return

    @staticmethod
    def get_header(plot_id, name):
        return [
            html.Thead(name,
                       style={'display': 'inline-block'}),
            html.Button(
                "X", id={"type": "close_plot", "index": plot_id}, style={
                    'display': 'inline-block', "float": 'right'
                }
            )
        ]

    @staticmethod
    def get_html(plot_id, plot_name, source, graph):
        html.Div(
            className="plot",
            children=[
                html.Div(
                    children=[
                        html.Thead(plot_name,
                                   style={'display': 'inline-block'}),
                        html.Button(
                            "X",
                            id={"type": "close_plot", "index": plot_id},
                            style={
                                'display': 'inline-block', "float": 'right'
                            }
                        )
                    ]
                ),
                graph,
            ]
        )
