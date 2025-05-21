# gestione Database remoto, gestione altra roba logica
from abc import ABC,abstractmethod

import psycopg2


connection = psycopg2.connect(
    host='aws-0-eu-central-2.pooler.supabase.com',
    dbname='postgres',
    user='postgres.dozqdfylbqeriitzoblm',
    password='IOtRbsJmgylEH5Pl',
    port='5432'
)

cur=connection.cursor()

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
        paziente=richiesta[12]

        if paziente:
            cur.execute("SELECT * FROM Paziente WHERE nome = %s AND cognome = %s",(nome,cognome))
            righe = cur.fetchall()
            num=len(righe)
            username=f"{nome}.{cognome}{num}_P"
        else:
            cur.execute("SELECT * FROM Diabetologo WHERE nome = %s AND  cognome = %s",(nome,cognome))
            righe = cur.fetchall()
            num=righe.count()
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

if __name__ == '__main__':
    Admin.approva_richiesta(1)