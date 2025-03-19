# Connect from Cloud SQL

from sqlalchemy import create_engine

# Create SQLAlchemy engine
engine = create_engine(
    'mysql+pymysql://service-acc-docker1@earnest-vine-451607-f1.iam.gserviceaccount.com@localhost:3306/hackathon'
)

# Use the connection
with engine.connect() as db_conn:
    # Your database operations
    pass
# import mysql.connector

# connection = mysql.connector.connect(
#     host='34.41.77.17',
#     user='patzer',
#     password='patzer-forever',
#     database='hackathon'
# )

# cursor = connection.cursor()
# cursor.execute("SELECT DATABASE();")
# result = cursor.fetchone()
# print("Connected to database:", result)