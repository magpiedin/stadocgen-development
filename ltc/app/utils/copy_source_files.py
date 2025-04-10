import urllib.request
import os
import config as cfg

"""
Copy LtC source files to local directory. Make sure to run the refresh_terms_source.py script to 
generate the latest terms source file before copying latest files
20250214
"""
root_dir = cfg.get_project_root()

def copy_files():
	download_urls = [
		"https://raw.githubusercontent.com/tdwg/ltc/main/source/terms/ltc_categories.csv",
		"https://raw.githubusercontent.com/tdwg/ltc/main/source/terms/ltc_datatypes.csv",
		"https://raw.githubusercontent.com/tdwg/ltc/main/source/terms/ltc_namespaces.csv",
		"https://raw.githubusercontent.com/tdwg/ltc/main/source/terms/ltc_terms_source.csv",
		"https://raw.githubusercontent.com/tdwg/ltc/main/source/terms/mapping/ltc_sssom_mapping.csv",
	]

	target_dir = str(root_dir) + '/ltc/app/data/sources'

	for url in download_urls:
		file_name = os.path.basename(url)
		local_path = os.path.join(target_dir, file_name)
		print(url + ' --> ' + local_path)
		urllib.request.urlretrieve(url, local_path)

copy_files()