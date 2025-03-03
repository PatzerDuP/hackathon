from h2o_wave import main, app, Q, ui
#import mysql.connector

from google.cloud.sql.connector import Connector, IPTypes
import pymysql

import sqlalchemy




def connect_with_connector() -> sqlalchemy.engine.base.Engine:

    instance_connection_name = "earnest-vine-451607-f1:us-central1:hackathon-run-one"
    db_user = "patzer"  # e.g. 'my-db-user'
    db_pass = "patzer-forever" # e.g. 'my-db-password'
    db_name = "hackathon"  # e.g. 'my-database'

    ip_type = IPTypes.PRIVATE

    connector = Connector(ip_type=ip_type, refresh_strategy="LAZY")

    def getconn() -> pymysql.connections.Connection:
        conn: pymysql.connections.Connection = connector.connect(
            instance_connection_name,
            "pymysql",
            user=db_user,
            password=db_pass,
            db=db_name,
        )
        return conn

    pool = sqlalchemy.create_engine(
        "mysql+pymysql://",
        creator=getconn,
        # ...
    )
    return pool


# Main app function to display the connection status
@app('/hackathon')

async def serve(q: Q):

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


    # BIG IF
    try:
        # Attempt to connect to the database
        engine = connect_with_connector()
        with engine.connect() as connection:
            result = connection.execute("SELECT 1")
            db_status = "CONNECTED" if result.fetchone() else "FAILED"
    except Exception as e:
        db_status = f"FAILED: {e}"



    q.page['db_status'] = ui.form_card(
        box=ui.box('content'),
        items=[
            ui.text_xl(f"Database Connection Status: {db_status}"),
        ]
    )

    # Save the page
    await q.page.save()
