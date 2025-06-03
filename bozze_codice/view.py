from dash import dcc, html
import dash_bootstrap_components as dbc

# Layout dell'app, intero. Si aggiorna quando viene cambiato l'url.
def getLayout():
    return html.Div([
        # html.Div("navbar-container"),
        guest_navbar,
        profile_offcanvas,
        dcc.Location(id= "url", refresh= True),
        html.Div(id= "contenuto-pagina")
    ])

# ******************************************************************************************************************
# NAVBAR + OFFCANVAS

# id = "profile-offcanvas"
profile_offcanvas = dbc.Offcanvas(
    [
        html.Hr(),
        html.H5("** Qui i links**"),
        html.Hr(),

        # DA COMPLETARE

        html.Span("Chiudi sessione: "),
        html.A(
            "Logout",
            href="/dashboard",
            className="text-danger"
        )
    ],
    id="profile-offcanvas",
    title=html.Div(
        "Profilo",
        style={"fontSize": "2rem", "fontWeight": "bold"}
    ),
    # Apri l'offcanvas sul lato destro della pagina
    placement="end",
    # Se True all'esecuzione è aperto
    is_open=False
)

# Per modificare la dimensione di ogni link della navbar scrivere qua:
dimensione_font = {"fontSize": "1.5rem"}

# Navbar per pazienti
patient_navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/home", className="mx-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Glicemia", href="/glicemia", className="me-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Grafici", href="/graph", className="me-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Chat", href="/chat", className="me-3", style=dimensione_font))
    ],
    navbar=True
)

# Navbar per dottori
doctor_navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/home", className="mx-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Pazienti", href="/patient", className="me-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Chat", href="/chat", className="me-3", style=dimensione_font))
    ],
    navbar=True
)

# Navbar per admin
admin_navbar = dbc.Nav(
    [
        dbc.NavItem(dbc.NavLink("Home", href="/home", className="mx-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Richieste", href="/request", className="me-3", style=dimensione_font)),
        dbc.NavItem(dbc.NavLink("Pazienti", href="/patient", className="me-3", style=dimensione_font))        
    ],
    navbar=True
)

# Pulsante per aprire l'offcanvas di controllo
# id = "open-offcanvas"
profile_button = dbc.Button(
    "≡", 
    id="open-offcanvas",
    style=dimensione_font, 
    n_clicks=0, 
    color="primary",
    size="lg",
    className="ms-auto"
)

# NAVBAR PER OSPITI
guest_navbar = dbc.Navbar(
    dbc.Container([
        # Brand
        dbc.NavbarBrand("App Diabete", href="/", style={"fontSize": "2rem"}),
        
        # Link di navigazione
        dbc.Nav(
            [
                dbc.NavItem(dbc.NavLink("Home", href="/", className="mx-3", style=dimensione_font)),
                dbc.NavItem(dbc.NavLink("Login", href="/login", className="me-3", style=dimensione_font)),
                dbc.NavItem(dbc.NavLink("Registration", href="/registration", className="me-3", style=dimensione_font)),
                dbc.NavItem(dbc.NavLink("Admin", href="/admin", className="me-3", style=dimensione_font)),
            ], 
            navbar=True,
            className="me-auto"
        )  
    ]),
    color="primary",
    dark=True,
    sticky="top",
    # NavBar alta 90 pixels
    style={"height": "90px"}
) 

# NAVBAR PER UTENTI 
# formata da: [Brand | NavLinks | ≡]
# I navLinks vengono modificati con una callback in base allo stato di autenticaione
# id = "authenticated-links"
user_navbar = dbc.Navbar(
    dbc.Container([
        # Brand
        dbc.NavbarBrand("App Diabete", href="/", style={"fontSize": "2rem"}),

        # Link delle pagine nel lato sinistro
        # html.Div(id="authenticated-links"),
        patient_navbar,                              # DA MODIFICARE CON LA CALLBACK

        # Pulsante del profilo a destra
        profile_button
    ]),
    color="primary",
    dark=True,
    sticky="top",
    # NavBar alta 90 pixels
    style={"height": "90px"}
)

# ******************************************************************************************************************

def admin_layout():
    
    admin_title = html.H2(
        "Benvenuto amministratore",
        style={"textAlign": "left"},
        className="mt-2"
    )

    buttons_options = html.Div([
        html.H6("Funzionalità disponibili"),
        dbc.Button("Grafico complessivo andamento glicemia", id="bottone_grafico_complessivo", n_clicks=0)],
        className="mb-2"
        )

    return dbc.Container([
        admin_title,
        buttons_options
    ])

# ******************************************************************************************************************
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
            href="/register",
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


# ******************************************************************************************************************

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

# da fare e aggiungere nella callback del routing
# implementazione aggiunta (AI) solo per fare un check delle classi nel model
def home_layout():
    return html.Div(
        className="home-container",
        children=[
            # Titolo della pagina
            html.H1("Home", className="text-center my-4"),
            
            # Riga con due pulsanti
            dbc.Row(
                justify="center",
                children=[
                    dbc.Col(
                        dbc.Button(
                            "Azione 1",
                            id="btn-1",
                            color="primary",
                            className="mx-2"
                        ),
                        width="auto"
                    ),
                    dbc.Col(
                        dbc.Button(
                            "Azione 2", 
                            id="btn-2",
                            color="danger",
                            className="mx-2"
                        ),
                        width="auto"
                    )
                ],
                className="mb-4"
            ),
            
            # Container per output testuale 1
            dbc.Card(
                [
                    dbc.CardHeader("Risultato Azione 1"),
                    dbc.CardBody(
                        dcc.Markdown(id="output-text-1", children="*Nessun risultato ancora*")
                    )
                ],
                className="mb-4"
            ),
            
            # Container per output testuale 2
            dbc.Card(
                [
                    dbc.CardHeader("Risultato Azione 2"),
                    dbc.CardBody(
                        dcc.Markdown(id="output-text-2", children="*Nessun risultato ancora*")
                    )
                ]
            )
        ]
    )

# ******************************************************************************************************************