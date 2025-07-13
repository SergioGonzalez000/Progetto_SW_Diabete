import datetime
from dash import dcc, html
import dash_bootstrap_components as dbc
import model
import control
from flask_login import UserMixin, login_user, logout_user, current_user 


# Layout dell'app, intero. Si aggiorna quando viene cambiato l'url.
def getLayout():
    return html.Div(
        [
            dcc.Location(id="url", refresh=True),
            # sidebar fissa, laterale sinistra
            sidebar,
            #fil-serve per non far fallire una callback -> forse si può risolvere in un altro modo
            dcc.Store(id="selected-patient-id",data=None),
            dcc.Store(id="terapia-selezionata", data=None),

            # interval per il modal "modifica terapia"
            dcc.Interval(
                id='interval-chiudi-modal-terapia',
                interval=2000,  
                n_intervals=0,
                disabled=True,
                max_intervals=1
            ),
            dcc.Store(id="store-valore-dropdown"),
            dcc.Store(id="store-reset-attivo", data=False),

            # interval per il modal "nuova terapia"
            dcc.Interval(
                id="interval-chiudi-modal-nuova-terapia",
                interval=1500,  
                n_intervals=0,
                disabled=True,
                max_intervals=1
            ),
            dcc.Store(id='store-refresh-terapie', data=0),
            
            # Contenuto della pagina:
            html.Div(id="page-content", style={"display" : "flex", "width" : "100vw", "height" : "auto"})
        ],
        style={
            "display": "flex",
            # Page content e navbar occupano l'intera altezza della pagina
            "minHeight": "100vh",
            # Colore sfondo standard fisso
            #"background-color": "#e6f2ff", #c2dfff 
            'background': 'linear-gradient(to bottom right, #dfffe0 0%, #e6f2ff 60%, #c2dfff 100%)',
            # Nessun margine al contenuto affinché occupi tutta la pagina disponibile
            "margin": 0
        }
    )

# ******************************************************************************************************************

# Links di navigazione per gli ospiti
guest_navlinks = dbc.Nav(
    [
        # Link per la pagina iniziale
        dbc.NavLink("Home", href="/", active="exact", className="mb-4 font-25"),
        # Link della pagina della chat
        dbc.NavLink("Login", href="/login", active="exact", className="mb-4 font-25"), 
        # Link per la pagina dei pazienti
        dbc.NavLink("Registration", href="/registration", active="exact", className="mb-1.5 font-25"),
        html.Hr() 
    ],
    # Disposizione dei NavLink in verticale
    vertical=True,
    # I Link sono racchiusi in un contenitore a pillola
    pills=True,
)

# Link di navigazione per i pazienti
patient_navlinks = dbc.Nav(
    [
        # Link della home/dashboard
        dbc.NavLink("Dashboard", href="/patient-dashboard", active="exact", className="mb-4 font-25"),
        # Link per la pagina di grafici
        dbc.NavLink("Overview", href="/grafici", active="exact", className="mb-4 font-25"),
        # Link della pagina della chat
        dbc.NavLink("Chat", href="/chat", active="exact", className="mb-1.5 font-25"),
        html.Hr(),
        # Link per il logout
        html.A("Log out", href="/logout", className="text-danger")
    ],
    # Disposizione dei NavLink in verticale
    vertical=True,
    # I Link sono racchiusi in un contenitore a pillola
    pills=True
)

# Links di navigazione per i dottori
doctor_navlinks = dbc.Nav(
    [
        # Link per la pagina iniziale
        dbc.NavLink("Dashboard", href="/doctor-dashboard", active="exact", className="mb-4 font-25"),
        # Link per la pagina dei pazienti
        dbc.NavLink("Pazienti", href="/doctor-patient", active="exact", className="mb-4 font-25"),
        # Link della pagina della chat
        dbc.NavLink("Chat", href="/chat", active="exact", className="mb-1.5 font-25"),
                html.Hr(),
        # Link per il logout
        html.A("Log out", href="/logout", className="text-danger")
    ],
    # Disposizione dei NavLink in verticale
    vertical=True,
    # I Link sono racchiusi in un contenitore a pillola
    pills=True
)

# Links di navigazione per l'admin

admin_navlinks = dbc.Nav(
    [
        # Link per la pagina iniziale
        dbc.NavLink("Overview", href="/admin-dashboard", active="exact", className="mb-4 font-25"),
        # Link della pagina della chat
        dbc.NavLink("Richieste", href="/request", active="exact", className="mb-4 font-25"), 
        # Link per la pagina dei pazienti
        dbc.NavLink("Pazienti", href="/admin-patient", active="exact", className="mb-4 font-25"),
        # Link per la pagina dei diabetologi
        dbc.NavLink("Diabetologi", href="/admin-doctor", active="exact", className="mb-1.5 font-25"),
        html.Hr(),
        # Link per il logout
        html.A("Log out", href="/logout", className="text-danger")       
    ],
    # Disposizione dei NavLink in verticale
    vertical=True,
    # I Link sono racchiusi in un contenitore a pillola
    pills=True
)

# SIDEBAR 
sidebar = html.Div(
    [
        # Titolo
        html.H1("DiaLog", className="b-gradient-text"),
        html.Hr(),

        # Per testare è fissa quella del paziente, da modificare con la callback in base al tipo di utente
        # patient_navlinks,
        html.Div(id="navlinks"),

        html.P("v1.3.2-beta", style={'margin-top': 'auto'}, className='text-primary font-18')
    ],
    style={
        "top": 0,
        "left": 0,
        "bottom" : 0,
        # Larghezza scelta fissa a 250px
        "width": "250px",
        # Il primo (2rem) è il padding verticale, il secondo (1rem) è quello orizzontale
        "padding": "2rem 1rem",
        # colore sfondo:
        "backgroundColor" : "white",
        "border": "1px solid #dee2e6",
    },
    className='flex-col rounded-15'
)

# ******************************************************************************************************************
# LAYOUT PER GLI OSPITI
# 1. Home
# 2. Login
# 3. Registration
# ******************************************************************************************************************

# HOME GUEST
def home(): 
    return html.Div(
    className='f-1 flex-col p-40 g-30',
    children=[
        
        #Prima riga:
        html.Div(
          className='f-1 flex-row',
          children=[
              # Numero Pazienti model.get_num_pazienti()
               html.Div(
                    [
                        html.Div(
                            [
                                html.P(model.get_num_pazienti(), id='num-pazienti', className='centered font-115 font-bold' ),
                                html.P("Pazienti",  className='centered font-25 font-bold mt-0')
                            ]
                        )
                    ],
                    className='f-1 centered flex-col b-gradient-text'
              ),

              # Presentazione
                html.Div(
                    [
                        html.P("DiaLog", className='font-85 centered font-bold text-primary b-gradient-text mb-0'),
                        html.P("🠈 Uniti nella cura 🠊", className='centered font-25 font-bold b-gradient-text mt-0 mb-4'),
                        html.P("Mettiamo in comunicazione i diabetologi con chi ne ha bisogno!", className='font-25 center')
                    ],
                    className='f-1 flex-col centered'
                ),

              # Numero diabetologi model.get_num_diabetologi()
                html.Div(
                    [
                        html.P(model.get_num_diabetologi(), id='num-dottori', className='centered font-115 font-bold' ),
                        html.P("Dottori",  className='centered font-25 font-bold mt-0')
                    ],
                    className='f-1 centered flex-col b-gradient-text'
                )
          ]
        ),

        # Seconda riga:
        html.Div(
          className='f-2',
          children=[
                # Immagini dell'app:
                dbc.Carousel(
                    items=[
                        {"key": "1", "src": "/assets/img1.png", "img_style":{"max-height": "565px"}},
                        {"key": "2", "src": "/assets/img2.png", "img_style":{"max-height": "565px"}},
                        {"key": "3", "src": "/assets/img3.png", "img_style":{"max-height": "565px"}},
                        {"key": "4", "src": "/assets/img4.png", "img_style":{"max-height": "565px"}},
                        {"key": "5", "src": "/assets/img5.png", "img_style":{"max-height": "565px"}},                        
                    ],
                    controls=True,
                    indicators=True,
                    interval=4000,
                    # ride="carousel",
                    variant="dark",
                    className='carousel'
                )
          ]
        )
    ],
)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

# LOGIN NUOVO:

login_title = html.H1(
    "Accedi",
    style={"textAlign": "center"},
    # margin bottom 3
    className="mb-3"
)
    
# Layout per lo username
# ID = "username-input"
username_box = html.Div(
    [
        html.H5("Username"),
        dbc.FormFloating(
            [
                # Il placeholder è necessario per il corretto funzionamento di FormFloating() anche se non visibile
                dbc.Input(type="text", id="username-input", placeholder="Username", className='input'),
                dbc.Label("Username"),
            ]
        )
    ],
    # margin bottom 3
    className="mb-3"
)

    # Layout per la password
    # ID = "password-input"
password_box = html.Div(
    [
        html.H5("Password"),
        dbc.FormFloating(
        [
            # Il placeholder è necessario per il corretto funzionamento di FormFloating() anche se non visibile
            dbc.Input(type="password", id="password-input", placeholder="Password", className='input'),
            dbc.Label("Password"),
        ])           
    ],
    # margin bottom 4, qui è a 4 per rendere esteticamente più carino
    className="mb-4"
)

# Pulsante Sign In
# ID = "login-input"
signIn_button = html.Div(
    dbc.Button("Accedi", id="login-input", size="lg", n_clicks=0, style={'border-radius':'35px'}, className='button'),
    style={'marginTop': '30px'}
)

# Sign Up link: Link per la pagina di registrazione qualora non si avesse ancora un account
signUp_link = html.Div([
    html.Span("Non hai un account? "),
    html.A(
        "Registrati",
        # Rimanda al link "/register" dove c'è la pagina con i form di registrazione
        href="/registration",
        className="text-primary"
        )
    ],
    # Padding da sopra di 2
    className="mt-4"
)

# div per gli alert 
output_box = html.Div(
    id='output-box'
)


# Layout del form
form = dbc.Form(
    [
        # Titolo
        login_title,
        # Box per lo username
        username_box,
        # Box per la password
        password_box,
        # Pulsante di Login
        signIn_button,
        # Link per la registrazione
        signUp_link,
        # div per gli alert
        output_box
    ])


# PAGE CONTENT PER IL LOGIN
login = html.Div(
    [
        html.Div(
            form,
            className='form-card'
        )
    ],
    className='f-1 centered'
)


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# REGISTRATION - NUOVO

# Titolo
registration_title = html.H1(
    "Registrati",
    style={"textAlign": "center"},
    # margin bottom 3
    className="mb-3"
)

# Form dei dati Anagrafici
# ID = "radio-user", "name-input", "surname-input", "codiceFiscale-input", "dataNascita-input", "radio-sesso", "next-button"
form1 = html.Div(
    [
        # Scelta paziente o diabetologo
        dbc.Row(
            dbc.Col(
                dbc.RadioItems(
                    id="radio-user",
                    options=[
                        {"label": "Paziente", "value": "P"},
                        {"label": "Diabetologo", "value": "D"},
                    ],
                    value="P",
                    inline=True,
                    labelClassName="me-3"
                ),
                width="auto"
            ),
            justify="center"
        ),
        # Riga di Nome + Cognome
        dbc.Row([
            dbc.Col(
                dbc.FormFloating(
                    [
                        dbc.Input(type="text", id="name-input", placeholder="Name",  className='input'),
                        dbc.Label("Nome"),
                    ]
                ),
                width=6 # Metà della riga
            ),
            dbc.Col(
                dbc.FormFloating(
                    [
                        dbc.Input(type="text", id="surname-input", placeholder="Surname",  className='input'),
                        dbc.Label("Cognome")
                    ]
                ),
                width=6 # Metà della riga
            )
        ],
        className="mt-4 mb-4"
        ),
        # Riga del Codice Fiscale
        dbc.FormFloating(
            [
                dbc.Input(type="text", id="codiceFiscale-input", placeholder="Codice Fiscale",  className='input'),
                dbc.Label("Codice Fiscale")
            ],
            className="mb-4"
        ),
        # Riga data di Nascita
        dbc.FormFloating(
            [
                dbc.Input(type="date", id="dataNascita-input", placeholder="Data di Nascita", className='input'),
                dbc.Label("Data di Nascita")
            ],
            className="mb-4"
        ),
        # Scelta del sesso
        dbc.Row(
            dbc.Col(
                dbc.RadioItems(
                    id="radio-sesso",
                    options=[
                        {"label": "Maschio", "value": "M"},
                        {"label": "Femmina", "value": "F"},
                    ],
                    value="M",
                    inline=True,
                    labelClassName="me-3"
                ),
                width="auto"
            ),
            justify="center"
        ),
        # Link per il Login
        html.Div(
            [
                html.Span("Hai già un account? "),
                html.A(
                    "Accedi",
                    href="/login",
                    className="text-primary"
                )
            ],
            className="mt-4"
        ),
    ],
    id="form1",
    style={"display": "block"}
)

