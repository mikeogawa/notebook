import glob
import os


def get_all_files(path: str) -> list[str]:
    return list(filter(lambda x: os.path.isfile(x), sorted(glob.glob(path, recursive=True))))