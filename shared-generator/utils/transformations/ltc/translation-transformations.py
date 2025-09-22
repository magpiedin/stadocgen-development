import pandas as pd
import os
import shutil
import yaml
from functools import reduce

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
source_dir = os.path.join(project_root, 'utils', 'sources', 'ltc')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
utils_dir = os.path.join(project_root, 'shared-generator', 'app', 'utils')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
translations_src_path = os.path.join(source_dir, 'latimer-translations.csv')
translations_dest_path = os.path.join(output_dir, 'latimer-translations.csv')
translations_yml_path = os.path.join(utils_dir, 'translations.yml')
termlist_path = os.path.join(output_dir, 'ltc-termlist.csv')

# --- Main Transformation Logic ---
print("Running ltc/translation-transformations...")

# 1. Copy the main translation source file
shutil.copy(translations_src_path, translations_dest_path)

# 2. Read the language configuration
with open(translations_yml_path, 'r') as f:
    lang_meta = yaml.load(f, Loader=yaml.FullLoader)

# 3. Create language-specific translation files
source_df = pd.read_csv(translations_dest_path, encoding="utf8", skip_blank_lines=True)
for lang_info in lang_meta.get('Languages', []):
    lang_code = lang_info['code']
    source_df.rename(columns={'term_localName': 'term_local_name'}, inplace=True)
    source_df.sort_values(by='term_local_name', axis='index', inplace=True, na_position='last')

    patterns = [f"{lang_code}$", 'term_local_name']
    combined_pattern = reduce(lambda x, y: f'{x}|{y}', patterns)
    lang_df = source_df.filter(regex=combined_pattern)

    lang_specific_path = os.path.join(output_dir, f'ltc-{lang_code}-translations.csv')
    lang_df.to_csv(lang_specific_path, index=False, encoding='utf8')

# 4. Merge translations with the main term list
if not os.path.exists(termlist_path):
    print(f"ERROR: Base termlist not found at {termlist_path}. Run terms-transformations first.")
else:
    ltc_df = pd.read_csv(termlist_path, encoding="utf8")

    for lang_info in lang_meta.get('Languages', []):
        lang_code = lang_info['code']
        lang_specific_path = os.path.join(output_dir, f'ltc-{lang_code}-translations.csv')
        translations_df = pd.read_csv(lang_specific_path, encoding='utf8')

        merge_cols = ['term_local_name']
        for col in translations_df.columns:
            if col.endswith(f"_{lang_code}"):
                merge_cols.append(col)

        ltc_df = pd.merge(ltc_df, translations_df[merge_cols], on='term_local_name', how='left')

    # 5. Save the final combined term list
    final_termlist_path = os.path.join(output_dir, 'ltc-translations-termlist.csv')
    ltc_df.to_csv(final_termlist_path, index=False, encoding='utf8')

print("ltc/translation-transformations complete.")