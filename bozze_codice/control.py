import json
import dash_bootstrap_components as dbc
from dash import MATCH, html, dcc, Input, Output, State, ALL, ctx
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
    # callback che gestisce i click dentro il dropdown della richiesta admin
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
    

    # ******************************************
    # callback che triggera il refresh delle opzioni disponibili all'interno del dropdown delle richieste di account
    @app.callback(
        Output("dropdown-selezione-richiesta-account", "options"),
        Input("dropdown-selezione-richiesta-account", "search_value")
    )
    def aggiorna_opzioni_dropdown(search_value):
        options = model.get_all_richieste_account()
        return options


    # **********************
    # callback che popola il dropdown e gestisce i bottoni nella pagina delle richieste, dell'admin.
    @app.callback(
        [Output("contenitore-informazioni-richiesta", "children", allow_duplicate=True),  # aggiorna magari con un messaggio di conferma
        Output("dropdown-selezione-richiesta-account", "options", allow_duplicate=True)],
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
            alert = dbc.Alert(f"Richiesta {id_richiesta} accettata con successo.", color="success", dismissable=True)           # da fare
            alert = dbc.Alert(f"Richiesta {id_richiesta} rifiutata con successo.", color="danger", dismissable=True)
            
        else:
            return dash.no_update, dash.no_update

        # aggiorna il dropdown con le richieste rimanenti
        richieste = model.get_all_richieste_account()                             # deve restituire lista di tuple/dict
        options = [{"label": f"{r[1]}", "value": r[0]} for r in richieste]

        return alert, options
    
# ******************************************************************************************************************

    @app.callback(
    Output("dettagli-paziente", "children"),
    Input({"type": "btn-paziente", "index": ALL}, "n_clicks"),
    prevent_initial_call=True
    )
    def mostra_dettagli_paziente(n_clicks):
        if not any(n_clicks):
            return dash.no_update

        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        matched_id = eval(triggered_id)  # trasforma la str in dict
        paziente_id = matched_id["index"]

        dati_paziente = model.get_dettagli_paziente(paziente_id)

        if not dati_paziente:
            return dbc.Alert("Dettagli non disponibili per questo paziente", color="danger")

        dettagli = [
            dbc.ListGroupItem([
                html.Strong(f"{k.capitalize().replace('_', ' ')}: "),
                html.Span(str(v))
            ])
            for k, v in dati_paziente.items()
        ]

        return dbc.Card(
            [
                dbc.CardHeader(html.H5(f"Dettagli paziente: {dati_paziente.get('nome', '')}")),
                dbc.CardBody(
                    dbc.ListGroup(dettagli, flush=True),
                    style={
                        "maxHeight": "380px",
                        "overflowY": "auto",
                        "paddingRight": "8px"  # per evitare scrollbar sopra il contenuto
                    }
                )
            ],
            className="shadow-sm"
        )


    @app.callback(
        Output("dettagli-diabetologo", "children"),
        Input({"type": "btn-diabetologo", "index": ALL}, "n_clicks"),
        prevent_initial_call=True
    )
    def mostra_dettagli_diabetologo(n_clicks):
        if not any(n_clicks):
            return dash.no_update

        ctx = dash.callback_context
        triggered_id = ctx.triggered[0]["prop_id"].split(".")[0]
        matched_id = eval(triggered_id)
        diabetologo_id = matched_id["index"]

        dati_diabetologo = model.get_dettagli_diabetologo(diabetologo_id)

        if not dati_diabetologo:
            return dbc.Alert("Dettagli non disponibili per questo diabetologo", color="danger")

        dettagli = [
            dbc.ListGroupItem([
                html.Strong(f"{k.capitalize().replace('_', ' ')}: "),
                html.Span(str(v))
            ])
            for k, v in dati_diabetologo.items()
        ]

        return dbc.Card(
            [
                dbc.CardHeader(html.H5(f"Dettagli diabetologo: {dati_diabetologo.get('nome', '')}")),
                dbc.CardBody(
                    dbc.ListGroup(dettagli, flush=True),
                    style={
                        "maxHeight": "380px",
                        "overflowY": "auto",
                        "paddingRight": "8px"  # per evitare scrollbar sopra il contenuto
                    }
                )
            ],
            className="shadow-sm"
        )

    
# ******************************************************************************************************************

    #permette di vedere i grafici paziente per paziente al diabetologo
    @app.callback(
        Output("dropdown-output-tutti","children"),
        Output("dropdown-tutti-pazienti","options"),
        Input("dropdown-tutti-pazienti","value"),
        Input("filtro-pazienti","value")
    )
    def visualizza_lista_pazienti(paziente,scelta):
        
        id = current_user.get_id_diabetologo()

        if scelta=='PA':
            lista=model.Diabetologo.visualizza_pazienti_associati(id)
        else:
            lista=model.Diabetologo.visualizza_tutti_pazienti()

        opzioni = [{"label": nome, "value": nome} for nome in lista]

        if not paziente:
            return "Seleziona un paziente per visualizzare il grafico.",opzioni
        #per test ora ritorna patient-dashboard ma dovrà ritornare quella del dottore
        return view.patient_dashboard,opzioni
       
        
       
# ******************************************************************************************************************
    @app.callback(
        Output("doctor-patient-queue", "children"),
        Input("url","pathname")
    )
    def aggiorna_lista_pazienti(path):
        if path=="/doctor-dashboard" or path=='/doctor-patient':
            return view.layout_lista_pazienti_associati()
        else:
            return dash.no_update
        
# ******************************************************************************************************************
    #permette di vedere i grafici paziente per paziente al diabetologo
    @app.callback(
        Output("patient-number", "children"),
        Output("patient-pie", "children"),
        Input("url", "pathname"),
        prevent_initial_call=True
    )
    def mostra_dati_dashboard(pathname):
        cur=model.connection.cursor()
        if pathname=="/doctor-dashboard":
            # labels del grafico a torta che indica la % di pazienti con valori fuori dal limite, alti, normali
            labels = ['Fuori dal limite','Alta','Normale']
            cur.execute("""
                SELECT AVG(g.valore)
                FROM Paziente p
                JOIN Glicemia g on p.id_paziente=g.paziente
                WHERE p.diabetologo_associato=%s
                GROUP BY id_paziente
            """, (current_user.get_id_diabetologo(),))
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
            num_paz=current_user.get_numero_pazienti_associati()
            if(a==0 and n==0 and o==0):
                return num_paz,"Nessun dato glicemico inserito"
            colors = ["#FF4C4C", '#FFD93B', '#08ff46'] 
            torta = go.Figure(data=[go.Pie(labels=labels, values=values,marker=dict(colors=colors))])
            return num_paz,dcc.Graph(figure=torta)
        else:
            return dash.no_update
        
# ******************************************************************************************************************
    # Restituisce il grafico plotly dell'andamento di glicemia del paziente selezionato nella pagina "patient" del dottore

    @app.callback(
        Output("patient-graph", "children"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def visualizza_andamento_glicemia(pathname, n_clicks):
        triggered = ctx.triggered

        if not triggered or not any(n_clicks):
            return "Nessun paziente selezionato"

        # Ottieni ID del paziente cliccato
        prop_id = triggered[0]['prop_id']
        id_dict_str = prop_id.split('.')[0]
        try:
            id_dict = json.loads(id_dict_str)
        except json.JSONDecodeError:
            raise dash.exceptions.PreventUpdate

        id_paz = id_dict['index']

        if pathname == "/doctor-patient":
            grafico = model.Diabetologo.visualizza_glicemia_paziente(id_paz)
            return dcc.Graph(figure=grafico, config={'responsive': True})
        else:
            return dash.no_update
# style={'width': '100%', 'height': '100%'}
# ******************************************************************************************************************
    # Callback che restituisce la card con le informazioni di base di un paziente nella dashboard del dottore:
    @app.callback(
        # Div delle Informazioni del paziente
        Output("doctor-patient-info", "children"),
        # Prende l'url della pagina
        Input("url", "pathname"),
        # Prende il pulsante del paziente
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def visualizza_infopaziente_base(path, n_clicks):
        trigger_id = ctx.triggered_id

        # All'apertura della pagina dashboard viene visualizzato di default questo messaggio:
        if not trigger_id or not isinstance(trigger_id, dict) or not any(n_clicks):
            return "Nessun paziente selezionato"            

        id_paz = trigger_id.get('index')

        if path == "/doctor-dashboard":
            info = current_user.get_info_base_paziente_associato(id_paz)
            return view.crea_div_info_base_paziente(info)
        else:
            return dash.no_update

# ******************************************************************************************************************
    
    @app.callback(
        Output("patient-info", "children"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        prevent_initial_call=True
    )
    def visualizza_infopaziente_dettagliate(path, n_clicks):
        trigger_id = ctx.triggered_id

        if not trigger_id or not isinstance(trigger_id, dict) or not any(n_clicks):
            return "Nessun paziente selezionato"            

        id_paz = trigger_id.get('index')

        if path == "/doctor-patient":
            dati = current_user.visualizza_dati_paziente(id_paz)
            segnalazioni=current_user.get_segnalazioni_paziente(id_paz)
            div = view.crea_div_paziente(dati[0], dati[1],segnalazioni)
            return div
        else:
            return dash.no_update

# ******************************************************************************************************************
    #fil-callback che si ricorda dell'id del paziente che è stato triggerato
    @app.callback(
        Output("selected-patient-id", "data"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),  # CORRETTO
        prevent_initial_call=True
    )
    def salva_id_paziente(n_clicks):
        triggered_id = ctx.triggered_id
        if any(n_clicks):
            return triggered_id.get('index')
        raise dash.exceptions.PreventUpdate

#******************************************************************************************************************   
    #callback per inserire nuovi dati paziente
    @app.callback(
        Output("inserisci-info-output", "children"),
        Output("inserisci-info-output", "color"),
        Output("inserisci-info-output", "is_open"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        Input("inserisci-modifiche-btn", "n_clicks"),
        Input("insert-rischio", "value"),
        Input("insert-patologie", "value"),
        Input("insert-comorb", "value"),
        State("selected-patient-id", "data"),
        prevent_initial_call=True
    )
    def modifica_inserisci_info_paziente(path, n_clicks, insertbtn, fattori, patologia, comorbidita, id_paz):
        trigger_id = ctx.triggered_id

        fattori = fattori or None
        patologia = patologia or None
        comorbidita = comorbidita or None

        if fattori==None and patologia==None and comorbidita==None and insertbtn>0:
            return "Informazioni mancanti", "danger", "True"

        if trigger_id != "inserisci-modifiche-btn":
            raise dash.exceptions.PreventUpdate

        if path == "/doctor-patient" and insertbtn > 0:
            if not any(n_clicks):
                return "Seleziona un paziente!", "danger","True"
            current_user.inserisci_info_paziente(id_paz, fattori, patologia, comorbidita)
            return "Modifica avvenuta con successo", "success", "True"
        else:
            return dash.no_update
        
#******************************************************************************************************************   
    #callback per modificare dati paziente
    @app.callback(
        Output("modifica-info-output", "children"),
        Output("modifica-info-output", "color"),
        Output("modifica-info-output", "is_open"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        Input("salva-modifiche-btn", "n_clicks"),
        Input("input-rischio", "value"),
        Input("input-patologie", "value"),
        Input("input-comorb", "value"),
        State("selected-patient-id", "data"),
        prevent_initial_call=True
    )
    def modifica_inserisci_info_paziente(path, n_clicks,modifybtn, fattori, patologia, comorbidita, id_paz):
        trigger_id = ctx.triggered_id

        fattori = fattori or None
        patologia = patologia or None
        comorbidita = comorbidita or None

        if fattori==None and patologia==None and comorbidita==None and modifybtn>0:
            return "Informazioni mancanti", "danger", "True"

        if trigger_id != "salva-modifiche-btn":
            raise dash.exceptions.PreventUpdate

        if path == "/doctor-patient" and modifybtn > 0:
            if not any(n_clicks):
                return "Seleziona un paziente!", "danger","True"
            current_user.modifica_info_paziente(id_paz, fattori, patologia, comorbidita)
            return "Modifica avvenuta con successo", "success", "True"
        else:
            return dash.no_update

# ******************************************************************************************************************
    #callback per aprire il popup di modifica
    @app.callback(
        Output("popup-modifica-info", "is_open"),
        [Input("modal-modifiche-btn", "n_clicks"), Input("close-modifica-infopaz", "n_clicks")],
        [dash.dependencies.State("popup-modifica-info", "is_open")]
    )
    def apri_chiudi_popup_modificainfopaz(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open
# ******************************************************************************************************************
    #callback per aprire il popup di inserimento
    @app.callback(
        Output("popup-inserisci-info", "is_open"),
        [Input("modal-insert-btn", "n_clicks"), Input("close-insert-infopaz", "n_clicks")],
        [dash.dependencies.State("popup-inserisci-info", "is_open")]
    )
    def apri_chiudi_popup_inserisciinfopaz(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open
# ******************************************************************************************************************
    @app.callback(
         Output("patient-therapy","children"),
         Input("url","pathname"),
         Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
    )
    def visualizza_dropdown_terapie(path,n_clicks):
        trigger_id = ctx.triggered_id

        if not trigger_id or not isinstance(trigger_id, dict) or not any(n_clicks):
            return "Nessun paziente selezionato"            
        id_paz = trigger_id.get('index')
        if path=="/doctor-patient":
            terapie=current_user.get_terapie_paziente(id_paz)
            return view.crea_div_terapia_dropdown(terapie)
        else:
            return dash.no_update()
        
    @app.callback(
        Output("div-terapia-selezionata", "children"),
        Input("dropdown-terapia-selezionata", "value"),
        State("selected-patient-id", "data"),
        prevent_initial_call=True
    )
    def mostra_terapia_selezionata(id_terapia, id_paz):
        if id_terapia is None:
            return html.Div("Seleziona una terapia.")

        lista_terapie = current_user.get_terapie_paziente(id_paz)
        terapia = next((t for t in lista_terapie if t[0] == id_terapia), None)
        if terapia is None:
            return html.Div("Terapia non trovata.")

        return view.crea_div_terapia_selezionata(terapia)

# ******************************************************************************************************************
    #callback per aprire il popup di modifica terapia
    @app.callback(
        Output("popup-modifica-terapia", "is_open"),
        [Input("apri-modal-terapia", "n_clicks"), Input("chiudi-modal-terapia", "n_clicks")],
        [dash.dependencies.State("popup-modifica-terapia", "is_open")]
    )
    def apri_chiudi_popup_modificainfopaz(open_clicks, close_clicks, is_open):
        if open_clicks or close_clicks:
            return not is_open
        return is_open
# ******************************************************************************************************************
#callback per modificare dati terapia
    @app.callback(
        Output("modifica-terapia-output", "children"),
        Output("modifica-terapia-output", "color"),
        Output("modifica-terapia-output", "is_open"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        Input("btn-salva-modifiche-terapia", "n_clicks"),
        Input("input-farmaco", "value"),
        Input("input-dosaggio", "value"),
        Input("input-assunzioni", "value"),
        Input("input-data-inizio", "value"),
        Input("input-data-fine", "value"),
        Input("input-indicazioni", "value"),
        State("selected-patient-id", "data"),
        prevent_initial_call=True
    )
    def modifica_terapia_paziente(path, n_clicks, modifybtn, farmaco,dosaggio,assunzioni,data_i,data_f,indicazioni, id_paz):
        trigger_id = ctx.triggered_id

        farmaco = farmaco or None
        dosaggio = dosaggio or None
        assunzioni = assunzioni or None
        indicazioni = indicazioni or None
        data_i = data_i or None
        data_f = data_f or None
        if farmaco==None and dosaggio==None and assunzioni==None and indicazioni==None and data_i==None and data_f==None and modifybtn>0:
            return "Informazioni mancanti", "danger", True
        if data_i and data_f and data_f<data_i:
            return "Data fine non valida","danger", True
        
        if trigger_id != "btn-salva-modifiche-terapia":
            raise dash.exceptions.PreventUpdate

        if path == "/doctor-patient" and modifybtn > 0:
            if not any(n_clicks):
                return "Seleziona un paziente!", "danger",True
            current_user.modifica_terapia_paziente(id_paz,farmaco,dosaggio,assunzioni,data_i,data_f,indicazioni)
            return "Modifica avvenuta con successo", "success", True
        else:
            return dash.no_update

#******************************************************************************************************************
    #callback per aprire il pop up aggiungi terapia
    @app.callback(
        Output("popup-nuova-terapia", "is_open"),
        [Input("aggiungi-terapia-btn", "n_clicks"), Input("chiudi-nuova-terapia", "n_clicks")],
        [State("popup-nuova-terapia", "is_open")]
    )
    def apri_aggiungi_terapia(n_apri, n_chiudi, is_open):
        if n_apri or n_chiudi:
            return not is_open
        return is_open


#******************************************************************************************************************
#callback per aggiungere nuovi dati terapia
    @app.callback(
        Output("aggiungi-terapia-output", "children"),
        Output("aggiungi-terapia-output", "color"),
        Output("aggiungi-terapia-output", "is_open"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        Input("salva-nuova-terapia-btn", "n_clicks"),
        Input("input-nuovo-farmaco", "value"),
        Input("input-nuovo-dosaggio", "value"),
        Input("input-nuovo-assunzioni", "value"),
        Input("input-nuovo-data-inizio", "date"),
        Input("input-nuovo-data-fine", "date"),
        Input("input-nuovo-indicazioni", "value"),
        State("selected-patient-id", "data"),
        prevent_initial_call=True
    )
    def aggiungi_terapia_paziente(path, n_clicks, savebtn, farmaco,dosaggio,assunzioni,data_i,data_f,indicazioni, id_paz):
        trigger_id = ctx.triggered_id

        farmaco = farmaco or None
        indicazioni = indicazioni or None
        dosaggio = dosaggio or None
        assunzioni = assunzioni or None
        if (farmaco==None or dosaggio==None or assunzioni==None or data_i==None or data_f==None) and trigger_id=="salva-nuova-terapia-btn":
            return "Informazioni mancanti", "danger", True

        if trigger_id != "salva-nuova-terapia-btn":
            raise dash.exceptions.PreventUpdate

        if path == "/doctor-patient" and savebtn > 0:
            if not any(n_clicks):
                return "Seleziona un paziente!", "danger",True
            current_user.inserisci_terapia(id_paz,farmaco,dosaggio,assunzioni,data_i,data_f,indicazioni)
            return "Modifica avvenuta con successo", "success", True
        else:
            return dash.no_update

#******************************************************************************************************************
    #callback per far partire correttamente la scelta della data fine terapia
    @app.callback(
        Output("input-nuovo-data-fine", "min_date_allowed"),
        Input("input-nuovo-data-inizio", "date")
    )
    def aggiorna_min_data_fine(data_inizio):
        if data_inizio:
            return data_inizio  # Imposta la data inizio come minimo selezionabile
        return None
#*******************************************************************************************************************
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