# Form dei dati di contatto
# ID = "tel-input", "email-input", "indirizzo-input", "city-input", "CAP-input", "prev-button"
form2 = html.Div(
    [
        # Telefono
        dbc.FormFloating(
            [
                dbc.Input(type="tel", id="tel-input", placeholder="Telefono",  className='input'),
                dbc.Label("Telefono")
            ],
            className="mb-4"
        ),
        # Email
        dbc.FormFloating(
            [
                dbc.Input(type="email", id="email-input", placeholder="Email",  className='input'),
                dbc.Label("Email")
            ],
            className="mb-4"
        ),
        # Indirizzo
        dbc.FormFloating(
            [
                dbc.Input(type="text", id="indirizzo-input", placeholder="Indirizzo",  className='input'),
                dbc.Label("Indirizzo")
            ],
            className="mb-4"
        ),
        # Riga di Città + Cap
        dbc.Row(
            [
                dbc.Col(
                    dbc.FormFloating([
                        dbc.Input(type="text", id="city-input", placeholder="Città",  className='input'),
                        dbc.Label("Città")
                    ]),
                    width=7    
                ),
                dbc.Col(
                    dbc.FormFloating([
                        dbc.Input(type="number", id="CAP-input", placeholder="CAP",  className='input'),
                        dbc.Label("CAP")
                    ]),
                    width=5
                )
            ],
            className="mb-4"
        ),
        # Link per il Login
        html.Div(
            [
                html.Span("Hai già un acccount? "),
                html.A(
                    "Login",
                    href="/login",
                    className="text-primary"
                )
            ],
            className="mt-2"
        ),
    ],
    id="form2",
    style={"display": "none"}
)

# Form Utente + password
# ID: "generated-username", "scelta-password", "conferma-password", "registration-input"
form3 = html.Div(
    [
        # Scelta password
        dbc.FormFloating(
            [
                dbc.Input(type="password", id="scelta-password", placeholder="Password",  className='input mb-4'),
                dbc.Label("Scegli una password")
            ],
        ),
        # Conferma password
        dbc.FormFloating(
            [
                dbc.Input(type="password", id="conferma-password", placeholder="Password", className='input mb-4'),
                dbc.Label("Conferma password")
            ]
        ),

        # Pulsante di registrazione
        html.Div(
            dbc.Button("Registrati", id="registration-input", size="lg",  style={'border-radius':'35px'}, n_clicks=0, className='button mb-3')
        ),

        # Link per il Login
        html.Div(
            [
                html.Span("Hai gia un account? "),
                html.A(
                    "Login",
                    href="/login",
                    className="text-primary"
                )
            ],
        ),

        # Username generato
        dbc.Card(
            [
                html.H5("Username generato:", className='gray'),
                dbc.CardBody(
                    [
                        html.P(id="generated-username")
                    ]
                )
            ], className='mt-3 mb-3'
        ),

        # Avviso:
        html.Small(
            "Attenzione: lo username apparirà solo quando la tua richiesta verrà accettata. Potrebbe volerci qualche minuto.",
            style={
                'color': 'red'
            },
            className='mb-3'
        )
    ],
    id="form3",
    style={"display": "none"}
)

# Pulsanti per la navigazione 
nav_buttons = html.Div(
    [
        dbc.Button("🡨", id="prev-button", n_clicks=0, disabled=True, style={"visibility": "hidden"}, className='rounded-25'),  # inizialmente questo pulsante sarà nascosto (nel form 1)
        dbc.Button("🡪", id="next-button", n_clicks=0, className='rounded-25')
    ],
    className="mt-3 d-flex justify-content-between"
)

# Box per il Form
# ID = "form-box"
form_box = html.Div(
    children=[
        form1,
        form2,
        form3
    ]
)

# Box per gli alert
registration_feedback = html.Div(
    dbc.Alert(id="registration-feedback", is_open=False, className="mt-3")
)

# CARD DI REGISTRAZIONE
registration = html.Div(
    [
        html.Div([
            registration_title,
            # Box per il form
            form_box,
            # Pulsanti per la navigazione
            nav_buttons,
            # Box per l'output
            registration_feedback,
            dcc.Store(id="form-step", data= 1),  # aggiunto per far comparire il pulsante "indietro" solo nei form 2 e 3
            ],
            className='form-card'
        ),
    ],
    className='f-1 centered'
)

# ******************************************************************************************************************
# LAYOUT DEL PAZIENTE:
# 1. Dashboard
# 2. Grafici
# 3. Chat
# ******************************************************************************************************************
#popover generale che viene riutilizzato nelle altre parti della view
def info_popover(button_id, popover_id, contenuto, title="Informazioni"):
    return html.Div([
        dbc.Button("i", id=button_id, color="light", style={
            "borderRadius": "50%",
            "width": "24px",
            "height": "24px",
            "padding": "0",
            "textAlign": "center",
            "lineHeight": "1",
            "fontSize": "12px"
        }),
        dbc.Popover(
            dbc.PopoverBody([
                html.H6(title),
                contenuto
            ]),
            target=button_id,
            body=True,
            trigger="click",
            placement="right",
            id=popover_id
        )
    ], style={
        "display": "flex",
        "alignItems": "center",
        "gap": "5px",
        "marginBottom": "10px"
    })

# DASHBOARD DEL PAZIENTE

patient_dashboard = html.Div(
    className='f-1 flex-row g-40 p-30',
    children=[
        # Layout finale:
        # _____________
        # | 3 | 4 |   |
        # |___|___|   |
        # |   5   | 6 |
        # |_______|___|
        #     1     2
        # Colonna a sinistra 1 (divisa in due righe)
        dcc.Store(id="trigger-aggiorna-grafico", data=0),
        html.Div(
            className= 'f-2 flex-col g-30',
            children=[
                # _________
                # | 3 | 4 |
                # |___|___|
                #
                # Prima riga della colonna centrale:
                html.Div(
                    className='f-1 d-flex g-30',
                    children=[
                        # 3 : Card paziente
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Paziente: ", className='gray'),
                                html.Hr(),
                                html.Div(id="info-paz",),
                            ]
                        ),

                        # 4 :Card Terapia
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Terapia: ", className='gray'),
                                html.Hr(),
                                html.Div(id="terapie-paz"),
                            ]
                        )
                    ]
                ),

                #  _______
                # |   5   |
                # |_______|
                #
                # Seconda riga colonna centrale:
                html.Div(
                    className='f-1 d-flex',
                    children=[
                        # 5: Card del grafico
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Grafico:", className='gray'),
                                html.Hr(),
                                html.Div(id="andamento-giornaliero"),
                            ]
                        )
                    ]
                )
            ]
        ),
        
        # _____
        # |   |
        # |   |
        # | 6 |
        # |___|
        #
        # 6: Colonna a destra 
        html.Div(
            className="card",
            style={'height': '100%'},
            children=[
                html.H5("Glicemia:", className='gray'),
                html.Hr(),

                # Cerchio della glicemia
                html.Div(
                    className="circle-slot",
                    children=[
                        html.Div(
                            className="outer",
                            style={"background" : "linear-gradient(to bottom right, #B3B3B3, #808080)"},
                            id="cerchio-colorato",
                            children=[
                                html.Div(
                                    className="inner",
                                    children=[
                                        html.Div("0", id="number"),
                                        html.H6("mg/dl", className='gray')
                                    ]
                                )
                            ]
                        ),
                    ]
                ),

                # Input glicemia
                html.H6("Nuova misurazione:", className='gray'),
                dcc.Input(
                    placeholder="Inserisci glicemia...",
                    type="number",
                    id="input-glicemia",
                    debounce=True,
                    n_submit=0,
                    className="input mb-3"
                ),
                

                html.H6("Sintomi riscontrati:", className='gray'),
                # Input Annotazione sintomi
                # Input glicemia
                dcc.Input(
                    id="input-sintomi-riscontrati",
                    placeholder="Sintomi (fac.)...",
                    type="text",
                    className="input mb-3"
                ),
                dcc.RadioItems(
                    id="pre-post-pasto",
                    options=[
                        {'label': 'Pre pasto', 'value': 'pre'},
                        {'label': 'Post pasto', 'value': 'post'}
                    ],
                    value='pre',
                    labelStyle={'display': 'inline-block', 'margin-right': '15px'},
                    inputStyle={"margin-right": "5px"},
                    style={"textAlign": "center"}
                ),
                dbc.Button("Aggiorna Glicemia",id="inserisci-glicemia",n_clicks=0,
                            class_name="mt-3 n-border rounded-25 font-20"
                        ),
                dbc.Alert(id="inserisci-glicemia-output",is_open=False,duration=5000),
                html.Hr(),
                html.Div(
                    [
                        html.H6("Assunzione farmaco:", className='gray'),
                        dbc.Row(
                            [
                                dbc.Col(
                                # Inserimento del nome del farmaco
                                    dcc.Input(
                                        id="input-farmaco-usato",
                                        placeholder="Inserisci farmaco...",
                                        type="text",
                                        className= 'input'
                                    ),
                                    width=7
                                ),

                                dbc.Col(
                                    # Inserimento del dosaggio
                                    dcc.Input(
                                        id="input-dosaggio-usato",
                                        placeholder="Dosaggio (mg)...",
                                        type="text",
                                        className= 'input'  
                                    ),
                                    width=5
                                )
                            ],
                            className="mb-3"
                        ),
                    ]
                ),
                dbc.Button("Inserisci assunzione", id="inserisci-assfarmaco-btn", n_clicks=0, 
                            class_name="mt-2 n-border rounded-25 font-20"
                        ),
                # Feedback
                dbc.Alert(id="output-assunzione", is_open=False,duration=5000),                           
            ]
        )
    ]
)

# GRAFICI DEL PAZIENTE
# _________
# | 1 | 3 |
# |___|___|
# | 2 | 4 |
# |___|___|

def filtro_temporale(grafico_id):
    return dcc.RadioItems(
        id=f"filtro-temporale{grafico_id}",
        options=[
            {'label': 'Tutto', 'value': 'tutto'},
            {'label': 'Annuale', 'value': 'annuale'},
            {'label': 'Mensile', 'value': 'mensile'},
            {'label': 'Settimanale', 'value': 'settimanale'},
            {'label': 'Giornaliero', 'value': 'giornaliero'}
        ],
        value='tutto',
        labelStyle={'display': 'inline-block', 'margin-right': '15px'},
        inputStyle={"margin-right": "5px"},
        style={"textAlign": "center"}
    )

def filtro_calendario():
    return dbc.Row([
                            dbc.Col([
                                html.Label("Seleziona mese"),
                                dcc.Dropdown(
                                    id="selezione-mese",
                                    options=[
                                        {"label": nome, "value": num}
                                        for num, nome in enumerate(
                                            ["Gennaio", "Febbraio", "Marzo", "Aprile", "Maggio", "Giugno",
                                            "Luglio", "Agosto", "Settembre", "Ottobre", "Novembre", "Dicembre"], 1
                                        )
                                    ],
                                    value=datetime.datetime.now().month,
                                    clearable=False
                                )
                            ], width=6),
                            dbc.Col([
                                html.Label("Seleziona anno"),
                                dcc.Dropdown(
                                    id="selezione-anno",
                                    options=[
                                        {"label": str(anno), "value": anno}
                                        for anno in range(2020, datetime.datetime.now().year + 1)
                                    ],
                                    value=datetime.datetime.now().year,
                                    clearable=False
                                )
                            ], width=6),
                        ], className="mt-3"),



