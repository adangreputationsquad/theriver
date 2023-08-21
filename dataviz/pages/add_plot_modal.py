from dash import html
import dash_bootstrap_components as dbc
from dataviz.irenderer import IDataStudyRenderer
from dash import dcc


def modal_add_plot(renderer: IDataStudyRenderer):
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
                        # TODO: Add generic panel to configurate new plot

                    ],
                    style={"height": "80vh"}
                ),
                dbc.ModalFooter([
                    dbc.Button(
                        "CLOSE BUTTON", id="close",
                        className="ml-auto"
                    ),
                    dbc.Button(
                        "VALIDATE", id="validate_add_plot",
                        className="ml-auto"
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
