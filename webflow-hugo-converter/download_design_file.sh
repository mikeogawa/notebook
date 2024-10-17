#!/bin/bash
set -e

set -a
source .env
set +a

python3 -m scripts.download.download_from_webflow

rm -rf design_file

unzip tmp/design_file.zip -d design_file

rm design_file