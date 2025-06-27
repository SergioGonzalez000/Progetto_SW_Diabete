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
            # Contenuto della pagina:
            # Per testare c'è la patient dashboard
            # patient_dashboard,
            html.Div(id="page-content", style={"display" : "flex", "width" : "100vw", "height" : "auto"})
        ],
        style={
            "display": "flex",
            # Page content e navbar occupano l'intera altezza della pagina
            "minHeight": "100vh",
            # Colore sfondo standard fisso
            "background-color": "#e6f2ff",
            #fil-altezza della parte azzurra che si adatta automaticamente
            #"height": "auto",
            # Nessun margine al contenuto affinché occupi tutta la pagina disponibile
            "margin": 0
        }
    )

# ******************************************************************************************************************

# Links di navigazione per gli ospiti
guest_navlinks = dbc.Nav(
    [
        # Link per la pagina iniziale
        dbc.NavLink("Home", href="/", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link della pagina della chat
        dbc.NavLink("Login", href="/login", active="exact", style={"fontSize": "25px"}, className="mb-4"), 
        # Link per la pagina dei pazienti
        dbc.NavLink("Registration", href="/registration", active="exact", style={"fontSize": "25px"}, className="mb-1.5"),
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
        dbc.NavLink("Dashboard", href="/patient-dashboard", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link per la pagina di grafici
        dbc.NavLink("Grafici", href="/grafici", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link della pagina della chat
        dbc.NavLink("Chat", href="/chat", active="exact", style={"fontSize": "25px"}, className="mb-1.5"),
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
        dbc.NavLink("Dashboard", href="/doctor-dashboard", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link per la pagina dei pazienti
        dbc.NavLink("Pazienti", href="/doctor-patient", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link della pagina della chat
        dbc.NavLink("Chat", href="/chat", active="exact", style={"fontSize": "25px"}, className="mb-1.5"),
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
        dbc.NavLink("Dashboard", href="/admin-dashboard", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link della pagina della chat
        dbc.NavLink("Richieste", href="/request", active="exact", style={"fontSize": "25px"}, className="mb-4"), 
        # Link per la pagina dei pazienti
        dbc.NavLink("Pazienti", href="/admin-patient", active="exact", style={"fontSize": "25px"}, className="mb-4"),
        # Link per la pagina dei diabetologi
        dbc.NavLink("Diabetologi", href="/admin-doctor", active="exact", style={"fontSize": "25px"}, className="mb-1.5"),
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
        html.H1("MyAPP", className="text-primary"),
        html.Hr(),

        # Per testare è fissa quella del paziente, da modificare con la callback in base al tipo di utente
        # patient_navlinks,
        html.Div(id="navlinks"),
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
        "box-shadow": "0 4px 8px rgba(0, 0, 255, 0.2)",
        "border": 'none',
        # Arrotonda gli angoli
        "border-radius": "15px",
        # Questo elemento diventa un contenitore "flessibile"
        "display": "flex",
        # definisce la direzione degli elementi in un contenitore di tipo flex : "column" = dall'alto verso il basso
        "flex-direction": "column"
    }
)

# ******************************************************************************************************************
# LAYOUT PER GLI OSPITI
# 1. Home
# 2. Login
# 3. Registration
# ******************************************************************************************************************

# HOME GUEST
home = html.Div(
    style={
        # L'elemento attuale si adatta automaticamente a tutto lo spazio disponibile
        "flex": 1,
        # Spazio dai margini esterni
        "padding": "40px",
        # divide lo spazio
        "display": "flex",
        # definisce la direzione degli elementi in un contenitore di tipo flex : "row" = da sinistra a destra
        "flex-direction": "row",
        # Spazio tra le colonne
        "gap": "40px" 
    },
    children=[
        html.H2("Da fare")
    ]
)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * 

# LOGIN NUOVO:

login_title = html.H1(
    "Login",
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
                dbc.Label("Enter username"),
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
    dbc.Button("Accedi", id="login-input", size="lg", n_clicks=0, className='button'),
    style={'marginTop': '30px'}
)

# Sign Up link: Link per la pagina di registrazione qualora non si avesse ancora un account
signUp_link = html.Div([
    html.Span("Don't have an account? "),
    html.A(
        "Register",
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
    style={'flex' : 1, 'justify-content': 'center', 'align-items': 'center', 'display': 'flex'}
)


# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

# REGISTRATION - NUOVO

# Titolo
registration_title = html.H1(
    "Registration",
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
                html.Span("Already have an account? "),
                html.A(
                    "Login",
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
                html.Span("Already have an account? "),
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
        # Username generato
        dbc.Card(
            [
                html.H5("Username:", style={'color': 'gray'}),
                dbc.CardBody(
                    [
                        html.P(id="generated-username")
                    ]
                )
            ], className='mb-4'
        ),
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
            dbc.Button("Registrati", id="registration-input", size="lg", n_clicks=0, className='button mb-4')
        ),

        # Link per il Login
        html.Div(
            [
                html.Span("Already have an account? "),
                html.A(
                    "Login",
                    href="/login",
                    className="text-primary"
                )
            ],
        )
    ],
    id="form3",
    style={"display": "none"}
)

# Pulsanti per la navigazione 
nav_buttons = html.Div(
    [
        dbc.Button("🡨", id="prev-button", n_clicks=0, disabled=True, style={"visibility": "hidden"}),  # inizialmente questo pulsante sarà nascosto (nel form 1)
        dbc.Button("🡪", id="next-button", n_clicks=0)
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
    style={'flex' : 1, 'display': 'flex', 'justify-content': 'center', 'align-items': 'center'}
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
    
    style={
        # L'elemento attuale si adatta automaticamente a tutto lo spazio disponibile
        "flex": 1,
        # Spazio dai margini esterni
        "padding": "30px",
        # divide lo spazio
        "display": "flex",
        # definisce la direzione degli elementi in un contenitore di tipo flex : "row" = da sinistra a destra
        "flex-direction": "row",
        # Spazio tra le colonne
        "gap": "40px" 
    },

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
            style={
                # Occupa 2/3 della page content
                "flex": 2, 
                "display": "flex",
                # definisce la direzione degli elementi in un contenitore di tipo flex : "column" = dall'alto verso il basso
                "flexDirection": "column",
                # Gli elementi qua dentro sono separati da 30px
                "gap" : "30px"
            },
            children=[
                # _________
                # | 3 | 4 |
                # |___|___|
                #
                # Prima riga della colonna centrale:
                html.Div(
                    style={
                        "flex": 1,
                        "display": "flex",
                        "gap": "30px"
                    },
                    children=[
                        # 3 : Card paziente
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Paziente: ", style={"color" : "grey"}),
                                html.Hr(),
                                html.Div(id="info-paz",),
                            ]
                        ),

                        # 4 :Card Terapia
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Terapia: ", style={"color" : "grey"}),
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
                    style={
                        "flex": 1,
                        "display": "flex"
                    },
                    children=[
                        # 5: Card del grafico
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Grafico:", style={"color" : "grey"}),
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
            children=[
                html.H5("Glicemia:", style={"color": "grey"}),
                html.Hr(),

                # Cerchio della glicemia
                html.Div(
                    className="circle-slot",
                    children=[
                        html.Div(
                            className="outer",
                            style={"background-color" : "#08ff46"},
                            id="cerchio-colorato",
                            children=[
                                html.Div(
                                    className="inner",
                                    children=[
                                        html.Div("0", id="number"),
                                        html.H6("mg/dl", style={"color": "grey"})
                                    ]
                                )
                            ]
                        ),
                    ]
                ),

                # Input glicemia
                html.H6("Nuova misurazione:", style={"color": "grey"}),
                dcc.Input(
                    placeholder="Inserisci glicemia...",
                    type="number",
                    value=0,
                    id="input-glicemia",
                    debounce=True,
                    n_submit=0,
                    className="input mb-3"
                ),

                # Input Farmaco:
                html.H6("Farmaco usato:", style={"color": "grey"}),
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
                                placeholder="Dosaggio...",
                                type="text",
                                className= 'input'  
                            ),
                            width=5
                        )
                    ],
                    className="mb-3"
                ),

                html.H6("Sintomi riscontrati:", style={"color": "grey"}),
                # Input Annotazione sintomi
                # Input glicemia
                dcc.Input(
                    id="input-sintomi-riscontrati",
                    placeholder="Sintomi...",
                    type="text",
                    className="input mb-3"
                ),

                dbc.Button("Inserisci glicemia",id="inserisci-glicemia",n_clicks=0),
                dbc.Alert(id="inserisci-glicemia-output",is_open=False),
                html.H6("Misurata:", style={"color": "grey"}),
                html.P("Qua da inserire eventuale radioitem per la selezione del pre e del post pranzo")
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


patient_graphs = html.Div(
    style={
        "flex": 1,
        "padding": "40px",
        "display": "flex",
        "flex-direction": "row",
        "gap": "40px"
    },
    children=[
        # Prima colonna
        html.Div(
            style={
                'flex': 1,
                'display': 'flex',
                'flexDirection': 'column',
                "gap": "40px"
            },
            children=[
                # Riquadro 1
                html.Div(
                    className='card',
                    style={'flex': 1, 'height': '100%', 'width': '100%'},
                    children=[
                        html.Div(
                            [
                                html.H5("Andamento: ", style={"color": "grey", "margin": "0", "marginRight": "8px"}),
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
                        html.Div(id='first-graph'),
                        html.Br(),
                        filtro_temporale(1),
                    ],                    

                ),

                # Riquadro 2
                html.Div(
                    className='card',
                    style={'flex': 1, 'height': '100%', 'width': '100%'},
                    children=[
                        html.Div(
                            [
                                html.H5("Media:", style={"color": "grey", "margin": "0", "marginRight": "8px"}),
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
                        html.Div(id='second-graph'),
                        html.Br(),
                        filtro_temporale(2),
                    ]
                ),
            ]
        ),

        # Seconda colonna
        html.Div(
            style={
                'flex': 1,
                'display': 'flex',
                'flexDirection': 'column',
                "gap": "40px"
            },
            children=[
                # Riquadro 3
                html.Div(
                    className='card',
                    style={'flex': 1, 'height': '100%', 'width': '100%'},
                    children=[
                        html.Div(
                            [
                                html.H5("Eventi glucosio basso: ", style={"color": "grey", "margin": "0", "marginRight": "8px"}),
                                info_popover(
                                    button_id="popover-button-4",
                                    popover_id="popover-4",
                                    contenuto=html.Div([
                                        "Mappa che mostra la probabilità giornaliera di avere un la glicemia bassa.",
                                    ])
                                )
                            ],
                            style={"display": "flex", "alignItems": "auto", "gap": "8px"}
                        ),
                        html.Div(id='third-graph'),
                        html.Br(),
                        filtro_temporale(3),
                    ]
                ),

                # Riquadro 4
                html.Div(
                    className='card',
                    style={'flex': 1, 'height': '100%', 'width': '100%'},
                    id='fourth-graph'
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
    style={
        # la doctor_dashboard si adatta automaticamente allo spazio disponibile
        'flex' : 1,
        'display': 'flex',
        # definisce la direzione degli elementi in un contenitore di tipo flex : "row" = da sinistra a destra
        'flex-direction': 'row',
        # Spazio dai margini esterni
        'padding': '40px',
        # Spazio interno tra le colonne
        'gap': '40px'
    },

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
                html.H5("I tuoi pazienti:", style={"color" : "grey"}),
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
                        html.H5("Informazioni paziente:", style={"color" : "grey"}),
                        html.Hr(),
                        html.Div( id="doctor-patient-info", style={"height": "100%","width": "100%"})
                    ],
                    style={"flex": 1},
                    className="card",
                ),

                html.Div(
                    [
                        # Numero 5
                        html.Div(
                            [
                                html.H5("Le tue info:", style={"color" : "grey"}),
                                html.Hr(),
                                # Qua va inserito il numero dei pazienti (associati)
                                html.Div(id="doctor-info")
                            ],
                            className="card"
                        ),
                        # Numero 6
                        html.Div(
                            [
                                html.H5("Andamento pazienti:", style={"color" : "grey"}),
                                html.Hr(),
                                # Qua va inserito un grafico
                                html.Div( id="patient-pie", style={"height": "100%","width": "100%"})
                            ],
                            className="card"
                        )
                    ],
                    style={
                        "flex": 1,
                        "display": "flex",
                        "flex-direction" : "row",
                        # spazio tra 5 e 6 di 40 px
                        "gap": "40px"
                    }
                )
            ],
            style= {
                "flex": 2,
                "display": "flex",
                "flex-direction" : "column",
                # spazio tra 4 e 5/6 di 40 px
                'gap': '40px'
            }
        )
    ]
)

# PAZIENTI DIABETOLOGO
doctor_patient = html.Div(
    style={
        'flex': 1,
        'display': 'flex',
        'flex-direction': 'row',
        'padding': '40px',
        'gap': '40px'
    },
    children=[
        # Prima colonna (1/3)
        html.Div(
            [
                html.H5("I tuoi pazienti:", style={"color": "grey"}),
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
            style={
                "flex": 2,
                "display": "flex",
                "flex-direction": "column",
                "gap": "40px"
            },
            children=[
                # Riga superiore (Paziente + Terapia)
                html.Div(
                    style={
                        "flex": 1,
                        "display": "flex",
                        "flex-direction": "row",
                        "gap": "40px"
                    },
                    children=[
                        # Box Paziente
                        html.Div(
                            [
                                html.H5("Paziente:", style={"color": "grey"}),
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
                                html.H5("Terapia:", style={"color": "grey"}),
                                html.Hr(),
                                # Qua va inserita la tabella delle terapie
                                html.Div( id="patient-therapy", style={'flex': 1, "height": "100%","width": "100%"}),

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
                                                    dbc.Input(id="input-nuovo-farmaco", type="text", style={'border': 'none'}),
                                                ], style={'flex': 3, 'display': 'flex', 'flexDirection': 'column'}),
                                                # Colonna dosaggio:
                                                html.Div([
                                                    # Dosaggio in mg
                                                    html.P("Dosaggio (mg):", className='mb-0'),
                                                    dbc.Input(id="input-nuovo-dosaggio", type="number", style={'border': 'none'})
                                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'}),
                                            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, className='mb-3'),

                                            # Assunzioni giornaliere + Indicazioni:
                                            html.Div([
                                                # Colonna farmaco: 
                                                html.Div([
                                                    # Assunzioni giornaliere
                                                    html.P("A. giornaliere:", className='mb-0'),
                                                    dbc.Input(id="input-nuovo-assunzioni", type="number", style={'border': 'none'}),
                                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'}),
                                                # Colonna dosaggio:
                                                html.Div([
                                                    # Indicazioni
                                                    html.P("Indicazioni:", className='mb-0'),
                                                    dbc.Input(id="input-nuovo-indicazioni", type='text', style={'border': 'none'})
                                                ], style={'flex': 3, 'display': 'flex', 'flexDirection': 'column'}),
                                            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, className='mb-3'),

                                            # Div delle date:
                                            html.Div([
                                                # Dal:
                                                html.Div([
                                                    html.P("Dal:", className='mb-0'),
                                                    dbc.Input(id="input-nuovo-data-inizio", type='date', min=control.get_today(), value=control.get_today() , style={'border': 'none', 'border-radius': '15px'}),
                                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'}),
                                                # Al:
                                                html.Div([
                                                    html.P("Al:", className='mb-0'),
                                                    dbc.Input(id="input-nuovo-data-fine", type='date', min=control.get_today(), value=control.get_today(), style={'border': 'none', 'border-radius': '15px'}),
                                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'})
                                            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, className='mb-3'),

                                            # Box per gli alert:
                                            dbc.Alert(id="aggiungi-terapia-output", is_open=False)
                                        ],
                                        style={
                                            'flex': 3,
                                            'display': 'flex',
                                            'flexDirection': 'column',
                                            'background-color': '#f8f9fa',
                                            'border-radius': '15px',
                                            'padding': '5px',
                                        }),
                                        
                                    ]),
                                    dbc.ModalFooter([
                                        # Pulsante per salvare le modifiche
                                        dbc.Button("Salva", id="salva-nuova-terapia-btn", n_clicks=0, color='success', style={'border': 'none', 'border-radius': '25px'}),
                                        # Pulsante per annullare e uscire
                                        dbc.Button("Annulla", id="chiudi-nuova-terapia", color='warning', style={'border': 'none', 'border-radius': '25px'}),
                                    ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '10px'}
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

                # Riga inferiore (Grafico)
                html.Div(
                    [
                        html.Div(
                            [
                                html.H5("Grafico:", style={"color": "grey", "margin": "0", "marginRight": "8px"}),
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
                                {"label": "Media durante il giorno", "value": "medie"}
                            ],
                            placeholder="Scegli una tipologia di grafico",
                            style={"width": "100%"}
                        ),
                        html.Hr(),
                        html.Div(
                            id="patient-graph",
                            style={"height": "100%", "width": "100%"}
                        ),
                        html.Br(),
                        filtro_temporale("")
                    ],
                    style={"flex": 1},
                    className="card"
                )
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
        style={
            "flex": 1,
            "display": "flex",
            "flexDirection": "row"
        },
        children=[
            # Colonna sinistra: elenco pazienti
            render_lista_pazienti_glicemia(pazienti),
        ]
    )

# Restituisce la lista di pulsanti dei pazienti:
def render_lista_pazienti_glicemia(pazienti):

    # Modifica il colore dei bollini in base al valore della media di glicemia.
    def colore_glicemia(media):
        # Se la media è nella norma: verde
        if 70 <= media <= 130:
            return '#08ff46'
        # Se la media è alta: giallo
        elif 131 <= media <= 180:
            return '#FFD93B'
        # Se la media è troppo alta o troppo bassa: rosso
        elif media > 180 or media < 70:
            return '#FF4C4C'
        # Se la media è nulla:
        elif media is None:
            return "gray"

    return html.Div(
        style={
            # Si adatta automaticamente allo spazio disponibile:
            "flex": 1,
            "display": "flex",
            # Impila gli elementi in children:
            "flexDirection": "column",
            # Mostra la barra di scorrimento se il contenuto supera l'altezza del contenitore:
            "overflowY": "auto",
            # "maxHeight": "87.5vh",

        },
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
                            "display": "flex", 
                            "alignItems": "center",
                            # Allinea il testo a sinistra
                            "textAlign": "left",
                            # Dimensione del nome:
                            "font-size": "25px",
                            # Colore del testo
                            "color": "gray"
                        }
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
    # Div per quando non ci sono informazioni:
    no_info = html.Div([
            # Header:
            html.Div([
                html.Div([
                    html.H4(f"{nome}, {eta}"),
                    #Codice fiscale tutto maiuscolo
                    html.H6(codice_fiscale.upper(), style={'color': 'gray'})
                ], style={'flex': 1}),
                html.Div([
                    # Pulsante per le annotazioni
                    dbc.Button("Annota", id="modal-insert-btn", n_clicks=0, style={'border-radius': '25px', 'padding': '10px 25px', 'font-size': '20px'}) 
                ], style={'flex': 1, 'display': 'flex', 'align-items': 'center', 'justify-content': 'flex-end'})
            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'margin-bottom': '5px'}),

            html.H5("Non ci sono informazioni.", style={'color': 'gray'}),

            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Paziente")),
                    dbc.ModalBody(html.Div([
                        # Informazioni generali
                        html.H4(f"{nome}, {eta}"),
                        html.H6(codice_fiscale.upper(), style={'color': 'gray', 'margin-bottom': '10px'}),

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
                                        'border': 'none',
                                        'border.radius': '15px',
                                        })
                            ]),

                            # Fattori di rischio: 
                            html.Div([
                                html.H6("Fattori di rischio:"),
                                dbc.Input(id="insert-rischio", type="text", value="", style={'border': 'none','border.radius': '15px'}),
                            ]),

                            # Comorbidità:
                            html.Div([
                                html.H6("Comorbidità:"),
                                dbc.Input(id="insert-comorb", type="text", value="", style={'border': 'none','border.radius': '15px'})
                            ]),
                        ],
                        style={
                            'flex': 1, 
                            'flexDirection': 'column',
                            'display': 'flex',
                            'gap': '20px', 
                            'background-color': '#f8f9fa', 
                            'border-radius': '15px', 
                            'padding': '5px',
                            'margin-bottom': '10px'
                        }),

                        # Alert per gli inserimenti:
                        dbc.Alert(id="inserisci-info-output", is_open=False),
                        
                    ])),
                    # Footer del modal:
                    dbc.ModalFooter([ # 'border': 'none'
                        dbc.Button("Annulla", id="close-insert-infopaz", style={'background-color':'red', 'border-radius': '25px', 'font-size': '20px', 'border': 'none'}),
                        dbc.Button("Salva", id="inserisci-modifiche-btn", n_clicks=0, style={'background-color':'green', 'border-radius': '25px', 'font-size': '20px', 'border': 'none'}),
                    ], style={'display': 'flex', 'justify-content': 'flex-end', 'gap': '10px'}),
                ],
                id="popup-inserisci-info",
                centered=True,
                is_open=False
            )
        ],
        style={
            'flex': 1,
            'display': 'flex',
            'flexDirection': 'column',
            'maxHeight': '250px',
        }
    )

    # Se non ci sono info:
    if not info:
        return no_info

    # Preparo set per info cliniche
    patologie_pregresse = set()
    fattori_rischio = set()
    comorbidita = set()

    for riga in info:
        if riga[0]: patologie_pregresse.add(riga[0])
        if riga[1]: fattori_rischio.add(riga[1])
        if riga[2]: comorbidita.add(riga[2])

    patologie = f"Patologie pregresse: {', '.join(sorted(patologie_pregresse))}" if patologie_pregresse else ""
    fattori = f"Fattori di rischio: {', '.join(sorted(fattori_rischio))}" if fattori_rischio else ""
    comorb = f"Comorbidità: {', '.join(sorted(comorbidita))}" if comorbidita else ""

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

    # DIV con informazioni del paziente:
    con_info = html.Div([
            # Header:
            html.Div([
                html.Div([
                    html.H4(f"{nome}, {eta}"),
                    #Codice fiscale tutto maiuscolo
                    html.H6(codice_fiscale.upper(), style={'color': 'gray'})
                ], style={'flex': 1}),
                html.Div([
                    # Pulsante per le annotazioni
                    dbc.Button("Annota", id="modal-modifiche-btn", n_clicks=0, style={'border-radius': '25px', 'padding': '10px 25px', 'font-size': '20px'}) 
                ], style={'flex': 1, 'display': 'flex', 'align-items': 'center', 'justify-content': 'flex-end'})
            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'margin-bottom': '5px'}),

            # Informazioni cliniche:
            html.Div([
                    html.H5("Informazioni cliniche:"),
                    html.P(patologie),
                    html.P(fattori),
                    html.P(comorb)
                ],
                style={
                    'flex': 1, 
                    'flexDirection': 'column', 
                    'background-color': '#f8f9fa', 
                    'border-radius': '15px', 
                    'overflowY': 'auto', 
                    'padding': '5px',
                    'margin-bottom': '10px'
                }
            ),

            # Segnalazioni del paziente
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

            # POP-UP per modifiche delle informazioni del paziente
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle("Paziente")),
                    dbc.ModalBody(html.Div([
                        # Informazioni generali
                        html.H4(f"Nome, {eta}"),
                        html.H6(codice_fiscale.upper(), style={'color': 'gray', 'margin-bottom': '10px'}),

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
                                        "height": "80px",
                                        'border': 'none',
                                        'border.radius': '15px',
                                        })
                            ]),

                            # Fattori di rischio: 
                            html.Div([
                                html.H6("Fattori di rischio:"),
                                dbc.Input(id="input-rischio", type="text", value=", ".join(sorted(fattori_rischio)), style={'border': 'none','border.radius': '15px'}),
                            ]),

                            # Comorbidità:
                            html.Div([
                                html.H6("Comorbidità:"),
                                dbc.Input(id="input-comorb", type="text", value=", ".join(sorted(comorbidita)), style={'border': 'none','border.radius': '15px'})
                            ]),
                        ],
                        style={
                            'flex': 1, 
                            'flexDirection': 'column',
                            'display': 'flex',
                            'gap': '20px', 
                            'background-color': '#f8f9fa', 
                            'border-radius': '15px', 
                            'padding': '5px',
                            'margin-bottom': '10px'
                        }),

                        # Alert per gli inserimenti:
                        dbc.Alert(id="modifica-info-output", is_open=False),
                        
                    ])),
                    # Footer del modal:
                    dbc.ModalFooter([ # 'border': 'none'
                        dbc.Button("Annulla", id="close-modifica-infopaz", style={'background-color':'red', 'border-radius': '25px', 'font-size': '20px', 'border': 'none'}),
                        dbc.Button("Salva", id="salva-modifiche-btn", n_clicks=0, style={'background-color':'green', 'border-radius': '25px', 'font-size': '20px', 'border': 'none'}),
                    ], style={'display': 'flex', 'justify-content': 'flex-end', 'gap': '10px'}),
                ],
                id="popup-modifica-info",
                centered=True,
                is_open=False
            )
        ],
        style={
            'flex': 1,
            'display': 'flex',
            'flexDirection': 'column',
            'maxHeight': '250px',
        }
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
                ], style={
                    'flex': 2,
                    'display': 'flex', 
                    'flexDirection': 'column', 
                    'border-radius': '15px',
                    'background-color': '#f8f9fa', 
                    'overflowY': 'auto',
                    'padding': '5px'
                    }
                ),

                # Div di destra
                html.Div([
                    # Pulsante modifica terapia
                    dbc.Button(
                        "Modifica", 
                        id="apri-modal-terapia",
                        n_clicks=0, 
                        style={
                            'border':'none',
                            'border-radius': '25px',
                            'padding': '10px 25px',
                            'font-size':'20px',
                        }
                    ),
                ], style={
                    'flex': 1,
                    'display': 'flex', 
                    'justifyContent': 'flex-end', 
                    'alignItems': 'flex-start'
                    }
                )

            ], style={'display': 'flex', 'flexDirection': 'row', 'height': '160px'},  className='mb-2'),

            # Pulsante di aggiunta terapia:
            dbc.Button(
                "Nuova Terapia",
                id='aggiungi-terapia-btn',
                n_clicks=0,
                style={
                    'width': '100%',
                    'border':'none',
                    'border-radius': '25px',
                    'padding': '10px 25px',
                    'font-size':'20px'                
                },
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
                            html.P(f"{terapia[5]} volte al giorno {terapia[9]}"),
                            # Ultima modifica
                            html.Small(f"Ultima modifica: {terapia[8]}", style={'text-align': 'center'})
                        ],
                        style={
                            'flex': 1,
                            'display': 'flex',
                            'flexDirection': 'column',
                            'background-color': '#f8f9fa',
                            'border-radius': '15px',
                            'padding': '5px',
                            'marginBottom':'15px'
                        }),

                        # Div di modifica della terapia:
                        html.Div([
                            html.H5("Modifica la terapia:"),
                            # Div Farmaco e dosaggio: 
                            html.Div([
                                # Colonna farmaco: 
                                html.Div([
                                    # Nome del farmaco
                                    html.P("Farmaco:", className='mb-0'),
                                    dbc.Input(id="input-farmaco", type="text", value=terapia[3], style={'border': 'none'}),
                                ], style={'flex': 3, 'display': 'flex', 'flexDirection': 'column'}),
                                # Colonna dosaggio:
                                html.Div([
                                    # Dosaggio in mg
                                    html.P("Dosaggio (mg):", className='mb-0'),
                                    dbc.Input(id="input-dosaggio", type="number", value=terapia[4], style={'border': 'none'})
                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'}),
                            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, className='mb-3'),

                            # Assunzioni giornaliere + Indicazioni:
                            html.Div([
                                # Colonna farmaco: 
                                html.Div([
                                    # Assunzioni giornaliere
                                    html.P("A. giornaliere:", className='mb-0'),
                                    dbc.Input(id="input-assunzioni", type="number", value=terapia[5], style={'border': 'none'}),
                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'}),
                                # Colonna dosaggio:
                                html.Div([
                                    # Indicazioni
                                    html.P("Indicazioni:", className='mb-0'),
                                    dbc.Input(id="input-indicazioni", value=terapia[9], style={'border': 'none'})
                                ], style={'flex': 3, 'display': 'flex', 'flexDirection': 'column'}),
                            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, className='mb-3'),

                            # Div delle date:
                            html.Div([
                                # Dal:
                                html.Div([
                                    html.P("Dal:", className='mb-0'),
                                    dbc.Input(id="input-data-inizio", type="date", value=str(terapia[6]), style={'border': 'none'}),
                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'}),
                                # Al:
                                html.Div([
                                    html.P("Al:", className='mb-0'),
                                    dbc.Input(id="input-data-fine", type="date", value=str(terapia[7]), style={'border': 'none'}),
                                ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'column'})
                            ], style={'flex': 1, 'display': 'flex', 'flexDirection': 'row', 'gap': '20px'}, className='mb-3'),

                            # Box per gli alert:
                            dbc.Alert(id="modifica-terapia-output", is_open=False),
                        ],
                        style={
                            'flex': 3,
                            'display': 'flex',
                            'flexDirection': 'column',
                            'background-color': '#f8f9fa',
                            'border-radius': '15px',
                            'padding': '5px',
                        }),
                        
                    ]),
                    dbc.ModalFooter([
                        # Pulsante per salvare le modifiche
                        dbc.Button("Salva", id="btn-salva-modifiche-terapia",n_clicks=0, color='success', style={'border': 'none', 'border-radius': '25px'}),
                        # Pulsante per annullare e uscire
                        dbc.Button("Annulla", id="chiudi-modal-terapia", color='warning', style={'border': 'none', 'border-radius': '25px'}),
                        # Pulsante per eliminare 
                        dbc.Button("Elimina", id='btn-elimina-terapia', n_clicks=0, color='danger', style={'border': 'none', 'border-radius': '25px'}),
                    ], style={'display': 'flex', 'flexDirection': 'row', 'gap': '10px'}
                    )
                ],
                id="popup-modifica-terapia",
                centered=True,
                is_open=False
            )
        ],
        style={'flex': 1})
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
                ], style={
                    'flex': 2,
                    'display': 'flex', 
                    'flexDirection': 'column', 
                    'border-radius': '15px',
                    'background-color': '#f8f9fa', 
                    'overflowY': 'auto',
                    'padding': '5px'
                    }
                ),
            ]),
        ])

            

