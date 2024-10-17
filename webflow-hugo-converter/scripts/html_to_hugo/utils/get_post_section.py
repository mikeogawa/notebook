import os

POST_SECTION = "post_section"
TEMPLATE = "template"
LIST = "list"
DETAIL = "detail"
TARGET_HTML_K = "target_html"
SOURCE_HTML_K = "src_html"


def get_post_section(settings_dict: dict) -> str:
    res = []
    for s in settings_dict[POST_SECTION]:
        template = s[TEMPLATE]
        res.extend([
            {
                TARGET_HTML_K: os.path.join(s["section"], "list.html"),
                SOURCE_HTML_K: template[LIST]
            },
            {
                TARGET_HTML_K: os.path.join(s["section"], "single.html"),
                SOURCE_HTML_K: template[DETAIL]
            }
        ])
    return res