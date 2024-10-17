import os
import glob
from .utils import copy_file, minify_css, minify_js
from .const import TEMP_DESIGH_PATH, TO_HUGO_PATH

TO_LAYOUTS_PATH = os.path.join(TO_HUGO_PATH, "layouts")
TO_ASSET_PATH = os.path.join(TO_HUGO_PATH, "assets")
TO_STATIC_PATH = os.path.join(TO_HUGO_PATH, "static")


def get_all_design_files() -> list[str]:
    globbed_design_files = filter(
        lambda x: os.path.isfile(x),
        sorted(
            glob.glob(
                os.path.join(TEMP_DESIGH_PATH, "**", "*"),
                recursive=True
            )
        )
    )
    return list(
        map(
            lambda x: os.path.relpath(x, TEMP_DESIGH_PATH),
            globbed_design_files
        )
    )


def extract_htmls(design_files: list[str]) -> list[str]:
    return list(filter(
        lambda x: x.endswith(".html"), design_files
    ))


def extract_assets(design_files: list[str]) -> list[str]:
    return list(filter(
        lambda x: x.endswith((".css", ".js")) and "/" not in x, design_files
    ))
    

def get_remaining_htmls(
        all_design_htmls: list[str], avoid_files: list[str],
) -> list[str]:
    return list(set(all_design_htmls) - set(avoid_files))


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


def copy_to_layout_pages(design_page_html: list[str]):
    for html in design_page_html:
        copy_file(
            os.path.join(TEMP_DESIGH_PATH, html),
            os.path.join(TO_LAYOUTS_PATH, "page", html)
        )


def copy_to_layout_sections(design_section_html: list[str]):
    for html in design_section_html:
        copy_file(
            os.path.join(TEMP_DESIGH_PATH, html),
            os.path.join(TO_LAYOUTS_PATH, html)
        )


def copy_to_assets(design_assets: list[str]):
    for asset in design_assets:
        copy_file(
            os.path.join(TEMP_DESIGH_PATH, asset),
            os.path.join(TO_ASSET_PATH, asset)
        )


def copy_to_static(design_statics: list[str]):
    for static_f in design_statics:
        copy_file(
            os.path.join(TEMP_DESIGH_PATH, static_f),
            os.path.join(TO_STATIC_PATH, static_f)
        )


def minify_js_and_css(design_statics: list[str]):
    for static_f in design_statics:
        static_f_after = os.path.join(TO_STATIC_PATH, static_f)
        if static_f_after.endswith(".js"):
            minify_js(static_f_after)
        if static_f_after.endswith(".css"):
            minify_css(static_f_after)


if __name__ == "__main__":
    design_files = get_all_design_files()
    all_design_htmls = extract_htmls(design_files)
    (
        design_page_html,
        design_section_html,
    ) = split_to_page_and_sections(all_design_htmls)
    copy_to_layout_pages(design_page_html)
    copy_to_layout_sections(design_section_html)
    all_design_assets = extract_assets(design_files)
    copy_to_assets(all_design_assets)
    remaining_files = get_remaining_htmls(
        design_files,
        all_design_htmls + all_design_assets,
    )
    copy_to_static(remaining_files)
    minify_js_and_css(remaining_files)

