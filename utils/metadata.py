import os
import pandas as pd
import torch
import torchaudio

def build_metadata(dir):
    class_names = os.listdir(dir) # a class per folder
    file_names = [os.listdir(os.path.join(dir, subdir)) for subdir in class_names]
    # build basic metadata dataframe including class and file_name
    df_dict = {}
    for c, class_name in enumerate(class_names):
        df_len = len(file_names[c])
        df_dict[class_name] = pd.DataFrame({
            'class': [class_name] * df_len,
            'file_name': file_names[c]
        })
    df = pd.concat([df_dict[class_name] for class_name in class_names], ignore_index=True)
    # calculate paths based on class and file_name
    df['file_path'] = 'dataset/' + df['class'] + '/' + df['file_name']
    # new columns with names matching torchvision.info attributes
    file_infos = [torchaudio.info(file_path) for file_path in df['file_path']]
    df['sample_rate'] = [file_info.sample_rate for file_info in file_infos]
    df['num_channels'] = [file_info.num_channels for file_info in file_infos]
    df['num_frames'] = [file_info.num_frames for file_info in file_infos]
    df['bits_per_sample'] = [file_info.bits_per_sample for file_info in file_infos]
    df['encoding'] = [file_info.encoding for file_info in file_infos]
    # calculate duration
    df['duration'] = df['num_frames'] / df['sample_rate']
    # calculate power
    pows = torch.zeros(len(df))
    for i, file_path in enumerate(df['file_path']):
        waveform, sample_rate = torchaudio.load(file_path)
        meanval = waveform.mean()
        pows[i] = ((waveform - meanval)**2.0).mean().item()
    df['power'] = pows

    return df