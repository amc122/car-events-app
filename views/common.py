from dash import html

PAGE_WIDTH = 1200

def header(title, text):
    return html.Div([
        html.Div(
            className='app-header',
            children=[html.Div(title, className='app-header--title')]
        ),
        html.Div([text], style={'padding-top': 20})
    ])