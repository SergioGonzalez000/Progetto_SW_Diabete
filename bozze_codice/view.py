from dash import dcc, html
import dash_bootstrap_components as dbc

def getLayout():
    return dbc.Container(
        [
            html.H1(
                "Welcome Nigga", 
                className="text-center my-4"),
            html.P(
                "In cosa ti identifichi coglionazzo?", 
                className="text-center"),
            html.Div(
                dbc.ButtonGroup([
                    dbc.Button("Paziente", color="primary"), 
                    dbc.Button("Diabetologo", color="danger")],
                    size="md",
                    className="mt-4",
                    vertical=True),
                className="d-flex justify-content-center" 
            ),
            dbc.Button(
                "Accedi", 
                href="/login", 
                color="secondary", 
                className="d-block mx-auto mt-3")
        ],
        fluid=True,
        className="p-4"
    )
