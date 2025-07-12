# gestione Database remoto, gestione altra roba logica
from collections import namedtuple
from werkzeug.security import generate_password_hash #password criptate
import psycopg2
from flask_login import UserMixin, current_user 
import plotly.graph_objects as go
import pandas as pd
import calendar
from contextlib import contextmanager

from abc import ABC, abstractmethod
from typing import List
from datetime import datetime

# Eseguito una sola volta all'avvio

class DBSingleton:
    _connection = None

    @classmethod
    @contextmanager
    def get_cursor(cls):
        if cls._connection is None or cls._connection.closed:
            cls._connection = psycopg2.connect(
                host='aws-0-eu-central-2.pooler.supabase.com',
                dbname='postgres',
                user='postgres.dozqdfylbqeriitzoblm',
                password='IOtRbsJmgylEH5Pl',
                port='5432'
            )
        
        cursor = cls._connection.cursor()
        try:
            yield cursor
            cls._connection.commit()
        except:
            cls._connection.rollback()
            raise
        finally:
            cursor.close()

    @classmethod
    def close_connection(cls):
        if cls._connection is not None:
            cls._connection.close()
            cls._connection = None



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


    



class Paziente(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)
    
    def get_id_paziente(self):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("SELECT id_paziente FROM Paziente WHERE codice_fiscale = %s", (self.cf,))
            res=cursore.fetchone()
        return res[0] 
    
    def inserisci_glicemia(self, valore, flag_pasto, sintomi=None ):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""INSERT INTO Glicemia 
                        (paziente, pasto, sintomi, valore) 
                        VALUES (%s, %s, %s, %s)""", 
                        (self.get_id_paziente(), flag_pasto, sintomi, valore))

    def inserisci_assunzione_farmaco(self, farmaco, dosaggio):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""INSERT INTO AssunzioniFarmaco 
                        (paziente, farmaco, dosaggio) 
                        VALUES (%s, %s, %s)""", 
                        (self.get_id_paziente(), farmaco, dosaggio))

    def inserisci_segnalazione(self, tipo_segnalazione, descrizione, data_inizio, data_fine=None):
        if tipo_segnalazione not in ('sintomo', 'patologia', 'terapia'):
            raise ValueError("Tipo segnalazione non valido. Deve essere 'sintomo', 'patologia' o 'terapia'.")
        print(tipo_segnalazione)
        with DBSingleton.get_cursor() as cursore:
            query = """
                INSERT INTO SegnalazioniPaziente (paziente, tipo_segnalazione, descrizione, data_inizio, data_fine)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursore.execute(query, (self.get_id_paziente(), tipo_segnalazione, descrizione, data_inizio, data_fine))

    def get_diabetologo(self):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                Select id_diabetologo, d.nome, d.cognome
                from paziente p
                join diabetologo d on d.id_diabetologo = p.diabetologo_associato
                where p.id_paziente = %s
            """, (self.get_id_paziente(),))
            result = cursore.fetchone()
            cursore.close()
            result = [
                    {
                        "id": result[0],
                        "nome": result[1],
                        "cognome": result[2],
                    }
                ]
        return result
    

    
    def inserisci_segnalazione(self,tipo,descrizione,data_i,data_f=None):
        with DBSingleton.get_cursor() as cursore:
            id=self.get_id_paziente()
            cursore.execute("INSERT INTO SegnalazioniPaziente (paziente,tipo_segnalazione,descrizione,data_inizio,data_fine) VALUES (%s,%s,%s,%s,%s)",(id,tipo,descrizione,data_i,data_f))
    


# Interfaccia Observer
class DiabetologoDeletionObserver(ABC):
    @abstractmethod
    #metodo implementato negli observer che quando viene chiamato esegue la sequenza:
    #trova nuovi diab, elimina diab, notifica pazienti con alert
    def on_diabetologo_deleted(self, deleted_diabetologo_id: int, deleted_diabetologo_name: str):
        pass

# Concrete Observer per i Pazienti
class PazienteDiabetologoObserver(DiabetologoDeletionObserver):
    def __init__(self, paziente: Paziente):
        self.paziente = paziente
    #implementazione del metodo degli observer
    def on_diabetologo_deleted(self, deleted_diabetologo_id: int, deleted_diabetologo_name: str):
        try:
            #Trova nuovo diabetologo (escludendo quello eliminato)
            nuovo_diabetologo_id = self._trova_nuovo_diabetologo(excluded_id=deleted_diabetologo_id)
            
            #Riassegna il paziente
            self._riassegna_paziente(nuovo_diabetologo_id)
            
            #Crea alert per il paziente
            self._crea_alert(deleted_diabetologo_name, nuovo_diabetologo_id)
        except Exception as e:
            print(f"Errore durante la riassegnazione del paziente {self.paziente.get_id_paziente()}: {str(e)}")
            self._crea_alert_fallback(deleted_diabetologo_name)

    def _trova_nuovo_diabetologo(self, excluded_id):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                SELECT d.id_diabetologo
                FROM Diabetologo d
                LEFT JOIN Paziente p ON d.id_diabetologo = p.diabetologo_associato
                WHERE d.id_diabetologo != %s
                GROUP BY d.id_diabetologo
                ORDER BY COUNT(p.id_paziente) ASC
                LIMIT 1
            """, (excluded_id,))
            
            result = cursore.fetchone()
            if not result:
                raise ValueError("Nessun altro diabetologo disponibile per la riassegnazione")
            return result[0]

    def _riassegna_paziente(self, nuovo_diabetologo_id):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                UPDATE Paziente
                SET diabetologo_associato = %s
                WHERE id_paziente = %s
            """, (nuovo_diabetologo_id, self.paziente.get_id_paziente()))

    def _crea_alert(self, old_diabetologo_name, new_diabetologo_id):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("SELECT nome, cognome FROM Diabetologo WHERE id_diabetologo = %s", (new_diabetologo_id,))
            new_doc = cursore.fetchone()
            new_name = f"{new_doc[0]} {new_doc[1]}" if new_doc else "un nuovo specialista"
            
            messaggio = f"Il tuo diabetologo {old_diabetologo_name} non è più disponibile. Sei stato riassegnato al Dr. {new_name}."
            cursore.execute("""
                INSERT INTO alerts (id_paziente, orario, alert_case)
                VALUES (%s, %s, %s)
            """, (self.paziente.get_id_paziente(),datetime.now(), messaggio))

    def _crea_alert_fallback(self, old_diabetologo_name):
        with DBSingleton.get_cursor() as cursore:
            messaggio = f"Il tuo diabetologo {old_diabetologo_name} non è più disponibile. Contatta l'amministrazione per la riassegnazione."
            cursore.execute("""
                INSERT INTO alerts (id_paziente, orario, alert_case)
                VALUES (%s, %s, %s)
            """, (self.paziente.get_id_paziente(),datetime.now(), messaggio))


    
