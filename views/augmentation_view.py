from dash import html, dcc
import dash_bootstrap_components as dbc
from views import common

def augmentation_view():
    return html.Div([
        common.header('Audio data explorer',
            '''
            A web application for audio data visualization and training with data augmentation.
            '''
        )
    ], style={'width':common.PAGE_WIDTH, 'padding-left':'5%', 'padding-right':'5%', 'padding-bottom':200})
