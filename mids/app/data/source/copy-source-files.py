import urllib.request
import os
import config as cfg

root_dir = cfg.get_project_root()

download_urls =  [
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/terms/information_elements/mids_information_elements_draft.csv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/terms/mids-levels/MIDS-levels-draft.csv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/abcd/biology/sssom_mids_abcd_biology_02.sssom.tsv",
    "https://raw.githubusercontent.com/tdwg/mids/refs/heads/main/source/mappings/dwc/biology/sssom_mids_dwc_biology_02.sssom.tsv",
]

target_dir = str(root_dir) + '/mids/app/data/source/mids-repo'

for url in download_urls:
    file_name = os.path.basename(url)
    local_path = os.path.join(target_dir, file_name)
    urllib.request.urlretrieve(url, local_path)
