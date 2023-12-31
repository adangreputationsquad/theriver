from dash import html
import dash_bootstrap_components as dbc
from dash.development.base_component import Component

from dataviz.irenderer import IDataStudyRenderer
from dash import dcc

from dataviz.plot_types import name_to_plot

from dataviz.assets.ids import IDAddPlotModal as ID

horizontal_line = html.Hr(style={'borderWidth': "0.3vh", "width": "100%",
                                 "backgroundColor": "#B4E1FF",
                                 "opacity": "1"})


def modal_add_plot(renderer: IDataStudyRenderer):
    print("rendering modal_add_plot")
    return dbc.ModalBody(
        children=[dbc.Modal(
            [
                dbc.ModalHeader("Add plot", style={"color": "#171F26"}),
                dbc.ModalBody(
                    id=ID.body,
                    children=[
                        dcc.Dropdown(
                            list(renderer.study.views.keys()),
                            id=ID.dropdown_views,
                            style={"araton": "black"},
                        ),
                        html.Div(id=ID.preview),
                        horizontal_line,
                        html.Div(
                            id=ID.dropdown_plots_div,
                            children=[
                                dcc.Dropdown(
                                    [],
                                    id=ID.dropdown_plots,
                                    style={"araton": "black"},
                                ),
                            ]
                        ),
                        html.Div(id=ID.config_panel_div),

                    ],
                    style={"height": "80vh"}
                ),
                dbc.ModalFooter([
                    dbc.Button(
                        "VALIDATE", id=ID.validate_button,
                        className="ml-auto",
                    )
                ]),
            ],
            id=ID.id,
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
            # Config panel given by the plot type
            updated_config = name_to_plot(plot_name).config_panel(selected_view)
    except NotImplementedError:
        print(len(updated_config))
    return updated_config
