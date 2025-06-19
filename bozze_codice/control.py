import json
import dash_bootstrap_components as dbc
from dash import html, dcc, Input, Output, State, ALL, ctx
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash 
import dash
import model
import view

import plotly.express as px
import plotly.graph_objects as go


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

            # 
            #   **modificata questa roba, dovrebbe andare**
            #
            if valid:
                login_user(user)

                if current_user.is_authenticated and isinstance(user, model.Paziente):
                    return "/patient-dashboard", dbc.Alert("Login effettuato!", color="success")
                elif current_user.is_authenticated and isinstance(user, model.Diabetologo):
                    return "/doctor-dashboard", dbc.Alert("Login effettuato!", color="success")
                elif current_user.is_authenticated and isinstance(user, model.Admin):
                    return "/admin-dashboard", dbc.Alert("Login effettuato!", color="success")
                else:
                    return dash.no_update, dbc.Alert("Credenziali sbagliate!", color="danger")
            else:
                    return dash.no_update, dbc.Alert("Credenziali sbagliate!", color="danger")      # nel caso in cui password non sia valid
            
        else: 
            return dash.no_update, dbc.Alert("Credenziali sbagliate!", color="danger")              # nel caso in cui la query di get_by_username() non abbia trovato un User.


        #     if valid:
        #         # Questa roba è orribile perchè metto nell'oggetto la password in chiaro...
        #         # nella pratica all'oggetto Persona andrà messa la password_hash invece della password in chiaro + tutto il resto degli attributi.
        #         login_user(user)    # loggo l'utente con flask
        #         return "/redirect", dbc.Alert("Login effettuato!", color= "success")
        #     else:
        #         return dash.no_update, dbc.Alert("Password sbagliata!", color= "danger")

        # else:
        #     return dash.no_update, dbc.Alert("Username inesistente", color= "danger")
    
    
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
        prevent_initial_call=True
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
    # CALLBACK ROUTING CON NAVBAR
    # !!!!! DA CONTROLLARE !!!!!
    # Deve: 
    # 1. cambiare i navlinks nella sidebar se ospite, paziente, medico, admin
    # 2. cambiare "page-content" in base all'url
    # 3. cambiare url
    # NB: quando un utente accede, la callback entra nell' "else" corrrispondente
    @app.callback(
        [
            # 1: Modifico i navlinks
            Output("navlinks", "children"),
            # 2: Modifico il contenuto della pagina
            Output("page-content", "children"),
            # 3: Modifico l'url
            Output("url", "pathname", allow_duplicate=True),
        ],
        # Prendo in input il pathname
        Input("url", "pathname"), prevent_initial_call=True
    )
    def routing(pathname):

        # Caso GUEST - NON AUTENTICATI
        if not current_user.is_authenticated:

            # Accesso alla home
            if pathname == "/":
                return view.guest_navlinks, view.home, "/"
            # Accesso al login
            elif pathname == "/login":
                return view.guest_navlinks, view.login_layout(), "/login"
            # Accesso alla registrazione
            elif pathname == "/registration":
                return view.guest_navlinks, view.registration_layout(), "/registration"
            # Se il guest cerca di accedere ad una pagina protetta, reindirizza alla home
            return view.guest_navlinks, html.H2("Accesso non autorizzato"), "/"
        
        # Caso UTENTI - AUTENTICATI
        
        # PAZIENTE
        elif isinstance(current_user, model.Paziente):
            # Se paziente nella dashboard
            if pathname == "/patient-dashboard":
                return view.patient_navlinks, view.patient_dashboard, "/patient-dashboard"
            # Se paziente nella pagina grafici
            elif pathname == "/grafici":
                return view.patient_navlinks, view.patient_graphs, "/grafici"
            # Se paziente nella chat
            elif pathname == "/chat":
                return view.patient_navlinks, view.chat_content, "/chat"
            # Effettua il logout
            elif pathname == "/logout":
                logout_user()
                return view.guest_navlinks, dash.no_update, "/login"
            # Tenta di accedere a pagina protetta:
            else:
                return view.patient_navlinks, view.patient_dashboard, "/patient-dashboard"
    
        # DIABETOLOGO
        elif isinstance(current_user, model.Diabetologo):
            # Se diabetologo nella dashboard
            if pathname == "/doctor-dashboard":
                return view.doctor_navlinks,view.doctor_dashboard, "/doctor-dashboard"
            # Se diabetologo nella pagina grafici
            elif pathname == "/doctor-patient":
                return view.doctor_navlinks,  view.doctor_patient, "/doctor-patient"
            # Se diabetologo nella chat
            elif pathname == "/chat":
                return view.doctor_navlinks, view.chat_content, "/chat"
            # Effettua il logout
            elif pathname == "/logout":
                logout_user()
                return view.guest_navlinks, dash.no_update, "/login"
            # Tenta di accedere a pagina protetta:
            else:
                return view.doctor_navlinks, view.doctor_dashboard, "/doctor-dashboard"
    
        # ADMIN
        elif isinstance(current_user, model.Admin):
            # Se admin nella dashboard
            if pathname == "/admin-dashboard":
                return view.admin_navlinks, view.admin_dashboard, "/admin-dashboard"
            # Se admin nella lista delle richieste
            elif pathname == "/request":
                return view.admin_navlinks, view.admin_request, "/request"
            # Se admin nella lista dei pazienti
            elif pathname == "/admin-patient":
                return view.admin_navlinks, view.admin_patient, "/admin-patient"
            # Se admin nella lista dei diabetologi
            elif pathname == "/admin-doctor":
                return view.admin_navlinks, view.admin_doctor, "/admin-doctor"
            # Logout dell'admin
            elif pathname == "/logout":
                logout_user()
                return view.guest_navlinks, dash.no_update, "/login"
            # Tenta di accedere a pagina protetta:
            else:
                return view.admin_navlinks, view.admin_dashboard, "/admin-dashboard"

        # Caso pagina inesistente
        else:
            return dash.no_update, html.H2("404 - Page not found"), "/404"

