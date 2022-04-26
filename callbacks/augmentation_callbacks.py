from dash import Input, Output
from dash import html, dcc
import dash_bootstrap_components as dbc


def _white_noise_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('SNR (dB)'),
                    html.Br(),
                    dcc.Input(
                        id='input-white_noise_snr',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220})


def _background_noise_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('SNR (dB)'),
                    html.Br(),
                    dcc.Input(
                        id='input-background_noise_snr',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Background class'),
                    dcc.Dropdown(
                        id='dropdown-background_noise_class',
                        options=['a', 'b'],
                        value='a'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220*2})


def _gain_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Gain factor'),
                    html.Br(),
                    dcc.Input(
                        id='input-gain_factor',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220})


def _time_shift_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Maximum shift'),
                    html.Br(),
                    dcc.Input(
                        id='input-time_shift_max_shift',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Background class'),
                    dcc.Dropdown(
                        id='dropdown-time_shift_shift_direction',
                        options=['right', 'left', 'both'],
                        value='both'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220*2})


def _pitch_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Fractional steps'),
                    dcc.Dropdown(
                        id='dropdown-pitch_fractional_steps',
                        options=[-3, -2, -1, 1, 2, 3],
                        value=1
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220})


def _speed_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Label('Speed factor'),
                    html.Br(),
                    dcc.Input(
                        id='input-speed_factor',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220})



def _otherwise():
    return []


def augmentation_callbacks(app, cfg):

    @app.callback(
        Output('content-augmentation_arguments', 'children'),
        Input('dropdown-augmentation_method', 'value'))
    def update_augmentation_arguments(method):
        if method == 'White noise':
            return _white_noise_children()
        elif method == 'Background noise':
            return _background_noise_children()
        elif method == 'Gain':
            return _gain_children()
        elif method == 'Time shift':
            return _time_shift_children()
        elif method == 'Pitch':
            return _pitch_children()
        elif method == 'Speed':
            return _speed_children()
        else:
            return _otherwise()
