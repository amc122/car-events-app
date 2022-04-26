from dash import html


TITLE = 'Audio data preprocessing'
DESCRIPTION = '''
    A web application for audio data visualization and training with data augmentation.
    '''
PAGE_WIDTH = 1200


def header(title, text):
    return html.Div([
        html.Div(
            className='app-header',
            children=[html.Div(title, className='app-header--title')]
        ),
        html.Div([text], style={'padding-top': 20, 'padding-bottom':20})
    ])


def my_header():
    return header(TITLE, DESCRIPTION)