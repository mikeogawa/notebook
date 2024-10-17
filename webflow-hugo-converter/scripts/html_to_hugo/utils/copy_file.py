import os
import shutil


def copy_file(from_path: str, to_path: str):
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    shutil.copy(from_path, to_path)
