import pandas as pd
import os
import shutil

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
source_dir = os.path.join(project_root, 'utils', 'sources', 'mids', 'mids-repo')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
source_file_path = os.path.join(source_dir, 'information_elements.tsv')
examples_source_path = os.path.join(source_dir, 'examples.tsv')
target_file_path = os.path.join(output_dir, 'information-elements.tsv')
examples_target_path = os.path.join(output_dir, 'examples.tsv')

# --- Main Logic ---
print("Running mids/information_elements_transformations...")

# 1. Copy source files
shutil.copy(source_file_path, target_file_path)
shutil.copy(examples_source_path, examples_target_path)

# 2. Process Information Elements
df = pd.read_csv(target_file_path, encoding="utf8", sep='\t')
df.rename(columns={'MIDSLevel_localName': 'class_name',
                   'informationElement_localName': 'term_local_name',
                   'term_added': 'term_created'}, inplace=True)
df['rdf_type'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Property'
df['term_ns_name'] = 'mids:' + df['term_local_name']
df["term_created"] = pd.to_datetime(df["term_created"], format='%d/%m/%Y')
df["term_modified"] = pd.to_datetime(df["term_modified"], format='%d/%m/%Y')
df['class_pref_label'] = df['class_name'].str.replace('MIDS', 'MIDS Level ')

# 3. Process Examples
df_examples = pd.read_csv(examples_target_path, encoding="utf8", sep='\t')
df_examples.rename(columns={'informationElement_localName': 'term_local_name'}, inplace=True)
df_examples.to_csv(examples_target_path, encoding="utf8", sep='\t', index=False)

# Let pandas auto-detect the line terminator
examples_df = pd.read_csv(examples_target_path, sep='\t', encoding='utf-8')
examples_df = examples_df.replace('\n', ' ', regex=True)
df2 = examples_df.groupby('term_local_name')['example'].apply(list).reset_index(name="examples_list")
df2 = df2[df2['examples_list'].notna()]

# 4. Merge Examples with Information Elements
df_final = pd.merge(df, df2, how="left", on=["term_local_name"])
df_final.to_csv(target_file_path, encoding="utf8", sep='\t', index=False)

print("mids/information_elements_transformations complete.")
