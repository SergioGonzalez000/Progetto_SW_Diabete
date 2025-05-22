# gestione Database remoto, gestione altra roba logica
import dash_bootstrap_components as dbc
from abc import ABC,abstractmethod

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
    pass
class autenticabile():
    pass
        
    

class Persona():
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

    def genera_username(id_richiesta):
        cur.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ",(id_richiesta,))
        richiesta = cur.fetchone()
        nome=richiesta[1]
        cognome=richiesta[2]
        paziente=richiesta[11]

        if paziente:
            cur.execute("SELECT * FROM Paziente WHERE nome = %s AND cognome = %s",(nome,cognome))
            righe = cur.fetchall()
            num=len(righe)
            username=f"{nome}.{cognome}{num}_P"
        else:
            cur.execute("SELECT * FROM Diabetologo WHERE nome = %s AND  cognome = %s",(nome,cognome))
            righe = cur.fetchall()
            num=len(righe)
            username=f"{nome}.{cognome}{num}_D"

        return username


    def approva_richiesta(id_richiesta):
        cur.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ",(id_richiesta,))
        richiesta = cur.fetchone()
        _,nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, flag_paziente, _,_, password=richiesta
        if flag_paziente:
            username=Admin.genera_username(id_richiesta)
            cur.execute("""INSERT INTO Paziente 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, password))
            connection.commit()
        else:
            username=Admin.genera_username(id_richiesta)
            cur.execute("""INSERT INTO Diabetologo 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, password))
            connection.commit()



class Terapia():
    def __init__(self):
        pass
        
class Farmaco():
    def __init__(self):
        pass

class Glicemia():
    def __init__(self):
        pass

def inserisci_richiesta(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, password):
    cur.execute("""INSERT INTO RichiesteAccount 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, paziente, password) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, password))
    connection.commit()

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
        


if __name__ == '__main__':
    Admin.approva_richiesta(4)
