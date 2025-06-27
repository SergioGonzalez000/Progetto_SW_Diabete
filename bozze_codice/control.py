import json
import dash.nbextension
import dash_bootstrap_components as dbc
from dash import MATCH, html, dcc, Input, Output, State, ALL, ctx
from flask_login import login_user, logout_user, current_user
from werkzeug.security import check_password_hash 
from datetime import date
import dash
import model
import view


import plotly.express as px
import plotly.graph_objects as go

# Funzione che restituisce una stringa della data di oggi
def get_today():
    return date.today().isoformat()

# Callbacks
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
                return view.guest_navlinks, view.login, "/login"
            # Accesso alla registrazione
            elif pathname == "/registration":
                return view.guest_navlinks, view.registration, "/registration"
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
    
    # #permette di vedere i grafici paziente per paziente al diabetologo
    # @app.callback(
    #     Output("dropdown-output","children"),
    #     Input("dropdown-pazienti","value"),
    # )
    # def visualizza_grafico_paziente(paziente):
    #     if not paziente:
    #         return "Seleziona un paziente per visualizzare il grafico."
    
    #     fig = model.Diabetologo.visualizza_glicemia_paziente(paziente)
    #     return dcc.Graph(figure=fig)
    

    # ****************************************************************

    # CALLBACKS PER L'ELENCO PAZIENTI
    # callback che carica i dettagli di un paziente scelto nel dropdown
    @app.callback(
        Output("dettagli-richiesta-paziente", "children"),
        Input("dropdown-richieste-pazienti", "value")
    )
    def mostra_dettagli_paziente(id_richiesta):
        if not id_richiesta:
            return None
        dati = model.get_dati_richiesta_account_by_id(id_richiesta)
        return view.render_dati_richiesta(dati)

    # callback che aggiorna il dropdown dei pazienti
    @app.callback(
        Output("dropdown-richieste-pazienti", "options"),
        Input("dropdown-richieste-pazienti", "search_value")
    )
    def aggiorna_opzioni_pazienti(search_value):
        return model.get_richieste_account_pazienti()

    # callback che gestisce le richiesta di inserimento dei pazienti
    @app.callback(
        [Output("alert-richiesta-paziente", "children", allow_duplicate=True),
        Output("dropdown-richieste-pazienti", "options", allow_duplicate=True)],
        [Input("btn-accetta-paziente", "n_clicks"),
        Input("btn-rifiuta-paziente", "n_clicks")],
        State("dropdown-richieste-pazienti", "value"),
        prevent_initial_call=True,
        allow_duplicate=True
    )
    def gestisci_richiesta_paziente(n_clicks_accetta, n_clicks_rifiuta, id_richiesta):
        if not id_richiesta:
            return dbc.Alert("Seleziona una richiesta prima di accettare o rifiutare.", color="warning", dismissable=True), dash.no_update

        bottone_premuto = ctx.triggered[0]["prop_id"].split(".")[0]

        if bottone_premuto == "btn-accetta-paziente":
            model.Admin.approva_richiesta(id_richiesta)
            alert = dbc.Alert(f"Richiesta {id_richiesta} accettata con successo.", color="success", dismissable=True)

        elif bottone_premuto == "btn-rifiuta-paziente":
            model.Admin.rifiuta_richiesta(id_richiesta)
            alert = dbc.Alert(f"Richiesta {id_richiesta} rifiutata con successo.", color="danger", dismissable=True)

        options = model.get_richieste_account_pazienti()
        return alert, options


    # CALLBACKS PER L'ELENCO DIABETOLOGI
    # callback che carica i dettagli di un diabetologo scelto nel dropdown
    @app.callback(
        Output("dettagli-richiesta-diabetologo", "children"),
        Input("dropdown-richieste-diabetologi", "value")
    )
    def mostra_dettagli_diabetologo(id_richiesta):
        if not id_richiesta:
            return None
        dati = model.get_dati_richiesta_account_by_id(id_richiesta)
        return view.render_dati_richiesta(dati)


    # callback che aggiorna il dropdown dei diabetologi
    @app.callback(
        Output("dropdown-richieste-diabetologi", "options"),
        Input("dropdown-richieste-diabetologi", "search_value")
    )
    def aggiorna_opzioni_diabetologi(search_value):
        return model.get_richieste_account_diabetologi()


    # callback che gestisce le richieste di inserimento dei pazienti
    @app.callback(
        [Output("alert-richiesta-diabetologo", "children", allow_duplicate=True),
        Output("dropdown-richieste-diabetologi", "options", allow_duplicate=True)],
        [Input("btn-accetta-diabetologo", "n_clicks"),
        Input("btn-rifiuta-diabetologo", "n_clicks")],
        State("dropdown-richieste-diabetologi", "value"),
        prevent_initial_call=True,
        allow_duplicate=True
    )
    def gestisci_richiesta_diabetologo(n_clicks_accetta, n_clicks_rifiuta, id_richiesta):
        if not id_richiesta:
            return dbc.Alert("Seleziona una richiesta prima di accettare o rifiutare.", color="warning", dismissable=True), dash.no_update

        bottone_premuto = ctx.triggered[0]["prop_id"].split(".")[0]

        if bottone_premuto == "btn-accetta-diabetologo":
            model.Admin.approva_richiesta(id_richiesta)
            alert = dbc.Alert(f"Richiesta {id_richiesta} accettata con successo.", color="success", dismissable=True)

        elif bottone_premuto == "btn-rifiuta-diabetologo":
            model.Admin.rifiuta_richiesta(id_richiesta)
            alert = dbc.Alert(f"Richiesta {id_richiesta} rifiutata con successo.", color="danger", dismissable=True)

        options = model.get_richieste_account_diabetologi()
        return alert, options

    
