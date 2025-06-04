# gestione Database remoto, gestione altra roba logica
import datetime
import dash_bootstrap_components as dbc
from abc import ABC,abstractmethod
from werkzeug.security import generate_password_hash #password criptate

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
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, password):
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
        self.pw=password

    def get_id(self):           # è il getter per gli utenti di flask-login. Deve avere questa signature, nonostante in questo caso ritorni "username"
        return self.username    # questa deve semplicemente essere una stringa univoca.
    
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

# si può scrivere nei diagrammi di classe UML senza metterla nel codice? 
class autenticabile():
    pass
    
      
class Paziente(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

    def inserisci_glicemia(id_paz, valore, farmaco, dose, sintomi="" ):
        cur.execute("""INSERT INTO Glicemia 
                    (paziente, farmaco, dosaggio, sintomo, valore) 
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (id_paz, farmaco, dose, sintomi, valore))
        connection.commit()

    # Fx che associ il paziente al diabetologo. (modifica quindi diabetologo.paziente_associato)
    # potremmo permettere al paziente di selezionare quale sarà il suo
    # medico di riferimento.
    def associa_a_diabetologo():
        pass


class Diabetologo(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)
    
    def inserisci_terapia(id_paz, id_diab, farmaco, dose, assunzioni_gg, data_inizio, data_fine):
        cur.execute("""INSERT INTO Terapia 
                    (paziente, diabetologo, farmaco, dosaggio, assunzioni_gg, data_inizio, data_fine) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s)""", 
                    (id_paz, id_diab, farmaco, dose, assunzioni_gg, data_inizio, data_fine))
        connection.commit()

    # Funzione per aggiornare la terapia corrente/i singoli campi della terapia corrente? 
    # ad es. in caso di errori
    def aggiorna_terapia_paziente():
        pass

    # Da buildare in un secondo momento.
    # Come detto dal prof, il diabetologo deve essere in grado di vedere solo i grafici delle glicemie dei pazienti 
    # a lui associati.
    def visualizza_glicemia_pazienti_associati():
        pass

    # Funzione che permetta al medico di visualizzare i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def visualizza_dati_paziente():
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


# classi Terapia, Farmaco e Glicemia abbozzate, variabili d'istanza minime necessarie, qualche idea per i metodi
class Terapia():
    def __init__(self, farmaco_prescritto, dose, via_somministrazione, periodo_terapia):
        self.farmaco_prescritto = farmaco_prescritto 
        self.dose = dose 
        self.via_somministrazione = via_somministrazione 
        self.periodo_terapia = periodo_terapia

    # Getter e Setter per farmaco_prescritto
    @property
    def farmaco_prescritto(self):
        return self._farmaco_prescritto
    
    @farmaco_prescritto.setter
    def farmaco_prescritto(self, value):
        self._farmaco_prescritto = value

    # Getter e Setter per dose
    @property
    def dose(self):
        return self._dose
    
    @dose.setter
    def dose(self, value):
        self._dose = value

    # Getter e Setter per via_somministrazione
    @property
    def via_somministrazione(self):
        return self._via_somministrazione
    
    @via_somministrazione.setter
    def via_somministrazione(self, value):
        self._via_somministrazione = value

    # Getter e Setter per periodo_terapia
    @property
    def periodo_terapia(self):
        return self._periodo_terapia
    
    @periodo_terapia.setter
    def periodo_terapia(self, value):
        self._periodo_terapia = value
        
        
class Farmaco():
    def __init__(self, nome, tipologia, unita_misura, codice_univoco):
        self.nome = nome
        self.tipologia = tipologia
        self.unita_misura = unita_misura
        self.codice_univoco = codice_univoco

    # Getter e Setter per nome
    @property
    def nome(self):
        return self._nome
    
    @nome.setter
    def nome(self, value):
        self._nome = value

    # Getter e Setter per tipologia
    @property
    def tipologia(self):
        return self._tipologia
    
    @tipologia.setter
    def tipologia(self, value):
        self._tipologia = value

    # Getter e Setter per unita_misura
    @property
    def unita_misura(self):
        return self._unita_misura
    
    @unita_misura.setter
    def unita_misura(self, value):
        self._unita_misura = value

    # Getter e Setter per codice_univoco
    @property
    def codice_univoco(self):
        return self._codice_univoco
    
    @codice_univoco.setter
    def codice_univoco(self, value):
        self._codice_univoco = value

    # fx che aggiunga un farmaco alla tabella farmaco nel db
    def aggiungi_farmaco():
        pass

    
class Glicemia():
    def __init__(self, valore, data_assunzione, ora_assunzione):
        self.valore = valore
        self.data_assunzione = data_assunzione
        self.ora_assunzione = ora_assunzione

    # Getter e setter del valore
    @property
    def valore(self):
        return self._valore

    @valore.setter
    def valore(self, valore):
        self._valore = valore

    # Getter e setter della data di assunzione
    @property
    def data_assunzione(self):
        return self._data_assunzione

    @data_assunzione.setter
    def data_assunzione(self, data_assunzione):
        self._data_assunzione = data_assunzione

    # Getter e setter dell'ora di assunzione
    @property
    def ora_assunzione(self):
        return self._ora_assunzione

    @ora_assunzione.setter
    def ora_assunzione(self, ora_assunzione):
        self._ora_assunzione = ora_assunzione
        

#fil - funzione che date tutte le informazioni che il paziente inserisce nella richiesta account, 
#      procede ad inserirle effettivamente nella base di dati 
def inserisci_richiesta(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, password):
    cur.execute("""INSERT INTO RichiesteAccount 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, paziente, password) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, generate_password_hash(password)))
    connection.commit()
        

