from h2o_wave import main, app, Q, ui
import mysql.connector



# Database credentials
user = 'patzer'
password = 'patzer-forever'
host = '34.41.77.17'
database = 'hackathon'



from google.cloud.sql.connector import Connector
import sqlalchemy

# initialize Connector object
connector = Connector()

# function to return the database connection object
def getconn():
    conn = connector.connect(
        'earnest-vine-451607-f1:us-central1:hackathon-run-one',
        "pymysql",
        user=user,
        password=password,
        db=database
    )
    return conn

# create connection pool with 'creator' argument to our connection object function
pool = sqlalchemy.create_engine(
    "mysql+pymysql://",
    creator=getconn,
)

with pool.connect() as db_conn:
  # create ratings table in our sandwiches database
  db_conn.execute(
    sqlalchemy.text(
      "CREATE TABLE IF NOT EXISTS ratings "
      "( id SERIAL NOT NULL, name VARCHAR(255) NOT NULL, "
      "origin VARCHAR(255) NOT NULL, rating FLOAT NOT NULL, "
      "PRIMARY KEY (id));"
    )
  )

  # commit transaction (SQLAlchemy v2.X.X is commit as you go)
  db_conn.commit()

  # insert data into our ratings table
  insert_stmt = sqlalchemy.text(
      "INSERT INTO ratings (name, origin, rating) VALUES (:name, :origin, :rating)",
  )

  # insert entries into table
  db_conn.execute(insert_stmt, parameters={"name": "HOTDOG", "origin": "Germany", "rating": 7.5})
  db_conn.execute(insert_stmt, parameters={"name": "BÀNH MÌ", "origin": "Vietnam", "rating": 9.1})
  db_conn.execute(insert_stmt, parameters={"name": "CROQUE MADAME", "origin": "France", "rating": 8.3})

  # commit transactions
  db_conn.commit()

  # query and fetch ratings table
  results = db_conn.execute(sqlalchemy.text("SELECT * FROM ratings")).fetchall()

  # show results
  for row in results:
    print(row)

connector.close()



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

    q.page['db_status'] = ui.form_card(
        box=ui.box('content'),
        items=[
            ui.text_xl(f"Database Connection Status: NONE"),
        ]
    )

    # Save the page
    await q.page.save()
