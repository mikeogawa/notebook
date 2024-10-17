import os
import json
import string
from dataclasses import dataclass, field
from typing import Self
from .core.utils import (
    read_file,
    read_csv,
    read_yaml,
    write_file,
)

DATA_PATH = "data"
TO_WRITE_PATH = "tmp/temp_data"
TO_HUGO_PATH = "hugo_site"

TO_LAYOUT_PATH = os.path.join(TO_HUGO_PATH, "layouts")
TO_CONTENT_PATH = os.path.join(TO_HUGO_PATH, "content")
TO_DATA_PATH = os.path.join(TO_HUGO_PATH, "data")
TO_WRITE_PAGE_PATH = os.path.join(TO_WRITE_PATH, "page.json")
TO_WRITE_POST_PATH = os.path.join(TO_WRITE_PATH, "posts.json")
CMS_PAGE_TO_HTML = os.path.join(DATA_PATH, "cms_page_to_html_allocation.csv")
SETTINGS_YAML_PATH = os.path.join(DATA_PATH, "settings.yaml")
LAYOUT_DISABLE_INDICATOR = "with .Site.Data"


def get_csv_dict() -> list[dict]:
    dict_list = read_csv(CMS_PAGE_TO_HTML)
    return {d["page_name"]: d["target_layout_html"] for d in dict_list}


def get_common_page_name(settings_dict: dict) -> str:
    return settings_dict["common_page_name"]


def get_first_section_for_post(settings_dict: dict) -> str:
    POST_SECTION = "post_section"
    post_section_list = settings_dict[POST_SECTION]
    return (
        post_section_list[0]["section"] 
        if post_section_list else ""
    )


settings_dict = read_yaml(SETTINGS_YAML_PATH)
CMS_TO_LAYOUT_ALLOCATION = get_csv_dict()
COMMON_PAGE_NAME = get_common_page_name(settings_dict)
POST_SECTION = get_first_section_for_post(settings_dict)
PAGE_TEMPLATE = read_file("templates/layouts/page.html")


@dataclass
class CmsContent:
    key: str
    name: str
    type: str
    value: str
    locale: str

    @classmethod
    def from_dict(
        cls, kantan_cms_post_dict: dict
    ) -> Self:
        return cls(
            key=kantan_cms_post_dict["key"],
            name=kantan_cms_post_dict["name"],
            type=kantan_cms_post_dict["type"],
            value=kantan_cms_post_dict["value"],
            locale=kantan_cms_post_dict["locale"],
        )


@dataclass
class CmsPost:
    id: str
    name: str
    date: str
    public: bool
    contents: list[CmsContent]
    _md_content: str = field(init=False)

    @classmethod
    def from_dict(
        cls, kantan_cms_post_dict: dict
    ) -> Self:
        return cls(
            id=kantan_cms_post_dict["id"],
            name=kantan_cms_post_dict["name"],
            date=kantan_cms_post_dict["date"],
            public=kantan_cms_post_dict["public"],
            contents=list(map(
                CmsContent.from_dict, 
                kantan_cms_post_dict["content"]
            )),
        )

    def override_md_content(self):
        front_matter = {c.key: c.value for c in self.contents}
        md_content = front_matter.pop("content")

        self._md_content = "\n".join([
            "---",
            "\n".join([f"{k}: {v}" for (k, v) in front_matter.items()]),
            "---",
            md_content
        ])

    def to_target_post(self):
        content_path = os.path.join(
            TO_CONTENT_PATH, POST_SECTION, f"{self.id}.md"
        )
        write_file(content_path, self._md_content)
    

@dataclass
class CmsPage:
    id: str
    name: str
    content: list[CmsContent]
    _yml_content: str = field(init=False)
    _replace_layout: str = field(init=False)

    @classmethod
    def from_dict(
        cls, kantan_cms_post_dict: dict
    ) -> Self:
        return cls(
            id=kantan_cms_post_dict["id"],
            name=kantan_cms_post_dict["name"],
            content=list(map(
                CmsContent.from_dict, 
                kantan_cms_post_dict["contents"]
            )),
        )

    def is_common_page(self) -> bool:
        return self.name == COMMON_PAGE_NAME

    def append_content_from_page(self, page: Self | None):
        if not page:
            return
        self.content.extend(page.content)

    def set_yml_content(self):
        self._yml_content = "\n".join([
            f"{content.key}: '{content.value}'"
            for content in self.content
        ])

    def set_wrap_hugo_layout(self):
        layout_html = CMS_TO_LAYOUT_ALLOCATION.get(self.name, None)
        layout = read_file(os.path.join(TO_LAYOUT_PATH, layout_html))
        if LAYOUT_DISABLE_INDICATOR in layout:
            self._replace_layout = layout
            return
        self._replace_layout = string.Template(PAGE_TEMPLATE).safe_substitute(
            {"name": self.name, "inside": layout}
        )

    def create_hugo_data(self):
        write_file(
            os.path.join(TO_DATA_PATH, f"{self.name}.yaml"),
            self._yml_content
        )

    def replace_hugo_layout(self):
        layout_html = CMS_TO_LAYOUT_ALLOCATION.get(self.name, None)
        write_file(
            os.path.join(TO_LAYOUT_PATH, layout_html),
            self._replace_layout
        )


def cms_page_to_hugo():
    json_dict = json.loads(read_file(TO_WRITE_PAGE_PATH))
    data = list(map(CmsPage.from_dict, json_dict["pages"]))
    commona_page = next(filter(lambda x: x.is_common_page(), data), None)
    for d in data:
        d.append_content_from_page(commona_page)
        d.set_yml_content()
        d.set_wrap_hugo_layout()
        d.create_hugo_data()
        d.replace_hugo_layout()


def cms_post_to_hugo():
    json_dict = json.loads(read_file(TO_WRITE_POST_PATH))
    data = list(map(CmsPost.from_dict, json_dict["posts"]))
    for d in data:
        d.override_md_content()
        d.to_target_post()


if __name__ == "__main__":
    cms_page_to_hugo()
    cms_post_to_hugo()
