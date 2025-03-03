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
