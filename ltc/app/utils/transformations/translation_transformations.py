from pathlib import Path
import pandas as pd
import shutil
import globals
import glob
import yaml
from functools import reduce

# Script to transform the translations source file
# Columns are grouped by language tag suffix, then each groupm is copied to a separate file.
# Important! Columns in the output translation file must match the columns in the default source file to render properly (ignorring the language tag
# appended to each file


namespace = 'ltc'
current_dir = Path().absolute()
root_dir = globals.get_project_root()
project_dir = str(root_dir) +'/'+namespace+'/app'
translations_src = str(project_dir)+'/data/sources/latimer-translations.csv'
translations_csv = str(project_dir)+'/data/output/ltc-translations.csv'
termlist_source = str(project_dir) + '/data/output/ltc-termlist.csv'
termlist_target = str(project_dir) + '/data/output/ltc-termlist-rev.csv'
termlist_translations_target = str(project_dir) + '/data/output/ltc-translations-termlist.csv'

# Create copies
shutil.copy(translations_src, translations_csv)

# Read translations YAML file
translations_yml = str(root_dir)+'/'+namespace+'/app/utils/translations.yml'
yml_dict = []
for yf in glob.glob(translations_yml, recursive=True):
    with open(yf, 'r') as f:
        meta = yaml.load(f, Loader=yaml.FullLoader)
        yml_dict.append(meta)
df_yml = pd.DataFrame.from_dict(yml_dict)

# -------------------------------------------------------


source_df = pd.read_csv(translations_csv, encoding="utf8", skip_blank_lines=True)
for k in meta['Languages']:

    # Get language tag and filter columns in source translation file
    lang = k['code']
    patterns = [lang+'$', 'term_localName']
    combined_pattern = reduce(lambda x, y: f'{x}|{y}', patterns)
    filtered_df = source_df.filter(regex=combined_pattern)
    filtered_df = filtered_df.fillna('')

    # Local LtC Term List
    terms_df = pd.read_csv(termlist_source, sep=',', encoding='utf-8', skip_blank_lines=True)
    terms_df = terms_df.sort_values(by=['class_name', 'term_local_name'])

    merged_df = pd.merge(left=terms_df, right=filtered_df, how='left', left_on='term_local_name', right_on='term_localName')
    merged_df.to_csv(termlist_translations_target, index=False, encoding='utf8', lineterminator='\r')