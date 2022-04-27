import os
import torch
import torchaudio
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Input, Output, State

from utils import featext


def index_callbacks(app, cfg, df):


    @app.callback(
        Output('dropdown-file_name', 'options'),
        Input('dropdown-class', 'value'))
    def update_dropdown_file_name(class_name):
        options = df['file_name'].loc[df['class'] == class_name]
        return [{'label':s, 'value':s} for s in options]


    @app.callback(
        Output('audio-player', 'src'),
        Input('dropdown-class', 'value'),
        Input('dropdown-file_name', 'value'))
    def update_audio_player(file_class, file_name):
        if (file_class is None) or (file_name is None):
            return ''
        else:
            file_path = os.path.join(cfg.DATASET_PATH, file_class, file_name)
            return file_path


    @app.callback(
        Output('wave-plot'                  , 'figure'),
        Input('dropdown-class'              , 'value'),
        Input('dropdown-file_name'          , 'value'),
        Input('dropdown-featext_method'     , 'value'),
        Input('dropdown-featext_sample_rate', 'value'),
        Input('dropdown-featext_n_fft'      , 'value'),
        Input('dropdown-featext_win_length' , 'value'),
        Input('dropdown-featext_hop_length' , 'value'),
        Input('dropdown-featext_n_filter'   , 'value'),
        Input('dropdown-featext_n_fcc'      , 'value'))
    def update_wave_plot(file_class, file_name, featext_method, sample_rate, n_fft, win_length, hop_length, n_filter, n_fcc):
        fig = make_subplots(rows=2, cols=1,
            specs=[[{'type': 'xy'}], [{'type': 'xy'}]],
            subplot_titles=['Wave', 'Features'],
            row_heights=[240, 240])
        fig.update_layout(
            xaxis_title='time (s)',
            yaxis_title='wave',
            margin=dict(l=20, r=20, t=50, b=50),
            height=480)
        if (file_class is None) or (file_name is None):
            return fig
        else:
            file_path = os.path.join(cfg.DATASET_PATH, file_class, file_name)
            if os.path.exists(file_path):
                wave, sample_rate = torchaudio.load(file_path)
                fig.add_trace(
                    go.Scatter(
                        x=torch.arange(wave.shape[1])/sample_rate, 
                        y=wave[0,:], 
                        mode='lines'),
                    row=1, col=1)

                feature_extractor = featext.get_featext(featext_method, 
                    sample_rate=sample_rate,
                    n_fft=n_fft, 
                    win_length=win_length,
                    hop_length=hop_length,
                    n_filter=n_filter)

                fig.add_trace(
                    go.Heatmap(
                        z=feature_extractor(wave[0,:])),
                    row=2, col=1)
            
            return fig


    @app.callback(
        Output('memory-classifier_classes', 'data'),
        Output('memory-background_classes', 'data'),
        State('checklist-classifier_classes', 'value'),
        State('checklist-background_classes', 'value'),
        Input('submit-index2aug', 'n_clicks'))
    def update_cache_classifier_classes(classifier_classes, background_classes, n_clicks):
        return classifier_classes, background_classes