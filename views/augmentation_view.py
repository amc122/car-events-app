from dash import html, dcc
import dash_bootstrap_components as dbc
from views import common

# html.Div([
#             dbc.Row([
#                 html.Label('Select and add the desired data augmentation methods'),
#                 dbc.Col(dcc.Dropdown(
#                     id='dropdown-augmentation_method',
#                     options=augmentation_options,
#                     value=augmentation_options[0]
#                 )),
#                 dbc.Col(dbc.Button('+',
#                     id='submit-augmentation_method',
#                     color='primary',
#                     className='me-1'
#                 ))
#             ])
#         ], style={'display':'inline-block'})


def augmentation_view(augmentation_options):
    return html.Div([
        common.my_header(),

        html.Div([
            html.H2('Data augmentation options')
        ]),

        html.Div([
            html.Label('Select and add the desired data augmentation methods'),
            dcc.Dropdown(
                id='dropdown-augmentation_method',
                options=augmentation_options,
                value=augmentation_options[0]
            )
        ], style={'display':'inline-block'}),
        
        html.Div(id='content-augmentation_arguments'),

        html.Div([
            dbc.Button('Add',
                id='submit-augmentation_add2list',
                color='primary',
                className='me-1'    
            ),
            dbc.Button('Clear list',
                id='submit-augmentation_clear_list',
                color='danger',
                className='me-1'
            )
        ], style={'padding':5}),
        html.Div(id='alert-augmentation', style={'padding':5}),

        html.Br(),

        html.Div(id='dummy', style={'display':'none'}),

        html.Div([
            html.H2('List of included augmentation methods'),
            html.Br(),
            html.Div(id='content-augmentation_list')
        ]),

        html.Div([
            html.H2('TODO: Set an augmentation weight for each class'),
            html.Br(),
            html.Div(id='content-augmentation_weights')
        ]),

        # html.Div([
        #     dcc.Loading(
        #         id='loading-augmentation',
        #         type='default',
        #         children=html.Div(id='loading-augmentation_output')
        #     )
        # ], style={'padding':5}),

        html.Div([
            html.Progress(id='progress-augmentation')
        ], style={'padding':5}),

        html.Div(id='alert-augmentation_process', style={'padding':5}),

        html.Div([
            dbc.Row([
                dbc.Col(
                    dbc.Button('Start data augmentation',
                        id='submit-augmentation_start',
                        color='primary',
                        className='me-1'
                    )
                ),
                dbc.Col(
                    dbc.Button('Get augmented dataset',
                        id='submit-get_augmented_dataset',
                        color='primary',
                        className='me-1'
                    )
                ),
                dbc.Col(
                    dcc.Link(
                        dbc.Button('Back',
                            id='submit-aug2index',
                            color='primary',
                            className='me-1'
                        ), href='/'
                    )
                )
            ])
        ], style={'padding':5})

    ], style={'width':common.PAGE_WIDTH, 'padding-left':'5%', 'padding-right':'5%', 'padding-top':50, 'padding-bottom':200})
