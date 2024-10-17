import os
from pathlib import Path
import re
from bs4 import BeautifulSoup
from .utils import get_all_files, read_file, write_file

DESIGN_FILE_PATH = "design_file"
DESTINATION_PATH = "tmp/html_text"

GLOB_DESIGN_FILE_PATH = os.path.join(DESIGN_FILE_PATH, "**", "*.html")


def extract_text_from_html(design_html: str) -> str:
    html = read_file(design_html)
    soup = BeautifulSoup(html, "html.parser")
    body = soup.find("body")

    if e := body.find("footer"):
        e.extract()
    if e := body.find(class_="navbar-component"):
        e.extract()

    remove_excess_new_lines = re.sub(
        "\n+", "\n\n", body.get_text()
    )
    return remove_excess_new_lines
    # split_by_new_line = list(filter(bool, remove_excess_new_lines.split("\n")))
    # return "\n".join(split_by_new_line)


def to_target_file(file_path: str) -> str:
    base_name = os.path.relpath(file_path, DESIGN_FILE_PATH)
    return os.path.join(DESTINATION_PATH, Path(base_name).with_suffix(".txt"))


def main():
    design_htmls = get_all_files(GLOB_DESIGN_FILE_PATH)
    for design_html in design_htmls:
        html = extract_text_from_html(design_html)
        target_html = to_target_file(design_html)
        write_file(target_html, html)


if __name__ == "__main__":
    main()
        