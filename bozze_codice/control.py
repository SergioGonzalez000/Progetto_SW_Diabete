# gestione collegamento view-model --> callbacks etc.from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash 
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
            valid = check_password_hash(user.pw, password_dal_form)  # ho eliminato la fx check_password mia, nel model.py

            if valid:
                # Questa roba è orribile perchè metto nell'oggetto la password in chiaro...
                # nella pratica all'oggetto Persona andrà messa la password_hash invece della password in chiaro + tutto il resto degli attributi.
                login_user(user)    # loggo l'utente con flask
                return "/home", dbc.Alert("Login effettuato!", color= "success")
            else:
                return dash.no_update, dbc.Alert("Password sbagliata!", color= "danger")

        else:
            return dash.no_update, dbc.Alert("Username inesistente", color= "danger")
    
    
    # ******************************************************************************************************************

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
        
    # ******************************************************************************************************************

    @app.callback(
        Output("form1", "style"),
        Output("form2", "style"),
        Output("form3", "style"),
        Output("prev-button", "disabled"),
        Output("prev-button", "style"),
        Output("next-button", "disabled"), #fil - aggiunta anche di next-button per nasconderlo al 3 form
        Output("next-button", "style"),
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
                return {"display": "none"}, {"display": "block"}, {"display": "none"}, False, {"display": "block"},False, {"display": "block"}, 2
            elif s2["display"] == "block":
                return {"display": "none"}, {"display": "none"}, {"display": "block"}, False, {"display": "block"},True, {"visibility": "hidden"}, 3
            
        elif ctx == "prev-button":
            if s3["display"] == "block":
                return {"display": "none"}, {"display": "block"}, {"display": "none"}, False, {"display": "block"},False, {"display": "block"}, 2
            elif s2["display"] == "block":
                return {"display": "block"}, {"display": "none"}, {"display": "none"}, True, {"visibility": "hidden"},False, {"display": "block"}, 1

        return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update

    # ******************************************************************************************************************

    # callback per il routing, cambia il contenuto della pagina a seconda dell'url
    # Problema nella gestione della logica del routing:
    #   Se da barra dell'indirizzo si digita "/home" o qualsiasi altro indirizzo, lo mostra senza controllare
    #   se l'utente è autenticato o meno.
    @app.callback(
        [Output("contenuto-pagina", "children"),
        Output("url", "pathname", allow_duplicate=True)],
        Input("url", "pathname"), prevent_initial_call=True
    )
    def mostra_pagina(pathname):
        # Se l'utente non è autenticato e prova ad accedere a una pagina protetta,
        # viene reindirizzato sul login. (magari in futuro avremo una navbar per i guests, che verrà personalizzata
        # per i diabetologi e i pazienti)
        if not current_user.is_authenticated and pathname not in ["/login", "/register"]:
            return view.login_layout(), "/login"
        
        # se (da utenti autenticati) si prova a scrivere "/login" o "/register" nella barra degli indirizzi,
        # si torna diretti alla home (in futuro sarà una home caruccia con navbar etc)
        if current_user.is_authenticated and pathname in ["/login", "/register"]:
            return view.home_layout(), "/home"
        
        # per fare logout
        if pathname == "/logout" and current_user.is_authenticated:
            logout_user()
            return view.login_layout(), "/login"
        
        # pagina di login, accessibile solo se l'utente non è autenticato
        if pathname == "/login" and not current_user.is_authenticated:
            return view.login_layout(), dash.no_update
        
        # pagina di registrazione, solo se l'utente non è autenticato
        if pathname == "/register" and not current_user.is_authenticated:
            return view.registration_layout(), dash.no_update
        
        # home, solo se l'utente è autenticato
        if pathname == "/home" and current_user.is_authenticated and isinstance(current_user, model.Admin):
            return view.home_layout(), dash.no_update
        
        # per reidirizzare alla pagina dell'Admin. Controllo che l'utente 
        # sia istanza della classe Admin. 
        # Bisogna implementare sta roba anche per gli altri due tipi di utente.
        if pathname == "/admin" and isinstance(current_user, model.Admin):
            return view.admin_layout(), dash.no_update
        
        # IMPORTANTE
        # altrimenti si potrebbe pensare un gateway? una specie di pagina intermedia in cui 
        # si viene mandati dopo il login, in cui si mettono i controlli di routing "isinstance()"
        # in modo da non doverli ripetere. Il login di defaulti mi porta su "/gateway" e
        # da li se sono paziente vado su /paziente , ... etc. 

        # in tutti gli altri casi, just in case...
        # se l'utente è autenticato --> home
        # se non è autenticato --> login
        if current_user.is_authenticated:
            return view.home_layout(), "/home"
        else:
            return view.login_layout(), "/login"
        

    # ******************************************************************************************************************

    # Callback per l'apertura del menu a tendina (profile_offcanvas)

    @app.callback(
        Output("profile-offcanvas", "is_open"),
        Input("open-offcanvas", "n_clicks"),
        [State("profile-offcanvas", "is_open")],
    )
    def toggle_offcanvas(n1, is_open):
        if n1:
            return not is_open
        return is_open

     # ******************************************************************************************************************