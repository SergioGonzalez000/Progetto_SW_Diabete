from dash import dcc, html
import dash_bootstrap_components as dbc
from flask_login import UserMixin, login_user, logout_user, current_user 


# Layout dell'app, intero. Si aggiorna quando viene cambiato l'url.
def getLayout():
    return html.Div(
        [
            dcc.Location(id="url", refresh=True),
            # sidebar fissa, laterale sinistra
            sidebar,

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
        dbc.NavLink("Home", href="/", active="exact", style={"fontSize": "20px"}, className="mb-3"),
        # Link della pagina della chat
        dbc.NavLink("Login", href="/login", active="exact", style={"fontSize": "20px"}, className="mb-3"), 
        # Link per la pagina dei pazienti
        dbc.NavLink("Registration", href="/registration", active="exact", style={"fontSize": "20px"}, className="mb-3"),
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
        dbc.NavLink("Dashboard", href="/patient-dashboard", active="exact", style={"fontSize": "20px"}, className="mb-3"),
        # Link per la pagina di grafici
        dbc.NavLink("Grafici", href="/grafici", active="exact", style={"fontSize": "20px"}, className="mb-3"),
        # Link della pagina della chat
        dbc.NavLink("Chat", href="/chat", active="exact", style={"fontSize": "20px"}, className="mb-3"),
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
        dbc.NavLink("Dashboard", href="/doctor-dashboard", active="exact", style={"fontSize": "20px"}, className="mb-3"),
        # Link per la pagina dei pazienti
        dbc.NavLink("Pazienti", href="/doctor-patient", active="exact", style={"fontSize": "20px"}, className="mb-3"),
        # Link della pagina della chat
        dbc.NavLink("Chat", href="/chat", active="exact", style={"fontSize": "20px"}, className="mb-3"),
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
        dbc.NavLink("Dashboard", href="/admin-dashboard", active="exact", style={"fontSize": "20px"}, className="mb-3"),
        # Link della pagina della chat
        dbc.NavLink("Richieste", href="/request", active="exact", style={"fontSize": "20px"}, className="mb-3"), 
        # Link per la pagina dei pazienti
        dbc.NavLink("Pazienti", href="/admin-patient", active="exact", style={"fontSize": "20px"}, className="mb-3"),
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
        html.H2("MyAPP", className="text-primary"),
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
        # Ombreggiatura esterna: 
        # 0 offset orizzontale
        # 4px ombra spostata di 4px verso il basso
        # 8px raggio di sfocatura
        # rgba() colore di sfocatura blu con opacità del 20%
        "box-shadow": "0 4px 8px rgba(0, 0, 255, 0.2)",
        # margine di 2px solido con colore #dee2e6 HEX
        "border": "1px solid rgba(255, 255, 255, 0.3)",
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

# LOGIN - Da rivedere
def login_layout():
    # Titolo
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
                    dbc.Input(type="text", id="username-input", placeholder="Username"),
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
                    dbc.Input(type="password", id="password-input", placeholder="Password"),
                    dbc.Label("Password"),
                ]
            )            
        ],
        # margin bottom 4, qui è a 4 per rendere esteticamente più carino
        className="mb-4"
    )

    # Pulsante Sign In
    # ID = "login-input"
    signIn_button = html.Div(
        [
            dbc.Button("Sign In", id="login-input", size="lg", n_clicks=0)
        ],
        # Larghezza completa nel box
        # d-grid di default usa la larghezza 100%
        className="d-grid gap-2"
    )

    # Sign Up link
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
        className="mt-2"
    )

    # srj - elemento html.Div per poter testare le callback
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

            # srj - per testare callback
            output_box
        ],
        # mx-auto: margin, x axis, imposta automaticamente; centra un elemento orizzontalmente
        # p-5: padding di 5 su ogni lato
        # bg-light: imposta uno sfondo chiaro
        # border: aggiunge un bordo sottile intorno all'elemento
        # rounded: arrotonda gli angoli del bordo
        # w-25: larghezza dell'elemento al 25% di quella del genitore
        className="mx-auto p-5 bg-light border rounded w-25")

    return dbc.Container(
        [
            form
        ],
        fluid=True,
        # vh-100: viewport height 100, altezza dell'elemento al 100% dell'altezza della finestra del browser
        # d-flex: imposta l'elemento come un contenitore flexbox, utile per allineare
        # align-items-center: allinea verticalmente -> al centro verticale della pagina 
        className="vh-100 d-flex align-items-center"
    )

