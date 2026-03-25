import zipfile
from pathlib import Path


def unzip_dir(zip_dir, extract_dir):
    for zip_dir in Path(extract_dir).iterdir():
        with zipfile.ZipFile(zip_dir, "r") as zip_ref:
            zip_ref.extractall(extract_dir)