# ******************************************************************************************************************
    
    #permette di vedere i grafici paziente per paziente al diabetologo
    @app.callback(
        Output("dropdown-output","children"),
        Input("dropdown-pazienti","value"),
    )
    def visualizza_grafico_paziente(paziente):
        if not paziente:
            return "Seleziona un paziente per visualizzare il grafico."
    
        fig = model.Diabetologo.visualizza_glicemia_paziente(paziente)
        return dcc.Graph(figure=fig)
    

    # ************************
    # callback del dropdown della richiesta admin
    @app.callback(
        Output("contenitore-informazioni-richiesta", "children"),
        Input("dropdown-selezione-richiesta-account", "value"),
    )
    def mostra_dettagli_richiesta(id_richiesta):
        if not id_richiesta:
            return dbc.Alert("Seleziona una richiesta per vedere i dettagli.", color="secondary")

        dati = model.get_dati_richiesta_account_by_id(id_richiesta)
        if not dati:
            return dbc.Alert("Non ci sono dati", color="danger")

        # crea lista di paragrafi con i dati
        return view.render_dati_richiesta(dati)
    
    # **********************
    # callback dei bottoni nella pagina delle richieste, dell'admin.
    @app.callback(
        [Output("contenitore-informazioni-richiesta", "children", allow_duplicate=True),  # aggiorna magari con un messaggio di conferma
        Output("dropdown-selezione-richiesta-account", "options")],
        [Input("btn-accetta-richiesta", "n_clicks"),
        Input("btn-rifiuta-richiesta", "n_clicks")],
        State("dropdown-selezione-richiesta-account", "value"),
        prevent_initial_call=True,
        allow_duplicate=True
    )
    def gestisci_richiesta_accetta_o_rifiuta(n_clicks_accetta, n_clicks_rifiuta, id_richiesta):
        ctx = dash.callback_context

        # controlla se è stato effettivamente premuto un bottone
        if not ctx.triggered:
            return dash.no_update, dash.no_update

        bottone_premuto = ctx.triggered[0]["prop_id"].split(".")[0]

        # nessuna richiesta selezionata
        if not id_richiesta:
            # ritorna un Alert in caso di azione a vuoto
            return dbc.Alert("Seleziona una richiesta prima di accettare o rifiutare.", color="warning", dismissable=True), dash.no_update

        # azioni da compiere in base al bottone premuto
        if bottone_premuto == "btn-accetta-richiesta":
            # funzione per accettare la richiesta
            model.Admin.approva_richiesta(id_richiesta)     # gia definita
            alert = dbc.Alert(f"Richiesta {id_richiesta} accettata con successo.", color="success", dismissable=True)

        elif bottone_premuto == "btn-rifiuta-richiesta":
            # chiamo la funzione che gestisce il rifiuto
            model.rifiuta_richiesta(id_richiesta)                 # da fare
            alert = dbc.Alert(f"Richiesta {id_richiesta} rifiutata con successo.", color="danger", dismissable=True)
            
        else:
            return dash.no_update, dash.no_update

        # aggiorna il dropdown con le richieste rimanenti
        richieste = model.get_all_richieste_account()                             # deve restituire lista di tuple/dict
        options = [{"label": f"{r[1]}", "value": r[0]} for r in richieste]

        return alert, options
        
       