patient_graphs = html.Div(
    className='f-1 flex-row g-40 p-40',
    children=[
        # Prima colonna
        html.Div(
            className= 'f-1 flex-col g-40',
            children=[
                # Riquadro 1
                html.Div(
                    className='f-1 card',
                    style={'height': '100%', 'width': '100%'},
                    children=[
                        html.Div(
                            [
                                html.H5("Andamento: ", style={"margin": "0", "marginRight": "8px"}, className='gray'),
                                info_popover(
                                    button_id="popover-button-2",
                                    popover_id="popover-2",
                                    contenuto=html.Div([
                                        "Mostra i valori di glicemia registrati durante il periodo selezionato.",
                                    ])
                                )
                            ],
                            style={"display": "flex", "alignItems": "auto", "gap": "8px"}
                        ),
                        html.Div(id='first-graph', children=[]),
                        html.Br(),
                        filtro_temporale(1),
                    ],                    

                ),

                # Riquadro 2
                html.Div(
                    className='f-1 card',
                    style={'height': '100%', 'width': '100%'},
                    children=[
                        html.Div(
                            [
                                html.H5("Media:", style={"margin": "0", "marginRight": "8px"}, className='gray'),
                                info_popover(
                                    button_id="popover-button-3",
                                    popover_id="popover-3",
                                    contenuto=html.Div([
                                        "Mostra i valori medi di glicemia per fascia oraria, registrati durante il periodo selezionato.",
                                    ])
                                )
                            ],
                            style={"display": "flex", "alignItems": "auto", "gap": "8px"}
                        ),
                        html.Div(id='second-graph', children=[]),
                        html.Br(),
                        filtro_temporale(2),
                    ]
                ),
            ]
        ),

        # Seconda colonna
        html.Div(
            className= 'f-1 flex-col g-40',
            children=[
                # Riquadro 3
                html.Div(
                    className='f-1 card',
                    style={'height': '100%', 'width': '100%'},
                    children=[
                        html.Div(
                            [
                                html.H5("Eventi glucosio basso: ", style={"margin": "0", "marginRight": "8px"}, className='gray'),
                                info_popover(
                                    button_id="popover-button-4",
                                    popover_id="popover-4",
                                    contenuto=html.Div([
                                        "Calendario degli eventi di glicemia bassa.",
                                    ])
                                )
                            ],
                            style={"display": "flex", "alignItems": "auto", "gap": "8px"}
                        ),
                        html.Div(id='third-graph'),
                        html.Div(filtro_calendario())
                    ]
                ),

                # Riquadro 4
                html.Div(
                    [
                        html.Div([

                            html.H5("Nuova Segnalazione:", className='gray'),
                            html.Br(),
                            # Tipo segnalazione
                            dcc.Dropdown(
                                id="tipo-segnalazione",
                                options=[
                                    {"label": "Sintomo", "value": "sintomo"},
                                    {"label": "Terapia", "value": "terapia"},
                                    {"label": "Patologia", "value": "patologia"}
                                ],
                                placeholder="Tipo di segnalazione...",
                                className="mb-3"
                            ),

                            # Descrizione
                            dbc.Input(
                                id="descrizione-segnalazione",
                                placeholder="Descrizione...",
                                style={"width": "100%", "height": "100px"},
                                className="mb-3"
                            ),

                            # Date inizio e fine
                            dbc.Row([
                                html.H6("Data inizio - Data fine (opzionale)", style={"color": "grey"}),
                                dbc.Col(
                                    dbc.Input(
                                        id="data-inizio-segnalazione",
                                        placeholder="Data inizio",
                                        type="date",
                                        className="mb-3",
                                        style={"width": "100%"}
                                    ),
                                    width=6
                                ),
                                dbc.Col(
                                    dbc.Input(
                                        id="data-fine-segnalazione",
                                        placeholder="Data fine (opzionale)",
                                        type="date",
                                        className="mb-3",
                                        style={"width": "100%"}
                                    ),
                                    width=6
                                ),
                            ]),

                            # Bottone di invio 'padding-top':'20px', 'padding-bottom':'20px'
                            dbc.Button("Invia Segnalazione", id="invia-segnalazione-btn", n_clicks=0, style={'padding-top':'10px', 'padding-bottom':'10px', 'width':'100%'}, className='n-border rounded-25 font-20'),

                            # Feedback
                            dbc.Alert(id="output-segnalazione", is_open=False, duration=5000),
                        ],
                        style={'height': '100%', 'width': '100%'}, className='f-1')

                    ],
                    className='f-1 card flex-col',
                    style={
                        'height': '100%',
                        'width': '100%',   
                    },
                    id='fourth-graph',
                    
                ),
            ]
        )
    ]
)



# ******************************************************************************************************************
# LAYOUT DEL DIABETOLOGO:
# 1. Dashboard
# 2. Pazienti
# 3. Chat (uguale a chat pazienti)
# ******************************************************************************************************************

# DASHBOARD DIABETOLOGO
doctor_dashboard = html.Div(
    className='f-1 flex-row g-40 p-40',
    # Layout finale:
    # _____________
    # |   |       |
    # |   |___4___|
    # | 3 |   |   |
    # |___|_5_|_6_|
    #   1     2  
    children=[

        # Prima colonna che occupa 1/3
        html.Div(
            [
                html.H5("I tuoi pazienti:", className='gray'),
                html.Hr(),
                # Box per la lista dei pazienti
                html.Div( id="doctor-patient-queue", style={"height": "100%","width": "100%", "flex-direction": "column"})
            ],
            className= "card"
        ),

        # Seconda colonna che occupa 2/3
        html.Div(
            [
                # Numero 4
                html.Div(
                    [
                        html.H5("Informazioni paziente:", className='gray'),
                        html.Hr(),
                        html.Div( id="doctor-patient-info", style={"height": "100%","width": "100%"}),

                    ],
                    className="f-1 card",
                ),

                html.Div(
                    [
                        # Numero 5
                        html.Div(
                            [
                                html.H5("Profilo:", className='gray'),
                                html.Hr(),
                                # Qua va inserito il numero dei pazienti (associati)
                                html.Div(id="doctor-info")
                            ],
                            className="card"
                        ),
                        # Numero 6
                        html.Div(
                            [
                                html.H5("Andamento pazienti:", className='gray'),
                                html.Hr(),
                                # Qua va inserito un grafico
                                html.Div( id="patient-pie", style={"height": "100%","width": "100%"})
                            ],
                            className="card"
                        )
                    ],
                    className='f-1 flex-row g-40'
                )
            ],
            className='f-2 flex-col g-40'
        )
    ]
)

# PAZIENTI DIABETOLOGO
doctor_patient = html.Div(
    className='f-1 flex-row g-40 p-40',
    children=[
        
        # Prima colonna (1/3)
        html.Div(
            [
                html.H5("I tuoi pazienti:", className='gray'),
                html.Hr(),
                html.Div(
                    id="doctor-patient-queue",
                    style={"height": "100%", "width": "100%", "flex-direction": "column"}
                )
            ],
            className="card"
        ),

        # Seconda colonna (2/3)
        html.Div(
            className='f-2 flex-col g-40',
            children=[
                # Riga superiore (Paziente + Terapia)
                html.Div(
                    className='f-1 flex-row g-40',
                    children=[
                        # Box Paziente
                        html.Div(
                            [
                                html.H5("Paziente:", className='gray'),
                                html.Hr(),
                                html.Div(
                                    id="patient-info",
                                    style={"height": "100%", "width": "100%"}
                                ),
                                dcc.Store(id="selected-patient-id", storage_type="session")
                            ],
                            className="card"
                        ),

                        # Box Terapia
                        html.Div(
                            [   
                                html.H5("Terapia:", className='gray'),
                                html.Hr(),
                                # Qua va inserita la tabella delle terapie
                                html.Div( id="patient-therapy", style={"height": "100%","width": "100%"}, className='f-1'),

                                # POP-UP Nuova terapia:
                                dbc.Modal(
                                    [
                                        # Header:
                                        dbc.ModalHeader(dbc.ModalTitle("Nuova Terapia")),

                                        # Body:
                                        dbc.ModalBody([
                                            # Div di modifica della terapia:
                                            html.Div([
                                                # Div Farmaco e dosaggio: 
                                                html.Div([
                                                    # Colonna farmaco: 
                                                    html.Div([
                                                        # Nome del farmaco
                                                        html.P("Farmaco:", className='mb-0'),
                                                        dbc.Input(id="input-nuovo-farmaco", type="text", className='n-border'),
                                                    ], className= 'f-3 flex-col'),
                                                    # Colonna dosaggio:
                                                    html.Div([
                                                        # Dosaggio in mg
                                                        html.P("Dosaggio (mg):", className='mb-0'),
                                                        dbc.Input(id="input-nuovo-dosaggio", type="number", className='n-border')
                                                    ], className= 'f-1 flex-col'),
                                                ], className='f-1 flex-row mb-3 g-20'),

                                                # Assunzioni giornaliere + Indicazioni:
                                                html.Div([
                                                    # Colonna farmaco: 
                                                    html.Div([
                                                        # Assunzioni giornaliere
                                                        html.P("A. giornaliere:", className='mb-0'),
                                                        dbc.Input(id="input-nuovo-assunzioni", type="number", className='n-border'),
                                                    ], className= 'f-1 flex-col'),
                                                    # Colonna dosaggio:
                                                    html.Div([
                                                        # Indicazioni
                                                        html.P("Indicazioni:", className='mb-0'),
                                                        dbc.Input(id="input-nuovo-indicazioni", type='text', className='n-border')
                                                    ], className= 'f-3 flex-col'),
                                                ], className='f-1 flex-row mb-3 g-20'),

                                                # Div delle date:
                                                html.Div([
                                                    # Dal:
                                                    html.Div([
                                                        html.P("Dal:", className='mb-0'),
                                                        dbc.Input(id="input-nuovo-data-inizio", type='date', min=control.get_today(), value=control.get_today() , className='n-border rounded-15'),
                                                    ], className= 'f-1 flex-col'),
                                                    # Al:
                                                    html.Div([
                                                        html.P("Al:", className='mb-0'),
                                                        dbc.Input(id="input-nuovo-data-fine", type='date', min=control.get_today(), value=control.get_today(), className='n-border rounded-15'),
                                                    ], className= 'f-1 flex-col')
                                                ], className='f-1 flex-row mb-3 g-20'),

                                                # Box per gli alert:
                                                dbc.Alert(id="aggiungi-terapia-output", is_open=False, duration= 1500)
                                            ],
                                            style={'padding': '5px'},
                                            className= 'f-3 flex-col rounded-15 l-gray'),
                                            
                                        ]),
                                        dbc.ModalFooter([
                                            # Pulsante per salvare le modifiche
                                            dbc.Button("Salva", id="salva-nuova-terapia-btn", n_clicks=0, color='success', className='n-border rounded-25'),
                                            # Pulsante per annullare e uscire
                                            dbc.Button("Annulla", id="chiudi-nuova-terapia", color='warning', className='n-border rounded-25'),
                                        ], className= 'flex-row g-10'
                                        )
                                    ],
                                    id="popup-nuova-terapia",
                                    centered=True,
                                    is_open=False,
                                ),
    
                            ],
                            className="card",
                            style={'height': '100%'}
                        )
                    ]
                ),
                
                # modal fittizio.
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle(id="modal-title")),
                        dbc.ModalBody([
                            html.H4(id="modal-nome-eta"),
                            html.H6(id="modal-codice-fiscale", className='gray'),
                            dbc.Textarea(id="input-patologie", value="", style={"width": "100%", "height": "80px"}),
                            dbc.Input(id="input-rischio", type="text", value=""),
                            dbc.Input(id="input-comorb", type="text", value=""),
                            dbc.Alert(id="modifica-info-output", is_open=False),
                            dcc.Interval(id="interval-salva-info-paziente", interval=1500, n_intervals=0, max_intervals=1, disabled=True),
                        ]),
                        dbc.ModalFooter([
                            dbc.Button("Annulla", id="close-modifica-infopaz", style={'background-color':'red'}),
                            dbc.Button("Salva", id="salva-modifiche-btn", n_clicks=0, style={'background-color':'green'}),
                        ]),
                    ],
                    id="modal-modifiche-btn",
                    centered=True,
                    is_open=False
                ),

                # Riga inferiore (Grafico)
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Grafico:", style={"margin": "0", "marginRight": "8px"}, className='gray'),
                                info_popover(
                                    button_id="popover-button-1",
                                    popover_id="popover-1",
                                    contenuto=html.Div([
                                        "Mostra i valori di glicemia registrati durante il periodo selezionato.",
                                        html.Br(),
                                        html.H6("Media giornaliera:"),
                                        "La media è calcolata su fasce orarie."
                                    ])
                                )
                            ],
                            style={"display": "flex", "alignItems": "auto", "gap": "8px"}
                        ),

                        dcc.Dropdown(
                            id="dropdown-scelta-grafico",
                            options=[
                                {"label": "Andamento", "value": "andamento"},
                                {"label": "Media durante il giorno", "value": "medie"},
                                {"label": "Eventi glucosio basso", "value": "basso"}
                            ],
                            placeholder="Scegli una tipologia di grafico",
                            style={"width": "100%"}
                        ),
                        # Contenitore del grafico
                        html.Div(
                            id="patient-graph",
                            style={"height": "100%", "width": "100%"}
                        ),
                        html.Br(),
                        html.Div([
                            html.Div(id="contenitore-filtro-temporale", children=filtro_temporale(""), style={"display": "none"}),
                            html.Div(id="contenitore-filtro-calendario", children=filtro_calendario(), style={"display": "none"}),
                        ]),
                    ],
                    className="f-1 card"
                ),

                dcc.Store(id="aggiorna-info-paziente", data=False)
            ]
        )
    ]
)


