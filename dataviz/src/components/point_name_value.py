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
    def config_panel(selected_view: View) -> list[Component]:
        return IPlot.html_input("Name", 0, input_type="text",
                                placeholder=selected_view.name)

    @staticmethod
    def are_plot_args_valid(plot_args: list, selected_view: View) -> bool:
        return True

    @staticmethod
    def from_config(plot_id: str, renderer: IDataStudyRenderer, plot_args: list,
                    selected_view: View):

        return PointNameValue.new(
            plot_id, renderer, selected_view,
            name=plot_args[0] if plot_args[0] else selected_view.name)

    @staticmethod
    def new(plot_id: str,
            renderer: IDataStudyRenderer, source: View, *args, **kwargs):
        plot_name = kwargs.get("plot_name", source.name)
        name = kwargs.get("name", source.name)

        plot = html.Div(
            className="plot",
            children=[
                html.Div(
                    children=IPlot.get_header(plot_id, plot_name)
                ),
                html.Div(
                    [
                        html.Strong(name),
                        ": ",
                        source.data
                    ]
                )
            ]
        )
        return plot
