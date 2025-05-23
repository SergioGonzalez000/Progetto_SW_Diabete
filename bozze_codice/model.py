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
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        self.nome=nome
        self.cognome=cognome
        self.data_nascita=data_nascita
        self.sesso=sesso
        self.cf=codice_fiscale
        self.indirizzo=indirizzo
        self.citta=citta
        self.cap=cap
        self.tel=telefono
        self.email=email
        self.username=username
        self.pw=pw

        # nome
    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, value):
        self._nome = value

    # cognome
    @property
    def cognome(self):
        return self._cognome

    @cognome.setter
    def cognome(self, value):
        self._cognome = value

    # data_nascita
    @property
    def data_nascita(self):
        return self._data_nascita

    @data_nascita.setter
    def data_nascita(self, value):
        self._data_nascita = value

    # sesso
    @property
    def sesso(self):
        return self._sesso

    @sesso.setter
    def sesso(self, value):
        self._sesso = value

    # codice fiscale
    @property
    def cf(self):
        return self._cf

    @cf.setter
    def cf(self, value):
        self._cf = value

    # indirizzo
    @property
    def indirizzo(self):
        return self._indirizzo

    @indirizzo.setter
    def indirizzo(self, value):
        self._indirizzo = value

    # citta
    @property
    def citta(self):
        return self._citta

    @citta.setter
    def citta(self, value):
        self._citta = value

    # cap
    @property
    def cap(self):
        return self._cap

    @cap.setter
    def cap(self, value):
        self._cap = value

    # telefono
    @property
    def tel(self):
        return self._tel

    @tel.setter
    def tel(self, value):
        self._tel = value

    # email
    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        self._email = value

    # username
    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    # password
    @property
    def pw(self):
        return self._pw

    @pw.setter
    def pw(self, value):
        self._pw = value


class autenticabile():
    pass
    
      
class Paziente(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

    def inserisci_glicemia():
        pass

class Diabetologo(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)
    
    def inserici_terapia():
        pass

class Admin(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

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

    def inserisci_paziente(p: Paziente):
        cur.execute("""INSERT INTO Paziente 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (p.nome, p.cognome, p.data_nascita, p.sesso, p.cf, p.indirizzo, p.citta, p.cap, p.tel, p.email, p.username, p.pw))
        connection.commit()

    def inserisci_diabetologo(d: Diabetologo):
        cur.execute("""INSERT INTO Diabetologo 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (d.nome, d.cognome, d.data_nascita, d.sesso, d.cf, d.indirizzo, d.citta, d.cap, d.tel, d.email, d.username, d.pw))
        connection.commit()

    def approva_richiesta(id_richiesta):
        cur.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ",(id_richiesta,))
        richiesta = cur.fetchone()
        _,nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, flag_paziente, _,_, password=richiesta
        

        tipo = "paziente" if flag_paziente else "diabetologo"
        username=Admin.genera_username(id_richiesta)
        persona = PersonaFactory.crea_persona(tipo, nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, password)

        if flag_paziente:
            Admin.inserisci_paziente(persona)
        else:
            Admin.inserisci_diabetologo(persona)
        

#fil - design pattern factory, per rendere la creazione di oggetti riguardanti gli attori principali più 'elegante'
#rende anche il codice più manutenibile (in teoria)
class PersonaFactory:
    @staticmethod
    def crea_persona(tipo, nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw):
        if tipo == "paziente":
            return Paziente(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw)
        elif tipo == "diabetologo":
            return Diabetologo(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw)
        elif tipo == "admin":
            return Admin(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw)
        else:
            raise ValueError("Tipo di persona non valido")

class Terapia():
    def __init__(self):
        pass
        
class Farmaco():
    def __init__(self):
        pass

class Glicemia():
    def __init__(self):
        pass

#fil - funzione che date tutte le informazioni che il paziente inserisce nella richiesta account, 
#      procede ad inserirle effettivamente nella base di dati 
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
        


#if __name__ == '__main__':
#    Admin.approva_richiesta(8)
