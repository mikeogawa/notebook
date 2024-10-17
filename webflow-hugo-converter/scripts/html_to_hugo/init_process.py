import os
import shutil
from .const import TO_HUGO_PATH, TEMP_DESIGH_PATH


def restart_dir(path: str):
    if os.path.isdir(path):
        shutil.rmtree(path)
        os.makedirs(path)


if __name__ == "__main__":
    if os.path.isdir(TEMP_DESIGH_PATH):
        shutil.rmtree(TEMP_DESIGH_PATH)

    dir_paths = [
        "content", 
        "layouts",
        "assets",
        "static",
        "public"
    ]
    for dir_path in dir_paths:
        restart_dir(os.path.join(TO_HUGO_PATH, dir_path))
