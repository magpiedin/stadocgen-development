import pandas as pd
import os
import shutil

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
source_dir = os.path.join(project_root, 'utils', 'sources', 'mids', 'mids-repo')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
source_file_path = os.path.join(source_dir, 'levels.tsv')
target_file_path = os.path.join(output_dir, 'levels.tsv')

# --- Main Logic ---
print("Running mids/levels_transformations...")

# 1. Copy source file
shutil.copy(source_file_path, target_file_path)

# 2. Process Levels data
df = pd.read_csv(target_file_path, encoding="utf8", sep='\t')
df['level'] = df['term_local_name'].str.replace('MIDS', '')
df['pref_label'] = 'MIDS Level ' + df['level']
df['rdf_type'] = 'http://www.w3.org/1999/02/22-rdf-syntax-ns#Class'
df['term_ns_name'] = 'mids:' + df['term_local_name']
df['namespace'] = 'mids:'
df.rename(columns={'notes': 'usage'}, inplace=True)
df.to_csv(target_file_path, index=False, encoding='utf8', sep='\t')

print("mids/levels_transformations complete.")