class Diabetologo(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

    def get_id_diabetologo(self):
        with DBSingleton.get_cursor() as cursore:        
            cursore.execute("""SELECT id_diabetologo
                        FROM Diabetologo 
                        WHERE codice_fiscale = %s""", (self.cf,))
            id=cursore.fetchone()[0]        
        return id
    
    def inserisci_terapia(self,id_paz, farmaco, dose, assunzioni_gg, data_inizio, data_fine, indicazioni=None):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""INSERT INTO Terapia 
                        (paziente, diabetologo, farmaco, dosaggio, assunzioni_gg, data_inizio, data_fine,indicazioni) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s,%s)""", 
                        (id_paz, self.get_id_diabetologo(), farmaco, dose, assunzioni_gg, data_inizio, data_fine,indicazioni))
    
    
    def modifica_terapia_paziente(self, id_paz,id_t, farmaco, dose, assunzioni_gg, data_inizio, data_fine, indicazioni=None):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""UPDATE Terapia 
                                SET farmaco=%s, dosaggio=%s, assunzioni_gg=%s, data_inizio=%s, data_fine=%s, indicazioni=%s,data_ultima_modifica = CURRENT_DATE
                                WHERE paziente=%s and diabetologo=%s AND id_terapia=%s""", 
                                (farmaco, dose, assunzioni_gg, data_inizio, data_fine, indicazioni, id_paz, self.get_id_diabetologo(),id_t))

    
    def visualizza_n_c_pazienti_associati(self):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                SELECT p.id_paziente, p.nome, p.cognome, COALESCE(AVG(g.valore), 0) AS media
                FROM paziente p
                LEFT JOIN Glicemia g ON p.id_paziente = g.paziente
                WHERE p.diabetologo_associato = %s
                GROUP BY p.id_paziente
                ORDER BY media DESC
            """, (self.get_id_diabetologo(),))
            
            result = cursore.fetchall()

            # Conversione in lista di dizionari
            pazienti = [
                {
                    "id": r[0],
                    "nome": r[1],
                    "cognome": r[2],
                    "media": r[3],
                }
                for r in result
            ]

        return pazienti

    
# ******************************************************************************************************************
    # Funzione che permetta al medico di inserire i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def inserisci_info_paziente(self,id_paz, patologie=None, fattori=None, comorbidita=None):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""INSERT INTO InfoPaziente 
                        (paziente, diabetologo, fattori_rischio, patologie_pregresse, comorbidita) 
                        VALUES (%s, %s, %s, %s, %s)""", 
                        (id_paz, self.get_id_diabetologo(), fattori, patologie, comorbidita))

    # Funzione che permetta al medico di modificare i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def modifica_info_paziente(self,id_paz, patologie=None, fattori=None, comorbidita=None):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""UPDATE InfoPaziente 
                            SET fattori_rischio=%s, patologie_pregresse=%s, comorbidita=%s, data_ultima_modifica = CURRENT_DATE
                            WHERE paziente=%s and diabetologo=%s""", (fattori, patologie, comorbidita, id_paz, self.get_id_diabetologo()))

    # funzione che prende tutti i pazienti nella db
    def get_all_pazienti_associati(self):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("SELECT id_paziente, nome, cognome FROM paziente where diabetologo_associato = %s ORDER BY cognome", (self.get_id_diabetologo(),))
            result = cursore.fetchall()

            # Conversione in lista di dizionari
            pazienti = [
                {
                    "id": r[0],
                    "nome": r[1],
                    "cognome": r[2],
                }
                for r in result
            ]
        return pazienti


#**********************************************************************************************************************************
    # Funzione che permetta al medico di visualizzare i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def visualizza_dati_paziente(self,id_paz):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""SELECT codice_fiscale, EXTRACT(year FROM CURRENT_DATE)-EXTRACT(year FROM data_nascita), nome
                            FROM Paziente
                            WHERE id_paziente=%s
                            """,(id_paz,))
            cfannonome=cursore.fetchall()
            cursore.execute("""SELECT i.patologie_pregresse, i.fattori_rischio, i.comorbidita
                                    FROM infopaziente i
                                    WHERE i.paziente=%s
                                    ORDER BY i.patologie_pregresse, i.fattori_rischio, i.comorbidita
                                """,(id_paz, ))
            info=cursore.fetchall()
        return cfannonome,info 

    def get_segnalazioni_paziente(self,id_paziente):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                SELECT sp.tipo_segnalazione, sp.descrizione, sp.data_inizio, sp.data_fine
                FROM SegnalazioniPaziente sp
                JOIN Paziente p on sp.paziente=p.id_paziente
                WHERE sp.paziente = %s AND p.diabetologo_associato=%s
                ORDER BY sp.data_inizio DESC
            """, (id_paziente,self.get_id_diabetologo()))
            risultati = cursore.fetchall()
        return risultati
    
class Admin(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

    def get_id_admin(self):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("SELECT id_admin FROM Admin WHERE codice_fiscale = %s", (self.cf,))
            res=cursore.fetchone()
        return res[0]
    
    def genera_username(id_richiesta):
        
        with DBSingleton.get_cursor() as cursore:
        
            cursore.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ",(id_richiesta,))
            richiesta = cursore.fetchone()
            n=richiesta[1]
            nome=n.replace(" ","")
            cognome=richiesta[2]
            paziente=richiesta[11]

            if paziente:
                cursore.execute("SELECT * FROM Paziente WHERE nome = %s AND cognome = %s",(nome,cognome))
                righe = cursore.fetchall()
                num=len(righe)
                username=f"{nome}.{cognome}{num}_P"
            else:
                cursore.execute("SELECT * FROM Diabetologo WHERE nome = %s AND  cognome = %s",(nome,cognome))
                righe = cursore.fetchall()
                num=len(righe)
                username=f"{nome}.{cognome}{num}_D"

        return username

    def inserisci_paziente(p: Paziente):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""INSERT INTO Paziente 
                        (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", 
                        (p.nome, p.cognome, p.data_nascita, p.sesso, p.cf, p.indirizzo, p.citta, p.cap, p.tel, p.email, p.username, p.pw))
            

    def inserisci_diabetologo(d: Diabetologo):
        
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""INSERT INTO Diabetologo 
                        (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                        VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                        (d.nome, d.cognome, d.data_nascita, d.sesso, d.cf, d.indirizzo, d.citta, d.cap, d.tel, d.email, d.username, d.pw))

    # Fx che associ il paziente al diabetologo. (modifica quindi diabetologo.paziente_associato)
    # potremmo permettere al paziente di selezionare quale sarà il suo
    # medico di riferimento.
    def associa_a_diabetologo(paziente):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute(""" SELECT d.id_diabetologo
                                FROM diabetologo d
                                LEFT JOIN paziente p ON d.id_diabetologo = p.diabetologo_associato
                                GROUP BY d.id_diabetologo
                                ORDER BY COUNT(p.id_paziente) ASC
                                LIMIT 1;
                            """)
            id_diabetologo=cursore.fetchone()[0]
            cursore.execute("UPDATE Paziente SET diabetologo_associato=%s WHERE codice_fiscale = %s ",(id_diabetologo,paziente.cf))
    
    def approva_richiesta(id_richiesta):
        
        with DBSingleton.get_cursor() as cursore:

            cursore.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ", (id_richiesta,))
            richiesta = cursore.fetchone()
            _,nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, flag_paziente, _,_, password=richiesta
            

            tipo = "paziente" if flag_paziente else "diabetologo"
            username=Admin.genera_username(id_richiesta)
            persona = PersonaFactory.crea_persona(tipo, nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, password)

            if flag_paziente:
                Admin.inserisci_paziente(persona)
                Admin.associa_a_diabetologo(persona)
            else:
                Admin.inserisci_diabetologo(persona)

            cursore.execute("UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s ",('approvata',id_richiesta))
            

    def approva_richiesta_cf(codice_fiscale):
        with DBSingleton.get_cursor() as cursore:

                # Recupera la richiesta tramite codice fiscale
                cursore.execute("SELECT * FROM RichiesteAccount WHERE codice_fiscale = %s", (codice_fiscale,))
                richiesta = cursore.fetchone()

                if richiesta is None:
                    cursore.close()
                    raise ValueError(f"Nessuna richiesta trovata per il codice fiscale {codice_fiscale}.")

                id_richiesta, nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, flag_paziente, _, _, password = richiesta

                tipo = "paziente" if flag_paziente else "diabetologo"
                username = Admin.genera_username(id_richiesta)
                persona = PersonaFactory.crea_persona(
                    tipo, nome, cognome, data_nascita, sesso, codice_fiscale,
                    indirizzo, citta, cap, telefono, email, username, password
                )

                if flag_paziente:
                    Admin.inserisci_paziente(persona)
                    Admin.associa_a_diabetologo(persona)
                else:
                    Admin.inserisci_diabetologo(persona)

                cursore.execute(
                    "UPDATE RichiesteAccount SET stato_richiesta = %s WHERE codice_fiscale = %s",
                    ('approvata', codice_fiscale)
                )

    
    def rifiuta_richiesta_cf(codice_fiscale):
        with DBSingleton.get_cursor() as cursore:

            cursore.execute("SELECT * FROM RichiesteAccount WHERE codice_fiscale = %s", (codice_fiscale,))
            richiesta = cursore.fetchone()

            if richiesta is None:
                raise ValueError(f"Nessuna richiesta trovata per il codice fiscale {codice_fiscale}.")

            cursore.execute(
                "UPDATE RichiesteAccount SET stato_richiesta = %s WHERE codice_fiscale = %s",
                ('rifiutata', codice_fiscale)
            )
        




    def rifiuta_richiesta(id_richiesta):
        """cambia lo stato della richiesta da << in_attesa >> a << rifiutata >>"""

        with DBSingleton.get_cursor() as cursore:
        
            cursore.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s", (id_richiesta,))
            richiesta = cursore.fetchone()
            
            if richiesta is None:
                cursore.close()
                raise ValueError(f"Richiesta con id {id_richiesta} non trovata.")

            cursore.execute(
                "UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s",
                ('rifiutata', id_richiesta)
            )

    # funzione che elimina un paziente nel database. Da problemi in quanto ci sono foreign key che vanno messe ON CASCADE
    def elimina_paziente(id_paziente):
        """elimina un paziente dal DB dato il suo id_paziente"""

        with DBSingleton.get_cursor() as cursore:
            cursore.execute("DELETE FROM Paziente WHERE id_paziente = %s", (id_paziente,))

    def get_pazienti_associati(self, id_diabetologo):
        """Helper method per ottenere i pazienti associati"""
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                SELECT nome, cognome, data_nascita, sesso, codice_fiscale, 
                       indirizzo, citta, cap, telefono, email, username, pw
                FROM Paziente
                WHERE diabetologo_associato = %s
            """, (id_diabetologo,))
            
            pazienti = []
            for row in cursore.fetchall():
                p = Paziente(*row)
                pazienti.append(p)
            return pazienti
        
    # funzione che elimina un diabetologo nel database. crea il subject che deve notificare gli observer 
    def elimina_diabetologo(self, id_diabetologo):
        """Versione semplificata che usa direttamente gli Observer"""
        
        # 1. Recupera info del diabetologo
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("SELECT nome, cognome FROM Diabetologo WHERE id_diabetologo = %s", (id_diabetologo,))
            result = cursore.fetchone()
            if not result:
                raise ValueError(f"Diabetologo con ID {id_diabetologo} non trovato")
            nome, cognome = result
            diabetologo_name = f"{nome} {cognome}"
            
            # Ottieni pazienti associati
            pazienti = self.get_pazienti_associati(id_diabetologo)
            
            # Crea e notifica gli Observer (uno per paziente) direttamente
            observers = [PazienteDiabetologoObserver(p) for p in pazienti]
            
            # PRIMA notifica gli observer (così possono accedere al diabetologo)
            for observer in observers:
                observer.on_diabetologo_deleted(id_diabetologo, diabetologo_name)
            
            # 5. POI elimina il diabetologo
            cursore.execute("DELETE FROM Diabetologo WHERE id_diabetologo = %s", (id_diabetologo,))

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
# class Terapia():
#     def __init__(self, farmaco_prescritto, dose, via_somministrazione, periodo_terapia):
#         self.farmaco_prescritto = farmaco_prescritto 
#         self.dose = dose 
#         self.via_somministrazione = via_somministrazione 
#         self.periodo_terapia = periodo_terapia