#********************************************************************************************************************
# LISTA PAZIENTI
# Metodo che crea la lista dei pazienti come lista di Buttons
def layout_lista_pazienti_associati():

    pazienti = current_user.visualizza_n_c_pazienti_associati()
    
    if not pazienti:
        return dbc.Alert("Nessun paziente registrato.", color="warning")

    return html.Div(
        children=[
            # Colonna sinistra: elenco pazienti
            render_lista_pazienti_glicemia(pazienti),
        ],
        className= 'f-1 flex-row'
    )

# Restituisce la lista di pulsanti dei pazienti:
def render_lista_pazienti_glicemia(pazienti):

    # Modifica il colore dei bollini in base al valore della media di glicemia.
    def colore_glicemia(media):
        # Se la media è nulla:
        if media == 0 or media is None:
            return "#D0D3DD"
        # Se la media è nella norma: verde
        elif 80 <= media <= 130:
            return '#08ff46'
        # Se la media è alta: giallo
        elif 131 <= media <= 180:
            return '#FFD93B'
        # Se la media è troppo alta o troppo bassa: rosso
        elif media > 180 or media < 80:
            return '#FF4C4C'
        

    return html.Div(
        className= 'f-1 flex-col scrollable',
        children=[
            *[
                # Pulsante per ogni paziente:
                dbc.Button(
                    # Contenitore per bollino colorato + Nome del paziente
                    html.Div([
                        # Bollino colorato:
                        html.Span(
                            style={
                                # Permette a un elemento di disporsi sulla stessa riga
                                "display": "inline-block",
                                "width": "20px",
                                "height": "20px",
                                # Lo rende tondo
                                "borderRadius": "50%",
                                "backgroundColor": colore_glicemia(d["media"]),
                                "margin-right": "10px"
                            }
                        ),

                        # Nome del paziente:
                        f"{d['nome']} {d['cognome']}"

                        ],
                        # Stile della div bollino + nome
                        style={
                            "alignItems": "center",
                            # Allinea il testo a sinistra
                            "textAlign": "left",
                        },
                        className='d-flex font-25 gray'
                    ),
                    # id del pulsante
                    id={"type": "btn-paziente", "index": d["id"]},
                    # Colore del pulsante    
                    color="light",
                    # Stile del pulsante
                    style={"marginBottom": "20px",},
                    className='button'
                )
                # Per ogni paziente
                for d in pazienti
            ]
        ]
    )
#********************************************************************************************************************
#fil-funzione che permette di creare una lista ordinata dalle info dei paziente 

def crea_div_paziente(cfanno, info, segnalazioni):
    codice_fiscale, eta, nome = cfanno[0]
     # Visualizzazione segnalazioni
    segnalazioni_div = []
    # Se ci sono segnalazioni:
    if segnalazioni:
        # Aggiungi un titolo
        segnalazioni_div.append(html.H5("Segnalazioni:"))
        for tipo, descrizione, data_inizio, data_fine in segnalazioni:
            periodo = f"Dal {data_inizio.strftime('%d/%m/%Y')}"
            if data_fine:
                periodo += f" al {data_fine.strftime('%d/%m/%Y')}"
            segnalazioni_div.append(
                html.Div([
                    html.Span(tipo.capitalize() + ": "), html.Span(descrizione),
                    html.Br(), html.Small(periodo),
                ])
            )
    else:
        segnalazioni_div = [html.H6("Nessuna segnalazione presente.")]

    # Div per quando non ci sono informazioni:
    no_info = html.Div([
            # Header:
            html.Div([
                html.Div([
                    html.H4(f"{nome}, {eta}"),
                    #Codice fiscale tutto maiuscolo
                    html.H6(codice_fiscale.upper(), className='gray')
                ], className='f-1'),
                html.Div([
                    # Pulsante per le annotazioni
                    dbc.Button("Annota", id="modal-insert-btn", n_clicks=0, style={'padding': '10px 25px'}, className='rounded-25 font-20') 
                ], style={'align-items': 'center', 'justify-content': 'flex-end'}, className='f-1 d-flex')
            ], style={'margin-bottom': '5px'}, className= 'f-1 flex-row'),

            html.H5("Non ci sono informazioni.", style={'color': 'gray'}),
            html.Div([
                    *segnalazioni_div,
                ],
                style={
                    'flex': 1, 
                    'flexDirection': 'column', 
                    'background-color': '#f8f9fa', 
                    'border-radius': '15px', 
                    'overflowY': 'auto',
                    'padding': '5px',
                }
            ),
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Paziente")),
                    dbc.ModalBody(html.Div([
                        # Informazioni generali
                        html.H4(f"{nome}, {eta}"),
                        html.H6(codice_fiscale.upper(), style={'margin-bottom': '10px'}, className='gray'),

                        # informazioni cliniche:
                        html.Div([
                            html.H5("Informazioni cliniche:"),
                            
                            # Patologie pregresse:
                            html.Div([
                                html.H6("Patologie pregresse:"),
                                dbc.Textarea(
                                    id="insert-patologie", 
                                    value="", 
                                    style={
                                        "width": "100%", 
                                        "height": "80px",
                                        },
                                    className='n-border rounded-15'    
                                    )
                            ]),

                            # Fattori di rischio: 
                            html.Div([
                                html.H6("Fattori di rischio:"),
                                dbc.Input(id="insert-rischio", type="text", value="", className='n-border rounded-15'),
                            ]),

                            # Comorbidità:
                            html.Div([
                                html.H6("Comorbidità:"),
                                dbc.Input(id="insert-comorb", type="text", value="", className='n-border rounded-15')
                            ]),
                        ],
                        style={
                            'margin-bottom': '10px',
                            'padding': '5px'
                        }, className= 'f-1 flex-col rounded-15 l-gray g-20'),

                        # Alert per gli inserimenti:
                        dbc.Alert(id="inserisci-info-output", is_open=False),
                        
                    ])),
                    # Footer del modal:
                    dbc.ModalFooter([
                        dbc.Button("Annulla", id="close-insert-infopaz", style={'background-color':'red'}, className='n-border rounded-25 font-20'),
                        dbc.Button("Salva", id="inserisci-modifiche-btn", n_clicks=0, style={'background-color':'green'}, className='n-border rounded-25 font-20'),
                    ], style={'justify-content': 'flex-end'}, className='d-flex g-10'),
                ],
                id="popup-inserisci-info",
                centered=True,
                is_open=False
            )
        ],
        style={
            'maxHeight': '250px',
        },
        className= 'f-1 flex-col'
    )

    # Se non ci sono info:
    if not info:
        return no_info
    
    # Preparo set per info cliniche
    patologie_pregresse = set()
    fattori_rischio = set()
    comorbidita = set()

    for riga in info:
        patologie_pregresse.add(riga[0]) if riga[0] else None
        fattori_rischio.add(riga[1]) if riga[1] else None
        comorbidita.add(riga[2]) if riga[2] else None

    patologie = f"Patologie pregresse: {', '.join(sorted(patologie_pregresse))}" if patologie_pregresse else ""
    fattori = f"Fattori di rischio: {', '.join(sorted(fattori_rischio))}" if fattori_rischio else ""
    comorb = f"Comorbidità: {', '.join(sorted(comorbidita))}" if comorbidita else ""

   
    # DIV con informazioni del paziente:
    con_info = html.Div([
            # Header:
            html.Div([
                html.Div([
                    html.H4(f"{nome}, {eta}"),
                    #Codice fiscale tutto maiuscolo
                    html.H6(codice_fiscale.upper(), className='gray')
                ], className='f-1'),
                html.Div([
                    # Pulsante per le annotazioni
                    dbc.Button("Annota", id="modal-modifiche-btn", n_clicks=0, style={'padding': '10px 25px'}, className='rounded-25 font-20') 
                ], style={'align-items': 'center', 'justify-content': 'flex-end'}, className='f-1 d-flex')
            ], style={'margin-bottom': '5px'}, className= 'f-1 flex-row'),

            # Informazioni cliniche:
            html.Div([
                    html.H5("Informazioni cliniche:"),
                    html.P(patologie),
                    html.P(fattori),
                    html.P(comorb)
                ],
                style={ 
                    'margin-bottom': '10px',
                    'padding': '5px'
                },
                className= 'f-1 flex-col rounded-15 scrollable l-gray'
            ),

            # Segnalazioni del paziente
            html.Div([
                    *segnalazioni_div,
                ],
                style={'padding': '5px'},
                className= 'f-1 flex-col rounded-15 scrollable l-gray'
            ),

            # POP-UP per modifiche delle informazioni del paziente
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Paziente")),
                    dbc.ModalBody(html.Div([
                        # Informazioni generali
                        html.H4(f"{nome}, {eta}"),
                        html.H6(codice_fiscale.upper(), style={'margin-bottom': '10px'}, className='gray'),

                        # informazioni cliniche:
                        html.Div([
                            html.H5("Informazioni cliniche:"),
                            
                            # Patologie pregresse:
                            html.Div([
                                html.H6("Patologie pregresse:"),
                                dbc.Textarea(
                                    id="input-patologie", 
                                    value=", ".join(sorted(patologie_pregresse)), 
                                    style={
                                        "width": "100%", 
                                        "height": "80px"
                                        },
                                    className='n-border rounded-15'
                                    )
                            ]),

                            # Fattori di rischio: 
                            html.Div([
                                html.H6("Fattori di rischio:"),
                                dbc.Input(id="input-rischio", type="text", value=", ".join(sorted(fattori_rischio)), className='n-border rounded-15'),
                            ]),

                            # Comorbidità:
                            html.Div([
                                html.H6("Comorbidità:"),
                                dbc.Input(id="input-comorb", type="text", value=", ".join(sorted(comorbidita)), className='n-border rounded-15')
                            ]),
                        ],
                        style={
                            'margin-bottom': '10px',
                            'padding': '5px'
                        }, className= 'f-1 flex-col rounded-15 l-gray g-20'),

                        # Alert per gli inserimenti:
                        dbc.Alert(id="modifica-info-output", is_open=False), 

                        # se è stata salvata con successo la modifica ai dati paziente, fa aspettare 1.5 sec, dopodichè chiude da
                        # solo il modal. 
                        dcc.Interval(id="interval-salva-info-paziente", interval=1500, n_intervals=0, max_intervals=1, disabled=True),
                        
                    ])),
                    # Footer del modal:
                    dbc.ModalFooter([
                        dbc.Button("Annulla", id="close-modifica-infopaz", style={'background-color':'red'}, className='n-border rounded-25 font-20'),
                        dbc.Button("Salva", id="salva-modifiche-btn", n_clicks=0, style={'background-color':'green'}, className='n-border rounded-25 font-20'),
                    ], style={'justify-content': 'flex-end'}, className='d-flex g-10'),
                ],
                id="popup-modifica-info",
                centered=True,
                is_open=False
            )
        ],
        style={
            'maxHeight': '250px',
        },
        className= 'f-1 flex-col'
    )

    return con_info

# ******************************************************************************************************************
# Funzione che crea dinamicamente il dropdown delle terapie correlate a un singolo paziente
def crea_div_terapia_dropdown(terapie):
    return html.Div([
        dcc.Dropdown(
            id="dropdown-terapia-selezionata",
            options=[
                {
                    # t[3] nome del farmaco, t[6/7] date dal Al
                    "label": f"{t[3].upper()} ({t[6]} - {t[7]})",
                    # id della terapia
                    "value": t[0]
                }
                for t in terapie
            ],
            placeholder="Scegli una terapia...",
            style={"flex": 1, "width": "100%"}
        ),
        html.Div(id="div-terapia-selezionata", style={'height': '210px', 'marginTop': '10px'})
    ])

# FUNZIONE CHE CREA LE INFO DI TERAPIA

