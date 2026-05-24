import psycopg2

def get_connection():
    conn = psycopg2.connect(                              
    host="localhost",                                      
    database="cjis",
    user="postgres",
    password="CJIS",
    port="5432")
    return conn