#     # Getter e Setter per farmaco_prescritto
#     @property
#     def farmaco_prescritto(self):
#         return self._farmaco_prescritto
    
#     @farmaco_prescritto.setter
#     def farmaco_prescritto(self, value):
#         self._farmaco_prescritto = value

#     # Getter e Setter per dose
#     @property
#     def dose(self):
#         return self._dose
    
#     @dose.setter
#     def dose(self, value):
#         self._dose = value

#     # Getter e Setter per via_somministrazione
#     @property
#     def via_somministrazione(self):
#         return self._via_somministrazione
    
#     @via_somministrazione.setter
#     def via_somministrazione(self, value):
#         self._via_somministrazione = value

#     # Getter e Setter per periodo_terapia
#     @property
#     def periodo_terapia(self):
#         return self._periodo_terapia
    
#     @periodo_terapia.setter
#     def periodo_terapia(self, value):
#         self._periodo_terapia = value
        




# class Farmaco():
#     def __init__(self, nome, tipologia, unita_misura, codice_univoco):
#         self.nome = nome
#         self.tipologia = tipologia
#         self.unita_misura = unita_misura
#         self.codice_univoco = codice_univoco

#     # Getter e Setter per nome
#     @property
#     def nome(self):
#         return self._nome
    
#     @nome.setter
#     def nome(self, value):
#         self._nome = value

