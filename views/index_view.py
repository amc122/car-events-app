from dash import html, dcc
import dash_bootstrap_components as dbc
from views import common


def _overview():
    return html.Div([
        html.H2('Overview'),
        html.P(
            '''
            This page provides information about the selected dataset and is utilized to setup the next steps, 
            i.e. data augmentation and/or data preparation.
            '''
        )
    ])


def _metadata_inspection(fig_class_histogram, fig_duration_histogram, fig_power_histogram):
    return html.Div([
        html.H2('Metadata inspection'),
        html.Div([
            dcc.Graph(
                id='class-histogram', figure=fig_class_histogram
            )
        ], style={'width':'34%', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(
                id='duration-histogram', figure=fig_duration_histogram
            )
        ], style={'width':'33%', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(
                id='power-histogram', figure=fig_power_histogram
            )
        ], style={'width':'33%', 'display':'inline-block'})
    ])


def _audio_data_inspection_and_setup(class_names, file_names, featext_methods):
    class_names_options = [{'label': cn, 'value': cn} for cn in class_names]
    return html.Div([
        html.H2('Audio data inspection and setup'),

        html.H3('Example audio'),
        html.Div([
            html.Label('Class'),
            dcc.Dropdown(
                id='dropdown-class',
                options=class_names,
                value=class_names[0]
            )
        ], style={'width':'24%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('File name'),
            dcc.Dropdown(
                id='dropdown-file_name',
                options=file_names,
                value=None
            )
        ], style={'width':'74%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Audio(
                id='audio-player',
                src=None,
                controls=True
            )
        ], style={'padding':5}),

        html.H3('Feature extraction'),
        html.Div(html.P([
            '''
            Choose a feature extraction method and the corresponding parameters to visualize the result.
            Your choice will be stored for further computations.
            '''
        ])),
            
        html.Div([
            html.Label('Method'),
            dcc.Dropdown(
                id='dropdown-featext_method',
                options=featext_methods,
                value=featext_methods[0]
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Sample rate'),
            dcc.Dropdown(
                id='dropdown-featext_sample_rate',
                options=[8000, 16000, 24000],
                value=16000
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Num. points FFT'),
            dcc.Dropdown(
                id='dropdown-featext_n_fft',
                options=[256, 512, 1024],
                value=512
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Window length'),
            dcc.Dropdown(
                id='dropdown-featext_win_length',
                options=[256, 512, 1024],
                value=512
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Hop length'),
            dcc.Dropdown(
                id='dropdown-featext_hop_length',
                options=[128, 256, 384, 512, 640, 768],
                value=384
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Num. filters'),
            dcc.Dropdown(
                id='dropdown-featext_n_filter',
                options=[32, 64, 128],
                value=128
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Num. FCC'),
            dcc.Dropdown(
                id='dropdown-featext_n_fcc',
                options=[20, 40, 60, 80],
                value=40
            )
        ], style={'width':'14%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            dcc.Graph(id='wave-plot')
        ]),

        html.Div([
            html.H3('Classifier classes'),
            html.P('Select classes included as classifier outputs'),
            html.Div([
                dbc.Checklist(
                    id='checklist-classifier_classes',
                    options=class_names_options,
                    value=class_names
                )
            ])
        ], style={'width':'40%', 'padding-right':'5%', 'display':'inline-block'}),

        html.Div([
            html.H3('Background classes'),
            html.P('Select classes included as classifier outputs'),
            html.Div([
                dbc.Checklist(
                    id='checklist-background_classes',
                    options=class_names_options,
                    value=[]
                )
            ])
        ], style={'width':'40%', 'padding-left':'5%', 'display':'inline-block'}),

        html.Div([
            html.H3('Next step'),
            html.P('Select your next step'),
            dcc.Link(
                dbc.Button('Data augmentation', 
                    id='submit-index2aug', 
                    color='primary', 
                    className='me-1'
                ), href='/augmentation'
            ),
            dbc.Button('Data preparation', 
                id='submit-index2preparation', 
                color='primary', 
                className='me-1'
            )
        ], style={'padding-top':20, 'padding-bottom':20}),
    ])



def index_view(fig_class_histogram, fig_duration_histogram, fig_power_histogram,
    class_names, file_names, featext_methods):
    return html.Div([
        common.my_header(),
        _overview(),
        _metadata_inspection(fig_class_histogram, fig_duration_histogram, fig_power_histogram),
        _audio_data_inspection_and_setup(class_names, file_names, featext_methods),
    ], style={'width':common.PAGE_WIDTH, 'padding-left':'5%', 'padding-right':'5%', 'padding-top':50, 'padding-bottom':200})