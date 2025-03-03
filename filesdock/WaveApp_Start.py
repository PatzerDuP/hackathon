from h2o_wave import main, app, Q, ui
import mysql.connector

# Database credentials
user = 'patzer'
password = 'patzer-forever'
host = '34.41.77.17'
database = 'hackathon'



# Main app function to display the connection status
@app('/hackathon')
async def serve(q: Q):
    q.page['db_status'] = ui.form_card(
        box=ui.box('content'),
        items=[
            ui.text_xl(f"Database Connection Status: NONE"),
        ]
    )
 
    
    
    # Save the page
    await q.page.save()