#     # Getter e Setter per tipologia
#     @property
#     def tipologia(self):
#         return self._tipologia
    
#     @tipologia.setter
#     def tipologia(self, value):
#         self._tipologia = value

#     # Getter e Setter per unita_misura
#     @property
#     def unita_misura(self):
#         return self._unita_misura
    
#     @unita_misura.setter
#     def unita_misura(self, value):
#         self._unita_misura = value

#     # Getter e Setter per codice_univoco
#     @property
#     def codice_univoco(self):
#         return self._codice_univoco
    
#     @codice_univoco.setter
#     def codice_univoco(self, value):
#         self._codice_univoco = value

#     # fx che aggiunga un farmaco alla tabella farmaco nel db
#     def aggiungi_farmaco():
#         pass




    
# class Glicemia():
#     def __init__(self, valore, data_assunzione, ora_assunzione):
#         self.valore = valore
#         self.data_assunzione = data_assunzione
#         self.ora_assunzione = ora_assunzione

#     # Getter e setter del valore
#     @property
#     def valore(self):
#         return self._valore

#     @valore.setter
#     def valore(self, valore):
#         self._valore = valore

#     # Getter e setter della data di assunzione
#     @property
#     def data_assunzione(self):
#         return self._data_assunzione

#     @data_assunzione.setter
#     def data_assunzione(self, data_assunzione):
#         self._data_assunzione = data_assunzione

#     # Getter e setter dell'ora di assunzione
#     @property
#     def ora_assunzione(self):
#         return self._ora_assunzione

#     @ora_assunzione.setter
#     def ora_assunzione(self, ora_assunzione):
#         self._ora_assunzione = ora_assunzione
        


#da qua in poi metodi generali non appartenenti a classi specifiche
#*************************************************************************************************************************************
# METODI DI UTILITY:
#miglio - funzione che a seconda della classe di appartenenza dell'utente 
#chiama i metodi per restituire la sua lista di contatti 
def get_contatti():
    contacts = []  

    if isinstance(current_user, Diabetologo):
        contacts = current_user.get_all_pazienti_associati()  # Ottieni i pazienti
        
    elif isinstance(current_user, Paziente):
        contacts = current_user.get_diabetologo()  # Ottieni il diabetologo
    return contacts
#miglio- funzione che resituisce l'id di current_user

def get_user_id():
    if isinstance(current_user, Diabetologo):
        id = current_user.get_id_diabetologo()  
    elif isinstance(current_user, Paziente):
        id = current_user.get_id_paziente()
    else:
        id = current_user.get_id_admin()
    return id

#fil - funzione che date tutte le informazioni che il paziente inserisce nella richiesta account, 
#      procede ad inserirle effettivamente nella base di dati 
def inserisci_richiesta(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, password):
    
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""INSERT INTO RichiesteAccount 
                        (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, paziente, password) 
                        VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                        (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, generate_password_hash(password)))
        

