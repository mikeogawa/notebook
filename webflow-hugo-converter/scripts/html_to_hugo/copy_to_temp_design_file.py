import os
import shutil
from .const import FROM_DESIGH_PATH, TEMP_DESIGH_PATH


if __name__ == "__main__":
    if os.path.isdir(TEMP_DESIGH_PATH):
        shutil.rmtree(TEMP_DESIGH_PATH)
    shutil.copytree(FROM_DESIGH_PATH, TEMP_DESIGH_PATH)
