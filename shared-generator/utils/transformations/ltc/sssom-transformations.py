import pandas as pd
import os
import shutil

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
source_dir = os.path.join(project_root, 'utils', 'sources', 'ltc')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
sssom_src_path = os.path.join(source_dir, 'ltc_sssom_mapping.csv')
sssom_dest_path = os.path.join(output_dir, 'ltc-sssom.csv')

# --- Main Transformation Logic ---
print("Running ltc/sssom-transformations...")
shutil.copy(sssom_src_path, sssom_dest_path)

sssom_df = pd.read_csv(sssom_dest_path, encoding='utf8')
sssom_df['term_local_name'] = sssom_df['subject_id']
sssom_df.rename(columns={'term_uri': 'term_iri'}, inplace=True)
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://rs.tdwg.org/ltc/terms/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://purl.org/dc/terms/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://rs.tdwg.org/dwc/terms/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('https://schema.org/', '')
sssom_df['term_local_name'] = sssom_df['term_local_name'].str.replace('http://rs.tdwg.org/chrono/terms/', '')
sssom_df['compound_name'] = sssom_df[["subject_category", "term_local_name"]].apply(".".join, axis=1)
sssom_df['term_iri'] = sssom_df['subject_id']
sssom_df.to_csv(sssom_dest_path, index=False, encoding='utf8')

print("ltc/sssom-transformations complete.")