# ******************************************************************************************************************
# Metodo che crea una card di informazioni di base del paziente: da visualizzare nella dashboard del dottore (card 4)
def crea_div_info_base(info,flagpaziente):
    if not info:
            return html.Div("Nessuna informazione disponibile per questo paziente.")
    if flagpaziente:

        username, nome, cognome, data_nascita, sesso, media_glicemia = info[0]

        return html.Div([
            # Nome + Username
            # 'padding': '5px 20px', 'textAlign': 'center' 
            html.Div(
                [
                    html.H3(f"{nome} {cognome}", style={"display": "inline-block", "margin-right": "20px", 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'padding': '5px 10px', 'textAlign': 'center'}),
                    html.H5(f"{username}", style={"display": "inline-block", "color": "gray"}),
                ],
                className="text-inline"
            ),
            # Data di nascita + sesso
            html.Div([
                html.Div([
                    html.P(f"Data di nascita:  {data_nascita.strftime('%d/%m/%Y')}", style={'font-size': '20px'}),
                    html.P(f"Sesso:  {'Femmina' if sesso == 'F' else 'Maschio'}", style={'font-size': '20px'})
                    ],
                    style={
                        'flex': 1,
                        'display': 'flex',
                        'flexDirection': 'column',
                        'padding': '10px'
                    }
                ),

                html.Div([
                    html.P("Glicata:", style={'font-size': '20px'}),
                    html.Div([
                        html.P(round((float(media_glicemia)*0.0348)+1.63, 2), style={'display': 'inline-block','font-size': '45px', 'font-weight': 'bold'}),
                        html.P(" mg/dL", style={'display': 'inline-block', 'color': 'gray'})
                    ]),
                ],
                    style={
                        'flex': 1,
                        'padding' : '10px',
                        'flexDirection': 'column'
                    }
                )

                ],
                style={
                    'display': 'flex',
                    'gap': '20px',
                }
            )
            ], 
        )
    else:
        username, nome, cognome, data_nascita, sesso, pazienti_associati = info[0]

        return html.Div([
            # Nome + Username
            # 'padding': '5px 20px', 'textAlign': 'center' 
            html.Div(
                [
                    html.H3(f"{nome} {cognome}", style={"display": "inline-block", "margin-right": "20px", 'backgroundColor': '#f8f9fa', 'borderRadius': '10px', 'padding': '5px 10px', 'textAlign': 'center'}),
                    html.H5(f"{username}", style={"display": "inline-block", "color": "gray"}),
                ],
                className="text-inline"
            ),
            # Data di nascita + sesso
            html.Div([
                html.Div([
                    html.P(f"Data di nascita:  {data_nascita.strftime('%d/%m/%Y')}", style={'font-size': '20px'}),
                    html.P(f"Sesso:  {'Femmina' if sesso == 'F' else 'Maschio'}", style={'font-size': '20px'})
                    ],
                    style={
                        'flex': 1,
                        'display': 'flex',
                        'flexDirection': 'column',
                        'padding': '10px'
                    }
                ),

                html.Div([
                    html.P("Pazienti associati:", style={'font-size': '20px'}),
                    html.Div([
                        html.P(pazienti_associati, style={'display': 'inline-block','font-size': '45px', 'font-weight': 'bold'}),
                    ]),
                ],
                    style={
                        'flex': 1,
                        'padding' : '10px',
                        'flexDirection': 'column'
                    }
                )

                ],
                style={
                    'display': 'flex',
                    'gap': '20px',
                }
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
    style={
        # la doctor_dashboard si adatta automaticamente allo spazio disponibile
        'flex' : 1,
        'display': 'flex',
        # definisce la direzione degli elementi in un contenitore di tipo flex : "row" = da sinistra a destra
        'flex-direction': 'row',
        # Spazio dai margini esterni
        'padding': '40px',
        # Spazio interno tra le colonne
        'gap': '40px'
    },
    children=[
        
        # Colonna con grafico generale di tutti i pazienti a sinistra, statistiche sui pazienti a destra (?)  
        # Colonna a sinistra 1 (divisa in due righe)
        html.Div(
            style={
                # Occupa 2/3 della page content
                "flex": 2, 
                "display": "flex",
                # definisce la direzione degli elementi in un contenitore di tipo flex : "column" = dall'alto verso il basso
                "flexDirection": "column",
                # Gli elementi qua dentro sono separati da 30px
                "gap" : "30px"
            },
            children=[
                
                # colonna a sx
                html.Div(
                    style={
                        "flex": 1,
                        "display": "flex"
                    },
                    children=[
                        # 5: Card del grafico
                        html.Div(
                            style={
                                "flex": 1,
                                "padding": "20px",
                                "background-color": "#ffffff",                    # sfondo bianco
                                "box-shadow": "0 4px 8px rgba(0, 0, 255, 0.2)",     # ombra standard diciamo
                                "border": "2px solid #dee2e6",                      # bordo di 2px grigio
                                "border-radius": "15px"                             # bordi arrotondati
                            },
                            children=[
                                html.H5("Glicemia media dei pazienti gestiti da ciascun diabetologo", style={"color" : "grey"}),
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
                                           "maxHeight": "100%"
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
        "overflow": "hidden",               # <-- cambio da overflowY:auto a overflow:hidden
        "padding": "20px",
        "backgroundColor": "#ffffff",
        "boxShadow": "0px 4px 8px rgba(0, 0, 255, 0.2)",
        "border": "2px solid #dee2e6",
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
            "display": "flex",
            "flex": 1,
            "flexDirection": "row",         
            "gap": "40px",
            "minHeight": "1"      
        },
        children=[

            # colonna pazienti
            html.Div(
                style=style_div_interno,
                children=[
                    html.H5("Richieste Pazienti", style={"color": "grey"}),
                    html.Hr(style={"margin-top": "5px"}),

                    html.Div(     # wrapper scrollabile aggiunto
                        style=style_scrollable_inner,
                        children=[
                            dcc.Dropdown(
                                id="dropdown-richieste-pazienti",           
                                placeholder="Seleziona una richiesta per visualizzarne i dettagli..."
                            ),

                            html.Div(id="alert-richiesta-paziente", style={"marginTop": "10px"}),

                            html.Div(id="dettagli-richiesta-paziente", style={"marginTop": "10px"}),

                            html.Div([
                                dbc.Button("Accetta", id="btn-accetta-paziente", color="primary"),
                                dbc.Button("Rifiuta", id="btn-rifiuta-paziente", color="danger"),
                            ], style={"display": "flex", "justifyContent": "center", "gap": "10px", "paddingTop": "10px"}),
                        ],
                    )
                ]
            ),

            # colonna diabetologi
            html.Div(
                style=style_div_interno,
                children=[
                    html.H5("Richieste Diabetologi", style={"color": "grey"}),
                    html.Hr(style={"margin-top": "5px"}),

                    html.Div(    # wrapper scrollabile aggiunto
                        style=style_scrollable_inner,
                        children=[
                            dcc.Dropdown(
                                id="dropdown-richieste-diabetologi",
                                placeholder="Seleziona una richiesta per visualizzarne i dettagli..."
                            ),

                            html.Div(id="alert-richiesta-diabetologo", style={"marginTop": "10px"}),

                            html.Div(id="dettagli-richiesta-diabetologo", style={"marginTop": "10px"}),

                            html.Div([
                                dbc.Button("Accetta", id="btn-accetta-diabetologo", color="primary"),
                                dbc.Button("Rifiuta", id="btn-rifiuta-diabetologo", color="danger"),
                            ], style={"display": "flex", "justifyContent": "center", "gap": "10px", "paddingTop": "10px"}),
                        ]
                    )
                ]
            )
        ]
    )



# layout principale della pagina della richiesta di inserimento nella piattaforma
admin_request = html.Div(
    style={ 
        "flex": "1",
        "display": "flex",
        "flexDirection": "column",
        "height": "100vh",
        "boxSizing": "border-box",
        "margin": "0",
        "padding": "40px",
        "gap": "20px",
        "overflow": "auto"
    },
    children=[
        render_richieste_account()
    ]
)



# funzione che prende i dati e li rende sotto forma di card piu carin e leggibile 
def render_dati_richiesta(dati):
    if not dati:
        return dbc.Alert("Nessuna richiesta trovata.", color="warning")

    def info(label, value):                         # funzione che genera ogni singola riga di informazione
        return html.P([
            html.Span(f"{label}: ", style={"fontWeight": 600}),
            html.Span(str(value))
        ], style={
            "marginBottom": "0.5rem",
            "fontSize": "1rem",
            "lineHeight": "1.6"
        })

    return dbc.Card(
        dbc.CardBody([
            html.H5(f"{dati['nome']} {dati['cognome']}", className="mb-3", style={"fontSize": "1.4rem"}),

            info("Codice Fiscale", dati["codice_fiscale"]),
            info("Data di nascita", dati["data_nascita"]),
            info("Sesso", dati["sesso"]),
            info("Indirizzo", dati["indirizzo"]),
            info("Città", dati["citta"]),
            info("CAP", dati["cap"]),
            info("Telefono", dati["telefono"]),
            info("Email", dati["email"]),

            html.Hr(style={"margin": "1rem 0"}),

            info("Tipo account", "Paziente" if dati["paziente"] else "Diabetologo"),
            info("Data richiesta", dati["data_richiesta"]),
            info("Stato", dati["stato_richiesta"]),
        ]),
        className="shadow-sm w-100 mb-2",
        style={ "padding": "0.75rem",
                "border": "1px solid #ced4da",       # stile del bordo della card della richiesta
                "borderRadius": "0.25rem"}
    )





# funzione che crea l'elenco di pazienti dato un dict di pazienti.
def render_lista_pazienti(pazienti):
    return html.Div(
        className="card",
        style={                                 # CONTENITORE ESTERNO
            "flex": 1,
            "display": "flex",
            "flexDirection": "column",
            "border": "2px solid #dee2e6",
            "borderRadius": "15px",
            "padding": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 255, 0.2)",
            "overflow": "hidden",               # nasconde la scrollbar esterna
            "maxHeight": "100vh",          
        },
        children=[
            # titolo della lista pazienti. Ho allineato il tutto con i precedenti titoli e con la linietta sotto "MyAPP"
            html.H5("Lista Pazienti", style={"color": "grey", "padding": "10px", "paddingBottom" :"8px"}),
            html.Hr(style= {"margin-top": "2px", "width": "93.5%", "alignSelf": "center"}),
            
            html.Div(
                style={                         # CONTENUTO SCROLLABILE
                    "display": "flex",
                    "flexDirection": "column",
                    "padding": "5px",
                    "paddingRight": "5px",     
                    "overflowY": "auto",
                    "boxSizing": "border-box",
                    "maxHeight": "70vh",        # REGOLA L'ALTEZZA DELLA ZONA DOVE APPAIONO I PULSANTI. PARAMETRO BUONO PER IL MIO PC (14 POLLICI). 
                },
                children=[
                    dbc.Button(                             # LISTA DI BOTTONI
                        f"{d['nome']} {d['cognome']}",
                        id={"type": "btn-paziente", "index": d["id_paziente"]},
                        color="light",
                        style={
                            "textAlign": "left",
                            "marginBottom": "10px",
                            "border": "1px solid #ccc",
                            "borderRadius": "10px",
                            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        },
                        className="text-start"
                    )
                    for d in pazienti
                ]
            )
        ]
    )


# funzione che da il layout COMPLETO della pagina di gestione dei pazienti dell'admin.
def layout_lista_pazienti():
    pazienti = model.get_all_pazienti()

    if not pazienti:
        return dbc.Alert("Nessun paziente registrato.", color="warning")

    return html.Div(
        style={
            "flex": 1,
            "display": "flex",
            "flexDirection": "row",
            "padding": "20px",
            "gap": "40px",
        },
        children=[

            # colonna sinistra: elenco pazienti
            html.Div(
                id= "contenitore-lista-pazienti",
                children= render_lista_pazienti(pazienti),
                style={
                    "flex": 1,
                }    
            ),
            
            # colonna destra: dettagli del paziente selezionato
            html.Div(
                id="dettagli-paziente",
                style={
                    "flex": 2,
                    "display": "flex",
                    "flexDirection": "column",
                },
                children=[
                    html.H5("Seleziona un paziente per visualizzarne i dettagli", style={"color": "grey", "padding": "20px"}),
                ]
            )
        ]
    )

# funzione che crea la card dove vengono visualizzati i dettagli del paziente selezionato dalla lista
def crea_card_paziente(dati_paziente, dati_diab):
    """Crea e restituisce la Card dei dettagli del paziente."""

    header_content = html.Div([
        html.Span(
            f"Paziente: {dati_paziente.get('nome', '')} {dati_paziente.get('cognome', '')}",
            style={'font-weight': 'bold', 'font-size': '1.1rem'}
        ),
        html.Span(
            children=[
                "(Diabetologo: ",
                html.Span(
                    f"{dati_diab.get('nome', '')} {dati_diab.get('cognome', '')}" if dati_diab else "Nessun diabetologo associato",
                    style={'font-style': 'italic', 'color': "#5A5A5A"}
                ),
                ")"
            ],
            style={'font-size': '0.95rem', "marginLeft": "40px"}
        ) if dati_diab else None
    ])

    dettagli = [
        dbc.ListGroupItem([
            html.Strong(f"{k.capitalize().replace('_', ' ')}: "),
            html.Span(str(v))
        ])
        for k, v in dati_paziente.items()
    ]

    return dbc.Card(
        [
            dbc.CardHeader(html.H5(header_content, style={'font-size': '1.1rem'})),
            dbc.CardBody(
                [
                    dbc.ListGroup(dettagli, flush=True, 
                        style={
                            "maxHeight": "50vh",
                            "overflowY": "auto",
                            "paddingBottom": "2px",
                            "border": "1px solid #dee2e6",
                            "borderRadius": "1px",
                            "width": "100%"
                        },
                        className="w-100"
                    ),

                    html.Div(
                    [
                        # prima riga pulsanti
                        dbc.Row([
                            dbc.Col(dbc.Button("Grafico glicemia paziente",
                                            id="btn-graf-paziente",
                                            color="primary",
                                            size="medium",
                                            className="w-100"), width=6),
                            dbc.Col(dbc.Button("Modifica dati paziente",
                                            id="btn-modifica-dati-paz",
                                            size="medium",
                                            className="w-100",
                                            style={
                                                "border": "#FF9100",
                                                "backgroundColor": "#FF9100"
                                                }), width=6),
                        ], justify="center", className="mb-2"),

                        # seconda riga pulsanti
                        dbc.Row([
                            dbc.Col(dbc.Button("Rimuovi paziente",
                                            id="btn-rimuovi-paz",
                                            color="danger",
                                            size="medium",
                                            className="w-100"), width=6),
                            dbc.Col(),      # vuoto per mantenere forma 
                            ], justify="center"),
                    ],
                    style={
                        "marginTop": "16px",
                        "display": "flex",
                        "flexDirection": "column",
                        "justifyContent": "center",
                        "width": "100%"},
                    className="w-100")

                ],
                style={
                    "display": "flex",
                    "flexDirection": "column",
                    "height": "100%",
                    "padding": "0",          # IMPORTANTE: FA SI CHE IL CONTENUTO DELLA CARD BODY (le info del paziente) SI PRENDANO IL GIUSTO SPAZIO
                    "width": "100%",
                }, 
                className="w-100"
            ),

            # salva l'id del paziente, in modo da usarlo per la callback col grafico
            dcc.Store(      
                id= "store-id-paziente",
                data= dati_paziente.get('id_paziente')
            ),

            # POP-UP DEL GRAFICO DEL PAZIENTE
            dbc.Modal(
                [
                    dbc.ModalHeader("Grafico glicemia paziente"),
                    dbc.ModalBody(
                        html.Div(
                            id="contenitore-popup-graf-paziente",
                            children=[],                                    # inizialmente vuoto, quando si clicca il pulsante viene messo il grafico
                            style={"width": "100%", "height": "90%"}        # dimensioni ottimizzate, ho controllato su due schermi diversi
                        ),
                        style={"padding": "2px"}  
                    ),
                ],
                id="pop-admin-grafico-paziente",
                is_open=False,
                size="xl",  
                centered=True          
            ),

            # pop-up per la rimozione del paziente selezionato
            dbc.Modal(
                [
                    dbc.ModalHeader("Attenzione!"),
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
            )
        ],
        style={"boxShadow": "0 4px 8px rgba(0, 0, 255, 0.2)", "maxHeight": "100vh"},
        className="w-100"
    )


# PAZIENTI ADMIN PRINCIPALE. riunisce tutto ciò che c'è di grafico riguardo alla pagina url "/admin-patient"
admin_patient = html.Div(
    id= "contenitore-admin-layout-gestione-pazienti",
    style={
        # la doctor_dashboard si adatta automaticamente allo spazio disponibile
        'flex' : 1,

        'display': 'flex',
        # "row" = da sinistra a destra
        'flex-direction': 'row',
        # sazio dai margini esterni
        'padding': '20px',
        # spazio interno tra le colonne
        'gap': '20px'
    },
    children=[
        layout_lista_pazienti()
    ]
)

# funzione per il layout dell'elenco diabetologi
def render_lista_diabetologi(diabetologi):
    return html.Div(
        className="card",
        style={                 # CONTENITORE ESTERNO
            "flex": 1,
            "display": "flex",
            "flexDirection": "column",
            "border": "2px solid #dee2e6",
            "borderRadius": "15px",
            "padding": "10px",
            "boxShadow": "0 4px 8px rgba(0, 0, 255, 0.2)",
            "overflow": "hidden",           # nasconde scrollbar esterna
            "maxHeight": "100vh",           
        },
        children=[
            # titolo della lista dibetologi. Ho allineato il tutto con i precedenti titoli e con la linietta sotto "MyAPP"
            html.H5("Lista Diabetologi", style={"color": "grey", "padding": "10px", "paddingBottom" :"8px"}),
            html.Hr(style= {"margin-top": "2px", "width": "93.5%", "alignSelf": "center"}),
            
            html.Div(
                style={         # CONTENUTO SCROLLABILE
                    "display": "flex",
                    "flexDirection": "column",
                    "padding": "5px",
                    "paddingRight": "5px",   # spazio extra sulla destra per ospitale la scrollbar
                    "overflowY": "auto",
                    "boxSizing": "border-box",
                    "maxHeight": "83vh",                        # IMPORTANTE: L'ALTEZZA DELLA LISTA DI BOTTONI PAZIENTE è DEFINITA QUI. QUESTO PARAMETRO è BUONO PER IL MIO PC (14 POLLICI)
                },
                children=[
                    
                    # bottoni che compongono l'elenco di diabetologi
                    dbc.Button(
                        f"{d['nome']} {d['cognome']}",
                        id={"type": "btn-diabetologo", "index": d["id_diabetologo"]},
                        color="light",
                        style={
                            "textAlign": "left",
                            "marginBottom": "10px",
                            "border": "1px solid #ccc",
                            "borderRadius": "10px",
                            "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                        },
                        className="text-start"
                    )
                    for d in diabetologi
                ]
            )
        ]
    )


# renderizza in modo corretto e uguale alla pagina dei pazienti, il layout.
def layout_lista_diabetologi():
    diabetologi = model.get_all_diabetologi()

    if not diabetologi:
        return dbc.Alert("Nessun diabetologo registrato.", color="warning")

    return html.Div(
        style={
            "flex": 1,
            "display": "flex",
            "flexDirection": "row",
            "padding": "20px",
            "gap": "40px"
        },
        children=[

            # elenco dei diabetologi
            html.Div(
                id="contenitore-lista-diabetologi",
                children= render_lista_diabetologi(diabetologi),
                style= {"flex": 1}
            ),

            # card a destra della lista diabetologi, con dentro i dettagli 
            html.Div(
                id="dettagli-diabetologo",
                style={
                    "flex": 2,
                    "display": "flex",
                    "flexDirection": "column",
                },
                children=[
                    html.H5("Seleziona un diabetologo per visualizzarne i dettagli", style={"color": "grey", "padding": "20px"}),
                ]
            )
        ]
    )

# funzione che crea la card dove vengono visualizzati i dettagli del diabetologo selezionato dalla lista
def crea_card_diabetologo(dati_diabetologo):
    """Crea e restituisce la Card dei dettagli del diabetologo."""

    # header
    header_content = html.Span(
        f"Diabetologo: {dati_diabetologo.get('nome', '')} {dati_diabetologo.get('cognome', '')}",
        style={'font-weight': 'bold', 'font-size': '1.05rem', 'margin-right': '10px'}
    )

    # dettagli
    dettagli = [
        dbc.ListGroupItem([
            html.Strong(f"{k.capitalize().replace('_', ' ')}: "),
            html.Span(str(v))
        ])
        for k, v in dati_diabetologo.items()
    ]

    return dbc.Card(
        [
            dbc.CardHeader(html.H5(header_content, style={'font-size': '1.1rem'})),
            dbc.CardBody([
                    dbc.ListGroup(dettagli, flush=True, style={
                        "maxHeight": "50vh",
                        "overflowY": "auto",
                        "paddingRight": "2px",
                        "border": "1px solid #dee2e6",
                        "borderRadius": "1px",
                    }),

                    html.Div([
                        # prima riga di pulsanti
                        dbc.Row([
                            dbc.Col(dbc.Button("Glicemia media pazienti",
                                            id="btn-graf-paz-assoc-diab",
                                            color="primary",
                                            size="medium",
                                            className="w-100"), width=6),
                            dbc.Col(dbc.Button("Modifica dati diabetologo",
                                            id="btn-modifica-dati-diab",
                                            style={
                                                "border": "#FF9100",
                                                "backgroundColor": "#FF9100"
                                                },
                                            size="medium",
                                            className="w-100"), width=6),
                        ], justify="center", className="mb-2"),

                        # seconda riga
                        dbc.Row([
                            dbc.Col(dbc.Button("Rimuovi diabetologo",
                                            id="btn-rimuovi-diab",
                                            color="danger",
                                            size="medium",
                                            className="w-100"), width=6),
                            dbc.Col(dbc.Button("Pazienti associati diabetologo",
                                            id="btn-lista-paz-assoc-diab",
                                            size="medium",
                                            className="w-100",
                                            style={
                                                "border": "#21BB35",
                                                "backgroundColor": "#21BB35"
                                                }), width=6),
                        ], justify="center")], 
                        
                        style={
                            "marginTop": "16px",
                            "display": "flex",
                            "flexDirection": "column",
                            "justifyContent": "center",
                        }
                    )
            ],
                style={"display": "flex",
                "flexDirection": "column",
                "height": "100%",
                "padding": "0",          # IMPORTANTE: FA SI CHE IL CONTENUTO DELLA CARD BODY (le info del paziente) SI PRENDANO IL GIUSTO SPAZIO,
                "paddingBottom": "0px"}),


            # salva l'id del diabetologo, in modo da usarlo per la callback col grafico
            dcc.Store(      
                id= "store-id-diabetologo",
                data= dati_diabetologo.get('id_diabetologo')
            ),

            # POP-UP DEL GRAFICO DEL DIABETOLOGO
            dbc.Modal(
                [
                    dbc.ModalHeader("Glicemia media pazienti associati"),
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

            # POP-UP per la rimozione del diabetologo selezionato
            dbc.Modal(
                [
                    dbc.ModalHeader("Attenzione!"),
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
            )      
        ],
        style={"boxShadow": "0 4px 8px rgba(0, 0, 255, 0.2)", "maxHeight": "100vh"}
    )


# funzione che crea la lista di pazienti associati a un diabetologo visualizzato dentro il modal del pulsante "lista pazienti associati" 
def genera_lista_pazienti_associati(lista_pazienti):
    
    if not lista_pazienti:
        return dbc.Alert(
            "Nessun paziente associato.",
            color="danger",  # rosso
            className="text-center",  # centra il testo orizzontalmente
            style={
                "padding": "20px",
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



# DIABETOLOGI ADMIN PRINCIPALE. riunisce tutto ciò che c'è di grafico riguardo alla pagina url "/admin-doctor"
admin_doctor = html.Div(
    id= "contenitore-admin-layout-gestione-diabetologi",
    style={
        # la doctor_dashboard si adatta automaticamente allo spazio disponibile
        'flex' : 1,
        'display': 'flex',
        # "row" = da sinistra a destra
        'flex-direction': 'row',
        # spazio dai margini esterni
        'padding': '20px',
        # spazio interno tra le colonne
        'gap': '20px'
    },
    children=[
        layout_lista_diabetologi()
    ]
)
#################################################################
def layout_lista_messaggi(messaggi):
    """Genera card messaggi allineate a sx/dx in base al mittente.
    
    Args:
        messages: Lista di tuple (contenuto, orario,d_is_mittente, user_is_diabetologo). ci appendo i messaggi della query
    """
    message_cards = []
    data_precedente = None  #variabile per capire quando si cambia giorno
    for contenuto, orario, giorno, d_is_mittente, user_is_diabetologo in messaggi:
        is_sender = (user_is_diabetologo == d_is_mittente) #se l'utente è il diabetologo e il diabetologo è il mittente allora lo user è il mittente
        if giorno != data_precedente:
            #card che segna la data
            day_header = dbc.Card(
                children = giorno,
                style={
                    'display': 'inline-block',
                    'width': '120px',
                    'height': '100px',
                    'maxHeight': 'fit-content',
                    'padding-left': '0.618rem',
                    'fontSize': '0.8rem',
                    'maxWidth': '62%',
                    'margin': '5px auto',
                    'textAlign': 'center'
                }
            #className="d-inline-block"  # Classe Bootstrap per inline-block
            )
            message_cards.append(day_header)
            data_precedente = giorno
        # Stile dinamico
        card_style = {
            'maxWidth': '62%',
            'width': 'fit-content',  # Adatta la larghezza al testo
            'minHeight': 'auto',     # Altezza minima automatica
            'maxHeight': 'fit-content',
            'marginLeft': 'auto' if is_sender else '0',
            'marginRight': '0' if is_sender else 'auto',
            'marginBottom': '10px',
            'padding': '8px 12px',
            'backgroundColor': "#00B7FF" if is_sender else '#ECECEC',
            'borderRadius': '12px',
            'wordBreak': 'break-word',  #Forza a capo per parole lunghe
            'height':'100px',
            'fontSize': '1.2em'
        }        
        card = dbc.Card(
            dbc.CardBody([
                contenuto,
                html.Br(),
                html.Small(
                    orario, 
                    className="text-muted mt-1", 
                    style={
                        'position': 'absolute',
                        'right': '5px',
                        'bottom': '5px',
                        'color': '#999',
                        'fontSize': '0.8rem'
                    }
                )
            ]),
            style=card_style
        )
        message_cards.append(card)
    
    return message_cards

def render_lista_contatti(contatti):
    return html.Div(
        className="card",
        style={
            "flex": 1,
            "display": "flex",
            "flexDirection": "column",
            "padding": "18px",
            "overflowY": "auto",
            "maxHeight": "87.5vh",
            "border": "2px solid #dee2e6",
            "borderRadius": "15px",
            "boxShadow": "0 4px 8px rgba(0, 0, 255, 0.2)",
        },
        children=[
            # html.H4("Pazienti", style={"color": "grey"}),
            # html.Hr(),
            *[
                dbc.Button(
                    f"{c['nome']} {c['cognome']}",
                    id = {
                        "type": "btn-contatto",
                        "index": c["id"],
                    },
                    color="light",
                    style={
                        "textAlign": "left",
                        "marginBottom": "10px",
                        "border": "1px solid #ccc",
                        "borderRadius": "10px",
                        "boxShadow": "0 2px 4px rgba(0,0,0,0.1)",
                    },
                    className="text-start",
                )
                for c in contatti
            ]
        ]
    )

def layout_lista_contatti():
    contatti = model.get_contatti()


    if not contatti:
        return dbc.Alert("Nessun contatto registrato.", color="warning")

    return html.Div(

        children=[
            # Colonna sinistra: elenco pazienti
            render_lista_contatti(contatti)
        ]
    )


# CHAT
#   ____________
#   |   |      |
#   | 1 |   2  |
#   |   |      |
#   |___|______|

chat_content = html.Div(
    style={
        "flex": 1,
        "display": "flex",
        "flexDirection": "row",  # Dash usa camelCase per gli stili
        "padding": "40px",
        "gap": "40px",
        "height": "100vh"  # Importante per il contenitore principale
    },
    children=[
        # Pannello sinistro - Lista chat
        html.Div(
            className="card",  
            style={
                "flex": 1,  # Occupa 1 parte dello spazio
                "display": "flex",
                "flexDirection": "column",
                "minWidth": "300px",  # Larghezza minima
                "overflowY": "auto"  # Scroll se necessario
            },
            children=[
                html.H2("Chat", style={"color": "grey"}),
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
                # Occupa 2/3 dello spazio disponibile
                "flex": 2,
                "display": "flex",
                # definisce la direzione degli elementi in un contenitore di tipo flex : "column" = dall'alto verso il basso
                "flexDirection": "column",
                "box-shadow": "0 4px 8px rgba(0, 0, 255, 0.2)",
                "border": "2px solid #dee2e6",
                # Arrotonda gli angoli
                "border-radius": "15px",
                "overflow": "hidden",
            },
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
                        "padding": "2rem 2rem",
                        "borderBottom": "2px solid #dee2e6",
                        
                    },
                    children=[
                        html.Div(id="nome-contatto", className="chat-header"),  # Aggiungi questo
                        dcc.Store(id="id-contatto-store", storage_type="memory") #memorizza l'id del contatto
                    ]
                ),

                # Contenitore dei messaggi:
                html.Div(
                    id="chat-box",
                    style={
                        "flex": "1",
                        # Occupa il 100% dello spazio disponibile in larghezza
                        "width": "100%",
                        # Occupa solo l'80% dello spazio disponibile in altezza
                        "height": "80%",
                        'display': 'flex',
                        # direzione degli elementi nel box: "column" = dall'alto al basso
                        'flexDirection': 'column',
                        # mostra la barra dello scroll verticale (y axis) : "auto" = solo se il contenuto
                        # eccede l'altezza del contenitore
                        'scrollbarWidth': 'thin',  
                        'scrollbarColor': '#cccccc transparent',
                        'overflowY': 'auto',
                        'padding': '20px',
                        # Nessuno sfondo inserito
                    }, 
                ),
                dcc.Interval(
                    id='interval-component',
                    interval=1000,
                    n_intervals = 0
                ),
                # Contenitore dell'Input:
                html.Div(
                    style={
                        # Occupa il 100% dello spazio disponibile in larghezza
                        "width": "100%",
                        # Occupa solo il 10% dello spazio disponibile in altezza
                        "height": "10%",
                        'padding': '20px',
                        # sfondo bianco
                        "background-color": "#ffffff",
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "borderTop": "2px solid #dee2e6"
                    },
                    children=[
                        # Input text per il messaggio
                        dbc.Input(
                            placeholder="Invia un messaggio...",
                            type="text",
                            id="input-text",
                            className='input',
                            debounce=True,
                            n_submit=0
                        ),
                        dbc.Button(
                            "+", color="primary",
                            id="send-btn",
                            style={
                                "display": "flex",
                                "justifyContent": "center",
                                "align-items": "center",
                                "width": "55px",
                                "height": "55px",
                                "border-radius": "50%",
                                "margin": "0",
                                "padding": "0",
                                "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                                "fontSize": "50px",
                                "lineHeight": "normal"
                            },
                            n_clicks = 0
                        )
                    
                    ]
                )
            ]
        )
    ]
)