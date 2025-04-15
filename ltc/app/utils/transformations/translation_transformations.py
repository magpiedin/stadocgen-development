from pathlib import Path
import pandas as pd
import shutil
import globals
import glob
import yaml

# Script to transform the translations source file
# Columns are grouped by language tag suffix, then each groupm is copied to a separate file.
# Important! Columns in the output translation file must match the columns in the default source file to render properly (ignorring the language tag
# appended to each file


namespace = 'ltc'
current_dir = Path().absolute()
root_dir = globals.get_project_root()
project_dir = str(root_dir) +'/'+namespace+'/app'
translations_yml = str(root_dir)+'/'+namespace+'/app/utils/translations.yml'


# Read translations YAML file
yml_dict = []
for yf in glob.glob(translations_yml, recursive=True):
    with open(yf, 'r') as f:
        meta_dict = yaml.load(f, Loader=yaml.FullLoader)
        yml_dict.append(meta_dict)

df_yml = pd.DataFrame.from_dict(yml_dict)


# -------------------------------------------------------
# Create copies
translations_src = str(project_dir)+'/data/sources/latimer-translations.csv'
translations_csv = str(project_dir)+'/data/output/ltc-termlist.csv'
shutil.copy(translations_src, translations_csv)


