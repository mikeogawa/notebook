#!/bin/bash
set -e

set -a
source .env
set +a


CMS_TOKEN=$(python3 -m scripts.cms_to_hugo.authenticate_local)
export CMS_TOKEN
# python3 -m scripts.cms_to_hugo.get_data_from_cms
python3 -m scripts.cms_to_hugo.cms_to_hugo_content
# python3 -m scripts.cms_to_hugo.remove_temp_cms_file