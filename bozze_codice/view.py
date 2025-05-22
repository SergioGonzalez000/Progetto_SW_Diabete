from dash import dcc, html
import dash_bootstrap_components as dbc

# Layout dell'app. DA FARE
def getLayout():
    return dbc.Container()

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
            "Sign Up",
            # Rimanda al link "/signup"     -> Da modificare
            href="/signup",
            className="text-primary"
            )
        ],
        # Padding da sopra di 2
        className="mt-2"
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
            signUp_link
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
        ]
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
        ]
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
        ]
    )

    # Pulsanti per la navigazione
    nav_buttons = html.Div(
        [
            dbc.Button("🡨", id="prev-button", n_clicks=0, color="secondary", disabled=True),
            dbc.Button("🡪", id="next-button", n_clicks=0)
        ],
        className="mt-3 d-flex justify-content-between"
    )

    # Box per il Form
    # ID = "form-box"
    form_box = html.Div(
        id="form-box",
        children=form1
    )

    # Layout del form
    form = dbc.Form(
        [
            # Titolo
            registration_title,
            # Box per il form
            form_box,
            # Pulsanti per la navigazione
            nav_buttons
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
            form
        ],
        fluid = True,
        # vh-100: viewport height 100, altezza dell'elemento al 100% dell'altezza della finestra del browser
        # d-flex: imposta l'elemento come un contenitore flexbox, utile per allineare
        # align-items-center: allinea verticalmente -> al centro verticale della pagina 
        className="mx-auto vh-100 d-flex align-items-center"
    )

# ******************************************************************************************************************