# Funzione che prende un utente dato lo username, e restituisce un oggetto Persona.diabetologo o Persona.paziente
# n.b lo username deve essere univoco altrimenti disastro 
# esteso per aggiungere la query sulla tabella "amministratore"
def get_by_username(username_utente):
    '''se l'utente esiste ritorna un oggetto paziente/diabetologo/admin con i campi compilati, se non esiste, ritorna None '''
    
    with DBSingleton.get_cursor() as cursore:

        presente_in_paziente = False     # flag per controllare se l'utente è un paz/diab
        presente_in_diabetologo = False  # flag per controllare se l'utente è un diab
        presente_in_admin = False        # flag per controllare se l'utente è un admin

        query_ricerca = "SELECT nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw FROM paziente WHERE username= %s" # pw deve essere la hash
        cursore.execute(query_ricerca, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo
        record = cursore.fetchone()

        if record:      # se non c'è in paziente, cerchiamo se c'è in diabetologo. se non c'è --> controlliamo admin. se non c'è --> return None
            presente_in_paziente = True
        else:
            query_ricerca = "SELECT nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw FROM diabetologo WHERE username= %s" # pw deve essere la hash
            cursore.execute(query_ricerca, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo
            record = cursore.fetchone()

            if record:
                presente_in_diabetologo = True
            else:
                query_ricerca = "SELECT nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw FROM amministratore WHERE username= %s" # pw deve essere la hash
                cursore.execute(query_ricerca, (username_utente,))   # deve essere sotto forma di tupla sennò psycopg non capisce un cazzo
                record = cursore.fetchone()
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



# PER I PAZIENTI
# funzione che ritorna tutte le richieste di creazione account con stato "in_attesa"
def get_richieste_account_pazienti():
    
    with DBSingleton.get_cursor() as cursore:

        cursore.execute("SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s ORDER BY cognome", ("in_attesa", "TRUE",))
        result = cursore.fetchall()
    

    # formato per il dropdown: mostra nome, cognome, usa l'id come value. Prendo anche il codice fiscale per usarlo come identificatore.
        options = [
            {"label": f"{nome} {cognome} {codice_fiscale}", "value": id_richiesta}
            for id_richiesta, nome, cognome, codice_fiscale in result
        ]
    return options


# PER I DIABETOLOGI
# funzione che ritorna tutte le richieste di creazione account con stato "in_attesa"
def get_richieste_account_diabetologi():
    
    with DBSingleton.get_cursor() as cursore:

        cursore.execute("SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s ORDER BY cognome", ("in_attesa", "FALSE",))
        result = cursore.fetchall()
        
        # formato per il dropdown: mostra nome, cognome, usa l'id come value. Prendo anche il codice fiscale per usarlo come identificatore.
        options = [
            {"label": f"{nome} {cognome} {codice_fiscale}", "value": id_richiesta}
            for id_richiesta, nome, cognome, codice_fiscale in result
        ]
    return options




# funzione che prende un diab/paz e ne mostra i dati nella richiesta. 
# viene triggerata dalla callback del dropdown.
def get_dati_richiesta_account_by_id(id_richiesta):
    
    with DBSingleton.get_cursor() as cursore:

        cursore.execute("""
            SELECT nome, cognome, data_nascita, sesso, codice_fiscale,
                indirizzo, citta, cap, telefono, email, paziente, data_richiesta, stato_richiesta
            FROM richiesteaccount
            WHERE id_richiesta = %s
        """, (id_richiesta,))
        result = cursore.fetchone()

    if result:
        chiavi = ["nome", "cognome", "data_nascita", "sesso", "codice_fiscale",
                  "indirizzo", "citta", "cap", "telefono", "email", "paziente", "data_richiesta", "stato_richiesta"]
        return dict(zip(chiavi, result))
    return None


# funzione che prende i dettagli di un singolo paziente dato il suo id.
def get_dettagli_paziente(id_paziente):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""
            SELECT id_paziente, nome, cognome, data_nascita, sesso, codice_fiscale,
                indirizzo, citta, cap, telefono, email, username, diabetologo_associato
            FROM paziente
            WHERE id_paziente = %s
        """, (id_paziente,))
        result = cursore.fetchone()

    if result:
        chiavi = ["id_paziente", "nome", "cognome", "data_nascita", "sesso", "codice_fiscale", "indirizzo", "citta", "cap", "telefono", "email", "username", "diabetologo_associato"]
        return dict(zip(chiavi, result))
    return None


# funzione che prende tutti i pazienti nella db, e ne ritorna i dati in un dict
def get_all_pazienti():
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("SELECT id_paziente, nome, cognome, codice_fiscale, data_nascita, email, telefono FROM paziente ORDER BY cognome")
        result = cursore.fetchall()

        # Conversione in lista di dizionari
        pazienti = [
            {
                "id_paziente": r[0],
                "nome": r[1],
                "cognome": r[2],
                "codice_fiscale": r[3],
                "data_nascita": r[4],
                "email": r[5],
                "telefono": r[6]
            }
            for r in result
        ]

    return pazienti


# funzione che dato l'id di un diabetologo, ritorna tutti i suoi dati (tranne pw)
def get_dettagli_diabetologo(id_diabetologo):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""
            SELECT id_diabetologo, nome, cognome, data_nascita, sesso, codice_fiscale,
                indirizzo, citta, cap, telefono, email, username
            FROM diabetologo
            WHERE id_diabetologo = %s
        """, (id_diabetologo,))
        result = cursore.fetchone()

    if result:
        chiavi = [
            "id_diabetologo",
            "nome",
            "cognome",
            "data_nascita",
            "sesso",
            "codice_fiscale",
            "indirizzo",
            "citta",
            "cap",
            "telefono",
            "email",
            "username"
        ]
        return dict(zip(chiavi, result))
    return None


# funzione che prende tutti i diabetologi nella db e li restituisce sotto forma di dict.
def get_all_diabetologi():
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("SELECT id_diabetologo, nome, cognome, codice_fiscale, data_nascita, email, telefono FROM diabetologo ORDER BY cognome")
        result = cursore.fetchall()

        diabetologi = [
            {
                "id_diabetologo": r[0],
                "nome": r[1],
                "cognome": r[2],
                "codice_fiscale": r[3],
                "data_nascita": r[4],
                "email": r[5],
                "telefono": r[6]
            }
            for r in result
        ]

    return diabetologi

# ***********************
# funzione che ritorna il grafico delle media della glicemia dei pazienti di ogni diabetologo
def visualizza_media_glicemia_per_diabetologi():
    with DBSingleton.get_cursor() as cursore:
        diabetologi = get_all_diabetologi()
        nomi = []
        medie = []

        for d in diabetologi:
            id_d = d["id_diabetologo"]
            cursore.execute("SELECT * FROM Diabetologo WHERE id_diabetologo=%s",(id_d,))
            r=cursore.fetchone()
            Diab=Diabetologo(r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12])
            dati_pazienti = Diab.visualizza_n_c_pazienti_associati()

            nome_completo = f"{d['nome']} {d['cognome']}"
            nomi.append(nome_completo)

            if not dati_pazienti:
                medie.append(0)  # oppure None, se si vuole lasciare vuota la colonna
                continue

            media_diabetologo = sum([r["media"] for r in dati_pazienti]) / len(dati_pazienti)
            medie.append(round(media_diabetologo, 2))

        if not nomi:
            fig = go.Figure()
            fig.add_annotation(
                text="Nessun dato disponibile",
                xref="paper", yref="paper",
                showarrow=False,
                font=dict(size=18, color="red")
            )
            return fig
        
        fig = go.Figure(data=[
            go.Bar(
                x=nomi,
                y=medie,
                marker=dict(
                    color=medie,
                    colorscale='Blues',  # scala di colore che associa a valori più alti tonalità più scure
                    line=dict(color='darkblue', width=1)  # bordo delle barre
                ),
                hovertemplate='%{x}<br>Glicemia media: %{y} mg/dL<extra></extra>'
            )
        ])

        fig.update_layout(
            title=dict(
                text="Media glicemia per diabetologo",
                x=0.5,
                xanchor='center',
                font=dict(size=20, color='darkblue')
            ),
            xaxis_title="Diabetologo",
            yaxis_title="Glicemia (mg/dL)",
            xaxis=dict(
                tickangle=-45,
                tickfont=dict(size=15)
            ),
            yaxis=dict(
                tickfont=dict(size=15)
            ),
            plot_bgcolor='rgba(245, 245, 245, 1)',
            paper_bgcolor='white',
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0
            ),
            margin=dict(l=40, r=40, t=60, b=20)
        )

        return fig

    # ***********************

