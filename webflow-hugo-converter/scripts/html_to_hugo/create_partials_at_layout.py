import os
from .utils import copy_file, write_file
from .const import TEMPLATE_PATH, TO_HUGO_PATH

TEMPLATE_PARTIAL_PATH = os.path.join(TEMPLATE_PATH, "partial", "header.html")
LAYOUT_PARTIAL_PATH = os.path.join(TO_HUGO_PATH, "layouts", "partials")

PARTIAL_FILE_NAMES = [
    "footer.html",
    "header.html",
    "head.html",
]

if __name__ == "__main__":
    for partial_file_name in PARTIAL_FILE_NAMES:
        from_file = os.path.join(TEMPLATE_PARTIAL_PATH, partial_file_name)
        to_file = os.path.join(LAYOUT_PARTIAL_PATH, partial_file_name)
        if os.path.isfile(from_file):
            copy_file(from_file, to_file)
        else:
            write_file(to_file, "")