def crea_div_terapia_selezionata(terapia,is_diabetologo):
    if is_diabetologo:
        return html.Div([

            html.Div([
                # Div di sinistra
                html.Div([
                    # nome farmaco, dosaggio
                    html.H4(f"{terapia[3].upper()}, {terapia[4]}mg"),
                    # assunzioni giornaliere
                    html.P(f"{terapia[5]} volte al giorno."),
                    # Indicazioni
                    html.P(f"{terapia[9]}"),
                    # Periodo
                    html.P(f"Dal: {terapia[6]}"),
                    html.P(f"Al: {terapia[7]}")
                ],
                style={'padding': '5px'},
                className= 'f-2 flex-col rounded-15 scrollable l-gray'
                ),

                # Div di destra
                html.Div([
                    # Pulsante modifica terapia
                    dbc.Button(
                        "Modifica", 
                        id="apri-modal-terapia",
                        n_clicks=0, 
                        style={'padding': '10px 25px'}, 
                        className='n-border rounded-25 font-20'
                    ),
                ], style={
                    'justifyContent': 'flex-end', 
                    'alignItems': 'flex-start'
                    },
                    className='f-1 d-flex'
                )

            ], style={'height': '160px'},  className='flex-row mb-2'),

            # Pulsante di aggiunta terapia:
            dbc.Button(
                "Nuova Terapia",
                id='aggiungi-terapia-btn',
                n_clicks=0,
                style={
                    'width': '100%',
                    'padding': '10px 25px'               
                }, 
                className='n-border rounded-25 font-20'
            ),

            # POP-UP per modificare una terapia esistente
            dbc.Modal(
                [
                    # Header:
                    dbc.ModalHeader(dbc.ModalTitle("Modifica Terapia")),

                    # Body:
                    dbc.ModalBody([
                        # Terapia attuale:
                        html.Div([
                            # Div nome farmaco e dosaggio:
                            html.H4(f"{terapia[3].upper()}, {terapia[4]}mg"),
                            # Dose giornaliera + Idicazioni
                            html.P(f"{terapia[5]} volte al giorno {'' if terapia[9] is None else terapia[9]}"),
                            # Ultima modifica
                            html.Small(f"Ultima modifica: {terapia[8].strftime('%d/%m/%Y')} - {terapia[8].strftime('%H:%M')}", style={'text-align': 'center'})
                        ],
                        style={
                            'marginBottom':'15px',
                        }, className= 'f-1 flex-col rounded-15 l-gray p-10'),

                        # Div di modifica della terapia:
                        html.Div([
                            html.H5("Modifica la terapia:"),
                            # Div Farmaco e dosaggio: 
                            html.Div([
                                # Colonna farmaco: 
                                html.Div([
                                    # Nome del farmaco
                                    html.P("Farmaco:", className='mb-0'),
                                    dbc.Input(id="input-farmaco", type="text", value=terapia[3], className='n-border'),
                                ], className='f-3 flex-col'),
                                # Colonna dosaggio:
                                html.Div([
                                    # Dosaggio in mg
                                    html.P("Dosaggio (mg):", className='mb-0'),
                                    dbc.Input(id="input-dosaggio", type="number", value=terapia[4], className='n-border')
                                ], className='f-1 flex-col'),
                            ], className='f-1 flex-row mb-3 g-20'),

                            # Assunzioni giornaliere + Indicazioni:
                            html.Div([
                                # Colonna farmaco: 
                                html.Div([
                                    # Assunzioni giornaliere
                                    html.P("A. giornaliere:", className='mb-0'),
                                    dbc.Input(id="input-assunzioni", type="number", value=terapia[5], className='n-border'),
                                ], className='f-1 flex-col'),
                                # Colonna dosaggio:
                                html.Div([
                                    # Indicazioni
                                    html.P("Indicazioni:", className='mb-0'),
                                    dbc.Input(id="input-indicazioni", value=terapia[9], className='n-border')
                                ], className='f-3 flex-col'),
                            ], className='f-1 flex-row mb-3 g-20'),

                            # Div delle date:
                            html.Div([
                                # Dal:
                                html.Div([
                                    html.P("Dal:", className='mb-0'),
                                    dbc.Input(id="input-data-inizio", type="date", value=str(terapia[6]), className='n-border'),
                                ], className='f-1 flex-col'),
                                # Al:
                                html.Div([
                                    html.P("Al:", className='mb-0'),
                                    dbc.Input(id="input-data-fine", type="date", value=str(terapia[7]), className='n-border'),
                                ], className='f-1 flex-col')
                            ], className='f-1 flex-row mb-3 g-20'),

                            # Box per gli alert:
                            dbc.Alert(id="modifica-terapia-output", is_open=False, duration=2000),

                            # Modal di eliminazione terapia:
                            dbc.Modal([
                                dbc.ModalHeader("Attenzione!", className='gray font-20'),
                                dbc.ModalBody("Eliminare la terapia è un'operazione irreversibile. Continuare?", className='font-20'),
                                dbc.ModalFooter([
                                    dbc.Button("No", id="declina-elimina-terapia", color="success", style={'padding': '5px 15px'}, className='rounded-25'),
                                    dbc.Button("Sì", id="conferma-elimina-terapia", n_clicks=0,color="danger", style={'padding': '5px 15px'}, className='rounded-25')
                                ])
                            ],
                                id="popup-elimina-terapia",
                                centered=True,
                                is_open=False
                            )
                            
                        ],
                        style={'padding': '5px'},
                        className='f-3 flex-col rounded-15 l-gray'),
                        
                    ]),
                    dbc.ModalFooter([
                        # Pulsante per salvare le modifiche
                        dbc.Button("Salva", id="btn-salva-modifiche-terapia",n_clicks=0, color='success', className='n-border rounded-25'),
                        # Pulsante per annullare e uscire
                        dbc.Button("Annulla", id="chiudi-modal-terapia", color='warning', className='n-border rounded-25'),
                        # Pulsante per eliminare 
                        dbc.Button("Elimina", id='btn-elimina-terapia', n_clicks=0, color='danger', className='n-border rounded-25'),
                    ], className='flex-row g-10'
                    )
                ],
                id="popup-modifica-terapia",
                centered=True,
                is_open=False
            )
        ], className='f-1')
    else:
        return html.Div([

            html.Div([
                # Div di sinistra
                html.Div([
                    # nome farmaco, dosaggio
                    html.H4(f"{terapia[3].upper()}, {terapia[4]}mg"),
                    # assunzioni giornaliere
                    html.P(f"{terapia[5]} volte al giorno."),
                    # Indicazioni
                    html.P(f"{terapia[9]}"),
                    # Periodo
                    html.P(f"Dal: {terapia[6]}"),
                    html.P(f"Al: {terapia[7]}")
                ],
                style={'padding': '5px'},
                className='f-2 flex-col rounded-15 scrollable l-gray'
                ),
            ]),
        ])

            

# ******************************************************************************************************************
# Metodo che crea una card di informazioni di base del paziente: da visualizzare nella dashboard del dottore (card 4)
def crea_div_info_base(info,flagpaziente):
    if not info:
            return html.Div("Nessuna informazione disponibile per questo paziente.")
    if flagpaziente:

        username, nome, cognome, data_nascita, sesso, media_glicemia = info

        glicata=0 if media_glicemia==0 else round((float(media_glicemia)*0.0348)+1.63, 2)
        return html.Div([
            # Nome + Username
            # 'padding': '5px 20px', 'textAlign': 'center' 
            html.Div(
                [
                    html.H3(f"{nome} {cognome}", style={"display": "inline-block", "margin-right": "20px", 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'padding': '5px 10px', 'textAlign': 'center'}),
                    html.H5(f"{username}", style={"display": "inline-block"}, className='gray'),
                ],
                className="text-inline"
            ),
            # Data di nascita + sesso
            html.Div([
                html.Div([
                    html.P(f"Data di nascita:  {data_nascita.strftime('%d/%m/%Y')}", className='font-20'),
                    html.P(f"Sesso:  {'Femmina' if sesso == 'F' else 'Maschio'}", className='font-20')
                    ],
                    className='f-1 flex-col p-10'
                ),

                html.Div([
                    html.P("Glicata:", className='font-20'),
                    html.Div([
                        html.P(glicata, style={'display': 'inline-block','font-size': '45px', 'font-weight': 'bold'}),
                        html.P(" mg/dL", style={'display': 'inline-block'}, className='gray')
                    ]),
                ], className='f-1 flex-col p-10'
                )

                ], className='d-flex g-20'
            )
            ]
        )
    else:
        username, nome, cognome, data_nascita, sesso, pazienti_associati = info[0]

        return html.Div([
            # Nome + Username
            # 'padding': '5px 20px', 'textAlign': 'center' 
            html.Div(
                [
                    html.H3(f"{nome} {cognome}", style={"display": "inline-block", "margin-right": "20px", 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'padding': '5px 10px', 'textAlign': 'center'}),
                    html.H5(f"{username}", style={"display": "inline-block"}, className='gray'),
                ],
                className="text-inline"
            ),
            # Data di nascita + sesso
            html.Div([
                html.Div([
                    html.P(f"Data di nascita:  {data_nascita.strftime('%d/%m/%Y')}", className='font-20'),
                    html.P(f"Sesso:  {'Femmina' if sesso == 'F' else 'Maschio'}", className='font-20')
                    ],
                    className='f-1 flex-col p-10'
                ),

                html.Div([
                    html.P("Pazienti associati:", className='font-20'),
                    html.Div([
                        html.P(pazienti_associati, style={'display': 'inline-block','font-size': '45px', 'font-weight': 'bold'}),
                    ]),
                ], className='f-1 flex-col p-10'
                )

                ], className='d-flex g-20'
            )
            ], 
        )       
        

# CHAT (= chat_content) -> Già fatta


# ******************************************************************************************************************
# LAYOUT DELL'ADMIN:
# 1. Dashboard
# 2. Richieste
# 3. Pazienti
# 4. Diabetologi
# ******************************************************************************************************************

# DASHBOARD ADMIN
admin_dashboard = html.Div(
    className='f-1 flex-row g-40 p-40',
    children=[
        
        # Colonna con grafico generale di tutti i pazienti a sinistra, statistiche sui pazienti a destra (?)  
        # Colonna a sinistra 1 (divisa in due righe)
        html.Div(
            className='f-2 flex-col g-30',
            style={
                "borderRadius": "15px",
            },
            children=[
                
                # colonna a sx
                html.Div(
                    className= 'f-1 d-flex',
                    children=[
                        # 5: Card del grafico
                        html.Div(
                            className='card',
                            children=[
                                html.H4("Glicemia media dei pazienti gestiti da ciascun diabetologo:", className='gray'),
                                html.Hr(style= {"margin-top": "18px"}),
                                
                                html.Div(

                                    # grafico principale dell'admin, parte extra chiesta dal prof.
                                    dcc.Graph(
                                        id= "grafico-glicemia-tutti",
                                        figure= model.visualizza_media_glicemia_per_diabetologi(),
                                        style={"height": "66vh"},
                                        config={
                                            "displayModeBar": False           # mostra la barra (puoi anche usare False per nasconderla)
                                        }
                                    ),

                                    # stile del Div dov'è contenuto il grafico
                                    style={"overflowX": "auto",     # racchiuso tutto in un div, in modo che se i diabetologi sono tanti, vengano visualizzati tramite scrollbar orizzontale
                                           "height": "100%",
                                           'justify-content': 'center',
                                           'align-items':'center',
                                           'margin-top': '40px',
                                    }        
                                ),
                                
                            ]
                        )
                    ]
                )
            ]
        ),
    ]
)



# RICHIESTE DI INSERIMENTO NELLA PIATTAFORMA 
# funzione che organizza in due colonne SEPARATE le richieste: una per pazienti e una diabetologi
def render_richieste_account():
    style_div_interno = {
        "flex": "1",
        "minHeight": "1",          
        "overflow": "hidden",
        "padding": "20px",
        "backgroundColor": "#ffffff",
        "border": "1px solid #dee2e6",
        "borderRadius": "15px",
        "display": "flex",
        "flexDirection": "column",
        "gap": "5px",
        "boxSizing": "border-box",
        "maxHeight": "calc(100vh - 80px)"           # importante per l'altezza
    }

    style_scrollable_inner = {
        "flex": "1",
        "overflowY": "scroll",
        "height": "100%",
        "boxSizing": "border-box",
        "paddingRight": "10px"
    }

    return html.Div(
        style={
            "minHeight": "1"      
        },
        className='f-1 flex-row g-40',
        children=[

            # colonna pazienti
            html.Div(
                style=style_div_interno,
                children=[
                    html.H4("Richieste Pazienti", className='gray'),
                    html.Hr(style={"margin-top": "5px"}),

                    html.Div(     # wrapper scrollabile aggiunto
                        style=style_scrollable_inner,
                        children=[
                            dcc.Dropdown(
                                id="dropdown-richieste-pazienti",           
                                placeholder="Seleziona una richiesta per visualizzarne i dettagli..."
                            ),

                            html.Div(id="alert-richiesta-paziente", style={"marginTop": "10px"}),
                            
                            html.Div(id="dettagli-richiesta-paziente", style={"marginTop": "10px"}, className='f-1'),
                        ],
                    )
                ]
            ),

            # colonna diabetologi
            html.Div(
                style=style_div_interno,
                children=[
                    html.H4("Richieste Diabetologi", className='gray'),
                    html.Hr(style={"margin-top": "5px"}),

                    html.Div(    # wrapper scrollabile aggiunto
                        style=style_scrollable_inner,
                        children=[
                            dcc.Dropdown(
                                id="dropdown-richieste-diabetologi",
                                placeholder="Seleziona una richiesta per visualizzarne i dettagli..."
                            ),

                            html.Div(id="alert-richiesta-diabetologo", style={"marginTop": "10px"}),

                            html.Div(id="dettagli-richiesta-diabetologo", style={"marginTop": "10px"}, className='f-1')
                        ]
                    )
                ]
            )
        ]
    )



