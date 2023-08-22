from dash import html
import dash_bootstrap_components as dbc
from dash.development.base_component import Component

from datafiles.views.view import View
from dataviz.irenderer import IDataStudyRenderer
from dash import dcc


def modal_add_plot(renderer: IDataStudyRenderer):
    print("rendering modal_add_plot")
    return dbc.ModalBody(
        children=[dbc.Modal(
            [
                dbc.ModalHeader("Add plot", style={"color": "#171F26"}),
                dbc.ModalBody(
                    id="modal_body_add_plot",
                    children=[
                        dcc.Dropdown(
                            list(renderer.study.views.keys()),
                            id="select_view_dropdown",
                            style={"araton": "black"},
                        ),
                        html.Div(id="view_preview"),
                        html.Div(
                            id="select_plot_dropdown_div",
                            children=[
                                dcc.Dropdown(
                                    [],
                                    id="select_plot_dropdown",
                                    style={"araton": "black"},
                                ),
                            ]
                        ),
                        html.Div(id="plot_args_div"),

                    ],
                    style={"height": "80vh"}
                ),
                dbc.ModalFooter([
                    dbc.Button(
                        "VALIDATE", id="validate_add_plot",
                        className="ml-auto",
                    )
                ]),
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


def plot_args_div_callback(plot_name, selected_view, plot_args_div_children,
                           select_plot_state) -> list[Component]:
    updated_config = []

    # If we don't have any plot selected or if we changed the plot, we must
    # update the plot args panel
    try:
        if ((not plot_args_div_children and plot_name) or
                (plot_name != select_plot_state)):
            updated_config = _update_plot_args_div(plot_name, selected_view)
    except NotImplementedError:
        print(len(updated_config))
    return updated_config


def _update_plot_args_div(plot_name, selected_view: View) -> list:
    match plot_name:
        case "timeseries":
            from dataviz.src.components.timeseries import Timeseries
            return Timeseries.config_panel(selected_view)
        case _:
            raise NotImplementedError()
        # return updated_config, apply_button_style