# ******************************************************************************************************************
    @app.callback(
        Output("doctor-patient-queue", "children"),
        Input("url","pathname")
    )
    def aggiorna_lista_pazienti(path):
        if path=="/doctor-dashboard" or path=='/doctor-patient':
            id=current_user.get_id_diabetologo()
            pazienti_con_media=model.Diabetologo.visualizza_pazienti_associati(id)
            elementi = []
            for username, media in pazienti_con_media:
                paz_id = model.get_id_paziente_by_username(username)
            
                if media is None:
                    colore = "#aaa"  # Grigio se non ci sono dati
                elif media < 70 or media > 180:
                    colore = "#FF4C4C"  # Rosso
                elif 130 <= media <= 180:
                    colore = "#FFD93B"  # Giallo
                else:
                    colore = "#08ff46"  # Verde

                bollino = html.Span(
                    style={
                        "display": "inline-block",
                        "width": "10px",
                        "height": "10px",
                        "borderRadius": "50%",
                        "backgroundColor": colore,
                        "marginRight": "10px"
                    }
                )

                elementi.append(
                    html.Div(
                        html.Div(
                            style={
                                "display": "flex",
                                "justifyContent": "space-between",
                                "alignItems": "center"
                            },
                            children=[
                                html.Span(username),
                                html.Span(
                                    style={
                                        "display": "inline-block",
                                        "width": "10px",
                                        "height": "10px",
                                        "borderRadius": "50%",
                                        "backgroundColor": colore
                                    }
                                )
                            ]
                        ),
                        id={'type': 'patient-row', 'index': paz_id},
                        n_clicks=0,
                        className="patient-row",
                        style={
                            "cursor": "pointer",
                            "padding": "10px",
                            "borderBottom": "1px solid #ccc"
                        }
                    )

                )

            return elementi
        else:
            return dash.no_update
        