# layout principale della pagina della richiesta di inserimento nella piattaforma
def admin_request(): 
    return html.Div(
    style={ 
        "height": "100vh",
        "boxSizing": "border-box",
        "margin": "0",
    },
    className='f-1 flex-col scrollable g-20 p-40',
    children=[
        render_richieste_account()
    ]
)



# FUNZIONE CHE GENERA LA CARD DI RICHIESTA PER PAZIENTE/DIABETOLOGO
def render_dati_richiesta(dati):
    if not dati:
        return dbc.Alert("Nessuna richiesta trovata.", color="warning")
    
    # Formattare la data 
    giorno = dati['data_richiesta'].strftime("%d/%m/%Y %H:%M")
    # data di nascita formattata
    data_nascita = dati['data_nascita'].strftime("%d/%m/%Y")

    data_card = html.Div([
            
            # Header Nome Cognome + tipo Account
            html.Div([
                # Colonna di sinistra
                html.Div([
                    html.H2(f"{dati['nome']} {dati['cognome']}, ({dati['sesso']})", style={'display': 'inline-block', 'padding': '5px'}, className='rounded-15 l-gray'),
                    html.H4(f"{dati['codice_fiscale'].upper()}", className='gray'),
                    html.H5(f"Data di nascita: {data_nascita}", className='gray')
                ], className='f-1'),
                # colonna di destra
                html.Div([
                    html.H2("PAZIENTE" if dati['paziente'] else "DIABETOLOGO", style={'padding': '5px'}),
                    html.H5("IN ATTESA" if dati['stato_richiesta'] else f"{dati['stato_richiesta']}", style={'color': 'green'})
                ], style={"textAlign": "center"}, className='f-1')
            ], style={'margin-bottom': '15px'}, className='f-1 flex-row'),
        
            # Dati vari anagrafici:
            html.Div([
                
                # Colonna dell'indirizzo
                html.Div([
                    html.H4("Indirizzo:", className='gray'),
                    html.H5(f"{dati['indirizzo']}")
                ], style={"textAlign": "center"}, className='f-1'),
                
                # Colonna Città
                html.Div([
                    html.H4("Città:", className='gray'),
                    html.H5(f"{dati['citta']}")
                ], style={"textAlign": "center"}, className='f-1'),
                
                # Colonna CAP
                html.Div([
                    html.H4("CAP:", className='gray'),
                    html.H5(f"{dati['cap']}")
                ], style={"textAlign": "center"}, className='f-1')
            ], 
            className='f-1 flex-row rounded-15 l-gray p-10'),

            # Dati sui contatti:
            html.Div([

                # Colonna telefono
                html.Div([
                    html.H4("Telefono:", className='gray'),
                    html.H5(f"{dati['telefono']}")
                ], style={"textAlign": "center"}, className='f-1'),

                # Colonna mail
                html.Div([
                    html.H4("Email:", className='gray'),
                    html.H5(f"{dati['email']}")
                ], style={"textAlign": "center"}, className='f-1')
            ],
            className='f-1 flex-row rounded-15 l-gray p-10'),
        
            # Data richiesta:
            html.H6(f"Data richiesta: {giorno}", style={"textAlign": "center"}, className='gray'),

            html.Hr(),

            #Pulsanti per accettare o rifiutare:
            html.Div([
                # Pulsante accetta 
                html.Div(
                    dbc.Button("Accetta", id={"type": "btn-accetta-richiesta", "codice_fiscale": dati["codice_fiscale"]}, n_clicks=0, color="success", style={'width': '100%', 'padding': '15px 20px'}, className='rounded-25 font-25'),
                    className='f-1'
                ),
                # Pulsante rifiuta
                html.Div(
                    dbc.Button("Rifiuta", id={"type": "btn-rifiuta-richiesta", "codice_fiscale": dati["codice_fiscale"]}, n_clicks=0, color="danger", style={'width': '100%', 'padding': '15px 20px'}, className='rounded-25 font-25'),
                    className='f-1'
                ),
                
            ], className='f-1 flex-row g-20'),

            html.Div(
                id={"type": "alert-richiesta", "codice_fiscale": dati["codice_fiscale"]},
                children=[],  # inizialmente vuoto
                style={'marginTop': '20px'}
            ),
        ],
        className='flex-col card g-20'
    )

    return data_card

#******************************************************************************************************************************

# Funzione che restituisce la lista dei pazienti per la pagina di ADMIN
def layout_lista_pazienti():
    pazienti = model.get_all_pazienti()

    if not pazienti:
        return dbc.Alert("Nessun paziente registrato.", color="warning")

    lista_pulsanti = [
        dbc.Button(
            f"{d['nome']} {d['cognome']}",
            id={"type": "btn-paziente", "index": d["id_paziente"]},
            color="light",
            style={
                "textAlign": "left",
                "marginBottom": "20px",
            },
            className="button font-25 gray"
        )
        for d in pazienti
    ]

    # Ritorna un contenitore con tutti i pulsanti
    return html.Div(lista_pulsanti, style={"overflowY": "auto", 'maxHeight': '74.5vh'})  

#*****************************************************************************************************

# Funzione che crea la card con i dati del paziente selezionato nella lista pazienti
# Pagina PAZIENTI di ADMIN

