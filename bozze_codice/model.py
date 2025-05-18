# gestione Database remoto, gestione altra roba logica

import psycopg2


connection = psycopg2.connect(
    host='aws-0-eu-central-2.pooler.supabase.com',
    dbname='postgres',
    user='postgres.dozqdfylbqeriitzoblm',
    password='IOtRbsJmgylEH5Pl',
    port='5432'
)

cur=connection.cursor()

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

class Terapia():
    def __init__(self):
        pass
        
class Farmaco():
    def __init__(self):
        pass

class Glicemia():
    def __init__(self):
        pass


        