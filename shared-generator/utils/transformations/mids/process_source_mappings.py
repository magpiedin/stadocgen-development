import pandas as pd
import os

# --- Configuration ---
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', '..'))
source_dir = os.path.join(project_root, 'utils', 'sources', 'mids', 'mids-repo')
output_dir = os.path.join(project_root, 'shared-generator', 'app', 'data', 'output')
os.makedirs(output_dir, exist_ok=True)

# --- File Paths ---
dwc_tsv_path = os.path.join(source_dir, 'sssom_dwc_biology_mappings.sssom.tsv')
dwc_sssom_path = os.path.join(output_dir, 'mids-dwc-sssom.tsv')
dwc_unique_path = os.path.join(output_dir, 'mids-dwc-sssom-unique.tsv')

abcd_tsv_path = os.path.join(source_dir, 'sssom_abcd_biology_mappings.sssom.tsv')
abcd_sssom_path = os.path.join(output_dir, 'mids-abcd-sssom.tsv')
abcd_unique_path = os.path.join(output_dir, 'mids-abcd-sssom-unique.tsv')

# --- Main Logic ---
print("Running mids/process_source_mappings...")

# DWC
print("  - Processing DWC mappings...")
df_dwc = pd.read_csv(dwc_tsv_path, encoding='utf8', sep='\t')
df_dwc_mapping = df_dwc[['sssom:subject_category', 'sssom:subject_id']].drop_duplicates()
df_dwc_mapping.rename(columns={'sssom:subject_id': 'qualified_term', 'sssom:subject_category': 'class_name'}, inplace=True)
df_dwc_mapping['term_local_name'] = df_dwc_mapping['qualified_term'].str.replace('mids:', '')
df_dwc_mapping.to_csv(dwc_unique_path, index=False, encoding='utf8', sep='\t')

df_dwc['object_source_version'] = 'http://rs.tdwg.org/dwc/terms'
df_dwc.columns = df_dwc.columns.str.replace(':', '_', regex=True)
df_dwc['object_url'] = df_dwc['sssom_object_id'].str.replace('dwc:', 'http://rs.tdwg.org/dwc/terms/')
df_dwc['subject_url'] = df_dwc['sssom_subject_id'].str.replace('mids:', 'https://tdwg.github.io/mids/information-elements#')
df_dwc['object_namespace'] = 'dwc'
df_dwc.to_csv(dwc_sssom_path, index=False, encoding='utf8', sep='\t')

# ABCD
print("  - Processing ABCD mappings...")
df_abcd = pd.read_csv(abcd_tsv_path, encoding="utf8", sep='\t')
df_abcd_mapping = df_abcd[['sssom:subject_category', 'sssom:subject_id']].drop_duplicates()
df_abcd_mapping.rename(columns={'sssom:subject_id': 'qualified_term', 'sssom:subject_category': 'class_name'}, inplace=True)
df_abcd_mapping['term_local_name'] = df_abcd_mapping['qualified_term'].str.replace('mids:', '')
df_abcd_mapping.to_csv(abcd_unique_path, index=False, encoding='utf8', sep='\t')

df_abcd['object_source_version'] = 'http://www.tdwg.org/schemas/abcd/2.06'
df_abcd.columns = df_abcd.columns.str.replace(':', '_', regex=True)
df_abcd['object_url'] = df_abcd['sssom_object_id'].str.replace('abcd:', 'http://rs.tdwg.org/abcd/terms/')
df_abcd['subject_url'] = df_abcd['sssom_subject_id'].str.replace('mids:', 'https://tdwg.github.io/mids/information-elements#')
df_abcd['object_namespace'] = 'abcd'
df_abcd.to_csv(abcd_sssom_path, index=False, encoding='utf8', sep='\t')

print("mids/process_source_mappings complete.")
