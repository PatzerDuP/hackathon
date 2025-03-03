from h2o_wave import site, ui

# Grab a reference to a page
page = site['/hackathon']

# Modify the page by adding a card
page['greeting'] = ui.markdown_card(
    box='1 1 2 2',
    title='Hello!',
    content='Welcome to H2O Wave!'
)

# Save the page
page.save()