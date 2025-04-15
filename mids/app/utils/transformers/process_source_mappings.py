import csv
from config import get_project_root
import pandas as pd
import urllib.request
import shutil

root = get_project_root()

# Mapping source files are stored as *.tsv (tab-delimited). StaDocGen parses CSV when generating documentation. This script converts the source tsv to source csv.
# Files:
dwc_tsv = str(root) + '/mids/app/data/source/mids-repo/sssom_dwc_biology_mappings.sssom.tsv'
dwc_sssom = str(root) + '/mids/app/data/output/mids-dwc-sssom.tsv'
dwc_unique = str(root) + '/mids/app/data/output/mids-dwc-sssom-unique.tsv'

abcd_tsv = str(root) + '/mids/app/data/source/mids-repo/sssom_abcd_biology_mappings.sssom.tsv'
abcd_sssom = str(root) + '/mids/app/data/output/mids-abcd-sssom.tsv'
abcd_unique = str(root) + '/mids/app/data/output/mids-abcd-sssom-unique.tsv'

# ------------------------------------------------------------
# DWC

df_dwc = pd.read_csv(dwc_tsv, encoding='utf8',sep='\t')

# Generate Unique Class-Property Pairs for DWC
df_dwc_mapping = df_dwc[['sssom:subject_category','sssom:subject_id']].drop_duplicates()
df_dwc_mapping.rename(columns={'sssom:subject_id': 'qualified_term',
                    'sssom:subject_category': 'class_name'
                   }, inplace=True)
df_dwc_mapping['term_local_name'] = df_dwc_mapping['qualified_term'].str.replace('mids:', '')
df_dwc_mapping.to_csv(dwc_unique, index=False, encoding='utf8',sep='\t')

# Write new mappings file
df_dwc['object_source_version'] = 'http://rs.tdwg.org/dwc/terms'
# Replace colon in column names with underscores - jinja2 template reserved character
df_dwc.columns = df_dwc.columns.str.replace(':','_', regex=True)
# Create persistent URLs
df_dwc['object_url'] = df_dwc['sssom_object_id'].str.replace('dwc:','http://rs.tdwg.org/dwc/terms/')
df_dwc['subject_url'] = df_dwc['sssom_subject_id'].str.replace('mids:','https://tdwg.github.io/mids/information-elements#')
df_dwc['object_namespace'] = 'dwc'

df_dwc.to_csv(dwc_sssom, index=False, encoding='utf8',sep='\t')

# ------------------------------------------------------------
# ABCD

df_abcd = pd.read_csv(abcd_tsv, encoding="utf8",sep='\t')
# Generate Unique Class-Property Pairs for ABCD
df_abcd_mapping = df_abcd[['sssom:subject_category','sssom:subject_id']].drop_duplicates()
df_abcd_mapping.rename(columns={'sssom:subject_id': 'qualified_term',
                    'sssom:subject_category': 'class_name'
                   }, inplace=True)
df_abcd_mapping['term_local_name'] = df_abcd_mapping['qualified_term'].str.replace('mids:', '')
df_abcd_mapping.to_csv(abcd_unique, index=False, encoding='utf8',sep='\t')

# Write new mappings file
df_abcd['object_source_version'] = 'http://www.tdwg.org/schemas/abcd/2.06'
# Replace colon in column names with underscores - jinja2 template reserved character
df_abcd.columns = df_abcd.columns.str.replace(':','_', regex=True)

df_abcd['object_url'] = df_abcd['sssom_object_id'].str.replace('abcd:','http://rs.tdwg.org/abcd/terms/')
df_abcd['subject_url'] = df_abcd['sssom_subject_id'].str.replace('mids:','https://tdwg.github.io/mids/information-elements#')
df_abcd['object_namespace'] = 'abcd'

df_abcd.to_csv(abcd_sssom, index=False, encoding='utf8',sep='\t')

