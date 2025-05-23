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
#       Da aggiugnere altra roba
class Persona(UserMixin):
    
    # costruttore. Ho usato l'attributo "username" al posto del classico id (fa nulla, perchè nel progetto lo username è univoco)
    def __init__(self, username, password):
        self.username = username    # è univoco.
        self.password = password
    
    def get_id(self):           # è il getter per gli utenti di flask-login. Deve avere questa signature, nonostante in questo caso ritorni "username"
        return self.username    # questa deve semplicemente essere una stringa univoca.


class autenticabile():
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
        

# Funzione che prende un utente.
def get_by_username(username_utente):
    '''se l'utente esiste ritorna un oggetto Persona con i campi compilati, se non esiste, ritorna None '''
    
    # non ho messo questa query direttamente nel main perchè avrei dovuto creare un cursore anche lì
    query_ricerca_username = "SELECT username, pw FROM paziente WHERE username= %s" # pw deve essere la hash
    cur.execute(query_ricerca_username, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo

    record = cur.fetchone()

    if record:
        return Persona(record [0], record[1])
    return None


# Funzione che controlla la password
def check_password(username, password_dal_form):
    query_get_password = "SELECT pw FROM paziente WHERE username= %s"
    cur.execute(query_get_password, (username,))

    pw_utente = cur.fetchone()

    # accedo al primo elemento della tupla (psycopg returna sempre una tupla del tipo (pw,) in questo caso)
    if pw_utente[0] == password_dal_form:
        return True
    else: 
        return False



if __name__ == '__main__':
    Admin.approva_richiesta(4)
