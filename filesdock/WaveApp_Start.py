# We import these to be able to read and write
from h2o_wave import main, app, Q, ui 
import mysql.connector
import pymysql
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
from google.auth import compute_engine
from google.auth.transport.requests import Request
import os

# Get feedback when app is started and stopped
def on_startup():
    print('App started!') 
def on_shutdown():
    print('App stopped!')

# Will find the app at localhost:10101/hackathon
@app('/hackathon', mode='unicast', on_startup=on_startup, on_shutdown=on_shutdown) # Also look into 'multicast' to sync for one user
# https://wave.h2o.ai/docs/realtime




async def get_db_connection(q):
    # Replace with your Cloud SQL instance connection name
    cloud_sql_connection_name = 'earnest-vine-451607-f1:us-central1:hackathon-run-one'
    # Connect using the Cloud SQL socket
    connection = mysql.connector.connect(
        user='patzer',  # Your MySQL username
        password='patzer-forever',  # Your MySQL password
        host = '34.41.77.17', #host='/cloudsql/{}'.format(cloud_sql_connection_name),  # Cloud SQL Unix socket
        database='hackathon',  # Database you want to connect to
    )
    
    return connection

#### Testign hopefully remove later
async def test_db_connection(q):
    try:
        # Try to get the connection
        connection = get_db_connection()
        # Create a cursor to run a test query (optional)
        cursor = connection.cursor()
        cursor.execute("SELECT 1")  # Simple query to check the connection
        result = cursor.fetchone()
        cursor.close()
        connection.close()
        
        # If the result is as expected, return success
        if result:
            return "Connection successful!"
        else:
            return "Connection failed: No result returned."
    except mysql.connector.Error as err:
        return f"Connection failed: {err}"






# Example: Function to query data from the DB
async def fetch_data(q):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM prem_upload")
    results = cursor.fetchall()
    cursor.close()
    connection.close()
    
    return results


# Async functions start here
async def serve(q: Q):

    # Declare the layout of the page beforehand
    q.page['meta'] = ui.meta_card(box='', layouts=[
        ui.layout(
            breakpoint='m',
            zones=[
                ui.zone('header'),
                ui.zone('body', direction=ui.ZoneDirection.ROW, zones=[
                    ui.zone('sidebarL', size='20%'),
                    ui.zone('content', size='60%'),
                    ui.zone('sidebarR', size='20%'),
                ]),
                ui.zone('footer'),
            ]
        )
    ])

    
    q.page['headerM'] = ui.header_card(
        box=ui.box('header'),
        title='Miway Hackathon',
        subtitle='Modelling your way',
        image='data:image/png;base64,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',

    )

    paths = q.args.dataset
    print("paths", paths)

    if not paths:
        # Display the file upload form since there are no paths yet
        q.page['upload'] = ui.form_card(
            box=ui.box('content'), 
            items=[
            ui.text_xl('Upload dataset'),
            ui.file_upload(name='dataset', label='Upload', multiple=False, file_extensions=['csv']),
        ])
    else:
        print(paths)
        for path in paths:
            local_path = await q.site.download(path, '.')
            print(f"File downloaded to: {local_path}", paths)
        
        # Pretty interesting trick, after uploaded, we change the page, and presumably change variable when button is clicked
        q.page['upload'] = ui.form_card(
            box=ui.box('content'), items=[
            ui.text_xl(f"File downloaded successfully: {local_path}"),
            ui.button(name='upload_another', label='Upload another file', primary=True)
        ])




    db_connection_status = await test_db_connection()
    print("Database Connection Status:", db_connection_status)  # Log to the console for server-side debugging
    
    # Display the connection status in the app
    q.page['db_status'] = ui.form_card(
        box=ui.box('content'),
        items=[
            ui.text_xl(f"Database Connection Status: {db_connection_status}"),
        ]
    )


    # Save this page to update the server side    
    await q.page.save()

