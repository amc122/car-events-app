#from glob import glob
import os
import pandas as pd
import torchaudio
from zipfile import ZipFile


def rmdir(dir):
    assert dir != '/'
    for root, dirs, files in os.walk(dir, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


def select_dataset_version(class_names, version):
    df = pd.read_csv(f'config/dataset_versions/{version}.csv')
    df = df.loc[df['class'].isin(class_names)]
    file_names = (df['class'] + '-' + df['version'].astype(str) + '.zip').tolist()
    return file_names


def extract_file(file_path, dest_dir):
    with ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)


def extract_waves(root_dir, file_names, dest_dir):
    if not os.path.exists(dest_dir):
        for file_name in file_names:
            file_path = os.path.join(root_dir, file_name)
            extract_file(file_path, dest_dir)
