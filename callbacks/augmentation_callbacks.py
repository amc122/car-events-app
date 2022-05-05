import time
import os
import shutil
from tqdm import tqdm
import zipfile
from dash import Input, Output, State
from dash import html, dcc, dash_table
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc

from AudioDataAugmentator import AudioDataAugmentator


AUGMENTATION_READABLE_ARGS_DICT = {
    'arg-white_noise_snr'            : 'SNR (dB)',
    'arg-background_noise_snr'       : 'SNR (dB)',
    'arg-background_noise_class'     : 'Background class',
    'arg-gain_factor'                : 'Gain factor',
    'arg-time_shift_max_shift'       : 'Maximum shift',
    'arg-time_shift_shift_direction' : 'Shift direction',
    'arg-pitch_fractional_steps'     : 'Fractional steps',
    'arg-speed_factor'               : 'Speed factor'
}

AUGMENTATION_READABLE_METHODS_DICT_R = {
    'White noise'      : 'noise_injection',
    'Background noise' : 'background_injection',
    'Gain'             : 'gain_change',
    'Time shift'       : 'time_shift',
    'Pitch'            : 'pitch_change',
    'Speed'            : 'speed_change'
}


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


def _background_noise_children(background_classes):
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
                        options=background_classes,
                        value=None
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
                    html.Label('Shift direction'),
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


# this is a format adapter for the augmentation_list
# TODO: modify AudioDataAugmentator so that no wrapper is needed
def _ada_augmentation_sequence(augmentation_list):
    sequence = []
    for ae in augmentation_list:
        m = list(ae.keys())[0] # the method (this is a string)
        a = list(ae.values())[0] # the arguments (this is a dict)
        # TODO: the following line needs to be generalized...
        if AUGMENTATION_READABLE_METHODS_DICT_R[m] == 'noise_injection':
            sequence += [[AUGMENTATION_READABLE_METHODS_DICT_R[m], [av for av in a.values()] + ['white']]] # assume correct argument ordering...
        else:
            sequence += [[AUGMENTATION_READABLE_METHODS_DICT_R[m], [av for av in a.values()]]] # assume correct argument ordering...
    return sequence


def _zipdir(root, folds, ziph):
    print('Compressing data...')
    for fold in folds:
        print('Compressing {}...'.format(fold))
        for file in tqdm(os.listdir(os.path.join(root, fold))):
            source_path = os.path.join(root, fold, file)
            ziph.write(source_path, os.path.relpath(source_path, os.path.join(root, '..')))


def _rmdir(dir):
    assert dir != '/'
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    os.rmdir(dir)