# ******************************************************************************************************************
    # CALLBACKS PER LA GESTIONE DEGLI ELENCHI DI PAZIENTI E DIABETOLOGI DELL'ADMIN

    # callback che gestisce la visualizzazione dei dettagli del paziente, dopo averlo selezionato dall'elenco "Pazienti"
    # dell'Admin  
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
        matched_id = eval(triggered_id)         # trasforma la str in dict
        paziente_id = matched_id["index"]

        dati_paziente = model.get_dettagli_paziente(paziente_id)
        if not dati_paziente:
            return dbc.Alert("Dettagli non disponibili per questo paziente", color="danger")

        # recupera nome e cognome del diabetologo associato
        diab_id = dati_paziente.get("diabetologo_associato")
        dati_diab = model.get_dettagli_diabetologo(diab_id) if diab_id else None
        
        return view.crea_card_paziente(dati_paziente, dati_diab)


    # callback che gestisce la visualizzazione dei dettagli del diabetologo, dopo averlo selezionato dall'elenco "Diabetologi"
    # dell'Admin  
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

        return view.crea_card_diabetologo(dati_diabetologo)


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
        Output("doctor-info", "children"),
        Output("patient-pie", "children"),
        Input("url", "pathname"),
        prevent_initial_call=True
    )
    def mostra_dati_dashboard(pathname):
        cur=model.connection.cursor()
        if pathname=="/doctor-dashboard":
            id=current_user.get_id_diabetologo()
            # labels del grafico a torta che indica la % di pazienti con valori fuori dal limite, alti, normali
            labels = ['Fuori dal limite','Alta','Normale']
            cur.execute("""
                SELECT AVG(g.valore)
                FROM Paziente p
                JOIN Glicemia g on p.id_paziente=g.paziente
                WHERE p.diabetologo_associato=%s
                GROUP BY id_paziente
            """, (id,))
            media_glicemie = cur.fetchall()

            a = n = o = 0
            for media in media_glicemie:
                valore = media[0]
                if valore < 80 or valore > 180:
                    a += 1
                elif 130 < valore < 180:
                    n += 1
                elif 70 <= valore <= 130:
                    o += 1

            values = [a,n,o]
            info=model.get_info_base_diabetologo(id)
            if(a==0 and n==0 and o==0):
                return info, html.H5("Nessun dato glicemico inserito.", style={'color': 'gray'})
            colors = ["#FF4C4C", '#FFD93B', '#08ff46'] 
            torta = go.Figure(data=[go.Pie(labels=labels, values=values,marker=dict(colors=colors))])
            return view.crea_div_info_base(info,False),dcc.Graph(figure=torta)
        else:
            return dash.no_update
        
# ******************************************************************************************************************
    #callback che mostra i grafici del paziente al diabetologo con il dropdown

    @app.callback(
        Output("patient-graph", "children"),
        Input("url", "pathname"),
        Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
        Input("filtro-temporale", "value"),
        Input("dropdown-scelta-grafico","value"),
        State("selected-patient-id", "data"),
        prevent_initial_call=True
    )
    def visualizza_andamento_glicemia(pathname, n_clicks, filtro, scelta, stored_id_paz):
        triggered_id = ctx.triggered_id

        if not triggered_id or not any(n_clicks):
            return html.H5("Seleziona un paziente.", style={'color': 'gray'})
        # Se è stato cliccato un nuovo paziente
        if isinstance(triggered_id, dict) and triggered_id.get("type") == "btn-paziente":
            id_paz = triggered_id["index"]
        else:
            # Nessun nuovo paziente cliccato → usa quello memorizzato
            id_paz = stored_id_paz

        if not id_paz or not any(n_clicks):
            return "Nessun paziente selezionato"
        if id_paz and not scelta:
            return "Seleziona un grafico"

        dati = model.get_dati_glicemia_filtrati(id_paz,filtro,scelta)

        if pathname == "/doctor-patient" and scelta:
            grafico = model.visualizza_andamento_glicemia(dati) if scelta == "andamento" else model.visualizza_media_glicemica_fasce_orarie(dati)
            return dcc.Graph(figure=grafico,  config={'responsive': True})
        else:
            return dash.no_update

        
