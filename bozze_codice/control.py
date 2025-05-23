# gestione collegamento view-model --> callbacks etc.from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from flask_login import login_user, logout_user, current_user
import dash
import model
import view


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
    def check_login_account(n_clicks, username, password_dal_form):    # molta della logica è scritta qui nel control.py, ma volendo la si può spostare nel model
        if n_clicks is None or n_clicks == 0:
            return dash.no_update, dash.no_update
        
        if not username or not password_dal_form:
            return dash.no_update, dbc.Alert('Devi compilare tutti i campi!', color='danger')
        
        user = model.get_by_username(username)  

        if user:        # è un oggetto Persona
            # controlliamo la password.
            # se la password va bene, chiamo login_user()
            valid = model.check_password(user.username, password_dal_form)  # qui andrà passata la hash della pw. Conviene metterla in una variabile prima.

            if valid:
                # Questa roba è orribile perchè metto nell'oggetto la password in chiaro...
                # nella pratica all'oggetto Persona andrà messa la password_hash invece della password in chiaro + tutto il resto degli attributi.
                login_user(user)    # loggo l'utente con flask
                return "/home", dbc.Alert("Login effettuato!", color= "success")
            else:
                return dash.no_update, dbc.Alert("Password sbagliata!", color= "danger")

        else:
            return dash.no_update, dbc.Alert("Username inesistente", color= "danger")
    
    
    @app.callback(
        Output("registration-feedback", "children"),
        Output("registration-feedback", "color"),
        Output("registration-feedback", "is_open"),
        Output("generated-username", "children"),
        Input("registration-input", "n_clicks"),
        State("radio-user", "value"),
        State("name-input", "value"),
        State("surname-input", "value"),
        State("codiceFiscale-input", "value"),
        State("dataNascita-input", "value"),
        State("radio-sesso", "value"),
        State("tel-input", "value"),
        State("email-input", "value"),
        State("indirizzo-input", "value"),
        State("city-input", "value"),
        State("CAP-input", "value"),
        State("scelta-password", "value"),
        State("conferma-password", "value"),
        prevent_initial_call='initial_duplicate'
    )
    def richiesta_account(n_clicks,user,nome,cognome,cf,datanascita,sesso,tel,email,indirizzo,citta,cap,pw,conf_pw):
        if n_clicks > 0:

            if not nome or not cognome or not cf or not datanascita or not sesso or not tel or not email or not indirizzo or not citta or not cap or not pw or not conf_pw:
                return "Inserisci tutti i campi!", "danger", True, None

            if pw != conf_pw:
                return "Password errata!", "danger", True, None
            
            if user=='P':
                model.inserisci_richiesta(nome,cognome,datanascita,sesso,cf,indirizzo,citta,cap,tel,email,True,pw)
                model.cur.execute("SELECT id_richiesta FROM RichiesteAccount WHERE codice_fiscale = %s ",(cf,))
                id_richiesta=model.cur.fetchone()
                return "Registrazione avvenuta con successo! attendi la verifica dei dati", "success", True, model.Admin.genera_username(id_richiesta)
            else:
                model.inserisci_richiesta(nome,cognome,datanascita,sesso,cf,indirizzo,citta,cap,tel,email,False,pw)
                model.cur.execute("SELECT id_richiesta FROM RichiesteAccount WHERE codice_fiscale = %s ",(cf,))
                id_richiesta=model.cur.fetchone()
                return "Registrazione avvenuta con successo! attendi la verifica dei dati", "success", True, model.Admin.genera_username(id_richiesta)
        else:
            return None,None,None,None
        

    @app.callback(
        Output("form1", "style"),
        Output("form2", "style"),
        Output("form3", "style"),
        Output("prev-button", "disabled"),
        Output("prev-button", "style"),
        Output("form-step", "data"),    # aggiorno lo stato delle freccette nel "dcc.Store" in "registration_layout()"
        Input("next-button", "n_clicks"),
        Input("prev-button", "n_clicks"),
        State("form1", "style"),
        State("form2", "style"),
        State("form3", "style"),
        State("form-step", "data"),     # controlla lo stato delle freccette del form nell'elemento "dcc.Store()" nella return della "registration_layout()"
        prevent_initial_call=True
    )
    def aggiorna_form(next_clicks, prev_clicks, s1, s2, s3, step):      # aggiunto "step"
        ctx = dash.callback_context.triggered_id # variabile che mantiene il 'contesto' dice quale bottone è stato triggerato

        if ctx == "next-button":
            if s1["display"] == "block":
                return {"display": "none"}, {"display": "block"}, {"display": "none"}, False, {"display": "block"}, 2
            elif s2["display"] == "block":
                return {"display": "none"}, {"display": "none"}, {"display": "block"}, False, {"display": "block"}, 3
            
        elif ctx == "prev-button":
            if s3["display"] == "block":
                return {"display": "none"}, {"display": "block"}, {"display": "none"}, False, {"display": "block"}, 2
            elif s2["display"] == "block":
                return {"display": "block"}, {"display": "none"}, {"display": "none"}, True, {"visibility": "hidden"}, 1

        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update


    # callback per il routing, cambia il contenuto della pagina a seconda dell'url
    @app.callback(
        [Output("contenuto-pagina", "children"),
        Output("url", "pathname", allow_duplicate=True)],
        Input("url", "pathname"), prevent_initial_call=True
    )
    def mostra_pagina(pathname):
        if pathname == "/logout" and current_user.is_authenticated:
            logout_user()  # Log the user out using Flask-Login
            return view.login_layout(), "/login"  # da cambiare quando avremo fatto la navbar
            # Display game page (only for authenticated users)
        # Display login page
        if pathname == "/login": # and not current_user.is_authenticated:
            return view.login_layout(), dash.no_update
        # Display registration page
        if pathname == "/register":
            return view.registration_layout(), dash.no_update
        if pathname == "/home":
            return html.H1("Hai effettuato l'accesso, sei nella Home."), dash.no_update   # qui va messa la home_layout()
        
        # qua ci va la pagina che vogliamo mostrare di default (home + navbar di solito)
        return view.login_layout(), dash.no_update  