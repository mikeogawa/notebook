from enum import Enum
import os
import csv
from dataclasses import dataclass, field
from typing import List, Optional, Self
from .utils import read_file

TEMPLATE_POST_PATH = "templates/content/post.md"
TEMPLATE_POST = read_file(TEMPLATE_POST_PATH)

@dataclass
class KantanCmsPostContent:
    key: str
    name: str
    type: str
    value: str
    locale: str


@dataclass
class KantanCmsPost:
    id: str
    name: str
    date: str
    public: bool
    content: list[KantanCmsPostContent]
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
            content=list(map(
                lambda x: KantanCmsPostContent.from_dict(**x), 
                kantan_cms_post_dict["content"]
            )),
        )