# Funzione che prende un utente dato lo username, e restituisce un oggetto Persona.diabetologo o Persona.paziente
# n.b lo username deve essere univoco altrimenti disastro dc
# esteso per aggiungere la query sulla tabella "amministratore"
def get_by_username(username_utente):
    '''se l'utente esiste ritorna un oggetto paziente/diabetologo/admin con i campi compilati, se non esiste, ritorna None '''
    
    # ho dovuto aggiungere questo cursore locale per evitare letture sporche e sovrapposizioni nelle query (dava errori strani)
    cursore_2 = connection.cursor()

    presente_in_paziente = False     # flag per controllare se l'utente è un paz/diab
    presente_in_diabetologo = False  # flag per controllare se l'utente è un diab
    presente_in_admin = False        # flag per controllare se l'utente è un admin

    # uso il cursore che c'è già a livello globale
    query_ricerca = "SELECT nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw FROM paziente WHERE username= %s" # pw deve essere la hash
    cursore_2.execute(query_ricerca, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo
    record = cursore_2.fetchone()

    if record:      # se non c'è in paziente, cerchiamo se c'è in diabetologo. se non c'è --> controlliamo admin. se non c'è --> return None
        presente_in_paziente = True
    else:
        query_ricerca = "SELECT nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw FROM diabetologo WHERE username= %s" # pw deve essere la hash
        cursore_2.execute(query_ricerca, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo
        record = cursore_2.fetchone()

        if record:
            presente_in_diabetologo = True
        else:
            query_ricerca = "SELECT nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw FROM amministratore WHERE username= %s" # pw deve essere la hash
            cursore_2.execute(query_ricerca, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo
            record = cursore_2.fetchone()
            if record:
                presente_in_admin = True

    # se il record proviene da diabetologo, uso il costruttore del diabetologo, altrimenti del paziente
    # i dati nel recordo sarebbero (in ordine):
    # nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw
    if record and presente_in_paziente:
        return PersonaFactory.crea_persona(
            "paziente", record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11])
    elif record and presente_in_diabetologo:
        return PersonaFactory.crea_persona(
            "diabetologo", record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11])
    elif record and presente_in_admin:
        return PersonaFactory.crea_persona(
            "admin", record[0], record[1], record[2], record[3], record[4], record[5], record[6], record[7], record[8], record[9], record[10], record[11])
    return None



if __name__ == '__main__':
    #Paziente.inserisci_glicemia(17,180,'fentanylo',20.5, 'geekd up')
    # Esempio: 31 dicembre 2025, ore 10:30
    data_i= datetime.datetime(2025, 12, 31, 10, 30, 0)
    # Esempio: 31 dicembre 2025, ore 10:30
    data_f = datetime.datetime(2026, 12, 31, 10, 30, 0)

    # Diabetologo.inserisci_terapia(17,1,'molly', 10.3, 3, data_i, data_f)
