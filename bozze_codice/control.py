# gestione collegamento view-model --> callbacks etc.
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dcc
import dash
from model import check_username_pw
from view import login_layout


def registra_callbacks(app):
    '''registro le callback dell'app'''

    @app.callback(
        [Output('url', 'pathname'),
         Output('output-box', 'children')],
        [Input('login-input', 'n_clicks'),
         State('username-input', 'value'),
         State('password-input', 'value')],
         prevent_initial_call=True
    )
    def check_login_account(n_clicks, username, password):    
        if n_clicks is None or n_clicks == 0:
            return dash.no_update, dash.no_update
        
        if not username or not password:
            return dash.no_update, dbc.Alert('devi compilare tutti i campi!', color='danger')
        
        return check_username_pw(username, password)
    

    @app.callback(
        Output("contenuto-pagina", "children"),
        Input("url", "pathname")
    )
    def mostra_pagina(pathname):
        if pathname == "/home":
            return html.H1("Hai effettuato l'accesso, sei nella Home.")    
        return login_layout()