#*************************************************************************************************************************************
    #
    @app.callback(
        Output("andamento-giornaliero", "children"),
        Input("url", "pathname"),
        Input("trigger-aggiorna-grafico", "data"),
    )
    def visualizza_andamento_giornaliero(pathname, _):
        if pathname == "/patient-dashboard":
            id_paz = current_user.get_id_paziente()
            dati = model.get_dati_glicemia_filtrati(id_paz, "giornaliero", "andamento")
            grafico = model.visualizza_andamento_glicemia(dati)
            return dcc.Graph(figure=grafico)
        return dash.no_update


# ******************************************************************************************************************
    #callback che fa vedere al diabetologo le informazioni di base del paziente 
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
            return html.H5("Seleziona un paziente.", style={'color': 'gray'})            

        id_paz = trigger_id.get('index')
        if path == "/doctor-dashboard":
            id_diab=current_user.get_id_diabetologo()
            info = model.get_info_base_paziente(id_diab,id_paz)
            div = view.crea_div_info_base(info,True)
            return div
        else:
            return dash.no_update
# ******************************************************************************************************************
    #callback che fa vedere al paziente le sue informazioni di base 
    @app.callback(
        Output("info-paz", "children"),
        Input("url", "pathname"),
        prevent_initial_call=True
    )
    def visualizza_info_base_paziente(path):
        
        if path == "/patient-dashboard":
            id_paz = current_user.get_id_paziente()
            diab= current_user.get_diabetologo()[0]
            id_diab=diab["id"]
            info = model.get_info_base_paziente(id_diab,id_paz)
            div = view.crea_div_info_base(info,True)
            return div
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
            return html.H5("Seleziona un paziente.", style={'color': 'gray'})            

        # id del paziente
        id_paz = trigger_id.get('index')

        # Se siamo nella pagine 'Pazienti' del diabetologo
        if path == "/doctor-patient":
            dati = current_user.visualizza_dati_paziente(id_paz)
            segnalazioni=current_user.get_segnalazioni_paziente(id_paz)
            return view.crea_div_paziente(dati[0], dati[1],segnalazioni)
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
    # CALLBACK PER DROPDOWN TERAPIE
    @app.callback(
         Output("patient-therapy","children"),
         Input("url","pathname"),
         Input({'type': 'btn-paziente', 'index': ALL}, 'n_clicks'),
    )
    def visualizza_dropdown_terapie(path,n_clicks):
        # id dell'ultimo elemento triggerato nel context (pagina)
        trigger_id = ctx.triggered_id

        if not trigger_id or not isinstance(trigger_id, dict) or not any(n_clicks):
            return html.H5("Seleziona un paziente.", style={'color': 'gray'})
        
        # Id paziente             
        id_paz = trigger_id.get('index')
        
        if path=="/doctor-patient":
            id_diab=current_user.get_id_diabetologo()
            terapie=model.get_terapie_paziente(id_diab,id_paz)
            # Se la lista delle terapie è vuota: mostra solo il pulsante "Nuova terapia"
            if not terapie:
                return html.Div([  
                    html.H5("Nessuna terapia registrata.", style={'color': 'gray', 'marginBottom':'80px'}),

                    dbc.Button(
                        "Nuova Terapia",
                        id='aggiungi-terapia-btn',
                        n_clicks=0,
                        style={
                            'width': '100%',
                            'border':'none',
                            'margin-top': 'auto',
                            'border-radius': '25px',
                            'padding': '10px 25px',
                            'font-size':'20px'                
                            }
                        )
                    ],
                    style={
                        'flex': 1,
                        'height': '100%',   
                        'display': 'flex',
                        'flexDirection': 'column',
                    }
                )
            # Altrimenti:   
            return view.crea_div_terapia_dropdown(terapie)
        else:
            return dash.no_update
        
# ******************************************************************************************************************
    #mostra al paziente la div col dropdown che contiene tutte le terapie
    @app.callback(
         Output("terapie-paz","children"),
         Input("url","pathname"),
    )
    def visualizza_dropdown_terapie_paz(path):
                    
        if path=="/patient-dashboard":
            id_paz=current_user.get_id_paziente()
            diab= current_user.get_diabetologo()[0]
            id_diab=diab["id"]
            terapie=model.get_terapie_paziente(id_diab,id_paz)
            return view.crea_div_terapia_dropdown(terapie)
        else:
            return dash.no_update