# REGISTRATION - Da rivedere
def registration_layout():
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
                            dbc.Input(type="text", id="name-input", placeholder="Name"),
                            dbc.Label("Nome"),
                        ]
                    ),
                    width=6 # Metà della riga
                ),
                dbc.Col(
                    dbc.FormFloating(
                        [
                            dbc.Input(type="text", id="surname-input", placeholder="Surname"),
                            dbc.Label("Cognome")
                        ]
                    ),
                    width=6 # Metà della riga
                )
            ],
            className="mt-3 mb-3"
            ),
            # Riga del Codice Fiscale
            dbc.FormFloating(
                [
                    dbc.Input(type="text", id="codiceFiscale-input", placeholder="Codice Fiscale"),
                    dbc.Label("Codice Fiscale")
                ],
                className="mb-3"
            ),
            # Riga data di Nascita
            dbc.FormFloating(
                [
                    dbc.Input(type="date", id="dataNascita-input", placeholder="Data di Nascita"),
                    dbc.Label("Data di Nascita")
                ],
                className="mb-3"
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
                className="mt-2"
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
                    dbc.Input(type="tel", id="tel-input", placeholder="Telefono"),
                    dbc.Label("Telefono")
                ],
                className="mb-3"
            ),
            # Email
            dbc.FormFloating(
                [
                    dbc.Input(type="email", id="email-input", placeholder="Email"),
                    dbc.Label("Email")
                ],
                className="mb-3"
            ),
            # Indirizzo
            dbc.FormFloating(
                [
                    dbc.Input(type="text", id="indirizzo-input", placeholder="Indirizzo"),
                    dbc.Label("Indirizzo")
                ],
                className="mb-3"
            ),
            # Riga di Città + Cap
            dbc.Row(
                [
                    dbc.Col(
                        dbc.FormFloating([
                            dbc.Input(type="text", id="city-input", placeholder="Città"),
                            dbc.Label("Città")
                        ]),
                        width=7    
                    ),
                    dbc.Col(
                        dbc.FormFloating([
                            dbc.Input(type="number", id="CAP-input", placeholder="CAP"),
                            dbc.Label("CAP")
                        ]),
                        width=5
                    )
                ],
                className="mb-3"
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
                    dbc.CardHeader("Username:"),
                    dbc.CardBody(
                        [
                            html.P(id="generated-username")
                        ]
                    )
                ],
                className="mt-3 mb-4"
            ),
            # Scelta password
            dbc.FormFloating(
                [
                    dbc.Input(type="password", id="scelta-password", placeholder="Password"),
                    dbc.Label("Scegli una password")
                ],
                className="mb-3"
            ),
            # Conferma password
            dbc.FormFloating(
                [
                    dbc.Input(type="password", id="conferma-password", placeholder="Password"),
                    dbc.Label("Conferma password")
                ],
                className="mb-4"
            ),

            # Pulsante di registrazione
            html.Div(
                [
                    dbc.Button("Register Now", id="registration-input", size="lg", n_clicks=0)
                ],
                # Larghezza completa nel box
                # d-grid di default usa la larghezza 100%
                className="d-grid gap-2 mb-5"
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

    registration_feedback = html.Div(
        html.Div(
        [
            dbc.Alert(id="registration-feedback", is_open=False, className="mt-3")
        ],
        className="mt-3 d-flex justify-content-between",
        )
    )
       

    # Layout del form, contiene tutti gli altri oggetti del layout sopra.
    form = dbc.Form(
        [
            # Titolo
            registration_title,
            # Box per il form
            form_box,
            # Pulsanti per la navigazione
            nav_buttons,
            # Box per l'output
            registration_feedback,
        ],
        # mx-auto: margin, x axis, imposta automaticamente; centra un elemento orizzontalmente
        # p-5: padding di 5 su ogni lato
        # bg-light: imposta uno sfondo chiaro
        # border: aggiunge un bordo sottile intorno all'elemento
        # rounded: arrotonda gli angoli del bordo
        # w-25: larghezza dell'elemento al 25% di quella del genitore
        className="mx-auto p-5 bg-light border rounded w-25"
    )

    return dbc.Container(
        [
            dcc.Store(id="form-step", data= 1),  # aggiunto per far comparire il pulsante "indietro" solo nei form 2 e 3
            form
        ],
        fluid = True,
        # vh-100: viewport height 100, altezza dell'elemento al 100% dell'altezza della finestra del browser
        # d-flex: imposta l'elemento come un contenitore flexbox, utile per allineare
        # align-items-center: allinea verticalmente -> al centro verticale della pagina 
        className="mx-auto vh-100 d-flex align-items-center"
    )

# ******************************************************************************************************************
# LAYOUT DEL PAZIENTE:
# 1. Dashboard
# 2. Grafici
# 3. Chat
# ******************************************************************************************************************

# DASHBOARD DEL PAZIENTE

patient_dashboard = html.Div(
    style={
        # L'elemento attuale si adatta automaticamente a tutto lo spazio disponibile
        "flex": 1,
        # Spazio dai margini esterni
        "padding": "10px",#modifica fil per far entrare tutto nella parte azzurra -> se volete cambiate
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

                                # DA FARE

                            ]
                        ),

                        # 4 :Card Terapia
                        html.Div(
                            className="card",
                            children=[
                                html.H5("Terapia: ", style={"color" : "grey"}),
                                html.Hr(),

                                # Tabella della terapia
                                #html.Div(id="tabella-terapia")
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
                                html.Hr()

                                # DA FARE

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
                    debounce=False,
                    n_submit=0,
                    style={
                        "width": "100%", # Occupa l'intera larghezza del box padre
                        "padding": "15px 20px",
                        "border-radius": "15px",
                        "border": "none",
                        "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                        "background-color": "#f0f0f0",
                        "fontSize": "20px"
                    },
                    className="mb-3"
                ),

                # Input Farmaco:
                html.H6("Farmaco usato:", style={"color": "grey"}),
                dbc.Row(
                    [
                        dbc.Col(
                            # Inserimento del nome del farmaco
                            dcc.Input(
                                placeholder="Inserisci farmaco...",
                                type="text",
                                style={
                                    "width": "100%",
                                    "padding": "15px 20px",
                                    "border-radius": "15px",
                                    "border": "none",
                                    "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                                    "background-color": "#f0f0f0",
                                    "fontSize": "20px"
                                }
                            ),
                            width=7
                        ),

                        dbc.Col(
                            # Inserimento del dosaggio
                            dcc.Input(
                                placeholder="Dosaggio...",
                                type="text",
                                style={
                                    "width": "100%",
                                    "padding": "15px 20px",
                                    "border-radius": "15px",
                                    "border": "none",
                                    "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                                    "background-color": "#f0f0f0",
                                    "fontSize": "20px"
                                }
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
                    placeholder="Sintomi...",
                    type="text",
                    style={
                        "width": "100%", # Occupa l'intera larghezza del box padre
                        "padding": "15px 20px",
                        "border-radius": "15px",
                        "border": "none",
                        "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                        "background-color": "#f0f0f0",
                        "fontSize": "20px"
                    },
                    className="mb-3"
                ),

                html.H6("Misurata:", style={"color": "grey"}),
                html.P("Qua da inserire eventuale radioitem per la selezione del pre e del post pranzo")
            ]
        )
    ]
)

# GRAFICI DEL PAZIENTE
patient_graphs = html.Div(
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
        # definisce la direzione degli elementi in un contenitore di tipo flex : "row" = da sinistra a destra
        "flex-direction": "row",
        # spazio dai margini esterni
        "padding": "40px",
        # spazio tra le colonne
        "gap": "40px"
    },
    children=[
        # Pannello delle chat disponibili
        #   _____
        #   |   |
        #   | 1 |
        #   |   |
        #   |___|

        html.Div(
            className="card",
            style={
                # definisce la direzione degli elementi in un contenitore di tipo flex : "column" = dall'alto verso il basso
                "flex-direction": "column",
            },
            children=[
                html.H2("Chat", style={"color": "grey"}),
                html.Hr(),

                # DA FARE

                # Funzione che carica la lista delle chat disponibili per l'utente
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
                        
                        # DA MODIFICARE

                        html.H2("Nome contatto", style={"color": "grey"})
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
                        'overflowY': 'auto',
                        'padding': '20px',
                        # Nessuno sfondo inserito
                    },
                    children=[
                        # Qua verranno visualizzati i messaggi con una funzione che genera dinamicamente le bubbles
                        # children= ***nome funzione***
                    ]

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
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "borderTop": "2px solid #dee2e6",
                        "gap": "30px"
                    },
                    children=[
                        # Input text per il messaggio
                        dbc.Input(
                            placeholder="Invia un messaggio...",
                            type="text",
                            id="input-text",
                            style={
                                "width": "70%",
                                "padding": "15px 20px",
                                "border-radius": "15px",
                                "border": "none",
                                "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                                "background-color": "#f0f0f0",
                                "fontSize": "20px"
                            }
                        ),

                        # Pulsante invio
                        # NB: il "+" non è perfettamente centrato
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
                            }
                        )
                    ]
                )
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
                        html.H5("Torta dei pazienti:", style={"color" : "grey"}),
                        html.Hr(),
                        # Grafico a torta + legenda che mostra i pazienti con bollino rosso/giallo/verde
                        html.Div( id="patient-pie", style={"height": "100%","width": "100%"})
                    ],
                    style={"flex": 1},
                    className="card",
                ),

                html.Div(
                    [
                        # Numero 5
                        html.Div(
                            [
                                html.H5("Pazienti totali:", style={"color" : "grey"}),
                                html.Hr(),
                                # Qua va inserito il numero dei pazienti (associati)
                                html.Div(
                                    [
                                        "0"
                                    ],
                                    style={
                                        "height": "100%",
                                        "width": "100%",
                                        "display": "flex",
                                        "align-items": "center",
                                        "justify-content": "center",
                                        # dimensione del numero
                                        "font-size": "150px",
                                        # colore per tutti i numeri
                                        "color": "#555"
                                    },
                                    id="patient-number"
                                )
                            ],
                            className="card"
                        ),
                        # Numero 6
                        html.Div(
                            [
                                html.H5("Grafico vario:", style={"color" : "grey"}),
                                html.Hr(),
                                # Qua va inserito un grafico ???
                                html.Div( id="graph-???", style={"height": "100%","width": "100%"})
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
            style= {
                # Occupa 2/3
                "flex": 2,
                "display": "flex",
                "flex-direction" : "column",
                # spazio tra 4 e 5/6 di 40 px
                'gap': '40px'
            },
            children=[
                # Numero 4
                html.Div(
                    [
                        html.H5("Andamento:", style={"color" : "grey"}),
                        html.Hr(),
                        # Qua va inserito il grafico dell'andamento della glicemia: settimanale di default
                        html.Div( id="patient-graph", style={"height": "100%","width": "100%"})
                    ],
                    style={"flex": 1},
                    className="card",
                ),

                html.Div(
                    [
                        # Numero 5
                        html.Div(
                            [
                                html.H5("Dati del paziente:", style={"color" : "grey"}),
                                html.Hr(),
                                # Qua vanno inserite le generalità del paziente
                                html.Div( id="patient-data", style={"height": "100%","width": "100%"})
                            ],
                            className="card"
                        ),
                        # Numero 6
                        html.Div(
                            [
                                html.H5("Terapia:", style={"color" : "grey"}),
                                html.Hr(),
                                # Qua va inserita la tabella delle terapie
                                html.Div( id="patient-therapy", style={"height": "100%","width": "100%"}),
                                dbc.Input(
                                    placeholder="Nuova terapia",
                                    type="text",
                                    id="new-therapy",
                                    # Attiva la callback solo quando l'utente digita qualcosa
                                    debounce=False,
                                    # Contatore per quando l'utente preme invio
                                    n_submit=0,
                                    style={
                                        "width": "100%", # Occupa l'intera larghezza del box padre
                                        "padding": "15px 20px",
                                        "border-radius": "15px",
                                        "border": "none",
                                        "box-shadow": "0 4px 4px rgba(0, 0, 0, 0.5)",
                                        "background-color": "#f0f0f0",
                                        "fontSize": "20px",
                                    }
                                )
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
            ]
        )
    ]
)

# CHAT (= chat_content) -> Già fatta

# ******************************************************************************************************************
# LAYOUT DELL'ADMIN:
# 1. Dashboard
# 2. Richieste
# 3. Pazienti
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
        html.H2("Da fare")
    ]
)

# RICHIESTE
admin_request = html.Div(
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
        html.H2("Da fare")
    ]
)

# PAZIENTI ADMIN
admin_patient = html.Div(
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
        html.H2("Da fare")
    ]
)