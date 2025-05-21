# gestione Database remoto, gestione altra roba logica
import dash_bootstrap_components as dbc
import psycopg2
from flask_login import UserMixin, login_user, logout_user, current_user 
import dash

connection = psycopg2.connect(
    host='aws-0-eu-central-2.pooler.supabase.com',
    dbname='postgres',
    user='postgres.dozqdfylbqeriitzoblm',
    password='IOtRbsJmgylEH5Pl',
    port='5432'
)

cur=connection.cursor()

# srj - Persona deve ereditare da UserMixin per permettere l'autenticazione con Flask
#       Da fare
class Persona(UserMixin):
    def __init__(self):
        pass
      
class Paziente(Persona):
    def __init__(self):
        super().__init__()

class Diabetologo(Persona):
    def __init__(self):
        super().__init__()

class Admin(Persona):
    def __init__(self):
        super().__init__()

class Terapia():
    def __init__(self):
        pass
        
class Farmaco():
    def __init__(self):
        pass

class Glicemia():
    def __init__(self):
        pass


# srj - Funzione che cerca lo username nel database e se c'è
#       confronta la password inserita da utente con quella 
#       nel database
def check_username_pw(username, password):
    
    query_ricerca_username = "SELECT username FROM paziente WHERE username= %s"
    cur.execute(query_ricerca_username, (username,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo

    nome_utente = cur.fetchone()

    if nome_utente:
        
        query_get_password = "SELECT pw FROM paziente WHERE username= %s"
        cur.execute(query_get_password, (username,))

        pw_utente = cur.fetchone()

        # accedo al primo elemento della tupla (psycopg returna sempre una tupla del tipo (pw,) in questo caso)
        if pw_utente[0] == password:
            return "/home", dbc.Alert('Accesso effettuato')
        else: 
            return dash.no_update, dbc.Alert('username o password non validi', color= 'danger')
    
    else: 
        return dash.no_update, dbc.Alert('username inesistente', color='danger')
        