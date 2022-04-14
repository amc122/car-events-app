from zipfile import ZipFile

def extract_waves(source_path, dest_dir):
    with ZipFile(source_path, 'r') as zip_ref:
        zip_ref.extractall(dest_dir)