# funzione che permette di prendere il grafico dei pazienti associati diun solo diabetologo
def visualizza_media_glicemia_pazienti_diabetologo(id_diabetologo):
    """Ritorna un grafico a istogramma contenente la media glicemica dei pazienti associati ad un diabetologo."""
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("SELECT * FROM Diabetologo WHERE id_diabetologo = %s", (id_diabetologo,))
        r = cursore.fetchone()

    if not r:
        fig = go.Figure()
        fig.update_layout(title="Diabetologo non trovato")
        return fig

    # istanzia un oggetto diabetologo, con tutti gli attributi suoi
    Diab = Diabetologo(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12])
    dati_pazienti = Diab.visualizza_n_c_pazienti_associati()   

    if not dati_pazienti:
        fig = go.Figure()
        fig.update_layout(title="Nessun dato glicemico disponibile")
        return fig

    # usa una lista di dizionari
    nomi_pazienti = [f"{p['nome']} {p['cognome']}" for p in dati_pazienti]
    medie_glicemia = [round(p["media"], 2) for p in dati_pazienti]

    fig = go.Figure(data=[
        go.Bar(x=nomi_pazienti, y=medie_glicemia, marker_color="teal")
    ])
    fig.update_layout(
        xaxis_title="Pazienti",
        yaxis_title="Glicemia (mg/dL)",
        margin=dict(l=10, r=10, t=30, b=40),
    )
    return fig


