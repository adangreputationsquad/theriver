from dash import html
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
from dataviz.src.components.iplot import IPlot


class PointNameValue(IPlot):
    _name = "point name/value"

    @classmethod
    def name(cls) -> str:
        return cls._name

    @staticmethod
    def config_panel(selected_view: View) -> Component:
        pass

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        pass

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):
        pass

    @staticmethod
    def new(plot_id: str,
            renderer: IDataStudyRenderer, source: View, *args, **kwargs):
        plot_name = kwargs.get("plot_name", source.name)

        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                html.Div(
                    [
                        html.Strong(source.name),
                        ": ",
                        source.data
                    ]
                )
            ]
        )
        return plot