# ******************************************************************************************************************
    
    #permette di vedere i grafici paziente per paziente al diabetologo
    @app.callback(
        Output("patient-number", "children"),
        Output("patient-pie", "children"),
        Output("graph-???", "children"),
        Input("url", "pathname"),
        prevent_initial_call=True
    )
    def mostra_dati_dashboard(pathname):
        id=current_user.get_id_diabetologo()
        cur=model.connection.cursor()
        if pathname=="/doctor-dashboard":    
            labels = ['Alterata','Normale','Ottima']
            cur.execute("""
                SELECT AVG(g.valore)
                FROM Paziente p
                JOIN Diabetologo d on p.diabetologo_associato=d.id_diabetologo
                JOIN Glicemia g on p.id_paziente=g.paziente
                WHERE id_diabetologo=%s
                GROUP BY id_paziente
            """, (id,))
            media_glicemie = cur.fetchall()

            a = n = o = 0
            for media in media_glicemie:
                valore = media[0]
                if valore < 70 or valore > 180:
                    a += 1
                elif 130 < valore < 180:
                    n += 1
                elif 70 <= valore <= 130:
                    o += 1

            values = [a,n,o]
            colors = ["#FF4C4C", '#FFD93B', '#08ff46'] 
            torta = go.Figure(data=[go.Pie(labels=labels, values=values,marker=dict(colors=colors))])
            num_paz=len(model.Diabetologo.visualizza_pazienti_associati(id))
            dati_paziente='dati tabella info paziente'
            return num_paz,dati_paziente,dcc.Graph(figure=torta)
        else:
            return dash.no_update
# ******************************************************************************************************************
    @app.callback(
        Output("patient-graph", "children"),
        Output("patient-data", "children"),
        Input("url","pathname"),
        Input({'type': 'patient-row', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def visualizza_andamento_glicemia(path,n_clicks):
        triggered = ctx.triggered

        if not triggered or not any(n_clicks):
            raise dash.exceptions.PreventUpdate

        # Ottieni ID del paziente cliccato
        prop_id = triggered[0]['prop_id']  
        id_dict_str = prop_id.split('.')[0]
        try:
            id_dict = json.loads(id_dict_str)
        except json.JSONDecodeError:
            raise dash.exceptions.PreventUpdate

        id_paz = id_dict['index']
        if path=="/doctor-patient":
            id=current_user.get_id_diabetologo()
            grafico=model.Diabetologo.visualizza_glicemia_paziente(id_paz)
            info_paziente="vedi e aggiorna fattori di rischio"

            return dcc.Graph(figure=grafico),info_paziente
        else:
            return dash.no_update,dash.no_update,dash.no_update
# ******************************************************************************************************************
    @app.callback(
        Output({'type': 'patient-row', 'index': ALL}, 'style'),
        Input({'type': 'patient-row', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def evidenzia_paziente_selezionato(n_clicks):
        triggered = ctx.triggered

        if not triggered:
            raise dash.exceptions.PreventUpdate

        id_str = triggered[0]['prop_id'].split('.')[0]
        id_dict = json.loads(id_str)
        id_paz = id_dict['index']

        component_ids = [c['id']['index'] for c in ctx.inputs_list[0]]

        style_default = {
            "padding": "10px",
            "borderBottom": "1px solid #ccc",
            "cursor": "pointer",
            "backgroundColor": "white",
            "fontWeight": "normal"
        }

        style_selected = {
            **style_default,
            "backgroundColor": "#dedbdb",
            "fontWeight": "bold"
        }

        style_list = []
        for cid in component_ids:
            style_list.append(style_selected if cid == id_paz else style_default)

        return style_list

# ******************************************************************************************************************
# Callback aggiornamento cerchio colorato glicemia:
    @app.callback(
        # Numero centrale visualizzato
        Output("number", "children"),
        # Colore dello sfondo
        Output("cerchio-colorato", "style"),
        Input("input-glicemia", "n_submit"),
        State("input-glicemia", "value"),
        State("number", "children"),
        State("cerchio-colorato", "style"),
        prevent_initial_call=True
    )
    def aggiorna_cerchio(n_submit, valore, number, stile_corrente):
        if not n_submit:
            return number, stile_corrente
        
        # Ipoglicemia
        if valore < 70:
            return valore, {"background-color": "#FF4C4C"}
        # Normoglicemia
        elif 70 <= valore <= 130:
            return valore, {"background-color": '#08ff46'}
        # Glicemia alta (merita attenzione)
        elif 131 <= valore <= 180:
            return valore, {"background-color": '#FFD93B'}
        # Iperglicemia
        else:
            return valore, {"background-color": '#FF4C4C'}