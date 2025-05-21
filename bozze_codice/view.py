from dash import dcc, html
import dash_bootstrap_components as dbc

# Layout dell'app. DA FARE
def getLayout():
    return html.Div([
        dcc.Location(id= "url", refresh= True),
        html.Div(id= "contenuto-pagina")
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
            "Sign Up",
            # Rimanda al link "/signup"     -> Da modificare
            href="/signup",
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
