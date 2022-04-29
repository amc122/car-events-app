from dash import html, dcc


TITLE = 'Audio data preprocessing'
DESCRIPTION = '''
    A web application for audio data visualization and training with data augmentation.
    '''
PAGE_WIDTH = 1400


def header(title, text):
    return html.Div([
        html.Div(
            className='app-header',
            children=[html.Div(title, className='app-header--title')]
        ),
        html.Div([text], style={'padding-top': 20, 'padding-bottom':20})
    ])


def storage():
    return html.Div([
        dcc.Store(id='memory-classifier_classes', data=[], storage_type='local'),
        dcc.Store(id='memory-augmentation_classes', data=[], storage_type='local'),
        dcc.Store(id='memory-background_classes', data=[], storage_type='local'),
        dcc.Store(id='memory-augmentation_list', data=[], storage_type='local'),
    ])


def my_header():
    return header(TITLE, DESCRIPTION)