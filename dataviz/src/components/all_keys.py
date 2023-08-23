from dash import html
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
from dataviz.src.components.iplot import IPlot


class AllKeys(IPlot):
    _name = "all keys"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def new(plot_id: str, renderer: IDataStudyRenderer, source: View, *args,
            **kwargs) -> Component:
        plot_name = kwargs.get("plot_name", source.name)
        if isinstance(source.data, list):
            data = source.data
        elif isinstance(source.data, dict):
            data = list(source.data.keys())
        else:
            raise AssertionError()

        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                html.Div([str(data)], className="plot")
            ]
        )

        return plot

    @staticmethod
    def config_panel(selected_view: View) -> list[Component]:
        return []

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        return True

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        return AllKeys.new(plot_id, renderer, selected_view)
