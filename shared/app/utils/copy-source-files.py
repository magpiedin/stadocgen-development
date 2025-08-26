import urllib.request
import os
import config as cfg
import yaml

with open('app/meta.yml') as metadata:
    meta = yaml.safe_load(metadata)
acronym = meta['acronym']
'''
Copies source data files and markdown content files from the source repository (https://github.com/tdwg/mids) to the StaDocGen repository
This script is run manually as a prerequisite to the documentation generator process
'''
root_dir = cfg.get_project_root()

# noinspection PyPackageRequirements
download_urls =  [
    # Source Data File URLs
]
download_md_urls =  [
    # Source Markdown URLs
]
target_dir = str(root_dir) + '/' + acronym + '/app/data/sources'
target_md_dir = str(root_dir) + '/' + acronym + '/app/md'

for url in download_urls:
    file_name = os.path.basename(url)
    local_path = os.path.join(target_dir, file_name)
    urllib.request.urlretrieve(url, local_path)
    print('Downloaded ' + url)

for md_url in download_md_urls:
    md_file_name = os.path.basename(md_url)
    local_md_path = os.path.join(target_md_dir, md_file_name)
    urllib.request.urlretrieve(md_url, local_md_path)
    print('Downloaded ' + md_url)
