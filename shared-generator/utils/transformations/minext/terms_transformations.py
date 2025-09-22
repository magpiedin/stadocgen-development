import pandas as pd
import os
import sys
import shutil
import numpy as np
from datetime import date

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
source_dir = os.path.join(project_root, 'utils', 'sources', 'minext')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
term_src_path = os.path.join(source_dir, 'minext-term-list.csv')
term_dest_path = os.path.join(output_dir, 'minext-termlist.csv')
ns_src_path = os.path.join(source_dir, 'namespaces.csv')
ns_dest_path = os.path.join(output_dir, 'minext-namespaces.csv')
meta_src_path = os.path.join(source_dir, 'metadata-terms.csv')
meta_dest_path = os.path.join(output_dir, 'metadata-terms.csv')
target_dest_path = os.path.join(output_dir, 'minext-target.csv')

# --- Main Logic ---
print("Running minext/terms_transformations...")

# 1. Copy source files
shutil.copy(term_src_path, term_dest_path)
shutil.copy(ns_src_path, ns_dest_path)
shutil.copy(meta_src_path, meta_dest_path)

# 2. Perform Header Validation & Correction
minext_df = pd.read_csv(term_dest_path, encoding="utf8")
if 'VALIDATION_HEADINGS_FILE' in locals():
    headings_file_path = locals()['VALIDATION_HEADINGS_FILE']
    headings_path = os.path.join(project_root, headings_file_path)
    try:
        required_headings_df = pd.read_csv(headings_path, encoding='utf-8-sig')
        required_headings = required_headings_df.iloc[:, 0].tolist()
        current_headings = minext_df.columns.tolist()

        missing_headings = [head for head in required_headings if head not in current_headings]

        if missing_headings:
            print("\nWARNING: The following required headers are missing from the input terms file:")
            for heading in missing_headings:
                print(f"  - {heading}")
                # Add the missing column with empty values
                minext_df[heading] = ""
            print("  - Missing columns have been added with empty values.")

    except FileNotFoundError:
        print(f"WARNING: Validation headings file not found at {headings_path}. Skipping validation.")
    except Exception as e:
        print(f"ERROR: An error occurred during header validation: {e}")
        sys.exit(1)

# 3. Process Terms
minext_df.rename(columns={'term': 'term_local_name', 'organized_in_class': 'class_name'}, inplace=True)
minext_df['compound_name'] = minext_df[["class_name", "term_local_name"]].apply(".".join, axis=1)
minext_df.to_csv(term_dest_path, index=False, encoding='utf8')

# 4. Process Namespaces
ns_df = pd.read_csv(ns_dest_path, encoding="utf8")
ns_df['namespace'] = ns_df['namespace'].astype(str) + ':'
ns_df.to_csv(ns_dest_path, index=False, encoding='utf8')

# 5. Merge Terms and Namespaces
terms_df = pd.read_csv(term_dest_path, encoding="utf8")
minext_df = pd.merge(terms_df, ns_df[['namespace', 'namespace_iri']], on='namespace', how='inner')
minext_df['term_iri'] = minext_df['namespace_iri'].astype(str) + minext_df['term_local_name']
minext_df['term_ns_name'] = minext_df['namespace'].astype(str) + minext_df['term_local_name']
minext_df.to_csv(target_dest_path, index=False, encoding='utf8')

# 6. Final Cleanup
minext_df['term_modified'] = date.today().strftime("%Y-%m-%d")
minext_df['examples'] = minext_df['examples'].str.replace('"', '')
minext_df['definition'] = minext_df['definition'].str.replace('"', '')
minext_df['usage_note'] = minext_df['usage_note'].str.replace('"', '')
minext_df['notes'] = minext_df['notes'].str.replace('"', '')
minext_df['is_required'] = minext_df['is_required'].replace('', np.nan).fillna('False')
minext_df['usage_note'] = minext_df['usage_note'].replace('', np.nan).fillna('')
minext_df.to_csv(term_dest_path, index=False, encoding='utf8')

print("minext/terms_transformations complete.")