def visualizza_pazienti_associati_singolo_diab(id_diabetologo):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""
            SELECT p.nome, p.cognome, p.username
            FROM paziente p
            WHERE p.diabetologo_associato = %s
            ORDER BY p.cognome, p.nome
        """, (id_diabetologo,))
        
        risultati = cursore.fetchall()
        pazienti = [
            {
                "nome": r[0],
                "cognome": r[1],
                "username": r[2]
            } for r in risultati
        ]
    return pazienti


def get_id_paziente_by_username(username):
    with DBSingleton.get_cursor() as cursore:
        query = "SELECT id_paziente FROM paziente WHERE username = %s"
        cursore.execute(query, (username,))
        result = cursore.fetchone()
    if result:
        return result[0]  # l'ID del paziente
    return None

#**********************************************************************************************************************************

#funzione per filtrare il periodo del grafico, 
#filtro_temporale è fatto in modo da combaciare con i value del radio items
def get_dati_glicemia_filtrati(id_paziente, filtro_temporale, filtro_grafico):
    with DBSingleton.get_cursor() as cursore:
        if filtro_grafico == "andamento":
            query_base = """
                SELECT valore, data_inserimento, sintomi
                FROM Glicemia
                WHERE paziente = %s
            """
        else:
            query_base = """
                SELECT 
                    FLOOR(EXTRACT(HOUR FROM data_inserimento) / 3) * 3 AS ora_inizio_fascia,
                    AVG(valore) AS media_glicemia
                FROM Glicemia
                WHERE paziente = %s
            """
        parametri = [id_paziente]

        if filtro_temporale == "giornaliero":
            query_base += " AND data_inserimento >= NOW()::date"
        elif filtro_temporale == "settimanale":
            query_base += " AND data_inserimento >= NOW() - INTERVAL '7 days'"
        elif filtro_temporale == "mensile":
            query_base += " AND data_inserimento >= NOW() - INTERVAL '1 month'"
        elif filtro_temporale == "annuale":
            query_base += " AND data_inserimento >= NOW() - INTERVAL '1 year'"
        # se "tutto", nessun filtro aggiunto

        query_base += " ORDER BY data_inserimento" if filtro_grafico=="andamento" else " GROUP BY ora_inizio_fascia ORDER BY ora_inizio_fascia"

        cursore.execute(query_base, parametri)
        dati = cursore.fetchall()
    return dati

#*************************************************************************************************************************
#serve per inserire i sintomi indicati dal paziente direttamente nel marker del grafico
def formatta_sintomo(s):
    return f"Sintomi: {s}" if s else ""

#grafico linea per l'andamento
def visualizza_andamento_glicemia(dati):

        if not dati:
            # Eccezione per assenza di dati
            raise ValueError("Nessun dato glicemico disponibile.")

        valori = [r[0] for r in dati]
        date = [r[1] for r in dati]
        sintomi= [r[2] for r in dati]

        sintomi_formattati = [formatta_sintomo(s) for s in sintomi]

        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=date,
            y=valori,
            mode='lines+markers',
            fill='tozeroy',
            fillcolor='rgba(0, 123, 255, 0.2)',
            line=dict(color='blue', width=3),
            marker=dict(size=6),
            name='Glicemia',
            customdata=[[s] for s in sintomi_formattati],
            hovertemplate='Valore: %{y} mg/dL<br>Data: %{x}<br>%{customdata[0]}<extra></extra>'
        ))

        # Linee soglia glicemica
        for soglia in [80, 130]:
            fig.add_trace(go.Scatter(   
                x=date,
                y=[soglia]*len(date),
                mode='lines',
                line=dict(color="#71BAFF", dash='dash'),
                name=f'Soglia {soglia} mg/dL',
                hoverinfo='skip'
            ))

        fig.update_layout(
            xaxis_title='Data rilevazione',
            yaxis_title='Glicemia (mg/dL)',
            yaxis=dict(range=[min(50, min(valori)-10), max(valori) + 50]),
            plot_bgcolor="#e6f2ff",
            hovermode='x unified',
            font=dict(family='Arial', size=14),
            # altezza forzata a 40px
            height=400,
            # margini forzati a top/bottom/left/right = 10px
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(
                x=0.01, # posizione orizzontale
                y=0.99, # posizione verticale
                xanchor='left', # a sinistra
                yanchor='top', # in alto
                bgcolor='rgba(255,255,255,0.3)', # sfondo semi trasparente di colore bianco
                borderwidth=0 # senza bordo
            )
        )

        return fig

#****************************************************************************************************************

def get_terapie_paziente(id_diab, id_paz):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("SELECT * FROM Terapia t WHERE paziente=%s AND diabetologo=%s",(id_paz,id_diab))
        result=cursore.fetchall()
    return result

#grafico a barre che rappresenta le medie
def visualizza_media_glicemica_fasce_orarie(dati):
    # Eccezione per dati nulli
    if not dati:
        raise ValueError("Nessun dato glicemico inserito.")

    fasce_orarie = list(range(0, 24, 3))  # 8 fasce
    media_dict = {ora: round(valore,2) for ora, valore in dati}

    ore = fasce_orarie
    valori = [media_dict.get(ora) for ora in ore]

    # Etichette tipo "00:00–03:00", "03:00–06:00", ecc.
    labels = [f"{str(h).zfill(2)}:00–{str((h + 3) % 24).zfill(2)}:00" for h in ore]

    # Colori condizionati dai valori
    colori = []
    for v in valori:
        if v is None:
            colori.append("#f8f9fa")
        elif v < 80:
            colori.append("#FF4C4C")
        # Normoglicemia
        elif 80 <= v <= 130:
            colori.append('#08ff46')
        # Glicemia alta (merita attenzione)
        elif 131 <= v <= 180:
            colori.append('#FFD93B')
        # Iperglicemia
        else:
            colori.append("#FF4C4C")

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=labels,
        y=valori,
        marker_color=colori,
        text=valori,
        textposition='outside'
    ))
    y_max = max([v for v in valori if v is not None], default=0)
    fig.update_layout(
        xaxis_title="Fascia oraria",
        yaxis_title="Glicemia media (mg/dL)",
        yaxis=dict(range=[0, y_max + 30]),
        height=400,
        margin=dict(t=10, b=10, l=10, r=10),
        legend=dict(
                x=0.01, # posizione orizzontale
                y=0.99, # posizione verticale
                xanchor='left', # a sinistra
                yanchor='top', # in alto
                bgcolor='rgba(255,255,255,0.3)', # sfondo semi trasparente di colore bianco
                borderwidth=0 # senza bordo
        )
    )

    return fig
#a partire da un paziente ritorna tutti gli eventi di glicemia minore di 60, con il relativo valore
def get_eventi_basso_glucosio(id_paz):
        with DBSingleton.get_cursor() as cursore:
        
            query_base="""SELECT valore, data_inserimento
                        FROM Glicemia 
                        WHERE paziente = %s AND valore < 60"""
            parametri = [id_paz]
            
            #query_base += " AND data_inserimento >= NOW() - INTERVAL '1 year'"
            # se "tutto", nessun filtro aggiunto

            query_base += " ORDER BY data_inserimento"
            cursore.execute(query_base,parametri)
            dati=cursore.fetchall()

        return dati

def crea_calendario_ipoglicemia_con_pallini(dati, anno, mese, soglia=60):
    
    # Creo DataFrame con colonne corrette
    df = pd.DataFrame(dati, columns=["valore", "data_inserimento"])
    df["data_inserimento"] = pd.to_datetime(df["data_inserimento"])
    df["giorno"] = df["data_inserimento"].dt.day
    df["mese"] = df["data_inserimento"].dt.month
    df["anno"] = df["data_inserimento"].dt.year

    # Seleziono solo eventi sotto soglia e nel mese/anno richiesti
    eventi = df[(df["valore"] < soglia) & (df["mese"] == mese) & (df["anno"] == anno)]

    giorni_evento = eventi["giorno"].tolist()
    valori_evento = eventi["valore"].tolist()

    cal = calendar.Calendar(firstweekday=0)
    settimane = list(cal.monthdayscalendar(anno, mese))

    fig = go.Figure()

    giorni_settimana = ["Lun", "Mar", "Mer", "Gio", "Ven", "Sab", "Dom"]
    # Etichette giorni
    for i, giorno in enumerate(giorni_settimana):
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            text=[giorno],
            mode="text",
            showlegend=False,
            textfont=dict(size=14, color="black")
        ))

    # Pallini e numeri giorni
    for settimana_idx, settimana in enumerate(settimane):
        for giorno_idx, giorno in enumerate(settimana):
            if giorno == 0:
                continue
            x = giorno_idx
            y = -settimana_idx - 1

            if giorno in giorni_evento:
                # Prendo il valore glicemico per quel giorno
                idx = giorni_evento.index(giorno)
                valore = valori_evento[idx]
                hover_text = f"Glucosio: {valore} mg/dL"
                mode = "markers+text"
                marker_color = "rgba(255,0,0,0.65)"
                marker_size = 30
            else:
                hover_text = f"Giorno {giorno}"
                mode = "text"
                marker_color = "rgba(0,0,0,0)"
                marker_size = 0

            fig.add_trace(go.Scatter(
                x=[x], y=[y],
                text=[str(giorno)],
                mode=mode,
                marker=dict(
                    color=marker_color,
                    size=marker_size
                ),
                hoverinfo="text",
                hovertext=hover_text,
                textfont=dict(size=14),
                showlegend=False
            ))

    fig.update_layout(
        xaxis=dict(range=[-0.5, 6.5], showgrid=False, showticklabels=False),
        yaxis=dict(visible=False),
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="white"
    )

    return fig


# METODO DI RECUPERO INFORMAZIONI DI BASE DI UN PAZIENTE
# Se la query fallisce lancia un'eccezione
def get_info_base_paziente(id_diab, id_paz):
    try:
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""
                SELECT 
                    username, 
                    nome, 
                    cognome, 
                    data_nascita, 
                    sesso, 
                    COALESCE(AVG(g.valore), 0) AS media
                FROM paziente p
                LEFT JOIN Glicemia g ON p.id_paziente = g.paziente
                WHERE p.diabetologo_associato = %s AND p.id_paziente = %s
                GROUP BY p.id_paziente
            """, (id_diab, id_paz))
            
            result = cursore.fetchone()
        return result  # Restituisce solo una riga, come ha più senso in questo contesto
    except Exception as e:
        print(f"Errore in get_info_base_paziente: {e}")
        raise

#*************************************************************************************************************************

