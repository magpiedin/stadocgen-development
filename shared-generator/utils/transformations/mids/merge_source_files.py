import pandas as pd
import os
import csv
import numpy as np

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
levelsFile = os.path.join(output_dir, 'levels.tsv')
infoElFile = os.path.join(output_dir, 'information-elements.tsv')
termsFile = os.path.join(output_dir, 'master-list.tsv')
abcdFile = os.path.join(output_dir, 'mids-abcd-sssom.tsv')
dwcFile = os.path.join(output_dir, 'mids-dwc-sssom.tsv')
mappingsFile = os.path.join(output_dir, 'mappings.tsv')

# --- Main Logic ---
print("Running mids/merge_source_files...")

# 1. Create empty master list if it doesn't exist
if not os.path.exists(termsFile):
    fields = ['namespace','term_local_name','label','definition','usage','notes','examples','rdf_type','term_created','term_modified','compound_name','namespace_iri','term_iri','term_ns_name','term_version_iri','datatype','purpose','alt_label','level']
    with open(termsFile, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fields, delimiter='\t')
        writer.writeheader()

# 2. Merge levels and information elements into master list
df_levels = pd.read_csv(levelsFile, encoding='utf8', sep='\t')
df_infoElements = pd.read_csv(infoElFile, encoding='utf8', sep='\t')
df_terms = pd.read_csv(termsFile, encoding='utf8', sep='\t')

df_terms = pd.concat([df_terms, df_levels])
df_final = pd.concat([df_terms, df_infoElements])
df_final['term_uri'] = 'https://mids.tdwg.org/information-elements/index.html#' + df_final['term_local_name']
df_final.to_csv(termsFile, index=False, encoding='utf8', sep='\t')

# 3. Merge SSSOM Mappings
df_abcd = pd.read_csv(abcdFile, encoding='utf8', sep='\t')
df_dwc = pd.read_csv(dwcFile, encoding='utf8', sep='\t')

if 'sssom_object_source' not in df_dwc:
    df_dwc['sssom_object_source'] = np.nan
if 'sssom_reviewer_id' not in df_abcd:
    df_abcd['sssom_reviewer_id'] = np.nan
if 'sssom_reviewer_label' not in df_abcd:
    df_abcd['sssom_reviewer_label'] = np.nan

df_mappings = pd.concat([df_abcd, df_dwc])
df_mappings.reset_index(inplace=True, drop=True)
df_mappings['term_local_name'] = df_mappings['sssom_subject_id'].str.replace('mids:', '')
df_mappings.insert(0, 'mapping_number', range(1, 1 + len(df_mappings)))
df_mappings.to_csv(mappingsFile, encoding='utf8', sep='\t')

print("mids/merge_source_files complete.")
