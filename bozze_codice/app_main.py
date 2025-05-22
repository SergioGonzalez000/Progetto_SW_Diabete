import dash
import dash_bootstrap_components as dbc
from flask_login import LoginManager
import os

# funzioni fatte da me
import view 
import control 

# inizializzazione app con dbc
app = dash.Dash(__name__, 
                external_stylesheets=[dbc.themes.BOOTSTRAP],
                suppress_callback_exceptions=True)

server = app.server

# environment secret key scelta a caso (dovrà essere sicura)
server.secret_key = os.environ.get('SECRET_KEY', 'wthellybronjames')

# configurazione Flask-Login
login_manager = LoginManager()
login_manager.init_app(server)
login_manager.login_view = '/login'


#*******************************************************************************************************
# Per testare, ho impostato di default la visualizzazione del layout di login!!!
control.registra_callbacks(app)
app.layout = view.registration_layout()

# avvio app
if __name__ == '__main__':
    app.run(debug=True)

