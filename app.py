import os
import shutil
import pandas as pd
import torch
import torchaudio
import plotly
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dash import Dash, dcc, html, Input, Output

import config.default as cfg
from utils import extract, metadata

app = Dash(__name__)



# TODO: move app setup to a different file
cfg.CLASS_NAMES = ['Security_Noise', 'Safety_Noise']
def setup(cfg):
    compressed_file_names = extract.select_dataset_version(cfg.CLASS_NAMES, cfg.DATASET_VERSION)
    extract.extract_waves(cfg.COMPRESSED_DATA_DIR, compressed_file_names, 'dataset')
    df = metadata.build_metadata('dataset')
    return df

#####################
# metadata (static) #
#####################

df = setup(cfg)

legend = dict(title='', orientation='h', y=-0.20)
margin = dict(l=20, r=20, t=30, b=30)
height = 360

fig_class_histogram = px.histogram(df, x='class', color='class', title='Class histogram')
fig_class_histogram.update_layout(legend=legend, margin=margin, height=height)

fig_duration_histogram = px.histogram(df, x='duration', color='class', title='Duration histogram')
fig_duration_histogram.update_layout(legend=legend, margin=margin, height=height)

fig_power_histogram = px.histogram(df, x='power', color='class', title='Power histogram')
fig_power_histogram.update_layout(legend=legend, margin=margin, height=height)



# TODO: move layout to a different file
dropdown_width = 150
app.layout = html.Div([
    html.Div(
        className='app-header',
        children=[html.Div('Audio data explorer', className='app-header--title')]
    ),
    html.Div([
        '''
        A web application for audio data visualization and training with data augmentation
        '''
    ], style={'padding-top': 20}),

    html.Div([
        html.H2('Metadata inspection'),
        html.Div([
            dcc.Graph(
                id='class-histogram', figure=fig_class_histogram
            )
        ], style={'width':'33.33%', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(
                id='duration-histogram', figure=fig_duration_histogram
            )
        ], style={'width':'33.33%', 'display':'inline-block'}),
        html.Div([
            dcc.Graph(
                id='power-histogram', figure=fig_power_histogram
            )
        ], style={'width':'33.33%', 'display':'inline-block'})
    ]),

    html.Div([
        html.H2('Audio data inspection'),

        html.H3('Example audio'),
        html.Div([
            html.Label('Class'),
            dcc.Dropdown(
                id='dropdown-class',
                options=cfg.CLASS_NAMES,
                value=cfg.CLASS_NAMES[0]
            )
        ], style={'width':'24%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('File name'),
            dcc.Dropdown(
                id='dropdown-file_name',
                options=df['file_name'].loc[df['class'] == cfg.CLASS_NAMES[0]],
                value=None
            )
        ], style={'width':'48%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Audio(
                id='audio-player',
                src=None,
                controls=True
            )
        ], style={'padding':5}),

        html.H3('Feature extraction'),
        html.Div([
            html.Label('Method'),
            dcc.Dropdown(
                id='dropdown-featext_method',
                options=cfg.FEATEXT_METHODS,
                value=cfg.FEATEXT_METHODS[0]
            )
        ], style={'width':'15%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Num. points FFT'),
            dcc.Dropdown(
                id='dropdown-featext_n_fft',
                options=[256, 512, 1024],
                value=256
            )
        ], style={'width':'15%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Window length'),
            dcc.Dropdown(
                id='dropdown-featext_win_length',
                options=[256, 512, 1024],
                value=256
            )
        ], style={'width':'15%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Hop length'),
            dcc.Dropdown(
                id='dropdown-featext_hop_length',
                options=[256, 512, 1024],
                value=256
            )
        ], style={'width':'15%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            html.Label('Num. mels'),
            dcc.Dropdown(
                id='dropdown-featext_n_mels',
                options=[256, 512, 1024],
                value=256
            )
        ], style={'width':'15%', 'padding':5, 'display':'inline-block'}),
        html.Div([
            dcc.Graph(id='wave-plot')
        ]),
    ])
], style={'width':1200, 'padding-left':50, 'padding-right':50})


@app.callback(
    Output('dropdown-file_name', 'options'),
    Input('dropdown-class', 'value'))
def update_dropdown_file_name(class_name):
    options = df['file_name'].loc[df['class'] == class_name]
    return [{'label':s, 'value':s} for s in options]


@app.callback(
    Output('audio-player', 'src'),
    Input('audio-player', 'src'),
    Input('dropdown-class', 'value'),
    Input('dropdown-file_name', 'value'))
def update_audio_player(audio_src, file_class, file_name):
    if (file_class is None) or (file_name is None):
        return ''
    else:
        file_path = 'dataset/' + file_class + '/' + file_name
        audio_player_dir = 'assets/audio-player/tmp/'
        audio_player_src = audio_player_dir + file_class + '__' + file_name
        if audio_player_src != audio_src:
            if os.path.exists(file_path):
                [os.remove('assets/audio-player/tmp/' + s) for s in os.listdir(audio_player_dir)]
                shutil.copy(file_path, audio_player_src)
        return audio_player_src


@app.callback(
    Output('wave-plot'                 , 'figure'),
    Input('dropdown-class'             , 'value'),
    Input('dropdown-file_name'         , 'value'))
def update_wave_plot(file_class, file_name):
    fig = go.Figure()
    fig.update_layout(
        title='Wave',
        xaxis_title='time (s)',
        yaxis_title='wave',
        margin=dict(l=20, r=20, t=30, b=30),
        height=200)
    if (file_class is None) or (file_name is None):
        return fig
    else:
        file_path = 'dataset/' + file_class + '/' + file_name
        if os.path.exists(file_path):
            wave, sample_rate = torchaudio.load(file_path)
            fig.add_trace(
                go.Scatter(
                    x=torch.arange(wave.shape[1])/sample_rate, 
                    y=wave[0,:], 
                    mode='lines')
            )
        return fig


# @app.callback(
#     Output('wave-plot'                 , 'figure'),
#     Input('dropdown-class'             , 'value'),
#     Input('dropdown-file_name'         , 'value'),
#     Input('dropdown-featext_method'    , 'value'),
#     Input('dropdown-featext_n_fft'     , 'value'),
#     Input('dropdown-featext_win_length', 'value'),
#     Input('dropdown-featext_n_mels'    , 'value'))



if __name__ == '__main__':
    app.run_server(debug=True, dev_tools_hot_reload=False)