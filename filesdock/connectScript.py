from h2o_wave import main, app, Q, ui 

from google.cloud.sql.connector import Connector

import psycopg2
from google.auth import default
import csv
import io


INSTANCE_CONNECTION_NAME = 'earnest-vine-451607-f1:us-central1:test-postgres-db' 
DB_USER = 'postgres'
DB_PASS = 'test-postgres'
DB_NAME = 'postgres'

# Connect to PostgreSQL via Cloud SQL
def get_db_connection():
    connector = Connector()
    conn = connector.connect(
        INSTANCE_CONNECTION_NAME,
        "pg8000",
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


def write_data_to_db(data):
    connection = get_db_connection()
    cursor = connection.cursor()
    print("Only connected")

    insert_query = "INSERT INTO prem_upload (idnr, premium) VALUES (%s, %s)"

    # Execute the insert query for each row in the data
    for row in data:
        cursor.execute(insert_query, row)
    print("Precommit")
    # Commit the transaction
    connection.commit()
    
    cursor.close()
    connection.close()

    # Print end of function
    print("Data written to database hopefully")


def write_csv_to_db(file_path):
    connection = get_db_connection()
    cursor = connection.cursor()
    print("Connected to database")

    # Use COPY command for efficient bulk insert
    with open(file_path, 'r') as f:
        cursor.copy_expert("COPY prem_upload (idnr, premium) FROM STDIN WITH CSV HEADER", f)
    
    print("Precommit")
    # Commit the transaction
    connection.commit()
    
    cursor.close()
    connection.close()

    # Print end of function
    print("Data written to database successfully")

def write_chunks_to_db(file_path, batch_size=10000):
    connection = get_db_connection()
    cursor = connection.cursor()
    print("Connected to database")

    insert_query = "INSERT INTO prem_upload (idnr, premium) VALUES (%s, %s)"
    
    with open(file_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # Skip the header row
        batch = []
        for row in reader:
            batch.append(row)
            if len(batch) >= batch_size:
                cursor.executemany(insert_query, batch)
                connection.commit()
                batch = []
        
        if batch:
            cursor.executemany(insert_query, batch)
            connection.commit()

    cursor.close()
    connection.close()

    print("Data written to database successfully")


def load_csv_to_db(csv_data):
    connection = get_db_connection()
    cursor = connection.cursor()

    try:
        # Convert CSV string to file-like object
        csv_file = io.StringIO(csv_data)
        
        # Use PostgreSQL COPY command to load data into table directly
        cursor.copy_from(csv_file, 'prem_upload', sep=',', null='\\N', columns=('idnr', 'premium'))  # Adjust column names
        connection.commit()  # Commit the transaction
        
        print("Data loaded successfully!")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        cursor.close()
        connection.close()

