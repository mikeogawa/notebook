import os
import json
import requests

TO_WRITE_PATH = "tmp/temp_data"
TO_WRITE_PAGE_PATH = os.path.join(TO_WRITE_PATH, "page.json")
TO_WRITE_POST_PATH = os.path.join(TO_WRITE_PATH, "posts.json")
CMS_TOKEN = os.getenv("CMS_TOKEN", "")
CMS_BASE_URL = os.getenv("CMS_BASE_URL", "")
TENANT_ID = os.getenv("TENANT_ID", "")
PROJECT_ID = os.getenv("PROJECT_ID", "")


def get_headers():
    return {
        "accept": "application/json",
        "tenant-id": TENANT_ID,
        "project-id": PROJECT_ID,
        "Authorization": f"Bearer {CMS_TOKEN}"
    }


def get_params():
    return {
        "lang": "ja"
    }


def get_cms_pages():
    return requests.get(
        f"{CMS_BASE_URL}/v1/api/pages/",
        headers=get_headers(),
        params=get_params(),
    ).json()


def get_cms_posts():
    return requests.get(
        f"{CMS_BASE_URL}/v1/api/posts/",
        headers=get_headers(),
        params=get_params()
    ).json()


def write_json_to_path(path, json_data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(json.dumps(json_data, indent=4))


if __name__ == "__main__":
    write_json_to_path(TO_WRITE_PAGE_PATH, get_cms_pages())
    write_json_to_path(TO_WRITE_POST_PATH, get_cms_posts())