#*****************************************************************************************************************************       
    #mostra al diabetologo le terapie del paziente selezionato e al paziente le sue, in base al path
    @app.callback(
        Output("div-terapia-selezionata", "children"),
        Input("dropdown-terapia-selezionata", "value"),
        Input("url","pathname"),
        State("selected-patient-id", "data"),
    )
    def mostra_terapia_selezionata(id_terapia,path, id_paz):
        # Se il parametro id_terapia è nullo (come ad esempio non'appena si seleziona un paziente):
        if id_terapia is None:
            return html.Div(
                dbc.Button(
                    "Nuova Terapia",
                    id='aggiungi-terapia-btn',
                    n_clicks=0,
                    style={
                        'width': '100%',
                        'margin-top': 'auto',
                        'border':'none',
                        'border-radius': '25px',
                        'padding': '10px 25px',
                        'font-size':'20px'                
                    }
                ),
                style={
                    'display': 'flex',
                    'flexDirection': 'column',
                    'height': '100%'
                }
            )

        # lista_terapie = current_user.get_terapie_paziente(id_paz)
        # # Costruzione della terapia: cerca la terapia
        # # t[0] id terapia
        # terapia = next((t for t in lista_terapie if t[0] == id_terapia), None)
        # # Se non trova la terapia:
        # if terapia is None:
        #     return html.Div("Terapia non trovata.")
        
        elif path == "/patient-dashboard":
            if id_terapia is None:
                return html.Div("Seleziona una terapia.")
            id_paz=current_user.get_id_paziente()
            diab= current_user.get_diabetologo()[0]
            id_diab=diab["id"]
            lista_terapie = model.get_terapie_paziente(id_diab,id_paz)
            terapia = next((t for t in lista_terapie if t[0] == id_terapia), None)
            if terapia is None:
                return html.Div("Terapia non trovata.")

            return view.crea_div_terapia_selezionata(terapia,False)
        elif path == "/doctor-patient":
            if id_terapia is None:
                return html.Div("Seleziona una terapia.")
            id_diab=current_user.get_id_diabetologo()
            lista_terapie = model.get_terapie_paziente(id_diab,id_paz)
            terapia = next((t for t in lista_terapie if t[0] == id_terapia), None)
            if terapia is None:
                return html.Div("Terapia non trovata.")
            return view.crea_div_terapia_selezionata(terapia,True)
        else:
            return dash.no_update
        
#*****************************************************************************************************************************       
        
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
#callback per modificare dati terapia o per eliminarne una dopo la conferma

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
        Input("conferma-elimina-terapia", "n_clicks"),
        State("selected-patient-id", "data"),
        State("terapia-selezionata", "data"),
        prevent_initial_call=True
    )
    def modifica_terapia_paziente(path, n_clicks, modifybtn, farmaco, dosaggio, assunzioni, data_i, data_f, indicazioni, conferma, id_paz, id_terapia):
        trigger_id = ctx.triggered_id

        if trigger_id == "conferma-elimina-terapia" and conferma > 0:
            # Azione di eliminazione terapia
            model.cur.execute("DELETE FROM Terapia WHERE id_terapia = %s", (id_terapia,))
            model.connection.commit()
            model.cur.close()
            return "Terapia eliminata correttamente", "success", True

        if trigger_id == "btn-salva-modifiche-terapia":
            # Gestione modifica terapia
            farmaco = farmaco or None
            dosaggio = dosaggio or None
            assunzioni = assunzioni or None
            indicazioni = indicazioni or None
            data_i = data_i or None
            data_f = data_f or None
            #controlla se sono tutte nulle, in tal caso ritorna informazioni mancanti
            if all(x is None for x in [farmaco, dosaggio, assunzioni, indicazioni, data_i, data_f]):
                return "Informazioni mancanti", "danger", True

            if data_i and data_f and data_f < data_i:
                return "Data fine non valida", "danger", True

            if path == "/doctor-patient" and modifybtn > 0:
                if not any(n_clicks):
                    return "Seleziona un paziente!", "danger", True

                current_user.modifica_terapia_paziente(
                    id_paz, id_terapia, farmaco, dosaggio, assunzioni, data_i, data_f, indicazioni
                )
                return "Modifica avvenuta con successo", "success", True

        # Se non è né il bottone salva né quello conferma, non aggiornare nulla
        raise dash.exceptions.PreventUpdate

