#from glob import glob
import os
from tqdm import tqdm
from hashlib import sha256
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
    os.rmdir(dir)


def select_dataset_version(class_names, version):
    df = pd.read_csv(f'config/dataset_versions/{version}.csv')
    df = df.loc[df['class'].isin(class_names)]
    file_names = (df['class'] + '-' + df['version'].astype(str) + '.zip').tolist()

    dsid = (str(class_names)+str(version)).encode('utf-8')
    hash = sha256(dsid).hexdigest()

    return file_names, hash


def extract_file(file_path, dest_dir):
    with ZipFile(file_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)


def extract_waves(root_dir, file_names, dest_dir, hash=''):
    # check the previous hash
    dataset_id_hash_path = 'cache/dataset_id_hash'
    if os.path.isfile(dataset_id_hash_path):
        with open(dataset_id_hash_path, 'r') as f:
            prev_hash = f.read()
            do_extraction = hash != prev_hash
    else:
        do_extraction = True
    # if the hash has changed, perform the extraction
    if do_extraction:
        with open(dataset_id_hash_path, 'w') as f:
            f.write(hash)
        for file_name in tqdm(file_names):
            file_path = os.path.join(root_dir, file_name)
            extract_file(file_path, dest_dir)
