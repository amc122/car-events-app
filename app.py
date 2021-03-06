import os
import sys
import shutil
import pandas as pd
import torch
import torchaudio
import plotly
import plotly.express as px

from plotly.subplots import make_subplots

from dash import Dash, html, dcc, Input, Output
from dash.long_callback import DiskcacheLongCallbackManager
from dash_bootstrap_components import themes
import diskcache

#from flask_caching import Cache

import config.default as cfg
import views
import callbacks
from utils import extract, metadata, featext


sys.setrecursionlimit(1500)


cache = diskcache.Cache('./cache')
long_callback_manager = DiskcacheLongCallbackManager(cache) # TODO: move to Celery
app = Dash(__name__, 
    title='Audio data preprocessing',
    external_stylesheets=[themes.BOOTSTRAP],
    long_callback_manager=long_callback_manager)
#app._favicon = ('favicon.ico')
app.config['suppress_callback_exceptions'] = True


server = app.server


# TODO: move app setup to a different file
cfg.CLASS_NAMES = [
    'Safety_Noise', 'Safety_Negatives', 'Music_Background', 'CrashSWP', 'Tire'
]
def setup(cfg):
    compressed_file_names, hash = extract.select_dataset_version(cfg.CLASS_NAMES, cfg.DATASET_VERSION)
    print('Extracting audio waves...', end='')
    extract.extract_waves(cfg.COMPRESSED_DATA_DIR, compressed_file_names, cfg.DATASET_PATH, hash)
    print(' done')
    print('Building metadata...', end='')
    df = metadata.build_metadata(cfg)
    print(' done')
    return df

#####################
# metadata (static) #
#####################

df = setup(cfg)

legend = dict(title='', orientation='h', y=-0.50)
margin = dict(l=20, r=20, t=30, b=30)
height = 420

fig_class_histogram = px.histogram(df, x='class', color='class', title='Class histogram')
fig_class_histogram.update_layout(legend=legend, margin=margin, height=height)

fig_duration_histogram = px.histogram(df, x='duration', color='class', title='Duration histogram', histnorm='probability density')
fig_duration_histogram.update_layout(legend=legend, margin=margin, height=height)

fig_power_histogram = px.histogram(df, x='power', color='class', title='Power histogram', histnorm='probability density')
fig_power_histogram.update_layout(legend=legend, margin=margin, height=height)


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    views.common.storage(),
    html.Div(id='page-content')
])

index_layout = views.index_view(
    fig_class_histogram=fig_class_histogram, 
    fig_duration_histogram=fig_duration_histogram, 
    fig_power_histogram=fig_power_histogram,
    class_names=cfg.CLASS_NAMES, 
    file_names=df['file_name'].loc[df['class'] == cfg.CLASS_NAMES[0]], 
    featext_methods=featext.FEATEXT_METHODS
)
augmentation_layout = views.augmentation_view(cfg.AUGMENTATION_METHODS)



callbacks.index_callbacks(app, cfg, df)
callbacks.augmentation_callbacks(app, cfg)

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return index_layout
    elif pathname == '/augmentation':
        return augmentation_layout
    else:
        return index_layout





if __name__ == '__main__':
    app.run_server(
        host='0.0.0.0',
        port='8050',
        debug=True,
        dev_tools_hot_reload=False)