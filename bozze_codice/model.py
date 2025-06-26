# gestione Database remoto, gestione altra roba logica
import datetime
import dash_bootstrap_components as dbc
from abc import ABC,abstractmethod
from werkzeug.security import generate_password_hash #password criptate

import psycopg2
from flask_login import UserMixin, login_user, logout_user, current_user 
import dash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


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
    
    def get_id_paziente(self):
        
        cursore = connection.cursor()
        
        cursore.execute("""SELECT id_paziente
                    FROM Paziente 
                    WHERE codice_fiscale = %s""", (self.cf,))
        id=cursore.fetchone()[0]
        cursore.close()
        return id
    
    def inserisci_glicemia(id_paz, valore, farmaco, dose, sintomi="" ):
        cursore_8=connection.cursor()
        cursore_8.execute("""INSERT INTO Glicemia 
                    (paziente, farmaco, dosaggio, sintomo, valore) 
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (id_paz, farmaco, dose, sintomi, valore))
        connection.commit()
        cursore_8.close()

    def inserisci_segnalazione(self, tipo_segnalazione, descrizione, data_inizio, data_fine=None):
        if tipo_segnalazione not in ('sintomo', 'patologia', 'terapia'):
            raise ValueError("Tipo segnalazione non valido. Deve essere 'sintomo', 'patologia' o 'terapia'.")

        cursore = connection.cursor()
        query = """
            INSERT INTO SegnalazioniPaziente (paziente, tipo_segnalazione, descrizione, data_inizio, data_fine)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursore.execute(query, (self.get_id_paziente(), tipo_segnalazione, descrizione, data_inizio, data_fine))
        connection.commit()
        cursore.close()


    






class Diabetologo(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

    def get_id_diabetologo(self):
        
        cursore_9 = connection.cursor()
        
        cursore_9.execute("""SELECT id_diabetologo
                    FROM Diabetologo 
                    WHERE codice_fiscale = %s""", (self.cf,))
        id=cursore_9.fetchone()[0]
        cursore_9.close()
        
        return id
    
    def inserisci_terapia(self,id_paz, farmaco, dose, assunzioni_gg, data_inizio, data_fine, indicazioni=None):
        cursore_10 = connection.cursor()
        cursore_10.execute("""INSERT INTO Terapia 
                    (paziente, diabetologo, farmaco, dosaggio, assunzioni_gg, data_inizio, data_fine,indicazioni) 
                    VALUES (%s, %s, %s, %s, %s, %s, %s,%s)""", 
                    (id_paz, self.get_id_diabetologo(), farmaco, dose, assunzioni_gg, data_inizio, data_fine,indicazioni))
        connection.commit()
        cursore_10.close()
    
    def get_terapie_paziente(self, id_paz):
        cursore=connection.cursor()
        cursore.execute("SELECT * FROM Terapia t WHERE paziente=%s AND diabetologo=%s",(id_paz,current_user.get_id_diabetologo()))
        result=cursore.fetchall()
        return result
    
    def modifica_terapia_paziente(self, id_paz, farmaco, dose, assunzioni_gg, data_inizio, data_fine, indicazioni=None):
        cursore=connection.cursor()
        cursore.execute("""UPDATE Terapia 
                            SET farmaco=%s, dosaggio=%s, assunzioni_gg=%s, data_inizio=%s, data_fine=%s, indicazioni=%s,data_ultima_modifica = CURRENT_DATE
                            WHERE paziente=%s and diabetologo=%s""", 
                            (farmaco, dose, assunzioni_gg, data_inizio, data_fine, indicazioni, id_paz, self.get_id_diabetologo()))
        connection.commit()
        cursore.close()


    def visualizza_pazienti_associati(self):
        #li ordina in base al valore medio di glicemia
        cursore_11 = connection.cursor()
        
        cursore_11.execute("""SELECT p.username, COALESCE(AVG(g.valore), 0) as media
                    FROM Paziente p
                    LEFT JOIN Glicemia g ON p.id_paziente=g.paziente
                    WHERE p.diabetologo_associato = %s
                    GROUP BY p.id_paziente
                    ORDER BY media DESC""",
                    (self.get_id_diabetologo(),))
        result=cursore_11.fetchall()
        cursore_11.close()
        return result
    
    def visualizza_n_c_pazienti_associati(self):
        cursore_12 = connection.cursor()
        cursore_12.execute("""
            SELECT p.id_paziente, p.nome, p.cognome, COALESCE(AVG(g.valore), 0) AS media
            FROM paziente p
            LEFT JOIN Glicemia g ON p.id_paziente = g.paziente
            WHERE p.diabetologo_associato = %s
            GROUP BY p.id_paziente
            ORDER BY media DESC
        """, (self.get_id_diabetologo(),))
        
        result = cursore_12.fetchall()

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
        cursore_12.close()
        return pazienti

    
    def get_numero_pazienti_associati(self):
        cursore=connection.cursor()
        cursore.execute("""
            SELECT COUNT(*) 
            FROM Paziente p 
            WHERE p.diabetologo_associato = %s
        """, (self.get_id_diabetologo(),))
        numero = cursore.fetchone()[0]
        cursore.close()
        return numero

    def get_info_base_paziente_associato(self,id_paz):
        cursore = connection.cursor()
        cursore.execute("""SELECT username, nome, cognome,data_nascita,sesso, COALESCE(AVG(g.valore), 0) AS media
                            FROM paziente p
                            LEFT JOIN Glicemia g on p.id_paziente=g.paziente
                            WHERE p.diabetologo_associato = %s and p.id_paziente=%s
                            GROUP BY p.id_paziente
                            """,(self.get_id_diabetologo(),id_paz))
        result = cursore.fetchall()
        cursore.close()
        return result
    
    def visualizza_glicemia_paziente(id_paziente):
        cursore = connection.cursor()
        cursore.execute("""
            SELECT valore, data_inserimento 
            FROM Glicemia 
            WHERE paziente = %s
            ORDER BY data_inserimento
        """, (id_paziente,))
        dati = cursore.fetchall()
        cursore.close()

        if not dati:
            return go.Figure().update_layout(title="Nessun dato glicemico disponibile")

        valori = [r[0] for r in dati]
        date = [r[1] for r in dati]

        fig = go.Figure()

        # Area azzurra sotto
        fig.add_trace(go.Scatter(
            x=date,
            y=valori,
            mode='lines',
            line=dict(width=0),
            showlegend=False
        ))

        fig.add_trace(go.Scatter(
            x=date,
            y=valori,
            mode='lines+markers',
            fill='tonexty',
            fillcolor='rgba(0, 123, 255, 0.2)',
            line=dict(color='blue', width=3),
            name='Glicemia'
        ))

        # Linee soglia glicemica
        for soglia in [70, 130]:
            fig.add_trace(go.Scatter(
                x=date,
                y=[soglia]*len(date),
                mode='lines',
                line=dict(color="#71BAFF", dash='dash'),
                name=f'Soglia {soglia} mg/dL',
            ))

        fig.update_layout(
            xaxis_title='Data rilevazione',
            yaxis_title='Glicemia (mg/dL)',
            yaxis=dict(range=[0, max(valori) + 50]),
            plot_bgcolor="#e6f2ff",
            hovermode='x unified',
            font=dict(family='Arial', size=14),
            height=500
        )

        return fig



    # Funzione che permetta al medico di inserire i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def inserisci_info_paziente(self,id_paz, patologie=None, fattori=None, comorbidita=None):
        cursore_14=connection.cursor()
        associati=current_user.visualizza_pazienti_associati()
        paz=[]
        for a in associati:
            paz.append(a[0])
        cursore_14.execute("SELECT username FROM Paziente WHERE id_paziente=%s",(id_paz,))
        username_paz=cursore_14.fetchone()[0]
        if username_paz in paz:
            cursore_14.execute("""INSERT INTO InfoPaziente 
                    (paziente, diabetologo, patologie_pregresse, fattori_rischio, comorbidita) 
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (id_paz, self.get_id_diabetologo(), patologie, fattori, comorbidita))
            connection.commit()

    # Funzione che permetta al medico di modificare i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def modifica_info_paziente(self,id_paz, patologie=None, fattori=None, comorbidita=None):
        cursore_15=connection.cursor()
        associati=current_user.visualizza_pazienti_associati()
        paz=[]
        for a in associati:
            paz.append(a[0])
        cursore_15.execute("SELECT username FROM Paziente WHERE id_paziente=%s",(id_paz,))
        username_paz=cursore_15.fetchone()[0]
        if username_paz in paz:
            cursore_15.execute("""UPDATE InfoPaziente 
                                SET fattori_rischio=%s, patologie_pregresse=%s, comorbidita=%s, data_ultima_modifica = CURRENT_DATE
                                WHERE paziente=%s and diabetologo=%s""", 

                    (fattori, patologie, comorbidita, id_paz, self.get_id_diabetologo()))
            connection.commit()

    # Funzione che permetta al medico di visualizzare i dati rilevanti del paziente,
    # insieme alle informazioni cliniche. 
    # Saranno da interrogare quindi sia "paziente" che "info_paziente"
    def visualizza_dati_paziente(self,id_paz):
        cursore_15=connection.cursor()
        associati=current_user.visualizza_pazienti_associati()
        paz=[]
        for a in associati:
            paz.append(a[0])
        cursore_15.execute("SELECT username FROM Paziente WHERE id_paziente=%s",(id_paz,))
        username_paz=cursore_15.fetchone()[0]
        if username_paz in paz:
            cursore_15.execute("""SELECT codice_fiscale, EXTRACT(year FROM CURRENT_DATE)-EXTRACT(year FROM data_nascita)
                        FROM Paziente
                        WHERE id_paziente=%s
                        """,(id_paz,))
            cfanno=cursore_15.fetchall()
            cursore_15.execute("""SELECT i.patologie_pregresse, i.fattori_rischio, i.comorbidita
                                FROM infopaziente i
                                WHERE i.paziente=%s
                               """,(id_paz, ))
            info=cursore_15.fetchall()
        cursore_15.close()
        return cfanno,info 

    def get_segnalazioni_paziente(self,id_paziente):
        cursore = connection.cursor()
        cursore.execute("""
            SELECT sp.tipo_segnalazione, sp.descrizione, sp.data_inizio, sp.data_fine
            FROM SegnalazioniPaziente sp
            JOIN Paziente p on sp.paziente=p.id_paziente
            WHERE sp.paziente = %s AND p.diabetologo_associato=%s
            ORDER BY sp.data_inizio DESC
        """, (id_paziente,self.get_id_diabetologo()))
        risultati = cursore.fetchall()
        cursore.close()
        return risultati
                              




    
class Admin(Persona):
    def __init__(self,nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw):
        super().__init__(nome,cognome,data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email,username, pw)

    def genera_username(id_richiesta):
        
        cursore_14 = connection.cursor()
        
        cursore_14.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ",(id_richiesta,))
        richiesta = cursore_14.fetchone()
        nome=richiesta[1]
        cognome=richiesta[2]
        paziente=richiesta[11]

        if paziente:
            cursore_14.execute("SELECT * FROM Paziente WHERE nome = %s AND cognome = %s",(nome,cognome))
            righe = cursore_14.fetchall()
            num=len(righe)
            username=f"{nome}.{cognome}{num}_P"
        else:
            cursore_14.execute("SELECT * FROM Diabetologo WHERE nome = %s AND  cognome = %s",(nome,cognome))
            righe = cursore_14.fetchall()
            num=len(righe)
            username=f"{nome}.{cognome}{num}_D"

        cursore_14.close()
        return username

    def inserisci_paziente(p: Paziente):
        
        cursore_15 = connection.cursor()

        cursore_15.execute("""INSERT INTO Paziente 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (p.nome, p.cognome, p.data_nascita, p.sesso, p.cf, p.indirizzo, p.citta, p.cap, p.tel, p.email, p.username, p.pw))
        connection.commit()
        cursore_15.close()

    def inserisci_diabetologo(d: Diabetologo):
        
        cursore_16 = connection.cursor()
        
        cursore_16.execute("""INSERT INTO Diabetologo 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, pw) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (d.nome, d.cognome, d.data_nascita, d.sesso, d.cf, d.indirizzo, d.citta, d.cap, d.tel, d.email, d.username, d.pw))
        connection.commit()
        cursore_16.close()

    # Fx che associ il paziente al diabetologo. (modifica quindi diabetologo.paziente_associato)
    # potremmo permettere al paziente di selezionare quale sarà il suo
    # medico di riferimento.
    def associa_a_diabetologo(paziente):
        cursore_17 = connection.cursor()
        cursore_17.execute(""" SELECT d.id_diabetologo
                            FROM diabetologo d
                            LEFT JOIN paziente p ON d.id_diabetologo = p.diabetologo_associato
                            GROUP BY d.id_diabetologo
                            ORDER BY COUNT(p.id_paziente) ASC
                            LIMIT 1;
                        """)
        id_diabetologo=cursore_17.fetchone()[0]
        cursore_17.execute("UPDATE Paziente SET diabetologo_associato=%s WHERE codice_fiscale = %s ",(id_diabetologo,paziente.cf))
        connection.commit()
        cursore_17.close()
    
    def approva_richiesta(id_richiesta):
        
        cursore_4 = connection.cursor()

        cursore_4.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s ", (id_richiesta,))
        richiesta = cursore_4.fetchone()
        _,nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, flag_paziente, _,_, password=richiesta
        

        tipo = "paziente" if flag_paziente else "diabetologo"
        username=Admin.genera_username(id_richiesta)
        persona = PersonaFactory.crea_persona(tipo, nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, username, password)

        if flag_paziente:
            Admin.inserisci_paziente(persona)
            Admin.associa_a_diabetologo(persona)
        else:
            Admin.inserisci_diabetologo(persona)

        cursore_4.execute("UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s ",('approvata',id_richiesta))
        connection.commit()
        
        cursore_4.close()

    def rifiuta_richiesta(id_richiesta):
        """cambia lo stato della richiesta da << in_attesa >> a << rifiutata >>"""

        cursore = connection.cursor()
        
        cursore.execute("SELECT * FROM RichiesteAccount WHERE id_richiesta = %s", (id_richiesta,))
        richiesta = cursore.fetchone()
        
        if richiesta is None:
            cursore.close()
            raise ValueError(f"Richiesta con id {id_richiesta} non trovata.")

        cursore.execute(
            "UPDATE RichiesteAccount SET stato_richiesta=%s WHERE id_richiesta = %s",
            ('rifiutata', id_richiesta)
        )
        connection.commit()
        
        cursore.close()

    # funzione che elimina un paziente nel database. Da problemi in quanto ci sono foreign key che vanno messe ON CASCADE
    def elimina_paziente(id_paziente):
        """elimina un paziente dal DB dato il suo id_paziente"""

        cursore = connection.cursor()
        cursore.execute("DELETE FROM Paziente WHERE id_paziente = %s", (id_paziente,))
        connection.commit()

        cursore.close()

    # funzione che elimina un diabetologo nel database. Da problemi in quanto ci sono foreign key che vanno messe ON CASCADE
    def elimina_diabetologo(id_diabetologo):
        """elimina un diabetologo dal DB dato il suo id_diabetologo"""

        cursore = connection.cursor()
        cursore.execute("DELETE FROM Diabetologo WHERE id_diabetologo = %s", (id_diabetologo,))
        connection.commit()

        cursore.close()

        

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
        


#da qua in poi metodi generali non appartenenti a classi specifiche


#fil - funzione che date tutte le informazioni che il paziente inserisce nella richiesta account, 
#      procede ad inserirle effettivamente nella base di dati 
def inserisci_richiesta(nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, password):
    
    # aggiunto cursore nuovo, per evitare errori di buffer
    cursore_3 = connection.cursor()
    
    cursore_3.execute("""INSERT INTO RichiesteAccount 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, paziente, password) 
                    VALUES (%s, %s, %s,%s, %s, %s,%s, %s, %s,%s, %s, %s)""", 
                    (nome, cognome, data_nascita, sesso, codice_fiscale, indirizzo, citta, cap, telefono, email, is_paziente, generate_password_hash(password)))
    connection.commit()
    cursore_3.close()       # chiudo il cursore per evitare leaks
        

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

    # chiudo il cursore dopo aver effettuato tutte le query.
    cursore_2.close()

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
    
    cursore_8 = connection.cursor()

    cursore_8.execute("SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s", ("in_attesa", "TRUE",))
    result = cursore_8.fetchall()
    
    cursore_8.close()

    # formato per il dropdown: mostra nome, cognome, usa l'id come value. Prendo anche il codice fiscale per usarlo come identificatore.
    options = [
        {"label": f"{nome} {cognome} {codice_fiscale}", "value": id_richiesta}
        for id_richiesta, nome, cognome, codice_fiscale in result
    ]
    return options


# PER I DIABETOLOGI
# funzione che ritorna tutte le richieste di creazione account con stato "in_attesa"
def get_richieste_account_diabetologi():
    
    cursore_23 = connection.cursor()

    cursore_23.execute("SELECT id_richiesta, nome, cognome, codice_fiscale FROM richiesteaccount WHERE stato_richiesta = %s AND paziente = %s", ("in_attesa", "FALSE",))
    result = cursore_23.fetchall()
    
    cursore_23.close()

    # formato per il dropdown: mostra nome, cognome, usa l'id come value. Prendo anche il codice fiscale per usarlo come identificatore.
    options = [
        {"label": f"{nome} {cognome} {codice_fiscale}", "value": id_richiesta}
        for id_richiesta, nome, cognome, codice_fiscale in result
    ]
    return options




# funzione che prende un diab/paz e ne mostra i dati nella richiesta. 
# viene triggerata dalla callback del dropdown.
def get_dati_richiesta_account_by_id(id_richiesta):
    
    cursore_5 = connection.cursor()

    cursore_5.execute("""
        SELECT nome, cognome, data_nascita, sesso, codice_fiscale,
               indirizzo, citta, cap, telefono, email, paziente, data_richiesta, stato_richiesta
        FROM richiesteaccount
        WHERE id_richiesta = %s
    """, (id_richiesta,))
    result = cursore_5.fetchone()

    cursore_5.close()

    if result:
        chiavi = ["nome", "cognome", "data_nascita", "sesso", "codice_fiscale",
                  "indirizzo", "citta", "cap", "telefono", "email", "paziente", "data_richiesta", "stato_richiesta"]
        return dict(zip(chiavi, result))
    return None


# funzione che prende i dettagli di un singolo paziente dato il suo id.
def get_dettagli_paziente(id_paziente):
    cursore_20 = connection.cursor()
    cursore_20.execute("""
        SELECT id_paziente, nome, cognome, data_nascita, sesso, codice_fiscale,
               indirizzo, citta, cap, telefono, email, username, diabetologo_associato
        FROM paziente
        WHERE id_paziente = %s
    """, (id_paziente,))
    result = cursore_20.fetchone()
    cursore_20.close()

    if result:
        chiavi = ["id_paziente", "nome", "cognome", "data_nascita", "sesso", "codice_fiscale", "indirizzo", "citta", "cap", "telefono", "email", "username", "diabetologo_associato"]
        return dict(zip(chiavi, result))
    return None


# funzione che prende tutti i pazienti nella db, e ne ritorna i dati in un dict
def get_all_pazienti():
    cursore_6 = connection.cursor()
    cursore_6.execute("SELECT id_paziente, nome, cognome, codice_fiscale, data_nascita, email, telefono FROM paziente")
    result = cursore_6.fetchall()

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

    cursore_6.close()
    return pazienti


# funzione che dato l'id di un diabetologo, ritorna tutti i suoi dati (tranne pw)
def get_dettagli_diabetologo(id_diabetologo):
    cursore_21 = connection.cursor()
    cursore_21.execute("""
        SELECT id_diabetologo, nome, cognome, data_nascita, sesso, codice_fiscale,
               indirizzo, citta, cap, telefono, email, username
        FROM diabetologo
        WHERE id_diabetologo = %s
    """, (id_diabetologo,))
    result = cursore_21.fetchone()
    cursore_21.close()

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
    cursore_7 = connection.cursor()
    cursore_7.execute("SELECT id_diabetologo, nome, cognome, codice_fiscale, data_nascita, email, telefono FROM diabetologo")
    result = cursore_7.fetchall()

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

    cursore_7.close()
    return diabetologi

# ***********************
# funzione che ritorna il grafico delle media della glicemia dei pazienti di ogni diabetologo
def visualizza_media_glicemia_per_diabetologi():
    cursore=connection.cursor()
    diabetologi = get_all_diabetologi()
    nomi = []
    medie = []

    for d in diabetologi:
        id_d = d["id_diabetologo"]
        cursore.execute("SELECT * FROM Diabetologo WHERE id_diabetologo=%s",(id_d,))
        r=cursore.fetchone()
        Diab=Diabetologo(r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12])
        dati_pazienti = Diab.visualizza_pazienti_associati()

        nome_completo = f"{d['nome']} {d['cognome']}"
        nomi.append(nome_completo)

        if not dati_pazienti:
            medie.append(0)  # oppure None, se si vuole lasciare vuota la colonna
            continue

        media_diabetologo = sum([r[1] for r in dati_pazienti]) / len(dati_pazienti)
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

    fig = go.Figure(data=[go.Bar(x=nomi, y=medie, marker_color="royalblue")])
    fig.update_layout(
        xaxis_title="Diabetologo",
        yaxis_title="glicemia (mg/dL)",
        legend=dict(
            orientation="h",  # orizzontale
            yanchor="bottom",
            y=1.02,  # poco sopra il grafico (y=0 per sotto)
            xanchor="left",
            x=0),
        margin=dict(l=10, r=10, t=5, b=10)
    )
    return fig

    # ***********************

# funzione che permette di prendere il grafico un solo diabetologo
def visualizza_media_glicemia_pazienti_diabetologo(id_diabetologo):
    """Ritorna un grafico a istogramma contenente la media glicemica dei pazienti associati ad un diabetologo."""

    cursore = connection.cursor()
    cursore.execute("SELECT * FROM Diabetologo WHERE id_diabetologo = %s", (id_diabetologo,))
    r = cursore.fetchone()

    if not r:
        fig = go.Figure()
        fig.add_annotation(
            text="Diabetologo non trovato",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=18, color="red")
        )
        return fig

    # Istanzia l'oggetto Diabetologo
    Diab = Diabetologo(r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8], r[9], r[10], r[11], r[12])
    dati_pazienti = Diab.visualizza_pazienti_associati()

    if not dati_pazienti:
        fig = go.Figure()
        fig.add_annotation(
            text=f"Nessun dato per {r[1]} {r[2]}",
            xref="paper", yref="paper",
            showarrow=False,
            font=dict(size=18, color="red")
        )
        return fig

    # dati_pazienti è una sequenza di tuple/dizionari dove:
    # - dati_pazienti[i][0]: nome paziente
    # - dati_pazienti[i][1]: media glicemia
    nomi_pazienti = [dp[0] for dp in dati_pazienti]
    medie_glicemia = [round(dp[1], 2) for dp in dati_pazienti]

    fig = go.Figure(data=[
        go.Bar(x=nomi_pazienti, y=medie_glicemia, marker_color="teal")
    ])
    fig.update_layout(
        xaxis_title="Pazienti",
        yaxis_title="Glicemia (mg/dL)",
        margin=dict(l=10, r=10, t=30, b=40),
    )
    return fig



def get_id_paziente_by_username(username):
    cursore = connection.cursor()
    query = "SELECT id_paziente FROM paziente WHERE username = %s"
    cursore.execute(query, (username,))
    result = cursore.fetchone()
    cursore.close()
    if result:
        return result[0]  # l'ID del paziente
    return None
    

#if __name__ == '__main__':
    
    # Esempio: 31 dicembre 2025, ore 10:30
    #Diabetologo.visualizza_dati_paziente(17,'Andrea.Agostini0_P')    
