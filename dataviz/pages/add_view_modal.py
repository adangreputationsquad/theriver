from dash import html
import dash_bootstrap_components as dbc

from dataviz.irenderer import IDataStudyRenderer
from dash import dcc
from dataviz.assets.ids import IDAddViewModal as ID

horizontal_line = html.Hr(style={'borderWidth': "0.3vh", "width": "100%",
                                 "backgroundColor": "#B4E1FF",
                                 "opacity": "1"})


def modal_add_view(renderer: IDataStudyRenderer):
    return dbc.ModalBody(
        children=[dbc.Modal(
            [
                dbc.ModalHeader("Add view", style={"color": "#171F26"}),
                dbc.ModalBody(
                    id=ID.body,
                    children=[
                        dcc.Dropdown(
                            list(renderer.study.views.keys()),
                            id=ID.dropdown_views,
                            style={"araton": "black"},
                        ),
                        html.Div(id=ID.preview),
                        horizontal_line

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
