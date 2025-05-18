from dash import dcc, html
import dash_bootstrap_components as dbc

def getLayout():
    return dbc.Container(
        [
            html.H1(
                "卐 Welcome Nigga 卐", 
                className="text-center my-4"),
            html.P(
                "卐 In cosa ti identifichi coglionazzo? 卐", 
                className="text-center"),
            html.Div(
                dbc.ButtonGroup([
                    dbc.Button("Paziente",id="btn_paz",href="/login_paz", color="primary"), 
                    dbc.Button("Diabetologo",id="btn_doc",href="/login_doc", color="danger")],
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
