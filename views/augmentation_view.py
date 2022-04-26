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
            )
        ], style={'padding':5}),

        html.Br(),

        html.Div([
            html.H2('List of included augmentation methods'),
            html.Br(),
            html.Div(id='content-augmentation_list')
        ])

    ], style={'width':common.PAGE_WIDTH, 'padding-left':'5%', 'padding-right':'5%', 'padding-top':50, 'padding-bottom':200})