def crea_card_paziente(dati_paziente, dati_diab):

    # Data di nascita formattata in %d/%m/%Y
    formatted_date = dati_paziente['data_nascita'].strftime("%d/%m/%Y")

    # Gestione del diabetologo (se non presente)
    diab_info = {
        'nome': "Nessun diabetologo associato",
        'cognome': "",
        'id_diabetologo': ""
    }
    
    if dati_diab:  # Se esiste un diabetologo associato
        diab_info = {
            'nome': dati_diab.get('nome', ''),
            'cognome': dati_diab.get('cognome', ''),
            'id_diabetologo': dati_diab.get('id_diabetologo', '')
        }


    card_paziente = html.Div([

        # Header con info principali
        html.Div([
            # Colonna dati generali
            html.Div([
                html.H2(f"{dati_paziente['nome']} {dati_paziente['cognome']}, ({dati_paziente['sesso']})", style={'display': 'inline-block', 'padding': '5px'}, className='rounded-15 l-gray'),
                html.H4(f"{dati_paziente['codice_fiscale'].upper()} (ID: {dati_paziente['id_paziente']})", className='gray'),
                html.H5(f"Data di nascita: {formatted_date}", className='gray')
            ], className='f-1'),
            # Diabetologo associato
            html.Div([
                html.H4("Diabetologo associato:", className='gray'),
                # html.H4(f"{dati_diab['nome']} {dati_diab['cognome']} (ID: {dati_diab['id_diabetologo']})")
                html.H4(
                    f"{dati_diab['nome']} {dati_diab['cognome']} (ID: {dati_diab['id_diabetologo']})" 
                    if dati_diab 
                    else "Nessun diabetologo associato"
                )
            ], className='f-1 flex-col centered')
        ], className='flex-row'),

        # Body con info varie
        # Username
        html.Div([
            html.H4("Username: ", className='gray'),
            html.H4(f"{dati_paziente['username']}")
        ], className='rounded-15 l-gray g-10 centered p-15'),

        # Dati di residenza
            html.Div([
                
                # Colonna dell'indirizzo
                html.Div([
                    html.H4("Indirizzo:", className='gray'),
                    html.H5(f"{dati_paziente['indirizzo']}")
                ], style={"textAlign": "center"}, className='f-1'),
                
                # Colonna Città
                html.Div([
                    html.H4("Città:", className='gray'),
                    html.H5(f"{dati_paziente['citta']}")
                ], style={"textAlign": "center"}, className='f-1'),
                
                # Colonna CAP
                html.Div([
                    html.H4("CAP:", className='gray'),
                    html.H5(f"{dati_paziente['cap']}")
                ], style={"textAlign": "center"}, className='f-1')
            ], 
            className='f-1 flex-row rounded-15 l-gray p-10'),
        
        # Dati di contatto
            html.Div([

                # Colonna telefono
                html.Div([
                    html.H4("Telefono:", className='gray'),
                    html.H5(f"{dati_paziente['telefono']}")
                ], style={"textAlign": "center"}, className='f-1'),

                # Colonna mail
                html.Div([
                    html.H4("Email:", className='gray'),
                    html.H5(f"{dati_paziente['email']}")
                ], style={"textAlign": "center"}, className='f-1')
            ],
            className='f-1 flex-row rounded-15 l-gray p-10'),

            # salva l'id del paziente, in modo da usarlo per la callback col grafico
            dcc.Store(      
                id= "store-id-paziente",
                data= dati_paziente.get('id_paziente')
            ),

            # POP-UP DEL GRAFICO DEL PAZIENTE
            dbc.Modal(
                [ 
                    dbc.ModalHeader("Glicemia del paziente:", className='font-20 gray'),
                    dbc.ModalBody([
                        html.Div(
                            id="contenitore-popup-graf-paziente",
                            children=[],                                    # inizialmente vuoto, quando si clicca il pulsante viene messo il grafico
                            style={"width": "100%", "height": "90%"}        # dimensioni ottimizzate, ho controllato su due schermi diversi
                        ),
                        filtro_temporale("")
                        ], style={"padding": "2px", 'margin-bottom': '15px'}  
                    ),
                ],
                id="pop-admin-grafico-paziente",
                is_open=False,
                size="xl",  
                centered=True          
            ),

            # POP-UP RIMOZIONE DEL PAZIENTE
            dbc.Modal(
                [
                    dbc.ModalHeader("Attenzione!", className='font-20 gray'),
                    dbc.ModalBody(
                        html.Div([
                            dbc.Alert(
                                f"""L'eliminazione di un account è un operazione irreversibile. 
                                E' sicuro/a di voler eliminare il/la paziente {dati_paziente.get('nome')} {dati_paziente.get('cognome')}?""",

                                color="danger",  # rosso
                                className="text-center",  # centra il testo orizzontalmente
                                style={
                                    "padding": "10px",
                                    "fontWeight": "bold",
                                    "fontSize": "1rem",
                                    "borderRadius": "10px",
                                    "margin": "10px",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                }
                            ),
                            dbc.Row(
                                [
                                    # pulsanti per la conferma o annullamento della rimozione del paziente
                                    dbc.Col(
                                        dbc.Button(
                                            "Si",
                                            id="btn-delete-paz-confirm-YES",
                                            color="danger",
                                            size="md",
                                            className="w-100"
                                        ),
                                        width=3
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "No",
                                            id="btn-delete-paz-confirm-NO",
                                            color="success",
                                            size="md",
                                            className="w-100"
                                        ),
                                        width=3
                                    )
                                ],
                                justify="center",
                                className="d-flex justify-content-center mt-3"
                            )
                        ]),
                        style={"padding": "10px", "color": "red"}  
                    ),
                ],
                id="pop-admin-delete-patient",
                is_open=False,
                size="md",  
                centered=True          
            ),

            
            # POP-UP per modificare i dati del paziente
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Modifica Dati Paziente")),
                    dbc.ModalBody(
                        html.Div([
                            html.Div([
                                html.H5("Informazioni account", className="mb-3"),

                                # Indirizzo + Città + CAP
                                html.Div([
                                    html.Div([
                                        dbc.Label("Indirizzo"),
                                        dbc.Input(
                                            id="modifica-indirizzo",
                                            type="text",
                                            value=dati_paziente.get("indirizzo", ""),
                                            placeholder="Inserisci l'indirizzo",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-2'),
                                    html.Div([
                                        dbc.Label("Città"),
                                        dbc.Input(
                                            id="modifica-citta",
                                            type="text",
                                            value=dati_paziente.get("citta", ""),
                                            placeholder="Inserisci la città",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1'),
                                    html.Div([
                                        dbc.Label("CAP"),
                                        dbc.Input(
                                            id="modifica-cap",
                                            type="text",
                                            value=dati_paziente.get("cap", ""),
                                            placeholder="Inserisci il CAP",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1')
                                ], style={'margin-top': '10px'}, className='d-flex g-10'),

                                # Email + Telefono
                                html.Div([
                                    html.Div([
                                        dbc.Label("Email"),
                                        dbc.Input(
                                            id="modifica-email",
                                            type="email",
                                            value=dati_paziente.get("email", ""),
                                            placeholder="Inserisci l'email",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1'),
                                    html.Div([
                                        dbc.Label("Telefono"),
                                        dbc.Input(
                                            id="modifica-telefono",
                                            type="tel",
                                            value=dati_paziente.get("telefono", ""),
                                            placeholder="Inserisci il numero di telefono",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1')
                                ], style={'margin-top': '10px'}, className='d-flex g-10'),

                            ],
                            style={
                                'margin-bottom': '10px'
                            }, className='f-1 flex-col rounded-15 l-gray g-10 p-10'),

                            dbc.Alert("Modifiche effettuate con successo!", id="modifica-paziente-alert", is_open=False, dismissable=True)
                        ])
                    ),
                    dbc.ModalFooter([
                        dbc.Button("Annulla", id="btn-annulla-modifiche-paziente",
                            style={'background-color': 'red'}, className='n-border rounded-25 font-20'),
                        dbc.Button("Salva", id="btn-salva-modifiche-paziente", n_clicks=0,
                            style={'background-color': 'green'}, className='n-border rounded-25 font-20'),
                    ],
                    style={'justify-content': 'flex-end'}, className='d-flex g-10'),
                    dcc.Interval(id="interval-update-card-paz", interval=1500, n_intervals=0, max_intervals=1, disabled=True)
                ],
                id="popup-modifica-dati-paziente",
                centered=True,
                is_open=False,
                size="lg"
            ),


            # Footer con pulsanti
            html.Hr(),
            html.Div([
                # Mostra la glicemia del paziente:
                dbc.Button("Glicemia", id="btn-graf-paziente", color="success", className='f-1 rounded-25 font-20'),

                # Modifica il profilo:
                dbc.Button("Modifica", id="btn-modifica-dati-paz", color="warning", className='f-1 rounded-25 font-20'),

                # Elimina paziente
                dbc.Button("Elimina", id="btn-rimuovi-paz", color="danger", className='f-1 rounded-25 font-20')

            ], className='f-1 flex-row g-20')


    ], className='flex-col card g-20')

    return card_paziente


#************************************************************************************************************************************************************

# PAZIENTI ADMIN:
def admin_patient():
    return html.Div(
        className='f-1 flex-row g-20 p-20',
        style={"paddingLeft": "40px",},
        children=[
            # Lista dei pazienti
            html.Div([
                html.H4("Pazienti:", className='gray'),
                html.Hr(),
                # Genera la lista dei pazienti
                html.Div(layout_lista_pazienti(), id="lista-pazienti-admin", style={'height': '100%'})
            ],  style={ 'maxHeight': '100%', 
                        "borderRadius": "15px",
                        "marginRight": "25px",
                        "marginTop": "20px",
                        "marginBottom": "20px",
                }, 
                className='flex-col card'),
            # Info dei pazienti:
            html.Div([
                html.H4("Informazioni:", className='gray'),
                html.Hr(),
                dcc.Store(id="trigger-update-paziente", data=False),
                # Genera la card di informazioni
                html.Div(id="dettagli-paziente")
            ], className='f-2 flex-col card', style={
                "borderRadius": "15px",
                "marginTop": "20px",
                "marginRight": "20px",
                "marginBottom": "20px"
            })   
        ]
)


#************************************************************************************************************************************************************
# renderizza in modo corretto e uguale alla pagina dei pazienti, il layout.
# Funzione che restituisce la lista dei pazienti per la pagina di ADMIN
def layout_lista_diabetologi():
    diabetologi = model.get_all_diabetologi()

    if not diabetologi:
        return dbc.Alert("Nessun paziente registrato.", color="warning")

    lista_pulsanti = [
        dbc.Button(
            f"{d['nome']} {d['cognome']}",
            id={"type": "btn-diabetologo", "index": d["id_diabetologo"]},
            color="light",
            style={
                "textAlign": "left",
                "marginBottom": "20px",
            },
            className="button font-25 gray"
        )
        for d in diabetologi
    ]

    # Ritorna un contenitore con tutti i pulsanti
    return html.Div(lista_pulsanti, style={"overflowY": "auto", "maxHeight": "74.5vh"})


# funzione che crea la card dove vengono visualizzati i dettagli del diabetologo selezionato dalla lista
def crea_card_diabetologo(dati_diabetologo):
    """Crea e restituisce la Card dei dettagli del diabetologo."""

    # Data di nascita formattata in %d/%m/%Y
    formatted_date = dati_diabetologo['data_nascita'].strftime("%d/%m/%Y")

    card_diabetologo = html.Div([
        # Header
        # Header con info principali
        html.Div([
            # Colonna dati generali
            html.Div([
                html.H2(f"{dati_diabetologo['nome']} {dati_diabetologo['cognome']}, ({dati_diabetologo['sesso']})", style={'display': 'inline-block', 'padding': '5px'}, className='rounded-15 l-gray'),
                html.H4(f"{dati_diabetologo['codice_fiscale'].upper()} (ID: {dati_diabetologo['id_diabetologo']})", className='gray'),
                html.H3(f"Data di nascita: {formatted_date}", className='gray')
            ], className='f-1'),

            # Numero pazienti associati
            html.Div([
                html.H4("Pazienti associati:", className='gray'),
                html.H3(model.get_numero_pazienti_associati_by_id(dati_diabetologo['id_diabetologo']))
            ], className='f-1 flex-col centered')
        
        ], className='flex-row'),

        # BODY
        # Username
        html.Div([
            html.H4("Username: ", className='gray'),
            html.H4(f"{dati_diabetologo['username']}")
        ], className='rounded-15 l-gray g-10 centered p-15'),

        # Dati di residenza
            html.Div([
                
                # Colonna dell'indirizzo
                html.Div([
                    html.H4("Indirizzo:", className='gray'),
                    html.H5(f"{dati_diabetologo['indirizzo']}")
                ], style={"textAlign": "center"}, className='f-1'),
                
                # Colonna Città
                html.Div([
                    html.H4("Città:", className='gray'),
                    html.H5(f"{dati_diabetologo['citta']}")
                ], style={"textAlign": "center"}, className='f-1'),
                
                # Colonna CAP
                html.Div([
                    html.H4("CAP:", className='gray'),
                    html.H5(f"{dati_diabetologo['cap']}")
                ], style={"textAlign": "center"}, className='f-1')
            ], 
            className='f-1 flex-row rounded-15 l-gray p-10'),
        
        # Dati di contatto
            html.Div([

                # Colonna telefono
                html.Div([
                    html.H4("Telefono:", className='gray'),
                    html.H5(f"{dati_diabetologo['telefono']}")
                ], style={"textAlign": "center"}, className='f-1'),

                # Colonna mail
                html.Div([
                    html.H4("Email:", className='gray'),
                    html.H5(f"{dati_diabetologo['email']}")
                ], style={"textAlign": "center"}, className='f-1')
            ],
            className='f-1 flex-row rounded-15 l-gray p-10'),
        
            # salva l'id del diabetologo, in modo da usarlo per la callback col grafico
            dcc.Store(      
                id= "store-id-diabetologo",
                data= dati_diabetologo.get('id_diabetologo')
            ),

            # POP-UP LISTA PAZIENTI ASSOCIATI
            dbc.Modal(
                [
                    dbc.ModalHeader(f"Pazienti associati a {dati_diabetologo.get('nome')} {dati_diabetologo.get('cognome')}", className='font-20 gray'),
                    dbc.ModalBody(
                        html.Div(
                            id="contenitore-popup-lista-paz-diabetologo",
                            children=[],                                  
                        ),
                        style={"padding": "2px"}  
                    ),
                ],
                id="pop-admin-lista-pazienti-ass",
                is_open=False,
                size="md",  
                centered=True          
            ),

            # POP-UP DEL GRAFICO DEL DIABETOLOGO
                dbc.Modal(
                    [
                        dbc.ModalHeader("Glicemia media pazienti associati", className='font-20 gray'),
                        dbc.ModalBody(
                            html.Div(
                                id="contenitore-popup-graf-diabetologo",
                                children=[],                                    # inizialmente vuoto, quando si clicca il pulsante viene messo il grafico
                                style={"width": "100%", "height": "90%"}        # dimensioni ottimizzate, ho controllato su due schermi diversi
                            ),
                            style={"padding": "2px"}  
                        ),
                    ],
                    id="pop-admin-grafico-diabetologo",
                    is_open=False,
                    size="xl",  
                    centered=True          
                ),
            
            # POP-UP RIMOZIONE ACCOUNT
            dbc.Modal(
                [
                    dbc.ModalHeader("Attenzione!", className='font-20 gray'),
                    dbc.ModalBody(
                        html.Div([
                            dbc.Alert(
                                f"""L'eliminazione di un account è un operazione irreversibile. 
                                E' sicuro/a di voler eliminare il/la diabetologo/a {dati_diabetologo.get('nome')} {dati_diabetologo.get('cognome')}?""",

                                color="danger",  # rosso
                                className="text-center",  # centra il testo orizzontalmente
                                style={
                                    "padding": "10px",
                                    "fontWeight": "bold",
                                    "fontSize": "1rem",
                                    "borderRadius": "10px",
                                    "margin": "10px",
                                    "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
                                }),
                            dbc.Row(
                                [
                                    # pulsanti per la conferma o annullamento della rimozione del paziente
                                    dbc.Col(
                                        dbc.Button(
                                            "Si",
                                            id="btn-delete-diab-confirm-YES",
                                            color="danger",
                                            size="md",
                                            className="w-100"
                                        ),
                                        width=3
                                    ),
                                    dbc.Col(
                                        dbc.Button(
                                            "No",
                                            id="btn-delete-diab-confirm-NO",
                                            color="success",
                                            size="md",
                                            className="w-100"
                                        ),
                                        width=3
                                    )
                                ],
                                justify="center",
                                className="d-flex justify-content-center mt-3"
                            )
                        ]),
                        style={"padding": "10px", "color": ""}          # da modificare perchè si vuole mettere il colore del "danger" tipo
                    ),
                ],
                id="pop-admin-delete-diab",
                is_open=False,
                size="md",  
                centered=True          
            ),

            # popup per visualizzare la lista di pazienti associati a uno specifico diabetologo.
            dbc.Modal(
                [
                    dbc.ModalHeader(f"Pazienti associati a {dati_diabetologo.get('nome')} {dati_diabetologo.get('cognome')}"),
                    dbc.ModalBody(
                        html.Div(
                            id="contenitore-popup-lista-paz-diabetologo",
                            children=[],                                  
                        ),
                        style={"padding": "2px"}  
                    ),
                ],
                id="pop-admin-lista-pazienti-ass",
                is_open=False,
                size="md",  
                centered=True          
            ),
            
            # POP-UP per modificare i dati del diabetologo
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Modifica Dati Diabetologo")),
                    dbc.ModalBody(
                        html.Div([
                            html.Div([
                                html.H5("Informazioni account", className="mb-3"),

                                # Indirizzo + Città + CAP
                                html.Div([
                                    html.Div([
                                        dbc.Label("Indirizzo"),
                                        dbc.Input(
                                            id="modifica-indirizzo-diabetologo",
                                            type="text",
                                            value=dati_diabetologo.get("indirizzo", ""),
                                            placeholder="Inserisci l'indirizzo",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ],className='f-2'),
                                    html.Div([
                                        dbc.Label("Città"),
                                        dbc.Input(
                                            id="modifica-citta-diabetologo",
                                            type="text",
                                            value=dati_diabetologo.get("citta", ""),
                                            placeholder="Inserisci la città",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1'),
                                    html.Div([
                                        dbc.Label("CAP"),
                                        dbc.Input(
                                            id="modifica-cap-diabetologo",
                                            type="text",
                                            value=dati_diabetologo.get("cap", ""),
                                            placeholder="Inserisci il CAP",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1')
                                ], style={'margin-top': '10px'}, className='d-flex g-10'),

                                # Email + Telefono
                                html.Div([
                                    html.Div([
                                        dbc.Label("Email"),
                                        dbc.Input(
                                            id="modifica-email-diabetologo",
                                            type="email",
                                            value=dati_diabetologo.get("email", ""),
                                            placeholder="Inserisci l'email",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1'),
                                    html.Div([
                                        dbc.Label("Telefono"),
                                        dbc.Input(
                                            id="modifica-telefono-diabetologo",
                                            type="tel",
                                            value=dati_diabetologo.get("telefono", ""),
                                            placeholder="Inserisci il numero di telefono",
                                            style={"border": "none", "border-radius": "15px"}
                                        )
                                    ], className='f-1')
                                ], style={'margin-top': '10px'}, className='d-flex g-10'),
                                
                            ],
                            style={
                                'margin-bottom': '10px'
                            }, className='f-1 flex-col rounded-15 l-gray g-10 p-10'),

                            dbc.Alert("Modifiche effettuate con successo!", id="modifica-diabetologo-alert", is_open=False, dismissable=True)
                        ])
                    ),
                    dbc.ModalFooter([
                        dbc.Button("Annulla", id="btn-annulla-modifiche-diabetologo",
                                style={'background-color': 'red'}, className='n-border rounded-25 font-20'),
                        dbc.Button("Salva", id="btn-salva-modifiche-diabetologo", n_clicks=0,
                                style={'background-color': 'green'}, className='n-border rounded-25 font-20'),
                    ],
                    style={'justify-content': 'flex-end'}, className='d-flex g-10'),
                    dcc.Interval(id="interval-update-diabetologo", interval=1500, n_intervals=0, max_intervals=1, disabled=True)
                ],
                id="popup-modifica-dati-diabetologo",
                centered=True,
                is_open=False,
                size="lg"
            ),


        # FOOTER
        html.Hr(),
        html.Div([
            # Lista pazienti
            dbc.Button("Lista pazienti", id="btn-lista-paz-assoc-diab", color="primary", className='f-1 rounded-25 font-20'),
 
            
            # Mostra la glicemia del paziente:
            dbc.Button("Glicemia pazienti", id="btn-graf-paz-assoc-diab", color="success", className='f-1 rounded-25 font-20'),

            # Modifica il profilo:
            dbc.Button("Modifica", id="btn-modifica-dati-diab", color="warning", className='f-1 rounded-25 font-20'),

            # Elimina paziente
            dbc.Button("Elimina", id="btn-rimuovi-diab", color="danger", className='f-1 rounded-25 font-20')

        ], className='f-1 flex-row g-20')

    ], className='flex-col card g-20')

    return card_diabetologo


# funzione che crea la lista di pazienti associati a un diabetologo visualizzato dentro il modal del pulsante "lista pazienti associati" 
def genera_lista_pazienti_associati(lista_pazienti):
    
    if not lista_pazienti:
        return dbc.Alert(
            "Nessun paziente associato.",
            color="danger",  # rosso
            className="text-center p-20 ",
            style={
                "fontWeight": "bold",
                "fontSize": "1.1rem",
                "borderRadius": "10px",
                "margin": "20px",
                "boxShadow": "0 4px 8px rgba(0, 0, 0, 0.1)",
            })

    return dbc.ListGroup(
        [
            dbc.ListGroupItem(
                [
                    html.Span(f"{p['nome']} {p['cognome']}", style={"fontWeight": "bold"}),
                    html.Span(f" — username: {p['username']}", className="text-muted", style={"marginLeft": "8px"}),
                ]
            )
            for p in lista_pazienti
        ],
        flush=True,
        style={"margin": "0.5rem", "padding": "0px"}
    )

# LAYOUT DIABETOLOGI ADMIN:
def admin_doctor():
    return html.Div(
        className='f-1 flex-row g-20 p-20',
        style={
            "paddingLeft": "40px"
        },
        children=[
            # Lista dei pazienti
            html.Div([
                html.H4("Diabetologi:", className='gray'),
                html.Hr(),
                # Genera la lista dei diabetologi
                html.Div(layout_lista_diabetologi(), id="lista-diabetologi-admin", style={'height': '100%'})
                
            ], style={'maxHeight': '100%',
                    "borderRadius": "15px",
                    "marginRight": "25px",
                    "marginTop": "20px",
                    "marginBottom": "20px"}, 
               className='flex-col card'),
            # Info dei pazienti:
            html.Div([
                html.H4("Informazioni:", className='gray'),
                html.Hr(),
                dcc.Store(id="trigger-update-diabetologo", data=False),
                # Genera la card di informazioni
                html.Div(id="dettagli-diabetologo")
            ], className='f-2 flex-col card', 
            style={
                "borderRadius": "15px",
                "marginTop": "20px",
                "marginRight": "20px",
                "marginBottom": "20px"
            })   
        ]
)

#******************************************************************************************************
# FUNZIONE CHE GENERA LE BUBBLES DEI MESSAGGI

def layout_lista_messaggi(messaggi):
    """Genera card messaggi allineate a sx/dx in base al mittente.
    
    Args:
        messages: Lista di tuple (contenuto, orario,is_mittente). ci appendo i messaggi della query
    """
    if not messaggi: return html.H4("Inizia a scrivere!", className='gray')
    message_cards = []
    data_precedente = None  #variabile per capire quando si cambia giorno
    for contenuto, orario, giorno, is_mittente, is_paziente in messaggi:
        is_mittente = ( is_mittente == is_paziente ) #se l'user è il mittente ed è un paziente allora il mex va a destra.
        if giorno != data_precedente:
            #card che segna la data
            day_header = dbc.Card(
                children = giorno.strftime("%d-%m-%Y"),
                style={
                    'maxHeight': 'fit-content',
                    'width': 'fit-content',
                    'height': 'fit-content', 
                    'padding': '4px 8px',
                    'margin': '4px auto',
                    'fontSize': '1rem',
                    'margin': '5px auto',
                    'textAlign': 'center'
                },
                className='n-border rounded-25'
            )
            message_cards.append(day_header)
            data_precedente = giorno

        # Stile dinamico
        card_style = {
            'maxWidth': '65%',
            'width': 'fit-content',  # Adatta la larghezza al testo
            'Height': 'fit-content',
            'marginLeft': 'auto' if is_mittente else '0',
            'marginRight': '0' if is_mittente else 'auto',
            'marginTop': '10px',
            'marginBottom': '10px',
            'padding': '8px 12px',
            'backgroundColor': "#C6E9F9" if is_mittente else '#f8f9fa',
            'border': 'none',
            'borderRadius': '25px',
            'wordBreak': 'break-word',  #Forza a capo per parole lunghe
            'fontSize': '1.2em',
        }        
        card = dbc.Card(
            dbc.CardBody([
                contenuto,
                # Orario:
                html.Small(
                    orario.strftime("%H:%M"), 
                    className="text-muted mt-1 gray", 
                    style={
                        'position': 'absolute',
                        'right': '15px',
                        'bottom': '5px',
                        'fontSize': '0.8rem'
                    }
                )
            ]),
            style=card_style
        )
        message_cards.append(card)
    
    return html.Div(message_cards)

#************************************************************************************************************
# GENERA LA LISTA DI PULSANTI DEI CONTATTI
def layout_lista_contatti():
    contatti = model.get_contatti()

    if not contatti:
        return dbc.Alert("Nessun contatto registrato.", color="warning")

    lista_contatti = [
        dbc.Button(
            f"{c['nome']} {c['cognome']}",
            id = {
                "type": "btn-contatto",
                "index": c["id"],
            },
            color="light",
            style={
                "textAlign": "left",
                "marginBottom": "20px",
            },
            className="button gray",
        )
        for c in contatti
    ]
    
    return html.Div(lista_contatti, id="", style={"overflowY": "auto", "height": "70vh"})

# CHAT
#   ____________
#   |   |      |
#   | 1 |   2  |
#   |   |      |
#   |___|______|

chat_content = html.Div(
    style={
        "height": "100vh"
    },
    className='f-1 flex-row g-40 p-40',
    children=[
        # Pannello sinistro - Lista chat
        html.Div(
            className="f-1 flex-col card scrollable",  
            style={
                "minWidth": "300px",  # Larghezza minima
            },
            children=[
                html.H2("Chat", className='gray'),
                html.Hr(),
                html.Div(
                    id="lista-contatti",
                    style={"height": "100%","width": "100%", "flex-direction": "column"}, 
                )
            ]
        ),

        # Box della chat
        #   ________
        #   |      |
        #   |   2  |
        #   |      |
        #   |______|

        html.Div(
            style={
                "border": "1px solid #dee2e6",
                "overflow": "hidden",
            },
            className='f-2 flex-col rounded-15',
            children=[
                # Nome del contatto e dati del contatto
                html.Div(
                    style={
                        # Occupa il 100% dello spazio disponibile in larghezza
                        "width": "100%",
                        # Occupa solo il 10% dello spazio disponibile in altezza
                        "height": "10%",
                        # sfondo bianco
                        "background-color": "#ffffff",
                        "borderBottom": "1px solid #dee2e6",
                    },
                    className='flex-row',
                    children=[

                        # Colonna Nome del contatto
                        html.Div(
                            id="nome-contatto",
                            style={
                                "float": "left",  # Allinea a sinistra
                                "margin-left": "0",
                                "align-self": "flex-start",  # Per flexbox
                                "padding": "2rem 2rem"
                            },
                            className='f-1'
                        ),

                        # Colonna Pulsante per gli avvisi
                        html.Div([
                            # Bottone per aprire gli avvisi
                            dbc.Button(
                                "Avvisi", 
                                id="open-alert-btn",
                                className = "btn-avvisi"
                            ),
                            
                            # Modal con body vuoto inizialmente:
                            # Qui vengono visualizzati gli alert
                            dbc.Modal(
                                [
                                    dbc.ModalHeader(
                                                    html.H4("Avvisi", className='font-20 gray'), 
                                                ),
                                    dbc.ModalBody(id="alert-body-content",
                                                style={
                                                    "background-color":"#e6f2ff",
                                                    'height': '80vh',
                                                },
                                                className='scrollable'
                                                ),  
                                    dbc.ModalFooter(
                                        dbc.Button("Chiudi", id="close-alert-btn", className='n-border rounded-25 font-20')
                                    )
                                ],
                                id="alert-modal",
                                is_open=False,
                                centered=True,
                                size="lg"
                            ),

                            dcc.Store(id="id-contatto-store", storage_type="memory"), #memorizza l'id del contatto                     
                            dcc.Store(id="alert-data-store")
                        ], 
                        style={
                            'justify-content':'flex-end',
                            'align-items': 'center',
                            'height': '100%',
                            'align-items':'center',
                        }, className='f-1 d-flex')
                    ]
                ),

                # Contenitore dei messaggi:
                html.Div(
                    id="chat-box",
                    style={
                        # Occupa il 100% dello spazio disponibile in larghezza
                        "width": "100%",
                        # Occupa solo l'80% dello spazio disponibile in altezza
                        "height": "80%",
                        # mostra la barra dello scroll verticale (y axis) : "auto" = solo se il contenuto
                        # eccede l'altezza del contenitore
                        'scrollbarWidth': 'thin',  
                        'scrollbarColor': '#cccccc transparent',
                        # sfondo della chat , , 
                        'background': 'linear-gradient(to bottom right, #e6f2ff, #dfffe0)'
                    }, 
                    className='f-1 flex-col scrollable p-20'
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=10000,
                    n_intervals = 0
                ),
                # Contenitore dell'Input:
                html.Div(
                    style={
                        # Occupa il 100% dello spazio disponibile in larghezza
                        "width": "100%",
                        # Occupa solo il 10% dello spazio disponibile in altezza
                        "height": "10%",
                        # sfondo bianco
                        "background-color": "#ffffff",
                        "borderTop": "1px solid #dee2e6"
                    },
                    className='centered p-20',
                    children=[
                        # Input text per il messaggio
                        dbc.Input(
                            placeholder="Invia un messaggio...",
                            type="text",
                            id="input-text",
                            className='input',
                            debounce=True,
                            n_submit=0
                        )
                    ]
                )
            ]
        )
    ]
)

#DIV PER VISUALIZZARE LE ALERTS:
def layout_lista_alerts(alerts):
    if not alerts: 
        return html.P("Il paziente sta seguendo correttamente la terapia.")
    
    alert_cards = []
    for contenuto, orario in alerts:
        card = dbc.Card(
            dbc.CardBody([
                html.H1(contenuto,
                        className = "text-muted mt-1 gray",
                        style={
                        'right': '15px',
                        'bottom': '5px',
                        'fontSize': '1.7rem'
                    }),
                html.H2(
                    orario,
                    className="text-muted mt-1 gray", 
                    style={
                        'right': '15px',
                        'bottom': '5px',
                        'fontSize': '1.2rem'
                    }
                )
            ]),
            style={  
                'marginBottom': '20px',
                'position': 'central',
            }
        )
        alert_cards.append(card)
    
    return html.Div(alert_cards, className='flex-col')



