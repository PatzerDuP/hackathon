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

@app('/hackathon', mode='unicast', on_startup=on_startup, on_shutdown=on_shutdown) 




#### Testign hopefully remove later
async def test_db_connection(q):
    try:
        # Try to get the connection
        connection = mysql.connector.connect(
        user='patzer',  # Your MySQL username
        password='patzer-forever',  # Your MySQL password
        host = '34.41.77.17', #host='/cloudsql/{}'.format(cloud_sql_connection_name),  # Cloud SQL Unix socket
        database='hackathon',  # Database you want to connect to
    )
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



# # Example: Function to query data from the DB
# async def fetch_data(q):
#     connection = mysql.connector.connect(
#         user='patzer',  # Your MySQL username
#         password='patzer-forever',  # Your MySQL password
#         host = '10.67.32.3', #host='/cloudsql/{}'.format(cloud_sql_connection_name),  # Cloud SQL Unix socket
#         database='hackathon',  # Database you want to connect to
#     )
#     cursor = connection.cursor(dictionary=True)
#     cursor.execute("SELECT * FROM prem_upload")
#     results = cursor.fetchall()
#     cursor.close()
#     connection.close()
    
#     return results


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
        image='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRivCct2RebT6-C8Rj2M3Az3PQiPr8jOEFu5Q&s',

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

