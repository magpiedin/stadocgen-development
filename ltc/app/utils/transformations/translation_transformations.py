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


# Read translations YAML file
translations_yml = str(root_dir)+'/'+namespace+'/app/utils/translations.yml'
yml_dict = []
for yf in glob.glob(translations_yml, recursive=True):
    with open(yf, 'r') as f:
        meta = yaml.load(f, Loader=yaml.FullLoader)
        yml_dict.append(meta)
df_yml = pd.DataFrame.from_dict(yml_dict)

# -------------------------------------------------------
# Create copies
translations_src = str(project_dir)+'/data/sources/latimer-translations.csv'
translations_csv = str(project_dir)+'/data/output/ltc-translations.csv'
shutil.copy(translations_src, translations_csv)


source_df = pd.read_csv(translations_csv, encoding="utf8")
for k in meta['Languages']:

    # Get language tag and filter columns in source translation file
    lang = k['code']
    patterns = [lang+'$', 'term_localName']
    combined_pattern = reduce(lambda x, y: f'{x}|{y}', patterns)
    filtered_df = source_df.filter(regex=combined_pattern)
    filtered_df = filtered_df.fillna('')
    #filtered_df.rename(columns={'term_localName': 'term_local_name'}, inplace=True)

    # Local LtC Term List
    terms_csv = str(project_dir) + '/data/output/ltc-termlist.csv'
    terms_df = pd.read_csv(terms_csv, sep=',', lineterminator='\r', encoding='utf-8',skip_blank_lines=True)
    terms_df = terms_df.replace('\n', '', regex=True)
    terms_df = terms_df.fillna('')
    terms_df = terms_df.sort_values(by=['class_name', 'term_local_name'])

    # Merge Term List with Translations
    #merged_df = pd.merge(terms_df, filtered_df[['term_local_name', 'label_fr', 'definition_fr', 'usage_fr', 'notes_fr']], on="term_local_name", how="inner")

    merged_df = pd.merge(left=terms_df, right=filtered_df, how='left', left_on='term_local_name', right_on='term_localName')

    fr_translations_target = str(project_dir) + '/data/output/' + lang + '_ltc_translations.csv'
    translations_target = str(project_dir) + '/data/output/ltc-termlist.csv'

    # Write Term list with translation to file
    merged_df.to_csv(fr_translations_target, index=False, encoding='utf8', lineterminator='\r', skip_blank_lines=True)
    merged_df.to_csv(translations_target, index=False, encoding='utf8', lineterminator='\r', skip_blank_lines=True)