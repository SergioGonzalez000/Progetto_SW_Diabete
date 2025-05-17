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

def get_balls():
    cur.execute("SELECT * FROM palle")
    