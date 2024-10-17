import os
import glob
from dataclasses import dataclass, field
import re
from bs4 import BeautifulSoup
from .const import DATA_PATH, TEMP_DESIGH_PATH
from .utils import (
    read_file,
    write_file,
    read_yaml,
)

SETTING_PATH = os.path.join(DATA_PATH, "settings.yaml")
UGLY_ALLOW_KEY = "ugly_urls"

SETTING = read_yaml(SETTING_PATH)
UGLY_ALLOW = SETTING[UGLY_ALLOW_KEY]
PARTIAL_FILE_NAMES = [
    "footer.html",
    "header.html",
    "head.html",
]


class TARGET_TAGS:
    link = 'link'
    script = 'script'
    header = 'head'
    img = 'img'
    a = 'a'


class IMAGE_ATTR:
    src = 'src'
    srcset = 'srcset'


PARTIAL_HEAD_TEXT = "{{ partial \"$partial\" . }}"


def replace_ugly_to_clean_html(path: str) -> str:
    return (
        (not UGLY_ALLOW and path.endswith(".html"))
        and path.replace(".html", "/")
        or path
    )


def add_rel_link(path: str) -> str:
    # return path
    return f'"{path}"|relURL'


def create_partial_header_text(partial_name: str) -> str:
    return PARTIAL_HEAD_TEXT.replace("$partial", partial_name)


@dataclass
class HtmlToHugoConverter:
    """Converter for converting html file to hugo html file."""

    file_path: str
    soup: BeautifulSoup = field(init=False)
    soup_str: str = field(init=False)

    def adjust_link(self, path: str) -> str:
        return (
            (not UGLY_ALLOW and "index.html" not in self.file_path)
            and re.sub(r"^\.\./", "../../", path)
            or path
        )

    def get_beautiful_soup(self):
        html_content = read_file(self.file_path)
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def modify_to_rel_link(self, path):
        src_value = self.adjust_link(path)
        rel_link = add_rel_link(src_value)
        return "{{%s}}" % rel_link

    def _add_rel_url_to_href(self, tag_name: str):
        soup = self.soup
        for tag in soup.find_all(tag_name, href=True):
            href_value = tag["href"]
            if "https://" in href_value or "http://" in href_value:
                continue
            href_value = href_value.replace("index.html", "/")
            href_value = replace_ugly_to_clean_html(href_value)
            tag['href'] = self.modify_to_rel_link(href_value)

    def _add_rel_url_to_src(self, tag_name: str):
        soup = self.soup
        for tag in soup.find_all(tag_name, src=True):
            src_value = tag["src"]
            tag['src'] = self.modify_to_rel_link(src_value)

    def _add_rel_url_to_src_image_el(self, tag_name: str):
        attr = IMAGE_ATTR.src
        soup = self.soup
        for tag in soup.findAll(tag_name):
            src_value = tag.get(attr, None)
            if not src_value or "images/" not in src_value:
                continue
            tag[attr] = self.modify_to_rel_link(src_value)

    def _add_rel_url_to_src_image_el_src_set(self, tag_name: str):

        attr = IMAGE_ATTR.srcset
        soup = self.soup
        for tag in soup.findAll(tag_name):
            src_value = tag.get(attr, None)
            if not src_value or "images/" not in src_value:
                continue
            tag[attr] = "" + ", ".join(list(map(
                self.modify_to_rel_link,
                src_value.split(", ")
            )))

    def soup_stringify(self):
        soup = self.soup
        self.soup_str = soup.prettify()

    def remove_css_comments(self):
        soup_str = self.soup_str
        self.soup_str = re.sub(r'/\*.+?\*/', '', soup_str, flags=re.DOTALL)

    def remove_xml_declaration_from_soup_str(self):
        soup_str = self.soup_str
        self.soup_str = re.sub(r'<\?.+?\?>', '', soup_str, flags=re.DOTALL)

    def replace_blank_action(self):
        soup_str = self.soup_str
        self.soup_str = re.sub(r'http://blank', '#', soup_str, flags=re.DOTALL)

    def save_soup_at_file(self):
        soup_str = self.soup_str
        write_file(self.file_path, soup_str)

    def add_rel_url_to_tags(self):
        """Add relURL to href."""

        self._add_rel_url_to_href(TARGET_TAGS.link)
        self._add_rel_url_to_src(TARGET_TAGS.script)
        self._add_rel_url_to_href(TARGET_TAGS.a)
        self._add_rel_url_to_src_image_el(TARGET_TAGS.img)
        self._add_rel_url_to_src_image_el_src_set(TARGET_TAGS.img)

    def add_hugo_partials_inside_tag(
            self, tag: str, partial_text: str, first: bool = False,
    ):
        """Add text to tag.

        Args:
            text (str): Text.
            tag (str): Tag.
        """
        soup = self.soup
        tags = soup.find_all(tag)
        if not tags:
            return

        # タグにテキストを追加
        for header in tags:
            if first:
                header.insert(0, partial_text)
            else:
                header.append(partial_text)

        self.soup = soup

    def add_paritals(self):
        self.add_hugo_partials_inside_tag(
            "head", create_partial_header_text("head.html"), first=False
        )
        self.add_hugo_partials_inside_tag(
            "body", create_partial_header_text("header.html"), first=True
        )
        self.add_hugo_partials_inside_tag(
            "body", create_partial_header_text("footer.html"), first=False
        )
        # print(f"Add {text} to {tag} in {self.file_path}.")

    def convert_html_to_hugo(self):
        """Convert html file to hugo file."""
        self.get_beautiful_soup()
        self.add_rel_url_to_tags()
        self.add_paritals()
        self.soup_stringify()
        self.remove_css_comments()
        self.save_soup_at_file()


def get_all_temp_files():
    return sorted(glob.glob(
            os.path.join(TEMP_DESIGH_PATH, "**", "*.html"),
            recursive=True
        ))


if __name__ == "__main__":
    for path in get_all_temp_files():
        converter = HtmlToHugoConverter(path)
        converter.convert_html_to_hugo()