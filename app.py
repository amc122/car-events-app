import os
import pandas as pd
import numpy as np
import plotly
import plotly.express as px
import plotly.graph_objects as go

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

df = setup(cfg)
# fig_metadata_table = go.Figure(data=[
#     go.Table(
#         header=dict(
#             values=['Class', 'File name', 'Sample rate', 'Duration'],
#             align='left'),
#         cells=dict(
#             values=[df['class'], df['file_name'], df['sample_rate'], df['duration']],
#             align='left')
#     )
# ])
#fig_class_histogram = px.histogram(df, x='class', color='class', title='Class histogram')
#fig_duration_histogram = px.histogram(df, x='duration', color='class', title='Duration histogram')
#fig_power_histogram = px.histogram(df, x='power', color='class', title='Power histogram')


# TODO: move layout to a different file
app.layout = html.Div([
    html.H1('Audio data explorer'),
    html.Div([
        '''
        A web application for audio data visualization and training with data augmentation
        '''
    ]),
    html.Div([
        html.H2('Data inspection'),
        # html.Div([
        #     dcc.Graph(
        #         id='class-histogram', figure=fig_class_histogram
        #     )
        # ], style={'width':'33%', 'display':'inline-block'}),
        # html.Div([
        #     dcc.Graph(
        #         id='duration-histogram', figure=fig_duration_histogram
        #     )
        # ], style={'width':'33%', 'display':'inline-block'})
    ])
])




if __name__ == '__main__':
    app.run_server(debug=True)