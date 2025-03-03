from h2o_wave import main, app, Q, ui
import mysql.connector

# Database credentials
user = 'patzer'
password = 'patzer-forever'
host = '34.41.77.17'
database = 'hackathon'

# Function to test database connection (no async needed)
async def test_db_connection(q: Q):
    try:
        connection = mysql.connector.connect(
            user=user,
            password=password,
            host=host,
            database=database
        )
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

# Main app function to display the connection status
@app('/hackathon')
async def serve(q: Q):
    # Test database connection (this is synchronous code)
    db_connection_status = test_db_connection()
    
    # Display the connection status on the screen
    q.page['db_status'] = ui.form_card(
        box=ui.box('content'),
        items=[
            ui.text_xl(f"Database Connection Status: {db_connection_status}"),
        ]
    )
    
    # Save the page
    await q.page.save()
