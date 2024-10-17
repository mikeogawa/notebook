
import os
import glob
from pathlib import Path
from .const import (
    TEMP_DESIGH_PATH,
    TEMPLATE_PAGE_PATH,
    TO_HUGO_PATH,
    DATA_PATH,
    DataFileName,
)
from .utils import (
    read_file,
    write_file,
    read_yaml,
    get_post_section,
)


SETTINGS_YML = read_yaml(os.path.join(
    DATA_PATH, 
    DataFileName.SETTINGS,
))
TEMPLATE_PAGE = read_file(TEMPLATE_PAGE_PATH)
TO_CONTENT_PATH = os.path.join(TO_HUGO_PATH, "content")
MOVE_FILE_MAPPING = get_post_section(SETTINGS_YML)
TARGET_HTML = "target_html"


def get_avoid_html_from_posts() -> list[str]:
    avoid_files = []
    for row in MOVE_FILE_MAPPING:
        avoid_files.append(row[TARGET_HTML])
    return avoid_files


def get_create_html_from_posts() -> list[str]:
    create_files = []
    for row in MOVE_FILE_MAPPING:
        if Path(row[TARGET_HTML]).name == "list.html":
            create_files.append(row[TARGET_HTML])
    return create_files


def get_all_design_htmls():
    globbed_design_files = glob.glob(
        os.path.join(TEMP_DESIGH_PATH, "**", "*"),
        recursive=True
    )
    globbed_design_files_html_only = filter(
        lambda x: x.endswith(".html"),
        globbed_design_files
    )
    return list(
        map(
            lambda x: os.path.relpath(x, TEMP_DESIGH_PATH),
            globbed_design_files_html_only
        )
    )


def allow_non_moved_files(all_design_htmls: list[str]) -> list[str]:
    avoid_files = get_avoid_html_from_posts()
    return list(filter(lambda x: x not in avoid_files, all_design_htmls))


def split_to_page_and_sections(
        all_design_htmls: list[str]) -> tuple[list[str], list[str]]:
    design_page_html = []
    design_section_html = []
    for html in all_design_htmls:
        if "/" not in html:
            design_page_html.append(html)
        else:
            design_section_html.append(html)
    return design_page_html, design_section_html


def generate_markdown_pages(design_page_html: list[str]):

    for html in design_page_html:
        if html == "index.html":
            continue
        target_md = str(Path(html).with_suffix(".md"))
        write_file(
            os.path.join(TO_CONTENT_PATH, target_md),
            TEMPLATE_PAGE.format(
                layout=str(Path(html).with_suffix(""))
            )
        )


def generate_layout_sections(design_section_html: list[str]):
    for html in design_section_html:
        path_html = Path(html)
        target_md = (
            str(path_html.with_name("_index.md"))
            if path_html.name == "index.html" else
            str(path_html.with_suffix(".md"))
        )
        layout_target_html_w_parent = path_html.with_suffix("")
        layout_target_html = Path(
            *layout_target_html_w_parent.parts[1:]
        )
        write_file(
            os.path.join(TO_CONTENT_PATH, target_md),
            TEMPLATE_PAGE.format(
                layout=str(layout_target_html)
            )
        )


def generate_posts():
    post_htmls = get_create_html_from_posts()
    for post_html in post_htmls:
        corr_html = Path(post_html)
        index_md = corr_html.with_name("_index.md")
        write_file(
            os.path.join(TO_CONTENT_PATH, index_md),
            ""
        )


if __name__ == "__main__":
    all_design_htmls = get_all_design_htmls()
    all_design_htmls = allow_non_moved_files(all_design_htmls)
    (
        design_page_html,
        design_section_html,
    ) = split_to_page_and_sections(all_design_htmls)
    generate_markdown_pages(design_page_html)
    generate_layout_sections(design_section_html)
    generate_posts()