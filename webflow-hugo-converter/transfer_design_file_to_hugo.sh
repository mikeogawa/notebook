#!/bin/bash
set -e

python3 -m scripts.html_to_hugo.init_process
python3 -m scripts.html_to_hugo.create_temp_design_file
python3 -m scripts.html_to_hugo.copy_to_temp_design_file
python3 -m scripts.html_to_hugo.format_at_temp_design_file
python3 -m scripts.html_to_hugo.move_files_at_temp_design
python3 -m scripts.html_to_hugo.generate_markdown_files
python3 -m scripts.html_to_hugo.transfer_to_layouts
python3 -m scripts.html_to_hugo.create_partials_at_layout
# python3 -m scripts.html_to_hugo.remove_temp_design_file