#******************************************************************************************************************
    #callback per aprire il pop up aggiungi terapia
    @app.callback(
        Output("popup-nuova-terapia", "is_open"),
        [Input("aggiungi-terapia-btn", "n_clicks"), Input("chiudi-nuova-terapia", "n_clicks")],
        [State("popup-nuova-terapia", "is_open")],
        prevent_initial_call=True
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
            return "Terapia inserita con successo", "success", True
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
    #callback per gestire il popup che serve a chiedere la conferma per eliminare una terapia
    @app.callback(
        Output("popup-elimina-terapia", "is_open"),
        [Input("btn-elimina-terapia", "n_clicks"), Input("declina-elimina-terapia", "n_clicks")],
        [State("popup-elimina-terapia", "is_open")]
    )
    def apri_elimina_terapia(n_apri, n_chiudi, is_open):
        if n_apri or n_chiudi:
            return not is_open
        return is_open
#*******************************************************************************************************************
# Callback aggiornamento cerchio colorato glicemia e per inserire la glicemia nella base di dati (pagina paziente)
    @app.callback(
        Output("number", "children"),
        Output("cerchio-colorato", "style"),
        Output("inserisci-glicemia-output", "children"),
        Output("inserisci-glicemia-output", "is_open"),
        Output("inserisci-glicemia-output", "color"),
        Output("trigger-aggiorna-grafico", "data"),
        Input("url", "pathname"),
        Input("inserisci-glicemia", "n_clicks"),
        Input("input-farmaco-usato", "value"),
        Input("input-dosaggio-usato", "value"),
        Input("input-sintomi-riscontrati", "value"),
        State("input-glicemia", "value"),
        State("number", "children"),
        State("cerchio-colorato", "style"),
        State("trigger-aggiorna-grafico", "data"),
        prevent_initial_call=True
    )
    def aggiorna_cerchio(path, n_clicks, farmaco, dosaggio, sintomi, valore, number, stile_corrente, trigger):
        if path != "/patient-dashboard":
            return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, trigger

        if n_clicks and farmaco and dosaggio and valore:
            current_user.inserisci_glicemia(valore, farmaco, dosaggio, sintomi)
            if valore < 70:
                colore = "#FF4C4C"
            elif 80 <= valore <= 130:
                colore = "#08ff46"
            elif 131 <= valore <= 180:
                colore = "#FFD93B"
            else:
                colore = "#FF4C4C"
            return valore, {"background-color": colore}, "Inserimento corretto", True, "success", trigger + 1

        elif n_clicks:
            return number, stile_corrente, "Informazioni mancanti", True, "danger", trigger
        else:
            return valore, {"background-color": '#FF4C4C'}, dash.no_update, dash.no_update, dash.no_update, dash.no_update
        

# ******************************************************************

# callbacks che gestiscono i click sui bottoni del paziente, che aprono i relativi pop-up.
    
    # PRIMO PULSANTE ADMIN-PAZIENTE
    # "Grafico glicemia paziente"
    # callback di gestione del pop-up
    @app.callback(
        Output("pop-admin-grafico-paziente", "is_open"),
        Input("btn-graf-paziente", "n_clicks"),
        [State("pop-admin-grafico-paziente", "is_open")]
    )
    def gestisci_popup_admin_graf_paziente(n_apri, is_open):
        if n_apri is None:
            # all'inizio NON si fa nulla 
            return is_open
        if n_apri:
            # toggle
            return not is_open
        return is_open

    # callback di gestione del grafico, con il giusto id_paziente. è attivata dallo stesso pulsante di 
    # quella sopra (forse si posssono unire?)
    @app.callback(
        Output("contenitore-popup-graf-paziente", "children"),
        Input("btn-graf-paziente", "n_clicks"),
        State("store-id-paziente", "data"),
        prevent_initial_call= True
    )
    def aggiorna_grafico_paziente(n_clicks, id_paziente):
        if not n_clicks or id_paziente is None:
            return "Seleziona un paziente e premi il bottone per vedere il grafico."

        # DA MODIFICARE IN MODO DA POTER ADOTTARE I FILTRI PER CUI LA FUNZIONE è PREDISPOSTA
        fig = model.visualizza_andamento_glicemia(model.get_dati_glicemia_filtrati(id_paziente, "annuale", "andamento"))  

        # logica se il grafico è vuoto.
        # non volendo sovrascrivere la funzione che genera l'andamento glicemia per farlo ritornare "None" se non ci sono dati.
        if fig.layout.title.text == "Nessun dato glicemico disponibile":
            return dbc.Alert("Nessun dato glicemico disponibile per questo paziente.", color="danger", dismissable=False)


        return dcc.Graph(figure=fig, style={"borderRadius": "5px", "padding": "10px"})
        

    # SECONDO PULSANTE ADMIN-PAZIENTE
    # "Rimuovi paziente". questa callback gestisce l'apertura e la chiusura del popup
    @app.callback(
        Output("pop-admin-delete-patient", "is_open", allow_duplicate=True),
        Input("btn-rimuovi-paz", "n_clicks"),
        [State("pop-admin-delete-patient", "is_open")],
        prevent_initial_call= True
    )
    def gestisci_popup_admin_rimozione_paziente(n_apri, is_open):
        if n_apri is None:
            return is_open
        if n_apri:
            # toggle
            return not is_open
        return is_open

    # callback dei pulsanti dentro il popup per confermare o meno la cancellazione di un paziente
    @app.callback(
    Output("contenitore-lista-pazienti", "children"),
    Output("pop-admin-delete-patient", "is_open"),
    Input("btn-delete-paz-confirm-YES", "n_clicks"),
    Input("btn-delete-paz-confirm-NO", "n_clicks"),
    State("store-id-paziente", "data"),
    prevent_initial_call=True
    )
    def rimozione_aggiornamento_lista_popup(n_clicks_yes, n_clicks_no, id_paziente):
        """gestisce la rimozione del paziente, aggiornando la lista."""

        # click sul pulsante "No"
        if n_clicks_no:
            return dash.no_update, False

        # click sul pulsante "Sì"
        if n_clicks_yes:
                model.Admin.elimina_paziente(id_paziente)                           # elimina dal DB
                nuova_lista = view.render_lista_pazienti(model.get_all_pazienti())  # aggiorna la lista in modo da togliere l'eliminato. N.B. Manca togliere l'eliminato anche dalla card a destra!
                return nuova_lista, False
        
        return dash.no_update, False
        
    
#*************************************************************************************************************************
# sacre callback      
#callback di gestione della chat:
    @app.callback(
            Output("lista-contatti", "children"),
            Input("url","pathname")
    )
    def aggiorna_lista_contatti(path):
        if path=="/chat":
            return view.layout_lista_contatti()
        else:
            return dash.no_update
        
    @app.callback(
        Output("nome-contatto","data"),
        Input({"type": "btn-contatto","index": dash.ALL},"n_clicks"),
        prevent_initial_call=True
    )
    def seleziona_chat(n_clicks):
        ctx = dash.callback_context
        if not ctx.triggered : return dash.no_update
        id_contatto = json.loads(ctx.triggered[0]["prop_id"].split(".")[0])["index"]
        return id_contatto
    
    @app.callback(
    [
        Output("chat-box", "children"),
        Output("nome-contatto","children")
    ],
    [
        Input({"type": "btn-contatto", "index": dash.ALL}, "n_clicks"),  # Pulsante contatto
        Input("send-btn", "n_clicks")  # Pulsante invio messaggio
    ],
    [
        State("input-text", "value"),
        State("nome-contatto", "data")
    ],
    prevent_initial_call=True
    )
    def update_chat(btn_clicks, send_clicks, messaggio, id_contatto):
        triggered_id = ctx.triggered_id  # Capisci quale input ha attivato la callback

        # Caso 1: Click su un contatto (prima si fa un check per capire se il trigger è un dizionario)
        if isinstance(triggered_id, dict) and triggered_id["type"] == "btn-contatto":
            return view.layout_lista_messaggi(model.get_messaggi(model.get_user_id(), triggered_id["index"])), model.get_nomecognome(triggered_id["index"])

        # Caso 2: Click su "Invia messaggio"
        elif triggered_id == "send-btn" and messaggio:
            model.insert_messaggio(model.get_user_id(), id_contatto, messaggio)
            return view.layout_lista_messaggi(model.get_messaggi(model.get_user_id(), id_contatto)), model.get_nomecognome(id_contatto)       
        return dash.no_update
    

    # CALLBACK PER IL MODAL E PULSANTE CHE MODIFICA DATI PAZIENTE

    @app.callback(
    Output("popup-modifica-dati-paziente", "is_open"),
    [Input("btn-modifica-dati-paz", "n_clicks"),
     Input("btn-annulla-modifiche-paziente", "n_clicks")],  
    [State("popup-modifica-dati-paziente", "is_open")],
    prevent_initial_call=True
    )
    def toggle_popup_modifica_paziente(apri, annulla, is_open):
        
        # apre modal se click sul "Modifica Dati Paziente"
        if ctx.triggered_id == "btn-modifica-dati-paz":
            return True
        # chiude il modal
        elif ctx.triggered_id == "btn-annulla-modifiche-paziente":
            return False
        return is_open


    @app.callback(
    Output("modifica-paziente-alert", "children"),
    Output("interval-update-card", "disabled", allow_duplicate=True), 
    Input("btn-salva-modifiche-paziente", "n_clicks"),
    Input("btn-annulla-modifiche-paziente", "n_clicks"),
    State("modifica-nome", "value"),
    State("modifica-cognome", "value"),
    State("modifica-email", "value"),
    State("modifica-telefono", "value"),
    State("modifica-indirizzo", "value"),
    State("modifica-citta", "value"),
    State("modifica-cap", "value"),
    State("store-id-paziente", "data"),
    prevent_initial_call=True
    )
    def modifica_dati_paziente(salva_clicks, annulla_clicks, nome, cognome, email, telefono, indirizzo, citta, cap, id_paziente):
        
        trigger_id = ctx.triggered_id

        if trigger_id == "btn-annulla-modifiche-paziente":
            raise dash.exceptions.PreventUpdate

        try:
            # chiamata alla funzione di query con tutti i parametri presi dagli state del form nel modal
            model.modifica_dati_paziente_db(
                id_paziente=id_paziente,
                nome=nome,
                cognome=cognome,
                email=email,
                telefono=telefono,
                indirizzo=indirizzo,
                citta=citta,
                cap=cap
            )
            # si da il feedback e si aggiorna la card direttamente.
            dati_paziente = model.get_dettagli_paziente(id_paziente)
            dati_diabetolo_associato = model.get_dettagli_diabetologo(dati_paziente.get("diabetologo_associato"))

            return dbc.Alert("Dati aggiornati con successo", color="success", dismissable=True), False
            
        except Exception as e:
            return dbc.Alert(f"Errore durante l'aggiornamento: {str(e)}", color="danger", dismissable=True), True
    

    @app.callback(
    Output("dettagli-paziente", "children",allow_duplicate=True),
    Output("interval-update-card", "disabled", allow_duplicate=True),
    Input("interval-update-card", "n_intervals"),
    State("store-id-paziente", "data"),
    prevent_initial_call=True
    )
    def aggiorna_card_dopo_delay(n_intervals, id_paziente):
        if n_intervals == 0:
            raise dash.exceptions.PreventUpdate

        dati_paziente = model.get_dettagli_paziente(id_paziente)
        dati_diabetologo = model.get_dettagli_diabetologo(dati_paziente.get("diabetologo_associato"))
        
        return view.crea_card_paziente(dati_paziente, dati_diabetologo), True



    @app.callback(
    Output("pop-admin-grafico-diabetologo", "is_open"),
    Input("btn-graf-paz-assoc-diab", "n_clicks"),
    State("pop-admin-grafico-diabetologo", "is_open")
    )
    def gestisci_popup_admin_graf_diabetologo(n_apri, is_open):
        """Apertura e chiusura del popup dei grafici dei diabetologi."""
        if n_apri is None:
            return is_open
        if n_apri:
            return not is_open
        return is_open
    

    @app.callback(
    Output("contenitore-popup-graf-diabetologo", "children"),
    Input("btn-graf-paz-assoc-diab", "n_clicks"),
    State("store-id-diabetologo", "data"),
    prevent_initial_call=True
    )
    def aggiorna_grafico_diabetologo(n_clicks, id_diabetologo):
        """Carica il grafico dei pazienti associati ad un dato diabetologo."""
        if not n_clicks or id_diabetologo is None:
            return "Seleziona un diabetologo e premi il bottone per vedere il grafico."

        fig = model.visualizza_media_glicemia_pazienti_diabetologo(id_diabetologo)

        # modo poco elegante di controllare se ci sono dati sensati, ma funziona
        if fig.layout.title.text == "Diabetologo non trovato":
            return dbc.Alert("Diabetologo non trovato.", color="danger", dismissable=False)
        
        if fig.layout.title.text == "Nessun dato glicemico disponibile":
            return dbc.Alert("Nessun dato glicemico.", color="danger", dismissable=False)

        return dcc.Graph(figure=fig, style={"borderRadius": "5px", "padding": "10px"})


    ########

    @app.callback(
    Output("pop-admin-delete-diab", "is_open", allow_duplicate=True),
    Input("btn-rimuovi-diab", "n_clicks"),
    State("pop-admin-delete-diab", "is_open"),
    prevent_initial_call=True
    )
    def gestisci_popup_admin_rimozione_diab(n_apri, is_open):
        """Apertura e chiusura del popup di eliminazione dei diabetologi."""
        if n_apri is None:
            return is_open
        if n_apri:
            return not is_open
        return is_open


    @app.callback(
    Output("contenitore-lista-diabetologi", "children"),
    Output("pop-admin-delete-diab", "is_open"),
    Input("btn-delete-diab-confirm-YES", "n_clicks"),
    Input("btn-delete-diab-confirm-NO", "n_clicks"),
    State("store-id-diabetologo", "data"),
    prevent_initial_call=True
    )
    def rimozione_aggiornamento_lista_popup_diab(n_clicks_yes, n_clicks_no, id_diabetologo):
        """Rimuove il diabetologo dal database e aggiorna la lista."""
        # Click su "No"
        if n_clicks_no:
            return dash.no_update, False

        # Click su "Sì"
        if n_clicks_yes:
            model.Admin.elimina_diabetologo(id_diabetologo)
            nuova_lista = view.render_lista_diabetologi(model.get_all_diabetologi())
            return nuova_lista, False

        return dash.no_update, False
    


    @app.callback(
    Output("pop-admin-lista-pazienti-ass", "is_open"),
    Input("btn-lista-paz-assoc-diab", "n_clicks"),
    State("pop-admin-lista-pazienti-ass", "is_open"),
    prevent_initial_call=True
    )
    def toggle_modal(n_clicks, is_open):
        if n_clicks:
            return not is_open
        return is_open
    
    @app.callback(
    Output("contenitore-popup-lista-paz-diabetologo", "children", allow_duplicate= True),
    Input("btn-lista-paz-assoc-diab", "n_clicks"),
    State("store-id-diabetologo", "data"),      
    prevent_initial_call=True
    )
    def mostra_lista_pazienti_assoc(n_clicks, id_diabetologo):
        if not id_diabetologo:
            return html.Div("Errore: ID diabetologo mancante.")

        lista_pazienti = model.visualizza_pazienti_associati_singolo_diab(id_diabetologo)

        return view.genera_lista_pazienti_associati(lista_pazienti)
    

    # CALLBACK PER IL MODAL E PULSANTE CHE MODIFICA DATI DIABETOLOGO
    
    @app.callback(
    Output("popup-modifica-dati-diabetologo", "is_open"),
    Input("btn-modifica-dati-diab", "n_clicks"),
    Input("btn-annulla-modifiche-diabetologo", "n_clicks"),
    State("popup-modifica-dati-diabetologo", "is_open"),
    prevent_initial_call=True
    )
    def toggle_popup_modifica_diabetologo(apri, annulla, is_open):
        trigger_id = ctx.triggered_id
        if trigger_id == "btn-modifica-dati-diab":
            return True
        elif trigger_id == "btn-annulla-modifiche-diabetologo":
            return False
        return is_open


    @app.callback(
    Output("modifica-diabetologo-alert", "children"),
    Output("interval-update-diabetologo", "disabled"),
    Input("btn-salva-modifiche-diabetologo", "n_clicks"),
    Input("btn-annulla-modifiche-diabetologo", "n_clicks"),
    State("modifica-nome", "value"),
    State("modifica-cognome", "value"),
    State("modifica-email", "value"),
    State("modifica-telefono", "value"),
    State("modifica-indirizzo", "value"),
    State("modifica-citta", "value"),
    State("modifica-cap", "value"),
    State("store-id-diabetologo", "data"),
    prevent_initial_call=True
    )
    def modifica_dati_diabetologo(salva_clicks, annulla_clicks, nome, cognome, email, telefono, indirizzo, citta, cap, id_diabetologo):
        trigger_id = ctx.triggered_id

        if trigger_id == "btn-annulla-modifiche-diabetologo":
            raise dash.exceptions.PreventUpdate

        try:
            model.modifica_dati_diabetologo_db(
                id_diabetologo=id_diabetologo,
                nome=nome,
                cognome=cognome,
                email=email,
                telefono=telefono,
                indirizzo=indirizzo,
                citta=citta,
                cap=cap
            )

            # do il feedback e aggiorno la card diabetologo
            return dbc.Alert("Dati aggiornati con successo", color="success", dismissable=True), False
        except Exception as e:
            return dbc.Alert(f"Errore durante l'aggiornamento: {str(e)}", color="danger", dismissable=True), True
        

    @app.callback(
    Output("dettagli-diabetologo", "children", allow_duplicate=True),
    Output("interval-update-diabetologo", "disabled", allow_duplicate=True),
    Input("interval-update-diabetologo", "n_intervals"),
    State("store-id-diabetologo", "data"),
    prevent_initial_call=True
    )
    def aggiorna_card_diabetologo_dopo_delay(n_intervals, id_diabetologo):
        if n_intervals == 0:
            raise dash.exceptions.PreventUpdate

        dati_diabetologo = model.get_dettagli_diabetologo(id_diabetologo)
        return view.crea_card_diabetologo(dati_diabetologo), True
        
