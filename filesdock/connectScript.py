from h2o_wave import main, app, Q, ui 

from google.cloud.sql.connector import Connector

import psycopg2
from google.auth import default

INSTANCE_CONNECTION_NAME = 'earnest-vine-451607-f1:us-central1:test-postgres-db' 
DB_USER = 'postgres'
DB_PASS = 'test-postgres'
DB_NAME = 'postgres'

# Connect to PostgreSQL via Cloud SQL
def get_db_connection():
    connector = Connector()
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "postgresql",
        user=DB_USER,
        password=DB_PASS,
        db=DB_NAME,
    )
    return conn

def fetch_data_from_db():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    # Query your database
    cursor.execute("SELECT * FROM prem_upload")
    data = cursor.fetchall()
    
    cursor.close()
    connection.close()
    
    return data

#data = fetch_data_from_db()
#print(data)