def augmentation_callbacks(app, cfg):

    @app.callback(
        Output('content-augmentation_arguments', 'children'),
        Input('dropdown-augmentation_method', 'value'),
        State('memory-background_classes', 'data'))
    def update_augmentation_arguments(method, background_classes):
        if method == 'White noise':
            return _white_noise_children()
        elif method == 'Background noise':
            return _background_noise_children(background_classes)
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
        Output('memory-augmentation_list', 'data'),
        Output('content-augmentation_list', 'children'),
        Output('alert-augmentation', 'children'),
        Output('submit-augmentation_add2list', 'n_clicks'),
        Output('submit-augmentation_clear_list', 'n_clicks'),
        State('memory-augmentation_list', 'data'),
        State('dropdown-augmentation_method', 'value'),
        State('content-augmentation_arguments', 'children'),
        Input('submit-augmentation_add2list', 'n_clicks'),
        Input('submit-augmentation_clear_list', 'n_clicks'))
    def update_augmentation_list(augmentation_list, method, all_args, n_clicks_add, n_clicks_clear):
        
        if n_clicks_add is None:
            n_clicks_add = 0
        if n_clicks_clear is None:
            n_clicks_clear = 0

        do_add = n_clicks_add > 0
        do_clear = n_clicks_clear > 0

        if do_add:
            new_augmentation_list = augmentation_list
        else:
            new_augmentation_list = []
            content_augmentation_list = []
        alert = []

        if do_add:
            if (method is not None) and (all_args is not None):
                aux = all_args['props']['children'][0]['props']['children']
                n_args = len(aux)
                kwargs = {}
                for i in range(n_args):
                    aux2 = aux[i]['props']['children'][0]['props']['children'][1]['props']
                    if 'value' in aux2.keys():
                        kwargs[aux2['id']] = aux2['value']
                    else:
                        kwargs['_'] = None

                # execute only if argument fields are filled with not None values
                if not any(kwargs[key] is None for key in kwargs.keys()):
                    new_augmentation_list += [{method:kwargs}]
            
                else:
                    alert = dbc.Alert('Please, fill all the input fields', color='warning')
            
            content_augmentation_list = []
            for i, ae in enumerate(new_augmentation_list):
                m = list(ae.keys())[0]
                a = list(ae.values())[0]
                content_augmentation_list += [dbc.Row([
                    dbc.Col([
                        html.B(f'{i+1}: {m}'),
                        html.Div(
                            [dbc.Row([ dbc.Col(AUGMENTATION_READABLE_ARGS_DICT[ka]), dbc.Col(f'{va}') ]) for ka, va in a.items()],
                            style={'width':'50%'}
                        ),
                        html.Br()
                    ])
                ])]

        return new_augmentation_list, content_augmentation_list, alert, 0, 0


    @app.callback(
        Output('download-data_augmented_zip', 'data'),
        State('memory-classifier_classes', 'data'),
        State('memory-augmentation_classes', 'data'),
        Input('submit-get_augmented_dataset', 'n_clicks'),
        prevent_initial_call=True)
    def get_augmented_dataset(classifier_classes, augmentation_classes, n_clicks):
        if n_clicks is None:
            return None
        else:
            # compress the dataset
            classifier_folds = classifier_classes
            augmentation_folds = [ac + '_augmented' for ac in augmentation_classes]
            folds = classifier_folds + augmentation_folds
            with zipfile.ZipFile('dataset.zip', 'w', zipfile.ZIP_DEFLATED) as zipf:
                _zipdir(cfg.DATASET_PATH, folds, zipf)
            # download the dataset

            return dcc.send_file('dataset.zip')


    @app.long_callback(
        Output('alert-augmentation_process', 'children'),
        State('memory-augmentation_classes', 'data'),
        State('memory-augmentation_list', 'data'),
        Input('submit-augmentation_start', 'n_clicks'),
        running=[
            (Output('submit-augmentation_start', 'disabled'), 
                True, False),
            (Output('progress-augmentation', 'style'), 
                {'visibility':'visible'}, {'visibility':'hidden'})
        ],
        progress=[
            Output('progress-augmentation', 'value'),
            Output('progress-augmentation', 'max')
        ],
        prevent_initial_call=True)
    def start_augmentation(set_progress, augmentation_classes, augmentation_list, n_clicks):
        condition_init = n_clicks is not None
        alert_before = dbc.Alert('Press \"Start data augmantation\" once the data augmentation list is completed', color='info')
        alert_after = dbc.Alert('Audio data augmentation done!', color='success')
        if condition_init:
            n_clicks_aux = n_clicks
        else:
            n_clicks_aux = 0
        condition_run = n_clicks_aux >= 1
        condition = condition_init | condition_run
        if not condition:
            if not condition_init:
                alert_content = alert_before
            else: # i.e. nore than one click
                alert_content = alert_after
        else:
            # clean previously augmented data
            for ac in augmentation_classes:
                dir_to_delete = os.path.join(cfg.DATASET_PATH, ac + '_augmented')
                if os.path.isdir(dir_to_delete):
                    _rmdir(dir_to_delete)
            # do the augmentation
            ada = AudioDataAugmentator(16000, 1000)
            ada_manipulation_sequence = _ada_augmentation_sequence(augmentation_list)
            ada.load_background(cfg.DATASET_PATH, ada_manipulation_sequence)
            for i, class_name in enumerate(augmentation_classes):
                ada.set_dirpath(cfg.DATASET_PATH, class_name)
                print(f'Doing data augmentation on {class_name} files...')
                ada.augment(ada_manipulation_sequence)
                set_progress((str(i+1), str(len(augmentation_classes))))
            alert_content = alert_after
        return alert_content, True


    # @app.callback(
    #     Output('dummy', 'value'),
    #     State('memory-augmentation_classes', 'data'),
    #     State('memory-background_classes', 'data'),
    #     Input('submit-augmentation_add2list', 'n_clicks'))
    # def display_index_cache(augmentation_classes, background_classes, n_clicks):
    #     return 0
    
