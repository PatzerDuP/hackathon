# We import these to be able to read and write
from h2o_wave import main, app, Q, ui 


# Get feedback when app is started and stopped
def on_startup():
    print('App started!')
def on_shutdown():
    print('App stopped!')

# Will find the app at localhost:10101/hackathon
@app('/hackathon', mode='unicast', on_startup=on_startup, on_shutdown=on_shutdown) # Also look into 'multicast' to sync for one user
# https://wave.h2o.ai/docs/realtime
# Async functions start here

async def serve(q: Q):

    paths = q.args.datasets
    print("paths", paths)

    if not paths:
        # Display the file upload form since there are no paths yet
        q.page['example'] = ui.form_card(box='1 1 4 5', items=[
            ui.text_xl('Upload datasets'),
            ui.file_upload(name='datasets', label='Upload', multiple=False, file_extensions=['csv']),
        ])
    else:
        print(paths)
        for path in paths:
            local_path = await q.site.download(paths, '.')
            print(f"File downloaded to: {local_path}", paths)
        
        q.page['example'] = ui.form_card(box='1 1 4 5', items=[
            ui.text_xl(f"File downloaded successfully: {local_path}"),
            ui.button(name='upload_another', label='Upload another file', primary=True)
        ])

    if q.args.upload_another:
            # Clear the datasets to allow the user to upload a new file
            q.args.datasets = None

            # Reset the file upload form
            q.page['example'] = ui.form_card(box='1 1 4 5', items=[
                ui.text_xl('Upload another dataset'),
                ui.file_upload(name='datasets', label='Upload', multiple=False, file_extensions=['csv']),
            ])

    # Save this page to update the server side    
    await q.page.save()