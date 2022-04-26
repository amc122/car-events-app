from dash import Input, Output, State
from dash import html, dcc
import dash_bootstrap_components as dbc


def _white_noise_children():
    return html.Div([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Div([
                        html.Label('SNR (dB)'),
                        html.Br()
                    ]),
                    dcc.Input(
                        id='arg-white_noise_snr',
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
                    html.Div([
                        html.Label('SNR (dB)'),
                        html.Br()
                    ]),
                    dcc.Input(
                        id='arg-background_noise_snr',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Background class'),
                    dcc.Dropdown(
                        id='arg-background_noise_class',
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
                    html.Div([
                        html.Label('Gain factor'),
                        html.Br()
                    ]),
                    dcc.Input(
                        id='arg-gain_factor',
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
                    html.Div([
                        html.Label('Maximum shift'),
                        html.Br()
                    ]),
                    dcc.Input(
                        id='arg-time_shift_max_shift',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ]),
            dbc.Col([
                html.Div([
                    html.Label('Background class'),
                    dcc.Dropdown(
                        id='arg-time_shift_shift_direction',
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
                        id='arg-pitch_fractional_steps',
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
                    html.Div([
                        html.Label('Speed factor'),
                        html.Br()
                    ]),
                    dcc.Input(
                        id='arg-speed_factor',
                        type='number',
                        placeholder='Enter a number'
                    )
                ], style={'width':200, 'padding':5, 'display':'inline-block'})
            ])
        ])
    ], style={'width':220})


def _list_row_children():
    pass


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
            return []


    @app.callback(
        Output('content-augmentation_list', 'children'),
        State('content-augmentation_list', 'children'),
        State('dropdown-augmentation_method', 'value'),
        State('content-augmentation_arguments', 'children'),
        Input('submit-augmentation_add2list', 'n_clicks'))
    def update_augmentation_list(augmentations, method, all_args, submit):
        if (method is not None) and (all_args is not None):
            aux = all_args['props']['children'][0]['props']['children']
            n_args = len(aux)
            kwargs = {}
            for i in range(n_args):
                aux2 = aux[i]['props']['children'][0]['props']['children'][1]['props']
                kwargs[aux2['id']] = aux2['value']
            
            print(kwargs)
            print(submit)
        return []
