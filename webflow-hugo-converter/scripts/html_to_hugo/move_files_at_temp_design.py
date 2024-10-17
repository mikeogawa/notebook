import os
from .const import DATA_PATH, TEMP_DESIGH_PATH, DataFileName
from .utils import move_file, read_yaml, get_post_section


SETTINGS_YML = read_yaml(os.path.join(
    DATA_PATH, 
    DataFileName.SETTINGS,
))
HEADERS = ["src_html", "target_html"]
MOVE_FILE_MAPPING = get_post_section(SETTINGS_YML)

if __name__ == "__main__":
    for row in MOVE_FILE_MAPPING:
        origin = os.path.join(TEMP_DESIGH_PATH, row[HEADERS[0]])
        target = os.path.join(TEMP_DESIGH_PATH, row[HEADERS[1]])
        if not os.path.isfile(origin):
            continue
        move_file(origin, target)