def get_info_base_diabetologo(id_diab):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""SELECT d.username, d.nome, d.cognome, d.data_nascita, d.sesso, COUNT(*)
                                FROM Diabetologo d
                                JOIN Paziente p ON d.id_diabetologo=p.diabetologo_associato
                                WHERE id_diabetologo=%s
                                GROUP BY d.username,d.nome,d.cognome,d.data_nascita,d.sesso
                                """,(id_diab,))
        result = cursore.fetchall()
    return result

#*************************************************************************************************************************
# Restituisce la tupla (contenuto, orario, giorno, is_mittente, is_diabetologo) per i messaggi
def get_messaggi(id_paziente): #current_user.get_id() e id_button

    Messaggio = namedtuple('Messaggio', ['contenuto', 'orario', 'giorno','is_mittente',"is_paziente"])
    with DBSingleton.get_cursor() as cursore:
    #query che restituisce i dati del messaggio capendo chi è il diabetologo e chi il paziente
        cursore.execute("""
            Select contenuto, orario, is_mittente
            from messaggio
            where id_paziente = %s
            order by orario
        """,(id_paziente,))

        result = cursore.fetchall()
        if not result: return
    return  [
        Messaggio(
            contenuto = r[0],
            orario = r[1].time(),
            giorno = r[1].date(),
            is_mittente = r[2],
            is_paziente = isinstance(current_user,Paziente)
        )
        for r in result
    ]
#*************************************************************************************************************************
#funzione che inserisci i messaggi nella base di dati. 
def insert_messaggio(id_paziente, contenuto, is_mittente):
        with DBSingleton.get_cursor() as cursore:
            cursore.execute("""Insert into messaggio values (%s,current_timestamp,%s,%s)""",(id_paziente,is_mittente,contenuto))
        return

#*************************************************************************************************************************
# Restituisce la tupla (nome, cognome) per il contatto della chat
def get_nomecognome(id):
    nomecognome = namedtuple('nomecognome',['nome','cognome'])
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""
            SELECT nome, cognome
            FROM diabetologo 
            WHERE id_diabetologo = %s

            UNION ALL

            SELECT nome, cognome
            FROM paziente 
            WHERE id_paziente = %s
        """,(id,id))
        result = cursore.fetchone()
    if not result : return
    return nomecognome(nome = result[0], cognome = result[1])
    

# funzione che permette la modifica dei dati del paziente nella db
def modifica_dati_paziente_db(id_paziente, indirizzo=None, citta=None, cap=None, email=None, telefono=None):
 
    updates = []
    params = []

    # Costruzione dinamica della query
    if indirizzo is not None:
        updates.append("indirizzo = %s")
        params.append(indirizzo)
    if citta is not None:
        updates.append("citta = %s")
        params.append(citta)
    if cap is not None:
        updates.append("cap = %s")
        params.append(cap)
    if email is not None:
        updates.append("email = %s")
        params.append(email)
    if telefono is not None:
        updates.append("telefono = %s")
        params.append(telefono)

    if not updates:
        raise ValueError("Nessun dato da aggiornare")

    # ID paziente come ultimo parametro per il WHERE
    params.append(id_paziente)

    query = f"""
    UPDATE paziente
    SET {', '.join(updates)}
    WHERE id_paziente = %s
    """

    with DBSingleton.get_cursor() as cursore:
        cursore.execute(query, params)

    return True




# funzione che permette la modifica dei dati del diabetologo nella db
def modifica_dati_diabetologo_db(id_diabetologo, email=None, telefono=None,
                                 indirizzo=None, citta=None, cap=None):

    updates = []
    params = []

    if email:
        updates.append("email = %s")
        params.append(email)
    if telefono:
        updates.append("telefono = %s")
        params.append(telefono)
    if indirizzo:
        updates.append("indirizzo = %s")
        params.append(indirizzo)
    if citta:
        updates.append("citta = %s")
        params.append(citta)
    if cap:
        updates.append("cap = %s")
        params.append(cap)

    if not updates:
        raise ValueError("Nessun dato da aggiornare")

    params.append(id_diabetologo)

    query = f"""
    UPDATE diabetologo
    SET {', '.join(updates)}
    WHERE id_diabetologo = %s
    """

    with DBSingleton.get_cursor() as cursor:
        cursor.execute(query, params)
    return True


def is_number(s):
    try:
        float(s)
        return True
    except (TypeError, ValueError):
        return False
    
# Dato un id del diabetologo estrae il numero di pazienti associati
def get_numero_pazienti_associati_by_id(id_diabetologo):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""
            SELECT COUNT(*) 
            FROM Paziente 
            WHERE diabetologo_associato = %s
        """, (id_diabetologo,))
        numero = cursore.fetchone()[0]

    return numero


def check_glicemia(id_paziente,valore,pasto):
    with DBSingleton.get_cursor() as cursore:

    #supponendo flag == True prima dei pasti
        if (80 > valore < 130 and pasto == "pre"):
            cursore.execute(
                """Insert into alerts values(%s,current_timestamp,%s)""",(
                id_paziente,
                f"Glicemia pre-pasto {valore} fuori range  [80 - 130]")
                )

        elif (valore > 180 and not pasto == "post"):
            cursore.execute(
            """Insert into alerts values(%s,current_timestamp,%s)""",(
                id_paziente,
                f"Glicemia post-pasto {valore} fuori range  [80 - 180]")
            )
    return
#************************************************************
#metodo che verifica che il farmaco e il dosaggio siano coerenti con le terapie attive
def check_farmaco(id_paziente,farmaco, dose):
    id_diabetologo = get_diabetologo_associato(id_paziente)
    with DBSingleton.get_cursor() as cursore:
    #query che restituisce le assunzioni di farmaci non coincidenti
        cursore.execute("""
            WITH terapie AS(
                SELECT * FROM Terapia t WHERE paziente=%s AND diabetologo=%s
            )
            SELECT 
                NOT EXISTS (SELECT 1 FROM terapie WHERE farmaco = %s) AS farmaco_mancante,
                NOT EXISTS (SELECT 1 FROM terapie WHERE farmaco = %s AND dosaggio = %s) AS dose_errata
        """,
        (id_paziente, id_diabetologo, farmaco, farmaco, dose))

        farmaco_mancante, dose_errata = cursore.fetchone()

        if farmaco_mancante:
            cursore.execute(
                """Insert into alerts values(%s,current_timestamp,%s)""",(
                id_paziente,
                f"Il paziente ha assunto un farmaco non previsto dalle terapie correnti: {farmaco}")
            )
        if dose_errata and not farmaco_mancante:
            cursore.execute(
                """Insert into alerts values(%s,current_timestamp,%s)""",(
                id_paziente,
                f"Il paziente ha assunto un dosaggio non previsto dalle terapie correnti: {dose}")
            )
    return

def get_alerts_paziente(id_paziente):
    with DBSingleton.get_cursor() as cursore:
        Alerts = namedtuple("Alerts", ["orario", "contenuto"])
        cursore.execute("""
            SELECT orario, alert_case
            FROM alerts 
            where id_paziente = %s
            order by orario desc
        """,(id_paziente,))
        result = cursore.fetchmany(5)
        if not result: return
        return [
            Alerts(
                orario = r[0].time().strftime("%H:%M"),
                contenuto = r[1]
            )
            for r in result
        ]
    
def get_diabetologo_associato(id_paziente):
    with DBSingleton.get_cursor() as cursore:
        cursore.execute("""Select p.diabetologo_associato from paziente p where p.id_paziente = %s""",(id_paziente,))
        return cursore.fetchone()
    